"""Local AI configuration loading and endpoint policy."""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from idne.local_ai.errors import ConfigurationError, EndpointRejectedError
from idne.local_ai.paths import find_repo_root

DEFAULT_BASE_URL = "http://127.0.0.1:1234/v1"
LOOPBACK_HOSTS = frozenset({"127.0.0.1", "localhost", "::1", "[::1]"})


def _load_toml(path: Path) -> dict[str, Any]:
    data = path.read_bytes()
    if sys.version_info >= (3, 11):
        import tomllib

        return tomllib.loads(data.decode("utf-8"))
    return _parse_minimal_toml(data.decode("utf-8"))


def _parse_minimal_toml(text: str) -> dict[str, Any]:
    """Subset TOML parser for simple Local AI config (Python 3.10 fallback)."""
    root: dict[str, Any] = {}
    section: dict[str, Any] = root
    section_name = ""
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("[") and line.endswith("]"):
            section_name = line[1:-1].strip()
            section = root.setdefault(section_name, {})
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if value.startswith('"') and value.endswith('"'):
            parsed: Any = value[1:-1]
        elif value.startswith("'") and value.endswith("'"):
            parsed = value[1:-1]
        elif value.lower() in {"true", "false"}:
            parsed = value.lower() == "true"
        elif "." in value:
            try:
                parsed = float(value)
            except ValueError:
                parsed = value
        else:
            try:
                parsed = int(value)
            except ValueError:
                parsed = value
        section[key] = parsed
    return root


@dataclass
class LocalAIConfig:
    adapter_type: str = "lm_studio"
    base_url: str = DEFAULT_BASE_URL
    model: str | None = None
    api_token_env: str = "LM_STUDIO_API_TOKEN"
    connect_timeout_seconds: float = 10.0
    response_timeout_seconds: float = 300.0
    retry_count: int = 2
    temperature: float = 0.1
    max_output_tokens: int = 2048
    seed: int | None = None
    context_budget: int = 12000
    allow_remote_endpoint: bool = False
    retain_raw_response: bool = True
    log_requests: bool = False
    config_path: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "adapter_type": self.adapter_type,
            "base_url": self.base_url,
            "model": self.model,
            "api_token_env": self.api_token_env,
            "connect_timeout_seconds": self.connect_timeout_seconds,
            "response_timeout_seconds": self.response_timeout_seconds,
            "retry_count": self.retry_count,
            "temperature": self.temperature,
            "max_output_tokens": self.max_output_tokens,
            "seed": self.seed,
            "context_budget": self.context_budget,
            "allow_remote_endpoint": self.allow_remote_endpoint,
            "retain_raw_response": self.retain_raw_response,
            "log_requests": self.log_requests,
            "config_path": self.config_path,
        }


def normalize_base_url(base_url: str) -> str:
    raw = base_url.strip().rstrip("/")
    parsed = urlparse(raw)
    if parsed.scheme not in {"http", "https"}:
        raise ConfigurationError(f"unsupported URL scheme: {parsed.scheme or '(none)'}")
    if not parsed.netloc:
        raise ConfigurationError(f"invalid base URL: {base_url}")
    path = parsed.path.rstrip("/")
    if path.endswith("/v1"):
        normalized_path = path
    elif path in {"", "/"}:
        normalized_path = "/v1"
    else:
        normalized_path = f"{path}/v1"
    return f"{parsed.scheme}://{parsed.netloc}{normalized_path}"


def endpoint_for_display(base_url: str) -> str:
    return normalize_base_url(base_url)


def validate_endpoint_policy(base_url: str, *, allow_remote_endpoint: bool) -> None:
    normalized = normalize_base_url(base_url)
    parsed = urlparse(normalized)
    host = (parsed.hostname or "").lower()
    if host in LOOPBACK_HOSTS:
        return
    if allow_remote_endpoint:
        return
    raise EndpointRejectedError(
        f"endpoint {parsed.scheme}://{parsed.netloc} is not loopback; "
        "set allow_remote_endpoint = true to permit LAN or remote hosts"
    )


def _merge_section(data: dict[str, Any], cfg: LocalAIConfig) -> LocalAIConfig:
    adapter = data.get("adapter", {}) or {}
    transport = data.get("transport", {}) or {}
    runtime = data.get("runtime", {}) or {}
    if "type" in adapter:
        cfg.adapter_type = str(adapter["type"])
    if "base_url" in adapter:
        cfg.base_url = str(adapter["base_url"])
    if "model" in adapter:
        model = adapter["model"]
        cfg.model = str(model) if model not in (None, "") else None
    if "api_token_env" in adapter:
        cfg.api_token_env = str(adapter["api_token_env"])
    if "allow_remote_endpoint" in adapter:
        cfg.allow_remote_endpoint = bool(adapter["allow_remote_endpoint"])
    if "connect_timeout_seconds" in transport:
        cfg.connect_timeout_seconds = float(transport["connect_timeout_seconds"])
    if "response_timeout_seconds" in transport:
        cfg.response_timeout_seconds = float(transport["response_timeout_seconds"])
    if "retry_count" in transport:
        cfg.retry_count = int(transport["retry_count"])
    if "temperature" in transport:
        cfg.temperature = float(transport["temperature"])
    if "max_output_tokens" in transport:
        cfg.max_output_tokens = int(transport["max_output_tokens"])
    if "seed" in transport:
        seed = transport["seed"]
        cfg.seed = int(seed) if seed is not None else None
    if "context_budget" in runtime:
        cfg.context_budget = int(runtime["context_budget"])
    if "retain_raw_response" in runtime:
        cfg.retain_raw_response = bool(runtime["retain_raw_response"])
    if "log_requests" in runtime:
        cfg.log_requests = bool(runtime["log_requests"])
    return cfg


def load_config(
    *,
    config_path: Path | None = None,
    repo_root: Path | None = None,
) -> LocalAIConfig:
    root = repo_root or find_repo_root()
    cfg = LocalAIConfig()
    chosen: Path | None = None

    if config_path is not None:
        chosen = config_path.resolve()
    else:
        env_path = os.environ.get("IDNE_LOCAL_AI_CONFIG")
        if env_path:
            chosen = Path(env_path).resolve()
        else:
            local = root / "local_ai.toml"
            if local.is_file():
                chosen = local

    if chosen is not None:
        if not chosen.is_file():
            raise ConfigurationError(f"config file not found: {chosen}")
        cfg = _merge_section(_load_toml(chosen), cfg)
        cfg.config_path = chosen.as_posix()

    cfg.base_url = normalize_base_url(cfg.base_url)
    if os.environ.get("IDNE_LOCAL_AI_BASE_URL"):
        cfg.base_url = normalize_base_url(os.environ["IDNE_LOCAL_AI_BASE_URL"])
    if os.environ.get("IDNE_LOCAL_AI_MODEL"):
        cfg.model = os.environ["IDNE_LOCAL_AI_MODEL"].strip() or None
    if os.environ.get("IDNE_LOCAL_AI_ADAPTER"):
        cfg.adapter_type = os.environ["IDNE_LOCAL_AI_ADAPTER"].strip()
    validate_endpoint_policy(cfg.base_url, allow_remote_endpoint=cfg.allow_remote_endpoint)
    return cfg


def resolve_api_token(cfg: LocalAIConfig) -> str | None:
    token = os.environ.get(cfg.api_token_env, "").strip()
    return token or None
