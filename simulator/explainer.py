"""Human-readable finding explanations for offline use."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from simulator.models import Finding


LAYER_LABELS = {
    "ENGINE": "engine rules",
    "ADVENTURE": "adventure logic",
    "DELIVERY_ADAPTER": "delivery adapter",
    "PLAYER_PACKAGE": "player package",
    "VALIDATOR": "validator",
    "SIMULATOR": "simulator code",
    "HUMAN_PLAYTEST": "human playtest",
    "UNDETERMINED": "undetermined until simulator is trusted",
}


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
            "## Why it matters to players",
            self.why_it_matters,
            "",
            "## Exact evidence",
            self.evidence,
            "",
            "## Expected rule",
            self.expected_rule,
            "",
            "## Actual behavior",
            self.actual_behavior,
            "",
            "## Likely root cause",
            self.likely_root_cause,
            "",
            "## Owning layer",
            f"{self.owning_layer} ({LAYER_LABELS.get(self.owning_layer, self.owning_layer)})",
            "",
            "## Confidence",
            self.confidence,
            "",
            "## Simulation trust affects conclusion",
            "Yes" if self.trust_affects_conclusion else "No",
            "",
            "## Where to look",
        ]
        lines.extend(f"- `{p}`" for p in self.where_to_look)
        lines.extend(["", "## Safe repair options"])
        lines.extend(f"- {o}" for o in self.safe_repair_options)
        lines.extend(["", "## Risks of each repair"])
        lines.extend(f"- {r}" for r in self.repair_risks)
        lines.extend(
            [
                "",
                "## Required human decision",
                self.required_human_decision,
                "",
                "## Validation to rerun after repair",
            ]
        )
        lines.extend(f"- `{c}`" for c in self.validation_after_repair)
        return "\n".join(lines) + "\n"


def _trust_affects(finding: Finding, metrics: dict[str, Any]) -> bool:
    if finding.layer == "UNDETERMINED":
        return True
    if not metrics.get("simulator_trustworthy", False):
        return finding.layer in ("ADVENTURE", "DELIVERY_ADAPTER", "PLAYER_PACKAGE")
    return False


def _templates() -> dict[str, dict[str, str]]:
    return {
        "SIM-TRUST-DOWNGRADE": {
            "plain_problem": "The simulator reported numbers, but adapter ambiguities or partial support mean those numbers are not fully trusted.",
            "why_it_matters": "You might chase adventure bugs that are actually simulator modeling gaps.",
            "actual_behavior": "Monte Carlo metrics are marked untrusted; adventure-blaming findings are downgraded.",
            "likely_root_cause": "Documented ambiguities in sim_adapter.json or partial mechanic support.",
            "required_human_decision": "Resolve adapter ambiguities or accept qualitative-only review until fixed.",
        },
        "SIM-FAKE": {
            "plain_problem": "A choice or node looks like a low-value retry loop with little story impact.",
            "why_it_matters": "Players may waste time on options that do not advance the case.",
            "actual_behavior": "The node is flagged as fake or duplicate-target hub choice.",
            "likely_root_cause": "Intentional filler choice or adapter marking.",
            "required_human_decision": "Confirm in playtest whether the choice should stay, be trimmed, or be relabeled.",
        },
        "SIM-NO-WIN": {
            "plain_problem": "No simulated runs reached the correct ending even though the simulator passed its own checks.",
            "why_it_matters": "Players may not be able to win on legal paths, or strategies are too weak.",
            "actual_behavior": "Zero wins in the batch with trusted simulator.",
            "likely_root_cause": "Proof requirements too tight, time too short, or strategy bias.",
            "required_human_decision": "Playtest a full cooperative run before changing proof rules.",
        },
        "VAL-": {
            "plain_problem": "Static validation found a structural problem in the adventure package.",
            "why_it_matters": "Broken links or missing nodes can block play entirely.",
            "actual_behavior": "Validator reported the issue before simulation.",
            "likely_root_cause": "Adapter or player text drift from logic.",
            "required_human_decision": "Fix the cited file or confirm the adapter is authoritative.",
        },
    }


def explain_finding(
    finding: Finding,
    metrics: dict[str, Any],
    adapter: dict[str, Any] | None = None,
) -> FindingExplanation:
    adapter = adapter or {}
    tpl = _templates()
    prefix = finding.id.split("-")[0] if "-" in finding.id else finding.id
    base = {}
    for key, val in tpl.items():
        if finding.id.startswith(key.rstrip("-")) or finding.id.startswith(key):
            base = val
            break

    layer = finding.layer
    trust = _trust_affects(finding, metrics)
    if trust and layer == "ADVENTURE":
        layer = "UNDETERMINED"

    where = [finding.file]
    if finding.identifier:
        where.append(f"identifier: {finding.identifier}")

    node_spec = adapter.get("nodes", {}).get(finding.identifier, {})
    if node_spec:
        where.append(f"sim_adapter.json nodes.{finding.identifier}")

    repairs = []
    risks = []
    if finding.auto_fix_possible and finding.layer == "SIMULATOR":
        repairs.append("Fix simulator code in the cited file.")
        risks.append("May mask a real adventure defect if the test was wrong.")
    elif finding.layer in ("ADVENTURE", "DELIVERY_ADAPTER", "PLAYER_PACKAGE", "UNDETERMINED"):
        repairs.append("Review cited file and update adapter or player text after human approval.")
        risks.append("May change pacing, difficulty, or fair-play if done without playtest.")
    else:
        repairs.append("Review evidence and confirm layer ownership before any edit.")
        risks.append("Changing the wrong layer wastes time and can break fair play.")

    validation = [
        "python3 idne_sim.py validate adventures/CASE_BENCHMARK_v0.4",
        "python3 idne_sim.py simulate adventures/CASE_BENCHMARK_v0.4 --runs 200 --seed 42",
    ]
    if finding.id.startswith("SIM-"):
        validation.append(f"python3 idne_sim.py explain <output_folder> --finding {finding.id}")

    return FindingExplanation(
        finding_id=finding.id,
        plain_problem=base.get("plain_problem", f"The simulator found: {finding.evidence}"),
        why_it_matters=base.get(
            "why_it_matters",
            "This can change whether players can finish fairly or trust reported metrics.",
        ),
        evidence=finding.evidence,
        expected_rule=finding.expected_rule,
        actual_behavior=base.get("actual_behavior", finding.evidence),
        likely_root_cause=base.get("likely_root_cause", f"See {finding.file} and {finding.identifier}"),
        owning_layer=layer,
        confidence="low" if trust and finding.confidence != "high" else finding.confidence,
        trust_affects_conclusion=trust,
        where_to_look=where,
        safe_repair_options=repairs,
        repair_risks=risks,
        required_human_decision=base.get(
            "required_human_decision",
            "Approve any gameplay or engine change after reading this report.",
        ),
        validation_after_repair=validation,
    )


def explain_all(
    findings: list[Finding],
    metrics: dict[str, Any],
    adapter: dict[str, Any] | None = None,
) -> list[FindingExplanation]:
    return [explain_finding(f, metrics, adapter) for f in findings]


def load_run_context(output_folder: Path) -> tuple[list[Finding], dict[str, Any], dict[str, Any]]:
    findings_path = output_folder / "findings.json"
    metrics_path = output_folder / "metrics.json"
    if not findings_path.exists():
        raise FileNotFoundError(f"No findings.json in {output_folder}")
    raw_findings = json.loads(findings_path.read_text(encoding="utf-8"))
    findings = [
        Finding(
            id=f["id"],
            severity=f["severity"],
            confidence=f["confidence"],
            evidence=f["evidence"],
            file=f["file"],
            identifier=f["identifier"],
            expected_rule=f["expected_rule"],
            layer=f["layer"],
            auto_fix_possible=f["auto_fix_possible"],
            human_approval_required=f["human_approval_required"],
            extra={k: v for k, v in f.items() if k not in {
                "id", "severity", "confidence", "evidence", "file", "identifier",
                "expected_rule", "layer", "auto_fix_possible", "human_approval_required",
            }},
        )
        for f in raw_findings
    ]
    metrics = json.loads(metrics_path.read_text(encoding="utf-8")) if metrics_path.exists() else {}
    adapter = metrics.get("adapter_snapshot", {})
    return findings, metrics, adapter


def write_explanations(
    output_folder: Path,
    explanations: list[FindingExplanation],
    finding_filter: str | None = None,
) -> Path:
    expl_dir = output_folder / "explanations"
    expl_dir.mkdir(parents=True, exist_ok=True)
    selected = explanations
    if finding_filter:
        selected = [e for e in explanations if e.finding_id == finding_filter]
    for expl in selected:
        (expl_dir / f"{expl.finding_id}.md").write_text(expl.to_markdown(), encoding="utf-8")
        (expl_dir / f"{expl.finding_id}.json").write_text(
            json.dumps(expl.to_dict(), indent=2), encoding="utf-8"
        )
    return expl_dir
