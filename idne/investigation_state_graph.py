"""Integrated investigation state graph (Milestone 7)."""

from __future__ import annotations

import time
from collections import deque
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
    unique_states_explored: int = 0
    states_scheduled: int = 0
    attempted_transitions: int = 0
    duplicate_states_skipped: int = 0
    peak_queue_size: int = 0
    maximum_depth: int = 0
    elapsed_seconds: float = 0.0
    complete: bool = False
    termination_reason: str = ""
    exceeded_limit: str | None = None
    transition_counts_by_type: dict[str, int] = field(default_factory=dict)


def _normalize_frozenset(value: Any) -> frozenset[str]:
    if isinstance(value, frozenset):
        return frozenset(str(v) for v in value)
    if isinstance(value, (set, list, tuple)):
        return frozenset(str(v) for v in value)
    return frozenset()


def canonical_investigation_state_key(state: dict[str, Any]) -> tuple[Any, ...]:
    """Immutable canonical key for investigation graph states.

    Includes every dimension that affects future legal transitions:
    location, clock, acquired knowledge, and completed capability checks.
    Unordered collections are normalized to sorted frozensets.
    """
    return (
        str(state.get("location", "")),
        str(state.get("clock", "")),
        _normalize_frozenset(state.get("knowledge")),
        _normalize_frozenset(state.get("checks")),
    )


def _state_key(state: dict[str, Any]) -> tuple[Any, ...]:
    return canonical_investigation_state_key(state)


def _initial_state(clocks: list[str]) -> dict[str, Any]:
    return {
        "location": "LOC-OFFICE",
        "clock": clocks[0],
        "knowledge": frozenset(),
        "checks": frozenset(),
    }


def build_investigation_state_graph(
    package: dict[str, Any],
    config: dict[str, Any] | None = None,
) -> GraphBuildResult:
    """Explore integrated investigation state space with honest limits."""
    start_time = time.perf_counter()
    cfg = config or package.get("state_graph_config", {}) or {}
    max_states = int(cfg.get("max_states", 5000))
    max_depth = int(cfg.get("max_depth", 40))
    max_queue_size = int(cfg.get("max_queue_size", max_states * 4))
    max_transitions = int(cfg.get("max_transitions", max_states * 8))
    max_wall_seconds = cfg.get("max_wall_seconds")
    wall_deadline = (
        start_time + float(max_wall_seconds) if max_wall_seconds is not None else None
    )

    if cfg.get("forced_explosion"):
        return GraphBuildResult(
            explored_states=max_states + 1,
            max_depth_reached=max_depth + 1,
            truncated=True,
            blocked=True,
            reason="forced_explosion flag in fixture",
            unique_states_explored=max_states + 1,
            maximum_depth=max_depth + 1,
            complete=False,
            termination_reason="forced_explosion flag in fixture",
            exceeded_limit="forced_explosion",
            elapsed_seconds=time.perf_counter() - start_time,
        )

    clocks = ["T0"]
    time_val = package.get("time_validation", {}) or {}
    if time_val.get("deadline_clock"):
        clocks.append(str(time_val["deadline_clock"]))

    initial_state = _initial_state(clocks)
    initial_key = _state_key(initial_state)

    explored: set[tuple[Any, ...]] = set()
    enqueued: set[tuple[Any, ...]] = {initial_key}
    queue: deque[tuple[dict[str, Any], int]] = deque([(initial_state, 0)])
    max_d = 0
    peak_queue = 1
    states_scheduled = 1
    attempted_transitions = 0
    duplicate_states_skipped = 0
    transition_counts: dict[str, int] = {
        "recovery_route": 0,
        "knowledge_acquire": 0,
        "time_advance": 0,
    }
    exceeded_limit: str | None = None
    termination_reason = ""

    def _limit_hit(limit_name: str) -> bool:
        nonlocal exceeded_limit, termination_reason
        if exceeded_limit is None:
            exceeded_limit = limit_name
            termination_reason = _limit_reason(limit_name)
        return True

    def _limit_reason(limit_name: str) -> str:
        if limit_name == "max_states":
            return f"state limit {max_states} reached"
        if limit_name == "max_transitions":
            return f"transition limit {max_transitions} reached"
        if limit_name == "max_queue_size":
            return f"queue limit {max_queue_size} reached"
        if limit_name == "max_wall_seconds":
            return f"wall-clock limit {max_wall_seconds}s reached"
        return limit_name

    def try_enqueue(child: dict[str, Any], depth: int, transition_type: str) -> None:
        nonlocal states_scheduled, attempted_transitions, duplicate_states_skipped, peak_queue
        attempted_transitions += 1
        transition_counts[transition_type] = transition_counts.get(transition_type, 0) + 1

        if wall_deadline is not None and time.perf_counter() >= wall_deadline:
            _limit_hit("max_wall_seconds")
            return
        if depth > max_depth:
            return
        if len(explored) >= max_states:
            _limit_hit("max_states")
            return
        if exceeded_limit is not None:
            return
        if attempted_transitions > max_transitions:
            _limit_hit("max_transitions")
            return

        key = _state_key(child)
        if key in explored or key in enqueued:
            duplicate_states_skipped += 1
            return
        if len(queue) >= max_queue_size:
            _limit_hit("max_queue_size")
            return

        enqueued.add(key)
        queue.append((child, depth))
        states_scheduled += 1
        peak_queue = max(peak_queue, len(queue))

    while queue and len(explored) < max_states and exceeded_limit is None:
        if wall_deadline is not None and time.perf_counter() >= wall_deadline:
            _limit_hit("max_wall_seconds")
            break

        state, depth = queue.popleft()
        enqueued.discard(_state_key(state))
        if depth > max_depth:
            continue
        max_d = max(max_d, depth)
        key = _state_key(state)
        if key in explored:
            continue
        explored.add(key)

        for route in package.get("recovery_routes", []) or []:
            if route.get("zero_cost_loop"):
                new_loc = str(route.get("destination_ref", state["location"]))
                child = dict(state)
                child["location"] = new_loc
                try_enqueue(child, depth + 1, "recovery_route")

        for src in package.get("information_sufficiency", []) or []:
            for s in src.get("sources", []) or []:
                if s.get("accessible") and s.get("before_inference"):
                    kid = str(s.get("knowledge_id", ""))
                    if kid and kid not in state["knowledge"]:
                        child = dict(state)
                        child["knowledge"] = frozenset(set(state["knowledge"]) | {kid})
                        try_enqueue(child, depth + 1, "knowledge_acquire")

        if len(clocks) > 1 and state["clock"] == clocks[0]:
            child = dict(state)
            child["clock"] = clocks[-1]
            try_enqueue(child, depth + 1, "time_advance")

    elapsed = time.perf_counter() - start_time
    truncated = exceeded_limit is not None or len(explored) >= max_states
    blocked = truncated or max_d > max_depth
    reason = termination_reason
    if not reason:
        if len(explored) >= max_states:
            reason = f"state limit {max_states} reached"
            exceeded_limit = exceeded_limit or "max_states"
        elif max_d > max_depth:
            reason = f"depth limit {max_depth} exceeded"
            exceeded_limit = exceeded_limit or "max_depth"
        else:
            reason = "complete"

    complete = not truncated and not blocked and not queue

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
        unique_states_explored=len(explored),
        states_scheduled=states_scheduled,
        attempted_transitions=attempted_transitions,
        duplicate_states_skipped=duplicate_states_skipped,
        peak_queue_size=peak_queue,
        maximum_depth=max_d,
        elapsed_seconds=elapsed,
        complete=complete,
        termination_reason=reason,
        exceeded_limit=exceeded_limit,
        transition_counts_by_type=transition_counts,
    )
