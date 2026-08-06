"""Simulator v2 CLI — canonical package offline diagnostics."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from simulator_v2.ai_context import export_ai_context
from simulator_v2.config import RunnerConfig
from simulator_v2.human_delivery.runner import (
    cmd_delivery_validate,
    cmd_human_simulate,
    cmd_human_trace,
)
from simulator_v2.runner import (
    cmd_compare,
    cmd_diagnose,
    cmd_exhaustive,
    cmd_simulate,
    cmd_trace,
    cmd_validate,
)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="idne.sim_v2",
        description="IDNE Simulator v2 — offline canonical package diagnostics",
    )
    sub = p.add_subparsers(dest="command", required=True)

    d = sub.add_parser("diagnose", help="Full integrated diagnostic run with all reports")
    d.add_argument("adventure", type=str)
    d.add_argument("--output-base", type=str, default="simulation_output_v2")
    d.add_argument("--seed", type=int, default=42)
    d.add_argument("--max-states", type=int, default=200_000)
    d.add_argument("--runs", type=int, default=1000)
    d.add_argument("--resume", action="store_true")

    v = sub.add_parser("validate", help="Validate package readiness")
    v.add_argument("adventure", type=str)

    t = sub.add_parser("trace", help="Deterministic single trace")
    t.add_argument("adventure", type=str)
    t.add_argument("--seed", type=int, default=42)
    t.add_argument("--strategy", type=str, default="random_legal")

    s = sub.add_parser("simulate", help="Seeded Monte Carlo simulation")
    s.add_argument("adventure", type=str)
    s.add_argument("--runs", type=int, default=1000)
    s.add_argument("--seed", type=int, default=42)

    e = sub.add_parser("exhaustive", help="Bounded exhaustive traversal")
    e.add_argument("adventure", type=str)
    e.add_argument("--max-states", type=int, default=200_000)
    e.add_argument("--timeout", type=float, default=300.0)

    c = sub.add_parser("compare", help="Strategy comparison")
    c.add_argument("adventure", type=str)
    c.add_argument("--runs-per-strategy", type=int, default=100)
    c.add_argument("--seed", type=int, default=42)

    hd = sub.add_parser("delivery-validate", help="Validate static gamebook human delivery")
    hd.add_argument("adventure", type=str)

    ht = sub.add_parser("human-trace", help="Deterministic human-delivery trace")
    ht.add_argument("adventure", type=str)
    ht.add_argument("--seed", type=int, default=42)
    ht.add_argument("--strategy", type=str, default="human_random_legal")

    hs = sub.add_parser("human-simulate", help="Human-delivery Monte Carlo simulation")
    hs.add_argument("adventure", type=str)
    hs.add_argument("--runs", type=int, default=100)
    hs.add_argument("--seed", type=int, default=42)
    hs.add_argument("--strategy", type=str, default="human_random_legal")

    x = sub.add_parser("export-ai-context", help="Export offline AI context for a finding")
    x.add_argument("output", type=str, help="Prior run output folder")
    x.add_argument("--finding", type=str, required=True, dest="finding_id")

    return p


def _config_from_args(args: argparse.Namespace) -> RunnerConfig:
    cfg = RunnerConfig()
    if hasattr(args, "output_base") and args.output_base:
        cfg.output_base = args.output_base
    if hasattr(args, "seed"):
        cfg.seed = args.seed
    if hasattr(args, "max_states"):
        cfg.max_states = args.max_states
    if hasattr(args, "runs"):
        cfg.monte_carlo_runs = args.runs
    if hasattr(args, "strategy"):
        cfg.strategy = args.strategy
    if hasattr(args, "runs_per_strategy"):
        cfg.compare_runs_per_strategy = args.runs_per_strategy
    if hasattr(args, "timeout"):
        cfg.exhaustive_timeout_seconds = args.timeout
    if getattr(args, "resume", False):
        cfg.resume_checkpoint = "1"
    return cfg


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    adventure = getattr(args, "adventure", None)
    if args.command != "export-ai-context":
        if not adventure or not Path(adventure).exists():
            print(f"error: adventure not found: {adventure}", file=sys.stderr)
            return 2

    cfg = _config_from_args(args)

    try:
        if args.command == "diagnose":
            out = cmd_diagnose(adventure, cfg)
            print(json.dumps({"status": "COMPLETED", "output": str(out)}, indent=2))
            return 0
        if args.command == "validate":
            result = cmd_validate(adventure, cfg)
            print(json.dumps(result, indent=2))
            return 0 if result.get("status") == "PASS" else 1
        if args.command == "trace":
            result = cmd_trace(adventure, args.seed, args.strategy, cfg)
            print(json.dumps(result, indent=2))
            return 0
        if args.command == "simulate":
            result = cmd_simulate(adventure, args.runs, args.seed, cfg)
            print(json.dumps(result, indent=2))
            return 0
        if args.command == "exhaustive":
            result = cmd_exhaustive(adventure, args.max_states, cfg)
            status = result.get("result", {}).get("status", "")
            print(json.dumps(result, indent=2))
            return 0 if status in ("COMPLETED", "BLOCKED", "CANCELLED") else 1
        if args.command == "compare":
            result = cmd_compare(adventure, args.runs_per_strategy, args.seed, cfg)
            print(json.dumps(result, indent=2))
            return 0
        if args.command == "delivery-validate":
            result = cmd_delivery_validate(adventure)
            print(json.dumps(result, indent=2))
            return 0 if result.get("status") == "PASS" else 1
        if args.command == "human-trace":
            result = cmd_human_trace(adventure, seed=args.seed, strategy=args.strategy)
            print(json.dumps(result, indent=2))
            return 0 if result.get("result", {}).get("status") in ("COMPLETED", "INCOMPLETE") else 1
        if args.command == "human-simulate":
            result = cmd_human_simulate(adventure, runs=args.runs, seed=args.seed, strategy=args.strategy)
            print(json.dumps(result, indent=2))
            trust = result.get("result", {}).get("trust", {})
            return 0 if trust.get("trusted") else 1
        if args.command == "export-ai-context":
            out = export_ai_context(Path(args.output), args.finding_id)
            print(json.dumps({"status": "COMPLETED", "context_dir": str(out)}, indent=2))
            return 0
    except KeyboardInterrupt:
        print("interrupted", file=sys.stderr)
        return 130
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
