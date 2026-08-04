"""Tests for Object Interaction System (Milestone 4)."""

import unittest
from pathlib import Path

from idne.object_interaction_validate import validate_object_interaction

FIXTURES = Path(__file__).resolve().parent / "fixtures"
HARBORVIEW = Path(__file__).resolve().parents[1] / "adventures" / "CASE_BENCHMARK_v0.4"


class TestObjectInteractionFixtures(unittest.TestCase):
    def test_valid_nested_passes(self):
        res = validate_object_interaction(FIXTURES / "obj_valid_nested")
        self.assertEqual(res.status, "PASS")

    def test_hidden_key_success_passes(self):
        res = validate_object_interaction(FIXTURES / "obj_hidden_key_success")
        self.assertEqual(res.status, "PASS")

    def test_failed_no_reveal_fails(self):
        res = validate_object_interaction(FIXTURES / "obj_failed_no_reveal")
        self.assertEqual(res.status, "FAIL")

    def test_check_changes_truth_fails(self):
        res = validate_object_interaction(FIXTURES / "obj_check_changes_truth")
        self.assertEqual(res.status, "FAIL")

    def test_pass_fail_same_unit_fails(self):
        res = validate_object_interaction(FIXTURES / "obj_pass_fail_same_unit")
        self.assertEqual(res.status, "FAIL")

    def test_bare_page_code_fails(self):
        res = validate_object_interaction(FIXTURES / "obj_bare_page_code")
        self.assertEqual(res.status, "FAIL")

    def test_repeated_check_fails(self):
        res = validate_object_interaction(FIXTURES / "obj_repeated_check")
        self.assertEqual(res.status, "FAIL")

    def test_doubled_cost_fails(self):
        res = validate_object_interaction(FIXTURES / "obj_doubled_cost")
        self.assertEqual(res.status, "FAIL")

    def test_missing_return_fails(self):
        res = validate_object_interaction(FIXTURES / "obj_missing_return")
        self.assertEqual(res.status, "FAIL")

    def test_state_reset_revisit_fails(self):
        res = validate_object_interaction(FIXTURES / "obj_state_reset_revisit")
        self.assertEqual(res.status, "FAIL")

    def test_child_before_parent_fails(self):
        res = validate_object_interaction(FIXTURES / "obj_child_before_parent")
        self.assertEqual(res.status, "FAIL")

    def test_collected_still_present_fails(self):
        res = validate_object_interaction(FIXTURES / "obj_collected_still_present")
        self.assertEqual(res.status, "FAIL")

    def test_impossible_inventory_fails(self):
        res = validate_object_interaction(FIXTURES / "obj_impossible_inventory")
        self.assertEqual(res.status, "FAIL")

    def test_mandatory_no_interaction_fails(self):
        res = validate_object_interaction(FIXTURES / "obj_mandatory_no_interaction")
        self.assertEqual(res.status, "FAIL")

    def test_wf_contradict_fails(self):
        res = validate_object_interaction(FIXTURES / "obj_wf_contradict")
        self.assertEqual(res.status, "FAIL")

    def test_harborview_skips(self):
        if not HARBORVIEW.exists():
            self.skipTest("Harborview missing")
        res = validate_object_interaction(HARBORVIEW)
        self.assertEqual(res.status, "SKIP")


if __name__ == "__main__":
    unittest.main()
