"""Tests for investigation state graph exploration."""

from __future__ import annotations

import time
import unittest
from pathlib import Path
from unittest import mock

from idne.investigation_state_graph import (
    build_investigation_state_graph,
    canonical_investigation_state_key,
)
from idne.investigation_validate import validate_investigation
from simulator_v2.human_delivery.engine import HumanDeliveryEngine
from simulator_v2.human_delivery.loader import resolve_adventure_workspace

FIXTURES = Path(__file__).resolve().parent / "fixtures"
COLD_ROOT = Path(__file__).resolve().parents[1] / "adventures" / "The_Cold_Storage_Alarm"
COLD_ADVENTURE = COLD_ROOT / "adventure"


def _knowledge_explosion_package(knowledge_count: int, **config_overrides) -> dict:
    sources = [
        {
            "knowledge_id": f"KNOW-{i}",
            "accessible": True,
            "before_inference": True,
        }
        for i in range(knowledge_count)
    ]
    cfg = {
        "max_states": 300000,
        "max_depth": 40,
    }
    cfg.update(config_overrides)
    return {
        "information_sufficiency": [{"sources": sources}],
        "recovery_routes": [],
        "state_graph_config": cfg,
    }


class TestCanonicalStateKey(unittest.TestCase):
    def test_equivalent_knowledge_orders_converge(self):
        """Requirement 1: equivalent knowledge acquisition orders share one key."""
        state_a = {
            "location": "LOC-A",
            "clock": "T0",
            "knowledge": frozenset({"K1", "K2", "K3"}),
            "checks": frozenset(),
        }
        state_b = {
            "location": "LOC-A",
            "clock": "T0",
            "knowledge": frozenset({"K3", "K1", "K2"}),
            "checks": frozenset(),
        }
        self.assertEqual(
            canonical_investigation_state_key(state_a),
            canonical_investigation_state_key(state_b),
        )

    def test_set_ordering_does_not_create_distinct_keys(self):
        """Requirement 10: unordered collection ordering differences normalize away."""
        base = {"location": "LOC-X", "clock": "T1", "checks": frozenset()}
        keys = {
            canonical_investigation_state_key({**base, "knowledge": frozenset({"A", "B", "C"})}),
            canonical_investigation_state_key({**base, "knowledge": frozenset(["C", "A", "B"])}),
            canonical_investigation_state_key({**base, "knowledge": {"B", "A", "C"}}),
        }
        self.assertEqual(len(keys), 1)

    def test_checks_difference_not_merged(self):
        """Requirement 9: capability-check dimension must not collapse distinct futures."""
        base = {"location": "LOC-X", "clock": "T0", "knowledge": frozenset({"K1"})}
        with_check = {**base, "checks": frozenset({"CHK-A"})}
        without_check = {**base, "checks": frozenset()}
        self.assertNotEqual(
            canonical_investigation_state_key(with_check),
            canonical_investigation_state_key(without_check),
        )


class TestInvestigationStateGraph(unittest.TestCase):
    def test_completes_quickly_with_many_knowledge_sources(self):
        """Requirement 4/11: large independent-fact graph completes without duplicate explosion."""
        package = _knowledge_explosion_package(18)
        start = time.perf_counter()
        result = build_investigation_state_graph(package)
        elapsed = time.perf_counter() - start
        self.assertLess(elapsed, 10.0, f"graph build took {elapsed:.2f}s")
        self.assertEqual(result.explored_states, 1 << 18)
        self.assertFalse(result.blocked)
        self.assertTrue(result.complete)
        self.assertGreater(result.duplicate_states_skipped, 0)

    def test_duplicate_child_states_rejected_before_enqueue(self):
        """Requirement 2: duplicates are skipped before queue insertion."""
        package = _knowledge_explosion_package(4)
        result = build_investigation_state_graph(package)
        self.assertEqual(result.states_scheduled, result.explored_states)
        self.assertGreater(result.duplicate_states_skipped, 0)
        self.assertLessEqual(result.peak_queue_size, result.states_scheduled)

    def test_peak_queue_bounded_relative_to_unique_states(self):
        """Requirement 5: peak queue stays near unique state count, not combinatorial duplicates."""
        package = _knowledge_explosion_package(14)
        result = build_investigation_state_graph(package)
        self.assertLessEqual(result.peak_queue_size, result.unique_states_explored + 10)
        self.assertLess(result.duplicate_states_skipped, result.attempted_transitions)

    def test_all_transition_types_use_shared_enqueue(self):
        """Requirement 3: every transition type flows through the shared bounded enqueue path."""
        package = {
            "information_sufficiency": [
                {
                    "sources": [
                        {"knowledge_id": "K1", "accessible": True, "before_inference": True},
                    ]
                }
            ],
            "recovery_routes": [
                {"zero_cost_loop": True, "destination_ref": "LOC-B"},
            ],
            "time_validation": {"deadline_clock": "T1"},
            "state_graph_config": {"max_states": 5000, "max_depth": 10},
        }
        result = build_investigation_state_graph(package)
        counts = result.transition_counts_by_type
        self.assertGreater(counts.get("knowledge_acquire", 0), 0)
        self.assertGreater(counts.get("recovery_route", 0), 0)
        self.assertGreater(counts.get("time_advance", 0), 0)
        self.assertEqual(
            sum(counts.values()),
            result.attempted_transitions,
        )

    def test_forced_explosion_short_circuits(self):
        """Requirement 8: forced explosion fixture retains BLOCKED meaning."""
        package = {
            "state_graph_config": {
                "max_states": 100,
                "max_depth": 10,
                "forced_explosion": True,
            }
        }
        result = build_investigation_state_graph(package)
        self.assertTrue(result.blocked)
        self.assertTrue(result.truncated)
        self.assertFalse(result.complete)
        self.assertEqual(result.exceeded_limit, "forced_explosion")

        res = validate_investigation(FIXTURES / "iv_state_explosion")
        self.assertEqual(res.status, "BLOCKED")
        self.assertEqual(res.checks.get("IV-STATE-GRAPH"), "BLOCKED")

    def test_transition_limit_blocks_explosion(self):
        """Requirement 6: oversized fixture terminates with structured limit finding."""
        package = _knowledge_explosion_package(20)
        package["state_graph_config"]["max_transitions"] = 100
        result = build_investigation_state_graph(package)
        self.assertTrue(result.blocked)
        self.assertTrue(result.truncated)
        self.assertIn("transition limit", result.reason)
        self.assertEqual(result.exceeded_limit, "max_transitions")
        self.assertFalse(result.complete)

    def test_depth_limit_diagnostic(self):
        """Requirement 7: shallow depth prunes expansion without hanging."""
        package = _knowledge_explosion_package(8, max_depth=2)
        result = build_investigation_state_graph(package)
        self.assertLess(result.explored_states, 1 << 8)
        self.assertLessEqual(result.maximum_depth, 2)

    def test_state_limit_diagnostic(self):
        package = _knowledge_explosion_package(10)
        package["state_graph_config"]["max_states"] = 50
        package["state_graph_config"]["max_transitions"] = 500000
        result = build_investigation_state_graph(package)
        self.assertTrue(result.blocked)
        self.assertEqual(result.exceeded_limit, "max_states")
        self.assertIn("state limit", result.reason)

    def test_diagnostics_fields_populated(self):
        package = _knowledge_explosion_package(6)
        result = build_investigation_state_graph(package)
        self.assertEqual(result.unique_states_explored, result.explored_states)
        self.assertEqual(result.maximum_depth, result.max_depth_reached)
        self.assertGreater(result.elapsed_seconds, 0.0)
        self.assertEqual(result.termination_reason, result.reason)

    def test_cold_storage_investigation_validation_completes(self):
        """Requirement 12: Cold Storage investigation validation completes."""
        if not COLD_ADVENTURE.exists():
            self.skipTest("Cold Storage adventure not present")
        start = time.perf_counter()
        res = validate_investigation(COLD_ADVENTURE)
        elapsed = time.perf_counter() - start
        self.assertLess(elapsed, 30.0, f"validation took {elapsed:.2f}s")
        sg = res.state_graph
        self.assertGreater(sg.get("unique_states_explored", 0), 0)
        self.assertEqual(res.checks.get("IV-STATE-GRAPH"), "PASS")

    def test_canonical_public_route_equivalence_completes(self):
        """Requirement 11: human-delivery canonical equivalence test completes."""
        if not COLD_ROOT.exists():
            self.skipTest("Cold Storage adventure not present")
        start = time.perf_counter()
        engine = HumanDeliveryEngine(resolve_adventure_workspace(COLD_ROOT))
        trace = engine.run_trace(strategy="human_random_legal", seed=42)
        elapsed = time.perf_counter() - start
        self.assertLess(elapsed, 30.0, f"trace took {elapsed:.2f}s")
        self.assertEqual(trace.canonical_equivalence, "PASS")

    def test_human_delivery_canonical_validation_not_rebuilt_per_step(self):
        """Requirement 13/14: canonical validation runs once per engine, not per trace step."""
        if not COLD_ROOT.exists():
            self.skipTest("Cold Storage adventure not present")
        engine = HumanDeliveryEngine(resolve_adventure_workspace(COLD_ROOT))
        with mock.patch(
            "simulator_v2.human_delivery.engine.load_simulator_package",
            wraps=__import__(
                "simulator_v2.package_loader", fromlist=["load_simulator_package"]
            ).load_simulator_package,
        ) as load_mock:
            engine.run_trace(strategy="human_random_legal", seed=42)
            self.assertEqual(load_mock.call_count, 1)


if __name__ == "__main__":
    unittest.main()
