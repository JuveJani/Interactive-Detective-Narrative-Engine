"""Model adapter interface and model selection."""

from __future__ import annotations

import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from idne.local_ai.config import LocalAIConfig
from idne.local_ai.errors import (
    ModelNotFoundTransportError,
    ModelSelectionError,
    TransportError,
)
from idne.local_ai.lm_studio_client import CompletionResult, ModelDescriptor


@dataclass
class ModelSelection:
    model_id: str
    reason: str
    available_models: list[str]


def select_model(cfg: LocalAIConfig, models: list[ModelDescriptor]) -> ModelSelection:
    ids = [m.model_id for m in models]
    if not ids:
        raise ModelSelectionError(
            "no models returned — load a model in LM Studio and start the local server"
        )
    if cfg.model:
        if cfg.model not in ids:
            raise ModelNotFoundTransportError(
                f"configured model not found: {cfg.model}; available: {', '.join(ids)}"
            )
        return ModelSelection(model_id=cfg.model, reason="configured", available_models=ids)
    if len(ids) == 1:
        return ModelSelection(model_id=ids[0], reason="single_available", available_models=ids)
    raise ModelSelectionError(
        "multiple models available — configure adapter.model explicitly",
        available_models=ids,
    )


class ModelAdapter(ABC):
    name: str

    @abstractmethod
    def list_models(self, cfg: LocalAIConfig) -> list[ModelDescriptor]:
        raise NotImplementedError

    @abstractmethod
    def complete(
        self,
        cfg: LocalAIConfig,
        *,
        model: str,
        user_prompt: str,
        max_output_tokens: int | None = None,
        temperature: float | None = None,
    ) -> CompletionResult:
        raise NotImplementedError


class LMStudioAdapter(ModelAdapter):
    name = "lm_studio"

    def list_models(self, cfg: LocalAIConfig) -> list[ModelDescriptor]:
        from idne.local_ai.lm_studio_client import list_models

        return list_models(cfg)

    def complete(
        self,
        cfg: LocalAIConfig,
        *,
        model: str,
        user_prompt: str,
        max_output_tokens: int | None = None,
        temperature: float | None = None,
    ) -> CompletionResult:
        from idne.local_ai.lm_studio_client import chat_completion

        return chat_completion(
            cfg,
            model=model,
            user_prompt=user_prompt,
            max_output_tokens=max_output_tokens,
            temperature=temperature,
        )


def create_adapter(cfg: LocalAIConfig, *, mock: bool = False) -> ModelAdapter:
    if mock or cfg.adapter_type == "mock":
        from idne.local_ai.mock_adapter import MockAdapter

        return MockAdapter()
    if cfg.adapter_type in {"lm_studio", "openai_compatible"}:
        return LMStudioAdapter()
    raise TransportError(f"unsupported adapter type: {cfg.adapter_type}", retryable=False)


def execute_with_retries(
    cfg: LocalAIConfig,
    operation: str,
    fn,
) -> Any:
    attempts = max(0, int(cfg.retry_count)) + 1
    delay = 0.5
    last_error: TransportError | None = None
    for attempt in range(attempts):
        try:
            return fn()
        except TransportError as exc:
            last_error = exc
            if not exc.retryable or attempt >= attempts - 1:
                raise
            time.sleep(delay)
            delay = min(delay * 2, 4.0)
    if last_error is not None:
        raise last_error
    raise TransportError(f"{operation} failed", retryable=False)
