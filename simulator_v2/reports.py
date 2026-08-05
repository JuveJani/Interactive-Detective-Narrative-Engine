"""Report generation for Simulator v2 diagnostics."""

from __future__ import annotations

import csv
import itertools
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from simulator_v2.atomic_io import atomic_write_json, atomic_write_text
from simulator_v2.diagnostics import DiagnosticReport
from simulator_v2.explainer import explain_all
from simulator_v2.findings import DiagnosticFinding
from simulator_v2.repair_advisor import build_repair_backlog, repair_options_for_finding

_OUTPUT_COUNTER = itertools.count()


def make_output_dir(base: Path = Path("simulation_output_v2"), mode: str = "diagnose") -> Path:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
    n = next(_OUTPUT_COUNTER)
    out = base / f"{ts}_{mode}_{n}"
    out.mkdir(parents=True, exist_ok=True)
    return out


def _executive_diagnostic(report: DiagnosticReport, explanations: list) -> str:
    trusted = report.trust.get("trusted", False)
    critical = [f for f in report.findings if f.severity == "critical"]
    lines = [
        "# Executive diagnostic",
        "",
        f"**Adventure:** {report.adventure_id}",
        f"**Play mode:** {report.play_mode}",
        f"**Integrated validation:** {report.integrated_validation.get('status')}",
        f"**Quantitative trust:** {'yes' if trusted else 'no'}",
        "",
        "## Critical findings",
    ]
    if critical:
        lines.extend(f"- **{f.finding_id}** ({f.severity}): {f.observed_behavior}" for f in critical)
    else:
        lines.append("- None")
    lines.extend(["", "## Trust blockers"])
    blockers = report.trust.get("blockers", [])
    lines.extend(f"- {b}" for b in blockers) if blockers else lines.append("- None")
    lines.extend(["", "## Simulation summary"])
    mc = report.simulation.get("monte_carlo", {})
    if mc:
        lines.append(f"- Monte Carlo endings: {mc.get('ending_frequencies', {})}")
    ex = report.simulation.get("exhaustive", {})
    if ex:
        lines.append(f"- Exhaustive: {ex.get('status')} ({ex.get('states_explored', 0)} states)")
    return "\n".join(lines) + "\n"


def _findings_md(findings: list[DiagnosticFinding]) -> str:
    lines = ["# Findings", ""]
    for f in sorted(findings, key=lambda x: (x.severity, x.finding_id)):
        lines.extend([
            f"## {f.finding_id} ({f.severity}, {f.confidence})",
            f"- **Validator:** {f.validator}",
            f"- **Owner:** {f.likely_owner}",
            f"- **Source:** `{f.source_file}` / `{f.canonical_source}`",
            f"- **Entity:** {f.affected_entity}",
            f"- **Expected:** {f.expected_behavior}",
            f"- **Observed:** {f.observed_behavior}",
            f"- **Evidence:** {f.simulation_evidence}",
            f"- **Trust impact:** {f.trust_impact}",
            f"- **Repair eligible:** {f.repair_eligible}",
            f"- **Human approval:** {f.human_approval_required}",
            "",
        ])
    return "\n".join(lines)


def _human_playtest_questions(explanations: list) -> str:
    lines = ["# Human playtest questions", ""]
    for e in explanations:
        if e.owning_layer in ("GENERATOR", "UNDETERMINED", "PACKAGE"):
            lines.extend([
                f"## {e.finding_id}",
                f"- Did players encounter: {e.plain_problem}?",
                f"- Does this matter at your table: {e.why_it_matters}?",
                "",
            ])
    return "\n".join(lines) if len(lines) > 2 else "# Human playtest questions\n\nNo playtest prompts for this run.\n"


def _parse_errors_md(errors: list[str]) -> str:
    if not errors:
        return "# Parse errors\n\nNo parse errors.\n"
    lines = ["# Parse errors", ""]
    lines.extend(f"- {e}" for e in errors)
    return "\n".join(lines) + "\n"


def _write_strategy_comparison_csv(path: Path, compare: dict[str, Any]) -> None:
    strategies = compare.get("strategies", {})
    endings: set[str] = set()
    for freq in strategies.values():
        endings.update(freq.keys())
    endings_sorted = sorted(endings)
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["strategy"] + endings_sorted)
        for name, freq in sorted(strategies.items()):
            w.writerow([name] + [freq.get(e, 0) for e in endings_sorted])


def _write_endings_csv(path: Path, mc: dict[str, Any]) -> None:
    freq = mc.get("ending_frequencies", {})
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["ending_id", "count"])
        for eid, count in sorted(freq.items()):
            w.writerow([eid, count])


def _write_paths_csv(path: Path, trace: dict[str, Any]) -> None:
    path_list = trace.get("path", [])
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["step", "action_id"])
        for i, act in enumerate(path_list):
            w.writerow([i + 1, act])


def _write_time_analysis_csv(path: Path, metrics: dict[str, Any], trace: dict[str, Any]) -> None:
    m = trace.get("metrics", {})
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["metric", "value"])
        w.writerow(["in_world_minutes", m.get("in_world_minutes", metrics.get("in_world_minutes", 0))])
        w.writerow(["player_active_minutes", m.get("player_active_minutes", 0)])
        w.writerow(["wall_clock_minutes", m.get("wall_clock_minutes", 0)])
        w.writerow(["session_minutes", m.get("session_minutes", 0)])
        w.writerow(["waiting_minutes", m.get("waiting_minutes", 0)])
        w.writerow(["steps", m.get("steps", metrics.get("trace_steps", 0))])


def _write_state_transitions_csv(path: Path, trace: dict[str, Any]) -> None:
    path_list = trace.get("path", [])
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["step", "action_id", "kind_guess"])
        for i, act in enumerate(path_list):
            kind = act.split(":", 1)[0] if ":" in act else "unknown"
            w.writerow([i + 1, act, kind])


def write_all_reports(output_dir: Path, report: DiagnosticReport) -> None:
    explanations = explain_all(report.findings, report.trust)

    atomic_write_text(output_dir / "executive_diagnostic.md", _executive_diagnostic(report, explanations))
    atomic_write_text(output_dir / "findings.md", _findings_md(report.findings))
    atomic_write_json(output_dir / "findings.json", report.to_dict())
    atomic_write_json(output_dir / "metrics.json", report.metrics)
    atomic_write_text(output_dir / "repair_backlog.md", build_repair_backlog(report.findings, explanations))
    atomic_write_text(output_dir / "human_playtest_questions.md", _human_playtest_questions(explanations))
    atomic_write_text(output_dir / "simulator_log.txt", "\n".join(report.log) + "\n")
    atomic_write_text(output_dir / "parse_errors.md", _parse_errors_md(report.parse_errors))

    sim = report.simulation
    if sim.get("compare"):
        _write_strategy_comparison_csv(output_dir / "strategy_comparison.csv", sim["compare"])
    if sim.get("monte_carlo"):
        _write_endings_csv(output_dir / "endings.csv", sim["monte_carlo"])
    if sim.get("trace"):
        _write_paths_csv(output_dir / "paths.csv", sim["trace"])
        _write_time_analysis_csv(output_dir / "time_analysis.csv", report.metrics, sim["trace"])
        _write_state_transitions_csv(output_dir / "state_transitions.csv", sim["trace"])

    explain_dir = output_dir / "explanations"
    explain_dir.mkdir(exist_ok=True)
    for exp in explanations:
        atomic_write_text(explain_dir / f"{exp.finding_id}.md", exp.to_markdown())

    repair_dir = output_dir / "repair_options"
    repair_dir.mkdir(exist_ok=True)
    for f, exp in zip(report.findings, explanations):
        opts = repair_options_for_finding(f, exp)
        if opts:
            atomic_write_json(repair_dir / f"{f.finding_id}.json", [o.to_dict() for o in opts])

    atomic_write_json(output_dir / "run_manifest.json", {
        "adventure_id": report.adventure_id,
        "play_mode": report.play_mode,
        "trust": report.trust,
        "finding_count": len(report.findings),
        "output_files": sorted(p.name for p in output_dir.iterdir() if p.is_file()),
    })
