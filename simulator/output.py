"""Write simulation output artifacts."""

from __future__ import annotations

import csv
import json
import itertools
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from simulator.models import Finding, RunResult

_OUTPUT_COUNTER = itertools.count()


def make_output_dir(base: Path = Path("simulation_output"), mode: str = "run") -> Path:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
    n = next(_OUTPUT_COUNTER)
    out = base / f"{ts}_{mode}_{n}"
    out.mkdir(parents=True, exist_ok=True)
    return out


def write_findings_md(findings: list[Finding], path: Path) -> None:
    lines = ["# Findings\n"]
    for f in sorted(findings, key=lambda x: (x.severity, x.id)):
        lines.append(f"## {f.id} ({f.severity}, {f.confidence})\n")
        lines.append(f"- **Layer:** {f.layer}")
        lines.append(f"- **File:** `{f.file}`")
        lines.append(f"- **Identifier:** `{f.identifier}`")
        lines.append(f"- **Evidence:** {f.evidence}")
        lines.append(f"- **Expected rule:** {f.expected_rule}")
        lines.append(f"- **Auto-fix possible:** {f.auto_fix_possible}")
        lines.append(f"- **Human approval required:** {f.human_approval_required}\n")
    path.write_text("\n".join(lines), encoding="utf-8")


def write_summary(metrics: dict[str, Any], findings: list[Finding], path: Path, mode: str) -> None:
    crit = sum(1 for f in findings if f.severity == "critical")
    major = sum(1 for f in findings if f.severity == "major")
    lines = [
        "# Simulation Summary\n",
        f"**Mode:** {mode}",
        f"**Runs:** {metrics.get('runs', 0)}",
        f"**Nodes:** {metrics.get('graph', {}).get('node_count', 0)}",
        f"**Edges:** {metrics.get('graph', {}).get('edge_count', 0)}",
        f"**Findings:** {len(findings)} (critical={crit}, major={major})",
        f"**Path diversity:** {metrics.get('path_diversity', 0)}",
        f"**Impactful decisions %:** {metrics.get('impactful_decision_pct', 0)}",
        f"**Simulator precheck OK:** {metrics.get('simulator_precheck_ok', False)}",
        f"**Simulator trustworthy:** {metrics.get('simulator_trustworthy', False)}",
        f"**Fiction minutes avg:** {metrics.get('fiction_minutes_avg', metrics.get('avg_wall_minutes', 0))}",
        "\n## Ending distribution\n",
    ]
    for k, v in sorted(metrics.get("ending_distribution", {}).items()):
        lines.append(f"- {k}: {v}")
    path.write_text("\n".join(lines), encoding="utf-8")


def write_csv_graph(edges: list[Any], path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["source", "target", "label", "minutes", "role"])
        for e in edges:
            w.writerow([e.source, e.target, e.label, e.minutes, e.role or ""])


def write_paths_csv(runs: list[RunResult], path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["seed", "strategy", "ending", "steps", "fiction_minutes", "clues", "path"])
        for r in runs:
            fm = getattr(r, "fiction_minutes", r.wall_minutes)
            w.writerow([r.seed, r.strategy, r.ending, r.steps, fm, ";".join(r.clues), "->".join(r.path)])


def write_endings_csv(runs: list[RunResult], path: Path) -> None:
    from collections import Counter

    c = Counter(r.ending for r in runs)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["ending", "count", "rate"])
        for ending, count in sorted(c.items()):
            w.writerow([ending, count, count / max(len(runs), 1)])


def write_clues_csv(adapter: dict[str, Any], path: Path) -> None:
    grants: dict[str, list[str]] = {}
    for nid, spec in adapter.get("nodes", {}).items():
        for c in spec.get("clues", []):
            grants.setdefault(c, []).append(nid)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["clue", "sources", "source_count"])
        for clue in sorted(grants):
            w.writerow([clue, ";".join(grants[clue]), len(grants[clue])])


def write_all_outputs(
    out_dir: Path,
    findings: list[Finding],
    metrics: dict[str, Any],
    runs: list[RunResult],
    adapter: dict[str, Any],
    edges: list[Any],
    mode: str,
    log_lines: list[str],
    trace: dict[str, Any] | None = None,
    parse_errors: list[str] | None = None,
) -> Path:
    write_summary(metrics, findings, out_dir / "summary.md", mode)
    write_findings_md(findings, out_dir / "findings.md")
    (out_dir / "findings.json").write_text(
        json.dumps([f.to_dict() for f in findings], indent=2), encoding="utf-8"
    )
    (out_dir / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    write_csv_graph(edges, out_dir / "graph.csv")
    write_paths_csv(runs, out_dir / "paths.csv")
    write_endings_csv(runs, out_dir / "endings.csv")
    write_clues_csv(adapter, out_dir / "clues.csv")
    _write_split_balance(runs, out_dir / "split_balance.csv")
    _write_time_analysis(runs, out_dir / "time_analysis.csv")
    _write_state_register(adapter, out_dir / "state_register.csv")
    (out_dir / "simulator_log.txt").write_text("\n".join(log_lines), encoding="utf-8")
    pe = parse_errors or []
    (out_dir / "parse_errors.md").write_text(
        "# Parse errors\n\n" + ("\n".join(f"- {e}" for e in pe) if pe else "None."),
        encoding="utf-8",
    )
    if trace:
        seed = trace.get("seed", 0)
        (out_dir / f"trace_{seed}.json").write_text(json.dumps(trace, indent=2), encoding="utf-8")
    return out_dir


def _write_split_balance(runs: list[RunResult], path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["seed", "strategy", "people_min", "records_min", "delta", "wall_min"])
        for r in runs:
            for seg in getattr(r, "split_segments", []) or []:
                p, rec = seg.get("people_minutes", 0), seg.get("records_minutes", 0)
                w.writerow([r.seed, r.strategy, p, rec, abs(p - rec), seg.get("wall_minutes", 0)])


def _write_time_analysis(runs: list[RunResult], path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["seed", "strategy", "fiction_minutes", "ending"])
        for r in runs:
            fm = getattr(r, "fiction_minutes", r.wall_minutes)
            w.writerow([r.seed, r.strategy, fm, r.ending])


def _write_state_register(adapter: dict[str, Any], path: Path) -> None:
    writers: dict[str, list[str]] = {}
    readers: dict[str, list[str]] = {}
    for th in adapter.get("thresholds", []):
        readers.setdefault(th["id"], []).append("clock")
    for nid, spec in adapter.get("nodes", {}).items():
        for fl in spec.get("flags", []):
            writers.setdefault(fl, []).append(nid)
        gate = spec.get("gate", {})
        if gate.get("requires_flag"):
            readers.setdefault(gate["requires_flag"], []).append(nid)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["state", "writers", "readers"])
        keys = sorted(set(writers) | set(readers))
        for k in keys:
            w.writerow([k, ";".join(writers.get(k, [])), ";".join(readers.get(k, []))])
