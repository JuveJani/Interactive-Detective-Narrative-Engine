"""Load epistemic progression manifests and packages."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from idne.epistemic_progression.model import EpistemicPackage, PlayableEvent


def _read_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    return data if isinstance(data, dict) else None


def load_epistemic_manifest(root: Path) -> dict[str, Any] | None:
    for name in ("epistemic_progression_manifest.json", "EPISTEMIC_PROGRESSION_MANIFEST.json"):
        data = _read_json(root / name)
        if data:
            return data
    gen = _read_json(root / "generation_manifest.json")
    if gen:
        block = gen.get("epistemic_progression")
        if isinstance(block, dict) and block.get("enabled"):
            return {
                "schema_version": gen.get("schema_version", "1.0"),
                "epistemic_progression_method": "canonical",
                "package_path": block.get(
                    "package_path", "DO_NOT_READ/epistemic_progression_package.json"
                ),
            }
    return None


def load_epistemic_package(root: Path, manifest: dict[str, Any] | None = None) -> EpistemicPackage | None:
    if manifest is None:
        manifest = load_epistemic_manifest(root)
    if not manifest:
        return None
    rel = manifest.get("package_path", "DO_NOT_READ/epistemic_progression_package.json")
    raw = _read_json(root / rel)
    if not raw:
        return None
    return parse_epistemic_package(raw)


def parse_epistemic_package(raw: dict[str, Any]) -> EpistemicPackage:
    events: dict[str, PlayableEvent] = {}
    events_by_unit: dict[str, PlayableEvent] = {}
    events_by_location: dict[str, list[PlayableEvent]] = {}
    for item in raw.get("playable_events") or []:
        event = PlayableEvent.from_dict(item)
        if event.event_id:
            events[event.event_id] = event
        if event.unit_id:
            events_by_unit[event.unit_id] = event
        loc = event.physical_location_id or event.location_id
        if loc:
            events_by_location.setdefault(loc, []).append(event)
    return EpistemicPackage(
        schema_version=str(raw.get("schema_version", "1.0")),
        adventure_id=str(raw.get("adventure_id", "")),
        initial_player_knowledge=frozenset(raw.get("initial_player_knowledge") or []),
        initial_world_state=dict(raw.get("initial_world_state") or {}),
        initial_observable_entities=frozenset(raw.get("initial_observable_entities") or []),
        initial_observable_objects=frozenset(raw.get("initial_observable_objects") or []),
        events=events,
        events_by_unit=events_by_unit,
        events_by_location=events_by_location,
    )


def initial_epistemic_state(package: EpistemicPackage) -> "EpistemicState":
    from idne.epistemic_progression.model import EpistemicState

    return EpistemicState(
        player_knowledge=package.initial_player_knowledge,
        world_state=dict(package.initial_world_state),
        interaction_state={"exhausted_actions": [], "completed_topics": []},
        observable_entities=package.initial_observable_entities,
        observable_objects=package.initial_observable_objects,
    )
