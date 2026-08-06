"""Deterministic mock model adapter for automated tests."""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, field
from typing import Any

from idne.local_ai.config import LocalAIConfig
from idne.local_ai.errors import (
    ConnectionRefusedTransportError,
    ConnectionTimeoutTransportError,
    EmptyCompletionTransportError,
    HttpTransportError,
    MalformedJsonTransportError,
    ModelNotFoundTransportError,
    ModelSelectionError,
    ResponseTimeoutTransportError,
    UnsupportedResponseTransportError,
)
from idne.local_ai.lm_studio_client import CompletionResult, ModelDescriptor
from idne.local_ai.model_adapter import ModelAdapter


@dataclass
class MockAdapterState:
    scenario: str = "success"
    models: list[ModelDescriptor] = field(default_factory=list)
    configured_model: str | None = None
    http_status: int = 200


class MockAdapter(ModelAdapter):
    name = "mock"

    def __init__(self, state: MockAdapterState | None = None) -> None:
        self.state = state or MockAdapterState(
            models=[
                ModelDescriptor(model_id="mock-model", display_identifier="mock-model", owner="mock")
            ]
        )

    def list_models(self, cfg: LocalAIConfig) -> list[ModelDescriptor]:
        self._maybe_fail("list")
        if self.state.scenario == "empty_models":
            return []
        if self.state.scenario == "multiple_models":
            return sorted(
                [
                    ModelDescriptor(model_id="mock-a", owner="mock"),
                    ModelDescriptor(model_id="mock-b", owner="mock"),
                ],
                key=lambda m: m.model_id,
            )
        if self.state.scenario == "missing_configured_model":
            return [ModelDescriptor(model_id="other-model", owner="mock")]
        return list(self.state.models)

    def complete(
        self,
        cfg: LocalAIConfig,
        *,
        model: str,
        user_prompt: str,
        max_output_tokens: int | None = None,
        temperature: float | None = None,
    ) -> CompletionResult:
        self._maybe_fail("complete")
        scenario = self.state.scenario
        if scenario == "empty_completion":
            raw = self._raw_response("")
            return self._wrap(raw, "", finish_reason="stop")
        if scenario == "null_content":
            raw = {"choices": [{"message": {"content": None}, "finish_reason": "stop"}]}
            raise EmptyCompletionTransportError("completion content is null")
        if scenario == "missing_choices":
            raw = {"choices": []}
            raise UnsupportedResponseTransportError("missing choices array")
        if scenario == "malformed_json":
            raise MalformedJsonTransportError("malformed JSON response")
        if scenario == "http_error":
            raise HttpTransportError("HTTP 500", status=500, retryable=True)

        digest = hashlib.sha256(user_prompt.encode("utf-8")).hexdigest()[:12]
        payload = {
            "universe": "real world",
            "genre": "detective story",
            "realism_level": "grounded",
            "player_mode": "single_investigator",
            "investigator_character": "mock investigator",
            "target_playtime_minutes": 90,
            "in_world_duration": "one night",
            "tone": "methodical",
            "difficulty": "standard",
            "location_scale": "single building",
            "content_boundaries": "no graphic violence",
            "author_notes": f"mock deterministic response {digest}",
        }
        content = json.dumps(payload, indent=2, sort_keys=True)
        raw = self._raw_response(content, usage={"prompt_tokens": 100, "completion_tokens": 50, "total_tokens": 150})
        return self._wrap(raw, content, finish_reason="stop")

    def _maybe_fail(self, phase: str) -> None:
        scenario = self.state.scenario
        if scenario == "connection_refused":
            raise ConnectionRefusedTransportError("connection refused")
        if scenario == "connection_timeout":
            raise ConnectionTimeoutTransportError("connection timeout")
        if scenario == "response_timeout":
            raise ResponseTimeoutTransportError("response timeout")
        if scenario == "multiple_models" and phase == "list":
            return
        if scenario == "missing_configured_model" and phase == "list":
            return

    def _raw_response(self, content: str, usage: dict[str, int] | None = None) -> dict[str, Any]:
        return {
            "id": "mock-completion",
            "object": "chat.completion",
            "choices": [
                {
                    "index": 0,
                    "message": {"role": "assistant", "content": content},
                    "finish_reason": "stop",
                }
            ],
            "usage": usage or {},
        }

    def _wrap(self, raw: dict[str, Any], content: str, *, finish_reason: str | None) -> CompletionResult:
        usage_raw = raw.get("usage") if isinstance(raw.get("usage"), dict) else {}
        usage = {
            "prompt_tokens": usage_raw.get("prompt_tokens"),
            "completion_tokens": usage_raw.get("completion_tokens"),
            "total_tokens": usage_raw.get("total_tokens"),
        }
        return CompletionResult(
            content=content,
            finish_reason=finish_reason,
            usage=usage,
            http_status=self.state.http_status,
            raw_response=raw,
            duration_seconds=0.01,
        )


def doctor_completion(cfg: LocalAIConfig, *, mock: bool = False) -> CompletionResult:
    adapter = MockAdapter() if mock else __import__("idne.local_ai.model_adapter", fromlist=["create_adapter"]).create_adapter(cfg)
    models = adapter.list_models(cfg)
    from idne.local_ai.model_adapter import select_model

    selection = select_model(cfg, models)
    prompt = '{"status":"ok","probe":"doctor"}'
    return adapter.complete(
        cfg,
        model=selection.model_id,
        user_prompt=prompt,
        max_output_tokens=32,
        temperature=0.0,
    )
