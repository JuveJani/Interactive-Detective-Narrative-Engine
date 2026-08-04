"""Persistent generation state manager."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from idne.generate.stages import STAGE_ORDER


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _hash_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _hash_file(path: Path) -> str:
    return _hash_bytes(path.read_bytes())


@dataclass
class GenerationState:
    adventure_id: str
    brief_version: str = "1"
    workspace_root: str = ""
    stage_status: dict[str, str] = field(default_factory=dict)
    input_hashes: dict[str, str] = field(default_factory=dict)
    output_hashes: dict[str, str] = field(default_factory=dict)
    validator_results: dict[str, Any] = field(default_factory=dict)
    repair_attempts: list[dict[str, Any]] = field(default_factory=list)
    human_approvals: dict[str, dict[str, Any]] = field(default_factory=dict)
    invalidated_stages: list[str] = field(default_factory=list)
    model_metadata: dict[str, Any] = field(default_factory=dict)
    token_estimates: dict[str, Any] = field(default_factory=dict)
    timestamps: dict[str, str] = field(default_factory=dict)
    checkpoint_stage: str = ""
    logic_validation_complete: bool = False
    readiness_status: str = "IN_PROGRESS"
    player_mapping_manifest: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": "1.0",
            "adventure_id": self.adventure_id,
            "brief_version": self.brief_version,
            "workspace_root": self.workspace_root,
            "stage_status": self.stage_status,
            "input_hashes": self.input_hashes,
            "output_hashes": self.output_hashes,
            "validator_results": self.validator_results,
            "repair_attempts": self.repair_attempts,
            "human_approvals": self.human_approvals,
            "invalidated_stages": self.invalidated_stages,
            "model_metadata": self.model_metadata,
            "token_estimates": self.token_estimates,
            "timestamps": self.timestamps,
            "checkpoint_stage": self.checkpoint_stage,
            "logic_validation_complete": self.logic_validation_complete,
            "readiness_status": self.readiness_status,
            "player_mapping_manifest": self.player_mapping_manifest,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> GenerationState:
        return cls(
            adventure_id=str(data.get("adventure_id", "")),
            brief_version=str(data.get("brief_version", "1")),
            workspace_root=str(data.get("workspace_root", "")),
            stage_status=dict(data.get("stage_status", {})),
            input_hashes=dict(data.get("input_hashes", {})),
            output_hashes=dict(data.get("output_hashes", {})),
            validator_results=dict(data.get("validator_results", {})),
            repair_attempts=list(data.get("repair_attempts", [])),
            human_approvals=dict(data.get("human_approvals", {})),
            invalidated_stages=list(data.get("invalidated_stages", [])),
            model_metadata=dict(data.get("model_metadata", {})),
            token_estimates=dict(data.get("token_estimates", {})),
            timestamps=dict(data.get("timestamps", {})),
            checkpoint_stage=str(data.get("checkpoint_stage", "")),
            logic_validation_complete=bool(data.get("logic_validation_complete", False)),
            readiness_status=str(data.get("readiness_status", "IN_PROGRESS")),
            player_mapping_manifest=dict(data.get("player_mapping_manifest", {})),
        )


class GenerationStateManager:
    def __init__(self, workspace_root: Path) -> None:
        self.workspace_root = workspace_root.resolve()
        self.state_path = self.workspace_root / ".generation" / "generation_state.json"
        self.adventure_root = self.workspace_root / "adventure"
        self.state = self._load_or_create()

    def _load_or_create(self) -> GenerationState:
        if self.state_path.exists():
            data = json.loads(self.state_path.read_text(encoding="utf-8"))
            return GenerationState.from_dict(data)
        adventure_id = self.workspace_root.name
        state = GenerationState(
            adventure_id=adventure_id,
            workspace_root=str(self.workspace_root),
            timestamps={"created": _utc_now()},
        )
        for stage in STAGE_ORDER:
            state.stage_status[stage] = "PENDING"
        self.save(state)
        return state

    def save(self, state: GenerationState | None = None) -> None:
        if state is not None:
            self.state = state
        self.state.timestamps["updated"] = _utc_now()
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        self.state_path.write_text(
            json.dumps(self.state.to_dict(), indent=2),
            encoding="utf-8",
        )

    def set_stage_status(self, stage_id: str, status: str) -> None:
        self.state.stage_status[stage_id] = status
        self.state.checkpoint_stage = stage_id
        self.state.timestamps[f"stage_{stage_id}"] = _utc_now()
        self.save()

    def record_output_hash(self, stage_id: str, path: Path) -> None:
        if path.exists():
            self.state.output_hashes[stage_id] = _hash_file(path)
            self.save()

    def record_input_hash(self, key: str, path: Path) -> None:
        if path.exists():
            self.state.input_hashes[key] = _hash_file(path)
            self.save()

    def record_validator(self, stage_id: str, result: dict[str, Any]) -> None:
        self.state.validator_results[stage_id] = result
        self.save()

    def record_repair(self, entry: dict[str, Any]) -> None:
        entry = dict(entry)
        entry["timestamp"] = _utc_now()
        self.state.repair_attempts.append(entry)
        self.save()

    def approve(self, stage_id: str, approver: str = "human", note: str = "") -> None:
        self.state.human_approvals[stage_id] = {
            "approved_at": _utc_now(),
            "approver": approver,
            "note": note,
        }
        if stage_id in self.state.invalidated_stages:
            self.state.invalidated_stages.remove(stage_id)
        self.save()

    def invalidate_downstream(self, stage_id: str, reason: str) -> list[str]:
        from idne.generate.stages import downstream_stages

        affected = downstream_stages(stage_id)
        for s in affected:
            self.state.stage_status[s] = "INVALIDATED"
            if s not in self.state.invalidated_stages:
                self.state.invalidated_stages.append(s)
        self.state.repair_attempts.append(
            {
                "type": "invalidate_downstream",
                "from_stage": stage_id,
                "reason": reason,
                "affected": affected,
                "timestamp": _utc_now(),
            }
        )
        self.save()
        return affected

    def is_approved(self, stage_id: str) -> bool:
        return stage_id in self.state.human_approvals

    def needs_approval(self, stage_id: str) -> bool:
        from idne.generate.stages import STAGE_DEFINITIONS

        defn = STAGE_DEFINITIONS.get(stage_id)
        if not defn or not defn.requires_human_approval:
            return False
        return not self.is_approved(stage_id)
