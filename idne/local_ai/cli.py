"""CLI for IDNE Offline Local AI Orchestrator."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from idne.local_ai.config import load_config
from idne.local_ai.context_builder import estimate_tokens
from idne.local_ai.doctor import format_doctor_report, run_doctor
from idne.local_ai.errors import TransportError
from idne.local_ai.model_adapter import create_adapter, execute_with_retries, select_model
from idne.local_ai.paths import find_repo_root
from idne.local_ai.run_state import load_context_manifest, load_status, load_task
from idne.local_ai.task_builder import TaskPreparationError, prepare_task
from idne.local_ai.transport import TaskRunError, run_task


def _print_json(data: object) -> None:
    print(json.dumps(data, indent=2, sort_keys=True))


def _add_config_arg(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--config", type=Path, default=None, help="Path to local_ai.toml")


def _add_mock_arg(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--mock", action="store_true", help="Use deterministic mock adapter")


def cmd_doctor(args: argparse.Namespace) -> int:
    report = run_doctor(
        config_path=args.config,
        mock=args.mock,
        test_completion=args.test_completion,
    )
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


def cmd_run(args: argparse.Namespace) -> int:
    try:
        result = run_task(
            Path(args.task_directory),
            config_path=args.config,
            mock=args.mock,
            force=args.force,
        )
    except KeyboardInterrupt:
        print("Interrupted")
        return 130
    except TaskRunError as exc:
        print(f"{exc.classification.upper()}: {exc}")
        return exc.exit_code
    print(f"Task: {result.task.task_id}")
    print(f"Status: {result.task.status.value}")
    print(f"Model: {result.transport_report.get('selected_model')}")
    print(f"Duration: {result.duration_seconds:.3f}s")
    usage = result.transport_report.get("usage", {})
    if usage.get("total_tokens") is not None:
        print(f"Tokens: {usage.get('total_tokens')}")
    print(f"Response: {result.transport_report.get('response_character_count')} chars")
    return 0


def cmd_models(args: argparse.Namespace) -> int:
    try:
        cfg = load_config(config_path=args.config)
        if args.mock:
            cfg.adapter_type = "mock"
        adapter = create_adapter(cfg, mock=args.mock)
        models = execute_with_retries(cfg, "list_models", lambda: adapter.list_models(cfg))
        try:
            selection = select_model(cfg, models)
            selected = selection.model_id
            reason = selection.reason
        except TransportError as exc:
            selected = None
            reason = str(exc)
        _print_json(
            {
                "adapter": adapter.name,
                "endpoint": cfg.base_url,
                "models": [m.to_dict() for m in models],
                "selected_model": selected,
                "selection_reason": reason,
            }
        )
        return 0
    except TransportError as exc:
        print(f"{exc.classification.upper()}: {exc}")
        return 4


def cmd_status(args: argparse.Namespace) -> int:
    run_dir = Path(args.task_directory)
    if not run_dir.is_dir():
        print(f"not a task directory: {run_dir}")
        return 1
    _print_json(load_status(run_dir))
    return 0


def cmd_show_prompt(args: argparse.Namespace) -> int:
    run_dir = Path(args.task_directory)
    prompt_path = run_dir / "prompt.txt"
    if not prompt_path.is_file():
        print(f"missing prompt: {prompt_path}")
        return 1
    print(prompt_path.read_text(encoding="utf-8"), end="")
    return 0


def cmd_show_response(args: argparse.Namespace) -> int:
    run_dir = Path(args.task_directory)
    response_path = run_dir / "response.txt"
    if not response_path.is_file():
        print(f"missing response: {response_path}")
        return 1
    print(response_path.read_text(encoding="utf-8"), end="")
    return 0


def cmd_transport_report(args: argparse.Namespace) -> int:
    run_dir = Path(args.task_directory)
    report_path = run_dir / "transport_report.json"
    if not report_path.is_file():
        print(f"missing transport report: {report_path}")
        return 1
    _print_json(json.loads(report_path.read_text(encoding="utf-8")))
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
    print(
        f"Tokens~: {manifest.get('approximate_tokens', estimate_tokens(manifest.get('character_count', 0)))}"
    )
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
        description="IDNE Offline Local AI Orchestrator",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    doctor = sub.add_parser("doctor", help="Check runtime and adapter readiness")
    _add_config_arg(doctor)
    _add_mock_arg(doctor)
    doctor.add_argument(
        "--test-completion",
        action="store_true",
        help="Send a tiny deterministic completion probe",
    )
    doctor.set_defaults(func=cmd_doctor)

    prepare = sub.add_parser("prepare", help="Prepare a Local AI task without calling a model")
    prepare.add_argument("--task-type", required=True)
    prepare.add_argument("--input", required=True, help="Repository-relative author input file")
    prepare.add_argument("--context-budget", type=int, default=None)
    prepare.set_defaults(func=cmd_prepare)

    run = sub.add_parser("run", help="Send prepared prompt to configured model")
    run.add_argument("task_directory")
    _add_config_arg(run)
    _add_mock_arg(run)
    run.add_argument("--force", action="store_true", help="Overwrite an existing response")
    run.set_defaults(func=cmd_run)

    models = sub.add_parser("models", help="List models from configured adapter")
    _add_config_arg(models)
    _add_mock_arg(models)
    models.set_defaults(func=cmd_models)

    status = sub.add_parser("status", help="Show task status JSON")
    status.add_argument("task_directory")
    status.set_defaults(func=cmd_status)

    show_prompt = sub.add_parser("show-prompt", help="Print prepared prompt.txt")
    show_prompt.add_argument("task_directory")
    show_prompt.set_defaults(func=cmd_show_prompt)

    show_response = sub.add_parser("show-response", help="Print response.txt")
    show_response.add_argument("task_directory")
    show_response.set_defaults(func=cmd_show_response)

    transport = sub.add_parser("transport-report", help="Print transport_report.json")
    transport.add_argument("task_directory")
    transport.set_defaults(func=cmd_transport_report)

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
