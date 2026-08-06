"""Validate parsed model responses."""

from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from idne.generate.brief import validate_brief
from idne.local_ai.run_state import write_json
from idne.local_ai.task_model import ProcessingStage, transition_processing_stage

RESPONSE_SCHEMA_REF = "idne/schemas/local_ai_adventure_brief_response.schema.json"
REQUIRED_FIELDS = (
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
    "premise",
    "opening_situation",
)
OPTIONAL_FIELDS = (
    "working_title",
    "setting",
    "initial_observable_facts",
    "required_themes",
    "forbidden_themes",
    "author_notes",
)
ALLOWED_FIELDS = frozenset(REQUIRED_FIELDS + OPTIONAL_FIELDS)
PROTECTED_FIELD_NAMES = frozenset(
    {
        "task_id",
        "adventure_id",
        "schema_version",
        "created_at",
        "updated_at",
        "timestamp",
        "file_path",
        "filename",
        "hash",
        "sha256",
        "validator_status",
        "approval_status",
        "manifest",
        "public_section",
        "internal_id",
        "stage_status",
        "output_path",
        "run_directory",
    }
)
COLD_STORAGE_MARKERS = (
    "cold storage alarm",
    "elena",
    "dock worker",
    "636",
    "the_cold_storage_alarm",
)
AUTHOR_ONLY_PATTERNS = (
    r"\bculprit\b",
    r"\bmotive\b",
    r"\bmethod\b",
    r"\bwho did it\b",
    r"\bsolution is\b",
)


@dataclass
class ValidationFinding:
    path: str
    code: str
    message: str
    severity: str = "error"

    def to_dict(self) -> dict[str, str]:
        return {"path": self.path, "code": self.code, "message": self.message, "severity": self.severity}


@dataclass
class ResponseValidationResult:
    passed: bool
    findings: list[ValidationFinding] = field(default_factory=list)
    protected_findings: list[ValidationFinding] = field(default_factory=list)
    warnings: list[ValidationFinding] = field(default_factory=list)
    duration_seconds: float = 0.0

    def to_report(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "findings": [f.to_dict() for f in self.findings],
            "protected_value_report": [f.to_dict() for f in self.protected_findings],
            "warnings": [f.to_dict() for f in self.warnings],
            "duration_seconds": self.duration_seconds,
        }


class ResponseValidationError(RuntimeError):
    pass


def _non_empty_string(value: Any, path: str, findings: list[ValidationFinding]) -> bool:
    if not isinstance(value, str) or not value.strip():
        findings.append(ValidationFinding(path, "empty_value", f"{path} must be a non-empty string"))
        return False
    return True


def validate_response_schema(data: dict[str, Any]) -> list[ValidationFinding]:
    findings: list[ValidationFinding] = []
    unexpected = sorted(set(data.keys()) - ALLOWED_FIELDS)
    for key in unexpected:
        findings.append(ValidationFinding(key, "unexpected_field", f"unexpected field: {key}"))
    for key in REQUIRED_FIELDS:
        if key not in data:
            findings.append(ValidationFinding(key, "missing_field", f"missing required field: {key}"))
    if "player_mode" in data and data["player_mode"] not in ("single_investigator", "two_player"):
        findings.append(ValidationFinding("player_mode", "invalid_enum", "invalid player_mode"))
    minutes = data.get("target_playtime_minutes")
    if not isinstance(minutes, int) or minutes <= 0:
        findings.append(ValidationFinding("target_playtime_minutes", "wrong_type", "must be positive integer"))
    for key in REQUIRED_FIELDS:
        if key in data and isinstance(data[key], str):
            _non_empty_string(data[key], key, findings)
    for key in ("required_themes", "forbidden_themes", "initial_observable_facts"):
        if key in data and data[key] is not None:
            if not isinstance(data[key], list):
                findings.append(ValidationFinding(key, "wrong_type", f"{key} must be an array"))
            else:
                for idx, item in enumerate(data[key]):
                    if not isinstance(item, str) or not item.strip():
                        findings.append(
                            ValidationFinding(f"{key}[{idx}]", "empty_value", "array item must be non-empty string")
                        )
    return findings


def validate_protected_values(data: dict[str, Any]) -> list[ValidationFinding]:
    findings: list[ValidationFinding] = []
    for key in data:
        lower = key.lower()
        if lower in PROTECTED_FIELD_NAMES:
            findings.append(ValidationFinding(key, "protected_field", f"protected field present: {key}"))
        if lower.endswith("_id") and lower not in {"investigator_character"}:
            if "character" not in lower:
                findings.append(ValidationFinding(key, "protected_field", f"suspected ID field: {key}"))
    blob = json.dumps(data).lower()
    if ".json" in blob or "do_not_read" in blob or "adventures/" in blob:
        findings.append(ValidationFinding("$", "protected_path", "response contains repository path-like content"))
    return findings


def validate_semantic_boundaries(data: dict[str, Any]) -> tuple[list[ValidationFinding], list[ValidationFinding]]:
    findings: list[ValidationFinding] = []
    warnings: list[ValidationFinding] = []
    opening = str(data.get("opening_situation", "")).lower()
    for pattern in AUTHOR_ONLY_PATTERNS:
        if re.search(pattern, opening):
            findings.append(
                ValidationFinding("opening_situation", "author_only_fact", "opening contains solution-like language")
            )
            break
    if any(marker in json.dumps(data).lower() for marker in COLD_STORAGE_MARKERS):
        findings.append(ValidationFinding("$", "forbidden_source_copy", "response appears to copy Cold Storage content"))
    solved_markers = ("already solved", "case closed", "killer was", "culprit is")
    if any(marker in opening for marker in solved_markers):
        findings.append(ValidationFinding("opening_situation", "solved_mystery", "opening appears already solved"))
    title = str(data.get("working_title", "")) + str(data.get("premise", ""))
    if re.search(r"[A-Z]:\\|/adventures/|UNIT-|LOC-", title):
        findings.append(ValidationFinding("$", "machine_identifier", "title/premise contains machine identifiers or paths"))
    if isinstance(data.get("target_playtime_minutes"), int) and data["target_playtime_minutes"] > 360:
        warnings.append(
            ValidationFinding("target_playtime_minutes", "human_review", "long playtime may need human review", "warning")
        )
    return findings, warnings


def validate_response(run_dir: Path) -> ResponseValidationResult:
    start = time.perf_counter()
    parsed_path = run_dir / "parsed_response.json"
    if not parsed_path.is_file():
        raise ResponseValidationError("parsed_response.json missing — run parse first")
    data = json.loads(parsed_path.read_text(encoding="utf-8"))
    findings = validate_response_schema(data)
    protected = validate_protected_values(data)
    semantic, warnings = validate_semantic_boundaries(data)
    findings.extend(semantic)
    passed = not findings and not protected
    duration = time.perf_counter() - start
    result = ResponseValidationResult(
        passed=passed,
        findings=findings,
        protected_findings=protected,
        warnings=warnings,
        duration_seconds=duration,
    )
    write_json(run_dir / "response_validation_report.json", result.to_report())
    if passed:
        transition_processing_stage(run_dir, ProcessingStage.RESPONSE_VALIDATED)
    return result
