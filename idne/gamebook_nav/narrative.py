"""State-aware narrative rendering for materialized delivery units."""

from __future__ import annotations

import re

from idne.epistemic_progression.eligibility import block_eligible
from idne.epistemic_progression.loader import initial_epistemic_state
from idne.epistemic_progression.model import ContentBlock, EpistemicPackage, EpistemicState, PlayableEvent


def state_from_event_snapshot(event: PlayableEvent, package: EpistemicPackage) -> EpistemicState:
    if not event.state_snapshot:
        return initial_epistemic_state(package)
    snap = event.state_snapshot
    return EpistemicState(
        player_knowledge=frozenset(snap.get("player_knowledge") or []),
        world_state=dict(snap.get("world_state") or {}),
        interaction_state={
            "completed_topics": list(snap.get("completed_topics") or []),
            "exhausted_actions": [],
        },
        observable_entities=package.initial_observable_entities,
        observable_objects=package.initial_observable_objects,
    )


def select_content_blocks(event: PlayableEvent, state: EpistemicState) -> list[ContentBlock]:
    eligible: list[ContentBlock] = []
    for block in event.content_blocks:
        ok, _ = block_eligible(block, state)
        if ok:
            eligible.append(block)
    eligible.sort(key=lambda b: (b.presentation_order, b.block_id))
    return eligible


def render_event_body(
    base_body: str,
    event: PlayableEvent,
    package: EpistemicPackage,
) -> str:
    """Compose template prose with eligible state-aware content blocks."""
    if not event.content_blocks:
        return base_body.strip()

    state = state_from_event_snapshot(event, package)
    blocks = select_content_blocks(event, state)
    seen: set[str] = set()
    parts: list[str] = []
    base = base_body.strip()
    if base:
        parts.append(base)
        seen.add(_normalize_text(base))

    for block in blocks:
        text = block.text.strip()
        if not text:
            continue
        norm = _normalize_text(text)
        if norm in seen:
            continue
        seen.add(norm)
        parts.append(text)

    return "\n\n".join(parts)


def _normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())
