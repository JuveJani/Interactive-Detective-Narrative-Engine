"""Deterministic mock model backend for tests and offline dry-runs."""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

from idne.model_adapter.base import (
    ModelAdapter,
    ModelConfig,
    ModelRequest,
    ModelResponse,
    ModelResultStatus,
)

MOCK_ROOT = Path(__file__).resolve().parent.parent / "generate" / "mock_overlays"


class MockModelAdapter(ModelAdapter):
    """Returns deterministic stage overlays or JSON payloads."""

    def __init__(self, config: ModelConfig) -> None:
        super().__init__(config)
        custom = config.extra.get("overlay_root")
        self.overlay_root = Path(custom) if custom else MOCK_ROOT

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

        mode = str(request.metadata.get("play_mode", "single_investigator"))
        overlay = self.overlay_root / mode / request.stage_id
        payload: dict[str, Any] = {
            "stage_id": request.stage_id,
            "overlay_path": str(overlay) if overlay.is_dir() else "",
            "play_mode": mode,
        }

        if overlay.is_dir():
            payload["overlay_files"] = sorted(
                str(p.relative_to(overlay)).replace("\\", "/")
                for p in overlay.rglob("*")
                if p.is_file()
            )

        if request.stage_id == "adventure_brief":
            brief = request.metadata.get("brief", {})
            payload["brief_echo"] = brief

        text = json.dumps(payload, indent=2, sort_keys=True)
        return ModelResponse(
            status=ModelResultStatus.SUCCESS,
            text=text,
            parsed=payload,
            input_tokens_estimate=input_est,
            output_tokens_estimate=max(1, len(text) // 4),
            backend=self.config.backend,
            model_name=self.config.model_name,
        )

    def apply_overlay(self, stage_id: str, play_mode: str, adventure_root: Path) -> list[str]:
        overlay = self.overlay_root / play_mode / stage_id
        if not overlay.is_dir():
            return []
        applied: list[str] = []
        for src in overlay.rglob("*"):
            if not src.is_file():
                continue
            rel = src.relative_to(overlay)
            dest = adventure_root / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)
            applied.append(str(rel).replace("\\", "/"))
        return applied

    def requires_network(self) -> bool:
        return False


def build_mock_adapter(config: ModelConfig | None = None) -> MockModelAdapter:
    cfg = config or ModelConfig(backend="mock", local_mode=True)
    cfg.backend = "mock"
    return MockModelAdapter(cfg)
