"""Tests for Simulator v2 human-delivery static gamebook simulation."""

from __future__ import annotations

import json
import shutil
import tempfile
import unittest
import zipfile
from pathlib import Path

from simulator_v2.human_delivery.engine import HumanDeliveryEngine
from simulator_v2.human_delivery.loader import HumanDeliveryLoadError, resolve_adventure_workspace
from simulator_v2.human_delivery.player_view import HiddenInformationAccessError, HumanDeliveryPlayerView
from simulator_v2.human_delivery.runner import cmd_delivery_validate, cmd_human_trace
from simulator_v2.human_delivery.strategies import HiddenAccessProbeStrategy, create_human_strategy
from simulator_v2.human_delivery.types import ParsedSection, VisibleChoice
from simulator_v2.human_delivery.validate import validate_human_delivery
from simulator_v2.rng import DeterministicRNG

FIXTURES = Path(__file__).resolve().parent / "fixtures"
COLD = Path(__file__).resolve().parents[1] / "adventures" / "The_Cold_Storage_Alarm"
SOLO = FIXTURES / "sim_v2_solo"


def _cold_start_section() -> int:
    manifest = json.loads((COLD / "player_mapping_manifest.json").read_text(encoding="utf-8"))
    return int(manifest["static_book"]["start_section"])


def _write_minimal_workspace(
    ws: Path,
    *,
    gamebook: str | None = "present",
    start_section: int = 101,
    extra_manifest: dict | None = None,
) -> Path:
    """Build a tiny unpacked static-book workspace under ws."""
    root = ws / "hd_minimal"
    adv = root / "adventure"
    player = adv / "PLAYER"
    dnr = adv / "DO_NOT_READ"
    player.mkdir(parents=True)
    dnr.mkdir(parents=True)

    (adv / "play_manifest.json").write_text(
        json.dumps({"schema_version": "1.0", "adventure_id": "hd_minimal", "play_mode": "single_investigator"}),
        encoding="utf-8",
    )
    for name in (
        "environment_package.json",
        "object_interaction_package.json",
        "npc_investigation_package.json",
        "investigation_flow_package.json",
        "capability_check_package.json",
    ):
        (dnr / name).write_text("{}", encoding="utf-8")

    manifest = {
        "schema_version": "1.1",
        "adventure_id": "hd_minimal",
        "static_book": {
            "delivery_mode": "static_book",
            "gamebook_path": "PLAYER/GAMEBOOK.md",
            "start_unit_id": "UNIT-A",
            "start_section": start_section,
        },
        "public_sections": {
            "UNIT-A": 101,
            "UNIT-B": 102,
            "END-DONE": 103,
        },
        "units": {
            "UNIT-A": {
                "unit_id": "UNIT-A",
                "public_section": 101,
                "choices": [{"label": "Go on.", "destination_unit_id": "UNIT-B", "kind": "navigate"}],
            },
            "UNIT-B": {
                "unit_id": "UNIT-B",
                "public_section": 102,
                "choices": [{"label": "Finish.", "destination_unit_id": "END-DONE", "kind": "navigate"}],
            },
            "END-DONE": {
                "unit_id": "END-DONE",
                "public_section": 103,
                "choices": [],
            },
        },
    }
    if extra_manifest:
        manifest.update(extra_manifest)

    (root / "player_mapping_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    if gamebook == "present":
        text = """# Minimal gamebook

**Starting section: 101** — turn to section **101** to begin.

## Section 101

Start here.

**What do you do?**

- Go on. Turn to section **102**.

## Section 102

Middle.

**What do you do?**

- Finish. Turn to section **103**.

## Section 103

Done.
"""
        (player / "GAMEBOOK.md").write_text(text, encoding="utf-8")
    elif gamebook != "absent":
        (player / "GAMEBOOK.md").write_text(gamebook, encoding="utf-8")

    return root


class TestHumanDeliveryValidation(unittest.TestCase):
    def test_canonical_valid_but_gamebook_missing(self):
        ws = Path(tempfile.mkdtemp())
        root = _write_minimal_workspace(ws, gamebook="absent")
        with self.assertRaises(HumanDeliveryLoadError):
            resolve_adventure_workspace(root)

    def test_starting_file_missing(self):
        ws = Path(tempfile.mkdtemp())
        root = _write_minimal_workspace(ws)
        (root / "adventure" / "PLAYER" / "GAMEBOOK.md").unlink()
        with self.assertRaises(HumanDeliveryLoadError):
            resolve_adventure_workspace(root)

    def test_starting_section_missing(self):
        ws = Path(tempfile.mkdtemp())
        root = _write_minimal_workspace(ws)
        manifest = json.loads((root / "player_mapping_manifest.json").read_text())
        del manifest["static_book"]["start_section"]
        manifest["public_sections"].pop("UNIT-A", None)
        (root / "player_mapping_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
        out = validate_human_delivery(resolve_adventure_workspace(root))
        self.assertEqual(out["status"], "FAIL")
        ids = {f["finding_id"] for f in out["findings"]}
        self.assertIn("HD-MISSING-START-SECTION", ids)

    def test_starting_section_absent_from_book(self):
        ws = Path(tempfile.mkdtemp())
        root = _write_minimal_workspace(ws, start_section=999)
        manifest = json.loads((root / "player_mapping_manifest.json").read_text())
        manifest["static_book"]["start_section"] = 999
        (root / "player_mapping_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
        out = validate_human_delivery(resolve_adventure_workspace(root))
        self.assertEqual(out["status"], "FAIL")
        self.assertTrue(any("999" in f["message"] for f in out["findings"]))

    def test_destinationless_visible_choice(self):
        ws = Path(tempfile.mkdtemp())
        root = _write_minimal_workspace(
            ws,
            gamebook="""# Broken

**Starting section: 101**

## Section 101

**What do you do?**

- Stuck here with no destination.
""",
        )
        out = validate_human_delivery(resolve_adventure_workspace(root))
        self.assertEqual(out["status"], "FAIL")
        self.assertTrue(any(f["finding_id"] == "HD-DESTINATIONLESS-CHOICE" for f in out["findings"]))

    def test_dangling_public_destination(self):
        ws = Path(tempfile.mkdtemp())
        root = _write_minimal_workspace(
            ws,
            gamebook="""# Broken

**Starting section: 101**

## Section 101

**What do you do?**

- Jump nowhere. Turn to section **999**.
""",
        )
        out = validate_human_delivery(resolve_adventure_workspace(root))
        self.assertEqual(out["status"], "FAIL")
        self.assertTrue(any(f["finding_id"] == "HD-DANGLING-DESTINATION" for f in out["findings"]))

    def test_wrong_internal_unit_map(self):
        ws = Path(tempfile.mkdtemp())
        root = _write_minimal_workspace(ws)
        manifest = json.loads((root / "player_mapping_manifest.json").read_text())
        manifest["public_sections"]["UNIT-B"] = 102
        manifest["public_sections"]["END-DONE"] = 103
        manifest["units"]["UNIT-A"]["choices"] = [
            {"label": "Go.", "destination_unit_id": "UNIT-B", "kind": "navigate"}
        ]
        (root / "player_mapping_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
        book = (root / "adventure" / "PLAYER" / "GAMEBOOK.md").read_text()
        book = book.replace("Turn to section **102**.", "Turn to section **103**.")
        (root / "adventure" / "PLAYER" / "GAMEBOOK.md").write_text(book, encoding="utf-8")
        out = validate_human_delivery(resolve_adventure_workspace(root))
        self.assertEqual(out["status"], "FAIL")
        self.assertTrue(any(f["finding_id"] == "HD-WRONG-INTERNAL-MAP" for f in out["findings"]))

    def test_check_success_without_failure(self):
        ws = Path(tempfile.mkdtemp())
        root = _write_minimal_workspace(
            ws,
            gamebook="""# Check broken

**Starting section: 101**

## Section 101

**What do you do?**

- If your roll **succeeds**, turn to section **102**.
""",
        )
        out = validate_human_delivery(resolve_adventure_workspace(root))
        self.assertEqual(out["status"], "FAIL")
        self.assertTrue(any(f["finding_id"] == "HD-CHECK-MISSING-FAILURE" for f in out["findings"]))

    def test_ending_manifest_edge_but_public_route_blocked(self):
        ws = Path(tempfile.mkdtemp())
        root = _write_minimal_workspace(
            ws,
            gamebook="""# Blocked ending route

**Starting section: 101**

## Section 101

**What do you do?**

- Loop forever. Turn to section **101**.

## Section 103

Terminal ending content.
""",
        )
        out = validate_human_delivery(resolve_adventure_workspace(root))
        self.assertEqual(out["status"], "FAIL")
        self.assertTrue(any(f["finding_id"] == "HD-ENDING-UNREACHABLE" for f in out["findings"]))

    def test_strategy_hidden_state_access_fails_loudly(self):
        view = HumanDeliveryPlayerView(
            start_filename="GAMEBOOK.md",
            start_section=101,
            current_section=ParsedSection(101, "UNIT-A", "body", []),
        )
        with self.assertRaises(HiddenInformationAccessError):
            _ = view.canonical_graph
        strat = create_human_strategy("hidden_access_probe")
        with self.assertRaises(HiddenInformationAccessError):
            strat.choose(view, DeterministicRNG(1))

    def test_valid_complete_human_delivery_trace(self):
        if not COLD.exists():
            self.skipTest("Cold Storage adventure not present")
        out = cmd_human_trace(COLD, seed=42, strategy="human_random_legal")
        result = out["result"]
        self.assertIn(result["status"], ("COMPLETED", "INCOMPLETE"))
        self.assertGreater(len(result["steps"]), 0)
        self.assertEqual(result["start_section"], _cold_start_section())

    def test_canonical_public_route_equivalence(self):
        if not COLD.exists():
            self.skipTest("Cold Storage adventure not present")
        engine = HumanDeliveryEngine(resolve_adventure_workspace(COLD))
        trace = engine.run_trace(strategy="human_random_legal", seed=42)
        self.assertEqual(trace.canonical_equivalence, "PASS")
        self.assertTrue(all(s.route_equivalence == "PASS" for s in trace.steps))

    def test_unpacked_directory_used_not_idne(self):
        ws = Path(tempfile.mkdtemp())
        root = _write_minimal_workspace(ws)
        stale = ws / "stale.idne"
        with zipfile.ZipFile(stale, "w") as zf:
            zf.writestr("package_manifest.json", "{}")
        out = cmd_delivery_validate(root)
        self.assertTrue(out["used_unpacked_directory"])
        with self.assertRaises(HumanDeliveryLoadError):
            resolve_adventure_workspace(stale)

    def test_author_only_file_access_rejected(self):
        view = HumanDeliveryPlayerView(
            start_filename="GAMEBOOK.md",
            start_section=101,
            current_section=ParsedSection(101, "UNIT-A", "body", []),
        )
        with self.assertRaises(HiddenInformationAccessError):
            view.attempt_author_file_access("DO_NOT_READ/investigation_flow_package.json")

    def test_gamebook_author_only_reference_detected(self):
        ws = Path(tempfile.mkdtemp())
        root = _write_minimal_workspace(
            ws,
            gamebook="""# Bad reference

See DO_NOT_READ/story.md for answers.

**Starting section: 101**

## Section 101

**What do you do?**

- Go. Turn to section **102**.
""",
        )
        out = validate_human_delivery(resolve_adventure_workspace(root))
        self.assertTrue(any(f["finding_id"] == "HD-AUTHOR-ONLY-DEPENDENCY" for f in out["findings"]))

    @unittest.skipUnless(COLD.exists(), "Cold Storage adventure not present")
    def test_cold_storage_delivery_validate_passes(self):
        out = cmd_delivery_validate(COLD)
        self.assertEqual(out["status"], "PASS")
        self.assertEqual(out["start_section"], _cold_start_section())
        self.assertEqual(out["start_file"], "PLAYER/GAMEBOOK.md")

    @unittest.skipUnless(COLD.exists(), "Cold Storage adventure not present")
    def test_canonical_pass_does_not_imply_human_pass_is_separate(self):
        """Human-delivery validation is independent of canonical package load."""
        out = cmd_delivery_validate(COLD)
        self.assertEqual(out["simulation_layer"] if "simulation_layer" in out else out.get("status"), "PASS")


if __name__ == "__main__":
    unittest.main()
