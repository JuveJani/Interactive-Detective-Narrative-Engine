"""Load adventure packages and machine-readable adapters."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class AdventureLoadError(Exception):
    pass


def adventure_root(path: str | Path) -> Path:
    root = Path(path).resolve()
    if not root.exists():
        raise AdventureLoadError(f"Adventure path not found: {root}")
    player = root / "PLAYER"
    if not player.is_dir():
        raise AdventureLoadError(f"Missing PLAYER directory: {player}")
    return root


def load_adapter(root: Path) -> dict[str, Any]:
    for name in ("sim_adapter.json", "SIM_ADAPTER.json"):
        candidate = root / name
        if candidate.exists():
            return json.loads(candidate.read_text(encoding="utf-8"))
    raise AdventureLoadError(
        f"No sim_adapter.json in {root}. Create a machine-readable adapter."
    )


def load_player_text(root: Path) -> dict[str, str]:
    player = root / "PLAYER"
    files = {
        "joint": player / "JOINT_SCENES.md",
        "people": player / "BOOKLET_PEOPLE.md",
        "records": player / "BOOKLET_RECORDS.md",
        "endings": player / "ENDINGS.md",
        "case_file": player / "SHARED" / "CASE_FILE.md",
        "navigation": player / "NAVIGATION_INDEX.md",
    }
    out: dict[str, str] = {}
    for key, path in files.items():
        if path.exists():
            out[key] = path.read_text(encoding="utf-8")
    return out


def load_adventure(path: str | Path) -> dict[str, Any]:
    root = adventure_root(path)
    adapter = load_adapter(root)
    player_text = load_player_text(root)
    logic_dir = root / "DO_NOT_READ" / "LOGIC"
    logic_text: dict[str, str] = {}
    if logic_dir.is_dir():
        for p in sorted(logic_dir.glob("*.md")):
            logic_text[p.name] = p.read_text(encoding="utf-8")
    return {
        "root": root,
        "adapter": adapter,
        "player_text": player_text,
        "logic_text": logic_text,
    }
