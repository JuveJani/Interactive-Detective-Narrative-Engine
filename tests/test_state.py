"""State and proof tag tests."""

import unittest

from simulator.loader import load_adventure
from simulator.state import GameState


class TestState(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.adapter = load_adventure("adventures/CASE_BENCHMARK_v0.4")["adapter"]

    def test_proof_method(self):
        st = GameState(node="J-500", clock=1200)
        st.clues = {"C-01", "C-04"}
        tags = st.compute_proof_tags(self.adapter)
        self.assertTrue(tags["PROOF_METHOD"])

    def test_proof_motive_witness_combo(self):
        st = GameState(node="J-500", clock=1200)
        st.clues = {"C-14"}
        st.flags = {"MOTIVE_WITNESS"}
        tags = st.compute_proof_tags(self.adapter)
        self.assertTrue(tags["PROOF_MOTIVE"])

    def test_infer_i01_requires_clues(self):
        st = GameState(node="J-210", clock=1200)
        st.clues = {"C-01"}
        self.assertFalse(st.can_complete_infer("I-01", self.adapter))
        st.clues.add("C-06")
        self.assertTrue(st.can_complete_infer("I-01", self.adapter))

    def test_clue_idempotent(self):
        st = GameState(node="J-110", clock=1140)
        self.assertTrue(st.grant_clue("C-01"))
        self.assertFalse(st.grant_clue("C-01"))


if __name__ == "__main__":
    unittest.main()
