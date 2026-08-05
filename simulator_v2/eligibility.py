"""Eligibility checks for legal actions."""

from __future__ import annotations

from typing import Any

from simulator_v2.derivation import CanonicalSimulationModel
from simulator_v2.state import SimulationState


def _clock_index(model: CanonicalSimulationModel, clock: str) -> int:
    try:
        return model.clocks.index(clock)
    except ValueError:
        return -1


def location_access(state: SimulationState, model: CanonicalSimulationModel, location_id: str) -> bool:
    env = model.raw_packages.get("environment", {})
    variants = state.ending_chain_state.get("location_variants", {})
    active_variant = variants.get(location_id)
    for loc_state in env.get("location_states", []) or []:
        if loc_state.get("location_id") != location_id:
            continue
        if active_variant and loc_state.get("variant_label") != active_variant:
            continue
        if not active_variant and loc_state.get("variant_label") not in ("default", None):
            if loc_state.get("active_from_clock"):
                if _clock_index(model, state.in_world_clock) < _clock_index(model, str(loc_state["active_from_clock"])):
                    continue
            elif loc_state.get("variant_label") != "default":
                continue
        attrs = loc_state.get("attributes", {})
        if attrs.get("access") == "locked":
            if state.flow_flags.get("basement_open"):
                return True
            if "ITEM-KEY" in state.items:
                return True
            return False
        return attrs.get("access", "open") == "open"
    if state.flow_flags.get("basement_open") and location_id == "LOC-BASEMENT":
        return True
    if location_id == "LOC-BASEMENT" and "ITEM-KEY" in state.items:
        return True
    return location_id != "LOC-BASEMENT"


def check_condition(
    condition: dict[str, Any] | None,
    state: SimulationState,
    model: CanonicalSimulationModel,
    npc_id: str = "",
) -> bool:
    if not condition:
        return True
    ctype = condition.get("type", "always")
    if ctype == "always":
        return True
    if ctype == "location_state":
        loc = condition.get("location_id", "")
        return location_access(state, model, loc)
    if ctype == "knowledge_held":
        kid = condition.get("knowledge_id", "")
        return kid in state.player_knowledge
    if ctype == "trust_threshold":
        nid = condition.get("npc_id", npc_id)
        dyn = state.npc_dynamic.get(nid, {})
        return int(dyn.get("trust", 0)) >= int(condition.get("min", 0))
    if ctype == "trust":
        nid = condition.get("npc_id", npc_id)
        dyn = state.npc_dynamic.get(nid, {})
        return int(dyn.get("trust", 0)) >= int(condition.get("min", 0))
    if ctype == "object_discovered":
        oid = condition.get("object_id", "")
        ostate = state.object_states.get(oid, "")
        return ostate not in ("concealed", "hidden", "")
    if ctype == "world_time":
        return _clock_index(model, state.in_world_clock) >= _clock_index(model, str(condition.get("clock", "")))
    return False


def object_visible(state: SimulationState, obj: dict[str, Any], parent_approached: set[str]) -> bool:
    oid = obj.get("object_id", "")
    ostate = state.object_states.get(oid, obj.get("initial_state", ""))
    if ostate == "collected":
        return False
    req = obj.get("visibility_requirement", "")
    if ostate == "concealed" and oid not in parent_approached:
        return False
    if req == "hidden_until_discovered":
        return ostate not in ("concealed", "hidden")
    if req == "after_parent_approached":
        parent = obj.get("parent_id", "")
        return parent in parent_approached or state.object_states.get(parent) in ("approached", "searched", "accessed")
    return True


def one_attempt_available(state: SimulationState, check_id: str) -> bool:
    return state.check_attempts.get(check_id, 0) < 1
