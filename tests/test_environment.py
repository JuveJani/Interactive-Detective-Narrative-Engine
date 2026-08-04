"""Tests for Environment System (Milestone 3)."""

import unittest
from pathlib import Path

from idne.environment_validate import validate_environment

FIXTURES = Path(__file__).resolve().parent / "fixtures"
HARBORVIEW = Path(__file__).resolve().parents[1] / "adventures" / "CASE_BENCHMARK_v0.4"


class TestEnvironmentFixtures(unittest.TestCase):
    def test_valid_minimal_passes(self):
        res = validate_environment(FIXTURES / "env_valid_minimal")
        self.assertEqual(res.status, "PASS")
        self.assertFalse(res.errors)

    def test_undeclared_destination_fails(self):
        res = validate_environment(FIXTURES / "env_undeclared_dest")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any("undeclared" in e.lower() or "LOC-MISSING" in e for e in res.errors))

    def test_feature_without_location_fails(self):
        res = validate_environment(FIXTURES / "env_feature_no_location")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any("FEAT-ORPHAN" in e or "LOC-NOWHERE" in e for e in res.errors))

    def test_hidden_feature_exposed_fails(self):
        res = validate_environment(FIXTURES / "env_hidden_exposed")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any("hidden" in e.lower() or "FEAT-HIDDEN" in e for e in res.errors))

    def test_unexplained_transition_fails(self):
        res = validate_environment(FIXTURES / "env_unexplained_transition")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any("TR-BAD" in e or "missing cause" in e for e in res.errors))

    def test_broken_return_fails(self):
        res = validate_environment(FIXTURES / "env_broken_return")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any("return" in e.lower() for e in res.errors))

    def test_state_reset_revisit_fails(self):
        res = validate_environment(FIXTURES / "env_state_reset_revisit")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any("revisit" in e.lower() or "reset" in e.lower() for e in res.errors))

    def test_bare_page_code_fails(self):
        res = validate_environment(FIXTURES / "env_bare_page_code")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any("bare" in e.lower() or "J-223" in e for e in res.errors))

    def test_impossible_access_fails(self):
        res = validate_environment(FIXTURES / "env_impossible_access")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any("impossible" in e.lower() for e in res.errors))

    def test_wf_contradict_fails(self):
        res = validate_environment(FIXTURES / "env_wf_contradict")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any("contradict" in e.lower() or "WF" in e for e in res.errors))

    def test_harborview_skips_environment(self):
        if not HARBORVIEW.exists():
            self.skipTest("Harborview not in workspace")
        res = validate_environment(HARBORVIEW)
        self.assertEqual(res.status, "SKIP")


if __name__ == "__main__":
    unittest.main()
