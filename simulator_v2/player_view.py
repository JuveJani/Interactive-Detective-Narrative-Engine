"""Player-visible state view — strategies must use this, not canonical truth."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from simulator_v2.state import SimulationState


@dataclass
class PlayerView:
    """Adventure-independent player-visible snapshot."""

    location_id: str
    location_variant: str
    in_world_clock: str
    in_world_minutes: int
    player_knowledge: frozenset[str]
    items: frozenset[str]
    observations: frozenset[str]
    flow_flags: dict[str, Any]
    npc_trust: dict[str, int]
    object_states: dict[str, str]
    available_action_ids: list[str]
    available_action_labels: list[str]
    play_mode: str
    split_active: bool = False
    active_role: str = "joint"

    @classmethod
    def from_state(cls, state: SimulationState, legal_action_ids: list[str], legal_labels: list[str]) -> PlayerView:
        npc_trust = {
            npc_id: int(dyn.get("trust", 0))
            for npc_id, dyn in state.npc_dynamic.items()
        }
        split_active = bool(state.two_player and state.two_player.split_active)
        active_role = state.two_player.active_role if state.two_player else "joint"
        return cls(
            location_id=state.location_id,
            location_variant=state.location_variant,
            in_world_clock=state.in_world_clock,
            in_world_minutes=state.in_world_minutes,
            player_knowledge=frozenset(state.player_knowledge),
            items=frozenset(state.items),
            observations=frozenset(state.observations),
            flow_flags=dict(state.flow_flags),
            npc_trust=npc_trust,
            object_states=dict(state.object_states),
            available_action_ids=list(legal_action_ids),
            available_action_labels=list(legal_labels),
            play_mode=state.play_mode,
            split_active=split_active,
            active_role=active_role,
        )
