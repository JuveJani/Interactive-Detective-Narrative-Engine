"""Regression tests for offline explainer review fixes."""

import json
import random
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from simulator.commands import cmd_repair_plan
from simulator.diagnostics import analyze_simulation, run_batch
from simulator.engine import SimulationEngine
from simulator.explainer import explain_all
from simulator.follow_ups import apply_follow_up, eligible_follow_up_options
from simulator.loader import load_adventure
from simulator.models import Finding, RunResult
from simulator.repair_plan import write_finding_repair_plan
from simulator.state import GameState
from simulator.validate import validate_static
from simulator.ai_context import build_finding_context
from simulator.repair_advisor import all_repair_options
from simulator.explainer import explain_finding


class TestFollowUpActions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.package = load_adventure("adventures/CASE_BENCHMARK_v0.4")
        cls.adapter = cls.package["adapter"]
        cls.engine = SimulationEngine(cls.package, random.Random(0))

    def test_eligible_follow_up_activates(self):
        st = GameState(node="J-300", clock=1200)
        st.flags.add("CHECK_FAIL_CHK_JAMES_PRESS")
        opts = eligible_follow_up_options(st, "J-300", self.adapter)
        ids = {o["id"] for o in opts}
        self.assertIn("FU_GYM_ALIBI", ids)

    def test_ineligible_when_clue_present(self):
        st = GameState(node="J-300", clock=1200)
        st.flags.add("CHECK_FAIL_CHK_JAMES_PRESS")
        st.clues.add("C-13")
        opts = eligible_follow_up_options(st, "J-300", self.adapter)
        self.assertNotIn("FU_GYM_ALIBI", {o["id"] for o in opts})

    def test_max_count_enforced(self):
        st = GameState(node="J-300", clock=1200)
        st.follow_ups_used = self.adapter["follow_up_max"]
        opts = eligible_follow_up_options(st, "J-300", self.adapter)
        self.assertEqual(opts, [])

    def test_follow_up_cost_and_effect_once(self):
        st = GameState(node="J-300", clock=1200)
        st.flags.add("CHECK_FAIL_CHK_JAMES_PRESS")
        clock_before = st.clock
        mins = apply_follow_up(st, "FU_GYM_ALIBI", self.adapter)
        self.assertEqual(mins, 10)
        self.assertIn("C-13", st.clues)
        self.assertEqual(st.follow_up_use_counts.get("FU_GYM_ALIBI"), 1)
        mins2 = apply_follow_up(st, "FU_GYM_ALIBI", self.adapter)
        self.assertEqual(mins2, 0)

    def test_no_hidden_grants_in_public_options(self):
        st = GameState(node="J-300", clock=1200)
        st.flags.add("CHECK_FAIL_CHK_JAMES_PRESS")
        opts = eligible_follow_up_options(st, "J-300", self.adapter)
        for o in opts:
            self.assertNotIn("grants_clues", o)
            self.assertNotIn("grants_clues_if_missing", o)

    def test_hub_step_applies_follow_up(self):
        st = GameState(node="J-300", clock=1200)
        st.flags.add("CHECK_FAIL_CHK_JAMES_PRESS")

        def pick_fu(s, o, r):
            return next(x for x in o if x["id"] == "FU_GYM_ALIBI")

        st2 = self.engine.step(st, pick_fu)
        self.assertEqual(st2.node, "J-300")
        self.assertIn("C-13", st2.clues)


class TestZeroWinDiagnostics(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.package = load_adventure("adventures/CASE_BENCHMARK_v0.4")

    def test_zero_success_untrusted_emits_finding(self):
        adapter = dict(self.package["adapter"])
        adapter["ambiguities"] = ["forced for untrusted test"]
        pkg = dict(self.package)
        pkg["adapter"] = adapter
        runs = [
            RunResult(0, "random", "E-904", 10, 200, 0, 200, 240, [], [], [], None, [], []),
        ] * 5
        findings, _ = analyze_simulation(pkg, runs, validate_static(pkg))
        ids = {f.id for f in findings}
        self.assertIn("SIM-NO-WIN-UNTRUSTED", ids)
        f = next(x for x in findings if x.id == "SIM-NO-WIN-UNTRUSTED")
        self.assertEqual(f.layer, "UNDETERMINED")

    def test_rare_win_untrusted_emits_info(self):
        adapter = dict(self.package["adapter"])
        adapter["ambiguities"] = ["forced for untrusted test"]
        pkg = dict(self.package)
        pkg["adapter"] = adapter
        runs = [
            RunResult(0, "random", "E-901", 10, 200, 0, 200, 240, [], [], [], None, [], []),
            RunResult(1, "random", "E-904", 10, 200, 0, 200, 240, [], [], [], None, [], []),
        ]
        findings, _ = analyze_simulation(pkg, runs, validate_static(pkg))
        self.assertIn("SIM-WIN-UNTRUSTED", {f.id for f in findings})

    def test_trusted_zero_win_layer_undetermined(self):
        adapter = dict(self.package["adapter"])
        adapter["ambiguities"] = []
        adapter["simulator_partial"] = []
        adapter["simulator_unsupported"] = []
        pkg = dict(self.package)
        pkg["adapter"] = adapter
        runs = [RunResult(0, "random", "E-904", 10, 200, 0, 200, 240, [], [], [], None, [], [])] * 3
        findings, metrics = analyze_simulation(pkg, runs, [])
        if metrics["simulator_trustworthy"]:
            f = next((x for x in findings if x.id == "SIM-NO-WIN"), None)
            self.assertIsNotNone(f)
            self.assertEqual(f.layer, "UNDETERMINED")


class TestRepairPlanBacklog(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.package = load_adventure("adventures/CASE_BENCHMARK_v0.4")

    def test_repair_plan_preserves_backlog(self):
        runs = run_batch(self.package, "random", 5, 42)
        findings, metrics = analyze_simulation(self.package, runs, validate_static(self.package))
        metrics["adapter_snapshot"] = self.package["adapter"]
        with tempfile.TemporaryDirectory() as td:
            out = Path(td)
            (out / "findings.json").write_text(
                json.dumps([f.to_dict() for f in findings]), encoding="utf-8"
            )
            (out / "metrics.json").write_text(json.dumps(metrics), encoding="utf-8")
            from simulator.advisory_output import write_advisory_outputs
            from simulator.repair_advisor import all_repair_options
            from simulator.explainer import explain_all

            expl = explain_all(findings, metrics, self.package["adapter"])
            opts = all_repair_options(findings, expl)
            write_advisory_outputs(out, findings, metrics, self.package["adapter"], opts)
            backlog_before = (out / "repair_backlog.md").read_text()
            options_before = json.loads((out / "repair_options.json").read_text())
            cmd_repair_plan(str(out), "SIM-FAKE-J-122")
            backlog_after = (out / "repair_backlog.md").read_text()
            options_after = json.loads((out / "repair_options.json").read_text())
            self.assertEqual(backlog_before, backlog_after)
            self.assertEqual(len(options_before), len(options_after))
            self.assertTrue((out / "repair_plan_SIM-FAKE-J-122.md").exists())
            self.assertTrue((out / "repair_plan_SIM-FAKE-J-122.json").exists())

    def test_repair_plan_idempotent(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td)
            findings = [
                Finding(
                    id="SIM-FAKE-J-122",
                    severity="minor",
                    confidence="low",
                    evidence="test",
                    file="sim_adapter.json",
                    identifier="J-122",
                    expected_rule="rule",
                    layer="UNDETERMINED",
                    auto_fix_possible=False,
                    human_approval_required=True,
                )
            ]
            metrics = {"simulator_trustworthy": False, "trust_blockers": ["test"]}
            (out / "findings.json").write_text(json.dumps([f.to_dict() for f in findings]))
            (out / "metrics.json").write_text(json.dumps(metrics))
            cmd_repair_plan(str(out), "SIM-FAKE-J-122")
            first = (out / "repair_plan_SIM-FAKE-J-122.json").read_text()
            cmd_repair_plan(str(out), "SIM-FAKE-J-122")
            second = (out / "repair_plan_SIM-FAKE-J-122.json").read_text()
            self.assertEqual(first, second)


class TestAIContextSections(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.package = load_adventure("adventures/CASE_BENCHMARK_v0.4")

    def test_trust_context_has_resolved_ambiguities(self):
        findings, metrics = analyze_simulation(self.package, [], validate_static(self.package))
        self.assertTrue(metrics["simulator_trustworthy"])
        adapter = dict(self.package["adapter"])
        adapter["ambiguities"] = ["forced ambiguity"]
        pkg = dict(self.package)
        pkg["adapter"] = adapter
        findings2, metrics2 = analyze_simulation(pkg, [], validate_static(pkg))
        trust = next(f for f in findings2 if f.id == "SIM-TRUST-DOWNGRADE")
        expl = explain_finding(trust, metrics2, adapter)
        opts = all_repair_options(findings2, [expl])
        ctx = build_finding_context(trust, expl, opts, metrics2, adapter)
        self.assertIn("PROVEN_FACTS", ctx)
        self.assertIn("FORBIDDEN_CONCLUSIONS", ctx)
        self.assertTrue(ctx["AMBIGUITIES"])
        self.assertNotIn("culprit", json.dumps(ctx).lower())


class TestExecutiveQuantitativeTrust(unittest.TestCase):
    def test_summary_untrusted_banner(self):
        from simulator.output import write_summary
        from simulator.models import Finding
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "summary.md"
            write_summary(
                {"runs": 10, "simulator_trustworthy": False, "trust_blockers": ["test blocker"], "ending_distribution": {"E-904": 10}},
                [],
                p,
                "simulate",
            )
            text = p.read_text()
            self.assertIn("UNTRUSTED", text)
            self.assertIn("test blocker", text)


if __name__ == "__main__":
    unittest.main()
