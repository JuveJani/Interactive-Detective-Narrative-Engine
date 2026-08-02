#!/usr/bin/env python3
"""IDNE offline adventure simulator and diagnostic CLI."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from simulator.config import DEFAULT_CONFIG, SimConfig
from simulator.runner import cmd_compare, cmd_simulate, cmd_trace, cmd_validate


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="IDNE offline simulator (Termux-safe)")
    sub = p.add_subparsers(dest="command", required=True)

    v = sub.add_parser("validate", help="Static validation")
    v.add_argument("adventure", type=str)

    s = sub.add_parser("simulate", help="Monte Carlo simulation")
    s.add_argument("adventure", type=str)
    s.add_argument("--runs", type=int, default=1000)
    s.add_argument("--seed", type=int, default=42)

    t = sub.add_parser("trace", help="Single seeded trace")
    t.add_argument("adventure", type=str)
    t.add_argument("--seed", type=int, default=42)
    t.add_argument("--strategy", type=str, default="clue-seeking")

    c = sub.add_parser("compare", help="Compare strategies")
    c.add_argument("adventure", type=str)
    c.add_argument("--runs-per-strategy", type=int, default=100)
    c.add_argument("--seed", type=int, default=42)

    p.add_argument("--timeout", type=int, default=DEFAULT_CONFIG.timeout_seconds)
    p.add_argument("--max-runs", type=int, default=DEFAULT_CONFIG.max_runs)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    config = SimConfig(
        timeout_seconds=args.timeout,
        max_runs=args.max_runs,
    )
    adventure = args.adventure
    if not Path(adventure).exists():
        print(f"error: adventure not found: {adventure}", file=sys.stderr)
        return 1
    try:
        if args.command == "validate":
            out = cmd_validate(adventure, config)
        elif args.command == "simulate":
            out = cmd_simulate(adventure, args.runs, args.seed, config)
        elif args.command == "trace":
            out = cmd_trace(adventure, args.seed, args.strategy)
        elif args.command == "compare":
            out = cmd_compare(adventure, args.runs_per_strategy, args.seed, config)
        else:
            return 1
        print(str(out))
        return 0
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
