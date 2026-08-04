"""Provider-independent model adapters for Adventure Generator v2."""

from idne.model_adapter.base import (
    ModelAdapter,
    ModelConfig,
    ModelRequest,
    ModelResponse,
    ModelResultStatus,
)
from idne.model_adapter.registry import create_adapter

__all__ = [
    "ModelAdapter",
    "ModelConfig",
    "ModelRequest",
    "ModelResponse",
    "ModelResultStatus",
    "create_adapter",
]
