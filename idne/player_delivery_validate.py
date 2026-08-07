"""Validate structured player delivery artifacts."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from idne.gamebook_nav.player_json import (
    PLAYER_GAMEBOOK_PATH,
    scan_forbidden_player_data,
)

_SELF_LOOP_KINDS = frozenset({"return", "scene_continue", "alias"})


@dataclass
class PlayerDeliveryValidationResult:
    adventure_root: Path
    status: str  # PASS | FAIL | SKIP
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    checks: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "adventure_root": str(self.adventure_root),
            "status": self.status,
            "errors": self.errors,
            "warnings": self.warnings,
            "checks": self.checks,
        }


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _mapping_path(root: Path) -> Path | None:
    candidate = root.parent / "player_mapping_manifest.json"
    if candidate.exists():
        return candidate
    nested = root / "player_mapping_manifest.json"
    return nested if nested.exists() else None


def validate_player_gamebook_payload(
    payload: dict[str, Any],
    *,
    manifest: dict[str, Any] | None = None,
    gamebook_text: str | None = None,
) -> PlayerDeliveryValidationResult:
    """Validate an in-memory player gamebook document."""
    result = PlayerDeliveryValidationResult(adventure_root=Path("."), status="PASS")

    if payload.get("schema_version") != "1.0":
        result.errors.append("unsupported or missing schema_version")
        result.checks["PD-SCHEMA"] = "FAIL"
    else:
        result.checks["PD-SCHEMA"] = "PASS"

    sections = payload.get("sections") or {}
    if not sections:
        result.errors.append("no sections in player gamebook")
        result.checks["PD-SECTIONS"] = "FAIL"
    else:
        result.checks["PD-SECTIONS"] = "PASS"

    nums = [entry.get("section") for entry in sections.values()]
    if len(nums) != len(set(nums)):
        result.errors.append("duplicate public section numbers in player gamebook")
        result.checks["PD-UNIQUE"] = "FAIL"
    else:
        result.checks["PD-UNIQUE"] = "PASS"

    start = payload.get("start_section")
    if start is None or str(start) not in sections:
        result.errors.append("starting section missing from player gamebook")
        result.checks["PD-START"] = "FAIL"
    else:
        result.checks["PD-START"] = "PASS"

    dangling: list[str] = []
    self_loops: list[str] = []
    self_loop_warnings: list[str] = []
    for sec_key, entry in sections.items():
        for choice in entry.get("choices") or []:
            target = choice.get("target_section")
            if target is None or str(target) not in sections:
                dangling.append(f"{sec_key}->{target}")
            elif int(sec_key) == int(target):
                label = f"{sec_key}:{choice.get('label', '')[:40]}"
                kind = choice.get("kind")
                if kind in _SELF_LOOP_KINDS:
                    continue
                if kind == "scene_variant":
                    self_loop_warnings.append(label)
                else:
                    self_loops.append(label)

    if dangling:
        result.errors.append(f"dangling choice targets: {dangling[:5]}")
        result.checks["PD-TARGETS"] = "FAIL"
    else:
        result.checks["PD-TARGETS"] = "PASS"

    if self_loops:
        result.errors.append(f"unexpected exact self-loops: {self_loops[:5]}")
        result.checks["PD-SELF-LOOP"] = "FAIL"
    elif self_loop_warnings:
        result.warnings.append(f"scene-variant self-loops: {self_loop_warnings[:5]}")
        result.checks["PD-SELF-LOOP"] = "WARN"
    else:
        result.checks["PD-SELF-LOOP"] = "PASS"

    leaks = scan_forbidden_player_data(payload)
    if leaks:
        result.errors.extend(leaks[:10])
        result.checks["PD-LEAK"] = "FAIL"
    else:
        result.checks["PD-LEAK"] = "PASS"

    if manifest:
        manifest_sections = manifest.get("public_sections") or {}
        expected = {str(v) for v in manifest_sections.values()}
        actual = set(sections.keys())
        if expected != actual:
            missing = sorted(expected - actual)[:5]
            extra = sorted(actual - expected)[:5]
            result.errors.append(
                f"player gamebook sections differ from manifest: missing={missing} extra={extra}"
            )
            result.checks["PD-MANIFEST-PARITY"] = "FAIL"
        else:
            result.checks["PD-MANIFEST-PARITY"] = "PASS"

    if gamebook_text and manifest:
        section_map = manifest.get("public_sections") or {}
        rev = {v: k for k, v in section_map.items()}
        mismatches: list[str] = []
        for sec_key, entry in sections.items():
            sec = int(sec_key)
            if f"## Section {sec}" not in gamebook_text:
                mismatches.append(f"missing markdown section {sec}")
                continue
            uid = rev.get(sec)
            if not uid:
                continue
            unit_entry = (manifest.get("units") or {}).get(uid, {})
            for choice in entry.get("choices") or []:
                label = choice.get("label", "")
                target = choice.get("target_section")
                if label and f"Turn to section" in gamebook_text:
                    needle = f"Turn to section [**{target}**](#section-{target})"
                    if needle not in gamebook_text and str(sec) in gamebook_text:
                        # check_success/failure use different prose
                        if choice.get("kind") not in {"check_success", "check_failure"}:
                            mismatches.append(f"section {sec} choice target {target}")
        if mismatches:
            result.warnings.append(f"gamebook markdown parity warnings: {mismatches[:3]}")
            result.checks["PD-GAMEBOOK-PARITY"] = "WARN"
        else:
            result.checks["PD-GAMEBOOK-PARITY"] = "PASS"

    if result.errors:
        result.status = "FAIL"
    return result


def validate_player_delivery(adventure_root: str | Path) -> PlayerDeliveryValidationResult:
    """Validate PLAYER/gamebook.json for an adventure workspace."""
    root = Path(adventure_root).resolve()
    result = PlayerDeliveryValidationResult(adventure_root=root, status="PASS")

    mapping_path = _mapping_path(root)
    if not mapping_path:
        result.status = "SKIP"
        result.warnings.append("no player_mapping_manifest — player delivery skipped")
        return result

    manifest = _load_json(mapping_path)
    static = manifest.get("static_book") or {}
    if not static.get("gamebook_path") and not static.get("delivery_mode"):
        result.status = "SKIP"
        result.warnings.append("static_book not declared")
        return result

    gamebook_json_path = root / PLAYER_GAMEBOOK_PATH
    if not gamebook_json_path.exists():
        result.status = "FAIL"
        result.errors.append(f"missing {PLAYER_GAMEBOOK_PATH}")
        result.checks["PD-PRESENT"] = "FAIL"
        return result

    result.checks["PD-PRESENT"] = "PASS"
    payload = _load_json(gamebook_json_path)

    gamebook_rel = static.get("gamebook_path", "PLAYER/GAMEBOOK.md")
    gamebook_md_path = root / gamebook_rel
    gamebook_text = gamebook_md_path.read_text(encoding="utf-8") if gamebook_md_path.exists() else None

    inner = validate_player_gamebook_payload(
        payload,
        manifest=manifest,
        gamebook_text=gamebook_text,
    )
    result.errors = inner.errors
    result.warnings = inner.warnings
    result.checks.update(inner.checks)
    result.status = inner.status
    return result


def validate_player_gamebook_determinism(
    first: dict[str, Any],
    second: dict[str, Any],
) -> PlayerDeliveryValidationResult:
    """Ensure two builds produce identical player payloads."""
    result = PlayerDeliveryValidationResult(adventure_root=Path("."), status="PASS")
    if first != second:
        result.errors.append("player gamebook build is not deterministic")
        result.checks["PD-DETERMINISTIC"] = "FAIL"
        result.status = "FAIL"
    else:
        result.checks["PD-DETERMINISTIC"] = "PASS"
    return result
