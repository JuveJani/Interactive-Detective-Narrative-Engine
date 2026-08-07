"""LM Studio OpenAI-compatible HTTP client (stdlib only)."""

from __future__ import annotations

import json
import socket
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from typing import Any

from idne.local_ai.config import LocalAIConfig, normalize_base_url, resolve_api_token
from idne.local_ai.errors import (
    ConnectionRefusedTransportError,
    ConnectionTimeoutTransportError,
    EmptyCompletionTransportError,
    HttpTransportError,
    InterruptedTransportError,
    MalformedJsonTransportError,
    ReasoningWithoutContentTransportError,
    ResponseTimeoutTransportError,
    UnsupportedResponseTransportError,
)

MAX_RESPONSE_BYTES = 8 * 1024 * 1024
SYSTEM_MESSAGE = (
    "You are an IDNE Local AI assistant. Return JSON only. "
    "Do not use Markdown fences. Do not add commentary outside JSON. "
    "Do not invent files, paths, or IDs. Obey protected-value rules in the user prompt."
)


@dataclass
class ModelDescriptor:
    model_id: str
    display_identifier: str | None = None
    owner: str | None = None
    raw_metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "model_id": self.model_id,
            "display_identifier": self.display_identifier,
            "owner": self.owner,
            "raw_metadata": self.raw_metadata,
        }


@dataclass
class ParsedCompletion:
    content: str
    finish_reason: str | None
    usage: dict[str, int | None]
    reasoning_content: str | None = None

    @property
    def reasoning_present(self) -> bool:
        return bool(self.reasoning_content and self.reasoning_content.strip())

    @property
    def reasoning_character_count(self) -> int:
        if not self.reasoning_content:
            return 0
        return len(self.reasoning_content)


@dataclass
class CompletionResult:
    content: str
    finish_reason: str | None
    usage: dict[str, int | None]
    http_status: int
    raw_response: dict[str, Any]
    duration_seconds: float
    reasoning_content: str | None = None
    reasoning_present: bool = False
    reasoning_character_count: int = 0


def _build_headers(cfg: LocalAIConfig) -> dict[str, str]:
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    token = resolve_api_token(cfg)
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def _request_json(
    cfg: LocalAIConfig,
    method: str,
    path: str,
    payload: dict[str, Any] | None = None,
) -> tuple[int, dict[str, Any], float]:
    base = normalize_base_url(cfg.base_url)
    url = f"{base}{path}"
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    headers = _build_headers(cfg)
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    start = time.perf_counter()
    try:
        with urllib.request.urlopen(
            req,
            timeout=cfg.response_timeout_seconds,
        ) as resp:
            raw = resp.read(MAX_RESPONSE_BYTES)
            duration = time.perf_counter() - start
            status = int(getattr(resp, "status", resp.getcode()))
    except urllib.error.HTTPError as exc:
        duration = time.perf_counter() - start
        raw = exc.read(MAX_RESPONSE_BYTES)
        status = exc.code
        retryable = status in {429, 500, 502, 503, 504}
        try:
            parsed = json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError:
            raise HttpTransportError(
                f"HTTP {status} from {url}",
                status=status,
                retryable=retryable,
            ) from exc
        raise HttpTransportError(
            f"HTTP {status} from {url}: {parsed}",
            status=status,
            retryable=retryable,
        ) from exc
    except urllib.error.URLError as exc:
        reason = exc.reason
        if isinstance(reason, socket.timeout):
            raise ResponseTimeoutTransportError(
                f"response timeout after {cfg.response_timeout_seconds}s: {url}"
            ) from exc
        if isinstance(reason, ConnectionRefusedError):
            raise ConnectionRefusedTransportError(
                f"connection refused: {url}"
            ) from exc
        if isinstance(reason, TimeoutError):
            raise ConnectionTimeoutTransportError(
                f"connection timeout: {url}"
            ) from exc
        raise ConnectionRefusedTransportError(f"connection failed: {url}: {reason}") from exc
    except TimeoutError as exc:
        raise ResponseTimeoutTransportError(
            f"response timeout after {cfg.response_timeout_seconds}s: {url}"
        ) from exc
    except KeyboardInterrupt as exc:
        raise InterruptedTransportError("request interrupted") from exc

    try:
        parsed = json.loads(raw.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise MalformedJsonTransportError(f"malformed JSON response from {url}") from exc
    if not isinstance(parsed, dict):
        raise UnsupportedResponseTransportError("top-level response is not a JSON object")
    return status, parsed, duration


def parse_models_response(data: dict[str, Any]) -> list[ModelDescriptor]:
    items = data.get("data")
    if not isinstance(items, list):
        raise UnsupportedResponseTransportError("models response missing data array")
    models: list[ModelDescriptor] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        model_id = str(item.get("id", "")).strip()
        if not model_id:
            continue
        models.append(
            ModelDescriptor(
                model_id=model_id,
                display_identifier=str(item.get("id")) if item.get("id") else None,
                owner=str(item.get("owned_by")) if item.get("owned_by") else None,
                raw_metadata=dict(item),
            )
        )
    return sorted(models, key=lambda m: m.model_id)


def list_models(cfg: LocalAIConfig) -> list[ModelDescriptor]:
    _status, data, _duration = _request_json(cfg, "GET", "/models")
    return parse_models_response(data)


def _extract_reasoning_content(message: dict[str, Any]) -> str | None:
    reasoning = message.get("reasoning_content")
    if isinstance(reasoning, str) and reasoning.strip():
        return reasoning
    return None


def parse_completion_response(data: dict[str, Any]) -> ParsedCompletion:
    choices = data.get("choices")
    if not isinstance(choices, list) or not choices:
        raise UnsupportedResponseTransportError("missing choices array")
    first = choices[0]
    if not isinstance(first, dict):
        raise UnsupportedResponseTransportError("first choice is not an object")
    message = first.get("message")
    if not isinstance(message, dict):
        raise UnsupportedResponseTransportError("missing message in first choice")
    if message.get("tool_calls"):
        raise UnsupportedResponseTransportError("tool-call-only response not supported")

    reasoning_content = _extract_reasoning_content(message)
    content_raw = message.get("content")
    finish_reason = first.get("finish_reason")
    finish = str(finish_reason) if finish_reason is not None else None
    usage_raw = data.get("usage") if isinstance(data.get("usage"), dict) else {}
    usage = {
        "prompt_tokens": usage_raw.get("prompt_tokens"),
        "completion_tokens": usage_raw.get("completion_tokens"),
        "total_tokens": usage_raw.get("total_tokens"),
    }

    if content_raw is None:
        if reasoning_content:
            raise ReasoningWithoutContentTransportError(
                "reasoning produced but no final content before output limit",
                reasoning_character_count=len(reasoning_content),
                finish_reason=finish,
            )
        raise EmptyCompletionTransportError("completion content is null")
    if not isinstance(content_raw, str):
        raise UnsupportedResponseTransportError("completion content is not a string")
    if not content_raw.strip():
        if reasoning_content:
            raise ReasoningWithoutContentTransportError(
                "reasoning produced but no final content before output limit",
                reasoning_character_count=len(reasoning_content),
                finish_reason=finish,
            )
        raise EmptyCompletionTransportError("completion content is blank")

    return ParsedCompletion(
        content=content_raw,
        finish_reason=finish,
        usage=usage,
        reasoning_content=reasoning_content,
    )


def extract_completion_content(data: dict[str, Any]) -> tuple[str, str | None, dict[str, int | None]]:
    parsed = parse_completion_response(data)
    return parsed.content, parsed.finish_reason, parsed.usage


def chat_completion(
    cfg: LocalAIConfig,
    *,
    model: str,
    user_prompt: str,
    max_output_tokens: int | None = None,
    temperature: float | None = None,
) -> CompletionResult:
    payload: dict[str, Any] = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_MESSAGE},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": temperature if temperature is not None else cfg.temperature,
        "max_tokens": max_output_tokens if max_output_tokens is not None else cfg.max_output_tokens,
        "stream": False,
    }
    if cfg.seed is not None:
        payload["seed"] = cfg.seed
    status, data, duration = _request_json(cfg, "POST", "/chat/completions", payload)
    parsed = parse_completion_response(data)
    return CompletionResult(
        content=parsed.content,
        finish_reason=parsed.finish_reason,
        usage=parsed.usage,
        http_status=status,
        raw_response=data,
        duration_seconds=duration,
        reasoning_content=parsed.reasoning_content,
        reasoning_present=parsed.reasoning_present,
        reasoning_character_count=parsed.reasoning_character_count,
    )
