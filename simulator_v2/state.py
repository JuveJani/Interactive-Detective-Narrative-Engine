"""Immutable / copyable simulation state for Simulator v2."""

from __future__ import annotations

import copy
import json
from dataclasses import dataclass, field
from typing import Any

from simulator_v2.derivation import CanonicalSimulationModel


@dataclass
class TwoPlayerState:
    active_role: str = "joint"
    people_location_id: str = ""
    records_location_id: str = ""
    private_knowledge: dict[str, set[str]] = field(default_factory=lambda: {"people": set(), "records": set()})
    split_active: bool = False
    regroup_pending: bool = False

    def copy(self) -> TwoPlayerState:
        return TwoPlayerState(
            active_role=self.active_role,
            people_location_id=self.people_location_id,
            records_location_id=self.records_location_id,
            private_knowledge={k: set(v) for k, v in self.private_knowledge.items()},
            split_active=self.split_active,
            regroup_pending=self.regroup_pending,
        )


@dataclass
class SimulationState:
    """Player-visible simulation state; never mutates fixed world truth."""

    adventure_id: str
    play_mode: str
    location_id: str
    location_variant: str
    in_world_clock: str
    in_world_minutes: int
    object_states: dict[str, str]
    items: set[str]
    observations: set[str]
    player_knowledge: set[str]
    testimony: set[str]
    hypotheses: set[str]
    conclusions: set[str]
    proof_status: dict[str, bool]
    check_attempts: dict[str, int]
    npc_locations: dict[str, str]
    npc_availability: dict[str, str]
    npc_dynamic: dict[str, dict[str, Any]]
    conversation_state: dict[str, Any]
    world_triggers: set[str]
    flow_flags: dict[str, Any]
    flow_counters: dict[str, int]
    ending_chain_state: dict[str, Any]
    two_player: TwoPlayerState | None = None
    state_id: int = 0

    def copy(self) -> SimulationState:
        cloned = SimulationState(
            adventure_id=self.adventure_id,
            play_mode=self.play_mode,
            location_id=self.location_id,
            location_variant=self.location_variant,
            in_world_clock=self.in_world_clock,
            in_world_minutes=self.in_world_minutes,
            object_states=dict(self.object_states),
            items=set(self.items),
            observations=set(self.observations),
            player_knowledge=set(self.player_knowledge),
            testimony=set(self.testimony),
            hypotheses=set(self.hypotheses),
            conclusions=set(self.conclusions),
            proof_status=dict(self.proof_status),
            check_attempts=dict(self.check_attempts),
            npc_locations=dict(self.npc_locations),
            npc_availability=dict(self.npc_availability),
            npc_dynamic={k: dict(v) for k, v in self.npc_dynamic.items()},
            conversation_state=dict(self.conversation_state),
            world_triggers=set(self.world_triggers),
            flow_flags=dict(self.flow_flags),
            flow_counters=dict(self.flow_counters),
            ending_chain_state=dict(self.ending_chain_state),
            two_player=self.two_player.copy() if self.two_player else None,
            state_id=self.state_id,
        )
        return cloned

    def identity_key(self) -> str:
        payload = {
            "location_id": self.location_id,
            "location_variant": self.location_variant,
            "in_world_clock": self.in_world_clock,
            "object_states": self.object_states,
            "items": sorted(self.items),
            "player_knowledge": sorted(self.player_knowledge),
            "flow_flags": self.flow_flags,
            "flow_counters": self.flow_counters,
            "two_player": None
            if not self.two_player
            else {
                "active_role": self.two_player.active_role,
                "split_active": self.two_player.split_active,
            },
        }
        return json.dumps(payload, sort_keys=True)

    def with_state_id(self, state_id: int) -> SimulationState:
        cloned = self.copy()
        cloned.state_id = state_id
        return cloned


def initial_state_from_model(model: CanonicalSimulationModel) -> SimulationState:
    env_pkg = model.raw_packages.get("environment", {})
    start_location = str(env_pkg.get("start_location_id", "LOC-LOBBY"))
    if start_location not in model.locations:
        for loc in model.locations.values():
            if loc.payload.get("location_id"):
                start_location = str(loc.payload["location_id"])
                break

    flow_flags: dict[str, Any] = {}
    flow_counters: dict[str, int] = {}
    for key, val in model.flow_initial_state.items():
        if isinstance(val, bool):
            flow_flags[key] = val
        elif isinstance(val, int):
            flow_counters[key] = val
        else:
            flow_flags[key] = val

    object_states = {
        oid: str(obj.payload.get("initial_state", obj.payload.get("current_state", "unknown")))
        for oid, obj in sorted(model.objects.items())
    }

    npc_locations: dict[str, str] = {}
    npc_dynamic: dict[str, dict[str, Any]] = {}
    npc_availability: dict[str, str] = {}
    for npc_id, npc in sorted(model.npcs.items()):
        npc_locations[npc_id] = ""
        npc_availability[npc_id] = "available"
        npc_dynamic[npc_id] = dict(npc.payload.get("initial_dynamic_state", {}) or {})

    clocks = model.clocks or ["T0"]
    two_player = TwoPlayerState() if model.play_mode == "two_player" else None

    return SimulationState(
        adventure_id=model.adventure_id,
        play_mode=model.play_mode,
        location_id=start_location,
        location_variant="default",
        in_world_clock=clocks[0],
        in_world_minutes=0,
        object_states=object_states,
        items=set(),
        observations=set(),
        player_knowledge=set(),
        testimony=set(),
        hypotheses=set(),
        conclusions=set(),
        proof_status={cid: False for cid in sorted(model.conclusions.keys())},
        check_attempts={cid: 0 for cid in sorted(model.checks.keys())},
        npc_locations=npc_locations,
        npc_availability=npc_availability,
        npc_dynamic=npc_dynamic,
        conversation_state={"topics_revealed": {}, "active_npc": None},
        world_triggers=set(),
        flow_flags=flow_flags,
        flow_counters=flow_counters,
        ending_chain_state={
            "active": True,
            "evaluated_endings": [],
            "ending_id": None,
            "visited_locations": [start_location],
            "revisit_counts": {start_location: 1},
            "location_variants": {},
            "accusation_answers": {},
        },
        two_player=two_player,
        state_id=0,
    )
