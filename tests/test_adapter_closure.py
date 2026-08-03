"""Regression tests for simulator adapter closure blockers."""

import copy
import random
import unittest

from simulator.diagnostics import analyze_simulation
from simulator.engine import SimulationEngine
from simulator.follow_ups import apply_follow_up, eligible_follow_up_options, legacy_keyword_follow_ups
from simulator.loader import load_adventure
from simulator.self_check import simulator_trustworthy
from simulator.state import GameState
from simulator.validate import validate_static


class TestP112ManagerKey(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.package = load_adventure("adventures/CASE_BENCHMARK_v0.4")
        cls.engine = SimulationEngine(cls.package, random.Random(0))

    def test_key_granted_when_records_lacks_it(self):
        people = GameState(node="P-112", clock=1180)
        people.path = ["people:P-111", "people:P-112"]
        people.grant_flag("MOTIVE_WITNESS")
        people.grant_clue("C-09")
        records = GameState(node="R-111a", clock=1180)
        records.path = ["records:R-111", "records:R-111a"]
        merged = GameState(node="J-200", clock=1180)
        from simulator.engine import _apply_partner_conditional_flags

        _apply_partner_conditional_flags(merged, people, records, self.package["adapter"]["nodes"])
        self.assertIn("ACCESS_MANAGER_KEY", merged.flags)

    def test_key_not_granted_when_records_has_it(self):
        people = GameState(node="P-112", clock=1180)
        people.path = ["people:P-111", "people:P-112"]
        people.grant_flag("MOTIVE_WITNESS")
        people.grant_clue("C-09")
        records = GameState(node="R-111b", clock=1180)
        records.path = ["records:R-111", "records:R-111b"]
        records.grant_flag("ACCESS_MANAGER_KEY")
        merged = GameState(node="J-200", clock=1180)
        from simulator.engine import _apply_partner_conditional_flags

        _apply_partner_conditional_flags(merged, people, records, self.package["adapter"]["nodes"])
        self.assertNotIn("ACCESS_MANAGER_KEY", merged.flags)
        self.assertNotIn("ACCESS_MANAGER_KEY", people.flags)

    def test_p112_node_has_no_unconditional_key(self):
        p112 = self.package["adapter"]["nodes"]["P-112"]
        self.assertNotIn("ACCESS_MANAGER_KEY", p112.get("flags", []))
        self.assertTrue(p112.get("partner_conditional_flags"))


class TestResolvedAmbiguities(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.package = load_adventure("adventures/CASE_BENCHMARK_v0.4")
        cls.adapter = cls.package["adapter"]

    def test_all_four_ambiguities_resolved(self):
        resolved = {r["id"] for r in self.adapter.get("resolved_ambiguities", [])}
        self.assertIn("AMB-J121", resolved)
        self.assertIn("AMB-P112", resolved)
        self.assertIn("AMB-P111", resolved)
        self.assertIn("AMB-R212B", resolved)
        self.assertEqual(self.adapter.get("ambiguities", []), [])

    def test_j121_next_options(self):
        self.assertEqual(
            self.adapter["nodes"]["J-121"]["next_options"],
            ["J-120", "J-130"],
        )

    def test_p111_gate_branch_choices(self):
        gate = self.adapter["nodes"]["P-111"]["gate"]
        ids = {c["id"] for c in gate["branch_choices"]}
        self.assertIn("skip_closed", ids)
        self.assertIn("phone_followup", ids)

    def test_r212b_fake_choice(self):
        self.assertTrue(self.adapter["nodes"]["R-212b"]["fake_choice"])


class TestTrustGate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.package = load_adventure("adventures/CASE_BENCHMARK_v0.4")

    def test_quantitative_trust_enabled_when_prerequisites_pass(self):
        ok, blockers = simulator_trustworthy(self.package["adapter"])
        self.assertTrue(ok, msg=f"Unexpected blockers: {blockers}")
        self.assertEqual(blockers, [])

    def test_unresolved_ambiguity_downgrades_trust(self):
        adapter = copy.deepcopy(self.package["adapter"])
        adapter["ambiguities"] = ["Synthetic unresolved ambiguity for test"]
        ok, blockers = simulator_trustworthy(adapter)
        self.assertFalse(ok)
        self.assertTrue(any("unresolved ambiguities" in b for b in blockers))

    def test_diagnostics_trust_when_canonical(self):
        findings, metrics = analyze_simulation(self.package, [], validate_static(self.package))
        self.assertTrue(metrics["simulator_trustworthy"])
        trust_findings = [f for f in findings if f.id == "SIM-TRUST-DOWNGRADE"]
        self.assertEqual(trust_findings, [])


class TestLegacyFollowUps(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.package = load_adventure("adventures/CASE_BENCHMARK_v0.4")

    def test_no_keyword_follow_ups_in_adapter(self):
        self.assertNotIn("follow_ups", self.package["adapter"])
        self.assertEqual(legacy_keyword_follow_ups(self.package["adapter"]), [])

    def test_no_legacy_followup_finding(self):
        findings, _ = analyze_simulation(self.package, [], validate_static(self.package))
        self.assertNotIn("SIM-LEGACY-FOLLOWUPS", {f.id for f in findings})


class TestExplicitFollowUps(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.package = load_adventure("adventures/CASE_BENCHMARK_v0.4")
        cls.adapter = cls.package["adapter"]
        cls.engine = SimulationEngine(cls.package, random.Random(0))

    def test_explicit_follow_up_executes(self):
        st = GameState(node="J-300", clock=1200)
        st.flags.add("CHECK_FAIL_CHK_JAMES_PRESS")
        mins = apply_follow_up(st, "FU_GYM_ALIBI", self.adapter)
        self.assertEqual(mins, 10)
        self.assertIn("C-13", st.clues)

    def test_hub_step_applies_explicit_follow_up_only(self):
        st = GameState(node="J-300", clock=1200)
        st.flags.add("CHECK_FAIL_CHK_JAMES_PRESS")

        def pick_fu(s, o, r):
            return next(x for x in o if x["id"] == "FU_GYM_ALIBI")

        st2 = self.engine.step(st, pick_fu)
        self.assertIn("C-13", st2.clues)
        self.assertEqual(st2.node, "J-300")


class TestI02RetryCost(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.package = load_adventure("adventures/CASE_BENCHMARK_v0.4")
        cls.engine = SimulationEngine(cls.package, random.Random(0))

    def test_blocked_i02_charges_minutes_once(self):
        st = GameState(node="J-410", clock=1260)
        st.clues = {"C-07"}
        clock_before = st.clock
        st2 = self.engine.step(st, lambda s, o, r: o[0] if o else {"target": s.node})
        self.assertEqual(st2.node, "J-300")
        self.assertNotIn("I-02", st2.infers_done)
        self.assertEqual(st2.clock - clock_before, 10)

    def test_successful_i02_charges_minutes_once(self):
        st = GameState(node="J-410", clock=1260)
        st.clues = {"C-05", "C-07", "C-11"}
        st.flags.add("MOTIVE_WITNESS")
        clock_before = st.clock
        st2 = self.engine.step(st, lambda s, o, r: o[0] if o else {"target": s.node})
        self.assertEqual(st2.node, "J-500")
        self.assertIn("I-02", st2.infers_done)
        self.assertEqual(st2.clock - clock_before, 10)

    def test_adapter_has_blocked_minutes(self):
        j410 = self.package["adapter"]["nodes"]["J-410"]
        self.assertEqual(j410.get("blocked_minutes"), 10)
        self.assertEqual(j410.get("blocked_return"), "J-300")


class TestP111ClosedBakeryGate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.package = load_adventure("adventures/CASE_BENCHMARK_v0.4")
        cls.engine = SimulationEngine(cls.package, random.Random(0))

    def test_phone_followup_grants_partial_c07(self):
        st = GameState(node="P-111", clock=1210)

        def pick_phone(s, o, r):
            return next(x for x in o if x["id"] == "phone_followup")

        local, mins = self.engine.run_role_path(st, "P-111", "J-200", "people", pick_phone)
        self.assertIn("C-07", local.clues)
        self.assertGreaterEqual(mins, 15)

    def test_skip_closed_no_partial_c07(self):
        st = GameState(node="P-111", clock=1210)

        def pick_skip(s, o, r):
            return next(x for x in o if x["id"] == "skip_closed")

        local, mins = self.engine.run_role_path(st, "P-111", "J-200", "people", pick_skip)
        self.assertNotIn("C-07", local.clues)


if __name__ == "__main__":
    unittest.main()
