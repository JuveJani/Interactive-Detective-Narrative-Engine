"""Resolve playable unit destinations against epistemic state variants."""

from __future__ import annotations

from typing import Any

from idne.epistemic_progression.eligibility import event_enterable
from idne.epistemic_progression.model import EpistemicPackage, EpistemicState, PlayableEvent


def _variant_candidates(package: EpistemicPackage, base_unit_id: str) -> list[PlayableEvent]:
    base = package.events_by_unit.get(base_unit_id)
    if not base:
        return []
    out = [base]
    for event in package.events.values():
        if event.unit_id == base_unit_id:
            continue
        if event.variant_of == base_unit_id or event.supersedes_unit_id == base_unit_id:
            out.append(event)
    return out


def _specificity(event: PlayableEvent) -> tuple[int, int, int]:
    return (
        len(event.required_knowledge_ids),
        len(event.required_world_state),
        1 if event.supersedes_unit_id else 0,
    )


def resolve_playable_unit(
    package: EpistemicPackage,
    state: EpistemicState,
    dest_unit_id: str,
) -> str:
    """Return the most specific enterable variant for a destination unit id."""
    candidates = _variant_candidates(package, dest_unit_id)
    if len(candidates) <= 1:
        event = package.events_by_unit.get(dest_unit_id)
        if event:
            ok, _ = event_enterable(event, state)
            if ok:
                return dest_unit_id
        return dest_unit_id

    enterable = [e for e in candidates if event_enterable(e, state)[0]]
    if not enterable:
        return dest_unit_id

    best = max(enterable, key=_specificity)
    return best.unit_id


def best_enterable_variant_for_knowledge(
    package: EpistemicPackage,
    state: EpistemicState,
    base_unit_id: str,
    *,
    knowledge_delta: frozenset[str] | set[str],
) -> str | None:
    """After applying knowledge_delta, return a superseding variant if one should be used."""
    probe = state.copy()
    probe.player_knowledge = frozenset(set(probe.player_knowledge) | set(knowledge_delta))
    resolved = resolve_playable_unit(package, probe, base_unit_id)
    if resolved != base_unit_id:
        return resolved
    base = package.events_by_unit.get(base_unit_id)
    if not base:
        return None
    gained = set(knowledge_delta)
    if not gained:
        return None
    deps = base.relevant_knowledge_dependencies
    if deps and gained.intersection(deps):
        for event in package.events.values():
            if event.variant_of != base_unit_id and event.supersedes_unit_id != base_unit_id:
                continue
            if event.required_knowledge_ids and event.required_knowledge_ids <= probe.player_knowledge:
                if event_enterable(event, probe)[0]:
                    return event.unit_id
    return None
