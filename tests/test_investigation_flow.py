"""Tests for Investigation Flow & Ending System (Milestone 5C)."""

import unittest
from pathlib import Path

from idne.investigation_flow_validate import validate_investigation_flow

FIXTURES = Path(__file__).resolve().parent / "fixtures"
HARBORVIEW = Path(__file__).resolve().parents[1] / "adventures" / "CASE_BENCHMARK_v0.4"


class TestInvestigationFlowFixtures(unittest.TestCase):
    def test_valid_minimal_passes(self):
        res = validate_investigation_flow(FIXTURES / "iflow_valid_minimal")
        self.assertEqual(res.status, "PASS")
        self.assertEqual(res.checks.get("FLOW-TRUTH-LEAK"), "PASS")
        self.assertEqual(res.checks.get("FLOW-DEADLINE"), "PASS")

    def test_impossible_ending_fails(self):
        res = validate_investigation_flow(FIXTURES / "iflow_impossible_ending")
        self.assertEqual(res.status, "FAIL")
        self.assertEqual(res.checks.get("FLOW-IMPOSSIBLE"), "FAIL")

    def test_deadline_missing_fails(self):
        res = validate_investigation_flow(FIXTURES / "iflow_deadline_missing")
        self.assertEqual(res.status, "FAIL")
        self.assertEqual(res.checks.get("FLOW-DEADLINE"), "FAIL")

    def test_unsupported_accusation_fails(self):
        res = validate_investigation_flow(FIXTURES / "iflow_unsupported_accusation")
        self.assertEqual(res.status, "FAIL")
        self.assertEqual(res.checks.get("FLOW-UNSUPPORTED-ACCUSATION"), "FAIL")

    def test_truth_leak_fails(self):
        res = validate_investigation_flow(FIXTURES / "iflow_truth_leak")
        self.assertEqual(res.status, "FAIL")
        self.assertEqual(res.checks.get("FLOW-TRUTH-LEAK"), "FAIL")

    def test_state_inconsistent_fails(self):
        res = validate_investigation_flow(FIXTURES / "iflow_state_inconsistent")
        self.assertEqual(res.status, "FAIL")
        self.assertEqual(res.checks.get("FLOW-STATE-INCONSIST"), "FAIL")

    def test_unreachable_chain_fails(self):
        res = validate_investigation_flow(FIXTURES / "iflow_unreachable_chain")
        self.assertEqual(res.status, "FAIL")
        self.assertEqual(res.checks.get("FLOW-UNREACHABLE"), "FAIL")

    def test_unreachable_ending_fails(self):
        res = validate_investigation_flow(FIXTURES / "iflow_unreachable_ending")
        self.assertEqual(res.status, "FAIL")
        self.assertEqual(res.checks.get("FLOW-UNREACHABLE"), "FAIL")

    def test_missing_questionnaire_fails(self):
        res = validate_investigation_flow(FIXTURES / "iflow_missing_questionnaire")
        self.assertEqual(res.status, "FAIL")
        self.assertEqual(res.checks.get("FLOW-UNSUPPORTED-ACCUSATION"), "FAIL")

    def test_harborview_skips(self):
        if not HARBORVIEW.exists():
            self.skipTest("no harborview")
        res = validate_investigation_flow(HARBORVIEW)
        self.assertEqual(res.status, "SKIP")


if __name__ == "__main__":
    unittest.main()
