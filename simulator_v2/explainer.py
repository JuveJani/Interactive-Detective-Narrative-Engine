"""Human-readable explanations for Simulator v2 findings."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from simulator_v2.findings import DiagnosticFinding


@dataclass
class FindingExplanation:
    finding_id: str
    plain_problem: str
    why_it_matters: str
    evidence: str
    expected_rule: str
    actual_behavior: str
    likely_root_cause: str
    owning_layer: str
    confidence: str
    trust_affects_conclusion: bool
    where_to_look: list[str]
    safe_repair_options: list[str]
    repair_risks: list[str]
    required_human_decision: str
    validation_after_repair: list[str]
    extra: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "finding_id": self.finding_id,
            "plain_problem": self.plain_problem,
            "why_it_matters": self.why_it_matters,
            "evidence": self.evidence,
            "expected_rule": self.expected_rule,
            "actual_behavior": self.actual_behavior,
            "likely_root_cause": self.likely_root_cause,
            "owning_layer": self.owning_layer,
            "confidence": self.confidence,
            "trust_affects_conclusion": self.trust_affects_conclusion,
            "where_to_look": self.where_to_look,
            "safe_repair_options": self.safe_repair_options,
            "repair_risks": self.repair_risks,
            "required_human_decision": self.required_human_decision,
            "validation_after_repair": self.validation_after_repair,
            **self.extra,
        }

    def to_markdown(self) -> str:
        lines = [
            f"# Finding {self.finding_id}",
            "",
            "## Plain-language problem",
            self.plain_problem,
            "",
            "## Why it matters",
            self.why_it_matters,
            "",
            "## Evidence",
            self.evidence,
            "",
            "## Expected",
            self.expected_rule,
            "",
            "## Observed",
            self.actual_behavior,
            "",
            "## Likely root cause",
            self.likely_root_cause,
            "",
            "## Owning layer",
            self.owning_layer,
            "",
            "## Confidence",
            self.confidence,
            "",
            "## Trust affects conclusion",
            "Yes" if self.trust_affects_conclusion else "No",
            "",
            "## Where to look",
        ]
        lines.extend(f"- `{p}`" for p in self.where_to_look)
        lines.extend(["", "## Safe repair options"])
        lines.extend(f"- {o}" for o in self.safe_repair_options)
        lines.extend(["", "## Risks"])
        lines.extend(f"- {r}" for r in self.repair_risks)
        lines.extend(["", "## Required human decision", self.required_human_decision, "", "## Validation after repair"])
        lines.extend(f"- `{c}`" for c in self.validation_after_repair)
        return "\n".join(lines) + "\n"


def explain_finding(finding: DiagnosticFinding, trust: dict[str, Any]) -> FindingExplanation:
    trusted = trust.get("trusted", False)
    trust_affects = finding.trust_impact not in ("none", "") and not trusted
    owner = finding.likely_owner
    if not trusted and owner == "GENERATOR" and finding.validator == "simulator":
        owner = "UNDETERMINED"

    paths = finding.affected_paths or ([finding.source_file] if finding.source_file else [])
    validation_cmds = [
        f"python -m idne.sim_v2 validate <adventure>",
        f"python -m idne.validate_adventure {finding.source_file or '<adventure_root>'}",
    ]
    if finding.validator in ("investigation", "story", "playtime", "dm_feeling"):
        validation_cmds.insert(0, f"python -m idne.{finding.validator}_validate <adventure_root>")

    return FindingExplanation(
        finding_id=finding.finding_id,
        plain_problem=finding.observed_behavior or finding.simulation_evidence,
        why_it_matters=f"Affects {finding.affected_entity or 'adventure integrity'}",
        evidence=finding.simulation_evidence,
        expected_rule=finding.expected_behavior,
        actual_behavior=finding.observed_behavior,
        likely_root_cause=f"Likely owned by {finding.likely_owner} ({finding.validator} validator)",
        owning_layer=owner,
        confidence=finding.confidence,
        trust_affects_conclusion=trust_affects,
        where_to_look=paths,
        safe_repair_options=[finding.extra.get("suggested_review_action", "Review canonical source and re-run validation")],
        repair_risks=["May affect player-facing balance or proof structure"],
        required_human_decision="Required" if finding.human_approval_required else "Optional review",
        validation_after_repair=validation_cmds[:3],
    )


def explain_all(findings: list[DiagnosticFinding], trust: dict[str, Any]) -> list[FindingExplanation]:
    return [explain_finding(f, trust) for f in findings]
