"""HTTP transport errors for Local AI model adapters."""

from __future__ import annotations


class TransportError(RuntimeError):
    classification: str = "transport_error"

    def __init__(self, message: str, *, retryable: bool = False) -> None:
        super().__init__(message)
        self.retryable = retryable


class ConfigurationError(TransportError):
    classification = "configuration_error"

    def __init__(self, message: str) -> None:
        super().__init__(message, retryable=False)


class EndpointRejectedError(ConfigurationError):
    classification = "endpoint_rejected"


class ConnectionRefusedTransportError(TransportError):
    classification = "connection_refused"

    def __init__(self, message: str) -> None:
        super().__init__(message, retryable=True)


class ConnectionTimeoutTransportError(TransportError):
    classification = "connection_timeout"

    def __init__(self, message: str) -> None:
        super().__init__(message, retryable=True)


class ResponseTimeoutTransportError(TransportError):
    classification = "response_timeout"

    def __init__(self, message: str) -> None:
        super().__init__(message, retryable=True)


class HttpTransportError(TransportError):
    classification = "http_error"

    def __init__(self, message: str, *, status: int, retryable: bool = False) -> None:
        super().__init__(message, retryable=retryable)
        self.status = status


class MalformedJsonTransportError(TransportError):
    classification = "malformed_json"

    def __init__(self, message: str) -> None:
        super().__init__(message, retryable=False)


class UnsupportedResponseTransportError(TransportError):
    classification = "unsupported_response_shape"

    def __init__(self, message: str) -> None:
        super().__init__(message, retryable=False)


class ModelNotFoundTransportError(TransportError):
    classification = "model_not_found"

    def __init__(self, message: str) -> None:
        super().__init__(message, retryable=False)


class EmptyCompletionTransportError(TransportError):
    classification = "empty_completion"

    def __init__(self, message: str) -> None:
        super().__init__(message, retryable=False)


class ReasoningWithoutContentTransportError(EmptyCompletionTransportError):
    classification = "reasoning_without_content"

    def __init__(
        self,
        message: str,
        *,
        reasoning_character_count: int = 0,
        finish_reason: str | None = None,
    ) -> None:
        super().__init__(message)
        self.reasoning_character_count = reasoning_character_count
        self.finish_reason = finish_reason


class InterruptedTransportError(TransportError):
    classification = "interrupted_request"

    def __init__(self, message: str) -> None:
        super().__init__(message, retryable=False)


class ModelSelectionError(TransportError):
    classification = "model_selection_blocked"

    def __init__(self, message: str, *, available_models: list[str] | None = None) -> None:
        super().__init__(message, retryable=False)
        self.available_models = available_models or []
