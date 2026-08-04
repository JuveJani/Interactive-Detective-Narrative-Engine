"""Generation report writers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from idne.generate.state import GenerationState


def reports_dir(workspace_root: Path) -> Path:
    path = workspace_root / ".generation" / "reports"
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_all_reports(workspace_root: Path, state: GenerationState) -> dict[str, str]:
    root = reports_dir(workspace_root)
    paths: dict[str, str] = {}

    summary = [
        "# Generation Summary",
        "",
        f"Adventure ID: {state.adventure_id}",
        f"Readiness: {state.readiness_status}",
        f"Logic validation complete: {state.logic_validation_complete}",
        "",
        "## Stage status",
        "",
    ]
    for stage, status in state.stage_status.items():
        summary.append(f"- {stage}: {status}")
    paths["generation_summary.md"] = str(root / "generation_summary.md")
    Path(paths["generation_summary.md"]).write_text("\n".join(summary), encoding="utf-8")

    stage_status_path = root / "stage_status.json"
    stage_status_path.write_text(json.dumps(state.stage_status, indent=2), encoding="utf-8")
    paths["stage_status.json"] = str(stage_status_path)

    repair_lines = ["# Repair History", ""]
    for entry in state.repair_attempts:
        repair_lines.append(f"- {json.dumps(entry)}")
    repair_path = root / "repair_history.md"
    repair_path.write_text("\n".join(repair_lines), encoding="utf-8")
    paths["repair_history.md"] = str(repair_path)

    approval_lines = ["# Human Approval Queue", ""]
    from idne.generate.stages import STAGE_DEFINITIONS

    for stage_id, defn in STAGE_DEFINITIONS.items():
        if defn.requires_human_approval:
            approved = stage_id in state.human_approvals
            approval_lines.append(
                f"- {stage_id}: {'APPROVED' if approved else 'PENDING'}"
            )
    approval_path = root / "human_approval_queue.md"
    approval_path.write_text("\n".join(approval_lines), encoding="utf-8")
    paths["human_approval_queue.md"] = str(approval_path)

    unresolved = {
        "invalidated_stages": state.invalidated_stages,
        "validator_results": {
            k: v.get("status")
            for k, v in state.validator_results.items()
            if isinstance(v, dict)
        },
    }
    unresolved_path = root / "unresolved_findings.json"
    unresolved_path.write_text(json.dumps(unresolved, indent=2), encoding="utf-8")
    paths["unresolved_findings.json"] = str(unresolved_path)

    usage_path = root / "model_usage.json"
    usage_path.write_text(json.dumps(state.token_estimates, indent=2), encoding="utf-8")
    paths["model_usage.json"] = str(usage_path)

    manifest_path = root / "package_manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "adventure_id": state.adventure_id,
                "readiness_status": state.readiness_status,
                "reports": paths,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    paths["package_manifest.json"] = str(manifest_path)

    return paths
