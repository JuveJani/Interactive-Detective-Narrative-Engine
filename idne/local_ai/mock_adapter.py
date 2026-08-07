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
    ReasoningWithoutContentTransportError,
    ResponseTimeoutTransportError,
    UnsupportedResponseTransportError,
)
from idne.local_ai.lm_studio_client import CompletionResult, ModelDescriptor
from idne.local_ai.model_adapter import ModelAdapter


def _default_models() -> list[ModelDescriptor]:
    return [ModelDescriptor(model_id="mock-model", display_identifier="mock-model", owner="mock")]


@dataclass
class MockAdapterState:
    scenario: str = "success"
    models: list[ModelDescriptor] = field(default_factory=_default_models)
    configured_model: str | None = None
    http_status: int = 200


def _semantic_payload(digest: str) -> dict[str, Any]:
    return {
        "working_title": "Museum Night Audit",
        "premise": (
            "A contract security auditor investigates an impossible theft during a brief "
            "power outage at a regional museum."
        ),
        "setting": "regional museum during a night shift",
        "universe": "real world",
        "genre": "detective story",
        "realism_level": "grounded",
        "player_mode": "single_investigator",
        "investigator_character": "meticulous security auditor with forensic curiosity",
        "target_playtime_minutes": 90,
        "in_world_duration": "one night shift",
        "tone": "methodical, slightly tense",
        "difficulty": "standard fair-play mystery",
        "location_scale": "single museum building",
        "content_boundaries": "no graphic violence; no supernatural explanations",
        "opening_situation": (
            "The night watch reports a display case opened during a two-minute outage; "
            "the player arrives before insurance review."
        ),
        "initial_observable_facts": [
            "Emergency lighting is still active in the east wing.",
            "The outage timer log shows exactly two minutes without power.",
        ],
        "required_themes": ["fair-play mystery", "access-control puzzle"],
        "forbidden_themes": ["supernatural explanations"],
        "author_notes": f"mock deterministic semantic response {digest}",
    }


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
            raise EmptyCompletionTransportError("completion content is null")
        if scenario == "missing_choices":
            raise UnsupportedResponseTransportError("missing choices array")
        if scenario == "malformed_json":
            raise MalformedJsonTransportError("malformed JSON response")
        if scenario == "http_error":
            raise HttpTransportError("HTTP 500", status=500, retryable=True)
        if scenario == "reasoning_blank_content":
            raise ReasoningWithoutContentTransportError(
                "reasoning produced but no final content before output limit",
                reasoning_character_count=len(
                    "Extended internal reasoning consumed the output budget."
                ),
                finish_reason="length",
            )

        digest = hashlib.sha256(user_prompt.encode("utf-8")).hexdigest()[:12]
        content = self._build_response_content(scenario, digest)
        reasoning = None
        if scenario == "reasoning_with_content":
            reasoning = "Thinking step by step about the model response."
        raw = self._raw_response(
            content,
            usage={"prompt_tokens": 100, "completion_tokens": 50, "total_tokens": 150},
            reasoning_content=reasoning,
        )
        return self._wrap(raw, content, finish_reason="stop", reasoning_content=reasoning)

    def _build_response_content(self, scenario: str, digest: str) -> str:
        if scenario == "duplicate_key":
            return '{"premise":"x","premise":"y","universe":"real world"}'
        if scenario == "missing_required_field":
            payload = _semantic_payload(digest)
            payload.pop("opening_situation", None)
            return json.dumps(payload, indent=2, sort_keys=True)
        if scenario == "wrong_type":
            payload = _semantic_payload(digest)
            payload["target_playtime_minutes"] = "ninety"
            return json.dumps(payload, indent=2, sort_keys=True)
        if scenario == "unexpected_field":
            payload = _semantic_payload(digest)
            payload["task_id"] = "injected-task"
            return json.dumps(payload, indent=2, sort_keys=True)
        if scenario == "protected_field_injection":
            payload = _semantic_payload(digest)
            payload["adventure_id"] = "ADV-999"
            return json.dumps(payload, indent=2, sort_keys=True)
        if scenario == "invalid_playtime":
            payload = _semantic_payload(digest)
            payload["target_playtime_minutes"] = 0
            return json.dumps(payload, indent=2, sort_keys=True)
        if scenario == "empty_semantic_value":
            payload = _semantic_payload(digest)
            payload["premise"] = "   "
            return json.dumps(payload, indent=2, sort_keys=True)
        if scenario == "response_malformed_json":
            return "{not valid json"
        if scenario == "response_empty":
            return ""
        if scenario == "response_multiple_objects":
            a = json.dumps({"a": 1})
            b = json.dumps({"b": 2})
            return f"{a}\n{b}"

        payload = _semantic_payload(digest)
        body = json.dumps(payload, indent=2, sort_keys=True)
        if scenario == "fenced_json":
            return f"```json\n{body}\n```"
        if scenario == "commentary_json":
            return f"Here is the brief:\n{body}\nEnd of response."
        return body

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

    def _raw_response(
        self,
        content: str,
        usage: dict[str, int] | None = None,
        *,
        reasoning_content: str | None = None,
    ) -> dict[str, Any]:
        message: dict[str, Any] = {"role": "assistant", "content": content}
        if reasoning_content is not None:
            message["reasoning_content"] = reasoning_content
        return {
            "id": "mock-completion",
            "object": "chat.completion",
            "choices": [
                {
                    "index": 0,
                    "message": message,
                    "finish_reason": "stop",
                }
            ],
            "usage": usage or {},
        }

    def _wrap(
        self,
        raw: dict[str, Any],
        content: str,
        *,
        finish_reason: str | None,
        reasoning_content: str | None = None,
    ) -> CompletionResult:
        usage_raw = raw.get("usage") if isinstance(raw.get("usage"), dict) else {}
        usage = {
            "prompt_tokens": usage_raw.get("prompt_tokens"),
            "completion_tokens": usage_raw.get("completion_tokens"),
            "total_tokens": usage_raw.get("total_tokens"),
        }
        reasoning_present = bool(reasoning_content and reasoning_content.strip())
        return CompletionResult(
            content=content,
            finish_reason=finish_reason,
            usage=usage,
            http_status=self.state.http_status,
            raw_response=raw,
            duration_seconds=0.01,
            reasoning_content=reasoning_content,
            reasoning_present=reasoning_present,
            reasoning_character_count=len(reasoning_content) if reasoning_content else 0,
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
        max_output_tokens=cfg.doctor_probe_max_tokens,
        temperature=0.0,
    )
