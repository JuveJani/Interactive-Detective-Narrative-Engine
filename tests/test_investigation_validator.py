"""Tests for Integrated Investigation Validator (Milestone 7)."""

import unittest
from pathlib import Path

from idne.investigation_validate import validate_investigation

FIXTURES = Path(__file__).resolve().parent / "fixtures"
HARBORVIEW = Path(__file__).resolve().parents[1] / "adventures" / "CASE_BENCHMARK_v0.4"


class TestInvestigationValidatorFixtures(unittest.TestCase):
    def test_complete_solo_passes(self):
        res = validate_investigation(FIXTURES / "iv_complete_solo")
        self.assertEqual(res.status, "PASS")
        self.assertEqual(res.checks.get("IV-CAPABILITY-DELEGATE"), "PASS")

    def test_complete_two_player_passes(self):
        res = validate_investigation(FIXTURES / "iv_complete_two_player")
        self.assertEqual(res.status, "PASS")

    def test_inference_missing_info_fails(self):
        res = validate_investigation(FIXTURES / "iv_inference_missing_info")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "IV-INFERENCE-MISSING-INFO" for f in res.findings))

    def test_info_after_inference_fails(self):
        res = validate_investigation(FIXTURES / "iv_info_after_inference")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "IV-INFO-AFTER-INFERENCE" for f in res.findings))

    def test_undefined_term_fails(self):
        res = validate_investigation(FIXTURES / "iv_undefined_term")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "IV-UNDEFINED-TERM" for f in res.findings))

    def test_equally_supported_fails(self):
        res = validate_investigation(FIXTURES / "iv_equally_supported")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "IV-EQUAL-ALTERNATIVES" for f in res.findings))

    def test_vague_recovery_fails(self):
        res = validate_investigation(FIXTURES / "iv_vague_recovery")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "IV-VAGUE-RECOVERY" for f in res.findings))

    def test_recovery_bare_code_fails(self):
        res = validate_investigation(FIXTURES / "iv_recovery_bare_code")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "IV-RECOVERY-BARE-CODE" for f in res.findings))

    def test_zero_cost_loop_fails(self):
        res = validate_investigation(FIXTURES / "iv_zero_cost_loop")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "IV-ZERO-COST-LOOP" for f in res.findings))

    def test_key_behind_own_lock_fails(self):
        res = validate_investigation(FIXTURES / "iv_key_behind_own_lock")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "IV-KEY-OWN-LOCK" for f in res.findings))

    def test_password_no_route_fails(self):
        res = validate_investigation(FIXTURES / "iv_password_no_route")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "IV-PASSWORD-NO-ROUTE" for f in res.findings))

    def test_item_consumed_early_fails(self):
        res = validate_investigation(FIXTURES / "iv_item_consumed_early")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "IV-ITEM-CONSUMED-EARLY" for f in res.findings))

    def test_check_destroys_routes_fails(self):
        res = validate_investigation(FIXTURES / "iv_check_destroys_routes")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "IV-CHECK-DESTROYS-ROUTES" for f in res.findings))

    def test_npc_disclosure_unreachable_fails(self):
        res = validate_investigation(FIXTURES / "iv_npc_disclosure_unreachable")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "IV-NPC-UNREACHABLE" for f in res.findings))

    def test_undefined_trust_fails(self):
        res = validate_investigation(FIXTURES / "iv_undefined_trust")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "IV-UNDEFINED-TRUST" for f in res.findings))

    def test_npc_leaves_early_fails(self):
        res = validate_investigation(FIXTURES / "iv_npc_leaves_early")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "IV-NPC-LEAVES-EARLY" for f in res.findings))

    def test_time_variant_not_used_fails(self):
        res = validate_investigation(FIXTURES / "iv_time_variant_not_used")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "IV-TIME-VARIANT" for f in res.findings))

    def test_deadline_exceeded_fails(self):
        res = validate_investigation(FIXTURES / "iv_deadline_exceeded")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "IV-DEADLINE-EXCEEDED" for f in res.findings))

    def test_unreachable_ending_fails(self):
        res = validate_investigation(FIXTURES / "iv_unreachable_ending")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "IV-UNREACHABLE-ENDING" for f in res.findings))

    def test_decorative_impossible_ending_fails(self):
        res = validate_investigation(FIXTURES / "iv_decorative_impossible_ending")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "IV-DECORATIVE-IMPOSSIBLE" for f in res.findings))

    def test_ending_truth_leak_fails(self):
        res = validate_investigation(FIXTURES / "iv_ending_truth_leak")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "IV-ENDING-TRUTH-LEAK" for f in res.findings))

    def test_accusation_reveals_answer_fails(self):
        res = validate_investigation(FIXTURES / "iv_accusation_reveals_answer")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "IV-ACCUSATION-REVEALS" for f in res.findings))

    def test_player_no_source_fails(self):
        res = validate_investigation(FIXTURES / "iv_player_no_source")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "IV-PLAYER-NO-SOURCE" for f in res.findings))

    def test_player_missing_action_fails(self):
        res = validate_investigation(FIXTURES / "iv_player_missing_action")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "IV-PLAYER-MISSING-ACTION" for f in res.findings))

    def test_pass_fail_leak_fails(self):
        res = validate_investigation(FIXTURES / "iv_pass_fail_leak")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "IV-PASS-FAIL-LEAK" for f in res.findings))

    def test_destination_missing_fails(self):
        res = validate_investigation(FIXTURES / "iv_destination_missing")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "IV-DESTINATION-MISSING" for f in res.findings))

    def test_location_reset_fails(self):
        res = validate_investigation(FIXTURES / "iv_location_reset")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "IV-LOCATION-RESET" for f in res.findings))

    def test_solo_requires_p2_fails(self):
        res = validate_investigation(FIXTURES / "iv_solo_requires_p2")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "IV-SOLO-REQUIRES-P2" for f in res.findings))

    def test_two_player_private_unshared_fails(self):
        res = validate_investigation(FIXTURES / "iv_two_player_private_unshared")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "IV-TWO-PLAYER-PRIVATE" for f in res.findings))

    def test_state_explosion_blocked(self):
        res = validate_investigation(FIXTURES / "iv_state_explosion")
        self.assertEqual(res.status, "BLOCKED")
        self.assertEqual(res.checks.get("IV-STATE-GRAPH"), "BLOCKED")
        self.assertTrue(any(f.finding_id == "IV-STATE-EXPLOSION" for f in res.findings))

    def test_harborview_skips(self):
        if not HARBORVIEW.exists():
            self.skipTest("no harborview")
        res = validate_investigation(HARBORVIEW)
        self.assertEqual(res.status, "SKIP")


if __name__ == "__main__":
    unittest.main()
