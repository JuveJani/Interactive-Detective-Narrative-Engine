#!/usr/bin/env python3
"""DEPRECATED: Legacy IDNE simulator CLI.

Use `python -m idne.sim_v2` for canonical .idne packages (Simulator v2).
This entry point remains for legacy sim_adapter.json adventures only.
"""

from __future__ import annotations

import argparse
import sys
import warnings
from pathlib import Path

from simulator_v2.legacy import is_legacy_simulator_path


def _warn_deprecated() -> None:
    warnings.warn(
        "idne_sim.py is deprecated. Use: python -m idne.sim_v2 <command> adventure.idne",
        DeprecationWarning,
        stacklevel=3,
    )
    print(
        "warning: idne_sim.py is deprecated — use `python -m idne.sim_v2` for Simulator v2",
        file=sys.stderr,
    )


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="DEPRECATED legacy simulator — use python -m idne.sim_v2 instead",
    )
    sub = p.add_subparsers(dest="command", required=True)
    for name in ("validate", "simulate", "trace", "compare", "explain", "repair-plan", "export-ai-context"):
        sub.add_parser(name, help="DEPRECATED — use idne.sim_v2")
    return p


def main(argv: list[str] | None = None) -> int:
    _warn_deprecated()
    if len(sys.argv) > 2:
        adventure = Path(sys.argv[2]) if len(sys.argv) > 2 else None
        if adventure and adventure.exists() and not is_legacy_simulator_path(adventure):
            print(
                "This looks like a canonical package. Re-run with:\n"
                f"  python -m idne.sim_v2 {sys.argv[1]} {adventure}",
                file=sys.stderr,
            )
            return 2

    from simulator.config import DEFAULT_CONFIG, SimConfig
    from simulator.runner import cmd_compare, cmd_simulate, cmd_trace, cmd_validate
    from simulator.commands import cmd_explain, cmd_export_ai_context, cmd_repair_plan

    p = argparse.ArgumentParser(description="DEPRECATED legacy simulator")
    sub = p.add_subparsers(dest="command", required=True)
    v = sub.add_parser("validate")
    v.add_argument("adventure", type=str)
    s = sub.add_parser("simulate")
    s.add_argument("adventure", type=str)
    s.add_argument("--runs", type=int, default=1000)
    s.add_argument("--seed", type=int, default=42)
    t = sub.add_parser("trace")
    t.add_argument("adventure", type=str)
    t.add_argument("--seed", type=int, default=42)
    t.add_argument("--strategy", type=str, default="clue-seeking")
    c = sub.add_parser("compare")
    c.add_argument("adventure", type=str)
    c.add_argument("--runs-per-strategy", type=int, default=100)
    c.add_argument("--seed", type=int, default=42)
    e = sub.add_parser("explain")
    e.add_argument("output_folder", type=str)
    e.add_argument("--finding", type=str, default=None, dest="finding_id")
    r = sub.add_parser("repair-plan")
    r.add_argument("output_folder", type=str)
    r.add_argument("--finding", type=str, default=None, dest="finding_id")
    x = sub.add_parser("export-ai-context")
    x.add_argument("output_folder", type=str)
    x.add_argument("--finding", type=str, default=None, dest="finding_id")
    p.add_argument("--timeout", type=int, default=DEFAULT_CONFIG.timeout_seconds)
    p.add_argument("--max-runs", type=int, default=DEFAULT_CONFIG.max_runs)

    args = p.parse_args(argv)
    config = SimConfig(timeout_seconds=args.timeout, max_runs=args.max_runs)
    adventure = getattr(args, "adventure", None)
    output_folder = getattr(args, "output_folder", None)
    try:
        if args.command == "validate":
            out = cmd_validate(adventure, config)
        elif args.command == "simulate":
            out = cmd_simulate(adventure, args.runs, args.seed, config)
        elif args.command == "trace":
            out = cmd_trace(adventure, args.seed, args.strategy)
        elif args.command == "compare":
            out = cmd_compare(adventure, args.runs_per_strategy, args.seed, config)
        elif args.command == "explain":
            out = cmd_explain(output_folder, getattr(args, "finding_id", None))
        elif args.command == "repair-plan":
            out = cmd_repair_plan(output_folder, getattr(args, "finding_id", None))
        elif args.command == "export-ai-context":
            out = cmd_export_ai_context(output_folder, getattr(args, "finding_id", None))
        else:
            return 1
        print(str(out))
        return 0
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
