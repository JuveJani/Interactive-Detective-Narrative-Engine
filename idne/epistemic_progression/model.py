"""Core types for epistemic scene progression."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


LOCATION_HUB_KINDS = frozenset({"location_hub", "location"})
NPC_INTERACTION_KINDS = frozenset({"npc_interaction", "npc_hub"})
DIALOGUE_TOPIC_KINDS = frozenset({"dialogue_topic", "npc_topic"})
TRAVEL_KINDS = frozenset({"travel", "approach", "nav"})
OBSERVATION_KINDS = frozenset({"observation_result", "object_interaction"})
INFERENCE_KINDS = frozenset({"inference", "inference_entry"})
RECOVERY_KINDS = frozenset({"recovery", "waiting"})
ENDING_KINDS = frozenset({"ending"})

HUB_KINDS = LOCATION_HUB_KINDS


@dataclass
class StructuredAction:
    action_id: str
    action_type: str
    label: str
    destination_unit_id: str
    requires_knowledge_ids: frozenset[str] = frozenset()
    forbidden_knowledge_ids: frozenset[str] = frozenset()
    requires_world_state: dict[str, Any] = field(default_factory=dict)
    forbidden_world_state: dict[str, Any] = field(default_factory=dict)
    requires_observable: frozenset[str] = frozenset()
    referenced_fact_ids: frozenset[str] = frozenset()
    referenced_entity_ids: frozenset[str] = frozenset()
    exhaustion: str = "repeatable"  # one_time | exhaustible | repeatable | ambient | recovery
    knowledge_delta: frozenset[str] = frozenset()
    world_state_delta: dict[str, Any] = field(default_factory=dict)
    interaction_delta: dict[str, Any] = field(default_factory=dict)
    investigative: bool = False
    purpose: str = ""

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> StructuredAction:
        return cls(
            action_id=str(raw.get("action_id", "")),
            action_type=str(raw.get("action_type", "action")),
            label=str(raw.get("label", "")),
            destination_unit_id=str(raw.get("destination_unit_id", "")),
            requires_knowledge_ids=frozenset(raw.get("requires_knowledge_ids") or []),
            forbidden_knowledge_ids=frozenset(raw.get("forbidden_knowledge_ids") or []),
            requires_world_state=dict(raw.get("requires_world_state") or {}),
            forbidden_world_state=dict(raw.get("forbidden_world_state") or {}),
            requires_observable=frozenset(raw.get("requires_observable") or []),
            referenced_fact_ids=frozenset(raw.get("referenced_fact_ids") or []),
            referenced_entity_ids=frozenset(raw.get("referenced_entity_ids") or []),
            exhaustion=str(raw.get("exhaustion", "repeatable")),
            knowledge_delta=frozenset(raw.get("knowledge_delta") or []),
            world_state_delta=dict(raw.get("world_state_delta") or {}),
            interaction_delta=dict(raw.get("interaction_delta") or {}),
            investigative=bool(raw.get("investigative", False)),
            purpose=str(raw.get("purpose", "")),
        )


@dataclass
class ContentBlock:
    block_id: str
    text: str
    provenance: str  # observation | prior_knowledge | action_reveal | atmosphere
    requires_knowledge_ids: frozenset[str] = frozenset()
    requires_world_state: dict[str, Any] = field(default_factory=dict)
    fact_ids: frozenset[str] = frozenset()

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> ContentBlock:
        return cls(
            block_id=str(raw.get("block_id", "")),
            text=str(raw.get("text", "")),
            provenance=str(raw.get("provenance", "atmosphere")),
            requires_knowledge_ids=frozenset(raw.get("requires_knowledge_ids") or []),
            requires_world_state=dict(raw.get("requires_world_state") or {}),
            fact_ids=frozenset(raw.get("fact_ids") or []),
        )


@dataclass
class PlayableEvent:
    event_id: str
    unit_id: str
    location_id: str
    event_kind: str
    physical_location_id: str
    variant_of: str | None = None
    required_knowledge_ids: frozenset[str] = frozenset()
    forbidden_knowledge_ids: frozenset[str] = frozenset()
    required_world_state: dict[str, Any] = field(default_factory=dict)
    forbidden_world_state: dict[str, Any] = field(default_factory=dict)
    relevant_knowledge_dependencies: frozenset[str] = frozenset()
    relevant_world_state_dependencies: frozenset[str] = frozenset()
    relevant_interaction_dependencies: frozenset[str] = frozenset()
    observable_entities: frozenset[str] = frozenset()
    observable_objects: frozenset[str] = frozenset()
    structured_actions: list[StructuredAction] = field(default_factory=list)
    content_blocks: list[ContentBlock] = field(default_factory=list)
    supersedes_unit_id: str | None = None
    time_layer: str | None = None
    template_unit_id: str | None = None
    state_snapshot: dict[str, Any] | None = None

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> PlayableEvent:
        actions = [StructuredAction.from_dict(a) for a in raw.get("structured_actions") or []]
        blocks = [ContentBlock.from_dict(b) for b in raw.get("content_blocks") or []]
        return cls(
            event_id=str(raw.get("event_id", "")),
            unit_id=str(raw.get("unit_id", "")),
            location_id=str(raw.get("location_id", "")),
            event_kind=str(raw.get("event_kind", "location_hub")),
            physical_location_id=str(raw.get("physical_location_id", raw.get("location_id", ""))),
            variant_of=raw.get("variant_of"),
            required_knowledge_ids=frozenset(raw.get("required_knowledge_ids") or []),
            forbidden_knowledge_ids=frozenset(raw.get("forbidden_knowledge_ids") or []),
            required_world_state=dict(raw.get("required_world_state") or {}),
            forbidden_world_state=dict(raw.get("forbidden_world_state") or {}),
            relevant_knowledge_dependencies=frozenset(raw.get("relevant_knowledge_dependencies") or []),
            relevant_world_state_dependencies=frozenset(raw.get("relevant_world_state_dependencies") or []),
            relevant_interaction_dependencies=frozenset(raw.get("relevant_interaction_dependencies") or []),
            observable_entities=frozenset(raw.get("observable_entities") or []),
            observable_objects=frozenset(raw.get("observable_objects") or []),
            structured_actions=actions,
            content_blocks=blocks,
            supersedes_unit_id=raw.get("supersedes_unit_id"),
            time_layer=raw.get("time_layer"),
            template_unit_id=raw.get("template_unit_id"),
            state_snapshot=raw.get("state_snapshot"),
        )


@dataclass
class EpistemicState:
    """Player-visible epistemic snapshot used for gating and validation."""

    player_knowledge: frozenset[str] = frozenset()
    world_state: dict[str, Any] = field(default_factory=dict)
    interaction_state: dict[str, Any] = field(default_factory=dict)
    observable_entities: frozenset[str] = frozenset()
    observable_objects: frozenset[str] = frozenset()
    current_unit_id: str = ""
    time_layer: str | None = None
    visited_events: frozenset[str] = frozenset()

    def copy(self) -> EpistemicState:
        return EpistemicState(
            player_knowledge=self.player_knowledge,
            world_state=dict(self.world_state),
            interaction_state=dict(self.interaction_state),
            observable_entities=self.observable_entities,
            observable_objects=self.observable_objects,
            current_unit_id=self.current_unit_id,
            time_layer=self.time_layer,
            visited_events=self.visited_events,
        )

    def apply_action_deltas(self, action: StructuredAction) -> EpistemicState:
        next_state = self.copy()
        next_state.player_knowledge = frozenset(
            set(next_state.player_knowledge) | set(action.knowledge_delta)
        )
        merged = dict(next_state.world_state)
        merged.update(action.world_state_delta)
        next_state.world_state = merged
        merged_int = dict(next_state.interaction_state)
        merged_int.update(action.interaction_delta)
        completed = set(merged_int.get("completed_topics") or [])
        for topic in action.interaction_delta.get("completed_topics") or []:
            completed.add(str(topic))
        if completed:
            merged_int["completed_topics"] = sorted(completed)
        next_state.interaction_state = merged_int
        if action.exhaustion in ("one_time", "exhaustible"):
            exhausted = set(next_state.interaction_state.get("exhausted_actions", []))
            exhausted.add(action.action_id)
            next_state.interaction_state["exhausted_actions"] = sorted(exhausted)
        return next_state


@dataclass
class EpistemicPackage:
    schema_version: str
    adventure_id: str
    initial_player_knowledge: frozenset[str]
    initial_world_state: dict[str, Any]
    initial_observable_entities: frozenset[str]
    initial_observable_objects: frozenset[str]
    events: dict[str, PlayableEvent]
    events_by_unit: dict[str, PlayableEvent]
    events_by_location: dict[str, list[PlayableEvent]]
