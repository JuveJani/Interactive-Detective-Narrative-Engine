"""Simulation modes: validate, trace, Monte Carlo, compare, exhaustive, path analysis."""

from __future__ import annotations

import time
from collections import deque
from dataclasses import dataclass, field
from typing import Any

from simulator_v2.action_enumerator import enumerate_legal_actions
from simulator_v2.engine import EngineConfig, SimulationEngine
from simulator_v2.metrics import RunMetrics, SimulationRunResult
from simulator_v2.package_loader import load_simulator_package
from simulator_v2.derivation import derive_simulation_model
from simulator_v2.rng import DeterministicRNG
from simulator_v2.strategies import STRATEGIES, create_strategy
from simulator_v2.trust_gate import evaluate_trust


@dataclass
class ExhaustiveConfig:
    max_states: int = 5000
    max_depth: int = 100
    timeout_seconds: float = 30.0


@dataclass
class MonteCarloConfig:
    runs: int = 100
    seed: int = 42


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

    def validate(self) -> dict[str, Any]:
        if not self.load_result.simulation_ready or not self.engine:
            return {
                "status": "BLOCKED",
                "errors": self.load_result.errors,
                "load": self.load_result.to_dict(),
            }
        state = self.engine.initial_state()
        legal = self.engine.legal_actions(state)
        trust = evaluate_trust(self.load_result, self.model, coverage="validate")
        return {
            "status": "PASS" if legal and trust.trusted else "BLOCKED",
            "legal_action_count": len(legal),
            "trust": trust.to_dict(),
            "load": self.load_result.to_dict(),
        }

    def trace(self, strategy: str = "random_legal", seed: int = 42) -> SimulationRunResult:
        if not self.engine:
            return SimulationRunResult(status="BLOCKED", metrics=RunMetrics(), errors=["not ready"])
        return self.engine.run_trace(strategy, seed=seed)

    def monte_carlo(self, config: MonteCarloConfig | None = None, strategy: str = "random_legal") -> dict[str, Any]:
        if not self.engine:
            return {"status": "BLOCKED", "errors": ["not ready"]}
        cfg = config or MonteCarloConfig()
        endings: dict[str, int] = {}
        step_counts: list[int] = []
        for i in range(cfg.runs):
            result = self.engine.run_trace(strategy, seed=cfg.seed + i)
            eid = result.ending_id or "INCOMPLETE"
            endings[eid] = endings.get(eid, 0) + 1
            step_counts.append(result.metrics.steps)
        trust = evaluate_trust(self.load_result, self.model, coverage="monte_carlo")
        return {
            "status": "COMPLETED",
            "runs": cfg.runs,
            "ending_frequencies": endings,
            "shortest_path_steps": min(step_counts) if step_counts else None,
            "longest_path_steps": max(step_counts) if step_counts else None,
            "trust": trust.to_dict(),
        }

    def compare_strategies(self, runs_per_strategy: int = 10, seed: int = 42) -> dict[str, Any]:
        if not self.engine:
            return {"status": "BLOCKED", "errors": ["not ready"]}
        report: dict[str, Any] = {}
        for name in STRATEGIES:
            endings: dict[str, int] = {}
            for i in range(runs_per_strategy):
                result = self.engine.run_trace(name, seed=seed + i)
                eid = result.ending_id or "INCOMPLETE"
                endings[eid] = endings.get(eid, 0) + 1
            report[name] = endings
        return {"status": "COMPLETED", "strategies": report}

    def exhaustive(
        self,
        config: ExhaustiveConfig | None = None,
        cancel_flag: list[bool] | None = None,
    ) -> dict[str, Any]:
        if not self.engine:
            return {"status": "BLOCKED", "errors": ["not ready"]}
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
                return {
                    "status": "CANCELLED",
                    "partial": True,
                    "states_explored": states_explored,
                    "ending_frequencies": endings,
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
        return {
            "status": status,
            "blocked_reason": blocked_reason,
            "states_explored": states_explored,
            "unique_states": len(visited),
            "ending_frequencies": endings,
            "partial": bool(blocked_reason),
            "coverage": "exhaustive_bounded",
        }

    def path_analysis(self, strategy: str = "proof_seeking", seed: int = 42) -> dict[str, Any]:
        result = self.trace(strategy, seed)
        return {
            "status": result.status,
            "path": result.path,
            "steps": result.metrics.steps,
            "ending_id": result.ending_id,
            "knowledge_gained": result.metrics.knowledge_gained,
            "object_interactions": result.metrics.object_interactions,
            "npc_interactions": result.metrics.npc_interactions,
            "failed_checks": result.metrics.failed_checks,
            "revisits": result.metrics.revisits,
        }
