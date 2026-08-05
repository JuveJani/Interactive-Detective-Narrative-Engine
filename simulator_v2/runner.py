"""Full diagnostic run orchestration for Simulator v2."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from simulator_v2.config import RunnerConfig
from simulator_v2.diagnostics import DiagnosticReport, build_integration_findings, run_integrated_diagnostics
from simulator_v2.derivation import derive_simulation_model
from simulator_v2.modes import ExhaustiveConfig, MonteCarloConfig, SimulationModes
from simulator_v2.package_loader import load_simulator_package
from simulator_v2.reports import make_output_dir, write_all_reports
from simulator_v2.trust_gate import integrated_validation_status


def _trust_from_simulation(sim_data: dict[str, Any]) -> dict[str, Any]:
    for key in ("trace", "monte_carlo", "compare", "exhaustive", "path_analysis"):
        block = sim_data.get(key)
        if isinstance(block, dict) and block.get("trust"):
            return dict(block["trust"])
        if hasattr(block, "to_dict"):
            td = block.to_dict()
            if td.get("trust"):
                return dict(td["trust"])
    return {}


def _integrated_from_simulation(sim_data: dict[str, Any], load) -> dict[str, Any]:
    for key in ("trace", "monte_carlo", "compare", "exhaustive", "path_analysis"):
        block = sim_data.get(key)
        if isinstance(block, dict) and block.get("integrated_validation"):
            return dict(block["integrated_validation"])
        if hasattr(block, "to_dict"):
            td = block.to_dict()
            if td.get("integrated_validation"):
                return dict(td["integrated_validation"])
    return {
        "status": integrated_validation_status(load),
        "failures": list(load.integrated_validation_failures or []),
    }


def _diagnostic_report(
    load,
    sim_data: dict[str, Any],
    metrics: dict[str, Any],
    log: list[str],
) -> DiagnosticReport:
    model = None
    if load.adventure_root and load.status.value == "READY":
        try:
            model = derive_simulation_model(load.adventure_root, load.play_mode)
        except Exception:
            model = None
    trust = _trust_from_simulation(sim_data)
    integrated = _integrated_from_simulation(sim_data, load)
    findings = build_integration_findings(load, model, sim_data, trust)
    return DiagnosticReport(
        adventure_id=load.adventure_id,
        play_mode=load.play_mode,
        integrated_validation=integrated,
        trust=trust,
        findings=findings,
        metrics=metrics,
        simulation=sim_data,
        log=log,
    )


def cmd_diagnose(package_path: str | Path, config: RunnerConfig | None = None) -> Path:
    cfg = config or RunnerConfig()
    out = make_output_dir(Path(cfg.output_base), mode="diagnose")
    checkpoint = out / "checkpoint_exhaustive.json"
    cancel_flag = [False]
    cancel_file = Path(cfg.cancel_flag_path) if cfg.cancel_flag_path else out / ".cancel"
    if cancel_file.exists():
        cancel_flag[0] = True

    report = run_integrated_diagnostics(
        package_path,
        config=cfg,
        run_simulation=True,
        cancel_flag=cancel_flag,
        checkpoint_path=checkpoint,
        resume=bool(cfg.resume_checkpoint),
    )
    write_all_reports(out, report)
    return out


def cmd_validate(package_path: str | Path, config: RunnerConfig | None = None) -> dict[str, Any]:
    cfg = config or RunnerConfig()
    modes = SimulationModes(str(package_path))
    result = modes.validate()
    if cfg.output_base:
        load = modes.load_result
        report = _diagnostic_report(load, {"validate": result}, {"legal_action_count": result.get("legal_action_count", 0)}, ["validate"])
        out = make_output_dir(Path(cfg.output_base), mode="validate")
        write_all_reports(out, report)
    return result


def cmd_trace(package_path: str | Path, seed: int = 42, strategy: str = "random_legal", config: RunnerConfig | None = None) -> dict[str, Any]:
    cfg = config or RunnerConfig()
    modes = SimulationModes(str(package_path))
    result = modes.trace(strategy, seed=seed)
    out = make_output_dir(Path(cfg.output_base), mode="trace")
    sim_data = {"trace": result.to_dict()}
    report = _diagnostic_report(
        modes.load_result,
        sim_data,
        result.metrics.to_dict(),
        [f"trace seed={seed} strategy={strategy}"],
    )
    write_all_reports(out, report)
    return {"output": str(out), "result": result.to_dict()}


def cmd_simulate(package_path: str | Path, runs: int = 1000, seed: int = 42, config: RunnerConfig | None = None) -> dict[str, Any]:
    cfg = config or RunnerConfig()
    runs = min(runs, cfg.max_runs)
    modes = SimulationModes(str(package_path))
    result = modes.monte_carlo(MonteCarloConfig(runs=runs, seed=seed))
    out = make_output_dir(Path(cfg.output_base), mode="simulate")
    sim_data = {"monte_carlo": result}
    report = _diagnostic_report(
        modes.load_result,
        sim_data,
        {"runs": runs, **{k: v for k, v in result.items() if k in ("shortest_path_steps", "longest_path_steps")}},
        [f"simulate runs={runs} seed={seed}"],
    )
    write_all_reports(out, report)
    return {"output": str(out), "result": result}


def cmd_exhaustive(
    package_path: str | Path,
    max_states: int = 200_000,
    config: RunnerConfig | None = None,
) -> dict[str, Any]:
    cfg = config or RunnerConfig()
    max_states = min(max_states, cfg.max_states)
    modes = SimulationModes(str(package_path))
    cancel = [False]
    result = modes.exhaustive(
        ExhaustiveConfig(max_states=max_states, timeout_seconds=cfg.exhaustive_timeout_seconds),
        cancel_flag=cancel,
    )
    out = make_output_dir(Path(cfg.output_base), mode="exhaustive")
    sim_data = {"exhaustive": result}
    report = _diagnostic_report(
        modes.load_result,
        sim_data,
        {"states_explored": result.get("states_explored", 0)},
        [f"exhaustive max_states={max_states}"],
    )
    write_all_reports(out, report)
    return {"output": str(out), "result": result}


def cmd_compare(
    package_path: str | Path,
    runs_per_strategy: int = 100,
    seed: int = 42,
    config: RunnerConfig | None = None,
) -> dict[str, Any]:
    cfg = config or RunnerConfig()
    modes = SimulationModes(str(package_path))
    result = modes.compare_strategies(runs_per_strategy=runs_per_strategy, seed=seed)
    out = make_output_dir(Path(cfg.output_base), mode="compare")
    sim_data = {"compare": result}
    report = _diagnostic_report(
        modes.load_result,
        sim_data,
        {"runs_per_strategy": runs_per_strategy},
        [f"compare runs_per_strategy={runs_per_strategy}"],
    )
    write_all_reports(out, report)
    return {"output": str(out), "result": result}
