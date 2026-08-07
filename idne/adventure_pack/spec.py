"""Load and validate adventure pack specifications."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class AdventurePackSpec:
    raw: dict[str, Any]
    pack_id: str
    brief: dict[str, Any]
    fixed_truth: dict[str, Any]
    locations: list[dict[str, Any]]
    npcs: list[dict[str, Any]]
    objects: list[dict[str, Any]]
    knowledge: dict[str, Any]
    player_units: dict[str, Any]
    navigation: list[dict[str, Any]]
    flow: dict[str, Any]
    conversations: list[dict[str, Any]]
    object_actions: list[dict[str, Any]]
    checks: list[dict[str, Any]]
    epistemic: dict[str, Any]
    gamebook: dict[str, Any]
    validator_seeds: dict[str, Any]

    @property
    def units(self) -> list[dict[str, Any]]:
        return list(self.player_units.get("units") or [])

    @property
    def unit_by_id(self) -> dict[str, dict[str, Any]]:
        return {u["unit_id"]: u for u in self.units if u.get("unit_id")}

    @property
    def start_unit_id(self) -> str:
        return str(
            self.epistemic.get("start_template_unit_id")
            or self.gamebook.get("start_template_unit_id")
            or "UNIT-START-BASE"
        )

    @property
    def start_location_id(self) -> str:
        for loc in self.locations:
            if loc.get("start_location"):
                return str(loc["location_id"])
        return str(self.locations[0]["location_id"]) if self.locations else "LOC-START"


def load_pack_spec(path: str | Path) -> AdventurePackSpec:
    path = Path(path).resolve()
    raw = json.loads(path.read_text(encoding="utf-8"))
    pack_id = str(raw.get("pack_id") or raw.get("adventure_id") or path.parent.name)
    return AdventurePackSpec(
        raw=raw,
        pack_id=pack_id,
        brief=dict(raw.get("brief") or {}),
        fixed_truth=dict(raw.get("fixed_truth") or {}),
        locations=list(raw.get("locations") or []),
        npcs=list(raw.get("npcs") or []),
        objects=list(raw.get("objects") or []),
        knowledge=dict(raw.get("knowledge") or {}),
        player_units=dict(raw.get("player_units") or {}),
        navigation=list(raw.get("navigation") or []),
        flow=dict(raw.get("flow") or {}),
        conversations=list(raw.get("conversations") or []),
        object_actions=list(raw.get("object_actions") or []),
        checks=list(raw.get("checks") or []),
        epistemic=dict(raw.get("epistemic") or {}),
        gamebook=dict(raw.get("gamebook") or {}),
        validator_seeds=dict(raw.get("validator_seeds") or {}),
    )


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
