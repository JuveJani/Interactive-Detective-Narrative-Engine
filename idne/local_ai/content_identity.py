"""Content identity tracking for Local AI tasks."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from idne.local_ai.run_state import load_status, load_task, write_json
from idne.local_ai.task_model import LocalAITask, compute_run_definition_identity, sha256_bytes, sha256_text


def response_sha256(run_dir: Path) -> str:
    return sha256_text((run_dir / "response.txt").read_text(encoding="utf-8"))


def parsed_response_sha256(run_dir: Path) -> str:
    return sha256_bytes((run_dir / "parsed_response.json").read_bytes())


def proposal_brief_sha256(run_dir: Path) -> str:
    return sha256_bytes((run_dir / "proposal" / "adventure_brief.json").read_bytes())


def load_identities(run_dir: Path) -> dict[str, Any]:
    status = load_status(run_dir)
    return dict(status.get("identities", {}))


def save_identities(run_dir: Path, identities: dict[str, Any]) -> None:
    status_path = run_dir / "status.json"
    status = json.loads(status_path.read_text(encoding="utf-8"))
    status["identities"] = identities
    write_json(status_path, status)


def verify_run_definition(run_dir: Path, task: LocalAITask) -> None:
    status = load_status(run_dir)
    stored_identity = status.get("run_definition_identity")
    current_identity = compute_run_definition_identity(task)
    if stored_identity and stored_identity != current_identity:
        raise ValueError("run definition identity mismatch")
    stored_outputs = status.get("allowed_output_files")
    if stored_outputs and stored_outputs != task.allowed_output_files:
        raise ValueError("allowed output destination mismatch")
    if (run_dir / "transport_report.json").is_file() and stored_identity:
        if task.task_id != status.get("task_id"):
            raise ValueError("transport task_id mismatch")


def verify_source_identity(run_dir: Path, task: LocalAITask) -> None:
    status = load_status(run_dir)
    stored = status.get("source_content_sha256")
    if stored and stored != task.source_content_identity.sha256:
        raise ValueError("source content identity mismatch")


def verify_prompt_identity(run_dir: Path) -> str:
    prompt_path = run_dir / "prompt.txt"
    prompt_sha256 = sha256_text(prompt_path.read_text(encoding="utf-8"))
    expected = load_status(run_dir).get("prompt_sha256")
    if expected and expected != prompt_sha256:
        raise ValueError("prompt identity mismatch")
    return prompt_sha256


def record_identity(run_dir: Path, key: str, value: str) -> None:
    identities = load_identities(run_dir)
    identities[key] = value
    save_identities(run_dir, identities)


def stable_brief_id(task: LocalAITask) -> str:
    payload = json.dumps(
        {
            "task_id": task.task_id,
            "source_sha256": task.source_content_identity.sha256,
            "task_type": task.task_type,
        },
        sort_keys=True,
        separators=(",", ":"),
    )
    return f"draft-{sha256_text(payload)[:12]}"
