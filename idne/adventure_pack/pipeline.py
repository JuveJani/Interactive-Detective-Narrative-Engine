"""Orchestrate full adventure pack build pipeline."""

from __future__ import annotations

import json
import shutil
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from idne.adventure_pack.canonical import write_canonical_packages
from idne.adventure_pack.epistemic import write_epistemic_package
from idne.adventure_pack.player import write_player_files
from idne.adventure_pack.playtime import write_playtime_and_dm_feeling
from idne.adventure_pack.spec import AdventurePackSpec, load_pack_spec, write_json
from idne.gamebook_nav.build import build_gamebook_package
from idne.idne_package import build_idne_package
from idne.validate_adventure.runner import validate_adventure


@dataclass
class BuildResult:
    workspace: Path
    adventure_root: Path
    template_count: int = 0
    materialized_count: int = 0
    public_section_count: int = 0
    gamebook_bytes: int = 0
    generation_seconds: float = 0.0
    validation_seconds: float = 0.0
    validation_status: str = "PENDING"
    validation_detail: dict[str, Any] = field(default_factory=dict)


def _write_brief(spec: AdventurePackSpec, workspace: Path) -> None:
    brief = dict(spec.brief)
    brief.setdefault("player_mode", "single_investigator")
    brief.setdefault("target_playtime_minutes", 120)
    write_json(workspace / "adventure_brief.json", brief)
    (workspace / "brief").mkdir(parents=True, exist_ok=True)
    write_json(workspace / "brief" / "adventure_brief.json", brief)


def _write_generation_state(spec: AdventurePackSpec, workspace: Path) -> None:
    gen_dir = workspace / ".generation"
    gen_dir.mkdir(parents=True, exist_ok=True)
    state = {
        "schema_version": "1.0",
        "adventure_id": spec.pack_id,
        "generation_method": "adventure_pack",
        "stage_status": {s: "COMPLETE" for s in [
            "adventure_brief", "fixed_truth", "causal_timeline", "world_state_timeline",
            "npcs", "environment", "objects", "investigation_core", "npc_conversation",
            "investigation_flow", "capability_checks", "story_player", "playtime",
            "dm_feeling", "final_validation", "package_export",
        ]},
        "status": "COMPLETE",
    }
    write_json(gen_dir / "generation_state.json", state)


def build_adventure_pack(spec_path: str | Path, *, workspace: str | Path | None = None, validate: bool = True) -> BuildResult:
    t0 = time.perf_counter()
    spec = load_pack_spec(spec_path)
    ws = Path(workspace or Path(spec_path).parent).resolve()
    adventure_root = ws / "adventure"
    adventure_root.mkdir(parents=True, exist_ok=True)
    (adventure_root / "DO_NOT_READ").mkdir(parents=True, exist_ok=True)
    (adventure_root / "PLAYER").mkdir(parents=True, exist_ok=True)

    _write_brief(spec, ws)
    write_canonical_packages(spec, adventure_root)
    manifest = write_player_files(spec, adventure_root)
    stats = write_epistemic_package(spec, adventure_root, manifest)
    write_playtime_and_dm_feeling(spec, adventure_root)
    _write_generation_state(spec, ws)

    gb = build_gamebook_package(
        adventure_root,
        adventure_id=spec.pack_id,
        start_unit_id=spec.start_unit_id,
    )
    gamebook_path = adventure_root / "PLAYER" / "GAMEBOOK.md"
    gamebook_bytes = gamebook_path.stat().st_size if gamebook_path.exists() else 0

    pkg_path = ws / f"{spec.pack_id}.idne"
    build_idne_package(adventure_root, pkg_path, spec.pack_id)

    generation_seconds = time.perf_counter() - t0
    result = BuildResult(
        workspace=ws,
        adventure_root=adventure_root,
        template_count=stats.template_count,
        materialized_count=stats.materialized_count,
        public_section_count=len(gb.get("public_sections") or {}),
        gamebook_bytes=gamebook_bytes,
        generation_seconds=generation_seconds,
    )

    if validate:
        tv0 = time.perf_counter()
        vres = validate_adventure(adventure_root)
        result.validation_seconds = time.perf_counter() - tv0
        result.validation_status = vres.status
        result.validation_detail = vres.to_dict()
    return result
