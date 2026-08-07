"""Apply validated proposals to approved draft destinations."""

from __future__ import annotations

import json
import os
import time
from pathlib import Path

from idne.local_ai.content_identity import (
    parsed_response_sha256,
    verify_prompt_identity,
    verify_source_identity,
)
from idne.local_ai.output_paths import output_created_by_task, output_exists, validate_output_path
from idne.local_ai.paths import find_repo_root
from idne.local_ai.run_state import load_status, load_task, write_json
from idne.local_ai.task_model import ProcessingStage, TaskStatus, sha256_bytes, transition_processing_stage, transition_task


class ApplyError(RuntimeError):
    pass


def apply_proposal(
    run_dir: Path,
    *,
    overwrite: bool = False,
    acknowledge_warnings: bool = False,
) -> dict[str, object]:
    start = time.perf_counter()
    task = load_task(run_dir)
    if task.status not in {TaskStatus.VALIDATED, TaskStatus.APPLIED}:
        raise ApplyError(f"task status must be VALIDATED, got {task.status.value}")
    if task.status == TaskStatus.APPLIED and not overwrite:
        raise ApplyError("task already applied; use --overwrite to rewrite same-task output")

    status = load_status(run_dir)
    if task.status == TaskStatus.VALIDATED and status.get("processing_stage") != ProcessingStage.VALIDATED.value:
        raise ApplyError("proposal validation must pass before apply")
    if task.status == TaskStatus.APPLIED and not overwrite:
        raise ApplyError("task already applied; use --overwrite to rewrite same-task output")

    response_validation = json.loads((run_dir / "response_validation_report.json").read_text(encoding="utf-8"))
    if response_validation.get("warnings") and not acknowledge_warnings:
        raise ApplyError("warnings require --acknowledge-warnings before apply")

    repo_root = find_repo_root(run_dir)
    verify_source_identity(run_dir, task)
    verify_prompt_identity(run_dir)

    output_rel = task.allowed_output_files[0]
    validate_output_path(output_rel, repo_root)
    dest = repo_root / output_rel
    if dest.exists() and not overwrite:
        if not output_created_by_task(repo_root, output_rel, task.task_id):
            raise ApplyError("output exists; use --overwrite only for same-task outputs")
    if dest.exists() and overwrite and not output_created_by_task(repo_root, output_rel, task.task_id):
        raise ApplyError("overwrite allowed only for outputs created by this task identity")

    brief_bytes = (run_dir / "proposal" / "adventure_brief.json").read_bytes()
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".tmp")
    tmp.write_bytes(brief_bytes)
    os.replace(tmp, dest)
    applied_hash = sha256_bytes(brief_bytes)

    sidecar = dest.with_suffix(".json.local_ai_applied")
    sidecar.write_text(
        json.dumps({"task_id": task.task_id, "applied_hash": applied_hash}, indent=2) + "\n",
        encoding="utf-8",
    )

    manifest_path = run_dir / "proposal" / "proposal_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["applied_hash"] = applied_hash
    manifest["applied_at"] = status.get("transport", {}).get("ended_at")
    write_json(manifest_path, manifest)

    duration = time.perf_counter() - start
    if task.status != TaskStatus.APPLIED:
        transition_processing_stage(run_dir, ProcessingStage.APPLIED)
        transition_task(task, TaskStatus.APPLIED)
        write_json(run_dir / "task.json", task.to_dict())
    apply_report = {
        "success": True,
        "output": output_rel,
        "applied_hash": applied_hash,
        "duration_seconds": duration,
    }
    write_json(run_dir / "apply_report.json", apply_report)
    status = load_status(run_dir)
    status["status"] = task.status.value
    write_json(run_dir / "status.json", status)
    return apply_report
