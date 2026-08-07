"""Tests for structured player delivery and offline player artifacts."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from idne.gamebook_nav.build import build_gamebook_package
from idne.gamebook_nav.player_json import scan_forbidden_player_data
from idne.player_delivery_validate import (
    validate_player_delivery,
    validate_player_gamebook_determinism,
    validate_player_gamebook_payload,
)

FIXTURES = Path(__file__).resolve().parent / "fixtures"
MINIMAL = FIXTURES / "gamebook_minimal"
REPO = Path(__file__).resolve().parents[1]
ADVENTURES = REPO / "adventures"

ENGLISH_ADVENTURE_PACK = (
    "The_Cold_Storage_Alarm",
    "The_Harbor_Light_Signal",
    "The_Gallery_Verdict",
    "The_Quarry_Silence",
    "The_Parish_Ledger",
)


def _adventure_root(adventure_id: str) -> Path:
    return ADVENTURES / adventure_id / "adventure"


def _ensure_player_gamebook(adventure_id: str) -> Path:
    root = _adventure_root(adventure_id)
    gamebook_path = root / "PLAYER" / "gamebook.json"
    if gamebook_path.exists():
        return gamebook_path
    manifest_path = ADVENTURES / adventure_id / "player_mapping_manifest.json"
    start_unit = None
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        start_unit = (manifest.get("static_book") or {}).get("start_unit_id")
    if start_unit:
        build_gamebook_package(root, start_unit_id=start_unit)
    else:
        build_gamebook_package(root)
    return gamebook_path


class TestPlayerDelivery(unittest.TestCase):
    def test_build_minimal_player_gamebook(self):
        ws = Path(tempfile.mkdtemp(prefix="pd_min_"))
        shutil.copytree(MINIMAL, ws / "gamebook_minimal")
        root = ws / "gamebook_minimal" / "adventure"
        result = build_gamebook_package(root, start_unit_id="UNIT-DOCK-BASE")
        self.assertEqual(result["player_delivery_validation"]["status"], "PASS")
        payload = json.loads((root / "PLAYER" / "gamebook.json").read_text(encoding="utf-8"))
        self.assertEqual(payload["schema_version"], "1.0")
        self.assertIn(str(payload["start_section"]), payload["sections"])
        self.assertEqual(scan_forbidden_player_data(payload), [])

    def test_player_validation_detects_dangling_target(self):
        payload = {
            "schema_version": "1.0",
            "adventure_id": "demo",
            "title": "Demo",
            "delivery_mode": "static_book",
            "opening": "Hello",
            "start_section": 101,
            "section_count": 1,
            "sections": {
                "101": {
                    "section": 101,
                    "title": "Start",
                    "body": "Body",
                    "choices": [{"label": "Go", "target_section": 999, "kind": "nav"}],
                }
            },
        }
        res = validate_player_gamebook_payload(payload)
        self.assertEqual(res.status, "FAIL")
        self.assertEqual(res.checks["PD-TARGETS"], "FAIL")

    def test_player_build_is_deterministic(self):
        ws = Path(tempfile.mkdtemp(prefix="pd_det_"))
        shutil.copytree(MINIMAL, ws / "gamebook_minimal")
        root = ws / "gamebook_minimal" / "adventure"
        build_gamebook_package(root, start_unit_id="UNIT-DOCK-BASE")
        first = json.loads((root / "PLAYER" / "gamebook.json").read_text(encoding="utf-8"))
        build_gamebook_package(root, start_unit_id="UNIT-DOCK-BASE")
        second = json.loads((root / "PLAYER" / "gamebook.json").read_text(encoding="utf-8"))
        res = validate_player_gamebook_determinism(first, second)
        self.assertEqual(res.status, "PASS")

    def test_five_english_adventures_discoverable_in_checkout(self):
        missing = [
            adventure_id
            for adventure_id in ENGLISH_ADVENTURE_PACK
            if not (ADVENTURES / adventure_id / "player_mapping_manifest.json").exists()
        ]
        self.assertEqual(missing, [], f"missing adventures on checkout: {missing}")

    def test_five_english_adventures_player_delivery_passes(self):
        for adventure_id in ENGLISH_ADVENTURE_PACK:
            root = _adventure_root(adventure_id)
            self.assertTrue(root.exists(), adventure_id)
            _ensure_player_gamebook(adventure_id)
            res = validate_player_delivery(root)
            self.assertEqual(res.status, "PASS", f"{adventure_id}: {res.errors}")

    def test_player_package_does_not_reference_other_git_branches(self):
        runtime_files = [
            REPO / "scripts" / "build_offline_player_package.py",
            REPO / "idne_player" / "js" / "player.js",
        ]
        forbidden = (
            "four-adventure-integration",
            "git archive",
            "git show",
            "INTEGRATION_BRANCH",
        )
        for path in runtime_files:
            text = path.read_text(encoding="utf-8")
            for token in forbidden:
                self.assertNotIn(token, text, f"{path.name} must not depend on {token}")

    def test_no_reverse_dependency_on_player_delivery_artifacts(self):
        """Canonical/epistemic generation must not read generated player delivery outputs."""
        upstream_files = [
            REPO / "idne" / "adventure_pack" / "canonical.py",
            REPO / "idne" / "adventure_pack" / "epistemic.py",
        ]
        upstream_files.extend(sorted((REPO / "idne" / "epistemic_progression").glob("*.py")))
        upstream_files = [
            path for path in upstream_files
            if path.exists() and not path.name.endswith("_validate.py")
        ]
        forbidden_reads = (
            "player_mapping_manifest.json",
            "PLAYER/gamebook.json",
            "PLAYER/GAMEBOOK.md",
        )
        offenders: list[str] = []
        for path in upstream_files:
            text = path.read_text(encoding="utf-8")
            for token in forbidden_reads:
                if token in text:
                    offenders.append(f"{path.relative_to(REPO)} reads {token}")
        self.assertEqual(offenders, [], offenders)

    def test_distant_navigation_target_exists(self):
        ws = Path(tempfile.mkdtemp(prefix="pd_dist_"))
        shutil.copytree(MINIMAL, ws / "gamebook_minimal")
        root = ws / "gamebook_minimal" / "adventure"
        build_gamebook_package(root, start_unit_id="UNIT-DOCK-BASE")
        payload = json.loads((root / "PLAYER" / "gamebook.json").read_text(encoding="utf-8"))
        start = str(payload["start_section"])
        far_target = None
        for choice in payload["sections"][start]["choices"]:
            if choice["target_section"] != payload["start_section"]:
                far_target = str(choice["target_section"])
                break
        self.assertIsNotNone(far_target)
        self.assertIn(far_target, payload["sections"])

    def test_offline_package_includes_five_english_adventures(self):
        out = Path(tempfile.mkdtemp(prefix="pd_dist_"))
        workspaces = [ADVENTURES / adventure_id for adventure_id in ENGLISH_ADVENTURE_PACK]
        for adventure_id in ENGLISH_ADVENTURE_PACK:
            _ensure_player_gamebook(adventure_id)
        subprocess.run(
            [
                sys.executable,
                str(REPO / "scripts" / "build_offline_player_package.py"),
                "--output",
                str(out),
                *map(str, workspaces),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        index = json.loads(
            (out / "library" / "index.js").read_text(encoding="utf-8").split("=", 1)[1].strip().rstrip(";")
        )
        bundled_ids = {entry["id"] for entry in index}
        self.assertEqual(bundled_ids, set(ENGLISH_ADVENTURE_PACK))
        for adventure_id in ENGLISH_ADVENTURE_PACK:
            self.assertTrue((out / "library" / "adventures" / f"{adventure_id}.js").exists())


if __name__ == "__main__":
    unittest.main()
