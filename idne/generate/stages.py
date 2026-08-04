"""Canonical generation stage definitions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

STAGE_ORDER: list[str] = [
    "adventure_brief",
    "fixed_truth",
    "causal_timeline",
    "world_state_timeline",
    "npcs",
    "environment",
    "objects",
    "investigation_core",
    "npc_conversation",
    "investigation_flow",
    "capability_checks",
    "story_player",
    "playtime",
    "dm_feeling",
    "final_validation",
    "package_export",
]

LOGIC_STAGES = frozenset(
    {
        "fixed_truth",
        "causal_timeline",
        "world_state_timeline",
        "npcs",
        "environment",
        "objects",
        "investigation_core",
        "npc_conversation",
        "investigation_flow",
        "capability_checks",
    }
)

PLAYER_STAGES = frozenset({"story_player"})

HUMAN_APPROVAL_STAGES = frozenset(
    {
        "adventure_brief",
        "fixed_truth",
        "npcs",
        "investigation_flow",
        "package_export",
    }
)

STORY_CRITICAL_FIELDS = frozenset(
    {
        "culprit_id",
        "motive",
        "method",
        "timeline_truth",
        "npc_motivation",
        "relationship",
        "conclusion_logic",
        "ending_meaning",
        "route_structure",
    }
)


@dataclass(frozen=True)
class StageDefinition:
    stage_id: str
    validator_name: str | None
    requires_logic_complete: bool = False
    requires_human_approval: bool = False


STAGE_DEFINITIONS: dict[str, StageDefinition] = {
    "adventure_brief": StageDefinition("adventure_brief", None, requires_human_approval=True),
    "fixed_truth": StageDefinition("fixed_truth", "world_first", requires_human_approval=True),
    "causal_timeline": StageDefinition("causal_timeline", None),
    "world_state_timeline": StageDefinition("world_state_timeline", None),
    "npcs": StageDefinition("npcs", "world_first", requires_human_approval=True),
    "environment": StageDefinition("environment", "environment"),
    "objects": StageDefinition("objects", "object_interaction"),
    "investigation_core": StageDefinition("investigation_core", "investigation_core"),
    "npc_conversation": StageDefinition("npc_conversation", "npc_investigation"),
    "investigation_flow": StageDefinition(
        "investigation_flow", "investigation_flow", requires_human_approval=True
    ),
    "capability_checks": StageDefinition("capability_checks", "capability_check"),
    "story_player": StageDefinition("story_player", "story", requires_logic_complete=True),
    "playtime": StageDefinition("playtime", "playtime"),
    "dm_feeling": StageDefinition("dm_feeling", "dm_feeling"),
    "final_validation": StageDefinition("final_validation", "integrated"),
    "package_export": StageDefinition("package_export", None, requires_human_approval=True),
}


def stage_index(stage_id: str) -> int:
    return STAGE_ORDER.index(stage_id)


def downstream_stages(stage_id: str) -> list[str]:
    idx = stage_index(stage_id)
    return STAGE_ORDER[idx + 1:]


def logic_complete_stage_ids() -> list[str]:
    return [s for s in STAGE_ORDER if s in LOGIC_STAGES]
