"""Local AI task model, status transitions, and serialization."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any

TASK_SCHEMA_VERSION = "1.0"


class TaskStatus(str, Enum):
    CREATED = "CREATED"
    PREPARED = "PREPARED"
    BLOCKED = "BLOCKED"
    READY_FOR_MODEL = "READY_FOR_MODEL"
    RESPONSE_RECEIVED = "RESPONSE_RECEIVED"
    VALIDATED = "VALIDATED"
    FAILED = "FAILED"
    APPLIED = "APPLIED"


ALLOWED_TRANSITIONS: dict[TaskStatus, frozenset[TaskStatus]] = {
    TaskStatus.CREATED: frozenset(
        {TaskStatus.PREPARED, TaskStatus.BLOCKED, TaskStatus.READY_FOR_MODEL}
    ),
    TaskStatus.PREPARED: frozenset({TaskStatus.READY_FOR_MODEL, TaskStatus.BLOCKED}),
    TaskStatus.BLOCKED: frozenset({TaskStatus.CREATED, TaskStatus.PREPARED}),
    TaskStatus.READY_FOR_MODEL: frozenset(
        {TaskStatus.RESPONSE_RECEIVED, TaskStatus.BLOCKED, TaskStatus.FAILED}
    ),
    TaskStatus.RESPONSE_RECEIVED: frozenset(
        {TaskStatus.VALIDATED, TaskStatus.FAILED, TaskStatus.BLOCKED}
    ),
    TaskStatus.VALIDATED: frozenset({TaskStatus.APPLIED, TaskStatus.FAILED}),
    TaskStatus.FAILED: frozenset({TaskStatus.CREATED, TaskStatus.PREPARED}),
    TaskStatus.APPLIED: frozenset(),
}


REQUIRED_TASK_FIELDS = (
    "schema_version",
    "task_id",
    "task_type",
    "created_at",
    "source_content_identity",
    "allowed_input_files",
    "allowed_output_files",
    "authoritative_sources",
    "approved_prior_stage_facts",
    "protected_values",
    "expected_output_schema_ref",
    "context_budget",
    "generation_settings",
    "validator_commands",
    "status",
    "attempt_count",
    "run_directory",
)


@dataclass
class SourceIdentity:
    sha256: str
    path: str

    def to_dict(self) -> dict[str, str]:
        return {"sha256": self.sha256, "path": self.path}


@dataclass
class AuthoritativeSource:
    path: str
    authority_rank: int
    kind: str
    heading: str
    char_count: int
    excerpt_chars: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class LocalAITask:
    schema_version: str
    task_id: str
    task_type: str
    created_at: str
    source_content_identity: SourceIdentity
    allowed_input_files: list[str]
    allowed_output_files: list[str]
    authoritative_sources: list[AuthoritativeSource]
    approved_prior_stage_facts: dict[str, Any]
    protected_values: dict[str, Any]
    expected_output_schema_ref: str
    context_budget: int
    generation_settings: dict[str, Any]
    validator_commands: list[str]
    status: TaskStatus
    attempt_count: int
    run_directory: str
    stage_name: str | None = None
    adventure_id: str | None = None
    task_instruction: str = ""

    def to_dict(self) -> dict[str, Any]:
        data = {
            "schema_version": self.schema_version,
            "task_id": self.task_id,
            "task_type": self.task_type,
            "stage_name": self.stage_name,
            "adventure_id": self.adventure_id,
            "created_at": self.created_at,
            "source_content_identity": self.source_content_identity.to_dict(),
            "allowed_input_files": list(self.allowed_input_files),
            "allowed_output_files": list(self.allowed_output_files),
            "authoritative_sources": [s.to_dict() for s in self.authoritative_sources],
            "approved_prior_stage_facts": dict(self.approved_prior_stage_facts),
            "protected_values": dict(self.protected_values),
            "expected_output_schema_ref": self.expected_output_schema_ref,
            "context_budget": self.context_budget,
            "generation_settings": dict(self.generation_settings),
            "validator_commands": list(self.validator_commands),
            "status": self.status.value,
            "attempt_count": self.attempt_count,
            "run_directory": self.run_directory,
            "task_instruction": self.task_instruction,
        }
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> LocalAITask:
        for field_name in REQUIRED_TASK_FIELDS:
            if field_name not in data:
                raise ValueError(f"missing task field: {field_name}")
        identity = data["source_content_identity"]
        return cls(
            schema_version=str(data["schema_version"]),
            task_id=str(data["task_id"]),
            task_type=str(data["task_type"]),
            stage_name=data.get("stage_name"),
            adventure_id=data.get("adventure_id"),
            created_at=str(data["created_at"]),
            source_content_identity=SourceIdentity(
                sha256=str(identity["sha256"]),
                path=str(identity["path"]),
            ),
            allowed_input_files=[str(p) for p in data["allowed_input_files"]],
            allowed_output_files=[str(p) for p in data["allowed_output_files"]],
            authoritative_sources=[
                AuthoritativeSource(**src) for src in data["authoritative_sources"]
            ],
            approved_prior_stage_facts=dict(data["approved_prior_stage_facts"]),
            protected_values=dict(data["protected_values"]),
            expected_output_schema_ref=str(data["expected_output_schema_ref"]),
            context_budget=int(data["context_budget"]),
            generation_settings=dict(data["generation_settings"]),
            validator_commands=[str(c) for c in data["validator_commands"]],
            status=TaskStatus(str(data["status"])),
            attempt_count=int(data["attempt_count"]),
            run_directory=str(data["run_directory"]),
            task_instruction=str(data.get("task_instruction", "")),
        )


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode("utf-8"))


def stable_task_identity(task_type: str, input_paths: list[str], input_hashes: list[str]) -> str:
    payload = json.dumps(
        {"task_type": task_type, "input_paths": input_paths, "input_hashes": input_hashes},
        sort_keys=True,
        separators=(",", ":"),
    )
    return sha256_text(payload)


def make_task_id(task_type: str, input_paths: list[str], input_hashes: list[str]) -> str:
    digest = stable_task_identity(task_type, input_paths, input_hashes)[:12]
    return f"{task_type}-{digest}"


def validate_task_schema(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for field_name in REQUIRED_TASK_FIELDS:
        if field_name not in data:
            errors.append(f"missing field: {field_name}")
    if data.get("schema_version") != TASK_SCHEMA_VERSION:
        errors.append("unsupported schema_version")
    status = data.get("status")
    if status is not None:
        try:
            TaskStatus(str(status))
        except ValueError:
            errors.append(f"invalid status: {status}")
    return errors


def assert_valid_transition(current: TaskStatus, new: TaskStatus) -> None:
    allowed = ALLOWED_TRANSITIONS.get(current, frozenset())
    if new not in allowed:
        raise ValueError(f"invalid status transition: {current.value} -> {new.value}")


def transition_task(task: LocalAITask, new_status: TaskStatus) -> LocalAITask:
    assert_valid_transition(task.status, new_status)
    task.status = new_status
    return task
