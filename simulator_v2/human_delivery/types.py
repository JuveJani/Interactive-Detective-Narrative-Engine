"""Types for human-delivery static gamebook simulation."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any


class DeliveryDefectClass(str, Enum):
    DELIVERY = "delivery_defect"
    STORY_LOGIC = "story_logic_defect"


@dataclass
class DeliveryFinding:
    finding_id: str
    message: str
    defect_class: DeliveryDefectClass = DeliveryDefectClass.DELIVERY
    severity: str = "error"
    context: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "finding_id": self.finding_id,
            "message": self.message,
            "defect_class": self.defect_class.value,
            "severity": self.severity,
            "context": dict(self.context),
        }


@dataclass
class VisibleChoice:
    label: str
    destination_section: int | None = None
    branch_kind: str = "navigate"  # navigate | check_success | check_failure

    def to_dict(self) -> dict[str, Any]:
        return {
            "label": self.label,
            "destination_section": self.destination_section,
            "branch_kind": self.branch_kind,
        }


@dataclass
class ParsedSection:
    section_number: int
    unit_id: str
    body_excerpt: str
    choices: list[VisibleChoice] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "section_number": self.section_number,
            "unit_id": self.unit_id,
            "body_excerpt": self.body_excerpt,
            "choices": [c.to_dict() for c in self.choices],
        }


@dataclass
class AdventureWorkspace:
    workspace_root: Path
    adventure_root: Path
    manifest_path: Path
    gamebook_path: Path
    manifest: dict[str, Any]
    used_idne: bool = False

    @property
    def adventure_id(self) -> str:
        return str(self.manifest.get("adventure_id", self.workspace_root.name))


@dataclass
class HumanTraceStep:
    step: int
    public_section: int
    internal_unit_id: str
    visible_choices: list[VisibleChoice]
    chosen_label: str
    chosen_dest_section: int | None
    dest_internal_unit_id: str | None
    d20_roll: int | None = None
    check_branch: str | None = None
    player_visible_state: dict[str, Any] = field(default_factory=dict)
    route_equivalence: str = "PASS"
    blocked_reason: str | None = None
    author_only_access_attempted: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "step": self.step,
            "public_section": self.public_section,
            "internal_unit_id": self.internal_unit_id,
            "visible_choices": [c.to_dict() for c in self.visible_choices],
            "chosen_label": self.chosen_label,
            "chosen_dest_section": self.chosen_dest_section,
            "dest_internal_unit_id": self.dest_internal_unit_id,
            "d20_roll": self.d20_roll,
            "check_branch": self.check_branch,
            "player_visible_state": dict(self.player_visible_state),
            "route_equivalence": self.route_equivalence,
            "blocked_reason": self.blocked_reason,
            "author_only_access_attempted": self.author_only_access_attempted,
        }


@dataclass
class HumanDeliveryResult:
    status: str
    adventure_id: str
    start_file: str
    start_section: int
    steps: list[HumanTraceStep] = field(default_factory=list)
    ending_unit_id: str | None = None
    findings: list[DeliveryFinding] = field(default_factory=list)
    trust: dict[str, Any] = field(default_factory=dict)
    canonical_equivalence: str = "UNKNOWN"
    visited_sections: list[int] = field(default_factory=list)
    author_only_files_accessed: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "adventure_id": self.adventure_id,
            "start_file": self.start_file,
            "start_section": self.start_section,
            "steps": [s.to_dict() for s in self.steps],
            "ending_unit_id": self.ending_unit_id,
            "findings": [f.to_dict() for f in self.findings],
            "trust": dict(self.trust),
            "canonical_equivalence": self.canonical_equivalence,
            "visited_sections": list(self.visited_sections),
            "author_only_files_accessed": list(self.author_only_files_accessed),
        }
