"""Reproducibility and stale-artifact regression tests for Cold Storage epistemic build."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COLD = ROOT / "adventures" / "The_Cold_Storage_Alarm"
ADV = COLD / "adventure"
EP_PKG = ADV / "DO_NOT_READ" / "epistemic_progression_package.json"
BUILD_SCRIPT = ROOT / "scripts" / "build_cold_storage_epistemic.py"

LOST_SUBTREES = (
    "UNIT-ALARM-HISTORY",
    "UNIT-BADGE-ARCHIVE-MENU",
    "UNIT-BADGE-COLD-ENTRY",
    "UNIT-BADGE-CONTROL-ENTRY",
    "UNIT-CHK-LOCKER-DECL",
    "UNIT-DOCK-VIEW",
    "UNIT-EXIT-SCAN",
    "UNIT-LOCKER-MENU",
    "UNIT-MANIFEST-GAP",
    "UNIT-MANIFEST-MENU",
    "UNIT-POD-CROSSREF",
)

CHECK_RESULT_TEMPLATES = (
    "UNIT-LOCKER-SUCCESS",
    "UNIT-LOCKER-FAIL",
    "UNIT-LABEL-SUCCESS",
    "UNIT-LABEL-FAIL",
    "UNIT-LATCH-SUCCESS",
    "UNIT-LATCH-FAIL",
    "UNIT-TREND-SUCCESS",
    "UNIT-TREND-FAIL",
)


def _load_committed_package() -> dict:
    return json.loads(EP_PKG.read_text(encoding="utf-8"))


def _regenerate_events() -> list[dict]:
    sys.path.insert(0, str(ROOT))
    from scripts.build_cold_storage_epistemic import _load_manifest, build_epistemic_events

    return build_epistemic_events(_load_manifest())


def _template_destinations(package: dict, template_id: str) -> set[str]:
    dests: set[str] = set()
    for event in package.get("playable_events") or []:
        tpl = event.get("template_unit_id") or event.get("unit_id", "")
        if tpl.split("--S-")[0] != template_id:
            continue
        for action in event.get("structured_actions") or []:
            dest = str(action.get("destination_unit_id", "")).split("--S-")[0]
            if dest:
                dests.add(dest)
    return dests


def _has_inbound_edge(package: dict, template_id: str) -> bool:
    for event in package.get("playable_events") or []:
        for action in event.get("structured_actions") or []:
            dest = str(action.get("destination_unit_id", "")).split("--S-")[0]
            if dest == template_id:
                return True
    return False


@unittest.skipUnless(COLD.exists(), "Cold Storage adventure not present")
class TestColdStorageEpistemicReproducibility(unittest.TestCase):
    def test_build_script_has_no_git_history_dependency(self):
        source = BUILD_SCRIPT.read_text(encoding="utf-8")
        self.assertNotIn("git show", source)
        self.assertNotIn("_load_canonical_choice_map", source)
        self.assertNotIn("_guess_dest", source)

    def test_unresolved_non_self_loop_raises(self):
        from idne.epistemic_progression.template_navigation import (
            UnresolvedDestinationError,
            resolve_template_destination,
        )

        choice_map = {("UNIT-TEST", "go somewhere"): ("UNIT-OTHER", "nav")}
        with self.assertRaises(UnresolvedDestinationError):
            resolve_template_destination("UNIT-TEST", "unknown choice", choice_map)
        with self.assertRaises(UnresolvedDestinationError):
            resolve_template_destination(
                "UNIT-TEST",
                "go somewhere",
                {("UNIT-TEST", "go somewhere"): ("UNIT-TEST", "nav")},
            )

    def test_double_generation_produces_identical_structural_digest(self):
        from idne.epistemic_progression.template_navigation import template_navigation_digest

        first = _regenerate_events()
        second = _regenerate_events()
        self.assertEqual(
            template_navigation_digest(first),
            template_navigation_digest(second),
        )

    def test_committed_package_matches_regeneration(self):
        from idne.epistemic_progression.template_navigation import epistemic_package_digest

        committed = epistemic_package_digest(_load_committed_package())
        events = _regenerate_events()
        sys.path.insert(0, str(ROOT))
        from scripts.build_cold_storage_epistemic import write_epistemic_package

        write_epistemic_package(events)
        regenerated = epistemic_package_digest(_load_committed_package())
        self.assertEqual(committed, regenerated)

    def test_eleven_previously_lost_subtrees_are_reachable(self):
        pkg = _load_committed_package()
        missing = [tpl for tpl in LOST_SUBTREES if not _has_inbound_edge(pkg, tpl)]
        self.assertEqual(missing, [], f"Unreachable template subtrees: {missing}")

    def test_check_result_supplemental_templates_are_reachable(self):
        pkg = _load_committed_package()
        missing = [tpl for tpl in CHECK_RESULT_TEMPLATES if not _has_inbound_edge(pkg, tpl)]
        self.assertEqual(missing, [], f"Unreachable check result templates: {missing}")

    def test_security_archive_and_alarm_routes(self):
        pkg = _load_committed_package()
        sec_dests = _template_destinations(pkg, "UNIT-SECURITY-BASE")
        self.assertIn("UNIT-ALARM-HISTORY", sec_dests)
        self.assertIn("UNIT-BADGE-ARCHIVE-MENU", sec_dests)
        self.assertIn("UNIT-DOCK-BASE", sec_dests)
        self.assertIn("UNIT-BREAK-BASE", sec_dests)

    def test_manager_manifest_and_pod_routes(self):
        pkg = _load_committed_package()
        mgr_dests = _template_destinations(pkg, "UNIT-MANAGER-BASE")
        self.assertIn("UNIT-MANIFEST-MENU", mgr_dests)
        manifest_dests = _template_destinations(pkg, "UNIT-MANIFEST-MENU")
        self.assertIn("UNIT-MANIFEST-GAP", manifest_dests)
        self.assertIn("UNIT-POD-CROSSREF", manifest_dests)

    def test_locker_declaration_and_menu_routes(self):
        pkg = _load_committed_package()
        break_dests = _template_destinations(pkg, "UNIT-BREAK-BASE")
        self.assertIn("UNIT-LOCKER-MENU", break_dests)
        self.assertIn("UNIT-DOCK-VIEW", break_dests)
        locker_dests = _template_destinations(pkg, "UNIT-LOCKER-MENU")
        self.assertIn("UNIT-CHK-LOCKER-DECL", locker_dests)

    def test_opening_still_has_exactly_three_choices(self):
        pkg = _load_committed_package()
        dock = next(
            e for e in pkg["playable_events"] if e.get("unit_id") == "UNIT-DOCK-BASE"
        )
        labels = [a["label"] for a in dock.get("structured_actions") or []]
        self.assertEqual(len(labels), 3)
        self.assertIn("Talk to Elena Morales.", labels)
        self.assertIn("Walk through the dock corridor to the cold storage hall.", labels)
        self.assertIn("Talk to a dock worker.", labels)

    def test_stale_artifact_detection_via_subprocess_build(self):
        """Running the build script must not change the structural digest."""
        from idne.epistemic_progression.template_navigation import epistemic_package_digest

        before = epistemic_package_digest(_load_committed_package())
        subprocess.run(
            [sys.executable, str(BUILD_SCRIPT)],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        after = epistemic_package_digest(_load_committed_package())
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
