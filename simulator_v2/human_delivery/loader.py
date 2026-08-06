"""Load unpacked adventure workspaces for human-delivery simulation."""

from __future__ import annotations

import json
from pathlib import Path

from simulator_v2.human_delivery.types import AdventureWorkspace


class HumanDeliveryLoadError(Exception):
    pass


def _read_json(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        raise HumanDeliveryLoadError(f"invalid json: {path}") from exc
    if not isinstance(data, dict):
        raise HumanDeliveryLoadError(f"expected object json: {path}")
    return data


def resolve_adventure_workspace(path: str | Path) -> AdventureWorkspace:
    """Resolve an unpacked adventure workspace; never silently fall back to .idne."""
    source = Path(path).resolve()
    if source.suffix.lower() == ".idne" and source.is_file():
        raise HumanDeliveryLoadError(
            "human-delivery simulation requires an unpacked adventure directory, not a .idne archive"
        )

    workspace_root: Path | None = None
    adventure_root: Path | None = None

    if (source / "player_mapping_manifest.json").exists() and (source / "adventure").is_dir():
        workspace_root = source
        adventure_root = source / "adventure"
    elif source.name == "adventure" and (source.parent / "player_mapping_manifest.json").exists():
        workspace_root = source.parent
        adventure_root = source
    elif (source / "generation_manifest.json").exists() or (source / "play_manifest.json").exists():
        workspace_root = source.parent if (source.parent / "player_mapping_manifest.json").exists() else source
        adventure_root = source
        if not (workspace_root / "player_mapping_manifest.json").exists():
            manifest_candidate = source.parent / "player_mapping_manifest.json"
            if manifest_candidate.exists():
                workspace_root = source.parent
    else:
        raise HumanDeliveryLoadError(f"not an unpacked adventure workspace: {source}")

    manifest_path = workspace_root / "player_mapping_manifest.json"
    if not manifest_path.exists():
        raise HumanDeliveryLoadError(f"missing player_mapping_manifest.json under {workspace_root}")

    manifest = _read_json(manifest_path)
    static = manifest.get("static_book") or {}
    gamebook_rel = static.get("gamebook_path", "PLAYER/GAMEBOOK.md")
    gamebook_path = adventure_root / gamebook_rel
    if not gamebook_path.exists():
        raise HumanDeliveryLoadError(f"missing gamebook file: {gamebook_path}")

    idne_candidates = list(workspace_root.glob("*.idne"))
    used_idne = False
    if idne_candidates and source.is_dir():
        used_idne = False  # explicit unpacked directory takes precedence

    return AdventureWorkspace(
        workspace_root=workspace_root,
        adventure_root=adventure_root,
        manifest_path=manifest_path,
        gamebook_path=gamebook_path,
        manifest=manifest,
        used_idne=used_idne,
    )
