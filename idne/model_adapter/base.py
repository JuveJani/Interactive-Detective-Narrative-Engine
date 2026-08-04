"""Base types for model adapters."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ModelResultStatus(str, Enum):
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"
    BLOCKED = "BLOCKED"
    TIMEOUT = "TIMEOUT"


@dataclass
class ModelConfig:
    backend: str = "mock"
    model_name: str = "mock-deterministic"
    context_size: int = 8192
    temperature: float = 0.1
    max_output_tokens: int = 2048
    timeout_seconds: float = 120.0
    max_retries: int = 2
    local_mode: bool = True
    endpoint_url: str = ""
    cli_command: str = ""
    extra: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "backend": self.backend,
            "model_name": self.model_name,
            "context_size": self.context_size,
            "temperature": self.temperature,
            "max_output_tokens": self.max_output_tokens,
            "timeout_seconds": self.timeout_seconds,
            "max_retries": self.max_retries,
            "local_mode": self.local_mode,
            "endpoint_url": self.endpoint_url,
            "cli_command": self.cli_command,
            "extra": self.extra,
        }


@dataclass
class ModelRequest:
    stage_id: str
    system_prompt: str
    user_prompt: str
    response_format: str = "json"
    metadata: dict[str, Any] = field(default_factory=dict)

    def estimated_input_tokens(self) -> int:
        text = self.system_prompt + self.user_prompt
        return max(1, len(text) // 4)


@dataclass
class ModelResponse:
    status: ModelResultStatus
    text: str = ""
    parsed: dict[str, Any] | None = None
    error: str = ""
    input_tokens_estimate: int = 0
    output_tokens_estimate: int = 0
    backend: str = ""
    model_name: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status.value,
            "text": self.text,
            "parsed": self.parsed,
            "error": self.error,
            "input_tokens_estimate": self.input_tokens_estimate,
            "output_tokens_estimate": self.output_tokens_estimate,
            "backend": self.backend,
            "model_name": self.model_name,
        }


class ModelAdapter:
    """Provider-independent model interface."""

    def __init__(self, config: ModelConfig) -> None:
        self.config = config

    def complete(self, request: ModelRequest) -> ModelResponse:
        raise NotImplementedError

    def requires_network(self) -> bool:
        return not self.config.local_mode
