"""Materialize template playable events into exact state snapshots."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from typing import Any

from idne.epistemic_progression.eligibility import action_eligible, event_enterable
from idne.epistemic_progression.fingerprint import (
    StateFingerprint,
    materialized_unit_id,
    template_unit_id,
)
from idne.epistemic_progression.model import (
    DIALOGUE_TOPIC_KINDS,
    EpistemicPackage,
    EpistemicState,
    PlayableEvent,
    StructuredAction,
)


@dataclass
class MaterializeStats:
    template_count: int = 0
    materialized_count: int = 0
    reachable_states: int = 0
    attempted_transitions: int = 0
    duplicate_states_skipped: int = 0
    peak_queue_size: int = 0
    truncated: bool = False
    max_states: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "template_count": self.template_count,
            "materialized_count": self.materialized_count,
            "reachable_states": self.reachable_states,
            "attempted_transitions": self.attempted_transitions,
            "duplicate_states_skipped": self.duplicate_states_skipped,
            "peak_queue_size": self.peak_queue_size,
            "truncated": self.truncated,
            "max_states": self.max_states,
        }


def _snapshot_dict(state: EpistemicState) -> dict[str, Any]:
    return {
        "player_knowledge": sorted(state.player_knowledge),
        "completed_topics": sorted(state.interaction_state.get("completed_topics") or []),
        "world_state": dict(sorted(state.world_state.items())),
    }


def _clone_action(action: StructuredAction, destination_unit_id: str) -> StructuredAction:
    return StructuredAction(
        action_id=action.action_id,
        action_type=action.action_type,
        label=action.label,
        destination_unit_id=destination_unit_id,
        requires_knowledge_ids=action.requires_knowledge_ids,
        forbidden_knowledge_ids=action.forbidden_knowledge_ids,
        requires_world_state=dict(action.requires_world_state),
        forbidden_world_state=dict(action.forbidden_world_state),
        requires_observable=action.requires_observable,
        referenced_fact_ids=action.referenced_fact_ids,
        referenced_entity_ids=action.referenced_entity_ids,
        exhaustion=action.exhaustion,
        knowledge_delta=action.knowledge_delta,
        world_state_delta=dict(action.world_state_delta),
        interaction_delta=dict(action.interaction_delta),
        investigative=action.investigative,
        purpose=action.purpose,
    )


def _clone_event(template: PlayableEvent, unit_id: str, state: EpistemicState, actions: list[StructuredAction]) -> PlayableEvent:
    return PlayableEvent(
        event_id=f"EVT-{unit_id}",
        unit_id=unit_id,
        location_id=template.location_id,
        event_kind=template.event_kind,
        physical_location_id=template.physical_location_id,
        variant_of=template.variant_of,
        required_knowledge_ids=frozenset(state.player_knowledge),
        forbidden_knowledge_ids=template.forbidden_knowledge_ids,
        required_world_state=dict(state.world_state),
        forbidden_world_state=template.forbidden_world_state,
        relevant_knowledge_dependencies=template.relevant_knowledge_dependencies,
        relevant_world_state_dependencies=template.relevant_world_state_dependencies,
        relevant_interaction_dependencies=template.relevant_interaction_dependencies,
        observable_entities=template.observable_entities,
        observable_objects=template.observable_objects,
        structured_actions=actions,
        content_blocks=list(template.content_blocks),
        supersedes_unit_id=template.supersedes_unit_id,
        time_layer=template.time_layer,
        template_unit_id=template.template_unit_id or template.unit_id,
        state_snapshot=_snapshot_dict(state),
    )


def _eligible_template_actions(template: PlayableEvent, state: EpistemicState) -> list[StructuredAction]:
    actions: list[StructuredAction] = []
    completed = set(state.interaction_state.get("completed_topics") or [])
    for action in template.structured_actions:
        eligible, _ = action_eligible(action, state)
        if not eligible:
            continue
        if action.action_type in {"dialogue_topic", "npc_topic", "topic"}:
            topic = template_unit_id(action.destination_unit_id)
            if topic in completed:
                continue
        actions.append(action)
    return actions


def materialize_package(
    templates: dict[str, PlayableEvent],
    *,
    start_template_unit: str,
    initial_state: EpistemicState,
    max_states: int = 500_000,
) -> tuple[EpistemicPackage, MaterializeStats]:
    stats = MaterializeStats(template_count=len(templates), max_states=max_states)
    initial_fp = StateFingerprint.from_state(initial_state)
    materialized: dict[str, PlayableEvent] = {}
    visited: set[tuple[str, StateFingerprint]] = set()
    queue: deque[tuple[str, EpistemicState]] = deque([(start_template_unit, initial_state.copy())])

    while queue:
        stats.peak_queue_size = max(stats.peak_queue_size, len(queue))
        if stats.materialized_count >= max_states:
            stats.truncated = True
            break

        tpl_id, state = queue.popleft()
        fp = StateFingerprint.from_state(state)
        visit_key = (tpl_id, fp)
        if visit_key in visited:
            stats.duplicate_states_skipped += 1
            continue
        visited.add(visit_key)
        stats.reachable_states += 1

        template = templates.get(tpl_id)
        if not template:
            continue

        unit_id = materialized_unit_id(tpl_id, fp, initial=initial_fp)
        eligible = _eligible_template_actions(template, state)
        actions_out: list[StructuredAction] = []
        for action in eligible:
            stats.attempted_transitions += 1
            next_state = state.apply_action_deltas(action)
            dest_tpl = template_unit_id(action.destination_unit_id)
            dest_id = materialized_unit_id(
                dest_tpl,
                StateFingerprint.from_state(next_state),
                initial=initial_fp,
            )
            actions_out.append(_clone_action(action, dest_id))
            queue.append((dest_tpl, next_state))

        materialized[unit_id] = _clone_event(template, unit_id, state, actions_out)
        stats.materialized_count = len(materialized)

    package = EpistemicPackage(
        schema_version="1.0",
        adventure_id="",
        initial_player_knowledge=initial_state.player_knowledge,
        initial_world_state=dict(initial_state.world_state),
        initial_observable_entities=initial_state.observable_entities,
        initial_observable_objects=initial_state.observable_objects,
        events={e.event_id: e for e in materialized.values() if e.event_id},
        events_by_unit=materialized,
        events_by_location={},
    )
    for event in materialized.values():
        loc = event.physical_location_id or event.location_id
        if loc:
            package.events_by_location.setdefault(loc, []).append(event)

    return package, stats


def lookup_materialized_unit(
    package: EpistemicPackage,
    template_id: str,
    state: EpistemicState,
    *,
    initial_state: EpistemicState,
) -> str | None:
    fp = StateFingerprint.from_state(state)
    initial_fp = StateFingerprint.from_state(initial_state)
    unit_id = materialized_unit_id(template_id, fp, initial=initial_fp)
    if unit_id in package.events_by_unit:
        return unit_id
    return None
