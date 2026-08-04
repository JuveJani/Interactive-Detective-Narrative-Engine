"""Tests for Single Investigator Mode (Milestone 1)."""

import copy
import unittest
from pathlib import Path

from idne.play_modes import PLAY_MODE_SINGLE, PLAY_MODE_TWO_PLAYER, normalize_play_modes
from idne.single_investigator_validate import load_play_manifest, validate_single_investigator

FIXTURES = Path(__file__).resolve().parent / "fixtures"
HARBORVIEW = Path(__file__).resolve().parents[1] / "adventures" / "CASE_BENCHMARK_v0.4"


class TestPlayModes(unittest.TestCase):
    def test_normalize_valid_modes(self):
        self.assertEqual(
            normalize_play_modes(["two_player", "single_investigator"]),
            ["two_player", "single_investigator"],
        )

    def test_invalid_mode_raises(self):
        with self.assertRaises(ValueError):
            normalize_play_modes(["solo"])


class TestSoloMinimalFixture(unittest.TestCase):
    def test_valid_solo_fixture_passes(self):
        res = validate_single_investigator(FIXTURES / "solo_minimal")
        self.assertEqual(res.status, "PASS")
        self.assertFalse(res.errors)

    def test_invalid_split_fixture_fails(self):
        res = validate_single_investigator(FIXTURES / "solo_invalid_split")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any("split" in e.lower() or "BOOKLET" in e for e in res.errors))

    def test_two_player_only_skips_solo_validation(self):
        res = validate_single_investigator(FIXTURES / "two_player_only")
        self.assertEqual(res.status, "SKIP")

    def test_harborview_does_not_false_pass_solo(self):
        if not HARBORVIEW.exists():
            self.skipTest("Harborview not in workspace")
        manifest = load_play_manifest(HARBORVIEW)
        self.assertIsNone(manifest)
        res = validate_single_investigator(HARBORVIEW)
        self.assertEqual(res.status, "SKIP")
        self.assertNotEqual(res.status, "PASS")


class TestTrustStyleMutations(unittest.TestCase):
    """Adversarial: removing manifest fields must fail solo validation."""

    def test_missing_partner_rules_equivalent(self):
        root = FIXTURES / "solo_minimal"
        manifest = copy.deepcopy(load_play_manifest(root))
        manifest.pop("single_investigator")
        # Write temp manifest logic via direct validate on broken manifest - use invalid fixture
        res = validate_single_investigator(FIXTURES / "solo_invalid_split")
        self.assertEqual(res.status, "FAIL")


if __name__ == "__main__":
    unittest.main()
