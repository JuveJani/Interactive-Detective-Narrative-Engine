"""Tests for Capability Check System (Milestone 6)."""

import unittest
from pathlib import Path

from idne.capability_check_validate import validate_capability_check

FIXTURES = Path(__file__).resolve().parent / "fixtures"
HARBORVIEW = Path(__file__).resolve().parents[1] / "adventures" / "CASE_BENCHMARK_v0.4"


class TestCapabilityCheckFixtures(unittest.TestCase):
    def test_valid_perception_key_passes(self):
        res = validate_capability_check(FIXTURES / "cap_valid_perception_key")
        self.assertEqual(res.status, "PASS")

    def test_valid_fail_no_leak_passes(self):
        res = validate_capability_check(FIXTURES / "cap_valid_fail_no_leak")
        self.assertEqual(res.status, "PASS")

    def test_valid_technical_access_passes(self):
        res = validate_capability_check(FIXTURES / "cap_valid_technical_access")
        self.assertEqual(res.status, "PASS")

    def test_valid_cooperative_two_passes(self):
        res = validate_capability_check(FIXTURES / "cap_valid_cooperative_two")
        self.assertEqual(res.status, "PASS")

    def test_valid_social_trust_pressure_passes(self):
        res = validate_capability_check(FIXTURES / "cap_valid_social_trust_pressure")
        self.assertEqual(res.status, "PASS")

    def test_evidence_existence_changed_fails(self):
        res = validate_capability_check(FIXTURES / "cap_evidence_existence_changed")
        self.assertEqual(res.status, "FAIL")
        self.assertEqual(res.checks.get("CAP-EVIDENCE-EXIST"), "FAIL")

    def test_document_contents_changed_fails(self):
        res = validate_capability_check(FIXTURES / "cap_document_contents_changed")
        self.assertEqual(res.status, "FAIL")
        self.assertEqual(res.checks.get("CAP-DOC-CONTENTS"), "FAIL")

    def test_meaningless_guaranteed_fails(self):
        res = validate_capability_check(FIXTURES / "cap_meaningless_guaranteed")
        self.assertEqual(res.status, "FAIL")

    def test_capability_mismatch_fails(self):
        res = validate_capability_check(FIXTURES / "cap_capability_mismatch")
        self.assertEqual(res.status, "FAIL")
        self.assertEqual(res.checks.get("CAP-CAP-MISMATCH"), "FAIL")

    def test_pass_fail_same_unit_fails(self):
        res = validate_capability_check(FIXTURES / "cap_pass_fail_same_unit")
        self.assertEqual(res.status, "FAIL")
        self.assertEqual(res.checks.get("CAP-PASS-FAIL-UNIT"), "FAIL")

    def test_fail_reveals_hidden_fails(self):
        res = validate_capability_check(FIXTURES / "cap_fail_reveals_hidden")
        self.assertEqual(res.status, "FAIL")
        self.assertEqual(res.checks.get("CAP-FAIL-LEAK"), "FAIL")

    def test_repeated_check_fails(self):
        res = validate_capability_check(FIXTURES / "cap_repeated_check")
        self.assertEqual(res.status, "FAIL")
        self.assertEqual(res.checks.get("CAP-REPEAT"), "FAIL")

    def test_free_second_player_retry_fails(self):
        res = validate_capability_check(FIXTURES / "cap_free_second_player_retry")
        self.assertEqual(res.status, "FAIL")
        self.assertEqual(res.checks.get("CAP-FREE-RETRY"), "FAIL")

    def test_only_proof_route_fails(self):
        res = validate_capability_check(FIXTURES / "cap_only_proof_route")
        self.assertEqual(res.status, "FAIL")
        self.assertEqual(res.checks.get("CAP-ONLY-ROUTE"), "FAIL")

    def test_success_full_conclusion_fails(self):
        res = validate_capability_check(FIXTURES / "cap_success_full_conclusion")
        self.assertEqual(res.status, "FAIL")
        self.assertEqual(res.checks.get("CAP-UNRELATED-CONCLUSION"), "FAIL")

    def test_duplicated_failure_cost_fails(self):
        res = validate_capability_check(FIXTURES / "cap_duplicated_failure_cost")
        self.assertEqual(res.status, "FAIL")
        self.assertEqual(res.checks.get("CAP-DUP-COST"), "FAIL")

    def test_npc_unknown_info_fails(self):
        res = validate_capability_check(FIXTURES / "cap_npc_unknown_info")
        self.assertEqual(res.status, "FAIL")
        self.assertEqual(res.checks.get("CAP-NPC-UNKNOWN"), "FAIL")

    def test_intimidation_as_trust_fails(self):
        res = validate_capability_check(FIXTURES / "cap_intimidation_as_trust")
        self.assertEqual(res.status, "FAIL")
        self.assertEqual(res.checks.get("CAP-INTIMIDATION-TRUST"), "FAIL")

    def test_missing_provenance_fails(self):
        res = validate_capability_check(FIXTURES / "cap_missing_provenance")
        self.assertEqual(res.status, "FAIL")
        self.assertEqual(res.checks.get("CAP-PROVENANCE"), "FAIL")

    def test_unjustified_dc_fails(self):
        res = validate_capability_check(FIXTURES / "cap_unjustified_dc")
        self.assertEqual(res.status, "FAIL")
        self.assertEqual(res.checks.get("CAP-DC-JUST"), "FAIL")

    def test_bare_code_choice_fails(self):
        res = validate_capability_check(FIXTURES / "cap_bare_code_choice")
        self.assertEqual(res.status, "FAIL")
        self.assertEqual(res.checks.get("CAP-BARE-CODE"), "FAIL")

    def test_solo_requires_player2_fails(self):
        res = validate_capability_check(FIXTURES / "cap_solo_requires_player2")
        self.assertEqual(res.status, "FAIL")
        self.assertEqual(res.checks.get("CAP-SOLO-P2"), "FAIL")

    def test_harborview_skips(self):
        if not HARBORVIEW.exists():
            self.skipTest("no harborview")
        res = validate_capability_check(HARBORVIEW)
        self.assertEqual(res.status, "SKIP")


if __name__ == "__main__":
    unittest.main()
