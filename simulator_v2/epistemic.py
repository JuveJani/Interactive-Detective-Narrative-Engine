"""Epistemic state tracking for Simulator v2."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from idne.epistemic_progression.eligibility import action_eligible, event_enterable, filter_eligible_actions
from idne.epistemic_progression.loader import initial_epistemic_state, load_epistemic_package
from idne.epistemic_progression.model import EpistemicState, StructuredAction
from idne.epistemic_progression.resolve import resolve_playable_unit
from idne.epistemic_progression.signatures import knowledge_signature, world_state_signature


def load_epistemic_for_adventure(adventure_root: str) -> tuple[Any, EpistemicState] | tuple[None, None]:
    from pathlib import Path

    root = Path(adventure_root).resolve()
    package = load_epistemic_package(root)
    if not package:
        return None, None
    return package, initial_epistemic_state(package)


def trace_epistemic_step(
    package,
    state: EpistemicState,
    unit_id: str,
    visible_labels: list[str],
    chosen_label: str | None = None,
) -> dict[str, Any]:
    event = package.events_by_unit.get(unit_id)
    if not event:
        return {
            "epistemic_enabled": False,
            "prerequisite_validation": "SKIP",
        }
    enterable, enter_reason = event_enterable(event, state)
    eligible_actions = filter_eligible_actions(event, state)
    decisions = [
        {
            "action_id": action.action_id,
            "label": action.label,
            "eligible": ok,
            "reason": reason,
        }
        for action, ok, reason in eligible_actions
    ]
    out: dict[str, Any] = {
        "epistemic_enabled": True,
        "internal_event": event.event_id,
        "relevant_knowledge_signature": sorted(knowledge_signature(event, state)),
        "relevant_world_state_signature": world_state_signature(event, state),
        "visible_actions": [a.label for a, ok, _ in eligible_actions if ok],
        "eligibility_decisions": decisions,
        "prerequisite_validation": "PASS" if enterable else f"FAIL:{enter_reason}",
    }
    if chosen_label:
        matched: StructuredAction | None = None
        for action, ok, _ in eligible_actions:
            if action.label == chosen_label and ok:
                matched = action
                break
        if matched:
            out["selected_action"] = matched.action_id
            out["knowledge_delta"] = sorted(matched.knowledge_delta)
            out["world_state_delta"] = matched.world_state_delta
            out["interaction_state_delta"] = matched.interaction_delta
            out["destination_variant"] = matched.destination_unit_id
        else:
            out["selected_action"] = None
            out["epistemic_eligibility_failure"] = True
    return out


def reachable_units_from_start(adventure_root: Path, *, start_unit_id: str = "UNIT-DOCK-BASE") -> set[str]:
    from collections import deque

    package = load_epistemic_package(adventure_root)
    if not package:
        return set()
    from idne.epistemic_progression.eligibility import filter_eligible_actions

    start_event = package.events_by_unit.get(start_unit_id)
    if not start_event:
        return {start_unit_id}
    q: deque[tuple[str, EpistemicState]] = deque([(start_unit_id, initial_epistemic_state(package))])
    reachable = {start_unit_id}
    seen: set[tuple[str, frozenset[str], frozenset[tuple[str, Any]]]] = set()
    while q:
        cur, state = q.popleft()
        event = package.events_by_unit.get(cur)
        if not event:
            continue
        state_key = (cur, state.player_knowledge, frozenset(state.world_state.items()))
        if state_key in seen:
            continue
        seen.add(state_key)
        for action, ok, _ in filter_eligible_actions(event, state):
            if not ok:
                continue
            dest = action.destination_unit_id
            reachable.add(dest)
            q.append((dest, state.apply_action_deltas(action)))
    return reachable


def apply_chosen_action(
    package,
    state: EpistemicState,
    unit_id: str,
    chosen_label: str,
) -> tuple[EpistemicState, StructuredAction | None, str]:
    event = package.events_by_unit.get(unit_id)
    if not event:
        return state, None, "no epistemic event"
    for action, ok, reason in filter_eligible_actions(event, state):
        if action.label == chosen_label:
            if not ok:
                return state, None, reason
            next_state = state.apply_action_deltas(action)
            dest = resolve_playable_unit(package, next_state, action.destination_unit_id)
            next_state.current_unit_id = dest
            return next_state, action, "PASS"
    return state, None, "action not in structured set or ineligible"
