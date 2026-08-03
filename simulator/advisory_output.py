"""Executive and layer-split diagnostic reports."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from simulator.atomic_io import atomic_write_json, atomic_write_text
from simulator.explainer import FindingExplanation, explain_all, _is_proven_fact
from simulator.models import Finding
from simulator.repair_advisor import RepairOption, all_repair_options, build_repair_backlog


def _layer_md(layer: str, explanations: list[FindingExplanation]) -> str:
    items = [e for e in explanations if e.owning_layer == layer]
    lines = [f"# {layer} findings", ""]
    if not items:
        lines.append("No findings in this layer.")
        return "\n".join(lines) + "\n"
    for e in items:
        lines.append(f"## {e.finding_id}")
        lines.append(e.plain_problem)
        lines.append(f"- Confidence: {e.confidence}")
        lines.append(f"- Trust affects conclusion: {e.trust_affects_conclusion}")
        lines.append("")
    return "\n".join(lines)


def _executive_diagnostic(
    findings: list[Finding],
    explanations: list[FindingExplanation],
    metrics: dict[str, Any],
) -> str:
    trustworthy = metrics.get("simulator_trustworthy", False)
    critical = [f for f in findings if f.severity == "critical"]
    by_id = {f.id: f for f in findings}
    proven = [e for e in explanations if _is_proven_fact(by_id[e.finding_id], metrics)]
    suspected = [e for e in explanations if e not in proven]
    layers: dict[str, int] = {}
    for e in explanations:
        layers[e.owning_layer] = layers.get(e.owning_layer, 0) + 1
    fix_first = sorted(
        findings,
        key=lambda f: {"critical": 0, "major": 1, "minor": 2, "info": 3}.get(f.severity, 9),
    )[:5]
    do_not_change = [
        "IDNE engine specification (no engine change for one adventure unless engine rule violated).",
    ]
    if not trustworthy:
        do_not_change.insert(0, "Adventure proof rules, thresholds, and balance numbers from this run.")
    untrustworthy = list(metrics.get("trust_blockers", []))
    if not trustworthy:
        untrustworthy.append("All Monte Carlo ending rates and fiction-minute averages")
    manual = [
        "Run one full two-player cooperative session on paper.",
        "Confirm hub revisit and deadline feel fair at the table.",
        "Verify accusation flow after all three proof tags are obtainable.",
    ]

    lines = [
        "# Executive diagnostic",
        "",
        "## Quantitative trust status",
        "",
        f"- **Qualitative diagnosis available:** yes",
        f"- **Repair planning scope:** suggestions only; no automatic file edits",
        f"- **Quantitative results trusted:** {'yes' if trustworthy else 'no'}",
    ]
    if not trustworthy:
        lines.append("- **Exact blockers preventing trust:**")
        for b in metrics.get("trust_blockers", []):
            lines.append(f"  - {b}")
    lines.extend(["", "## 1. What is broken?", ""])
    if critical:
        lines.extend(f"- **{f.id}** ({f.severity}): {f.evidence}" for f in critical)
    else:
        lines.append("- No critical findings. Review major and minor items below.")
    lines.extend(["", "## 2. What is proven?", ""])
    if proven:
        lines.extend(f"- {e.finding_id}: {e.evidence}" for e in proven[:12])
    else:
        lines.append("- No proven findings in this batch.")
    lines.extend(["", "## 3. What is only suspected?", ""])
    if suspected:
        lines.extend(f"- {e.finding_id}: {e.likely_root_cause}" for e in suspected[:12])
    else:
        lines.append("- No suspected-only items.")
    lines.extend(["", "## 4. Which layer owns it?", ""])
    for layer, count in sorted(layers.items()):
        lines.append(f"- {layer}: {count} finding(s)")
    lines.extend(["", "## 5. What should be fixed first?", ""])
    for f in fix_first:
        lines.append(f"- {f.id} ({f.severity}) — {f.file}")
    lines.extend(["", "## 6. What must not be changed yet?", ""])
    lines.extend(f"- {x}" for x in do_not_change)
    lines.extend(["", "## 7. Which data is untrustworthy?", ""])
    if untrustworthy:
        lines.extend(f"- {u}" for u in untrustworthy)
    else:
        lines.append("- Simulator marked trustworthy for this run.")
    lines.extend(["", "## 8. What should the human test manually?", ""])
    lines.extend(f"- {m}" for m in manual)
    return "\n".join(lines) + "\n"


def _human_playtest_questions(explanations: list[FindingExplanation]) -> str:
    lines = [
        "# Human playtest questions",
        "",
        "Use these during a live session. Do not read simulator conclusions aloud to players.",
        "",
    ]
    for e in explanations:
        if e.finding_id.startswith("SIM-FAKE") or e.owning_layer in ("ADVENTURE", "UNDETERMINED", "HUMAN_PLAYTEST"):
            lines.append(f"## {e.finding_id}")
            lines.append(f"- Did players encounter: {e.plain_problem}?")
            lines.append(f"- Does this matter at your table: {e.why_it_matters}?")
            lines.append("")
    return "\n".join(lines)


def write_advisory_outputs(
    out_dir: Path,
    findings: list[Finding],
    metrics: dict[str, Any],
    adapter: dict[str, Any],
    options: list[RepairOption] | None = None,
) -> None:
    explanations = explain_all(findings, metrics, adapter)
    if options is None:
        options = all_repair_options(findings, explanations)

    atomic_write_text(out_dir / "executive_diagnostic.md", _executive_diagnostic(findings, explanations, metrics))
    atomic_write_text(out_dir / "repair_backlog.md", build_repair_backlog(options, findings))
    atomic_write_json(out_dir / "repair_options.json", [o.to_dict() for o in options])
    atomic_write_text(out_dir / "engine_findings.md", _layer_md("ENGINE", explanations))
    atomic_write_text(
        out_dir / "adventure_findings.md",
        _layer_md("ADVENTURE", explanations) + _layer_md("UNDETERMINED", explanations),
    )
    atomic_write_text(out_dir / "delivery_findings.md", _layer_md("DELIVERY_ADAPTER", explanations))
    atomic_write_text(out_dir / "simulator_findings.md", _layer_md("SIMULATOR", explanations))
    atomic_write_text(out_dir / "human_playtest_questions.md", _human_playtest_questions(explanations))

    expl_dir = out_dir / "explanations"
    expl_dir.mkdir(exist_ok=True)
    for e in explanations:
        atomic_write_text(expl_dir / f"{e.finding_id}.md", e.to_markdown())
