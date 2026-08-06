"""Run all applicable validators and aggregate results."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

from idne.epistemic_progression_validate import validate_epistemic_progression
from idne.capability_check_validate import validate_capability_check
from idne.dm_feeling_validate import validate_dm_feeling
from idne.environment_validate import validate_environment
from idne.investigation_core_validate import validate_investigation_core
from idne.investigation_flow_validate import validate_investigation_flow
from idne.investigation_validate import validate_investigation
from idne.npc_investigation_validate import validate_npc_investigation
from idne.object_interaction_validate import validate_object_interaction
from idne.play_modes import PLAY_MODE_SINGLE, normalize_play_modes
from idne.playtime_validate import validate_playtime
from idne.single_investigator_validate import load_play_manifest, validate_single_investigator
from idne.story_validate import validate_story
from idne.gamebook_validate import validate_gamebook, requires_static_gamebook
from idne.world_first_validate import load_generation_manifest, validate_world_first


ValidatorFn = Callable[[Path], Any]


@dataclass
class IntegratedValidationResult:
    adventure_root: Path
    status: str  # PASS | FAIL | BLOCKED | CONDITIONAL_PASS | SKIP
    validators: dict[str, dict[str, Any]] = field(default_factory=dict)
    tier_b_pending: list[str] = field(default_factory=list)
    tier_c_complete: bool = False
    mandatory_failures: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "adventure_root": str(self.adventure_root),
            "status": self.status,
            "validators": self.validators,
            "tier_b_pending": self.tier_b_pending,
            "tier_c_complete": self.tier_c_complete,
            "mandatory_failures": self.mandatory_failures,
            "warnings": self.warnings,
        }


def _entry(name: str, res: Any) -> dict[str, Any]:
    status = getattr(res, "status", "FAIL")
    tier_b = list(getattr(res, "tier_b_pending", []) or [])
    tier_c = bool(getattr(res, "tier_c_complete", False))
    return {
        "status": status,
        "tier_b_pending": tier_b,
        "tier_c_complete": tier_c,
        "checks": dict(getattr(res, "checks", {}) or {}),
        "warnings": list(getattr(res, "warnings", []) or []),
        "findings_count": len(getattr(res, "findings", []) or []),
        "errors_count": len(getattr(res, "errors", []) or []),
    }


def _read_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    return data if isinstance(data, dict) else None


def _solo_mode_required(root: Path) -> bool:
    manifest = load_play_manifest(root)
    if manifest:
        try:
            modes = normalize_play_modes(manifest.get("play_modes"))
            if PLAY_MODE_SINGLE in modes:
                return True
        except ValueError:
            pass

    for candidate in (
        root.parent / "brief" / "adventure_brief.json",
        root.parent / "adventure_brief.json",
    ):
        brief = _read_json(candidate)
        if brief and str(brief.get("player_mode", "")) == PLAY_MODE_SINGLE:
            return True

    story = _read_json(root / "DO_NOT_READ" / "story_validator_package.json")
    if story:
        modes = story.get("play_modes")
        if isinstance(modes, list) and PLAY_MODE_SINGLE in modes:
            return True
    return False


def _is_canonical_adventure(root: Path) -> bool:
    gen = load_generation_manifest(root)
    if gen and gen.get("generation_method") == "world_first":
        return True
    markers = (
        "investigation_validator_manifest.json",
        "story_validator_manifest.json",
        "environment_manifest.json",
        "generation_manifest.json",
    )
    return any((root / m).exists() for m in markers)


def validate_adventure(adventure_root: str | Path) -> IntegratedValidationResult:
    root = Path(adventure_root).resolve()
    result = IntegratedValidationResult(adventure_root=root, status="PASS")

    canonical = _is_canonical_adventure(root)
    if not canonical:
        result.status = "SKIP"
        result.warnings.append(
            "legacy or undeclared adventure — validators skipped; not reporting PASS"
        )
        result.validators["legacy"] = {"status": "SKIP", "reason": "no canonical manifests"}
        return result

    solo_required = _solo_mode_required(root)

    validators: list[tuple[str, ValidatorFn, bool]] = [
        ("single_investigator", validate_single_investigator, solo_required),
        ("world_first", validate_world_first, True),
        ("environment", validate_environment, True),
        ("object_interaction", validate_object_interaction, True),
        ("investigation_core", validate_investigation_core, True),
        ("npc_investigation", validate_npc_investigation, True),
        ("investigation_flow", validate_investigation_flow, True),
        ("epistemic_progression", validate_epistemic_progression, True),
        ("capability_check", validate_capability_check, True),
        ("investigation", validate_investigation, True),
        ("story", validate_story, True),
        ("playtime", validate_playtime, True),
        ("dm_feeling", validate_dm_feeling, True),
    ]

    if requires_static_gamebook(root):
        validators.append(("gamebook", validate_gamebook, True))

    play_manifest = load_play_manifest(root)
    solo_declared = False
    if play_manifest:
        try:
            modes = normalize_play_modes(play_manifest.get("play_modes"))
            solo_declared = PLAY_MODE_SINGLE in modes
        except ValueError:
            solo_declared = False

    applicable_statuses: list[str] = []
    for name, fn, mandatory_when_applicable in validators:
        if name == "single_investigator":
            if not solo_required:
                result.validators[name] = {
                    "status": "SKIP",
                    "reason": "single_investigator not declared",
                }
                continue
            if not solo_declared:
                result.validators[name] = {
                    "status": "FAIL",
                    "tier_b_pending": [],
                    "tier_c_complete": False,
                    "checks": {"QA-SI-MANIFEST": "FAIL"},
                    "warnings": [],
                    "findings_count": 0,
                    "errors_count": 1,
                    "errors": [
                        "single_investigator required by brief/story package but play_manifest.json missing or incomplete"
                    ],
                }
                applicable_statuses.append("FAIL")
                if mandatory_when_applicable:
                    result.mandatory_failures.append(name)
                continue

        res = fn(root)
        entry = _entry(name, res)
        result.validators[name] = entry

        status = entry["status"]
        if status == "SKIP":
            continue

        applicable_statuses.append(status)
        result.tier_b_pending.extend(entry["tier_b_pending"])
        if entry["tier_c_complete"]:
            result.tier_c_complete = True

        if mandatory_when_applicable and status in ("FAIL", "BLOCKED"):
            result.mandatory_failures.append(name)

    if result.mandatory_failures:
        if any(
            result.validators[n].get("status") == "BLOCKED"
            for n in result.mandatory_failures
        ):
            result.status = "BLOCKED"
        else:
            result.status = "FAIL"
    elif not applicable_statuses:
        result.status = "SKIP"
        result.warnings.append("no applicable validators ran")
    elif any(s == "CONDITIONAL_PASS" for s in applicable_statuses):
        result.status = "CONDITIONAL_PASS"
    else:
        result.status = "PASS"

    result.tier_b_pending = sorted(set(result.tier_b_pending))
    return result


def write_validator_reports(adventure_root: Path, result: IntegratedValidationResult) -> dict[str, str]:
    root = Path(adventure_root).resolve()
    reports = root / ".generation" / "reports"
    reports.mkdir(parents=True, exist_ok=True)

    summary_lines = [
        "# Validator Summary",
        "",
        f"Overall status: **{result.status}**",
        "",
        "| Validator | Status |",
        "|---|---|",
    ]
    for name, entry in result.validators.items():
        summary_lines.append(f"| {name} | {entry.get('status', '')} |")

    if result.tier_b_pending:
        summary_lines.extend(["", "## Tier B pending", "", *[f"- {t}" for t in result.tier_b_pending]])
    summary_lines.extend(
        [
            "",
            f"Tier C complete: {result.tier_c_complete}",
            "",
        ]
    )
    if result.mandatory_failures:
        summary_lines.extend(["## Mandatory failures", "", *[f"- {n}" for n in result.mandatory_failures]])

    summary_path = reports / "validator_summary.md"
    summary_path.write_text("\n".join(summary_lines), encoding="utf-8")

    unresolved = {
        "status": result.status,
        "mandatory_failures": result.mandatory_failures,
        "tier_b_pending": result.tier_b_pending,
        "tier_c_complete": result.tier_c_complete,
    }
    unresolved_path = reports / "unresolved_findings.json"
    unresolved_path.write_text(json.dumps(unresolved, indent=2), encoding="utf-8")

    return {
        "validator_summary.md": str(summary_path),
        "unresolved_findings.json": str(unresolved_path),
    }
