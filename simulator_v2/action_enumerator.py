"""Enumerate legal actions from canonical packages."""

from __future__ import annotations

from simulator_v2.actions import ActionKind, LegalAction
from simulator_v2.derivation import CanonicalSimulationModel
from simulator_v2.eligibility import check_condition, location_access, object_visible, one_attempt_available
from simulator_v2.state import SimulationState

ENV_FILE = "DO_NOT_READ/environment_package.json"
OBJ_FILE = "DO_NOT_READ/object_interaction_package.json"
NPC_FILE = "DO_NOT_READ/npc_investigation_package.json"
CORE_FILE = "DO_NOT_READ/investigation_core_package.json"
CAP_FILE = "DO_NOT_READ/capability_check_package.json"
FLOW_FILE = "DO_NOT_READ/investigation_flow_package.json"


def _approached_objects(state: SimulationState) -> set[str]:
    return {oid for oid, st in state.object_states.items() if st in ("approached", "searched", "accessed")}


def enumerate_legal_actions(state: SimulationState, model: CanonicalSimulationModel) -> list[LegalAction]:
    if state.ending_chain_state.get("ending_id"):
        return []

    actions: list[LegalAction] = []
    env = model.raw_packages.get("environment", {})
    obj_pkg = model.raw_packages.get("object_interaction", {})
    npc_pkg = model.raw_packages.get("npc_investigation", {})
    flow = model.raw_packages.get("investigation_flow", {})
    cap_pkg = model.raw_packages.get("capability_check", {})

    for nav in env.get("navigation", []) or []:
        if nav.get("source_location_id") != state.location_id:
            continue
        dest = nav.get("destination_location_id", "")
        if not location_access(state, model, dest):
            continue
        actions.append(
            LegalAction(
                action_id=f"nav:{nav.get('nav_id')}",
                kind=ActionKind.NAVIGATE,
                player_label=str(nav.get("player_label", "Travel")),
                canonical_source_id=str(nav.get("nav_id", "")),
                source_file=ENV_FILE,
                time_cost_minutes=int(nav.get("travel_cost_minutes", 0)),
                repeat_policy="allowed",
                destination=dest,
                eligibility_reason="navigation_accessible",
                state_effects={"location_id": dest},
                payload=nav,
            )
        )

    approached = _approached_objects(state)
    for obj in obj_pkg.get("objects", []) or []:
        parent = obj.get("parent_id")
        parent_type = obj.get("parent_type")
        if parent_type == "location" and parent != state.location_id:
            continue
        if parent_type == "object" and parent not in approached and obj.get("object_id") not in approached:
            continue
        if not object_visible(state, obj, approached):
            continue
        oid = obj.get("object_id", "")
        ostate = state.object_states.get(oid, obj.get("initial_state", ""))
        if ostate == "collected":
            continue
        for act in obj_pkg.get("actions", []) or []:
            if act.get("object_id") != oid:
                continue
            act_id = act.get("action_id", "")
            depth = act.get("interaction_depth", "")
            current = state.object_states.get(oid, "")
            if depth == "searched" and current == "searched":
                continue
            if depth == "approached" and current in ("approached", "searched", "accessed"):
                continue
            binding = act.get("check_binding")
            if binding:
                cap_check = _find_cap_check(cap_pkg, act_id)
                check_id = cap_check.get("check_id", binding.get("check_id", "")) if cap_check else binding.get("check_id", "")
                if check_id and not one_attempt_available(state, check_id):
                    continue
            actions.append(
                LegalAction(
                    action_id=f"obj:{act_id}",
                    kind=ActionKind.OBJECT,
                    player_label=str(act.get("player_label", "Interact")),
                    canonical_source_id=act_id,
                    source_file=OBJ_FILE,
                    time_cost_minutes=int(act.get("time_cost_minutes", 0)),
                    repeat_policy="once" if act.get("cost_applied_once") else "allowed",
                    destination=str(act.get("destination_unit", state.location_id)),
                    eligibility_reason="object_interaction",
                    state_effects={"object_id": oid, "depth": depth},
                    payload=act,
                )
            )

    for conv in npc_pkg.get("conversation_graph", []) or []:
        npc_id = conv.get("npc_id", "")
        for node in conv.get("nodes", []) or []:
            requires = node.get("requires", {})
            if int(state.npc_dynamic.get(npc_id, {}).get("trust", 0)) < int(requires.get("trust_min", 0)):
                continue
            if not check_condition({"type": "trust", "npc_id": npc_id, "min": requires.get("trust_min", 0)}, state, model, npc_id):
                continue
            node_id = node.get("node_id", "")
            if node_id in state.conversation_state.get("topics_revealed", {}).get(npc_id, []):
                continue
            actions.append(
                LegalAction(
                    action_id=f"npc:{node_id}",
                    kind=ActionKind.NPC,
                    player_label=str(node.get("player_label", "Talk")),
                    canonical_source_id=node_id,
                    source_file=NPC_FILE,
                    time_cost_minutes=2,
                    repeat_policy="once",
                    destination=npc_id,
                    eligibility_reason="npc_conversation",
                    payload=node,
                )
            )

    for hyp in model.hypotheses.values():
        req = set(hyp.payload.get("requires_knowledge_ids", []) or [])
        if not req.issubset(state.player_knowledge):
            continue
        hid = hyp.entity_id
        if hyp.payload.get("yields_knowledge_id") in state.player_knowledge:
            continue
        actions.append(
            LegalAction(
                action_id=f"hyp:{hid}",
                kind=ActionKind.HYPOTHESIS,
                player_label=f"Consider hypothesis {hid}",
                canonical_source_id=hid,
                source_file=CORE_FILE,
                time_cost_minutes=3,
                repeat_policy="once",
                destination=hid,
                eligibility_reason="hypothesis_ready",
                payload=hyp.payload,
            )
        )

    clocks = model.clocks or []
    idx = clocks.index(state.in_world_clock) if state.in_world_clock in clocks else 0
    if idx + 1 < len(clocks):
        next_clock = clocks[idx + 1]
        actions.append(
            LegalAction(
                action_id=f"time:{next_clock}",
                kind=ActionKind.ADVANCE_TIME,
                player_label=f"Advance time to {next_clock}",
                canonical_source_id=next_clock,
                source_file=FLOW_FILE,
                time_cost_minutes=15,
                repeat_policy="once",
                destination=next_clock,
                eligibility_reason="clock_advance",
                state_effects={"clock": next_clock},
            )
        )

    loc = state.location_id
    visited = state.ending_chain_state.get("visited_locations", [])
    if loc in visited and (state.ending_chain_state.get("revisit_counts", {}).get(loc, 0) or 0) > 1:
        for rule_set in flow.get("location_revisits", []) or []:
            if rule_set.get("location_id") != loc:
                continue
            for rule in rule_set.get("revisit_rules", []) or []:
                req = set(rule.get("when_knowledge_held", []) or [])
                if req.issubset(state.player_knowledge):
                    actions.append(
                        LegalAction(
                            action_id=f"rev:{rule.get('rule_id')}",
                            kind=ActionKind.REVISIT,
                            player_label=f"Revisit {loc}",
                            canonical_source_id=str(rule.get("rule_id", "")),
                            source_file=FLOW_FILE,
                            time_cost_minutes=1,
                            repeat_policy="once",
                            destination=loc,
                            eligibility_reason="location_revisit",
                            payload=rule,
                        )
                    )

    min_knowledge = 2
    if len(state.player_knowledge) >= min_knowledge or state.flow_flags.get("ready_to_accuse"):
        for q in flow.get("accusation_questionnaire", {}).get("questions", []) or []:
            qid = q.get("question_id", "")
            actions.append(
                LegalAction(
                    action_id=f"acc:{qid}",
                    kind=ActionKind.ACCUSATION,
                    player_label=f"Accuse ({qid})",
                    canonical_source_id=qid,
                    source_file=FLOW_FILE,
                    time_cost_minutes=5,
                    repeat_policy="once",
                    destination=qid,
                    eligibility_reason="accusation_available",
                    payload=q,
                )
            )

    if state.play_mode == "two_player" and state.two_player:
        if not state.two_player.split_active:
            actions.append(
                LegalAction(
                    action_id="tp:split",
                    kind=ActionKind.SPLIT,
                    player_label="Split up to investigate separately",
                    canonical_source_id="split",
                    source_file=FLOW_FILE,
                    time_cost_minutes=0,
                    repeat_policy="once",
                    destination="split",
                    eligibility_reason="two_player_split",
                )
            )
        else:
            actions.append(
                LegalAction(
                    action_id="tp:regroup",
                    kind=ActionKind.REGROUP,
                    player_label="Regroup with partner",
                    canonical_source_id="regroup",
                    source_file=FLOW_FILE,
                    time_cost_minutes=0,
                    repeat_policy="allowed",
                    destination="joint",
                    eligibility_reason="two_player_regroup",
                )
            )

    actions.sort(key=lambda a: a.action_id)
    return actions


def _find_cap_check(cap_pkg: dict, action_id: str) -> dict:
    for chk in cap_pkg.get("checks", []) or []:
        if chk.get("parent_action_id") == action_id:
            return chk
    return {}
