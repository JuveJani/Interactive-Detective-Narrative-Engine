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
from idne.gamebook_nav.player_json import build_player_gamebook, scan_forbidden_player_data
from idne.player_delivery_validate import (
    validate_player_delivery,
    validate_player_gamebook_determinism,
    validate_player_gamebook_payload,
)

FIXTURES = Path(__file__).resolve().parent / "fixtures"
MINIMAL = FIXTURES / "gamebook_minimal"
COLD = Path(__file__).resolve().parents[1] / "adventures" / "The_Cold_Storage_Alarm"
HUTOR = Path(__file__).resolve().parents[1] / "adventures" / "A_Hutoriasztas"
INTEGRATION_BRANCH = "origin/cursor/four-adventure-integration-aa1a"
FOUR_ADVENTURES = (
    "The_Gallery_Verdict",
    "The_Harbor_Light_Signal",
    "The_Parish_Ledger",
    "The_Quarry_Silence",
)


def _extract_adventure_from_git(adventure_id: str, dest: Path) -> Path | None:
    repo = Path(__file__).resolve().parents[1]
    branch = INTEGRATION_BRANCH
    verify = subprocess.run(
        ["git", "rev-parse", "--verify", branch],
        cwd=repo,
        capture_output=True,
    )
    if verify.returncode != 0:
        return None
    archive = subprocess.run(
        ["git", "archive", branch, f"adventures/{adventure_id}"],
        cwd=repo,
        capture_output=True,
        check=True,
    )
    extract = subprocess.run(
        ["tar", "-x", "-C", str(dest)],
        input=archive.stdout,
        capture_output=True,
        check=True,
    )
    if extract.returncode != 0:
        return None
    workspace = dest / "adventures" / adventure_id
    if not workspace.exists():
        workspace = dest / adventure_id
    if not (workspace / "player_mapping_manifest.json").exists():
        return None
    root = workspace / "adventure"
    gamebook_path = root / "PLAYER" / "gamebook.json"
    if not gamebook_path.exists():
        manifest = json.loads((workspace / "player_mapping_manifest.json").read_text(encoding="utf-8"))
        start_unit = (manifest.get("static_book") or {}).get("start_unit_id")
        build_gamebook_package(root, start_unit_id=start_unit) if start_unit else build_gamebook_package(root)
    return workspace if gamebook_path.exists() else None


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

    @unittest.skipUnless(COLD.exists(), "Cold Storage adventure not present")
    def test_cold_storage_player_delivery_passes(self):
        root = COLD / "adventure"
        gamebook_path = root / "PLAYER" / "gamebook.json"
        if not gamebook_path.exists():
            build_gamebook_package(root)
        res = validate_player_delivery(root)
        self.assertEqual(res.status, "PASS", res.errors)
        payload = json.loads(gamebook_path.read_text(encoding="utf-8"))
        self.assertGreater(payload["section_count"], 4000)

    @unittest.skipUnless(HUTOR.exists(), "Hungarian mirror not present")
    def test_hungarian_mirror_player_delivery_passes(self):
        root = HUTOR / "adventure"
        gamebook_path = root / "PLAYER" / "gamebook.json"
        if not gamebook_path.exists():
            build_gamebook_package(root)
        res = validate_player_delivery(root)
        self.assertEqual(res.status, "PASS", res.errors)

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

    def test_offline_package_builder(self):
        ws = Path(tempfile.mkdtemp(prefix="pd_pkg_"))
        shutil.copytree(MINIMAL, ws / "gamebook_minimal")
        root = ws / "gamebook_minimal" / "adventure"
        build_gamebook_package(root, start_unit_id="UNIT-DOCK-BASE")
        out = Path(tempfile.mkdtemp(prefix="pd_dist_"))
        repo = Path(__file__).resolve().parents[1]
        subprocess.run(
            [
                sys.executable,
                str(repo / "scripts" / "build_offline_player_package.py"),
                "--output",
                str(out),
                str(ws / "gamebook_minimal"),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertTrue((out / "index.html").exists())
        self.assertTrue((out / "library" / "index.js").exists())
        index = (out / "library" / "index.js").read_text(encoding="utf-8")
        self.assertIn("IDNE_LIBRARY", index)

    @unittest.skipUnless(
        subprocess.run(["git", "rev-parse", "--verify", INTEGRATION_BRANCH], capture_output=True).returncode == 0,
        "four-adventure integration branch unavailable",
    )
    def test_four_generated_adventures_player_delivery(self):
        temp = Path(tempfile.mkdtemp(prefix="pd_four_"))
        opened = 0
        for adventure_id in FOUR_ADVENTURES:
            workspace = _extract_adventure_from_git(adventure_id, temp)
            if not workspace:
                continue
            root = workspace / "adventure"
            gamebook_path = root / "PLAYER" / "gamebook.json"
            if not gamebook_path.exists():
                build_gamebook_package(root)
            res = validate_player_delivery(root)
            self.assertEqual(res.status, "PASS", f"{adventure_id}: {res.errors}")
            opened += 1
        self.assertEqual(opened, 4, "expected four generated adventures from integration branch")


if __name__ == "__main__":
    unittest.main()
