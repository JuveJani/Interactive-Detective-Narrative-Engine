"""Persist model transport artifacts inside task run directories."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from idne.local_ai.config import endpoint_for_display
from idne.local_ai.lm_studio_client import CompletionResult
from idne.local_ai.run_state import write_json
from idne.local_ai.task_model import LocalAITask, utc_now_iso


@dataclass
class TransportReport:
    adapter: str
    endpoint: str
    selected_model: str
    started_at: str
    ended_at: str
    wall_clock_seconds: float
    retry_count: int
    http_status: int
    finish_reason: str | None
    usage: dict[str, int | None]
    response_character_count: int
    task_content_identity: dict[str, str]
    prompt_sha256: str
    classification: str
    success: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def redact_endpoint(base_url: str) -> str:
    return endpoint_for_display(base_url)


def save_transport_artifacts(
    run_dir: Path,
    *,
    task: LocalAITask,
    prompt_sha256: str,
    request_payload: dict[str, Any],
    result: CompletionResult,
    adapter_name: str,
    endpoint: str,
    selected_model: str,
    started_at: str,
    ended_at: str,
    wall_clock_seconds: float,
    retry_count: int,
    retain_raw: bool,
) -> TransportReport:
    write_json(run_dir / "request.json", request_payload)
    if retain_raw:
        write_json(run_dir / "raw_response.json", result.raw_response)
    (run_dir / "response.txt").write_text(result.content + "\n", encoding="utf-8")
    report = TransportReport(
        adapter=adapter_name,
        endpoint=redact_endpoint(endpoint),
        selected_model=selected_model,
        started_at=started_at,
        ended_at=ended_at,
        wall_clock_seconds=wall_clock_seconds,
        retry_count=retry_count,
        http_status=result.http_status,
        finish_reason=result.finish_reason,
        usage=result.usage,
        response_character_count=len(result.content),
        task_content_identity=task.source_content_identity.to_dict(),
        prompt_sha256=prompt_sha256,
        classification="success",
        success=True,
    )
    write_json(run_dir / "transport_report.json", report.to_dict())
    return report


def save_transport_failure(
    run_dir: Path,
    *,
    task: LocalAITask,
    prompt_sha256: str,
    adapter_name: str,
    endpoint: str,
    selected_model: str | None,
    started_at: str,
    ended_at: str,
    wall_clock_seconds: float,
    retry_count: int,
    classification: str,
    message: str,
    available_models: list[str] | None = None,
) -> None:
    report = {
        "adapter": adapter_name,
        "endpoint": redact_endpoint(endpoint),
        "selected_model": selected_model,
        "started_at": started_at,
        "ended_at": ended_at,
        "wall_clock_seconds": wall_clock_seconds,
        "retry_count": retry_count,
        "http_status": None,
        "finish_reason": None,
        "usage": {
            "prompt_tokens": None,
            "completion_tokens": None,
            "total_tokens": None,
        },
        "response_character_count": 0,
        "task_content_identity": task.source_content_identity.to_dict(),
        "prompt_sha256": prompt_sha256,
        "classification": classification,
        "success": False,
        "message": message,
        "available_models": available_models or [],
    }
    write_json(run_dir / "transport_report.json", report)
    diagnostics_path = run_dir / "diagnostics.json"
    diagnostics: dict[str, Any] = {}
    if diagnostics_path.is_file():
        diagnostics = json.loads(diagnostics_path.read_text(encoding="utf-8"))
    diagnostics["last_transport_failure"] = report
    write_json(diagnostics_path, diagnostics)
