"""Executive and layer-split diagnostic reports."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from simulator.explainer import FindingExplanation, explain_all
from simulator.models import Finding
from simulator.repair_advisor import RepairOption, all_repair_options, build_repair_backlog


LAYER_FILES = {
    "ENGINE": "engine_findings.md",
    "ADVENTURE": "adventure_findings.md",
    "DELIVERY_ADAPTER": "delivery_findings.md",
    "SIMULATOR": "simulator_findings.md",
    "PLAYER_PACKAGE": "delivery_findings.md",
    "VALIDATOR": "simulator_findings.md",
    "UNDETERMINED": "adventure_findings.md",
    "HUMAN_PLAYTEST": "human_playtest_questions.md",
}


def _layer_md(layer: str, explanations: list[FindingExplanation]) -> str:
    items = [e for e in explanations if e.owning_layer == layer or (layer == "UNDETERMINED" and e.trust_affects_conclusion)]
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
    critical = [f for f in findings if f.severity == "critical"]
    proven = [e for e in explanations if not e.trust_affects_conclusion and e.confidence in ("high", "medium")]
    suspected = [e for e in explanations if e.trust_affects_conclusion or e.confidence == "low"]
    layers: dict[str, int] = {}
    for e in explanations:
        layers[e.owning_layer] = layers.get(e.owning_layer, 0) + 1
    fix_first = sorted(
        findings,
        key=lambda f: {"critical": 0, "major": 1, "minor": 2, "info": 3}.get(f.severity, 9),
    )[:5]
    do_not_change = []
    if not metrics.get("simulator_trustworthy", True):
        do_not_change.append("Adventure proof rules and ending thresholds until simulator ambiguities are resolved.")
    do_not_change.append("IDNE engine specification (no engine change for one adventure unless engine rule violated).")
    untrustworthy = metrics.get("trust_blockers", []) + (
        ["Monte Carlo ending rates"] if not metrics.get("simulator_trustworthy") else []
    )
    manual = [
        "Run one full two-player cooperative session on paper.",
        "Confirm hub revisit and deadline feel fair at the table.",
        "Verify accusation flow after all three proof tags are obtainable.",
    ]

    lines = [
        "# Executive diagnostic",
        "",
        "## 1. What is broken?",
        "",
    ]
    if critical:
        lines.extend(f"- **{f.id}** ({f.severity}): {f.evidence}" for f in critical)
    else:
        lines.append("- No critical findings. Review major and minor items below.")
    lines.extend(
        [
            "",
            "## 2. What is proven?",
            "",
        ]
    )
    if proven:
        lines.extend(f"- {e.finding_id}: {e.evidence}" for e in proven[:10])
    else:
        lines.append("- Little is proven while simulator trust is down.")
    lines.extend(["", "## 3. What is only suspected?", ""])
    if suspected:
        lines.extend(f"- {e.finding_id}: {e.likely_root_cause}" for e in suspected[:10])
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

    (out_dir / "executive_diagnostic.md").write_text(
        _executive_diagnostic(findings, explanations, metrics), encoding="utf-8"
    )
    (out_dir / "repair_backlog.md").write_text(build_repair_backlog(options, findings), encoding="utf-8")
    (out_dir / "repair_options.json").write_text(
        json.dumps([o.to_dict() for o in options], indent=2), encoding="utf-8"
    )
    (out_dir / "engine_findings.md").write_text(_layer_md("ENGINE", explanations), encoding="utf-8")
    (out_dir / "adventure_findings.md").write_text(
        _layer_md("ADVENTURE", explanations) + _layer_md("UNDETERMINED", explanations),
        encoding="utf-8",
    )
    (out_dir / "delivery_findings.md").write_text(
        _layer_md("DELIVERY_ADAPTER", explanations), encoding="utf-8"
    )
    (out_dir / "simulator_findings.md").write_text(_layer_md("SIMULATOR", explanations), encoding="utf-8")
    (out_dir / "human_playtest_questions.md").write_text(
        _human_playtest_questions(explanations), encoding="utf-8"
    )

    expl_dir = out_dir / "explanations"
    expl_dir.mkdir(exist_ok=True)
    for e in explanations:
        (expl_dir / f"{e.finding_id}.md").write_text(e.to_markdown(), encoding="utf-8")
