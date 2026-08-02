"""Repair option generation — suggestions only, no automatic edits."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from simulator.explainer import FindingExplanation
from simulator.models import Finding


@dataclass
class RepairOption:
    option_id: str
    intended_change: str
    files_likely_affected: list[str]
    expected_effect: str
    possible_side_effects: list[str]
    changes_engine: bool
    changes_adventure_logic: bool
    changes_delivery_adapter: bool
    changes_player_package: bool
    changes_simulator_only: bool
    human_approval_required: bool
    finding_id: str
    extra: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "option_id": self.option_id,
            "finding_id": self.finding_id,
            "intended_change": self.intended_change,
            "files_likely_affected": self.files_likely_affected,
            "expected_effect": self.expected_effect,
            "possible_side_effects": self.possible_side_effects,
            "changes": {
                "engine": self.changes_engine,
                "adventure_logic": self.changes_adventure_logic,
                "delivery_adapter": self.changes_delivery_adapter,
                "player_package": self.changes_player_package,
                "simulator_only": self.changes_simulator_only,
            },
            "human_approval_required": self.human_approval_required,
            **self.extra,
        }


def _layer_flags(layer: str) -> dict[str, bool]:
    return {
        "changes_engine": layer == "ENGINE",
        "changes_adventure_logic": layer == "ADVENTURE",
        "changes_delivery_adapter": layer == "DELIVERY_ADAPTER",
        "changes_player_package": layer == "PLAYER_PACKAGE",
        "changes_simulator_only": layer == "SIMULATOR",
    }


def repair_options_for_finding(
    finding: Finding,
    explanation: FindingExplanation,
) -> list[RepairOption]:
    opts: list[RepairOption] = []
    layer = explanation.owning_layer
    flags = _layer_flags(layer)

    if finding.layer == "SIMULATOR" or finding.auto_fix_possible:
        opts.append(
            RepairOption(
                option_id=f"REP-{finding.id}-SIM",
                finding_id=finding.id,
                intended_change=f"Patch simulator to match expected rule: {finding.expected_rule}",
                files_likely_affected=[finding.file, "tests/"],
                expected_effect="Simulator behavior aligns with adapter semantics.",
                possible_side_effects=["May reveal adventure issues previously hidden by bugs."],
                human_approval_required=False,
                changes_engine=False,
                changes_adventure_logic=False,
                changes_delivery_adapter=False,
                changes_player_package=False,
                changes_simulator_only=True,
            )
        )

    if layer in ("ADVENTURE", "DELIVERY_ADAPTER", "UNDETERMINED"):
        opts.append(
            RepairOption(
                option_id=f"REP-{finding.id}-ADAPTER",
                finding_id=finding.id,
                intended_change=f"Clarify or fix adapter entry for {finding.identifier}",
                files_likely_affected=["adventures/CASE_BENCHMARK_v0.4/sim_adapter.json"],
                expected_effect="Machine-readable graph matches intended play logic.",
                possible_side_effects=["Requires player text cross-check; may need logic author review."],
                human_approval_required=True,
                changes_engine=False,
                changes_simulator_only=False,
                changes_adventure_logic=layer == "ADVENTURE",
                changes_delivery_adapter=True,
                changes_player_package=False,
            )
        )

    if layer == "PLAYER_PACKAGE":
        opts.append(
            RepairOption(
                option_id=f"REP-{finding.id}-PLAYER",
                finding_id=finding.id,
                intended_change=f"Edit player-facing text cited in {finding.file}",
                files_likely_affected=[finding.file],
                expected_effect="Printed or digital player materials match fair-play rules.",
                possible_side_effects=["Changes what players read; needs layout review."],
                human_approval_required=True,
                changes_engine=False,
                changes_simulator_only=False,
                changes_adventure_logic=False,
                changes_delivery_adapter=False,
                changes_player_package=True,
            )
        )

    if layer == "HUMAN_PLAYTEST" or finding.human_approval_required:
        opts.append(
            RepairOption(
                option_id=f"REP-{finding.id}-PLAYTEST",
                finding_id=finding.id,
                intended_change="Run a manual cooperative playtest focusing on this finding.",
                files_likely_affected=["human_playtest_questions.md"],
                expected_effect="Confirms whether the issue is felt by real players.",
                possible_side_effects=["Time cost only; no file changes."],
                human_approval_required=True,
                changes_engine=False,
                changes_adventure_logic=False,
                changes_delivery_adapter=False,
                changes_player_package=False,
                changes_simulator_only=False,
            )
        )

    if not opts:
        opts.append(
            RepairOption(
                option_id=f"REP-{finding.id}-REVIEW",
                finding_id=finding.id,
                intended_change="Manual review of evidence; no automatic change recommended.",
                files_likely_affected=[finding.file],
                expected_effect="Human decides next step with full context.",
                possible_side_effects=[],
                human_approval_required=True,
                changes_engine=flags["changes_engine"],
                changes_adventure_logic=flags["changes_adventure_logic"],
                changes_delivery_adapter=flags["changes_delivery_adapter"],
                changes_player_package=flags["changes_player_package"],
                changes_simulator_only=flags["changes_simulator_only"],
            )
        )

    return opts


def build_repair_backlog(options: list[RepairOption], findings: list[Finding]) -> str:
    sev_order = {"critical": 0, "major": 1, "minor": 2, "info": 3}
    by_id = {f.id: f for f in findings}
    ranked = sorted(
        options,
        key=lambda o: (
            sev_order.get(by_id.get(o.finding_id, Finding("", "info", "", "", "", "", "", "", False, False)).severity, 9),
            o.finding_id,
        ),
    )
    lines = ["# Repair backlog", "", "Ordered by severity. Options are suggestions only.", ""]
    for opt in ranked:
        f = by_id.get(opt.finding_id)
        sev = f.severity if f else "unknown"
        lines.append(f"## {opt.finding_id} ({sev}) — {opt.option_id}")
        lines.append(f"- **Change:** {opt.intended_change}")
        lines.append(f"- **Files:** {', '.join(opt.files_likely_affected)}")
        lines.append(f"- **Human approval:** {'yes' if opt.human_approval_required else 'no'}")
        lines.append("")
    return "\n".join(lines)


def write_proposed_patch(
    output_folder: Path,
    option: RepairOption,
    explanation: FindingExplanation,
) -> tuple[Path, Path]:
    patch_path = output_folder / f"proposed_fix_{option.finding_id}.patch"
    md_path = output_folder / f"proposed_fix_{option.finding_id}.md"
    md_path.write_text(
        "\n".join(
            [
                f"# Proposed fix for {option.finding_id}",
                "",
                f"**Option:** {option.option_id}",
                "",
                "## Intended change",
                option.intended_change,
                "",
                "## Files likely affected",
                *[f"- `{f}`" for f in option.files_likely_affected],
                "",
                "## Expected effect",
                option.expected_effect,
                "",
                "## Side effects",
                *[f"- {s}" for s in option.possible_side_effects],
                "",
                "## Human approval required",
                "Yes — apply only after review.",
                "",
                "## Context",
                explanation.plain_problem,
                "",
                "_This file does not modify the repository. Apply changes manually._",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    patch_path.write_text(
        f"# Proposed patch placeholder for {option.finding_id}\n"
        f"# Option: {option.option_id}\n"
        f"# Generate real diff after human selects an approach.\n",
        encoding="utf-8",
    )
    return patch_path, md_path


def all_repair_options(
    findings: list[Finding],
    explanations: list[FindingExplanation],
) -> list[RepairOption]:
    expl_by_id = {e.finding_id: e for e in explanations}
    out: list[RepairOption] = []
    for f in findings:
        expl = expl_by_id.get(f.id)
        if expl:
            out.extend(repair_options_for_finding(f, expl))
    return out
