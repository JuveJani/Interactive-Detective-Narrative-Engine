"""Evaluate investigation endings from player-visible epistemic state."""

from __future__ import annotations

from typing import Any


def evaluate_ending(
    flow_pkg: dict[str, Any],
    *,
    player_knowledge: set[str] | frozenset[str],
    world_state: dict[str, Any],
    accusation_answers: dict[str, str] | None = None,
    clock_id: str | None = None,
) -> str | None:
    """Return highest-priority ending id matching current state, or None."""
    accusation_answers = accusation_answers or {}
    order = (flow_pkg.get("ending_graph") or {}).get("evaluation_order") or []
    endings = {e["ending_id"]: e for e in flow_pkg.get("endings", []) or [] if e.get("ending_id")}
    if not order:
        order = list(endings.keys())

    deadline = (flow_pkg.get("deadline") or {}).get("deadline_clock")
    if clock_id and deadline and clock_id == deadline:
        timeout_id = (flow_pkg.get("deadline") or {}).get("deadline_ending_id", "END-TIMEOUT")
        if timeout_id in endings:
            return timeout_id

    for eid in order:
        ending = endings.get(eid)
        if not ending:
            continue
        trigger = ending.get("trigger") or {}
        ttype = trigger.get("type", "")
        if ttype == "deadline_expired":
            if clock_id and deadline and clock_id == deadline:
                return eid
            continue
        if ttype != "state_driven":
            continue
        req_k = set(trigger.get("required_knowledge_ids") or [])
        if req_k and not req_k.issubset(player_knowledge):
            continue
        req_state = trigger.get("required_state") or {}
        if any(world_state.get(k) != v for k, v in req_state.items()):
            continue
        req_acc = trigger.get("required_accusation") or {}
        if req_acc and not all(accusation_answers.get(k) == v for k, v in req_acc.items()):
            continue
        min_count = trigger.get("min_knowledge_count")
        if min_count is not None and len(player_knowledge) < int(min_count):
            continue
        return eid
    return None


def ending_prerequisites_met(
    ending: dict[str, Any],
    *,
    player_knowledge: set[str] | frozenset[str],
    world_state: dict[str, Any],
) -> bool:
    trigger = ending.get("trigger") or {}
    if trigger.get("type") != "state_driven":
        return False
    req_k = set(trigger.get("required_knowledge_ids") or [])
    if req_k and not req_k.issubset(player_knowledge):
        return False
    req_state = trigger.get("required_state") or {}
    if any(world_state.get(k) != v for k, v in req_state.items()):
        return False
    min_count = trigger.get("min_knowledge_count")
    if min_count is not None and len(player_knowledge) < int(min_count):
        return False
    return True


def ending_submit_actions(flow_pkg: dict[str, Any]) -> list[dict[str, Any]]:
    """Gated submit actions for accusation prep; only endings with state_driven triggers."""
    actions: list[dict[str, Any]] = []
    labels = {
        "END-PERFECT": "Submit your full supported accountability statement.",
        "END-PARTIAL-TECH-ONLY": "Submit a technical mechanism statement without naming personnel.",
        "END-PARTIAL-MOTIVE-GAP": "Submit receiving discrepancy findings without full relabel synthesis.",
        "END-PARTIAL-WRONG-CULPRIT": "Submit a statement centering on the contractor exit record.",
        "END-PARTIAL-INCOMPLETE": "Submit the best statement you can with incomplete proof.",
        "END-HIDDEN-RECORDS": "Close the case using the records-only archive route.",
        "END-NARRATIVE-CONTINUE": "Defer final accountability and continue investigating.",
    }
    for ending in flow_pkg.get("endings") or []:
        eid = ending.get("ending_id", "")
        if eid == "END-TIMEOUT":
            continue
        trigger = ending.get("trigger") or {}
        if trigger.get("type") != "state_driven":
            continue
        req_k = list(trigger.get("required_knowledge_ids") or [])
        req_state = dict(trigger.get("required_state") or {})
        actions.append(
            {
                "action_id": f"ACT-SUBMIT-{eid}",
                "action_type": "ending_submit",
                "label": labels.get(eid, f"Submit investigation outcome ({eid})."),
                "destination_unit_id": eid,
                "requires_knowledge_ids": req_k,
                "requires_world_state": req_state,
                "world_state_delta": {"accusation_complete": True},
                "investigative": True,
                "purpose": "accusation submission",
            }
        )
    actions.append(
        {
            "action_id": "ACT-ACCUSATION-CONTINUE",
            "action_type": "return",
            "label": "Return to the location base section for this area.",
            "destination_unit_id": "UNIT-DOCK-BASE",
            "investigative": False,
        }
    )
    return actions
