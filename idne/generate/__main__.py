"""CLI for Adventure Generator v2."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from idne.generate.brief import load_brief
from idne.generate.pipeline import GenerationPipeline


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="IDNE Adventure Generator v2")
    parser.add_argument("brief", type=Path, help="Path to adventure brief JSON")
    parser.add_argument("--workspace", type=Path, default=None, help="Generation workspace root")
    parser.add_argument("--resume", action="store_true", help="Resume from checkpoint")
    parser.add_argument("--stage", type=str, default=None, help="Run through named stage")
    parser.add_argument("--config", type=Path, default=None, help="Model adapter JSON config")
    parser.add_argument("--auto-approve", action="store_true", help="Auto-approve human gates (tests)")
    args = parser.parse_args(argv)

    brief = load_brief(args.brief)
    workspace = args.workspace or Path("generated") / Path(args.brief).stem
    workspace.mkdir(parents=True, exist_ok=True)

    model_config: dict = {"backend": "mock", "local_mode": True}
    if args.config and args.config.exists():
        model_config = json.loads(args.config.read_text(encoding="utf-8"))

    pipeline = GenerationPipeline(
        workspace,
        args.brief,
        model_config=model_config,
        auto_approve=args.auto_approve,
    )
    result = pipeline.run(resume=args.resume, target_stage=args.stage)

    print(json.dumps(
        {
            "status": result.status,
            "last_stage": result.last_stage,
            "message": result.message,
            "state_path": result.state_path,
            "errors": result.errors,
        },
        indent=2,
    ))

    if result.status == "COMPLETE":
        return 0
    if result.status == "AWAITING_APPROVAL":
        return 3
    if result.status == "BLOCKED":
        return 4
    return 1


if __name__ == "__main__":
    sys.exit(main())
