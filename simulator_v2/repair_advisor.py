"""Repair advisor for Simulator v2 — suggestions only."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from simulator_v2.explainer import FindingExplanation
from simulator_v2.findings import DiagnosticFinding


@dataclass
class RepairOption:
    option_id: str
    finding_id: str
    intended_change: str
    files_likely_affected: list[str]
    expected_effect: str
    possible_side_effects: list[str]
    changes_engine: bool
    changes_adventure_logic: bool
    changes_player_package: bool
    changes_simulator_only: bool
    human_approval_required: bool
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
                "player_package": self.changes_player_package,
                "simulator_only": self.changes_simulator_only,
            },
            "human_approval_required": self.human_approval_required,
            **self.extra,
        }


def repair_options_for_finding(
    finding: DiagnosticFinding,
    explanation: FindingExplanation,
) -> list[RepairOption]:
    if not finding.repair_eligible:
        return []
    owner = finding.likely_owner
    return [
        RepairOption(
            option_id=f"REP-{finding.finding_id}-1",
            finding_id=finding.finding_id,
            intended_change=explanation.safe_repair_options[0] if explanation.safe_repair_options else "Review and correct canonical source",
            files_likely_affected=[finding.source_file] if finding.source_file else [],
            expected_effect="Finding resolved on re-validation",
            possible_side_effects=["May require coordinated changes across layers"],
            changes_engine=False,
            changes_adventure_logic=owner == "GENERATOR",
            changes_player_package=owner == "GENERATOR",
            changes_simulator_only=owner == "SIMULATOR",
            human_approval_required=finding.human_approval_required,
        )
    ]


def build_repair_backlog(findings: list[DiagnosticFinding], explanations: list[FindingExplanation]) -> str:
    by_id = {e.finding_id: e for e in explanations}
    lines = ["# Repair backlog", "", "Suggestions only — no automatic edits.", ""]
    for f in sorted(findings, key=lambda x: (x.severity, x.finding_id)):
        exp = by_id.get(f.finding_id)
        opts = repair_options_for_finding(f, exp) if exp else []
        lines.append(f"## {f.finding_id} ({f.severity})")
        lines.append(f"- Owner: {f.likely_owner}")
        lines.append(f"- Repair eligible: {f.repair_eligible}")
        for o in opts:
            lines.append(f"- **{o.option_id}:** {o.intended_change}")
        lines.append("")
    return "\n".join(lines) + "\n"
