"""D20 check tests."""

import random
import unittest

from simulator.checks import apply_check_outcome, roll_check
from simulator.loader import load_adventure
from simulator.state import GameState


class TestChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.checks = load_adventure("adventures/CASE_BENCHMARK_v0.4")["adapter"]["checks"]

    def test_roll_deterministic_with_seed(self):
        r1 = random.Random(99)
        r2 = random.Random(99)
        self.assertEqual(roll_check(r1, "people", 10), roll_check(r2, "people", 10))

    def test_pass_grants_clues(self):
        st = GameState(node="R-212a", clock=1200)
        apply_check_outcome(st, "CHK_INVOICE", True, self.checks)
        self.assertIn("C-05", st.clues)

    def test_fail_grants_alternate(self):
        st = GameState(node="R-212a", clock=1200)
        apply_check_outcome(st, "CHK_INVOICE", False, self.checks)
        self.assertIn("C-14", st.clues)
        self.assertIn("CERTAINTY_DEGRADED", st.flags)


if __name__ == "__main__":
    unittest.main()
