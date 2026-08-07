"""Build structured player-facing gamebook JSON from the public delivery graph."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from idne.gamebook_nav.extract import PlayerUnit
from idne.gamebook_nav.graph import UnitNavigation

PLAYER_GAMEBOOK_SCHEMA_VERSION = "1.0"
PLAYER_GAMEBOOK_PATH = "PLAYER/gamebook.json"

# Keys that must never appear in player delivery artifacts.
_FORBIDDEN_KEYS = frozenset(
    {
        "unit_id",
        "template_unit_id",
        "prose_template_unit_id",
        "destination_unit_id",
        "player_knowledge",
        "world_state",
        "state_snapshot",
        "structured_actions",
        "events_by_unit",
        "internal",
        "author_only",
    }
)

_STATE_SUFFIX = re.compile(r"--S-[0-9a-f]{10}$", re.I)
_INTERNAL_UNIT = re.compile(r"^(UNIT|SC|INF|REC|END|CHK)-", re.I)


def _clean_body(unit: PlayerUnit) -> str:
    body = unit.body
    for meta in unit.meta_lines:
        body = body.replace(meta, "")
    return body.strip()


def _choice_label(edge_kind: str, label: str) -> str:
    if edge_kind == "check_success":
        return "If your roll succeeds"
    if edge_kind == "check_failure":
        return "If your roll fails"
    return label


def build_player_gamebook(
    *,
    adventure_id: str,
    adventure_title: str,
    opening: str,
    start_section: int,
    delivery_mode: str,
    player_units: dict[str, PlayerUnit],
    graph: dict[str, UnitNavigation],
    section_map: dict[str, int],
) -> dict[str, Any]:
    """Project the public delivery graph into a player-runtime JSON document."""
    sections: dict[str, dict[str, Any]] = {}
    for uid, unit in player_units.items():
        sec = section_map[uid]
        nav = graph.get(uid)
        meta = [m for m in unit.meta_lines if m.strip()]
        choices: list[dict[str, Any]] = []
        if nav:
            for edge in nav.choices:
                dest_sec = section_map.get(edge.destination_unit_id)
                if dest_sec is None:
                    continue
                choices.append(
                    {
                        "label": _choice_label(edge.edge_kind, edge.label),
                        "target_section": dest_sec,
                        "kind": edge.edge_kind,
                    }
                )
        entry: dict[str, Any] = {
            "section": sec,
            "title": unit.title,
            "body": _clean_body(unit),
            "choices": choices,
        }
        if meta:
            entry["meta"] = meta
        sections[str(sec)] = entry

    return {
        "schema_version": PLAYER_GAMEBOOK_SCHEMA_VERSION,
        "adventure_id": adventure_id,
        "title": adventure_title,
        "delivery_mode": delivery_mode,
        "opening": opening,
        "start_section": start_section,
        "section_count": len(sections),
        "sections": sections,
    }


def write_player_gamebook(path: Path, payload: dict[str, Any]) -> int:
    """Write gamebook.json; return byte size."""
    text = json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return len(text.encode("utf-8"))


def scan_forbidden_player_data(payload: dict[str, Any]) -> list[str]:
    """Return leak findings for keys/patterns that must not reach players."""
    findings: list[str] = []

    def walk(obj: Any, path: str) -> None:
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key in _FORBIDDEN_KEYS:
                    findings.append(f"forbidden key at {path}.{key}")
                walk(value, f"{path}.{key}")
        elif isinstance(obj, list):
            for idx, item in enumerate(obj):
                walk(item, f"{path}[{idx}]")
        elif isinstance(obj, str):
            if "DO_NOT_READ" in obj:
                findings.append(f"author path reference at {path}")
            if _STATE_SUFFIX.search(obj):
                findings.append(f"internal state suffix at {path}")
            if path.endswith(".body") or path.endswith(".label") or path.endswith(".title"):
                if _INTERNAL_UNIT.search(obj) and "--S-" in obj:
                    findings.append(f"internal unit reference at {path}")

    walk(payload, "$")
    return findings
