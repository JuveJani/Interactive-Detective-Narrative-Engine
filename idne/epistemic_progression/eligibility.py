"""Eligibility checks for epistemic events and actions."""

from __future__ import annotations

from typing import Any

from idne.epistemic_progression.model import ContentBlock, EpistemicState, PlayableEvent, StructuredAction


def _world_state_matches(required: dict[str, Any], state: dict[str, Any]) -> bool:
    for key, expected in required.items():
        if state.get(key) != expected:
            return False
    return True


def _forbidden_world_state(forbidden: dict[str, Any], state: dict[str, Any]) -> bool:
    for key, bad in forbidden.items():
        if state.get(key) == bad:
            return True
    return False


def _snapshot_matches(event: PlayableEvent, state: EpistemicState) -> tuple[bool, str]:
    snap = event.state_snapshot
    if not snap:
        return True, "PASS"
    know = frozenset(snap.get("player_knowledge") or [])
    if know != state.player_knowledge:
        return False, f"knowledge snapshot mismatch: event {sorted(know)} vs state {sorted(state.player_knowledge)}"
    topics = frozenset(str(x) for x in (snap.get("completed_topics") or []))
    state_topics = frozenset(str(x) for x in (state.interaction_state.get("completed_topics") or []))
    if topics != state_topics:
        return False, f"completed topic snapshot mismatch: event {sorted(topics)} vs state {sorted(state_topics)}"
    snap_ws = dict(snap.get("world_state") or {})
    for key, expected in snap_ws.items():
        if state.world_state.get(key) != expected:
            return False, f"world state snapshot mismatch at {key}"
    return True, "PASS"


def event_enterable(event: PlayableEvent, state: EpistemicState) -> tuple[bool, str]:
    if event.state_snapshot:
        ok, reason = _snapshot_matches(event, state)
        if not ok:
            return False, reason
        return True, "PASS"
    missing = event.required_knowledge_ids - state.player_knowledge
    if missing:
        return False, f"missing knowledge: {sorted(missing)}"
    if event.forbidden_knowledge_ids & state.player_knowledge:
        return False, "forbidden knowledge held"
    if not _world_state_matches(event.required_world_state, state.world_state):
        return False, "world state prerequisites unmet"
    if _forbidden_world_state(event.forbidden_world_state, state.world_state):
        return False, "forbidden world state active"
    return True, "PASS"


def action_eligible(action: StructuredAction, state: EpistemicState) -> tuple[bool, str]:
    missing = action.requires_knowledge_ids - state.player_knowledge
    if missing:
        return False, f"missing knowledge: {sorted(missing)}"
    if action.forbidden_knowledge_ids & state.player_knowledge:
        return False, "forbidden knowledge held"
    if not _world_state_matches(action.requires_world_state, state.world_state):
        return False, "world state prerequisites unmet"
    if _forbidden_world_state(action.forbidden_world_state, state.world_state):
        return False, "forbidden world state active"
    missing_obs = action.requires_observable - state.observable_entities - state.observable_objects
    if missing_obs:
        return False, f"entity/object not observable: {sorted(missing_obs)}"
    unknown_facts = action.referenced_fact_ids - state.player_knowledge
    if unknown_facts:
        return False, f"references unknown facts: {sorted(unknown_facts)}"
    exhausted = set(state.interaction_state.get("exhausted_actions") or [])
    if action.action_id in exhausted:
        return False, "action exhausted"
    completed = set(state.interaction_state.get("completed_topics") or [])
    if action.action_type in {"dialogue_topic", "npc_topic", "topic"}:
        topic = action.destination_unit_id.split("--S-", 1)[0]
        if topic in completed:
            return False, "conversation topic already completed"
    return True, "PASS"


def block_eligible(block: ContentBlock, state: EpistemicState) -> tuple[bool, str]:
    missing = block.requires_knowledge_ids - state.player_knowledge
    if missing:
        return False, f"missing knowledge: {sorted(missing)}"
    if block.forbidden_knowledge_ids & state.player_knowledge:
        return False, "forbidden knowledge held"
    if not _world_state_matches(block.requires_world_state, state.world_state):
        return False, "world state prerequisites unmet"
    if _forbidden_world_state(block.forbidden_world_state, state.world_state):
        return False, "forbidden world state active"
    unknown_facts = block.fact_ids - state.player_knowledge
    if unknown_facts and block.provenance not in ("observation", "atmosphere"):
        return False, f"references unknown facts: {sorted(unknown_facts)}"
    return True, "PASS"


def filter_eligible_actions(
    event: PlayableEvent, state: EpistemicState
) -> list[tuple[StructuredAction, bool, str]]:
    ok, reason = event_enterable(event, state)
    if not ok:
        return []
    out: list[tuple[StructuredAction, bool, str]] = []
    for action in event.structured_actions:
        eligible, detail = action_eligible(action, state)
        out.append((action, eligible, detail))
    return out
