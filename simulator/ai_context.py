"""Compact offline AI handoff packages per finding."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from simulator.atomic_io import atomic_write_json, atomic_write_text
from simulator.explainer import FindingExplanation
from simulator.follow_ups import follow_up_actions, legacy_keyword_follow_ups
from simulator.models import Finding
from simulator.repair_advisor import RepairOption

ENGINE_RULE_SNIPPETS = {
    "deadline": "Play MUST end when in-fiction clock reaches the deadline (timeout ending E-904).",
    "hub_cost": "Hub travel cost is charged once per hub choice under hub_authoritative policy.",
    "split": "Split paths run in parallel; wall time is max(role windows) plus regroup overhead.",
    "infer": "Inference nodes require proof state before advancing; incomplete infer may return to hub.",
    "follow_up": "Follow-up phone slots are limited per case (follow_up_max). Only follow_up_actions are simulated.",
    "fair_play": "Correct conclusion must be reachable from information obtainable in play.",
}


def _relevant_rules(finding: Finding) -> list[str]:
    rules = [ENGINE_RULE_SNIPPETS["fair_play"]]
    fid = finding.id
    if "DEADLINE" in fid or "904" in finding.evidence or "TRUST" in fid:
        rules.append(ENGINE_RULE_SNIPPETS["deadline"])
    if "HUB" in fid or "FAKE" in fid:
        rules.append(ENGINE_RULE_SNIPPETS["hub_cost"])
    if "SPLIT" in fid or "SOLO" in fid:
        rules.append(ENGINE_RULE_SNIPPETS["split"])
    if "INFER" in fid or finding.identifier.startswith("I-"):
        rules.append(ENGINE_RULE_SNIPPETS["infer"])
    if "FOLLOW" in fid or "TRUST" in fid:
        rules.append(ENGINE_RULE_SNIPPETS["follow_up"])
    return rules


def _node_excerpt(adapter: dict[str, Any], node_id: str) -> dict[str, Any]:
    nodes = adapter.get("nodes", {})
    if node_id in nodes:
        return {node_id: nodes[node_id]}
    return {}


def _trust_context(adapter: dict[str, Any]) -> dict[str, Any]:
    return {
        "ambiguities": list(adapter.get("ambiguities", [])),
        "simulator_partial": list(adapter.get("simulator_partial", [])),
        "simulator_unsupported": list(adapter.get("simulator_unsupported", [])),
        "follow_up_actions": follow_up_actions(adapter),
        "legacy_follow_ups_not_simulated": legacy_keyword_follow_ups(adapter),
        "p112_node": _node_excerpt(adapter, "P-112"),
    }


def build_finding_context(
    finding: Finding,
    explanation: FindingExplanation,
    options: list[RepairOption],
    metrics: dict[str, Any],
    adapter: dict[str, Any],
) -> dict[str, Any]:
    trustworthy = metrics.get("simulator_trustworthy", False)
    node_excerpt = _node_excerpt(adapter, finding.identifier)
    if finding.id == "SIM-TRUST-DOWNGRADE" or finding.identifier == "ambiguities":
        node_excerpt = _trust_context(adapter)

    proven_facts = [
        f"Finding ID: {finding.id}",
        f"Severity: {finding.severity}",
        f"Evidence from simulator: {finding.evidence}",
        f"simulator_trustworthy: {trustworthy}",
    ]
    if not trustworthy:
        proven_facts.append("Quantitative ending rates are NOT facts about the adventure.")
    for blocker in metrics.get("trust_blockers", []):
        proven_facts.append(f"Trust blocker: {blocker}")

    simulation_observations = []
    if metrics.get("ending_distribution") and not trustworthy:
        simulation_observations.append(
            "Ending counts below are UNTRUSTED simulation observations only: "
            + str(metrics.get("ending_distribution"))
        )
    elif metrics.get("ending_distribution") and trustworthy:
        simulation_observations.append(
            "Ending distribution (trusted simulation): " + str(metrics.get("ending_distribution"))
        )
    if metrics.get("fiction_minutes_avg") is not None:
        simulation_observations.append(
            f"Average fiction minutes: {metrics.get('fiction_minutes_avg')} "
            f"({'untrusted' if not trustworthy else 'trusted'})"
        )

    ambiguities = list(adapter.get("ambiguities", [])) if finding.id.startswith("SIM-TRUST") else []
    if finding.identifier in adapter.get("nodes", {}):
        ambiguities.extend(adapter.get("simulator_partial", []))

    hypotheses = [explanation.likely_root_cause]
    if finding.extra.get("possible_adventure_issue"):
        hypotheses.append("This might be an adventure issue, but that is not proven while untrusted.")

    forbidden = [
        "Do not treat untrusted Monte Carlo rates as proof about adventure balance.",
        "Do not invent engine rules not listed under engine_rules.",
        "Do not invent story facts or clues not in node_excerpt or proven_facts.",
        "Do not recommend engine changes for one adventure unless an engine rule is clearly violated.",
    ]
    if not trustworthy:
        forbidden.append("Do not assign layer ADVENTURE for quantitative conclusions.")

    return {
        "finding_id": finding.id,
        "PROVEN_FACTS": proven_facts,
        "SIMULATION_OBSERVATIONS": simulation_observations,
        "AMBIGUITIES": ambiguities,
        "HYPOTHESES": hypotheses,
        "FORBIDDEN_CONCLUSIONS": forbidden,
        "SAFE_REPAIR_OPTIONS": [o.to_dict() for o in options if o.finding_id == finding.id],
        "REQUIRED_HUMAN_DECISIONS": [explanation.required_human_decision],
        "engine_rules": _relevant_rules(finding),
        "node_excerpt": node_excerpt,
        "validation_commands": explanation.validation_after_repair,
        "explanation": explanation.to_dict(),
        "finding_raw": finding.to_dict(),
    }


def _context_markdown(ctx: dict[str, Any]) -> str:
    lines = [f"# AI context: {ctx['finding_id']}", ""]
    for section in (
        "PROVEN_FACTS",
        "SIMULATION_OBSERVATIONS",
        "AMBIGUITIES",
        "HYPOTHESES",
        "FORBIDDEN_CONCLUSIONS",
        "SAFE_REPAIR_OPTIONS",
        "REQUIRED_HUMAN_DECISIONS",
    ):
        lines.append(f"## {section.replace('_', ' ')}")
        val = ctx.get(section, [])
        if isinstance(val, list):
            for item in val:
                if isinstance(item, dict):
                    lines.append(f"- {item.get('option_id', item.get('intended_change', item))}")
                else:
                    lines.append(f"- {item}")
        else:
            lines.append(str(val))
        lines.append("")
    lines.append("## Engine rules (do not extend)")
    for r in ctx.get("engine_rules", []):
        lines.append(f"- {r}")
    lines.append("")
    lines.append("## Validation commands")
    for c in ctx.get("validation_commands", []):
        lines.append(f"- `{c}`")
    return "\n".join(lines) + "\n"


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
        atomic_write_json(ctx_dir / f"finding_context_{f.id}.json", ctx)
        atomic_write_text(ctx_dir / f"finding_context_{f.id}.md", _context_markdown(ctx))
    return ctx_dir
