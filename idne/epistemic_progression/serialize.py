"""Serialize epistemic progression models to JSON-compatible dicts."""

from __future__ import annotations

from typing import Any

from idne.epistemic_progression.model import ContentBlock, PlayableEvent, StructuredAction


def _action_to_dict(action: StructuredAction) -> dict[str, Any]:
    return {
        "action_id": action.action_id,
        "action_type": action.action_type,
        "label": action.label,
        "destination_unit_id": action.destination_unit_id,
        "requires_knowledge_ids": sorted(action.requires_knowledge_ids),
        "forbidden_knowledge_ids": sorted(action.forbidden_knowledge_ids),
        "requires_world_state": dict(action.requires_world_state),
        "forbidden_world_state": dict(action.forbidden_world_state),
        "requires_observable": sorted(action.requires_observable),
        "referenced_fact_ids": sorted(action.referenced_fact_ids),
        "referenced_entity_ids": sorted(action.referenced_entity_ids),
        "exhaustion": action.exhaustion,
        "knowledge_delta": sorted(action.knowledge_delta),
        "world_state_delta": dict(action.world_state_delta),
        "interaction_delta": dict(action.interaction_delta),
        "investigative": action.investigative,
        "purpose": action.purpose,
    }


def _block_to_dict(block: ContentBlock) -> dict[str, Any]:
    return {
        "block_id": block.block_id,
        "text": block.text,
        "provenance": block.provenance,
        "requires_knowledge_ids": sorted(block.requires_knowledge_ids),
        "requires_world_state": dict(block.requires_world_state),
        "fact_ids": sorted(block.fact_ids),
    }


def event_to_dict(event: PlayableEvent) -> dict[str, Any]:
    out: dict[str, Any] = {
        "event_id": event.event_id,
        "unit_id": event.unit_id,
        "location_id": event.location_id,
        "event_kind": event.event_kind,
        "physical_location_id": event.physical_location_id,
        "required_knowledge_ids": sorted(event.required_knowledge_ids),
        "forbidden_knowledge_ids": sorted(event.forbidden_knowledge_ids),
        "required_world_state": dict(event.required_world_state),
        "forbidden_world_state": dict(event.forbidden_world_state),
        "relevant_knowledge_dependencies": sorted(event.relevant_knowledge_dependencies),
        "relevant_world_state_dependencies": sorted(event.relevant_world_state_dependencies),
        "relevant_interaction_dependencies": sorted(event.relevant_interaction_dependencies),
        "observable_entities": sorted(event.observable_entities),
        "observable_objects": sorted(event.observable_objects),
        "structured_actions": [_action_to_dict(a) for a in event.structured_actions],
        "content_blocks": [_block_to_dict(b) for b in event.content_blocks],
    }
    if event.variant_of:
        out["variant_of"] = event.variant_of
    if event.supersedes_unit_id:
        out["supersedes_unit_id"] = event.supersedes_unit_id
    if event.time_layer:
        out["time_layer"] = event.time_layer
    if event.template_unit_id:
        out["template_unit_id"] = event.template_unit_id
    if event.state_snapshot is not None:
        out["state_snapshot"] = event.state_snapshot
    return out
