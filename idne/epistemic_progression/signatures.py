"""Relevant-state signatures for event reuse rules."""

from __future__ import annotations

from typing import Any

from idne.epistemic_progression.model import EpistemicState, PlayableEvent


def knowledge_signature(event: PlayableEvent, state: EpistemicState) -> frozenset[str]:
    deps = event.relevant_knowledge_dependencies
    if not deps:
        return frozenset()
    return frozenset(k for k in state.player_knowledge if k in deps)


def world_state_signature(event: PlayableEvent, state: EpistemicState) -> dict[str, Any]:
    deps = event.relevant_world_state_dependencies
    if not deps:
        return {}
    return {k: state.world_state.get(k) for k in deps if k in state.world_state}


def interaction_signature(event: PlayableEvent, state: EpistemicState) -> dict[str, Any]:
    deps = event.relevant_interaction_dependencies
    if not deps:
        return {}
    out: dict[str, Any] = {}
    for dep in deps:
        if dep in state.interaction_state:
            out[dep] = state.interaction_state[dep]
        elif dep.startswith("exhausted:"):
            action_id = dep.split(":", 1)[1]
            exhausted = set(state.interaction_state.get("exhausted_actions") or [])
            out[dep] = action_id in exhausted
    return out


def reuse_signature(event: PlayableEvent, state: EpistemicState) -> tuple[Any, ...]:
    ws = world_state_signature(event, state)
    return (
        knowledge_signature(event, state),
        tuple(sorted(ws.items())),
        tuple(sorted(interaction_signature(event, state).items())),
    )
