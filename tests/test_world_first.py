"""Tests for World-First Generation (Milestone 2)."""

import unittest
from pathlib import Path

from idne.world_first_validate import validate_world_first

FIXTURES = Path(__file__).resolve().parent / "fixtures"
HARBORVIEW = Path(__file__).resolve().parents[1] / "adventures" / "CASE_BENCHMARK_v0.4"


class TestWorldFirstFixtures(unittest.TestCase):
    def test_valid_minimal_passes(self):
        res = validate_world_first(FIXTURES / "wf_valid_minimal")
        self.assertEqual(res.status, "PASS")
        self.assertFalse(res.errors)

    def test_contradictory_timeline_fails(self):
        res = validate_world_first(FIXTURES / "wf_contradictory_timeline")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any("contradiction" in e.lower() or "cause" in e.lower() for e in res.errors))

    def test_npc_overknow_fails(self):
        res = validate_world_first(FIXTURES / "wf_npc_overknow")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any("NPC" in e and "knows" in e for e in res.errors))

    def test_evidence_no_source_fails(self):
        res = validate_world_first(FIXTURES / "wf_evidence_no_source")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any("source_event" in e or "EVD" in e for e in res.errors))

    def test_conclusion_missing_fails(self):
        res = validate_world_first(FIXTURES / "wf_conclusion_missing")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any("unobtainable" in e.lower() or "FACT-MISSING" in e for e in res.errors))

    def test_ambiguous_date_fails(self):
        res = validate_world_first(FIXTURES / "wf_ambiguous_date")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any("ambiguous" in e.lower() or "timestamp" in e.lower() for e in res.errors))

    def test_scene_contradicts_truth_fails(self):
        res = validate_world_first(FIXTURES / "wf_scene_contradicts_truth")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(
            any("contradicts" in e.lower() or "FACT-INVENTED" in e or "culprit" in e.lower() for e in res.errors)
        )

    def test_harborview_skips_world_first(self):
        if not HARBORVIEW.exists():
            self.skipTest("Harborview not in workspace")
        res = validate_world_first(HARBORVIEW)
        self.assertEqual(res.status, "SKIP")


if __name__ == "__main__":
    unittest.main()
