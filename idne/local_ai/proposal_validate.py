"""Validate canonical brief proposals."""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

from idne.generate.brief import validate_brief
from idne.local_ai.content_identity import (
    parsed_response_sha256,
    proposal_brief_sha256,
    verify_prompt_identity,
    verify_source_identity,
)
from idne.local_ai.output_paths import validate_output_path
from idne.local_ai.paths import find_repo_root
from idne.local_ai.run_state import load_status, load_task, write_json
from idne.local_ai.task_model import ProcessingStage, TaskStatus, transition_processing_stage, transition_task


def validate_proposal(run_dir: Path) -> dict[str, Any]:
    start = time.perf_counter()
    status = load_status(run_dir)
    if status.get("processing_stage") != ProcessingStage.PROPOSAL_READY.value:
        raise RuntimeError("proposal must be built before validation")

    task = load_task(run_dir)
    repo_root = find_repo_root(run_dir)
    proposal_dir = run_dir / "proposal"
    brief_path = proposal_dir / "adventure_brief.json"
    manifest_path = proposal_dir / "proposal_manifest.json"
    if not brief_path.is_file() or not manifest_path.is_file():
        raise RuntimeError("proposal artifacts missing")

    findings: list[str] = []
    verify_source_identity(run_dir, task)
    verify_prompt_identity(run_dir)
    brief = json.loads(brief_path.read_text(encoding="utf-8"))
    findings.extend(validate_brief(brief))

    output_rel = task.allowed_output_files[0]
    try:
        validated_output = validate_output_path(output_rel, repo_root)
        if validated_output != output_rel:
            findings.append("output path normalization mismatch")
    except Exception as exc:  # noqa: BLE001
        findings.append(str(exc))

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("output_destination") != output_rel:
        findings.append("proposal manifest output mismatch")
    if manifest.get("task_id") != task.task_id:
        findings.append("proposal manifest task_id mismatch")

    stored_parsed = status.get("identities", {}).get("parsed_response_sha256")
    current_parsed = parsed_response_sha256(run_dir)
    if stored_parsed and stored_parsed != current_parsed:
        findings.append("parsed response identity changed since proposal build")
    stored_brief = status.get("identities", {}).get("proposal_brief_sha256")
    current_brief = proposal_brief_sha256(run_dir)
    if stored_brief and stored_brief != current_brief:
        findings.append("proposal brief identity changed since proposal build")

    passed = not findings
    duration = time.perf_counter() - start
    report = {
        "passed": passed,
        "findings": findings,
        "canonical_brief_validator": "PASS" if not findings else "FAIL",
        "duration_seconds": duration,
    }
    write_json(proposal_dir / "validation_report.json", report)
    if passed:
        transition_processing_stage(run_dir, ProcessingStage.VALIDATED)
        transition_task(task, TaskStatus.VALIDATED)
        write_json(run_dir / "task.json", task.to_dict())
        status = load_status(run_dir)
        status["status"] = task.status.value
        write_json(run_dir / "status.json", status)
    return report
