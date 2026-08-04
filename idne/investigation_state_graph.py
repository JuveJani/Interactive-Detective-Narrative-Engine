"""Integrated investigation state graph (Milestone 7)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class GraphBuildResult:
    explored_states: int
    max_depth_reached: int
    truncated: bool
    blocked: bool
    reason: str = ""
    sample_states: list[dict[str, Any]] = field(default_factory=list)


def build_investigation_state_graph(
    package: dict[str, Any],
    config: dict[str, Any] | None = None,
) -> GraphBuildResult:
    """Explore integrated investigation state space with honest limits."""
    cfg = config or package.get("state_graph_config", {}) or {}
    max_states = int(cfg.get("max_states", 5000))
    max_depth = int(cfg.get("max_depth", 40))
    if cfg.get("forced_explosion"):
        return GraphBuildResult(
            explored_states=max_states + 1,
            max_depth_reached=max_depth + 1,
            truncated=True,
            blocked=True,
            reason="forced_explosion flag in fixture",
        )

    # Seed dimensions from package model
    locations = {str(r.get("location_id", "LOC-START")) for r in package.get("access_requirements", []) or []}
    locations.add("LOC-OFFICE")
    knowledge = set()
    for inf in package.get("inference_questions", []) or []:
        for kid in inf.get("required_knowledge_ids", []) or []:
            knowledge.add(str(kid))
    for trace in package.get("conclusion_traces", []) or []:
        for step in trace.get("chain", []) or []:
            if step.get("layer") == "knowledge":
                knowledge.add(str(step.get("ref")))

    clocks = ["T0"]
    time_val = package.get("time_validation", {}) or {}
    if time_val.get("deadline_clock"):
        clocks.append(str(time_val["deadline_clock"]))

    explored: set[str] = set()
    queue: list[tuple[dict[str, Any], int]] = [
        (
            {
                "location": "LOC-OFFICE",
                "clock": clocks[0],
                "knowledge": frozenset(),
                "checks": frozenset(),
            },
            0,
        )
    ]
    max_d = 0

    while queue and len(explored) < max_states:
        state, depth = queue.pop(0)
        if depth > max_depth:
            continue
        max_d = max(max_d, depth)
        key = (
            state["location"],
            state["clock"],
            state["knowledge"],
            state["checks"],
        )
        if key in explored:
            continue
        explored.add(key)

        # Expand via recovery routes and knowledge acquisition (simplified)
        for route in package.get("recovery_routes", []) or []:
            if route.get("zero_cost_loop"):
                new_loc = str(route.get("destination_ref", state["location"]))
                child = dict(state)
                child["location"] = new_loc
                queue.append((child, depth + 1))

        for src in package.get("information_sufficiency", []) or []:
            for s in src.get("sources", []) or []:
                if s.get("accessible") and s.get("before_inference"):
                    kid = str(s.get("knowledge_id", ""))
                    if kid and kid not in state["knowledge"]:
                        child = dict(state)
                        child["knowledge"] = frozenset(set(state["knowledge"]) | {kid})
                        queue.append((child, depth + 1))

        # Time advance
        if len(clocks) > 1 and state["clock"] == clocks[0]:
            child = dict(state)
            child["clock"] = clocks[-1]
            queue.append((child, depth + 1))

    truncated = len(explored) >= max_states
    blocked = truncated or max_d > max_depth
    reason = ""
    if truncated:
        reason = f"state limit {max_states} reached"
    elif max_d > max_depth:
        reason = f"depth limit {max_depth} exceeded"

    samples = []
    for i, k in enumerate(list(explored)[:5]):
        samples.append({"state_key": str(k), "index": i})

    return GraphBuildResult(
        explored_states=len(explored),
        max_depth_reached=max_d,
        truncated=truncated,
        blocked=blocked,
        reason=reason,
        sample_states=samples,
    )
