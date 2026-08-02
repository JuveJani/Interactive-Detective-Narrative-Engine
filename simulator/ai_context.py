"""Compact offline AI handoff packages per finding."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from simulator.explainer import FindingExplanation
from simulator.models import Finding
from simulator.repair_advisor import RepairOption

ENGINE_RULE_SNIPPETS = {
    "deadline": "Play MUST end when in-fiction clock reaches the deadline (E-904 timeout).",
    "hub_cost": "Hub travel cost is charged once per hub choice under hub_authoritative policy.",
    "split": "Split paths run in parallel; wall time is max(role windows) plus regroup overhead.",
    "infer": "Inference nodes require proof state before advancing; incomplete infer may return to hub.",
    "follow_up": "Follow-up phone slots are limited per case (follow_up_max).",
    "fair_play": "Correct conclusion must be reachable from information obtainable in play.",
}


def _relevant_rules(finding: Finding) -> list[str]:
    rules = [ENGINE_RULE_SNIPPETS["fair_play"]]
    fid = finding.id
    if "DEADLINE" in fid or "904" in finding.evidence:
        rules.append(ENGINE_RULE_SNIPPETS["deadline"])
    if "HUB" in fid or "FAKE" in fid:
        rules.append(ENGINE_RULE_SNIPPETS["hub_cost"])
    if "SPLIT" in fid or "SOLO" in fid:
        rules.append(ENGINE_RULE_SNIPPETS["split"])
    if "INFER" in fid or finding.identifier.startswith("I-"):
        rules.append(ENGINE_RULE_SNIPPETS["infer"])
    if "FOLLOW" in fid:
        rules.append(ENGINE_RULE_SNIPPETS["follow_up"])
    return rules


def _node_excerpt(adapter: dict[str, Any], node_id: str) -> dict[str, Any] | None:
    nodes = adapter.get("nodes", {})
    if node_id in nodes:
        return {node_id: nodes[node_id]}
    return None


def build_finding_context(
    finding: Finding,
    explanation: FindingExplanation,
    options: list[RepairOption],
    metrics: dict[str, Any],
    adapter: dict[str, Any],
) -> dict[str, Any]:
    node_excerpt = _node_excerpt(adapter, finding.identifier) or {}
    return {
        "finding_id": finding.id,
        "severity": finding.severity,
        "confidence": explanation.confidence,
        "simulator_trustworthy": metrics.get("simulator_trustworthy", False),
        "trust_blockers": metrics.get("trust_blockers", []),
        "engine_rules": _relevant_rules(finding),
        "explanation": explanation.to_dict(),
        "finding_raw": finding.to_dict(),
        "node_excerpt": node_excerpt,
        "simulator_evidence": {
            "evidence": finding.evidence,
            "ending_distribution": metrics.get("ending_distribution", {}),
            "trust_blockers": metrics.get("trust_blockers", []),
        },
        "repair_options": [o.to_dict() for o in options if o.finding_id == finding.id],
        "validation_commands": explanation.validation_after_repair,
        "do_not_invent": [
            "Do not invent engine rules not listed in engine_rules.",
            "Do not invent story facts or clues not in node_excerpt or evidence.",
            "Distinguish proven simulator output from hypotheses.",
        ],
    }


def write_ai_context(
    output_folder: Path,
    findings: list[Finding],
    explanations: list[FindingExplanation],
    options: list[RepairOption],
    metrics: dict[str, Any],
    adapter: dict[str, Any],
    finding_filter: str | None = None,
) -> Path:
    ctx_dir = output_folder / "local_ai_context"
    ctx_dir.mkdir(parents=True, exist_ok=True)
    expl_by_id = {e.finding_id: e for e in explanations}
    selected = findings
    if finding_filter:
        selected = [f for f in findings if f.id == finding_filter]
    for f in selected:
        expl = expl_by_id.get(f.id)
        if not expl:
            continue
        ctx = build_finding_context(f, expl, options, metrics, adapter)
        (ctx_dir / f"finding_context_{f.id}.json").write_text(
            json.dumps(ctx, indent=2), encoding="utf-8"
        )
        md_lines = [
            f"# AI context: {f.id}",
            "",
            "## Problem (simple)",
            expl.plain_problem,
            "",
            "## Proven facts",
            f"- Evidence: {f.evidence}",
            f"- Simulator trustworthy: {metrics.get('simulator_trustworthy', False)}",
            "",
            "## Hypotheses only",
            f"- Root cause: {expl.likely_root_cause}",
            "",
            "## Engine rules (do not extend)",
        ]
        md_lines.extend(f"- {r}" for r in ctx["engine_rules"])
        md_lines.extend(["", "## Repair options"])
        for o in ctx["repair_options"]:
            md_lines.append(f"- {o['option_id']}: {o['intended_change']}")
        md_lines.extend(["", "## Validation commands"])
        md_lines.extend(f"- `{c}`" for c in ctx["validation_commands"])
        (ctx_dir / f"finding_context_{f.id}.md").write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    return ctx_dir
