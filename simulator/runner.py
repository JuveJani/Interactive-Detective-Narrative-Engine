"""High-level run orchestration."""

from __future__ import annotations

import random
import resource
import signal
import sys
import time
from pathlib import Path
from typing import Any

from simulator.config import DEFAULT_CONFIG, SimConfig
from simulator.diagnostics import analyze_simulation, run_batch
from simulator.engine import SimulationEngine, SimulationLimitError
from simulator.graph import build_edges, graph_stats
from simulator.loader import load_adventure
from simulator.output import make_output_dir, write_all_outputs
from simulator.state import GameState
from simulator.strategies import STRATEGIES, get_strategy
from simulator.validate import validate_static


class RunInterrupted(Exception):
    pass


class RunLimitExceeded(Exception):
    pass


def _memory_mb() -> float:
    usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if sys.platform == "darwin":
        return usage / (1024 * 1024)
    return usage / 1024


def _check_limits(config: SimConfig, states: int = 0) -> None:
    mem = _memory_mb()
    if mem > config.memory_guard_mb:
        raise RunLimitExceeded(f"memory guard exceeded ({mem:.0f} MB > {config.memory_guard_mb} MB)")
    if states > config.max_states:
        raise RunLimitExceeded(f"max_states exceeded ({states} > {config.max_states})")


def _install_sigint() -> None:
    def handler(signum, frame):
        raise RunInterrupted()

    signal.signal(signal.SIGINT, handler)


def cmd_validate(adventure_path: str, config: SimConfig = DEFAULT_CONFIG) -> Path:
    log: list[str] = []
    package = load_adventure(adventure_path)
    findings = validate_static(package)
    edges = build_edges(package["adapter"])
    metrics = {"graph": graph_stats(package["adapter"]), "runs": 0}
    out = make_output_dir(mode="validate")
    write_all_outputs(out, findings, metrics, [], package["adapter"], edges, "validate", log)
    log.append(f"Validation complete: {len(findings)} findings")
    (out / "simulator_log.txt").write_text("\n".join(log), encoding="utf-8")
    return out


def cmd_simulate(
    adventure_path: str,
    runs: int,
    seed: int,
    config: SimConfig = DEFAULT_CONFIG,
) -> Path:
    runs = min(runs, config.max_runs)
    package = load_adventure(adventure_path)
    static = validate_static(package)
    log = [f"simulate runs={runs} seed={seed}"]
    out = make_output_dir(mode="simulate")
    results = []
    start = time.time()
    try:
        _install_sigint()
        for i in range(runs):
            if time.time() - start > config.timeout_seconds:
                log.append("timeout reached")
                break
            _check_limits(config)
            if i and i % config.progress_interval == 0:
                print(f"progress {i}/{runs}", file=sys.stderr)
            batch = run_batch(package, "random", 1, seed + i, config)
            results.extend(batch)
            if results:
                _check_limits(config, results[-1].states_explored if hasattr(results[-1], "states_explored") else 0)
    except RunInterrupted:
        log.append("interrupted — saving partial results")
    except (RunLimitExceeded, SimulationLimitError) as exc:
        log.append(f"limit reached: {exc}")
    findings, metrics = analyze_simulation(package, results, static)
    edges = build_edges(package["adapter"])
    write_all_outputs(out, findings, metrics, results, package["adapter"], edges, "simulate", log)
    return out


def cmd_trace(adventure_path: str, seed: int, strategy: str = "clue-seeking") -> Path:
    package = load_adventure(adventure_path)
    static = validate_static(package)
    rng = random.Random(seed)
    strat = get_strategy(strategy, rng, package["adapter"])
    engine = SimulationEngine(package, rng)
    trace_steps: list[dict[str, Any]] = []

    def choose(state: GameState, options: list, role: str):
        pick = strat.choose(state, options, role)
        trace_steps.append({"node": state.node, "role": role, "pick": pick, "snapshot": state.snapshot()})
        return pick

    final = engine.run(choose)
    trace = {"seed": seed, "strategy": strategy, "ending": final.node, "steps": trace_steps, "final": final.snapshot()}
    results = run_batch(package, strategy, 1, seed)
    findings, metrics = analyze_simulation(package, results, static)
    edges = build_edges(package["adapter"])
    out = make_output_dir(mode="trace")
    write_all_outputs(out, findings, metrics, results, package["adapter"], edges, "trace", [f"trace seed={seed}"], trace=trace)
    return out


def cmd_compare(adventure_path: str, runs_per: int, seed: int, config: SimConfig = DEFAULT_CONFIG) -> Path:
    package = load_adventure(adventure_path)
    static = validate_static(package)
    all_results = []
    log = [f"compare runs_per_strategy={runs_per}"]
    for name in STRATEGIES:
        all_results.extend(run_batch(package, name, min(runs_per, config.max_runs), seed, config))
    findings, metrics = analyze_simulation(package, all_results, static)
    metrics["per_strategy"] = {n: sum(1 for r in all_results if r.strategy == n) for n in STRATEGIES}
    edges = build_edges(package["adapter"])
    out = make_output_dir(mode="compare")
    write_all_outputs(out, findings, metrics, all_results, package["adapter"], edges, "compare", log)
    return out
