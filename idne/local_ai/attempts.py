"""Preserve prior model attempts when re-running with --force."""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

from idne.local_ai.run_state import load_status, write_json

ATTEMPT_ARTIFACTS = (
    "request.json",
    "raw_response.json",
    "response.txt",
    "transport_report.json",
    "response_parse_report.json",
    "parsed_response.json",
    "response_validation_report.json",
    "apply_report.json",
)


def attempts_root(run_dir: Path) -> Path:
    return run_dir / "attempts"


def next_attempt_number(run_dir: Path) -> int:
    root = attempts_root(run_dir)
    if not root.is_dir():
        return 1
    existing = []
    for child in root.iterdir():
        if child.is_dir() and child.name.isdigit():
            existing.append(int(child.name))
    return max(existing, default=0) + 1


def _copy_if_exists(src: Path, dest: Path) -> None:
    if src.is_file():
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)


def _copy_tree_if_exists(src: Path, dest: Path) -> None:
    if src.is_dir():
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(src, dest)


def archive_current_attempt(run_dir: Path) -> Path | None:
    """Move active response/proposal artifacts into attempts/NNN/."""
    if not (run_dir / "response.txt").is_file():
        return None
    attempt_num = next_attempt_number(run_dir)
    attempt_dir = attempts_root(run_dir) / f"{attempt_num:03d}"
    attempt_dir.mkdir(parents=True, exist_ok=True)
    for name in ATTEMPT_ARTIFACTS:
        _copy_if_exists(run_dir / name, attempt_dir / name)
    _copy_tree_if_exists(run_dir / "proposal", attempt_dir / "proposal")
    status = load_status(run_dir)
    snapshot: dict[str, Any] = {
        "attempt": attempt_num,
        "processing_stage": status.get("processing_stage"),
        "transport": status.get("transport"),
        "identities": status.get("identities"),
    }
    write_json(attempt_dir / "attempt_status.json", snapshot)
    return attempt_dir


def reset_processing_state(run_dir: Path) -> None:
    """Clear post-response artifacts before a forced re-run."""
    for name in ATTEMPT_ARTIFACTS:
        path = run_dir / name
        if path.is_file():
            path.unlink()
    proposal = run_dir / "proposal"
    if proposal.is_dir():
        shutil.rmtree(proposal)
    status_path = run_dir / "status.json"
    if status_path.is_file():
        status = load_status(run_dir)
        status["processing_stage"] = "NONE"
        status.pop("identities", None)
        write_json(status_path, status)


def list_attempts(run_dir: Path) -> list[dict[str, Any]]:
    root = attempts_root(run_dir)
    if not root.is_dir():
        return []
    attempts: list[dict[str, Any]] = []
    for child in sorted(root.iterdir()):
        if not child.is_dir() or not child.name.isdigit():
            continue
        info: dict[str, Any] = {"attempt": child.name, "directory": child.as_posix()}
        status_path = child / "attempt_status.json"
        if status_path.is_file():
            info.update(json.loads(status_path.read_text(encoding="utf-8")))
        attempts.append(info)
    return attempts


def active_attempt(run_dir: Path) -> str:
    status = load_status(run_dir)
    archived = list_attempts(run_dir)
    current = len(archived) + (1 if (run_dir / "response.txt").is_file() else 0)
    if current == 0:
        return "none"
    return f"{current:03d}"
