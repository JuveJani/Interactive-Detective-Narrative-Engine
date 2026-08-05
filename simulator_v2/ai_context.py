"""Local-AI context export for Simulator v2 findings."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from simulator_v2.atomic_io import atomic_write_json, atomic_write_text
from simulator_v2.explainer import FindingExplanation, explain_finding
from simulator_v2.findings import DiagnosticFinding
from simulator_v2.repair_advisor import RepairOption, repair_options_for_finding


def _canonical_excerpt(model_packages: dict[str, dict], source_file: str, entity_id: str) -> dict[str, Any]:
    if not source_file or not model_packages:
        return {}
    layer_key = ""
    for key, path in {
        "environment": "DO_NOT_READ/environment_package.json",
        "object_interaction": "DO_NOT_READ/object_interaction_package.json",
        "investigation_core": "DO_NOT_READ/investigation_core_package.json",
        "npc_investigation": "DO_NOT_READ/npc_investigation_package.json",
        "investigation_flow": "DO_NOT_READ/investigation_flow_package.json",
        "capability_check": "DO_NOT_READ/capability_check_package.json",
    }.items():
        if path in source_file or source_file.endswith(path.split("/")[-1]):
            layer_key = key
            break
    pkg = model_packages.get(layer_key, {})
    if not pkg:
        return {"note": "layer not loaded", "source_file": source_file}
    excerpt: dict[str, Any] = {"source_file": source_file, "entity_id": entity_id}
    for collection in ("locations", "objects", "knowledge", "hypotheses", "endings", "checks", "npcs"):
        items = pkg.get(collection, [])
        if isinstance(items, list):
            for item in items:
                iid = item.get(f"{collection[:-1]}_id") or item.get("object_id") or item.get("npc_id") or item.get("knowledge_id")
                if str(iid) == entity_id:
                    excerpt[collection] = [item]
    return excerpt


def build_finding_context(
    finding: DiagnosticFinding,
    explanation: FindingExplanation,
    options: list[RepairOption],
    trust: dict[str, Any],
    metrics: dict[str, Any],
    model_packages: dict[str, dict] | None = None,
) -> dict[str, Any]:
    trusted = trust.get("trusted", False)
    proven_facts = [
        f"Finding ID: {finding.finding_id}",
        f"Severity: {finding.severity}",
        f"Confidence: {finding.confidence}",
        f"Validator: {finding.validator}",
        f"simulator_trustworthy: {trusted}",
        finding.simulation_evidence,
    ]
    if not trusted:
        proven_facts.append("Quantitative simulation rates are NOT proven facts about the adventure.")

    prohibited = [
        "Do not treat untrusted Monte Carlo rates as proof about adventure balance.",
        "Do not invent canonical facts not in excerpts or proven_facts.",
        "Do not recommend engine changes for one adventure unless an engine rule is clearly violated.",
    ]
    if not trusted:
        prohibited.append("Do not assign adventure blame for quantitative conclusions while untrusted.")

    return {
        "finding_id": finding.finding_id,
        "PROVEN_FACTS": proven_facts,
        "RELEVANT_CANONICAL_EXCERPTS": _canonical_excerpt(
            model_packages or {},
            finding.source_file,
            finding.affected_entity or finding.canonical_source,
        ),
        "SIMULATION_EVIDENCE": {
            "evidence": finding.simulation_evidence,
            "metrics_snapshot": {
                k: metrics.get(k)
                for k in ("trace_steps", "trace_ending", "exhaustive_states")
                if k in metrics
            },
        },
        "AMBIGUITIES": trust.get("blockers", []) if not trusted else [],
        "PROHIBITED_CONCLUSIONS": prohibited,
        "SAFE_REPAIR_SCOPE": [o.intended_change for o in options],
        "VALIDATION_COMMANDS": explanation.validation_after_repair,
        "EXPLANATION": explanation.to_dict(),
    }


def export_ai_context(
    output_dir: Path,
    finding_id: str,
    *,
    model_packages: dict[str, dict] | None = None,
) -> Path:
    findings_path = output_dir / "findings.json"
    if not findings_path.exists():
        raise FileNotFoundError(f"findings.json not found in {output_dir}")
    data = json.loads(findings_path.read_text(encoding="utf-8"))
    trust = data.get("trust", {})
    metrics = data.get("metrics", {})
    raw_findings = data.get("findings", [])
    target = None
    for raw in raw_findings:
        if raw.get("finding_id") == finding_id:
            fields = {k: raw[k] for k in DiagnosticFinding.__dataclass_fields__ if k in raw}
            extra = {k: v for k, v in raw.items() if k not in DiagnosticFinding.__dataclass_fields__}
            fields["extra"] = extra
            target = DiagnosticFinding(**fields)
            break
    if not target:
        raise KeyError(f"finding not found: {finding_id}")

    explanation = explain_finding(target, trust)
    options = repair_options_for_finding(target, explanation)
    ctx = build_finding_context(target, explanation, options, trust, metrics, model_packages)

    out_dir = output_dir / "ai_context" / finding_id
    out_dir.mkdir(parents=True, exist_ok=True)
    atomic_write_json(out_dir / "context.json", ctx)
    atomic_write_text(out_dir / "context.md", _context_markdown(ctx))
    atomic_write_text(out_dir / "README.txt", "Offline AI context — do not include whole repository.\n")
    return out_dir


def _context_markdown(ctx: dict[str, Any]) -> str:
    lines = [f"# AI context: {ctx.get('finding_id')}", ""]
    for section in ("PROVEN_FACTS", "PROHIBITED_CONCLUSIONS", "SAFE_REPAIR_SCOPE", "VALIDATION_COMMANDS"):
        lines.append(f"## {section}")
        for item in ctx.get(section, []):
            lines.append(f"- {item}")
        lines.append("")
    return "\n".join(lines)
