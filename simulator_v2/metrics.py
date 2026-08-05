"""Run metrics for Simulator v2."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class RunMetrics:
    in_world_minutes: int = 0
    wall_clock_minutes: float = 0.0
    player_active_minutes: float = 0.0
    session_minutes: float = 0.0
    waiting_minutes: float = 0.0
    steps: int = 0
    revisits: int = 0
    failed_checks: int = 0
    object_interactions: int = 0
    npc_interactions: int = 0
    knowledge_gained: list[str] = field(default_factory=list)
    ending_id: str | None = None
    path_action_ids: list[str] = field(default_factory=list)
    ending_frequencies: dict[str, int] = field(default_factory=dict)
    shortest_path_steps: int | None = None
    longest_path_steps: int | None = None
    perfect_ending_reachable: bool = False
    deadline_used: bool = False

    def record_step(self, action_kind: str, time_cost: int, action_id: str) -> None:
        self.steps += 1
        self.in_world_minutes += time_cost
        self.player_active_minutes += time_cost
        self.wall_clock_minutes += time_cost * 1.0
        self.session_minutes += time_cost * 1.0
        self.path_action_ids.append(action_id)
        if action_kind == "object":
            self.object_interactions += 1
        if action_kind == "npc":
            self.npc_interactions += 1
        if action_kind == "revisit":
            self.revisits += 1

    def to_dict(self) -> dict[str, Any]:
        return {
            "in_world_minutes": self.in_world_minutes,
            "wall_clock_minutes": self.wall_clock_minutes,
            "player_active_minutes": self.player_active_minutes,
            "session_minutes": self.session_minutes,
            "waiting_minutes": self.waiting_minutes,
            "steps": self.steps,
            "revisits": self.revisits,
            "failed_checks": self.failed_checks,
            "object_interactions": self.object_interactions,
            "npc_interactions": self.npc_interactions,
            "knowledge_gained": self.knowledge_gained,
            "ending_id": self.ending_id,
            "path_action_ids": self.path_action_ids,
            "ending_frequencies": self.ending_frequencies,
            "shortest_path_steps": self.shortest_path_steps,
            "longest_path_steps": self.longest_path_steps,
            "perfect_ending_reachable": self.perfect_ending_reachable,
            "deadline_used": self.deadline_used,
        }


@dataclass
class SimulationRunResult:
    status: str
    metrics: RunMetrics
    final_state_key: str = ""
    ending_id: str | None = None
    path: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    partial: bool = False
    coverage: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "metrics": self.metrics.to_dict(),
            "ending_id": self.ending_id,
            "path": self.path,
            "errors": self.errors,
            "partial": self.partial,
            "coverage": self.coverage,
        }
