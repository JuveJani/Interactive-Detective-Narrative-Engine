"""Finding-specific repair plan files (preserves global backlog)."""

from __future__ import annotations

import json
from pathlib import Path

from simulator.atomic_io import atomic_write_json, atomic_write_text
from simulator.explainer import FindingExplanation
from simulator.repair_advisor import RepairOption, build_repair_backlog


def write_finding_repair_plan(
    output_folder: Path,
    finding_id: str,
    options: list[RepairOption],
    explanation: FindingExplanation,
) -> tuple[Path, Path]:
    md_path = output_folder / f"repair_plan_{finding_id}.md"
    json_path = output_folder / f"repair_plan_{finding_id}.json"

    lines = [
        f"# Repair plan: {finding_id}",
        "",
        "## Plain-language problem",
        explanation.plain_problem,
        "",
        "## Options (suggestions only — no automatic edits)",
        "",
    ]
    for opt in options:
        lines.append(f"### {opt.option_id}")
        lines.append(f"- **Change:** {opt.intended_change}")
        lines.append(f"- **Files:** {', '.join(opt.files_likely_affected)}")
        lines.append(f"- **Human approval required:** {'yes' if opt.human_approval_required else 'no'}")
        lines.append("")

    payload = {
        "finding_id": finding_id,
        "explanation": explanation.to_dict(),
        "repair_options": [o.to_dict() for o in options],
    }

    atomic_write_text(md_path, "\n".join(lines) + "\n")
    atomic_write_json(json_path, payload)
    return md_path, json_path


def ensure_global_backlog(
    output_folder: Path,
    options: list[RepairOption],
    findings: list,
) -> None:
    """Write full backlog only if missing; never shrink existing backlog."""
    backlog_path = output_folder / "repair_backlog.md"
    options_path = output_folder / "repair_options.json"
    if not backlog_path.exists():
        atomic_write_text(backlog_path, build_repair_backlog(options, findings))
    if not options_path.exists():
        atomic_write_json(options_path, [o.to_dict() for o in options])
