"""Regression tests for final trust-gate, R-212b loop, I-02 cost, and follow-up budget fixes."""

from __future__ import annotations

import copy
import random
import unittest

from simulator.diagnostics import analyze_simulation
from simulator.engine import SimulationEngine
from simulator.follow_ups import apply_follow_up, eligible_follow_up_options
from simulator.loader import load_adventure
from simulator.self_check import simulator_trustworthy
from simulator.state import GameState
from simulator.trust_gate import validate_trust_invariants


class TestTrustGateInvariants(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.package = load_adventure("adventures/CASE_BENCHMARK_v0.4")
        cls.adapter = cls.package["adapter"]

    def test_canonical_adapter_trusted(self):
        ok, blockers = simulator_trustworthy(self.adapter)
        self.assertTrue(ok, msg=f"blockers={blockers}")

    def _assert_untrusted_after_mutation(self, label: str, mutate_fn):
        adapter = copy.deepcopy(self.adapter)
        mutate_fn(adapter)
        ok, blockers = simulator_trustworthy(adapter)
        self.assertFalse(ok, msg=f"{label} should be untrusted")
        self.assertTrue(blockers, msg=f"{label} should produce blockers")

    def test_regression_unconditional_p112_key(self):
        def mutate(a):
            a["nodes"]["P-112"]["flags"] = ["MOTIVE_WITNESS", "ACCESS_MANAGER_KEY"]
            a["nodes"]["P-112"].pop("partner_conditional_flags", None)

        self._assert_untrusted_after_mutation("unconditional P-112 key", mutate)

    def test_regression_missing_p112_partner_rules(self):
        def mutate(a):
            a["nodes"]["P-112"].pop("partner_conditional_flags", None)

        self._assert_untrusted_after_mutation("missing P-112 partner_conditional_flags", mutate)

    def test_regression_missing_i02_blocked_fields(self):
        def mutate(a):
            j = a["nodes"]["J-410"]
            j.pop("blocked_return", None)
            j.pop("blocked_minutes", None)

        self._assert_untrusted_after_mutation("missing I-02 blocked fields", mutate)

    def test_regression_missing_i02_blocked_minutes_only(self):
        def mutate(a):
            a["nodes"]["J-410"].pop("blocked_minutes", None)

        self._assert_untrusted_after_mutation("missing blocked_minutes", mutate)

    def test_regression_missing_follow_up_actions(self):
        def mutate(a):
            a["follow_up_actions"] = []

        self._assert_untrusted_after_mutation("empty follow_up_actions", mutate)

    def test_regression_restored_keyword_follow_ups(self):
        def mutate(a):
            a["follow_ups"] = [{"keywords": ["gym"], "minutes": 10}]

        self._assert_untrusted_after_mutation("keyword follow_ups restored", mutate)

    def test_regression_missing_ambiguities_key(self):
        def mutate(a):
            a.pop("ambiguities", None)

        self._assert_untrusted_after_mutation("missing ambiguities key", mutate)

    def test_regression_r212b_auto_next_loop(self):
        def mutate(a):
            a["nodes"]["R-212b"]["next"] = "R-212"
            a["nodes"]["R-212b"].pop("next_options", None)
            a["nodes"]["R-212"]["choices"] = [
                {"id": "duplicates", "target": "R-212a"},
                {"id": "skim", "target": "R-212b"},
            ]

        self._assert_untrusted_after_mutation("R-212b loop regression", mutate)

    def test_regression_i02_cost_resolution_removed(self):
        def mutate(a):
            a["nodes"]["J-410"].pop("minutes_cost_resolution", None)

        self._assert_untrusted_after_mutation("missing minutes_cost_resolution", mutate)

    def test_regression_i02_entity_conflict_unresolved(self):
        def mutate(a):
            a["nodes"]["J-410"]["minutes"] = 12
            a["nodes"]["J-410"]["blocked_minutes"] = 12
            a["nodes"]["J-410"]["minutes_cost_resolution"]["unresolved"] = True

        self._assert_untrusted_after_mutation("unresolved I-02 cost", mutate)

    def test_validate_invariants_lists_multiple_blockers(self):
        adapter = copy.deepcopy(self.adapter)
        adapter["nodes"]["P-112"]["flags"].append("ACCESS_MANAGER_KEY")
        adapter.pop("follow_up_actions", None)
        blockers = validate_trust_invariants(adapter)
        self.assertGreaterEqual(len(blockers), 2)


class TestR212bLoopTermination(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.package = load_adventure("adventures/CASE_BENCHMARK_v0.4")
        cls.engine = SimulationEngine(cls.package, random.Random(0))

    def test_adversarial_skim_terminates_without_depth_burn(self):
        st = GameState(node="R-212", clock=1280)

        def always_skim_then_back(s, o, r):
            for x in o:
                if x.get("target") == "R-212b" or x.get("id") == "skim":
                    return x
            for x in o:
                if x.get("target") == "R-212" or x.get("id") == "R-212":
                    return x
            return o[0]

        local, mins = self.engine.run_role_path(
            st, "R-212", "J-400", "records", always_skim_then_back
        )
        skim_visits = sum(1 for p in local.path if p.endswith("R-212b"))
        self.assertLessEqual(skim_visits, 1, msg=f"path tail={local.path[-20:]}")
        self.assertLess(mins, 200, msg=f"skim loop burned {mins} minutes")
        self.assertIn("R-214", {p.split(":")[-1] for p in local.path})

    def test_r212b_has_player_next_options(self):
        opts = self.package["adapter"]["nodes"]["R-212b"]["next_options"]
        self.assertEqual(set(opts), {"R-212", "R-214"})


class TestI02CostResolution(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.package = load_adventure("adventures/CASE_BENCHMARK_v0.4")

    def test_player_authoritative_ten_minutes(self):
        j410 = self.package["adapter"]["nodes"]["J-410"]
        res = j410["minutes_cost_resolution"]
        self.assertEqual(j410["minutes"], 10)
        self.assertEqual(j410["blocked_minutes"], 10)
        self.assertEqual(res["authoritative_minutes"], 10)
        self.assertFalse(res["unresolved"])
        ok, blockers = simulator_trustworthy(self.package["adapter"])
        self.assertTrue(ok, msg=blockers)


class TestFollowUpBudgetSeparation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.package = load_adventure("adventures/CASE_BENCHMARK_v0.4")
        cls.adapter = cls.package["adapter"]
        cls.engine = SimulationEngine(cls.package, random.Random(0))

    def test_needs_followup_does_not_consume_phone_budget(self):
        local, _ = self.engine.run_role_path(
            GameState(node="P-211a", clock=1200),
            "P-211a",
            "J-400",
            "people",
            lambda s, o, r: o[0],
        )
        local.pending_followup = "P-214"
        local2, _ = self.engine.run_role_path(
            local, "P-211a", "J-400", "people", lambda s, o, r: o[0]
        )
        self.assertIn("P-214", {p.split(":")[-1] for p in local2.path})
        self.assertEqual(local2.follow_ups_used, 0)

    def test_follow_up_availability_without_budget_use(self):
        st = GameState(node="J-300", clock=1200)
        st.flags.add("CHECK_FAIL_CHK_JAMES_PRESS")
        self.assertEqual(st.follow_ups_used, 0)
        opts = eligible_follow_up_options(st, "J-300", self.adapter)
        self.assertTrue(opts)
        self.assertEqual(st.follow_ups_used, 0)

    def test_follow_up_selection_still_available(self):
        st = GameState(node="J-300", clock=1200)
        st.flags.add("CHECK_FAIL_CHK_JAMES_PRESS")
        opts = eligible_follow_up_options(st, "J-300", self.adapter)
        self.assertIn("FU_GYM_ALIBI", {o["id"] for o in opts})

    def test_follow_up_execution_consumes_budget(self):
        st = GameState(node="J-300", clock=1200)
        st.flags.add("CHECK_FAIL_CHK_JAMES_PRESS")
        apply_follow_up(st, "FU_GYM_ALIBI", self.adapter)
        self.assertEqual(st.follow_ups_used, 1)
        self.assertEqual(st.follow_up_use_counts["FU_GYM_ALIBI"], 1)

    def test_budget_exhaustion_blocks_availability_not_selection_state(self):
        st = GameState(node="J-300", clock=1200)
        st.follow_ups_used = self.adapter["follow_up_max"]
        self.assertEqual(eligible_follow_up_options(st, "J-300", self.adapter), [])


if __name__ == "__main__":
    unittest.main()
