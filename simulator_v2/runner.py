"""Full diagnostic run orchestration for Simulator v2."""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path
from typing import Any

from simulator_v2.config import RunnerConfig
from simulator_v2.diagnostics import DiagnosticReport, run_integrated_diagnostics
from simulator_v2.modes import ExhaustiveConfig, MonteCarloConfig, SimulationModes
from simulator_v2.package_loader import load_simulator_package
from simulator_v2.reports import make_output_dir, write_all_reports


class RunInterrupted(Exception):
    pass


def _memory_mb() -> float:
    try:
        import resource

        usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        if sys.platform == "darwin":
            return usage / (1024 * 1024)
        return usage / 1024
    except Exception:
        return 0.0


def _check_memory(config: RunnerConfig) -> None:
    mem = _memory_mb()
    if mem > config.memory_guard_mb:
        raise MemoryError(f"memory guard exceeded ({mem:.0f} MB > {config.memory_guard_mb} MB)")


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
        out = make_output_dir(Path(cfg.output_base), mode="validate")
        write_all_reports(out, DiagnosticReport(
            adventure_id=result.get("load", {}).get("adventure_id", ""),
            play_mode=result.get("load", {}).get("play_mode", ""),
            integrated_validation={"status": result.get("status")},
            trust=result.get("trust", {}),
            findings=[],
            metrics={"legal_action_count": result.get("legal_action_count", 0)},
        ))
    return result


def cmd_trace(package_path: str | Path, seed: int = 42, strategy: str = "random_legal", config: RunnerConfig | None = None) -> dict[str, Any]:
    cfg = config or RunnerConfig()
    cfg.seed = seed
    cfg.strategy = strategy
    modes = SimulationModes(str(package_path))
    result = modes.trace(strategy, seed=seed)
    out = make_output_dir(Path(cfg.output_base), mode="trace")
    load = load_simulator_package(package_path)
    report = DiagnosticReport(
        adventure_id=load.adventure_id,
        play_mode=load.play_mode,
        integrated_validation={},
        trust=result.to_dict().get("trust", {}),
        findings=[],
        metrics=result.metrics.to_dict(),
        simulation={"trace": result.to_dict()},
        log=[f"trace seed={seed} strategy={strategy}"],
    )
    write_all_reports(out, report)
    return {"output": str(out), "result": result.to_dict()}


def cmd_simulate(package_path: str | Path, runs: int = 1000, seed: int = 42, config: RunnerConfig | None = None) -> dict[str, Any]:
    cfg = config or RunnerConfig()
    runs = min(runs, cfg.max_runs)
    modes = SimulationModes(str(package_path))
    result = modes.monte_carlo(MonteCarloConfig(runs=runs, seed=seed))
    out = make_output_dir(Path(cfg.output_base), mode="simulate")
    load = load_simulator_package(package_path)
    report = DiagnosticReport(
        adventure_id=load.adventure_id,
        play_mode=load.play_mode,
        integrated_validation={},
        trust=result.get("trust", {}),
        findings=[],
        metrics={"runs": runs},
        simulation={"monte_carlo": result},
        log=[f"simulate runs={runs} seed={seed}"],
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
    load = load_simulator_package(package_path)
    report = DiagnosticReport(
        adventure_id=load.adventure_id,
        play_mode=load.play_mode,
        integrated_validation={},
        trust={},
        findings=[],
        metrics={"states_explored": result.get("states_explored", 0)},
        simulation={"exhaustive": result},
        log=[f"exhaustive max_states={max_states}"],
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
    load = load_simulator_package(package_path)
    report = DiagnosticReport(
        adventure_id=load.adventure_id,
        play_mode=load.play_mode,
        integrated_validation={},
        trust={},
        findings=[],
        metrics={"runs_per_strategy": runs_per_strategy},
        simulation={"compare": result},
        log=[f"compare runs_per_strategy={runs_per_strategy}"],
    )
    write_all_reports(out, report)
    return {"output": str(out), "result": result}
