"""Simulation engine for Simulator v2."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from simulator_v2.action_enumerator import enumerate_legal_actions
from simulator_v2.actions import ActionKind
from simulator_v2.derivation import CanonicalSimulationModel
from simulator_v2.executor import apply_action
from simulator_v2.metrics import RunMetrics, SimulationRunResult
from simulator_v2.player_view import PlayerView
from simulator_v2.rng import DeterministicRNG
from simulator_v2.state import SimulationState, initial_state_from_model
from simulator_v2.strategies import Strategy, create_strategy, terminal_fallback


@dataclass
class EngineConfig:
    max_steps: int = 500
    check_modifier: int = 5
    accusation_answer: str = "NPC-A"
    stagnation_repeat_limit: int = 3


class SimulationEngine:
    def __init__(self, model: CanonicalSimulationModel, config: EngineConfig | None = None) -> None:
        self.model = model
        self.config = config or EngineConfig()

    def initial_state(self) -> SimulationState:
        return initial_state_from_model(self.model)

    def legal_actions(self, state: SimulationState):
        return enumerate_legal_actions(state, self.model)

    def step(
        self,
        state: SimulationState,
        action_id: str,
        rng: DeterministicRNG,
        *,
        accusation_answer: str | None = None,
    ) -> tuple[SimulationState, dict[str, Any]]:
        legal = self.legal_actions(state)
        chosen = next((a for a in legal if a.action_id == action_id), None)
        if chosen is None:
            raise ValueError(f"illegal action: {action_id}")
        new_state = state.copy()
        meta = apply_action(
            new_state,
            self.model,
            chosen,
            rng,
            check_modifier=self.config.check_modifier,
            accusation_answer=accusation_answer or self.config.accusation_answer,
        )
        self._update_proof(new_state)
        return new_state, meta

    def run_trace(
        self,
        strategy: Strategy | str,
        seed: int = 42,
        max_steps: int | None = None,
        *,
        cancel_flag: list[bool] | None = None,
    ) -> SimulationRunResult:
        rng = DeterministicRNG(seed)
        strat_name = strategy if isinstance(strategy, str) else strategy.name
        strat = create_strategy(strategy) if isinstance(strategy, str) else strategy
        state = self.initial_state()
        metrics = RunMetrics()
        path: list[str] = []
        limit = max_steps or self.config.max_steps
        prev_knowledge = set(state.player_knowledge)
        seen_state_keys: list[str] = []
        last_action_id = ""
        repeat_action_count = 0
        incomplete_reason: str | None = None
        errors: list[str] = []

        for step_idx in range(limit):
            if cancel_flag and cancel_flag[0]:
                incomplete_reason = "CANCELLED"
                break

            legal = self.legal_actions(state)
            if not legal:
                incomplete_reason = "NO_LEGAL_ACTION"
                break

            state_key = state.identity_key()
            view = PlayerView.from_state(state, [a.action_id for a in legal], [a.player_label for a in legal])

            try:
                chosen = strat.choose(view, legal, rng)
            except Exception as exc:
                incomplete_reason = "ERROR"
                errors.append(str(exc))
                break

            if chosen is None:
                chosen = terminal_fallback(legal)
                if chosen is None:
                    incomplete_reason = "NO_LEGAL_ACTION"
                    break

            if state_key in seen_state_keys:
                fallback = terminal_fallback(legal)
                if fallback is not None:
                    chosen = fallback
                elif seen_state_keys.count(state_key) >= 2:
                    incomplete_reason = "CYCLE"
                    break

            if chosen.action_id == last_action_id:
                repeat_action_count += 1
            else:
                repeat_action_count = 1
            if repeat_action_count >= self.config.stagnation_repeat_limit:
                fallback = terminal_fallback(legal)
                if fallback is not None and fallback.action_id != chosen.action_id:
                    chosen = fallback
                    repeat_action_count = 1
                else:
                    incomplete_reason = "CYCLE"
                    break

            try:
                state, _meta = self.step(state, chosen.action_id, rng)
            except ValueError as exc:
                incomplete_reason = "ERROR"
                errors.append(str(exc))
                break

            path.append(chosen.action_id)
            last_action_id = chosen.action_id
            seen_state_keys.append(state_key)

            metrics.record_step(chosen.kind.value, chosen.time_cost_minutes, chosen.action_id)
            gained = set(state.player_knowledge) - prev_knowledge
            metrics.knowledge_gained.extend(sorted(gained))
            prev_knowledge = set(state.player_knowledge)
            metrics.failed_checks = state.ending_chain_state.get("failed_checks", 0)

            if state.ending_chain_state.get("ending_id"):
                metrics.ending_id = state.ending_chain_state["ending_id"]
                break
        else:
            if incomplete_reason is None:
                incomplete_reason = "MAX_STEPS"

        ending = state.ending_chain_state.get("ending_id")
        metrics.ending_id = ending
        if ending == "END-TIMEOUT":
            metrics.deadline_used = True
        if ending == "END-PERFECT":
            metrics.perfect_ending_reachable = True

        status = "COMPLETED" if ending else ("CANCELLED" if incomplete_reason == "CANCELLED" else "INCOMPLETE")
        if incomplete_reason == "ERROR":
            status = "ERROR"

        return SimulationRunResult(
            status=status,
            metrics=metrics,
            final_state_key=state.identity_key(),
            last_state_key=state.identity_key(),
            ending_id=ending,
            path=path,
            errors=errors,
            coverage="single_trace",
            incomplete_reason=None if ending else incomplete_reason,
            strategy=strat_name,
            seed=seed,
        )

    def _update_proof(self, state: SimulationState) -> None:
        for proof in self.model.raw_packages.get("investigation_core", {}).get("proofs", []) or []:
            req = set(proof.get("required_knowledge_ids", []) or [])
            cid = proof.get("conclusion_id", "")
            if req.issubset(state.player_knowledge):
                state.proof_status[cid] = True
