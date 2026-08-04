"""Adventure brief parsing and validation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REQUIRED_BRIEF_FIELDS = (
    "universe",
    "genre",
    "realism_level",
    "player_mode",
    "investigator_character",
    "target_playtime_minutes",
    "in_world_duration",
    "tone",
    "difficulty",
    "location_scale",
    "content_boundaries",
)


def load_brief(path: Path) -> dict[str, Any]:
    path = path.resolve()
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        data = json.loads(text)
    else:
        data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError("brief must be a JSON object")
    return data


def validate_brief(brief: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for field in REQUIRED_BRIEF_FIELDS:
        if field not in brief:
            errors.append(f"missing brief field: {field}")
    mode = brief.get("player_mode")
    if mode not in ("single_investigator", "two_player"):
        errors.append("player_mode must be single_investigator or two_player")
    try:
        minutes = int(brief.get("target_playtime_minutes", 0))
        if minutes <= 0:
            errors.append("target_playtime_minutes must be positive")
    except (TypeError, ValueError):
        errors.append("target_playtime_minutes must be an integer")
    return errors


def brief_play_mode(brief: dict[str, Any]) -> str:
    return str(brief.get("player_mode", "single_investigator"))
