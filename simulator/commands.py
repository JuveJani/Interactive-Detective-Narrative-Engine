"""CLI commands for explain, repair-plan, and AI context export."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from simulator.advisory_output import write_advisory_outputs
from simulator.ai_context import write_ai_context
from simulator.explainer import explain_all, load_run_context, write_explanations
from simulator.loader import load_adventure
from simulator.repair_advisor import all_repair_options, write_proposed_patch
from simulator.repair_plan import ensure_global_backlog, write_finding_repair_plan


def _resolve_output_folder(path: str) -> Path:
    out = Path(path).resolve()
    if not out.is_dir():
        raise FileNotFoundError(f"Output folder not found: {out}")
    if not (out / "findings.json").exists():
        raise FileNotFoundError(f"No findings.json in {out}")
    return out


def _load_adapter_for_run(output_folder: Path, metrics: dict[str, Any]) -> dict[str, Any]:
    snap = metrics.get("adapter_snapshot")
    if snap:
        return snap
    adv = metrics.get("adventure_path", "adventures/CASE_BENCHMARK_v0.4")
    if Path(adv).exists():
        return load_adventure(adv)["adapter"]
    return {}


def cmd_explain(output_folder: str, finding_id: str | None = None) -> Path:
    out = _resolve_output_folder(output_folder)
    findings, metrics, adapter = load_run_context(out)
    if not adapter:
        adapter = _load_adapter_for_run(out, metrics)
    explanations = explain_all(findings, metrics, adapter)
    write_explanations(out, explanations, finding_id)
    write_advisory_outputs(out, findings, metrics, adapter)
    return out / "explanations"


def cmd_repair_plan(output_folder: str, finding_id: str | None = None) -> Path:
    out = _resolve_output_folder(output_folder)
    findings, metrics, adapter = load_run_context(out)
    if not adapter:
        adapter = _load_adapter_for_run(out, metrics)
    explanations = explain_all(findings, metrics, adapter)
    all_options = all_repair_options(findings, explanations)
    ensure_global_backlog(out, all_options, findings)

    if finding_id:
        fopts = [o for o in all_options if o.finding_id == finding_id]
        expl = next((e for e in explanations if e.finding_id == finding_id), None)
        if expl:
            write_finding_repair_plan(out, finding_id, fopts, expl)
            if fopts:
                write_proposed_patch(out, fopts[0], expl)
        return out

    write_advisory_outputs(out, findings, metrics, adapter, all_options)
    return out


def cmd_export_ai_context(output_folder: str, finding_id: str | None = None) -> Path:
    out = _resolve_output_folder(output_folder)
    findings, metrics, adapter = load_run_context(out)
    if not adapter:
        adapter = _load_adapter_for_run(out, metrics)
    explanations = explain_all(findings, metrics, adapter)
    options = all_repair_options(findings, explanations)
    return write_ai_context(out, findings, explanations, options, metrics, adapter, finding_id)
