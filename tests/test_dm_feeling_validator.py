"""Tests for DM Feeling Validator (Milestone 10)."""

import unittest
from pathlib import Path

from idne.dm_feeling_validate import validate_dm_feeling

FIXTURES = Path(__file__).resolve().parent / "fixtures"
HARBORVIEW = Path(__file__).resolve().parents[1] / "adventures" / "CASE_BENCHMARK_v0.4"


class TestDmFeelingFixtures(unittest.TestCase):
    def test_valid_solo_agency_passes(self):
        res = validate_dm_feeling(FIXTURES / "df_valid_solo_agency")
        self.assertEqual(res.status, "PASS")
        self.assertEqual(res.category_scores.get("player_agency"), "PASS")

    def test_valid_two_player_passes(self):
        res = validate_dm_feeling(FIXTURES / "df_valid_two_player")
        self.assertEqual(res.status, "PASS")

    def test_bare_code_choice_fails(self):
        res = validate_dm_feeling(FIXTURES / "df_bare_code_choice")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "DF-BARE-CODE" for f in res.findings))

    def test_unexplained_choice_fails(self):
        res = validate_dm_feeling(FIXTURES / "df_unexplained_choice")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "DF-UNEXPLAINED-CHOICE" for f in res.findings))

    def test_fake_branch_fails(self):
        res = validate_dm_feeling(FIXTURES / "df_fake_branch")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "DF-FAKE-BRANCH" for f in res.findings))

    def test_passive_reading_fails(self):
        res = validate_dm_feeling(FIXTURES / "df_passive_reading")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "DF-PASSIVE-READING" for f in res.findings))

    def test_auto_major_grant_fails(self):
        res = validate_dm_feeling(FIXTURES / "df_auto_major_grant")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "DF-AUTO-MAJOR-GRANT" for f in res.findings))

    def test_valid_layered_object_passes(self):
        res = validate_dm_feeling(FIXTURES / "df_valid_layered_object")
        self.assertEqual(res.status, "PASS")

    def test_hidden_exposed_early_fails(self):
        res = validate_dm_feeling(FIXTURES / "df_hidden_exposed_early")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "DF-HIDDEN-EARLY" for f in res.findings))

    def test_check_leak_failure_fails(self):
        res = validate_dm_feeling(FIXTURES / "df_check_leak_failure")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "DF-FAIL-LEAK" for f in res.findings))

    def test_valid_multi_fact_inference_passes(self):
        res = validate_dm_feeling(FIXTURES / "df_valid_multi_fact_inference")
        self.assertEqual(res.status, "PASS")

    def test_inference_theatre_fails(self):
        res = validate_dm_feeling(FIXTURES / "df_inference_theatre")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "DF-INFERENCE-THEATRE" for f in res.findings))

    def test_answer_in_question_fails(self):
        res = validate_dm_feeling(FIXTURES / "df_answer_in_question")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "DF-ANSWER-IN-QUESTION" for f in res.findings))

    def test_valid_aha_structure_passes(self):
        res = validate_dm_feeling(FIXTURES / "df_valid_aha_structure")
        self.assertEqual(res.status, "PASS")

    def test_direct_conclusion_delivery_fails(self):
        res = validate_dm_feeling(FIXTURES / "df_direct_conclusion_delivery")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "DF-DIRECT-CONCLUSION" for f in res.findings))

    def test_persistent_revisit_passes(self):
        res = validate_dm_feeling(FIXTURES / "df_persistent_revisit")
        self.assertEqual(res.status, "PASS")

    def test_reset_location_fails(self):
        res = validate_dm_feeling(FIXTURES / "df_reset_location")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "DF-RESET-LOCATION" for f in res.findings))

    def test_inert_time_threshold_fails(self):
        res = validate_dm_feeling(FIXTURES / "df_inert_time_threshold")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "DF-INERT-TIME" for f in res.findings))

    def test_irrelevant_deadline_fails(self):
        res = validate_dm_feeling(FIXTURES / "df_irrelevant_deadline")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "DF-IRRELEVANT-DEADLINE" for f in res.findings))

    def test_meaningful_failure_passes(self):
        res = validate_dm_feeling(FIXTURES / "df_meaningful_failure")
        self.assertEqual(res.status, "PASS")

    def test_failure_no_effect_fails(self):
        res = validate_dm_feeling(FIXTURES / "df_failure_no_effect")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "DF-FAILURE-NO-EFFECT" for f in res.findings))

    def test_responsive_npc_passes(self):
        res = validate_dm_feeling(FIXTURES / "df_responsive_npc")
        self.assertEqual(res.status, "PASS")

    def test_exposition_npc_menu_fails(self):
        res = validate_dm_feeling(FIXTURES / "df_exposition_npc_menu")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "DF-EXPOSITION-MENU" for f in res.findings))

    def test_trust_unused_fails(self):
        res = validate_dm_feeling(FIXTURES / "df_trust_unused")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "DF-TRUST-UNUSED" for f in res.findings))

    def test_final_choice_only_ending_fails(self):
        res = validate_dm_feeling(FIXTURES / "df_final_choice_only_ending")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "DF-FINAL-CHOICE-ONLY" for f in res.findings))

    def test_valid_causal_ending_passes(self):
        res = validate_dm_feeling(FIXTURES / "df_valid_causal_ending")
        self.assertEqual(res.status, "PASS")

    def test_imperfect_ending_leak_fails(self):
        res = validate_dm_feeling(FIXTURES / "df_imperfect_ending_leak")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "DF-ENDING-TRUTH-LEAK" for f in res.findings))

    def test_absent_partner_dependency_passes(self):
        res = validate_dm_feeling(FIXTURES / "df_absent_partner_dependency")
        self.assertEqual(res.status, "PASS")

    def test_two_player_little_joint_fails(self):
        res = validate_dm_feeling(FIXTURES / "df_two_player_little_joint")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "DF-LITTLE-JOINT" for f in res.findings))

    def test_state_limit_blocked(self):
        res = validate_dm_feeling(FIXTURES / "df_state_limit_blocked")
        self.assertEqual(res.status, "BLOCKED")
        self.assertTrue(any(f.finding_id == "DF-STATE-EXPLOSION" for f in res.findings))

    def test_missing_tier_b_conditional(self):
        res = validate_dm_feeling(FIXTURES / "df_missing_tier_b")
        self.assertEqual(res.status, "CONDITIONAL_PASS")
        self.assertTrue(any(f.finding_id == "DF-TIER-B-DF-B-AGENCY" for f in res.findings))

    def test_missing_playtest_conditional(self):
        res = validate_dm_feeling(FIXTURES / "df_missing_playtest")
        self.assertEqual(res.status, "CONDITIONAL_PASS")
        self.assertTrue(any(f.finding_id == "DF-TIER-C-MISSING" for f in res.findings))

    def test_valid_offline_ai_export_passes(self):
        res = validate_dm_feeling(FIXTURES / "df_valid_offline_ai_export")
        self.assertEqual(res.status, "PASS")

    def test_harborview_skips(self):
        if not HARBORVIEW.exists():
            self.skipTest("no harborview")
        res = validate_dm_feeling(HARBORVIEW)
        self.assertEqual(res.status, "SKIP")


if __name__ == "__main__":
    unittest.main()
