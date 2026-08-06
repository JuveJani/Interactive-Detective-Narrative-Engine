"""Execute prepared Local AI tasks against a model adapter."""

from __future__ import annotations

import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from idne.local_ai.attempts import archive_current_attempt, reset_processing_state
from idne.local_ai.config import LocalAIConfig, load_config
from idne.local_ai.errors import ModelSelectionError, TransportError
from idne.local_ai.lm_studio_client import SYSTEM_MESSAGE
from idne.local_ai.model_adapter import create_adapter, execute_with_retries, select_model
from idne.local_ai.response_capture import save_transport_artifacts, save_transport_failure
from idne.local_ai.run_state import load_status, load_task, write_json
from idne.local_ai.task_model import LocalAITask, TaskStatus, sha256_text, transition_task, utc_now_iso


class TaskRunError(RuntimeError):
    def __init__(self, message: str, *, exit_code: int = 1, classification: str = "failed") -> None:
        super().__init__(message)
        self.exit_code = exit_code
        self.classification = classification


@dataclass
class TaskRunResult:
    task: LocalAITask
    run_dir: Path
    transport_report: dict[str, Any]
    duration_seconds: float


RUNNABLE_WITH_FORCE = frozenset({TaskStatus.READY_FOR_MODEL, TaskStatus.RESPONSE_RECEIVED})
BLOCKED_FROM_RUN = frozenset(
    {TaskStatus.CREATED, TaskStatus.PREPARED, TaskStatus.BLOCKED, TaskStatus.VALIDATED, TaskStatus.APPLIED}
)


def _load_prompt_sha256(run_dir: Path) -> str | None:
    status = load_status(run_dir)
    return status.get("prompt_sha256")


def verify_prompt_identity(run_dir: Path, task: LocalAITask) -> str:
    prompt_path = run_dir / "prompt.txt"
    if not prompt_path.is_file():
        raise TaskRunError("prompt.txt missing", exit_code=4, classification="malformed_task")
    prompt = prompt_path.read_text(encoding="utf-8")
    prompt_sha256 = sha256_text(prompt)
    expected = _load_prompt_sha256(run_dir)
    if expected and expected != prompt_sha256:
        raise TaskRunError(
            "prompt.txt content identity mismatch",
            exit_code=4,
            classification="malformed_task",
        )
    return prompt_sha256


def assert_runnable(task: LocalAITask, *, force: bool) -> None:
    if task.status in BLOCKED_FROM_RUN:
        raise TaskRunError(
            f"task status {task.status.value} cannot be executed",
            exit_code=4,
            classification="invalid_status",
        )
    if task.status == TaskStatus.RESPONSE_RECEIVED and not force:
        raise TaskRunError(
            "task already has a response; use --force to run again",
            exit_code=4,
            classification="invalid_status",
        )
    if task.status not in RUNNABLE_WITH_FORCE:
        raise TaskRunError(
            f"task status {task.status.value} is not ready for model transport",
            exit_code=4,
            classification="invalid_status",
        )


def response_exists(run_dir: Path) -> bool:
    return (run_dir / "response.txt").is_file() and (run_dir / "transport_report.json").is_file()


def run_task(
    run_dir: Path,
    *,
    config_path: Path | None = None,
    mock: bool = False,
    force: bool = False,
) -> TaskRunResult:
    run_dir = run_dir.resolve()
    if not run_dir.is_dir():
        raise TaskRunError(f"not a task directory: {run_dir}", exit_code=4)

    task = load_task(run_dir)
    assert_runnable(task, force=force)
    if response_exists(run_dir) and not force:
        raise TaskRunError(
            "response already saved; use --force to overwrite",
            exit_code=4,
            classification="invalid_status",
        )

    prompt_sha256 = verify_prompt_identity(run_dir, task)
    prompt = (run_dir / "prompt.txt").read_text(encoding="utf-8")
    if force and response_exists(run_dir):
        archive_current_attempt(run_dir)
        reset_processing_state(run_dir)
    cfg = load_config(config_path=config_path)
    if mock:
        cfg.adapter_type = "mock"

    adapter = create_adapter(cfg, mock=mock)
    started_at = utc_now_iso()
    start = time.perf_counter()
    retry_count = max(0, int(cfg.retry_count))
    selected_model: str | None = None

    try:
        models = execute_with_retries(cfg, "list_models", lambda: adapter.list_models(cfg))
        selection = select_model(cfg, models)
        selected_model = selection.model_id

        request_payload = {
            "model": selected_model,
            "messages": [
                {"role": "system", "content": SYSTEM_MESSAGE},
                {"role": "user", "content": "<prompt.txt>"},
            ],
            "temperature": cfg.temperature,
            "max_tokens": cfg.max_output_tokens,
            "stream": False,
        }
        if cfg.seed is not None:
            request_payload["seed"] = cfg.seed
        request_payload["prompt_sha256"] = prompt_sha256
        if cfg.log_requests:
            request_payload["logged"] = True

        result = execute_with_retries(
            cfg,
            "chat_completion",
            lambda: adapter.complete(
                cfg,
                model=selected_model,
                user_prompt=prompt,
            ),
        )
        ended_at = utc_now_iso()
        duration = time.perf_counter() - start
        report = save_transport_artifacts(
            run_dir,
            task=task,
            prompt_sha256=prompt_sha256,
            request_payload=request_payload,
            result=result,
            adapter_name=adapter.name,
            endpoint=cfg.base_url,
            selected_model=selected_model,
            started_at=started_at,
            ended_at=ended_at,
            wall_clock_seconds=duration,
            retry_count=retry_count,
            retain_raw=cfg.retain_raw_response,
        )
        task.attempt_count += 1
        transition_task(task, TaskStatus.RESPONSE_RECEIVED)
        write_json(run_dir / "task.json", task.to_dict())
        write_json(
            run_dir / "status.json",
            {
                "task_id": task.task_id,
                "status": task.status.value,
                "attempt_count": task.attempt_count,
                "prompt_sha256": prompt_sha256,
                "source_content_sha256": task.source_content_identity.sha256,
                "processing_stage": "NONE",
                "transport": report.to_dict(),
            },
        )
        return TaskRunResult(
            task=task,
            run_dir=run_dir,
            transport_report=report.to_dict(),
            duration_seconds=duration,
        )
    except ModelSelectionError as exc:
        ended_at = utc_now_iso()
        duration = time.perf_counter() - start
        save_transport_failure(
            run_dir,
            task=task,
            prompt_sha256=prompt_sha256,
            adapter_name=adapter.name,
            endpoint=cfg.base_url,
            selected_model=selected_model,
            started_at=started_at,
            ended_at=ended_at,
            wall_clock_seconds=duration,
            retry_count=retry_count,
            classification=exc.classification,
            message=str(exc),
            available_models=exc.available_models,
        )
        raise TaskRunError(str(exc), exit_code=4, classification="blocked") from exc
    except TransportError as exc:
        ended_at = utc_now_iso()
        duration = time.perf_counter() - start
        save_transport_failure(
            run_dir,
            task=task,
            prompt_sha256=prompt_sha256,
            adapter_name=adapter.name,
            endpoint=cfg.base_url,
            selected_model=selected_model,
            started_at=started_at,
            ended_at=ended_at,
            wall_clock_seconds=duration,
            retry_count=retry_count,
            classification=exc.classification,
            message=str(exc),
        )
        exit_code = 4 if exc.classification in {
            "endpoint_rejected",
            "configuration_error",
            "model_not_found",
            "model_selection_blocked",
        } else 1
        raise TaskRunError(str(exc), exit_code=exit_code, classification=exc.classification) from exc
