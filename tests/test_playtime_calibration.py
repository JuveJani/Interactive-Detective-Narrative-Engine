"""Tests for Playtime Calibration (Milestone 9)."""

import unittest
from pathlib import Path

from idne.playtime_activity import estimate_activity, sum_activities
from idne.playtime_estimate import estimate_playtime
from idne.playtime_validate import validate_playtime

FIXTURES = Path(__file__).resolve().parent / "fixtures"
HARBORVIEW = Path(__file__).resolve().parents[1] / "adventures" / "CASE_BENCHMARK_v0.4"

ASSUMPTIONS = {
    "simple_seconds_per_word": 1,
    "complex_seconds_per_word": 2,
    "reread_add_full_reading_plus_seconds": 10,
    "callback_recent_minutes": 2,
    "callback_old_minutes": 5,
    "callback_old_threshold_minutes": 60,
}


class TestPlaytimeEstimator(unittest.TestCase):
    def test_rereading_adds_overhead(self):
        base = estimate_activity(
            {"activity_class": "simple_reading", "word_count": 100, "complexity": "simple"},
            ASSUMPTIONS,
            {},
        )
        reread = estimate_activity(
            {"activity_class": "rereading", "word_count": 100, "reread_expected": True},
            ASSUMPTIONS,
            {},
        )
        self.assertGreater(reread.expected_minutes, base.expected_minutes * 1.5)

    def test_callback_old_longer_than_recent(self):
        recent = estimate_activity(
            {"activity_class": "callback_lookup", "callback_age": "recent"},
            ASSUMPTIONS,
            {},
        )
        old = estimate_activity(
            {"activity_class": "callback_lookup", "callback_age": "old"},
            ASSUMPTIONS,
            {},
        )
        self.assertGreater(old.expected_minutes, recent.expected_minutes)


class TestPlaytimeFixtures(unittest.TestCase):
    def test_valid_solo_120_passes(self):
        res = validate_playtime(FIXTURES / "pt_valid_solo_120")
        self.assertEqual(res.status, "PASS")
        self.assertGreater(res.estimate["wall_clock_median_minutes"], 100)

    def test_solo_30_min_content_fails(self):
        res = validate_playtime(FIXTURES / "pt_solo_30_min_content")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "PT-TARGET-HARD-LOW" for f in res.findings))

    def test_two_player_parallel_summed_fails(self):
        res = validate_playtime(FIXTURES / "pt_two_player_parallel_summed")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "PT-PARALLEL-SUMMED" for f in res.findings))

    def test_valid_two_player_max_branch_passes(self):
        res = validate_playtime(FIXTURES / "pt_valid_two_player_max_branch")
        self.assertEqual(res.status, "PASS")
        tp = res.estimate.get("two_player")
        self.assertIsNotNone(tp)
        self.assertFalse(tp["incorrectly_summed_parallel"])

    def test_mutually_exclusive_summed_fails(self):
        res = validate_playtime(FIXTURES / "pt_mutually_exclusive_summed")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "PT-MUTEX-SUMMED" for f in res.findings))

    def test_simple_as_complex_fails(self):
        res = validate_playtime(FIXTURES / "pt_simple_as_complex")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "PT-SIMPLE-AS-COMPLEX" for f in res.findings))

    def test_rereading_overhead_passes(self):
        res = validate_playtime(FIXTURES / "pt_rereading_overhead")
        self.assertEqual(res.status, "PASS")

    def test_callback_recent_passes(self):
        res = validate_playtime(FIXTURES / "pt_callback_recent")
        self.assertEqual(res.status, "PASS")

    def test_callback_old_passes(self):
        res = validate_playtime(FIXTURES / "pt_callback_old")
        self.assertEqual(res.status, "PASS")

    def test_fake_decision_no_credit_fails(self):
        res = validate_playtime(FIXTURES / "pt_fake_decision_no_credit")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "PT-FAKE-DECISION-CREDIT" for f in res.findings))

    def test_meaningful_decision_passes(self):
        res = validate_playtime(FIXTURES / "pt_meaningful_decision")
        self.assertEqual(res.status, "PASS")

    def test_simple_inference_passes(self):
        res = validate_playtime(FIXTURES / "pt_simple_inference")
        self.assertEqual(res.status, "PASS")

    def test_inference_many_facts_passes(self):
        res = validate_playtime(FIXTURES / "pt_inference_many_facts")
        self.assertEqual(res.status, "PASS")

    def test_checkbox_masquerade_puzzle_fails(self):
        res = validate_playtime(FIXTURES / "pt_checkbox_masquerade_puzzle")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "PT-CHECKBOX-PUZZLE" for f in res.findings))

    def test_medium_puzzle_authored_passes(self):
        res = validate_playtime(FIXTURES / "pt_medium_puzzle_authored")
        self.assertEqual(res.status, "PASS")

    def test_failed_inference_recovery_passes(self):
        res = validate_playtime(FIXTURES / "pt_failed_inference_recovery")
        self.assertEqual(res.status, "PASS")

    def test_revisit_heavy_conditional(self):
        res = validate_playtime(FIXTURES / "pt_revisit_heavy")
        self.assertIn(res.status, ("PASS", "CONDITIONAL_PASS"))
        self.assertGreater(res.estimate["wall_clock_median_minutes"], 130)

    def test_exhaustive_fits_scarcity_fails(self):
        res = validate_playtime(FIXTURES / "pt_exhaustive_fits_scarcity")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "PT-SCARCITY-NO-PRESSURE" for f in res.findings))

    def test_deadline_impossible_fair_fails(self):
        res = validate_playtime(FIXTURES / "pt_deadline_impossible_fair")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "PT-DEADLINE-BEFORE-SOLUTION" for f in res.findings))

    def test_time_gated_unreachable_fails(self):
        res = validate_playtime(FIXTURES / "pt_time_gated_unreachable")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "PT-TIME-GATED-UNREACHABLE" for f in res.findings))

    def test_missing_metadata_blocked(self):
        res = validate_playtime(FIXTURES / "pt_missing_metadata_blocked")
        self.assertEqual(res.status, "BLOCKED")
        self.assertTrue(any(f.finding_id == "PT-METADATA-MISSING" for f in res.findings))

    def test_valid_solo_path_report_passes(self):
        res = validate_playtime(FIXTURES / "pt_valid_solo_path_report")
        self.assertEqual(res.status, "PASS")
        types = {p["path_type"] for p in res.estimate["paths"]}
        self.assertIn("shortest_valid", types)
        self.assertIn("median_expected", types)
        self.assertIn("longest_valid_before_deadline", types)

    def test_valid_two_player_split_wait_passes(self):
        res = validate_playtime(FIXTURES / "pt_valid_two_player_split_wait")
        self.assertEqual(res.status, "PASS")
        tp = res.estimate["two_player"]
        self.assertIn("per_player_waiting", tp)

    def test_severe_split_imbalance_conditional(self):
        res = validate_playtime(FIXTURES / "pt_severe_split_imbalance")
        self.assertEqual(res.status, "CONDITIONAL_PASS")
        self.assertTrue(any(f.finding_id == "PT-SPLIT-IMBALANCE" for f in res.findings))

    def test_playtest_predicted_120_measured_30(self):
        res = validate_playtime(FIXTURES / "pt_playtest_predicted_120_measured_30")
        self.assertEqual(res.status, "CONDITIONAL_PASS")
        self.assertTrue(any(f.finding_id == "PT-CAL-ERROR" for f in res.findings))

    def test_playtest_predicted_120_measured_70(self):
        res = validate_playtime(FIXTURES / "pt_playtest_predicted_120_measured_70")
        self.assertEqual(res.status, "CONDITIONAL_PASS")

    def test_one_playtest_insufficient_fails(self):
        res = validate_playtime(FIXTURES / "pt_one_playtest_insufficient")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "PT-CAL-SINGLE-OBS" for f in res.findings))

    def test_multiple_playtests_recommendation_passes(self):
        res = validate_playtime(FIXTURES / "pt_multiple_playtests_recommendation")
        self.assertEqual(res.status, "PASS")
        self.assertTrue(any("calibration recommendation" in w for w in res.warnings))

    def test_ending_questionnaire_time_passes(self):
        res = validate_playtime(FIXTURES / "pt_ending_questionnaire_time")
        self.assertEqual(res.status, "PASS")

    def test_perfect_ending_path_passes(self):
        res = validate_playtime(FIXTURES / "pt_perfect_ending_path")
        self.assertEqual(res.status, "PASS")
        types = {p["path_type"] for p in res.estimate["paths"]}
        self.assertIn("perfect_ending", types)

    def test_harborview_skips(self):
        if not HARBORVIEW.exists():
            self.skipTest("no harborview")
        res = validate_playtime(HARBORVIEW)
        self.assertEqual(res.status, "SKIP")


if __name__ == "__main__":
    unittest.main()
