"""Command-line local model runner adapter."""

from __future__ import annotations

import json
import subprocess
from typing import Any

from idne.model_adapter.base import (
    ModelAdapter,
    ModelRequest,
    ModelResponse,
    ModelResultStatus,
)


class CliRunnerAdapter(ModelAdapter):
    """Invokes a configured shell command with prompt on stdin."""

    def complete(self, request: ModelRequest) -> ModelResponse:
        input_est = request.estimated_input_tokens()
        if input_est > self.config.context_size:
            return ModelResponse(
                status=ModelResultStatus.BLOCKED,
                error="context budget exceeded",
                input_tokens_estimate=input_est,
                backend=self.config.backend,
                model_name=self.config.model_name,
            )
        if not self.config.cli_command:
            return ModelResponse(
                status=ModelResultStatus.ERROR,
                error="cli_command not configured",
                backend=self.config.backend,
                model_name=self.config.model_name,
            )

        payload = {
            "system": request.system_prompt,
            "user": request.user_prompt,
            "stage_id": request.stage_id,
            "metadata": request.metadata,
        }
        try:
            proc = subprocess.run(
                self.config.cli_command,
                input=json.dumps(payload),
                capture_output=True,
                text=True,
                timeout=self.config.timeout_seconds,
                shell=True,
                check=False,
            )
        except subprocess.TimeoutExpired:
            return ModelResponse(
                status=ModelResultStatus.TIMEOUT,
                error="cli runner timeout",
                input_tokens_estimate=input_est,
                backend=self.config.backend,
                model_name=self.config.model_name,
            )

        if proc.returncode != 0:
            return ModelResponse(
                status=ModelResultStatus.ERROR,
                error=proc.stderr or f"exit {proc.returncode}",
                input_tokens_estimate=input_est,
                backend=self.config.backend,
                model_name=self.config.model_name,
            )

        text = proc.stdout.strip()
        parsed: dict[str, Any] | None = None
        if request.response_format == "json":
            try:
                parsed = json.loads(text)
            except json.JSONDecodeError:
                parsed = None
        return ModelResponse(
            status=ModelResultStatus.SUCCESS,
            text=text,
            parsed=parsed,
            input_tokens_estimate=input_est,
            output_tokens_estimate=max(1, len(text) // 4),
            backend=self.config.backend,
            model_name=self.config.model_name,
        )

    def requires_network(self) -> bool:
        return False
