"""Regression tests for simulator critical fixes."""

import inspect
import random
import unittest
from pathlib import Path

from simulator.diagnostics import analyze_simulation, run_batch
from simulator.endings import evaluate_ending
from simulator.engine import SimulationEngine
from simulator.loader import load_adventure
from simulator.output import make_output_dir
from simulator.self_check import SimulatorSelfCheck
from simulator.state import GameState
from simulator.strategies import ClueSeekingStrategy, get_strategy
from simulator.validate import validate_static
from simulator.checks import apply_check_outcome


class TestEndingsReachable(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.adapter = load_adventure("adventures/CASE_BENCHMARK_v0.4")["adapter"]
        cls.culprit = cls.adapter["truth"]["culprit"]

    def test_e904_timeout(self):
        st = GameState(node="J-600", clock=1380)
        self.assertEqual(evaluate_ending(st, self.adapter), "E-904")

    def test_e905_decline(self):
        st = GameState(node="J-600", clock=1300)
        st.filed_without_accusation = True
        self.assertEqual(evaluate_ending(st, self.adapter), "E-905")

    def test_e901_correct(self):
        st = GameState(node="J-600", clock=1300)
        st.infers_done = {"I-01", "I-02", "I-03"}
        st.accused = self.culprit
        st.clues = {"C-01", "C-04", "C-05", "C-06", "C-12"}
        st.flags = {"MOTIVE_WITNESS"}
        self.assertEqual(evaluate_ending(st, self.adapter), "E-901")

    def test_e902_wrong_with_proof(self):
        st = GameState(node="J-600", clock=1300)
        st.infers_done = {"I-03"}
        st.accused = "Mira Kwan"
        st.clues = {"C-01", "C-04", "C-05", "C-06", "C-12"}
        self.assertEqual(evaluate_ending(st, self.adapter), "E-902")

    def test_e903_incomplete(self):
        st = GameState(node="J-600", clock=1300)
        st.accused = self.culprit
        st.infers_done = {"I-03"}
        st.clues = {"C-01"}
        self.assertEqual(evaluate_ending(st, self.adapter), "E-903")

    def test_timeout_beats_decline(self):
        st = GameState(node="J-600", clock=1380)
        st.filed_without_accusation = True
        self.assertEqual(evaluate_ending(st, self.adapter), "E-904")


class TestEngineE901(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.package = load_adventure("adventures/CASE_BENCHMARK_v0.4")

    def test_j510_marks_i03_after_accusation(self):
        engine = SimulationEngine(self.package, random.Random(0))
        st = GameState(node="J-510", clock=1300)
        st.clues = {"C-01", "C-04", "C-05", "C-06", "C-12"}
        st.flags = {"MOTIVE_WITNESS"}
        st.infers_done = {"I-01", "I-02"}

        def accuse(s, o, r):
            return {"target": self.package["adapter"]["truth"]["culprit"]}

        st2 = engine.step(st, accuse)
        self.assertIn("I-03", st2.infers_done)
        self.assertEqual(st2.node, "J-600")
        self.assertEqual(evaluate_ending(st2, self.package["adapter"]), "E-901")


class TestHubCostOnce(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.package = load_adventure("adventures/CASE_BENCHMARK_v0.4")
        cls.engine = SimulationEngine(cls.package, random.Random(1))

    def test_stairwell_charged_once(self):
        st = self.engine.new_state()
        while st.node != "J-120":
            st = self.engine.step(st, lambda s, o, r: o[0] if o else {"target": st.node})
        clock_before = st.clock

        def pick_stairwell(s, o, r):
            return next(x for x in o if x["id"] == "stairwell")

        st = self.engine.step(st, pick_stairwell)
        self.assertEqual(st.node, "J-110")
        self.assertEqual(st.clock - clock_before, 15)
        st = self.engine.step(st, pick_stairwell)
        self.assertEqual(st.node, "J-120")
        self.assertEqual(st.clock - clock_before, 15)
        self.assertIn("C-01", st.clues)


class TestSplitWindowLocal(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.package = load_adventure("adventures/CASE_BENCHMARK_v0.4")

    def test_two_splits_use_window_local_maxima(self):
        engine = SimulationEngine(self.package, random.Random(99))

        def split1_choose(s, o, r):
            if r == "people":
                if s.node == "P-111":
                    return {"id": "rent", "target": "P-111a"}
                return {"target": "P-113"}
            if s.node == "R-111":
                return {"id": "logs", "target": "R-111b"}
            return {"target": "R-114"}

        st = engine.new_state()
        st.node = "J-130"
        st = engine.resolve_split(st, "split1", split1_choose)
        seg1 = st.split_segments[-1]
        self.assertEqual(seg1["wall_minutes"], max(seg1["people_minutes"], seg1["records_minutes"]) + 5)

        st.node = "J-330"
        st = engine.resolve_split(st, "split2", split1_choose)
        seg2 = st.split_segments[-1]
        self.assertEqual(seg2["wall_minutes"], max(seg2["people_minutes"], seg2["records_minutes"]) + 5)
        self.assertLess(seg2["people_minutes"], seg1["people_minutes"] + 40)


class TestCheckFailTiming(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.checks = load_adventure("adventures/CASE_BENCHMARK_v0.4")["adapter"]["checks"]

    def test_invoice_fail_extra_once(self):
        st = GameState(node="R-212a", clock=1200)
        extra = apply_check_outcome(st, "CHK_INVOICE", False, self.checks)
        self.assertEqual(extra, 15)


class TestHiddenInformation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.package = load_adventure("adventures/CASE_BENCHMARK_v0.4")

    def test_public_options_no_grants_clues(self):
        engine = SimulationEngine(self.package, random.Random(0))
        opts = engine.public_options(self.package["adapter"]["nodes"]["J-120"]["choices"])
        for o in opts:
            self.assertNotIn("grants_clues", o)

    def test_strategy_source_no_culprit_hardcode(self):
        src = inspect.getsource(ClueSeekingStrategy)
        self.assertNotIn("Tomás", src)
        src_base = inspect.getsource(ClueSeekingStrategy.pick_accused)
        self.assertNotIn("C-15", src_base)

    def test_pick_accused_no_truth_access(self):
        strat = ClueSeekingStrategy(random.Random(0), self.package["adapter"])
        st = GameState(node="J-510", clock=1300)
        st.clues = {"C-06", "C-12", "C-15"}
        name = strat.pick_accused(st)
        self.assertIn(name, self.package["adapter"]["suspects"])


class TestDiagnosticsGates(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.package = load_adventure("adventures/CASE_BENCHMARK_v0.4")

    def test_self_check_passes(self):
        self.assertTrue(SimulatorSelfCheck(self.package).run_all())

    def test_no_win_not_adventure_when_engine_fails(self):
        findings, _ = analyze_simulation(self.package, [], validate_static(self.package))
        layers = {f.id: f.layer for f in findings}
        self.assertNotEqual(layers.get("SIM-NO-WIN"), "ADVENTURE")


class TestOutputFolders(unittest.TestCase):
    def test_unique_folders(self):
        a = make_output_dir(mode="test_a")
        b = make_output_dir(mode="test_b")
        self.assertNotEqual(a, b)


class TestDeterministicSeeds(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.package = load_adventure("adventures/CASE_BENCHMARK_v0.4")

    def test_same_seed_same_result(self):
        a = run_batch(self.package, "random", 1, 42)[0]
        b = run_batch(self.package, "random", 1, 42)[0]
        self.assertEqual(a.ending, b.ending)
        self.assertEqual(a.clues, b.clues)


class TestI02Block(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.package = load_adventure("adventures/CASE_BENCHMARK_v0.4")

    def test_incomplete_i02_returns_to_hub(self):
        engine = SimulationEngine(self.package, random.Random(0))
        st = GameState(node="J-410", clock=1260)
        st.clues = {"C-07"}
        clock_before = st.clock
        st2 = engine.step(st, lambda s, o, r: o[0] if o else {"target": s.node})
        self.assertEqual(st2.node, "J-300")
        self.assertNotIn("I-02", st2.infers_done)
        self.assertEqual(st2.clock - clock_before, 10)


if __name__ == "__main__":
    unittest.main()
