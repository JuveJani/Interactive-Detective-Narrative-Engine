"""OpenAI-compatible HTTP endpoint adapter (local LM Studio, etc.)."""

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


class OpenAICompatibleAdapter(ModelAdapter):
    """Calls a local or remote OpenAI-compatible chat completions API."""

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

        url = self.config.endpoint_url.rstrip("/") + "/v1/chat/completions"
        body: dict[str, Any] = {
            "model": self.config.model_name,
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_output_tokens,
            "messages": [
                {"role": "system", "content": request.system_prompt},
                {"role": "user", "content": request.user_prompt},
            ],
        }
        data = json.dumps(body).encode("utf-8")
        req = urllib.request.Request(
            url,
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

        text = raw.get("choices", [{}])[0].get("message", {}).get("content", "")
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
        return not self.config.local_mode
