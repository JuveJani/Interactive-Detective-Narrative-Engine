"""Tests for explainer, repair advisor, V2 blockers, and advisory CLI."""

import json
import random
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from simulator.advisory_output import write_advisory_outputs
from simulator.ai_context import write_ai_context
from simulator.commands import cmd_explain, cmd_export_ai_context, cmd_repair_plan
from simulator.diagnostics import analyze_simulation, run_batch
from simulator.endings import evaluate_ending
from simulator.engine import SimulationEngine, SimulationLimitError
from simulator.explainer import explain_all, explain_finding
from simulator.loader import load_adventure
from simulator.models import Finding
from simulator.repair_advisor import all_repair_options, repair_options_for_finding
from simulator.self_check import simulator_trustworthy
from simulator.state import GameState
from simulator.strategies import PoorDecisionsStrategy
from simulator.validate import validate_static


class TestDeadlineBehavior(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.package = load_adventure("adventures/CASE_BENCHMARK_v0.4")
        cls.engine = SimulationEngine(cls.package, random.Random(0))

    def test_hub_at_deadline_only_decline_or_timeout(self):
        st = GameState(node="J-500", clock=1380)
        spec = self.package["adapter"]["nodes"]["J-500"]
        opts = self.engine.hub_options(st, spec)
        ids = {o["id"] for o in opts}
        self.assertIn("decline", ids)
        self.assertNotIn("accuse", ids)

    def test_run_forces_timeout_ending(self):
        st = self.engine.new_state()
        st.clock = 1380
        st.node = "J-500"

        def noop(s, o, r):
            return o[0] if o else {"target": "J-600", "id": "decline"}

        st2 = self.engine.step(st, noop)
        self.assertEqual(st2.node, "J-600")
        ending = evaluate_ending(st2, self.package["adapter"])
        self.assertEqual(ending, "E-904")


class TestHubRevisit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.package = load_adventure("adventures/CASE_BENCHMARK_v0.4")
        cls.engine = SimulationEngine(cls.package, random.Random(2))

    def test_stairwell_revisit_returns_to_hub2(self):
        st = GameState(node="J-300", clock=1200)
        st.hub_visits = {2: set()}

        def pick_revisit(s, o, r):
            return next(x for x in o if x["id"] == "stairwell_revisit")

        st = self.engine.step(st, pick_revisit)
        self.assertEqual(st.node, "J-110")
        self.assertEqual(st.return_hub, "J-300")
        st = self.engine.step(st, pick_revisit)
        self.assertEqual(st.node, "J-300")


class TestFollowUpJames(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.package = load_adventure("adventures/CASE_BENCHMARK_v0.4")

    def test_pending_followup_routes_to_p214(self):
        engine = SimulationEngine(self.package, random.Random(0))
        local, _ = engine.run_role_path(
            GameState(node="P-211a", clock=1200),
            "P-211a",
            "J-400",
            "people",
            lambda s, o, r: o[0],
        )
        local.pending_followup = "P-214"
        local2, mins = engine.run_role_path(local, "P-211a", "J-400", "people", lambda s, o, r: o[0])
        path_nodes = [p.split(":")[-1] for p in local2.path]
        self.assertIn("P-214", path_nodes)


class TestTrustDowngrade(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.package = load_adventure("adventures/CASE_BENCHMARK_v0.4")

    def test_simulator_not_trustworthy_with_ambiguities(self):
        ok, blockers = simulator_trustworthy(self.package["adapter"])
        self.assertFalse(ok)
        self.assertTrue(blockers)

    def test_fake_findings_undetermined_when_untrusted(self):
        findings, metrics = analyze_simulation(self.package, [], validate_static(self.package))
        fake = [f for f in findings if f.id.startswith("SIM-FAKE-")]
        self.assertTrue(fake)
        for f in fake:
            self.assertEqual(f.layer, "UNDETERMINED")


class TestExplainer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.package = load_adventure("adventures/CASE_BENCHMARK_v0.4")

    def test_explanation_has_required_fields(self):
        findings, metrics = analyze_simulation(self.package, [], validate_static(self.package))
        expl = explain_finding(findings[0], metrics, self.package["adapter"])
        self.assertTrue(expl.plain_problem)
        self.assertTrue(expl.where_to_look)
        self.assertTrue(expl.validation_after_repair)

    def test_simple_language_no_abbreviations_in_template(self):
        findings, metrics = analyze_simulation(self.package, [], validate_static(self.package))
        for expl in explain_all(findings[:3], metrics, self.package["adapter"]):
            self.assertNotIn("UNDET", expl.plain_problem)

    def test_deterministic_explanations(self):
        findings, metrics = analyze_simulation(self.package, [], validate_static(self.package))
        a = explain_all(findings, metrics, self.package["adapter"])
        b = explain_all(findings, metrics, self.package["adapter"])
        self.assertEqual([x.to_dict() for x in a], [x.to_dict() for x in b])


class TestRepairAdvisor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.package = load_adventure("adventures/CASE_BENCHMARK_v0.4")

    def test_repair_options_generated(self):
        findings, metrics = analyze_simulation(self.package, [], validate_static(self.package))
        expl = explain_all(findings, metrics, self.package["adapter"])
        opts = all_repair_options(findings, expl)
        self.assertTrue(opts)
        for o in opts:
            self.assertTrue(o.option_id.startswith("REP-"))

    def test_no_engine_change_for_adventure_only(self):
        f = Finding(
            id="SIM-FAKE-J-122",
            severity="minor",
            confidence="medium",
            evidence="test",
            file="sim_adapter.json",
            identifier="J-122",
            expected_rule="test",
            layer="ADVENTURE",
            auto_fix_possible=False,
            human_approval_required=True,
        )
        expl = explain_finding(f, {"simulator_trustworthy": False}, self.package["adapter"])
        opts = repair_options_for_finding(f, expl)
        for o in opts:
            self.assertFalse(o.changes_engine)

    def test_no_story_invention_in_context(self):
        findings, metrics = analyze_simulation(self.package, [], validate_static(self.package))
        expl = explain_all(findings[:1], metrics, self.package["adapter"])
        opts = all_repair_options(findings[:1], expl)
        with tempfile.TemporaryDirectory() as td:
            out = Path(td)
            (out / "findings.json").write_text(json.dumps([findings[0].to_dict()]), encoding="utf-8")
            (out / "metrics.json").write_text(json.dumps(metrics), encoding="utf-8")
            write_ai_context(out, findings[:1], expl, opts, metrics, self.package["adapter"])
            ctx = json.loads((out / "local_ai_context" / f"finding_context_{findings[0].id}.json").read_text())
            self.assertIn("do_not_invent", ctx)


class TestAdvisoryCLI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.package = load_adventure("adventures/CASE_BENCHMARK_v0.4")

    def test_explain_command_writes_files(self):
        findings, metrics = analyze_simulation(self.package, [], validate_static(self.package))
        metrics["adapter_snapshot"] = self.package["adapter"]
        with tempfile.TemporaryDirectory() as td:
            out = Path(td)
            (out / "findings.json").write_text(
                json.dumps([f.to_dict() for f in findings]), encoding="utf-8"
            )
            (out / "metrics.json").write_text(json.dumps(metrics), encoding="utf-8")
            cmd_explain(str(out))
            self.assertTrue((out / "executive_diagnostic.md").exists())
            self.assertTrue((out / "explanations").is_dir())

    def test_export_ai_context_command(self):
        findings, metrics = analyze_simulation(self.package, [], validate_static(self.package))
        metrics["adapter_snapshot"] = self.package["adapter"]
        with tempfile.TemporaryDirectory() as td:
            out = Path(td)
            (out / "findings.json").write_text(
                json.dumps([f.to_dict() for f in findings[:1]]), encoding="utf-8"
            )
            (out / "metrics.json").write_text(json.dumps(metrics), encoding="utf-8")
            ctx = cmd_export_ai_context(str(out), findings[0].id)
            self.assertTrue((ctx / f"finding_context_{findings[0].id}.md").exists())

    def test_repair_plan_no_repo_modification(self):
        findings, metrics = analyze_simulation(self.package, [], validate_static(self.package))
        metrics["adapter_snapshot"] = self.package["adapter"]
        repo_file = Path("adventures/CASE_BENCHMARK_v0.4/sim_adapter.json")
        mtime_before = repo_file.stat().st_mtime
        with tempfile.TemporaryDirectory() as td:
            out = Path(td)
            (out / "findings.json").write_text(
                json.dumps([f.to_dict() for f in findings[:1]]), encoding="utf-8"
            )
            (out / "metrics.json").write_text(json.dumps(metrics), encoding="utf-8")
            cmd_repair_plan(str(out), findings[0].id)
        self.assertEqual(repo_file.stat().st_mtime, mtime_before)


class TestMaxStates(unittest.TestCase):
    def test_max_states_raises(self):
        from simulator.config import SimConfig

        package = load_adventure("adventures/CASE_BENCHMARK_v0.4")
        cfg = SimConfig(max_states=5)
        engine = SimulationEngine(package, random.Random(0), cfg)
        with self.assertRaises(SimulationLimitError):
            engine.run(lambda s, o, r: o[0] if o else {"target": s.node})


class TestPoorDecisionsGeneric(unittest.TestCase):
    def test_accuse_not_hardcoded_to_last_suspect(self):
        adapter = {
            "suspects": ["A", "B", "C", "D"],
            "strategy_hints": {},
            "nodes": {},
        }
        strat = PoorDecisionsStrategy(random.Random(1), adapter)
        picks = {strat.choose(GameState("J-510", 1200), [], "accuse")["target"] for _ in range(50)}
        self.assertIn("D", picks)


class TestFictionMinutesBounded(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.package = load_adventure("adventures/CASE_BENCHMARK_v0.4")

    def test_deadline_caps_fiction_minutes(self):
        runs = run_batch(self.package, "clue-seeking", 20, 99)
        max_fiction = self.package["adapter"]["deadline_clock"] - self.package["adapter"]["start_clock"]
        for r in runs:
            self.assertLessEqual(r.fiction_minutes, max_fiction)


class TestInterruptedRecovery(unittest.TestCase):
    def test_partial_output_still_explainable(self):
        package = load_adventure("adventures/CASE_BENCHMARK_v0.4")
        findings, metrics = analyze_simulation(package, [], validate_static(package))
        metrics["adapter_snapshot"] = package["adapter"]
        with tempfile.TemporaryDirectory() as td:
            out = Path(td)
            (out / "findings.json").write_text(
                json.dumps([f.to_dict() for f in findings]), encoding="utf-8"
            )
            (out / "metrics.json").write_text(json.dumps(metrics), encoding="utf-8")
            write_advisory_outputs(out, findings, metrics, package["adapter"])
            self.assertTrue((out / "repair_options.json").exists())
            cmd_explain(str(out))


if __name__ == "__main__":
    unittest.main()
