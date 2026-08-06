"""Tests for static gamebook navigation."""

from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from idne.gamebook_nav.build import build_gamebook_package
from idne.gamebook_nav.numbering import assign_public_sections
from idne.gamebook_nav.validate import validate_gamebook_navigation
from idne.gamebook_validate import requires_static_gamebook, validate_gamebook
from idne.validate_adventure.runner import validate_adventure

FIXTURES = Path(__file__).resolve().parent / "fixtures"
MINIMAL = FIXTURES / "gamebook_minimal"
COLD = Path(__file__).resolve().parents[1] / "adventures" / "The_Cold_Storage_Alarm"


class TestGamebookNav(unittest.TestCase):
    def test_numbering_is_deterministic_and_scrambled(self):
        units = ["UNIT-A", "UNIT-B", "UNIT-C", "UNIT-D"]
        first = assign_public_sections(units, "demo-adventure")
        second = assign_public_sections(units, "demo-adventure")
        self.assertEqual(first, second)
        self.assertEqual(len(set(first.values())), len(units))
        self.assertTrue(all(101 <= n <= 999 for n in first.values()))
        self.assertNotEqual(sorted(first.values()), sorted(units))

    def test_numbering_retains_existing_assignments(self):
        existing = {"UNIT-A": 111, "UNIT-B": 222}
        out = assign_public_sections(["UNIT-A", "UNIT-B", "UNIT-C"], "demo", existing_map=existing)
        self.assertEqual(out["UNIT-A"], 111)
        self.assertEqual(out["UNIT-B"], 222)
        self.assertNotIn(out["UNIT-C"], (111, 222))

    def test_validate_detects_duplicate_sections(self):
        manifest = {
            "units": {"UNIT-A": {}, "UNIT-B": {}},
            "public_sections": {"UNIT-A": 101, "UNIT-B": 101},
            "static_book": {"start_unit_id": "UNIT-A", "delivery_mode": "static_book"},
        }
        res = validate_gamebook_navigation(MINIMAL / "adventure", manifest=manifest, section_map=manifest["public_sections"])
        self.assertEqual(res.checks.get("GB-DUPLICATE"), "FAIL")

    def test_build_minimal_gamebook(self):
        ws = Path(tempfile.mkdtemp(prefix="gb_min_"))
        shutil.copytree(MINIMAL, ws / "gamebook_minimal")
        root = ws / "gamebook_minimal" / "adventure"
        result = build_gamebook_package(root, start_unit_id="UNIT-DOCK-BASE")
        self.assertEqual(result["validation"]["status"], "PASS")
        gamebook = (root / "PLAYER" / "GAMEBOOK.md").read_text(encoding="utf-8")
        self.assertIn("Starting section:", gamebook)
        self.assertIn("Turn to section", gamebook)
        manifest = json.loads((ws / "gamebook_minimal" / "player_mapping_manifest.json").read_text())
        self.assertEqual(manifest["schema_version"], "1.1")
        self.assertIn("static_book", manifest)

    def test_integrated_validator_skips_without_static_book_declaration(self):
        if not (FIXTURES / "gen_v2_canonical_solo").exists():
            self.skipTest("fixture missing")
        res = validate_adventure(FIXTURES / "gen_v2_canonical_solo")
        self.assertNotIn("gamebook", res.validators)

    def test_gamebook_validator_requires_declaration(self):
        res = validate_gamebook(MINIMAL / "adventure")
        self.assertEqual(res.status, "SKIP")

    @unittest.skipUnless(COLD.exists(), "Cold Storage adventure not present")
    def test_cold_storage_gamebook_build_passes(self):
        ws = Path(tempfile.mkdtemp(prefix="gb_cold_"))
        shutil.copytree(COLD, ws / "The_Cold_Storage_Alarm")
        root = ws / "The_Cold_Storage_Alarm" / "adventure"
        result = build_gamebook_package(root, adventure_id="The_Cold_Storage_Alarm")
        self.assertEqual(result["section_count"], 105)
        self.assertEqual(result["validation"]["status"], "PASS")
        self.assertTrue(requires_static_gamebook(root))
        gb = validate_gamebook(root)
        self.assertEqual(gb.status, "PASS")


if __name__ == "__main__":
    unittest.main()
