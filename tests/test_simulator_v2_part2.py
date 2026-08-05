"""Tests for Simulator v2 Part 2 — execution, strategies, modes, trust."""

from __future__ import annotations

import unittest
from pathlib import Path

from simulator_v2.action_enumerator import enumerate_legal_actions
from simulator_v2.actions import ActionKind
from simulator_v2.derivation import derive_simulation_model
from simulator_v2.engine import EngineConfig, SimulationEngine
from simulator_v2.modes import ExhaustiveConfig, SimulationModes
from simulator_v2.package_loader import load_simulator_package
from simulator_v2.player_view import PlayerView
from simulator_v2.rng import DeterministicRNG
from simulator_v2.state import initial_state_from_model
from simulator_v2.strategies import STRATEGIES, create_strategy
from simulator_v2.trust_gate import evaluate_trust

FIXTURES = Path(__file__).resolve().parent / "fixtures"
SOLO = FIXTURES / "sim_v2_solo"
TWO = FIXTURES / "sim_v2_two_player"


def _engine(path: Path = SOLO) -> tuple[SimulationEngine, object]:
    load = load_simulator_package(path)
    model = derive_simulation_model(load.adventure_root, load.play_mode)
    return SimulationEngine(model), model


class TestSimulatorV2Part2(unittest.TestCase):
    def setUp(self) -> None:
        self.engine, self.model = _engine()
        self.rng = DeterministicRNG(1)

    def _step(self, state, action_id: str, *, seed: int = 1):
        return self.engine.step(state, action_id, DeterministicRNG(seed))

    def test_legal_action_fields(self):
        state = self.engine.initial_state()
        legal = self.engine.legal_actions(state)
        self.assertTrue(legal)
        action = legal[0]
        self.assertTrue(action.player_label)
        self.assertTrue(action.eligibility_reason)
        self.assertIsInstance(action.time_cost_minutes, int)
        self.assertTrue(action.canonical_source_id)
        self.assertIn(action.repeat_policy, ("allowed", "once"))

    def test_illegal_action_rejected(self):
        state = self.engine.initial_state()
        with self.assertRaises(ValueError):
            self.engine.step(state, "obj:ACT-NOT-EXIST", self.rng)

    def test_persistent_revisit(self):
        state = self.engine.initial_state()
        state, _ = self._step(state, "nav:NAV-LOBBY-OFFICE")
        state, _ = self._step(state, "nav:NAV-OFFICE-LOBBY")
        self.assertIn("LOC-OFFICE", state.ending_chain_state["visited_locations"])
        counts = state.ending_chain_state["revisit_counts"]
        self.assertGreaterEqual(counts.get("LOC-OFFICE", 0), 1)
        state, _ = self._step(state, "nav:NAV-LOBBY-OFFICE")
        self.assertGreater(counts.get("LOC-OFFICE", 0), 1)

    def test_time_based_location_variant(self):
        state = self.engine.initial_state()
        self.assertFalse(state.flow_flags.get("basement_open"))
        for clock in ("T1", "T2"):
            legal = self.engine.legal_actions(state)
            time_act = next(a for a in legal if a.action_id == f"time:{clock}")
            state, _ = self.engine.step(state, time_act.action_id, self.rng)
        self.assertEqual(state.in_world_clock, "T2")
        self.assertTrue(state.flow_flags.get("basement_open"))

    def test_nested_objects(self):
        state = self.engine.initial_state()
        state, _ = self._step(state, "nav:NAV-LOBBY-OFFICE")
        before = {a.action_id for a in self.engine.legal_actions(state)}
        self.assertNotIn("obj:ACT-LOGIN-COMPUTER", before)
        state, _ = self._step(state, "obj:ACT-APPROACH-DESK")
        after = {a.action_id for a in self.engine.legal_actions(state)}
        self.assertIn("obj:ACT-LOGIN-COMPUTER", after)

    def test_item_removal_after_acquisition(self):
        state = self.engine.initial_state()
        state, _ = self._step(state, "nav:NAV-LOBBY-OFFICE")
        state, _ = self._step(state, "obj:ACT-APPROACH-DESK")
        state, meta = self._step(state, "obj:ACT-SEARCH-DESK")
        self.assertTrue(meta.get("check_success"))
        self.assertIn("ITEM-KEY", state.items)
        self.assertEqual(state.object_states.get("OBJ-KEY-HIDDEN"), "collected")
        legal_ids = {a.action_id for a in self.engine.legal_actions(state)}
        self.assertFalse(any("OBJ-KEY-HIDDEN" in a for a in legal_ids))

    def test_one_attempt_check(self):
        state = self.engine.initial_state()
        state, _ = self._step(state, "nav:NAV-LOBBY-OFFICE")
        state, _ = self._step(state, "obj:ACT-APPROACH-DESK")
        state, _ = self._step(state, "obj:ACT-SEARCH-DESK", seed=99)
        legal = self.engine.legal_actions(state)
        self.assertNotIn("obj:ACT-SEARCH-DESK", [a.action_id for a in legal])

    def test_failed_check_information_protection(self):
        state = self.engine.initial_state()
        state, _ = self._step(state, "nav:NAV-LOBBY-OFFICE")
        state, _ = self._step(state, "obj:ACT-APPROACH-DESK")
        state, meta = self._step(state, "obj:ACT-SEARCH-DESK", seed=2)
        self.assertFalse(meta.get("check_success"))
        self.assertFalse(meta.get("failure_leaked"))
        self.assertNotIn("KNOW-001", state.player_knowledge)
        self.assertNotIn("ITEM-KEY", state.items)

    def test_npc_trust_gate(self):
        state = self.engine.initial_state()
        state.npc_dynamic["NPC-B"]["trust"] = 10
        legal = self.engine.legal_actions(state)
        self.assertNotIn("npc:CN-001", [a.action_id for a in legal])

    def test_npc_knowledge_gate(self):
        state = self.engine.initial_state()
        state.npc_dynamic["NPC-B"]["information_known"] = []
        legal = self.engine.legal_actions(state)
        state, _ = self._step(state, "npc:CN-001")
        self.assertNotIn("KNOW-003", state.player_knowledge)

    def test_relationship_reaction_on_accusation(self):
        state = self.engine.initial_state()
        state.player_knowledge.update({"KNOW-001", "KNOW-002", "KNOW-003"})
        before = state.npc_dynamic["NPC-A"]["trust"]
        state, _ = self.engine.step(state, "acc:Q-CULPRIT", DeterministicRNG(1), accusation_answer="NPC-B")
        after = state.npc_dynamic["NPC-A"]["trust"]
        self.assertGreater(after, before)

    def test_multi_fact_inference(self):
        state = self.engine.initial_state()
        state.player_knowledge.update({"KNOW-001", "KNOW-002"})
        legal = self.engine.legal_actions(state)
        self.assertIn("hyp:HYP-001", [a.action_id for a in legal])
        state, _ = self._step(state, "hyp:HYP-001")
        self.assertIn("KNOW-004", state.player_knowledge)

    def test_inference_recovery_via_testimony(self):
        state = self.engine.initial_state()
        state, _ = self._step(state, "npc:CN-001")
        self.assertIn("KNOW-003", state.player_knowledge)

    def test_deadline_ending(self):
        state = self.engine.initial_state()
        for clock in ("T1", "T2", "T_DEADLINE"):
            legal = self.engine.legal_actions(state)
            act = next(a for a in legal if a.action_id == f"time:{clock}")
            state, meta = self.engine.step(state, act.action_id, self.rng)
        self.assertEqual(state.ending_chain_state.get("ending_id"), "END-TIMEOUT")
        self.assertEqual(meta.get("ending_id"), "END-TIMEOUT")

    def test_partial_ending(self):
        state = self.engine.initial_state()
        state.player_knowledge.update({"KNOW-001", "KNOW-003"})
        state, meta = self._step(state, "acc:Q-CULPRIT")
        self.assertEqual(meta.get("ending_id"), "END-PARTIAL")

    def test_perfect_ending(self):
        state = self.engine.initial_state()
        state.player_knowledge.update({"KNOW-001", "KNOW-002", "KNOW-003", "KNOW-004"})
        state.flow_flags["accusation_complete"] = False
        state, meta = self._step(state, "acc:Q-CULPRIT")
        self.assertEqual(meta.get("ending_id"), "END-PERFECT")

    def test_final_accusation(self):
        state = self.engine.initial_state()
        state.player_knowledge.update({"KNOW-001", "KNOW-003"})
        state, meta = self._step(state, "acc:Q-CULPRIT")
        answers = state.ending_chain_state.get("accusation_answers", {})
        self.assertEqual(answers.get("Q-CULPRIT"), "NPC-A")
        self.assertTrue(state.flow_flags.get("accusation_complete"))

    def test_hidden_truth_isolation(self):
        state = self.engine.initial_state()
        legal = self.engine.legal_actions(state)
        view = PlayerView.from_state(state, [a.action_id for a in legal], [a.player_label for a in legal])
        self.assertNotIn("culprit_id", view.flow_flags)
        self.assertNotIn("culprit_id", vars(view))
        strat = create_strategy("random_legal")
        rng = DeterministicRNG(42)
        chosen = strat.choose(view, legal, rng)
        self.assertIsNotNone(chosen)
        self.assertIn(chosen.action_id, [a.action_id for a in legal])

    def test_deterministic_seeds(self):
        r1 = self.engine.run_trace("random_legal", seed=7)
        r2 = self.engine.run_trace("random_legal", seed=7)
        self.assertEqual(r1.path, r2.path)
        self.assertEqual(r1.final_state_key, r2.final_state_key)

    def test_two_player_split_regroup_shared_clock(self):
        engine, _ = _engine(TWO)
        state = engine.initial_state()
        self.assertEqual(state.play_mode, "two_player")
        legal = engine.legal_actions(state)
        self.assertIn("tp:split", [a.action_id for a in legal])
        state, _ = engine.step(state, "tp:split", DeterministicRNG(1))
        self.assertTrue(state.two_player.split_active)
        clock_before = state.in_world_clock
        state, _ = engine.step(state, "tp:regroup", DeterministicRNG(1))
        self.assertFalse(state.two_player.split_active)
        self.assertEqual(state.in_world_clock, clock_before)

    def test_exhaustive_blocked_on_state_explosion(self):
        modes = SimulationModes(str(SOLO))
        result = modes.exhaustive(ExhaustiveConfig(max_states=20, timeout_seconds=5.0))
        self.assertEqual(result["status"], "BLOCKED")
        self.assertEqual(result["blocked_reason"], "state_explosion")
        self.assertTrue(result["partial"])

    def test_exhaustive_cancellation_partial_safe(self):
        modes = SimulationModes(str(SOLO))
        cancel = [False]
        cancel[0] = True
        result = modes.exhaustive(ExhaustiveConfig(max_states=5000), cancel_flag=cancel)
        self.assertEqual(result["status"], "CANCELLED")
        self.assertTrue(result["partial"])

    def test_validate_mode_and_trust_gate(self):
        modes = SimulationModes(str(SOLO))
        report = modes.validate()
        self.assertEqual(report["status"], "PASS")
        self.assertTrue(report["trust"]["trusted"])
        self.assertEqual(report["trust"]["ownership"], "ADVENTURE")

    def test_untrusted_ownership_not_adventure(self):
        load = load_simulator_package(FIXTURES / "sim_v2_missing_layer")
        trust = evaluate_trust(load, None, coverage="validate")
        self.assertFalse(trust.trusted)
        self.assertIn(trust.ownership, ("SIMULATOR", "PACKAGE", "GENERATOR", "UNDETERMINED"))

    def test_all_strategies_registered(self):
        expected = {
            "random_legal",
            "broad_explorer",
            "time_conserving",
            "object_focused",
            "npc_focused",
            "information_seeking",
            "proof_seeking",
            "cautious",
            "risk_taking",
            "poor_baseline",
            "cooperative_two_player",
        }
        self.assertEqual(set(STRATEGIES.keys()), expected)

    def test_monte_carlo_and_compare_modes(self):
        modes = SimulationModes(str(SOLO))
        mc = modes.monte_carlo()
        self.assertEqual(mc["status"], "COMPLETED")
        self.assertIn("ending_frequencies", mc)
        cmp = modes.compare_strategies(runs_per_strategy=2, seed=10)
        self.assertEqual(cmp["status"], "COMPLETED")
        self.assertEqual(len(cmp["strategies"]), len(STRATEGIES))

    def test_location_revisit_rule(self):
        state = self.engine.initial_state()
        state.player_knowledge.add("KNOW-002")
        state, _ = self._step(state, "nav:NAV-LOBBY-OFFICE")
        state, _ = self._step(state, "nav:NAV-OFFICE-LOBBY")
        state, _ = self._step(state, "nav:NAV-LOBBY-OFFICE")
        legal = self.engine.legal_actions(state)
        self.assertIn("rev:REV-001", [a.action_id for a in legal])
        state, _ = self._step(state, "rev:REV-001")
        self.assertTrue(state.flow_flags.get("office_searched"))

    def test_basement_access_with_key(self):
        state = self.engine.initial_state()
        state.items.add("ITEM-KEY")
        legal = self.engine.legal_actions(state)
        self.assertIn("nav:NAV-LOBBY-BASEMENT", [a.action_id for a in legal])


if __name__ == "__main__":
    unittest.main()
