"""Tests for NPC Investigation System (Milestone 5B)."""

import unittest
from pathlib import Path

from idne.npc_investigation_validate import validate_npc_investigation

FIXTURES = Path(__file__).resolve().parent / "fixtures"
HARBORVIEW = Path(__file__).resolve().parents[1] / "adventures" / "CASE_BENCHMARK_v0.4"


class TestNpcInvestigationFixtures(unittest.TestCase):
    def test_valid_minimal_passes(self):
        res = validate_npc_investigation(FIXTURES / "npc_valid_minimal")
        self.assertEqual(res.status, "PASS")
        self.assertEqual(res.checks.get("NPC-PKG-PRESENT"), "PASS")
        self.assertEqual(res.checks.get("NPC-STATIC"), "PASS")
        self.assertEqual(res.checks.get("NPC-TRUST"), "PASS")

    def test_missing_static_fails(self):
        res = validate_npc_investigation(FIXTURES / "npc_missing_static")
        self.assertEqual(res.status, "FAIL")
        self.assertEqual(res.checks.get("NPC-STATIC"), "FAIL")

    def test_orphan_graph_fails(self):
        res = validate_npc_investigation(FIXTURES / "npc_orphan_graph")
        self.assertEqual(res.status, "FAIL")
        self.assertEqual(res.checks.get("NPC-GRAPH"), "FAIL")

    def test_topic_no_unlock_fails(self):
        res = validate_npc_investigation(FIXTURES / "npc_topic_no_unlock")
        self.assertEqual(res.status, "FAIL")
        self.assertEqual(res.checks.get("NPC-TOPIC-UNLOCK"), "FAIL")

    def test_conversation_no_route_fails(self):
        res = validate_npc_investigation(FIXTURES / "npc_conversation_no_route")
        self.assertEqual(res.status, "FAIL")
        self.assertEqual(res.checks.get("NPC-CONVERSATION"), "FAIL")

    def test_info_invalid_knowledge_fails(self):
        res = validate_npc_investigation(FIXTURES / "npc_info_invalid_knowledge")
        self.assertEqual(res.status, "FAIL")
        self.assertEqual(res.checks.get("NPC-INFO-KNOWN"), "FAIL")

    def test_trust_positive_only_fails(self):
        res = validate_npc_investigation(FIXTURES / "npc_trust_positive_only")
        self.assertEqual(res.status, "FAIL")
        self.assertEqual(res.checks.get("NPC-TRUST"), "FAIL")

    def test_reaction_invalid_npc_fails(self):
        res = validate_npc_investigation(FIXTURES / "npc_reaction_invalid_npc")
        self.assertEqual(res.status, "FAIL")
        self.assertEqual(res.checks.get("NPC-RELATION-REACT"), "FAIL")

    def test_empty_conversation_nodes_fails(self):
        res = validate_npc_investigation(FIXTURES / "npc_empty_conversation_nodes")
        self.assertEqual(res.status, "FAIL")
        self.assertEqual(res.checks.get("NPC-CONVERSATION"), "FAIL")

    def test_harborview_skips(self):
        if not HARBORVIEW.exists():
            self.skipTest("no harborview")
        res = validate_npc_investigation(HARBORVIEW)
        self.assertEqual(res.status, "SKIP")


if __name__ == "__main__":
    unittest.main()
