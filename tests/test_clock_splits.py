"""Shared clock and parallel split wall-time tests."""

import unittest

from simulator.diagnostics import run_batch
from simulator.engine import SimulationEngine
from simulator.loader import load_adventure
from simulator.strategies import get_strategy


class TestClockAndSplits(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.package = load_adventure("adventures/CASE_BENCHMARK_v0.4")

    def test_parallel_wall_clock_not_sum(self):
        rng = __import__("random").Random(7)
        engine = SimulationEngine(self.package, rng)
        strat = get_strategy("time-efficient", rng, self.package["adapter"])

        def choose(state, options, role):
            return strat.choose(state, options, role)

        final = engine.run(choose, max_steps=50)
        if final.split_segments:
            seg = final.split_segments[0]
            self.assertEqual(
                seg["wall_minutes"],
                max(seg["people_minutes"], seg["records_minutes"]) + 5,
            )

    def test_shared_world_clock_advances(self):
        results = run_batch(self.package, "clue-seeking", 5, 100)
        for r in results:
            self.assertGreater(r.wall_minutes, 0)
            self.assertLess(r.wall_minutes, 400)

    def test_deterministic_seed(self):
        a = run_batch(self.package, "random", 1, 42)[0]
        b = run_batch(self.package, "random", 1, 42)[0]
        self.assertEqual(a.ending, b.ending)
        self.assertEqual(a.clues, b.clues)


if __name__ == "__main__":
    unittest.main()
