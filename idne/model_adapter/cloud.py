"""External cloud model adapter (generic HTTP JSON API)."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any

from idne.model_adapter.base import (
    ModelAdapter,
    ModelRequest,
    ModelResponse,
    ModelResultStatus,
)


class CloudModelAdapter(ModelAdapter):
    """POST prompt bundle to a configured remote endpoint."""

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
        if not self.config.endpoint_url:
            return ModelResponse(
                status=ModelResultStatus.ERROR,
                error="endpoint_url not configured",
                backend=self.config.backend,
                model_name=self.config.model_name,
            )

        body: dict[str, Any] = {
            "model": self.config.model_name,
            "temperature": self.config.temperature,
            "max_output_tokens": self.config.max_output_tokens,
            "stage_id": request.stage_id,
            "system_prompt": request.system_prompt,
            "user_prompt": request.user_prompt,
            "response_format": request.response_format,
            "metadata": request.metadata,
        }
        data = json.dumps(body).encode("utf-8")
        req = urllib.request.Request(
            self.config.endpoint_url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=self.config.timeout_seconds) as resp:
                raw = json.loads(resp.read().decode("utf-8"))
        except urllib.error.URLError as exc:
            return ModelResponse(
                status=ModelResultStatus.ERROR,
                error=str(exc),
                input_tokens_estimate=input_est,
                backend=self.config.backend,
                model_name=self.config.model_name,
            )

        text = raw.get("text", "") if isinstance(raw, dict) else str(raw)
        parsed = raw.get("parsed") if isinstance(raw, dict) else None
        if parsed is None and request.response_format == "json":
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
        return True
