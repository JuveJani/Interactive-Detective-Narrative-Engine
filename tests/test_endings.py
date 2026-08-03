"""Ending and simulation integration tests."""

import unittest

from simulator.diagnostics import run_batch
from simulator.endings import evaluate_ending
from simulator.loader import load_adventure
from simulator.state import GameState
from simulator.validate import validate_static


class TestEndingsAndSim(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.package = load_adventure("adventures/CASE_BENCHMARK_v0.4")
        cls.adapter = cls.package["adapter"]

    def test_timeout_ending(self):
        st = GameState(node="J-600", clock=1380)
        self.assertEqual(evaluate_ending(st, self.adapter), "E-904")

    def test_correct_ending_requires_proof(self):
        st = GameState(node="J-600", clock=1300)
        st.infers_done = {"I-03"}
        st.accused = "Tomás Reyes"
        st.clues = {
            "C-01", "C-04", "C-05", "C-06", "C-12", "C-15",
        }
        st.flags = {"MOTIVE_WITNESS"}
        self.assertEqual(evaluate_ending(st, self.adapter), "E-901")

    def test_validate_no_critical_spoiler(self):
        findings = validate_static(self.package)
        critical = [f for f in findings if f.severity == "critical"]
        self.assertEqual(len(critical), 0)

    def test_monte_carlo_completes(self):
        results = run_batch(self.package, "random", 20, 1)
        self.assertEqual(len(results), 20)
        endings = {r.ending for r in results}
        self.assertTrue(endings.issubset({"E-901", "E-902", "E-903", "E-904", "E-905"}))


if __name__ == "__main__":
    unittest.main()
