"""Simulation modes: validate, trace, Monte Carlo, compare, exhaustive, path analysis."""

from __future__ import annotations

import time
from collections import deque
from dataclasses import dataclass
from typing import Any

from simulator_v2.action_enumerator import enumerate_legal_actions
from simulator_v2.engine import SimulationEngine
from simulator_v2.metrics import RunMetrics, SimulationRunResult
from simulator_v2.package_loader import load_simulator_package
from simulator_v2.derivation import derive_simulation_model
from simulator_v2.rng import DeterministicRNG
from simulator_v2.strategies import STRATEGIES, strategy_compatible
from simulator_v2.trust_gate import integrated_validation_status, trust_dict_for_mode


@dataclass
class ExhaustiveConfig:
    max_states: int = 5000
    max_depth: int = 100
    timeout_seconds: float = 30.0


@dataclass
class MonteCarloConfig:
    runs: int = 100
    seed: int = 42


def _integrated_validation_dict(load_result) -> dict[str, Any]:
    return {
        "status": integrated_validation_status(load_result),
        "failures": list(load_result.integrated_validation_failures or []),
    }


def _attach_run_metadata(
    load_result,
    model,
    coverage: str,
    result: SimulationRunResult,
) -> SimulationRunResult:
    result.integrated_validation = _integrated_validation_dict(load_result)
    result.trust = trust_dict_for_mode(load_result, model, coverage)
    return result


class SimulationModes:
    def __init__(self, package_path: str) -> None:
        self.load_result = load_simulator_package(package_path)
        self.model = None
        if self.load_result.adventure_root and self.load_result.status.value == "READY":
            self.model = derive_simulation_model(
                self.load_result.adventure_root,
                self.load_result.play_mode,
            )
        self.engine = SimulationEngine(self.model) if self.model else None

    def _blocked_result(self, errors: list[str]) -> dict[str, Any]:
        trust = trust_dict_for_mode(self.load_result, self.model, "blocked")
        return {
            "status": "BLOCKED",
            "errors": errors,
            "integrated_validation": _integrated_validation_dict(self.load_result),
            "trust": trust,
            "load": self.load_result.to_dict(),
        }

    def validate(self) -> dict[str, Any]:
        if not self.load_result.simulation_ready or not self.engine:
            return self._blocked_result(self.load_result.errors)
        state = self.engine.initial_state()
        legal = self.engine.legal_actions(state)
        trust = trust_dict_for_mode(self.load_result, self.model, "validate")
        return {
            "status": "PASS" if legal and trust.get("trusted") else "BLOCKED",
            "legal_action_count": len(legal),
            "integrated_validation": _integrated_validation_dict(self.load_result),
            "trust": trust,
            "load": self.load_result.to_dict(),
        }

    def trace(self, strategy: str = "random_legal", seed: int = 42) -> SimulationRunResult:
        if not self.engine:
            trust = trust_dict_for_mode(self.load_result, self.model, "trace")
            return SimulationRunResult(
                status="BLOCKED",
                metrics=RunMetrics(),
                errors=["not ready"],
                trust=trust,
                integrated_validation=_integrated_validation_dict(self.load_result),
            )
        result = self.engine.run_trace(strategy, seed=seed)
        return _attach_run_metadata(self.load_result, self.model, "trace", result)

    def monte_carlo(self, config: MonteCarloConfig | None = None, strategy: str = "random_legal") -> dict[str, Any]:
        if not self.engine:
            return self._blocked_result(["not ready"])
        cfg = config or MonteCarloConfig()
        endings: dict[str, int] = {}
        step_counts: list[int] = []
        incomplete_details: list[dict[str, Any]] = []
        for i in range(cfg.runs):
            result = self.engine.run_trace(strategy, seed=cfg.seed + i)
            if result.ending_id:
                eid = result.ending_id
            elif result.incomplete_reason:
                eid = f"INCOMPLETE:{result.incomplete_reason}"
                incomplete_details.append({
                    "reason": result.incomplete_reason,
                    "steps": result.metrics.steps,
                    "last_state_key": result.last_state_key,
                    "seed": cfg.seed + i,
                })
            else:
                eid = "INCOMPLETE:UNKNOWN"
            endings[eid] = endings.get(eid, 0) + 1
            step_counts.append(result.metrics.steps)
        trust = trust_dict_for_mode(self.load_result, self.model, "monte_carlo")
        return {
            "status": "COMPLETED",
            "runs": cfg.runs,
            "strategy": strategy,
            "ending_frequencies": endings,
            "incomplete_details": incomplete_details,
            "shortest_path_steps": min(step_counts) if step_counts else None,
            "longest_path_steps": max(step_counts) if step_counts else None,
            "integrated_validation": _integrated_validation_dict(self.load_result),
            "trust": trust,
        }

    def compare_strategies(self, runs_per_strategy: int = 10, seed: int = 42) -> dict[str, Any]:
        if not self.engine:
            return self._blocked_result(["not ready"])
        play_mode = self.load_result.play_mode
        report: dict[str, Any] = {}

        for name in STRATEGIES:
            if not strategy_compatible(play_mode, name):
                report[name] = {
                    "status": "SKIPPED_INCOMPATIBLE_MODE",
                    "reason": f"strategy requires two_player; package is {play_mode}",
                    "ending_frequencies": {},
                    "incomplete_details": [],
                }
                continue

            endings: dict[str, int] = {}
            incomplete_details: list[dict[str, Any]] = []
            for i in range(runs_per_strategy):
                result = self.engine.run_trace(name, seed=seed + i)
                if result.ending_id:
                    eid = result.ending_id
                elif result.incomplete_reason:
                    eid = f"INCOMPLETE:{result.incomplete_reason}"
                    incomplete_details.append({
                        "reason": result.incomplete_reason,
                        "steps": result.metrics.steps,
                        "last_state_key": result.last_state_key,
                        "seed": seed + i,
                    })
                else:
                    eid = "INCOMPLETE:UNKNOWN"
                    incomplete_details.append({
                        "reason": "UNKNOWN",
                        "steps": result.metrics.steps,
                        "last_state_key": result.last_state_key,
                        "seed": seed + i,
                    })
                endings[eid] = endings.get(eid, 0) + 1

            report[name] = {
                "status": "COMPLETED",
                "ending_frequencies": endings,
                "incomplete_details": incomplete_details,
            }

        trust = trust_dict_for_mode(self.load_result, self.model, "compare")
        return {
            "status": "COMPLETED",
            "play_mode": play_mode,
            "strategies": report,
            "integrated_validation": _integrated_validation_dict(self.load_result),
            "trust": trust,
        }

    def exhaustive(
        self,
        config: ExhaustiveConfig | None = None,
        cancel_flag: list[bool] | None = None,
    ) -> dict[str, Any]:
        if not self.engine:
            return self._blocked_result(["not ready"])
        cfg = config or ExhaustiveConfig()
        start = time.monotonic()
        state = self.engine.initial_state()
        queue: deque[tuple[Any, list[str], int]] = deque([(state, [], 0)])
        visited: set[str] = set()
        endings: dict[str, int] = {}
        states_explored = 0
        blocked_reason = ""

        while queue:
            if cancel_flag and cancel_flag[0]:
                trust = trust_dict_for_mode(self.load_result, self.model, "exhaustive_bounded")
                return {
                    "status": "CANCELLED",
                    "partial": True,
                    "states_explored": states_explored,
                    "ending_frequencies": endings,
                    "blocked_reason": "cancelled",
                    "integrated_validation": _integrated_validation_dict(self.load_result),
                    "trust": trust,
                    "coverage": "exhaustive_bounded",
                }
            if time.monotonic() - start > cfg.timeout_seconds:
                blocked_reason = "timeout"
                break
            if states_explored >= cfg.max_states:
                blocked_reason = "state_explosion"
                break

            cur, path, depth = queue.popleft()
            key = cur.identity_key()
            if key in visited:
                continue
            visited.add(key)
            states_explored += 1

            ending = cur.ending_chain_state.get("ending_id")
            if ending:
                endings[ending] = endings.get(ending, 0) + 1
                continue
            if depth >= cfg.max_depth:
                continue

            legal = enumerate_legal_actions(cur, self.engine.model)
            rng = DeterministicRNG(42 + states_explored)
            for action in legal[:8]:
                try:
                    nxt, _ = self.engine.step(cur, action.action_id, rng)
                except ValueError:
                    continue
                nkey = nxt.identity_key()
                if nkey not in visited:
                    queue.append((nxt, path + [action.action_id], depth + 1))

        status = "COMPLETED" if not blocked_reason else "BLOCKED"
        trust = trust_dict_for_mode(self.load_result, self.model, "exhaustive_bounded")
        return {
            "status": status,
            "blocked_reason": blocked_reason,
            "states_explored": states_explored,
            "unique_states": len(visited),
            "ending_frequencies": endings,
            "partial": bool(blocked_reason),
            "coverage": "exhaustive_bounded",
            "integrated_validation": _integrated_validation_dict(self.load_result),
            "trust": trust,
        }

    def path_analysis(self, strategy: str = "proof_seeking", seed: int = 42) -> dict[str, Any]:
        result = self.trace(strategy, seed)
        return {
            "status": result.status,
            "path": result.path,
            "steps": result.metrics.steps,
            "ending_id": result.ending_id,
            "incomplete_reason": result.incomplete_reason,
            "last_state_key": result.last_state_key,
            "knowledge_gained": result.metrics.knowledge_gained,
            "object_interactions": result.metrics.object_interactions,
            "npc_interactions": result.metrics.npc_interactions,
            "failed_checks": result.metrics.failed_checks,
            "revisits": result.metrics.revisits,
            "integrated_validation": result.integrated_validation,
            "trust": result.trust,
        }
