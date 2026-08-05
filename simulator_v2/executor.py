"""Apply legal actions to simulation state."""

from __future__ import annotations

from typing import Any

from simulator_v2.actions import ActionKind, LegalAction
from simulator_v2.derivation import CanonicalSimulationModel
from simulator_v2.eligibility import location_access
from simulator_v2.rng import DeterministicRNG
from simulator_v2.state import SimulationState

CAP_FILE = "DO_NOT_READ/capability_check_package.json"
OBJ_FILE = "DO_NOT_READ/object_interaction_package.json"


def _apply_time(state: SimulationState, minutes: int) -> None:
    state.in_world_minutes += minutes


def _update_revisit(state: SimulationState, location_id: str) -> None:
    visited = state.ending_chain_state.setdefault("visited_locations", [])
    counts = state.ending_chain_state.setdefault("revisit_counts", {})
    if location_id in visited:
        counts[location_id] = counts.get(location_id, 1) + 1
    else:
        visited.append(location_id)
        counts[location_id] = 1


def _apply_location_variants(state: SimulationState, model: CanonicalSimulationModel) -> None:
    env = model.raw_packages.get("environment", {})
    variants = state.ending_chain_state.setdefault("location_variants", {})
    clocks = model.clocks or []
    idx = clocks.index(state.in_world_clock) if state.in_world_clock in clocks else 0
    for loc_state in env.get("location_states", []) or []:
        loc_id = loc_state.get("location_id", "")
        active_from = loc_state.get("active_from_clock")
        if active_from and idx >= clocks.index(active_from):
            variants[loc_id] = loc_state.get("variant_label", "default")
            if loc_id == "LOC-BASEMENT" and loc_state.get("attributes", {}).get("access") == "open":
                state.flow_flags["basement_open"] = True


def _grant_knowledge(state: SimulationState, knowledge_ids: list[str], model: CanonicalSimulationModel) -> None:
    for kid in knowledge_ids:
        if not kid:
            continue
        state.player_knowledge.add(kid)
        k = model.knowledge.get(kid)
        if k:
            acq = k.payload.get("acquisition", {})
            if acq.get("source_type") == "testimony":
                state.testimony.add(kid)


def _resolve_result_unit_id(check: dict[str, Any], obj_pkg: dict[str, Any], *, success: bool) -> str:
    """Prefer object-layer check_binding destinations when cap-layer IDs differ."""
    key = "success_destination" if success else "failure_destination"
    cap_dest = check.get("destinations", {}).get(key, "")
    act_id = check.get("parent_action_id", "")
    for act in obj_pkg.get("actions", []) or []:
        if act.get("action_id") != act_id:
            continue
        binding = act.get("check_binding", {}) or {}
        obj_dest = binding.get(key, "")
        if obj_dest:
            unit_ids = {u.get("unit_id") for u in obj_pkg.get("result_units", []) or []}
            if obj_dest in unit_ids:
                return obj_dest
        break
    return cap_dest


def _collect_item_from_object(
    state: SimulationState,
    model: CanonicalSimulationModel,
    object_id: str,
) -> None:
    obj_pkg = model.raw_packages.get("object_interaction", {})
    for obj in obj_pkg.get("objects", []) or []:
        if obj.get("object_id") != object_id:
            continue
        if obj.get("object_type") != "item_concealed":
            return
        item_id = obj.get("item_id", "")
        if not item_id:
            for reg in obj_pkg.get("items_registry", []) or []:
                if reg.get("item_id", "").endswith("KEY") or object_id.endswith("KEY-HIDDEN"):
                    item_id = reg.get("item_id", "")
                    break
            if not item_id and object_id == "OBJ-KEY-HIDDEN":
                item_id = "ITEM-KEY"
        if item_id:
            state.items.add(item_id)
        state.object_states[object_id] = "collected"
        return


def _evaluate_endings(state: SimulationState, model: CanonicalSimulationModel) -> str | None:
    flow = model.raw_packages.get("investigation_flow", {})
    order = flow.get("ending_graph", {}).get("evaluation_order") or list(model.endings.keys())
    for eid in order:
        ending = model.endings.get(eid)
        if not ending:
            continue
        trigger = ending.payload.get("trigger", {})
        ttype = trigger.get("type", "")
        if ttype == "deadline_expired":
            deadline = flow.get("deadline", {}).get("deadline_clock", "T_DEADLINE")
            if state.in_world_clock == deadline:
                return eid
            continue
        if ttype == "state_driven":
            req_k = set(trigger.get("required_knowledge_ids", []) or [])
            if req_k and not req_k.issubset(state.player_knowledge):
                continue
            req_state = trigger.get("required_state", {}) or {}
            if any(state.flow_flags.get(k) != v for k, v in req_state.items()):
                continue
            req_acc = trigger.get("required_accusation", {}) or {}
            answers = state.ending_chain_state.get("accusation_answers", {})
            if req_acc and not all(answers.get(k) == v for k, v in req_acc.items()):
                continue
            min_count = trigger.get("min_knowledge_count")
            if min_count and len(state.player_knowledge) < int(min_count):
                continue
            return eid
    return None


def apply_action(
    state: SimulationState,
    model: CanonicalSimulationModel,
    action: LegalAction,
    rng: DeterministicRNG,
    *,
    check_modifier: int = 5,
    accusation_answer: str = "NPC-A",
) -> dict[str, Any]:
    """Apply one legal action; returns result metadata. Never mutates fixed truth."""
    result: dict[str, Any] = {"action_id": action.action_id, "kind": action.kind.value, "success": True}

    if action.kind == ActionKind.NAVIGATE:
        dest = action.payload.get("destination_location_id", action.destination)
        _apply_time(state, action.time_cost_minutes)
        state.location_id = dest
        _update_revisit(state, dest)
        result["destination"] = dest
        return result

    if action.kind == ActionKind.OBJECT:
        act = action.payload
        oid = act.get("object_id", "")
        depth = act.get("interaction_depth", "")
        _apply_time(state, action.time_cost_minutes)
        if depth:
            state.object_states[oid] = depth
        binding = act.get("check_binding")
        cap_pkg = model.raw_packages.get("capability_check", {})
        cap_check = None
        for chk in cap_pkg.get("checks", []) or []:
            if chk.get("parent_action_id") == act.get("action_id"):
                cap_check = chk
                break
        if cap_check:
            return _apply_check(state, model, cap_check, rng, check_modifier, result)
        return result

    if action.kind == ActionKind.CHECK:
        return _apply_check(state, model, action.payload, rng, check_modifier, result)

    if action.kind == ActionKind.NPC:
        node = action.payload
        npc_id = ""
        for conv in model.raw_packages.get("npc_investigation", {}).get("conversation_graph", []) or []:
            for n in conv.get("nodes", []) or []:
                if n.get("node_id") == action.canonical_source_id:
                    npc_id = conv.get("npc_id", "")
        _apply_time(state, action.time_cost_minutes)
        topics = state.conversation_state.setdefault("topics_revealed", {})
        topics.setdefault(npc_id, []).append(action.canonical_source_id)
        npc_pkg = model.raw_packages.get("npc_investigation", {})
        npc_info = set(state.npc_dynamic.get(npc_id, {}).get("information_known", []) or [])
        info_to_knowledge = {
            row.get("info_id", ""): row.get("knowledge_id", "")
            for row in npc_pkg.get("information_known_model", []) or []
            if row.get("npc_id") == npc_id
        }
        for link in npc_pkg.get("testimony_links", []) or []:
            if link.get("conversation_node_id") != action.canonical_source_id:
                continue
            kid = link.get("grants_knowledge_id", "")
            if not kid:
                continue
            if not npc_info:
                continue
            if any(info_to_knowledge.get(iid) == kid for iid in npc_info):
                _grant_knowledge(state, [kid], model)
        result["npc_id"] = npc_id
        return result

    if action.kind == ActionKind.HYPOTHESIS:
        _apply_time(state, action.time_cost_minutes)
        state.hypotheses.add(action.canonical_source_id)
        kid = action.payload.get("yields_knowledge_id")
        if kid:
            _grant_knowledge(state, [kid], model)
        return result

    if action.kind == ActionKind.ADVANCE_TIME:
        state.in_world_clock = action.destination
        _apply_time(state, action.time_cost_minutes)
        _apply_location_variants(state, model)
        ending = _evaluate_endings(state, model)
        if ending:
            state.ending_chain_state["ending_id"] = ending
            result["ending_id"] = ending
        return result

    if action.kind == ActionKind.REVISIT:
        rule = action.payload
        updates = rule.get("state_updates", {}) or {}
        for k, v in updates.items():
            if k in state.flow_flags:
                state.flow_flags[k] = v
            elif k in state.flow_counters:
                state.flow_counters[k] = v
        _apply_time(state, action.time_cost_minutes)
        return result

    if action.kind == ActionKind.ACCUSATION:
        _apply_time(state, action.time_cost_minutes)
        answers = state.ending_chain_state.setdefault("accusation_answers", {})
        answers[action.canonical_source_id] = accusation_answer
        state.flow_flags["accusation_complete"] = True
        state.conclusions.add(action.payload.get("conclusion_id", ""))
        _apply_relationship_reactions(state, model, accusation_answer)
        ending = _evaluate_endings(state, model)
        if not ending:
            ending = "END-PARTIAL"
        state.ending_chain_state["ending_id"] = ending
        result["ending_id"] = ending
        result["accusation"] = accusation_answer
        return result

    if action.kind == ActionKind.SPLIT and state.two_player:
        state.two_player.split_active = True
        state.two_player.active_role = "people"
        return result

    if action.kind == ActionKind.REGROUP and state.two_player:
        state.two_player.split_active = False
        state.two_player.active_role = "joint"
        state.two_player.regroup_pending = False
        return result

    return result


def _apply_check(
    state: SimulationState,
    model: CanonicalSimulationModel,
    check: dict[str, Any],
    rng: DeterministicRNG,
    modifier: int,
    result: dict[str, Any],
) -> dict[str, Any]:
    check_id = check.get("check_id", "")
    state.check_attempts[check_id] = state.check_attempts.get(check_id, 0) + 1
    roll = rng.roll_check(modifier)
    dc = int(check.get("dc", 10))
    success = roll >= dc
    result["check_roll"] = roll
    result["check_dc"] = dc
    result["check_success"] = success
    obj_pkg = model.raw_packages.get("object_interaction", {})
    if success:
        grants = check.get("success_effects", {}).get("grants_knowledge_ids", []) or []
        _grant_knowledge(state, grants, model)
        for info in check.get("success_effects", {}).get("reveals_information_ids", []) or []:
            state.observations.add(info)
        act_id = check.get("parent_action_id", "")
        for act in obj_pkg.get("actions", []) or []:
            if act.get("action_id") == act_id:
                oid = act.get("object_id", "")
                if oid:
                    state.object_states[oid] = act.get("interaction_depth", "searched")
        dest = _resolve_result_unit_id(check, obj_pkg, success=True)
        for unit in obj_pkg.get("result_units", []) or []:
            if unit.get("unit_id") == dest:
                for info in unit.get("reveals_information", []) or []:
                    state.observations.add(info)
                for child in unit.get("reveals_child_objects", []) or []:
                    state.object_states[child] = "discovered"
                    _collect_item_from_object(state, model, child)
                break
        act_id = check.get("parent_action_id", "")
        for act in obj_pkg.get("actions", []) or []:
            if act.get("action_id") != act_id:
                continue
            binding = act.get("check_binding", {}) or {}
            for info in binding.get("information_on_success", []) or []:
                state.observations.add(info)
            break
    else:
        dest = _resolve_result_unit_id(check, obj_pkg, success=False)
        leaked = bool(
            check.get("failure_effects", {}).get("grants_knowledge_ids")
            or check.get("failure_effects", {}).get("reveals_information_ids")
        )
        for unit in obj_pkg.get("result_units", []) or []:
            if unit.get("unit_id") == dest:
                leaked = leaked or bool(unit.get("reveals_information"))
                break
        result["failure_leaked"] = leaked
        state.ending_chain_state["failed_checks"] = state.ending_chain_state.get("failed_checks", 0) + 1
    _apply_time(state, int(check.get("time_cost_minutes", 0)))
    return result


def _apply_relationship_reactions(
    state: SimulationState,
    model: CanonicalSimulationModel,
    accused_npc_id: str,
) -> None:
    npc_pkg = model.raw_packages.get("npc_investigation", {})
    for mod in npc_pkg.get("trust_model", {}).get("modifiers", []) or []:
        if mod.get("trigger") != "player_accuses_npc":
            continue
        if mod.get("target_npc_id") != accused_npc_id:
            continue
        subject = mod.get("subject_npc_id", "")
        reaction = mod.get("relationship_reaction", {}) or {}
        rel_type = reaction.get("if_relationship", "")
        delta = int(reaction.get("trust_delta", 0))
        if not subject or not delta:
            continue
        for npc in npc_pkg.get("npcs", []) or []:
            if npc.get("npc_id") != subject:
                continue
            for rel in npc.get("relationships", []) or []:
                if rel.get("target_npc_id") == accused_npc_id and rel.get("relationship_type") == rel_type:
                    dyn = state.npc_dynamic.setdefault(subject, {})
                    dyn["trust"] = int(dyn.get("trust", 0)) + delta
                    break
    for react in npc_pkg.get("relationship_reactions", []) or []:
        if react.get("trigger") != "accuse_npc" or react.get("target_npc_id") != accused_npc_id:
            continue
        actor = react.get("actor_npc_id", "")
        if actor:
            dyn = state.npc_dynamic.setdefault(actor, {})
            dyn["trust"] = int(dyn.get("trust", 0)) + int(react.get("trust_delta", 0))
