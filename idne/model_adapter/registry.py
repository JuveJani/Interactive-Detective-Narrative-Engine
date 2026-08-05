"""Factory for model adapters."""

from __future__ import annotations

from typing import Any

from idne.model_adapter.base import ModelAdapter, ModelConfig
from idne.model_adapter.cli_runner import CliRunnerAdapter
from idne.model_adapter.cloud import CloudModelAdapter
from idne.model_adapter.mock import MockModelAdapter, build_mock_adapter
from idne.model_adapter.openai_compatible import OpenAICompatibleAdapter


def config_from_dict(data: dict[str, Any]) -> ModelConfig:
    return ModelConfig(
        backend=str(data.get("backend", "mock")),
        model_name=str(data.get("model_name", "mock-deterministic")),
        context_size=int(data.get("context_size", 8192)),
        temperature=float(data.get("temperature", 0.1)),
        max_output_tokens=int(data.get("max_output_tokens", 2048)),
        timeout_seconds=float(data.get("timeout_seconds", 120.0)),
        max_retries=int(data.get("max_retries", 2)),
        local_mode=bool(data.get("local_mode", True)),
        endpoint_url=str(data.get("endpoint_url", "")),
        cli_command=str(data.get("cli_command", "")),
        extra=dict(data.get("extra", {})),
    )


def create_adapter(config: ModelConfig | dict[str, Any] | None = None) -> ModelAdapter:
    cfg = config if isinstance(config, ModelConfig) else config_from_dict(config or {})
    backend = cfg.backend.lower()
    if backend == "mock":
        return build_mock_adapter(cfg)
    if backend in ("openai_compatible", "local_openai"):
        return OpenAICompatibleAdapter(cfg)
    if backend in ("cli", "cli_runner"):
        return CliRunnerAdapter(cfg)
    if backend in ("cloud", "remote"):
        return CloudModelAdapter(cfg)
    raise ValueError(f"unknown model backend: {cfg.backend}")
