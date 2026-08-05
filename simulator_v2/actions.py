"""Legal action definitions for Simulator v2."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ActionKind(str, Enum):
    NAVIGATE = "navigate"
    OBJECT = "object"
    CHECK = "check"
    NPC = "npc"
    HYPOTHESIS = "hypothesis"
    ADVANCE_TIME = "advance_time"
    ACCUSATION = "accusation"
    SPLIT = "split"
    REGROUP = "regroup"
    REVISIT = "revisit"


@dataclass(frozen=True)
class LegalAction:
    action_id: str
    kind: ActionKind
    player_label: str
    canonical_source_id: str
    source_file: str
    time_cost_minutes: int
    repeat_policy: str
    destination: str
    eligibility_reason: str
    state_effects: dict[str, Any] = field(default_factory=dict)
    payload: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "action_id": self.action_id,
            "kind": self.kind.value,
            "player_label": self.player_label,
            "canonical_source_id": self.canonical_source_id,
            "source_file": self.source_file,
            "time_cost_minutes": self.time_cost_minutes,
            "repeat_policy": self.repeat_policy,
            "destination": self.destination,
            "eligibility_reason": self.eligibility_reason,
            "state_effects": self.state_effects,
        }
