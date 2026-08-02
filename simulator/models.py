"""Shared data models."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Finding:
    id: str
    severity: str
    confidence: str
    evidence: str
    file: str
    identifier: str
    expected_rule: str
    layer: str
    auto_fix_possible: bool
    human_approval_required: bool
    extra: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "severity": self.severity,
            "confidence": self.confidence,
            "evidence": self.evidence,
            "file": self.file,
            "identifier": self.identifier,
            "expected_rule": self.expected_rule,
            "layer": self.layer,
            "auto_fix_possible": self.auto_fix_possible,
            "human_approval_required": self.human_approval_required,
            **self.extra,
        }


@dataclass
class GraphEdge:
    source: str
    target: str
    label: str
    minutes: int
    role: str | None = None


@dataclass
class RunResult:
    seed: int
    strategy: str
    ending: str
    steps: int
    joint_minutes: int
    split_minutes: int
    wall_minutes: int
    clues: list[str]
    flags: list[str]
    proof_tags: list[str]
    accused: str | None
    path: list[str] = field(default_factory=list)
