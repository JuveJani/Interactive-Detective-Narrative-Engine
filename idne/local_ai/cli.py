"""CLI for IDNE Offline Local AI Orchestrator."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from idne.local_ai.context_builder import estimate_tokens
from idne.local_ai.doctor import format_doctor_report, run_doctor
from idne.local_ai.paths import find_repo_root
from idne.local_ai.run_state import load_context_manifest, load_status, load_task
from idne.local_ai.task_builder import TaskPreparationError, prepare_task


def _print_json(data: object) -> None:
    print(json.dumps(data, indent=2, sort_keys=True))


def cmd_doctor(_: argparse.Namespace) -> int:
    report = run_doctor()
    print(format_doctor_report(report))
    if report.status == "BLOCKED":
        return 4
    if report.status == "DEGRADED":
        return 3
    return 0


def cmd_prepare(args: argparse.Namespace) -> int:
    try:
        task, context, _prompt, metrics, run_dir = prepare_task(
            args.task_type,
            args.input,
            context_budget=args.context_budget,
        )
    except TaskPreparationError as exc:
        print(f"BLOCKED: {exc}")
        return 4

    files = task.allowed_input_files + [src.path for src in task.authoritative_sources]
    print(f"Task: {task.task_id}")
    print(f"Dir: {run_dir.as_posix()}")
    print(f"Status: {task.status.value}")
    print(f"Files: {len(files)}")
    for path in files:
        print(f"  - {path}")
    print(f"Context: {metrics.character_count} chars (~{metrics.approximate_tokens} tokens)")
    print(f"Budget: {metrics.context_budget}")
    print(f"Duration: {metrics.preparation_seconds:.3f}s")
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    run_dir = Path(args.task_directory)
    if not run_dir.is_dir():
        print(f"not a task directory: {run_dir}")
        return 1
    status = load_status(run_dir)
    _print_json(status)
    return 0


def cmd_show_prompt(args: argparse.Namespace) -> int:
    run_dir = Path(args.task_directory)
    prompt_path = run_dir / "prompt.txt"
    if not prompt_path.is_file():
        print(f"missing prompt: {prompt_path}")
        return 1
    print(prompt_path.read_text(encoding="utf-8"), end="")
    return 0


def cmd_inspect_context(args: argparse.Namespace) -> int:
    run_dir = Path(args.task_directory)
    manifest_path = run_dir / "context_manifest.json"
    if not manifest_path.is_file():
        print(f"missing context manifest: {manifest_path}")
        return 1
    manifest = load_context_manifest(run_dir)
    task = load_task(run_dir)
    print(f"Task: {task.task_id}")
    print(f"Chars: {manifest.get('character_count', 0)}")
    print(f"Tokens~: {manifest.get('approximate_tokens', estimate_tokens(manifest.get('character_count', 0)))}")
    print(f"Budget: {task.context_budget}")
    print("Sections:")
    for section in manifest.get("sections", []):
        print(
            f"  - {section.get('path')} [{section.get('kind')}] "
            f"{section.get('char_count', 0)} chars"
        )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="idne.local_ai",
        description="IDNE Offline Local AI Orchestrator — deterministic task preparation",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    doctor = sub.add_parser("doctor", help="Check runtime readiness")
    doctor.set_defaults(func=cmd_doctor)

    prepare = sub.add_parser("prepare", help="Prepare a Local AI task without calling a model")
    prepare.add_argument("--task-type", required=True)
    prepare.add_argument("--input", required=True, help="Repository-relative author input file")
    prepare.add_argument("--context-budget", type=int, default=None)
    prepare.set_defaults(func=cmd_prepare)

    status = sub.add_parser("status", help="Show task status JSON")
    status.add_argument("task_directory")
    status.set_defaults(func=cmd_status)

    show_prompt = sub.add_parser("show-prompt", help="Print prepared prompt.txt")
    show_prompt.add_argument("task_directory")
    show_prompt.set_defaults(func=cmd_show_prompt)

    inspect = sub.add_parser("inspect-context", help="Summarize context manifest")
    inspect.add_argument("task_directory")
    inspect.set_defaults(func=cmd_inspect_context)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        find_repo_root()
    except Exception as exc:  # noqa: BLE001
        print(f"repository root not found: {exc}")
        return 2
    return int(args.func(args))


if __name__ == "__main__":
    sys.exit(main())
