"""Safe repository-relative path resolution for Local AI tasks."""

from __future__ import annotations

import os
from pathlib import Path


class PathValidationError(ValueError):
    """Raised when a path fails Local AI allowlist validation."""


REPO_MARKERS = ("AGENTS.md", "IDNE_ENGINE_v0.4.md")


def find_repo_root(start: Path | None = None) -> Path:
    """Locate repository root by walking parents for canonical markers."""
    current = (start or Path.cwd()).resolve()
    if current.is_file():
        current = current.parent
    for candidate in (current, *current.parents):
        if all((candidate / marker).is_file() for marker in REPO_MARKERS):
            return candidate
        if (candidate / ".git").exists():
            return candidate
    raise PathValidationError("repository root not found")


def to_posix_relpath(path: Path, repo_root: Path) -> str:
    rel = path.resolve().relative_to(repo_root.resolve())
    return rel.as_posix()


def normalize_repo_relative(path: str | Path, repo_root: Path) -> str:
    """Normalize a repository-relative path to deterministic POSIX form."""
    raw = str(path).strip().replace("\\", "/")
    if not raw:
        raise PathValidationError("empty path")
    if raw.startswith("/") or (len(raw) > 1 and raw[1] == ":"):
        raise PathValidationError(f"absolute path not allowed: {path}")
    if ".." in Path(raw).parts:
        raise PathValidationError(f"path traversal not allowed: {path}")
    normalized = Path(raw).as_posix()
    while normalized.startswith("./"):
        normalized = normalized[2:]
    return normalized


def resolve_allowed_file(
    repo_relative: str,
    repo_root: Path,
    *,
    require_file: bool = True,
) -> Path:
    """Resolve one allowlisted repository-relative path safely."""
    rel = normalize_repo_relative(repo_relative, repo_root)
    candidate = (repo_root / rel).resolve()
    root_resolved = repo_root.resolve()
    try:
        candidate.relative_to(root_resolved)
    except ValueError as exc:
        raise PathValidationError(f"path escapes repository: {repo_relative}") from exc
    if candidate.is_symlink():
        target = candidate.resolve()
        try:
            target.relative_to(root_resolved)
        except ValueError as exc:
            raise PathValidationError(f"symlink escapes repository: {repo_relative}") from exc
        candidate = target
    if require_file and not candidate.is_file():
        if candidate.is_dir():
            raise PathValidationError(f"directory not allowed where file required: {repo_relative}")
        raise PathValidationError(f"missing allowlisted file: {repo_relative}")
    return candidate


def normalize_allowlist(paths: list[str], repo_root: Path) -> list[str]:
    """Normalize, validate, deduplicate, and sort allowlisted paths deterministically."""
    seen: set[str] = set()
    normalized: list[str] = []
    for raw in paths:
        rel = normalize_repo_relative(raw, repo_root)
        if rel in seen:
            raise PathValidationError(f"duplicate normalized path: {rel}")
        seen.add(rel)
        normalized.append(rel)
    return sorted(normalized)


def resolve_allowlist(paths: list[str], repo_root: Path) -> list[Path]:
    """Resolve a normalized allowlist to absolute paths."""
    ordered = normalize_allowlist(paths, repo_root)
    return [resolve_allowed_file(rel, repo_root) for rel in ordered]


def is_repo_path_within(path: Path, repo_root: Path) -> bool:
    try:
        path.resolve().relative_to(repo_root.resolve())
        return True
    except ValueError:
        return False


def safe_task_directory_name(task_id: str) -> str:
    """Return a filesystem-safe task directory name."""
    safe = "".join(ch if ch.isalnum() or ch in "-_" else "-" for ch in task_id)
    safe = safe.strip("-") or "task"
    return safe[:120]
