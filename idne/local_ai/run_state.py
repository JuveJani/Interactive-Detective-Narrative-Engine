"""Run directory persistence and status artifacts."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from idne.local_ai.context_builder import ContextBuildResult
from idne.local_ai.paths import safe_task_directory_name
from idne.local_ai.platform_runtime import local_ai_runs_root
from idne.local_ai.task_model import LocalAITask, TaskStatus, transition_task


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
) -> None:
    run_dir.mkdir(parents=True, exist_ok=True)
    write_json(run_dir / "task.json", task.to_dict())
    write_json(run_dir / "context_manifest.json", context.to_manifest())
    (run_dir / "context.txt").write_text(context.context_text + "\n", encoding="utf-8")
    (run_dir / "prompt.txt").write_text(prompt, encoding="utf-8")
    write_json(
        run_dir / "status.json",
        {
            "task_id": task.task_id,
            "status": task.status.value,
            "attempt_count": task.attempt_count,
            "metrics": metrics.to_dict(),
        },
    )
    write_json(run_dir / "diagnostics.json", diagnostics)


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
