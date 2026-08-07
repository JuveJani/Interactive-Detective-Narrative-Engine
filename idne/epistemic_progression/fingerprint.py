"""Deterministic epistemic state fingerprints for materialized event snapshots."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any

from idne.epistemic_progression.model import EpistemicState

STATE_SUFFIX = "--S-"


@dataclass(frozen=True)
class StateFingerprint:
    player_knowledge: frozenset[str]
    completed_topics: frozenset[str]
    world_state: tuple[tuple[str, Any], ...]

    @classmethod
    def from_state(cls, state: EpistemicState) -> StateFingerprint:
        completed = state.interaction_state.get("completed_topics") or []
        return cls(
            player_knowledge=frozenset(state.player_knowledge),
            completed_topics=frozenset(str(x) for x in completed),
            world_state=tuple(sorted(state.world_state.items())),
        )

    def key(self) -> str:
        payload = {
            "k": sorted(self.player_knowledge),
            "t": sorted(self.completed_topics),
            "w": list(self.world_state),
        }
        digest = hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode()).hexdigest()
        return digest[:10]


def template_unit_id(unit_id: str) -> str:
    if STATE_SUFFIX in unit_id:
        return unit_id.split(STATE_SUFFIX, 1)[0]
    return unit_id


def materialized_unit_id(template_id: str, fp: StateFingerprint, *, initial: StateFingerprint) -> str:
    if fp == initial:
        return template_id
    return f"{template_id}{STATE_SUFFIX}{fp.key()}"


def parse_materialized_unit_id(unit_id: str) -> tuple[str, str | None]:
    if STATE_SUFFIX not in unit_id:
        return unit_id, None
    base, suffix = unit_id.split(STATE_SUFFIX, 1)
    return base, suffix
