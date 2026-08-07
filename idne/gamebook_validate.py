"""Integrated gamebook navigation validator entry point."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from idne.gamebook_nav.validate import GamebookValidationResult, validate_gamebook_navigation


@dataclass
class ValidationResult:
    adventure_root: Path
    status: str
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    checks: dict[str, str] = field(default_factory=dict)
    findings: list[Any] = field(default_factory=list)
    tier_b_pending: list[str] = field(default_factory=list)
    tier_c_complete: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "adventure_root": str(self.adventure_root),
            "status": self.status,
            "errors": self.errors,
            "warnings": self.warnings,
            "checks": self.checks,
            "findings": self.findings,
            "tier_b_pending": self.tier_b_pending,
            "tier_c_complete": self.tier_c_complete,
        }


def _mapping_path(root: Path) -> Path | None:
    candidate = root.parent / "player_mapping_manifest.json"
    if candidate.exists():
        return candidate
    nested = root / "player_mapping_manifest.json"
    return nested if nested.exists() else None


def requires_static_gamebook(root: Path) -> bool:
    """True when an adventure declares static-book delivery via its mapping manifest."""
    path = _mapping_path(root)
    if not path:
        return False
    data = json.loads(path.read_text(encoding="utf-8"))
    static = data.get("static_book") or {}
    return bool(static.get("delivery_mode") == "static_book" or static.get("gamebook_path"))


def validate_gamebook(adventure_root: str | Path) -> ValidationResult:
    root = Path(adventure_root).resolve()
    out = ValidationResult(adventure_root=root, status="PASS")

    play_manifest = root / "play_manifest.json"
    if not play_manifest.exists():
        out.status = "SKIP"
        out.warnings.append("no play_manifest — gamebook validation skipped")
        return out

    mapping_path = _mapping_path(root)
    if not mapping_path:
        out.status = "SKIP"
        out.warnings.append("no player_mapping_manifest — gamebook validation skipped")
        return out

    manifest = json.loads(mapping_path.read_text(encoding="utf-8"))
    if not requires_static_gamebook(root):
        out.status = "SKIP"
        out.warnings.append("static_book not declared in player_mapping_manifest")
        out.checks["GB-DECLARED"] = "SKIP"
        return out

    out.checks["GB-DECLARED"] = "PASS"
    gamebook_rel = manifest.get("static_book", {}).get("gamebook_path", "PLAYER/GAMEBOOK.md")
    gamebook_path = root / gamebook_rel
    if not gamebook_path.exists():
        out.status = "FAIL"
        out.errors.append(f"static book not built — missing {gamebook_rel}")
        out.checks["GB-PRESENT"] = "FAIL"
        return out

    out.checks["GB-PRESENT"] = "PASS"
    gamebook_text = gamebook_path.read_text(encoding="utf-8")

    player_units = None
    graph = None
    section_map = manifest.get("public_sections")
    delivery_mode = (manifest.get("static_book") or {}).get("delivery_mode")
    if delivery_mode == "materialized_static_book":
        from idne.gamebook_nav.delivery import load_materialized_delivery
        from idne.gamebook_nav.extract import parse_player_units

        template_units = parse_player_units(root / "PLAYER", None)
        _, player_units, graph, _ = load_materialized_delivery(
            root,
            template_units,
            manifest_units=manifest.get("units") or {},
        )

    res: GamebookValidationResult = validate_gamebook_navigation(
        root,
        manifest=manifest,
        player_units=player_units,
        graph=graph,
        section_map=section_map,
        gamebook_text=gamebook_text,
    )
    out.checks.update(res.checks)
    out.errors = list(res.errors)
    out.warnings = list(res.warnings)
    out.status = res.status if res.status != "SKIP" else "FAIL"
    if out.status == "FAIL":
        for err in out.errors[:10]:
            out.findings.append({"finding_id": "GB-NAV", "message": err})
    return out
