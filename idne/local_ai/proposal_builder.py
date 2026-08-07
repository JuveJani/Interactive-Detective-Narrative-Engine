"""Build canonical Adventure Generator v2 brief proposals."""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

from idne.local_ai.content_identity import (
    parsed_response_sha256,
    proposal_brief_sha256,
    record_identity,
    response_sha256,
    stable_brief_id,
)
from idne.local_ai.paths import find_repo_root
from idne.local_ai.run_state import load_status, load_task, write_json
from idne.local_ai.task_model import ProcessingStage, TaskStatus, transition_processing_stage, utc_now_iso

OPTIONAL_NARRATIVE_STRING_FIELDS = ("working_title", "setting")


def _optional_author_notes(data: dict[str, Any]) -> str | None:
    raw = data.get("author_notes")
    if raw is None:
        return None
    notes = str(raw).strip()
    return notes or None


def _optional_string_list(data: dict[str, Any], key: str) -> list[str] | None:
    raw = data.get(key)
    if not raw:
        return None
    items = [str(item).strip() for item in raw]
    items = [item for item in items if item]
    return items or None


def map_semantic_to_canonical(data: dict[str, Any]) -> dict[str, Any]:
    brief: dict[str, Any] = {
        "universe": data["universe"].strip(),
        "genre": data["genre"].strip(),
        "realism_level": data["realism_level"].strip(),
        "player_mode": data["player_mode"],
        "investigator_character": data["investigator_character"].strip(),
        "target_playtime_minutes": int(data["target_playtime_minutes"]),
        "in_world_duration": data["in_world_duration"].strip(),
        "tone": data["tone"].strip(),
        "difficulty": data["difficulty"].strip(),
        "location_scale": data["location_scale"].strip(),
        "content_boundaries": data["content_boundaries"].strip(),
        "premise": data["premise"].strip(),
        "opening_situation": data["opening_situation"].strip(),
    }
    for field in OPTIONAL_NARRATIVE_STRING_FIELDS:
        value = data.get(field)
        if value is not None and str(value).strip():
            brief[field] = str(value).strip()
    facts = _optional_string_list(data, "initial_observable_facts")
    if facts:
        brief["initial_observable_facts"] = facts
    if data.get("required_themes"):
        brief["required_themes"] = [str(x).strip() for x in data["required_themes"]]
    if data.get("forbidden_themes"):
        brief["forbidden_themes"] = [str(x).strip() for x in data["forbidden_themes"]]
    author_notes = _optional_author_notes(data)
    if author_notes:
        brief["author_notes"] = author_notes
    return brief


def build_proposal(run_dir: Path) -> dict[str, Any]:
    start = time.perf_counter()
    status = load_status(run_dir)
    if status.get("processing_stage") != ProcessingStage.RESPONSE_VALIDATED.value:
        raise RuntimeError("response validation must pass before building proposal")
    validation = json.loads((run_dir / "response_validation_report.json").read_text(encoding="utf-8"))
    if not validation.get("passed"):
        raise RuntimeError("response validation failed")

    task = load_task(run_dir)
    repo_root = find_repo_root(run_dir)
    parsed = json.loads((run_dir / "parsed_response.json").read_text(encoding="utf-8"))
    canonical = map_semantic_to_canonical(parsed)
    brief_id = stable_brief_id(task)
    output_rel = task.allowed_output_files[0]
    transport = status.get("transport", {})
    proposal_dir = run_dir / "proposal"
    proposal_dir.mkdir(parents=True, exist_ok=True)

    brief_text = json.dumps(canonical, indent=2, sort_keys=True) + "\n"
    (proposal_dir / "adventure_brief.json").write_text(brief_text, encoding="utf-8")

    provenance = {
        "task_id": task.task_id,
        "brief_id": brief_id,
        "source_content_identity": task.source_content_identity.to_dict(),
        "prompt_sha256": status.get("prompt_sha256"),
        "response_sha256": response_sha256(run_dir),
        "parsed_response_sha256": parsed_response_sha256(run_dir),
        "model": transport.get("selected_model"),
        "semantic_fields": sorted(parsed.keys()),
        "deterministic_fields_added": [
            "brief_id",
            "output_destination",
            "provenance",
            "approval_status",
            "stage_status",
        ],
    }
    write_json(proposal_dir / "provenance.json", provenance)

    manifest = {
        "schema_version": "1.0",
        "task_id": task.task_id,
        "brief_id": brief_id,
        "output_destination": output_rel,
        "approval_status": "PENDING_HUMAN_REVIEW",
        "stage_status": "AWAITING_APPROVAL",
        "brief_sha256": proposal_brief_sha256(run_dir),
        "generated_at": utc_now_iso(),
    }
    write_json(proposal_dir / "proposal_manifest.json", manifest)

    review_lines = [
        f"# Human Review — {task.task_type}",
        "",
        f"Task: {task.task_id}",
        f"Model: {transport.get('selected_model', 'unknown')}",
        f"Source concept: {task.source_content_identity.path}",
        "",
        "## Semantic fields produced",
        ", ".join(sorted(parsed.keys())),
        "",
        "## Deterministic fields added by Python",
        "brief_id, output destination, provenance, approval/stage status placeholders",
        "",
        f"## Intended apply destination",
        output_rel,
        "",
        "## Validator result",
        "Pending proposal validation",
        "",
        "No files have been applied to the repository yet.",
    ]
    (proposal_dir / "human_review.md").write_text("\n".join(review_lines) + "\n", encoding="utf-8")

    duration = time.perf_counter() - start
    write_json(
        proposal_dir / "validation_report.json",
        {"proposal_build_seconds": duration, "status": "PENDING_VALIDATION"},
    )
    record_identity(run_dir, "proposal_brief_sha256", proposal_brief_sha256(run_dir))
    record_identity(run_dir, "parsed_response_sha256", parsed_response_sha256(run_dir))
    transition_processing_stage(run_dir, ProcessingStage.PROPOSAL_READY)
    return {"brief_id": brief_id, "output_destination": output_rel, "duration_seconds": duration}
