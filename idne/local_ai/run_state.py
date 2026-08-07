"""Run directory persistence and status artifacts."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from idne.local_ai.context_builder import ContextBuildResult
from idne.local_ai.paths import safe_task_directory_name
from idne.local_ai.platform_runtime import local_ai_runs_root
from idne.local_ai.task_model import AuthoritativeSource, LocalAITask, TaskStatus, sha256_text, transition_task

ACTIVE_MODEL_ARTIFACTS = (
    "response.txt",
    "transport_report.json",
    "parsed_response.json",
    "response_parse_report.json",
    "response_validation_report.json",
)


def has_active_model_artifacts(run_dir: Path) -> bool:
    if any((run_dir / name).is_file() for name in ACTIVE_MODEL_ARTIFACTS):
        return True
    return (run_dir / "proposal").is_dir()


@dataclass
class PreparationMetrics:
    files_read: int
    bytes_read: int
    character_count: int
    approximate_tokens: int
    context_budget: int
    preparation_seconds: float
    status: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def run_directory_for_task(repo_root: Path, task_id: str) -> Path:
    return local_ai_runs_root(repo_root) / safe_task_directory_name(task_id)


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_run_artifacts(
    run_dir: Path,
    task: LocalAITask,
    context: ContextBuildResult,
    prompt: str,
    metrics: PreparationMetrics,
    diagnostics: dict[str, Any],
    *,
    run_definition_identity: str,
) -> None:
    run_dir.mkdir(parents=True, exist_ok=True)
    write_json(run_dir / "task.json", task.to_dict())
    write_json(run_dir / "context_manifest.json", context.to_manifest())
    (run_dir / "context.txt").write_text(context.context_text + "\n", encoding="utf-8")
    (run_dir / "prompt.txt").write_text(prompt, encoding="utf-8")
    prompt_sha256 = sha256_text(prompt)
    status_path = run_dir / "status.json"
    write_json(
        status_path,
        {
            "task_id": task.task_id,
            "status": task.status.value,
            "attempt_count": task.attempt_count,
            "prompt_sha256": prompt_sha256,
            "source_content_sha256": task.source_content_identity.sha256,
            "run_definition_identity": run_definition_identity,
            "allowed_output_files": list(task.allowed_output_files),
            "processing_stage": "NONE",
            "metrics": metrics.to_dict(),
        },
    )
    write_json(run_dir / "diagnostics.json", diagnostics)


def reload_prepared_task(
    run_dir: Path,
) -> tuple[LocalAITask, ContextBuildResult, str, PreparationMetrics, Path]:
    task = load_task(run_dir)
    manifest = load_context_manifest(run_dir)
    prompt = (run_dir / "prompt.txt").read_text(encoding="utf-8")
    context_text = (run_dir / "context.txt").read_text(encoding="utf-8").rstrip("\n")
    status = load_status(run_dir)
    metrics_data = status.get("metrics", {})
    metrics = PreparationMetrics(
        files_read=int(metrics_data.get("files_read", manifest.get("files_read", 0))),
        bytes_read=int(metrics_data.get("bytes_read", manifest.get("bytes_read", 0))),
        character_count=int(metrics_data.get("character_count", manifest.get("character_count", 0))),
        approximate_tokens=int(
            metrics_data.get("approximate_tokens", manifest.get("approximate_tokens", 0))
        ),
        context_budget=int(metrics_data.get("context_budget", task.context_budget)),
        preparation_seconds=float(metrics_data.get("preparation_seconds", 0.0)),
        status=task.status.value,
    )
    context = ContextBuildResult(
        context_text=context_text,
        character_count=manifest.get("character_count", len(context_text)),
        approximate_tokens=manifest.get("approximate_tokens", 0),
        files_read=manifest.get("files_read", 0),
        bytes_read=manifest.get("bytes_read", 0),
        authoritative_sources=[
            AuthoritativeSource(**src) for src in manifest.get("authoritative_sources", [])
        ],
    )
    return task, context, prompt, metrics, run_dir


def load_task(run_dir: Path) -> LocalAITask:
    data = json.loads((run_dir / "task.json").read_text(encoding="utf-8"))
    return LocalAITask.from_dict(data)


def load_status(run_dir: Path) -> dict[str, Any]:
    return json.loads((run_dir / "status.json").read_text(encoding="utf-8"))


def load_context_manifest(run_dir: Path) -> dict[str, Any]:
    return json.loads((run_dir / "context_manifest.json").read_text(encoding="utf-8"))


def set_task_status(task: LocalAITask, new_status: TaskStatus) -> LocalAITask:
    transition_task(task, new_status)
    return task
