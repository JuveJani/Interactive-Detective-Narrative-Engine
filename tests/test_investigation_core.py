"""Tests for Investigation Core (Milestone 5A)."""

import unittest
from pathlib import Path

from idne.investigation_core_validate import validate_investigation_core

FIXTURES = Path(__file__).resolve().parent / "fixtures"
HARBORVIEW = Path(__file__).resolve().parents[1] / "adventures" / "CASE_BENCHMARK_v0.4"


class TestInvestigationCoreFixtures(unittest.TestCase):
    def test_valid_minimal_passes(self):
        res = validate_investigation_core(FIXTURES / "inv_core_valid_minimal")
        self.assertEqual(res.status, "PASS")

    def test_evidence_no_provenance_fails(self):
        res = validate_investigation_core(FIXTURES / "inv_evidence_no_provenance")
        self.assertEqual(res.status, "FAIL")

    def test_conclusion_unprovable_fails(self):
        res = validate_investigation_core(FIXTURES / "inv_conclusion_unprovable")
        self.assertEqual(res.status, "FAIL")

    def test_proof_not_independent_fails(self):
        res = validate_investigation_core(FIXTURES / "inv_proof_not_independent")
        self.assertEqual(res.status, "FAIL")

    def test_unresolved_contradiction_fails(self):
        res = validate_investigation_core(FIXTURES / "inv_unresolved_contradiction")
        self.assertEqual(res.status, "FAIL")

    def test_clue_drives_investigation_fails(self):
        res = validate_investigation_core(FIXTURES / "inv_clue_drives_investigation")
        self.assertEqual(res.status, "FAIL")

    def test_orphan_knowledge_fails(self):
        res = validate_investigation_core(FIXTURES / "inv_orphan_knowledge")
        self.assertEqual(res.status, "FAIL")

    def test_hypothesis_auto_proved_fails(self):
        res = validate_investigation_core(FIXTURES / "inv_hypothesis_auto_proved")
        self.assertEqual(res.status, "FAIL")

    def test_missing_acquisition_fails(self):
        res = validate_investigation_core(FIXTURES / "inv_missing_acquisition")
        self.assertEqual(res.status, "FAIL")

    def test_testimony_no_source_fails(self):
        res = validate_investigation_core(FIXTURES / "inv_testimony_no_source")
        self.assertEqual(res.status, "FAIL")

    def test_clue_package_flag_fails(self):
        res = validate_investigation_core(FIXTURES / "inv_clue_package_flag")
        self.assertEqual(res.status, "FAIL")

    def test_unmapped_legacy_clue_fails(self):
        res = validate_investigation_core(FIXTURES / "inv_unmapped_legacy_clue")
        self.assertEqual(res.status, "FAIL")

    def test_harborview_skips(self):
        if not HARBORVIEW.exists():
            self.skipTest("no harborview")
        res = validate_investigation_core(HARBORVIEW)
        self.assertEqual(res.status, "SKIP")


if __name__ == "__main__":
    unittest.main()
