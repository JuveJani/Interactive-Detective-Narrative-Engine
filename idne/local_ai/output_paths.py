"""Approved output path validation for Local AI draft writes."""

from __future__ import annotations

from pathlib import Path

from idne.local_ai.paths import PathValidationError, normalize_repo_relative

DRAFT_ROOT = "adventures/_local_ai_drafts"
DEFAULT_BRIEF_OUTPUT = f"{DRAFT_ROOT}/example_offline_brief/adventure_brief.json"
FORBIDDEN_OUTPUT_PREFIXES = (
    "adventures/The_Cold_Storage_Alarm/",
    "adventures/A_Hutoriasztas/",
    "idne/",
    "tests/",
    "simulator_v2/",
    "OFFLINE_AI/",
)
FORBIDDEN_OUTPUT_EXACT = frozenset(
    {
        "adventure_brief.json",
    }
)


def validate_output_path(repo_relative: str, repo_root: Path) -> str:
    rel = normalize_repo_relative(repo_relative, repo_root)
    if not rel.startswith(f"{DRAFT_ROOT}/"):
        raise PathValidationError(f"output must be under {DRAFT_ROOT}/")
    if not rel.endswith("/adventure_brief.json"):
        raise PathValidationError("output must end with /adventure_brief.json")
    for prefix in FORBIDDEN_OUTPUT_PREFIXES:
        if rel.startswith(prefix):
            raise PathValidationError(f"output not allowed under {prefix}")
    candidate = (repo_root / rel).resolve()
    root_resolved = repo_root.resolve()
    try:
        candidate.relative_to(root_resolved)
    except ValueError as exc:
        raise PathValidationError("output escapes repository") from exc
    rel_path = repo_root / rel
    if rel_path.is_symlink():
        resolved = rel_path.resolve()
        try:
            resolved.relative_to(root_resolved)
        except ValueError as exc:
            raise PathValidationError("output symlink escapes repository") from exc
        candidate = resolved
    if candidate.exists() and candidate.is_dir():
        raise PathValidationError("output path is a directory")
    return rel


def output_exists(repo_root: Path, output_rel: str) -> bool:
    return (repo_root / output_rel).is_file()


def output_created_by_task(repo_root: Path, output_rel: str, task_id: str) -> bool:
    marker = repo_root / output_rel
    if not marker.is_file():
        return False
    sidecar = marker.with_suffix(".json.local_ai_applied")
    if not sidecar.is_file():
        return False
    return task_id in sidecar.read_text(encoding="utf-8")
