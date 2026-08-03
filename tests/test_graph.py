"""Graph parsing tests."""

import unittest

from simulator.graph import build_edges, graph_stats, reachable_nodes, unreachable_nodes
from simulator.loader import load_adventure


class TestGraph(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.package = load_adventure("adventures/CASE_BENCHMARK_v0.4")
        cls.adapter = cls.package["adapter"]

    def test_node_count(self):
        self.assertGreaterEqual(len(self.adapter["nodes"]), 40)

    def test_reachable_from_start(self):
        reach = reachable_nodes(self.adapter)
        self.assertIn("J-120", reach)
        self.assertIn("J-600", reach)
        self.assertIn("E-901", reach)

    def test_no_unreachable_endings(self):
        unreach = unreachable_nodes(self.adapter)
        for e in ("E-901", "E-902", "E-903", "E-904", "E-905"):
            self.assertNotIn(e, unreach)

    def test_edges_have_targets(self):
        for edge in build_edges(self.adapter):
            self.assertIn(edge.target, self.adapter["nodes"])

    def test_graph_stats(self):
        stats = graph_stats(self.adapter)
        self.assertGreater(stats["edge_count"], 50)
        self.assertGreater(stats["reachable_count"], 40)


if __name__ == "__main__":
    unittest.main()
