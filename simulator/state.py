"""Game state and proof evaluation."""

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from typing import Any


def _fmt_clock(minutes: int) -> str:
    h, m = divmod(minutes, 60)
    return f"{h:02d}:{m:02d}"


@dataclass
class GameState:
    node: str
    clock: int
    clues: set[str] = field(default_factory=set)
    flags: set[str] = field(default_factory=set)
    infers_done: set[str] = field(default_factory=set)
    accused: str | None = None
    follow_ups_used: int = 0
    follow_up_use_counts: dict[str, int] = field(default_factory=dict)
    visited: set[str] = field(default_factory=set)
    hub_visits: dict[int, set[str]] = field(default_factory=dict)
    role_nodes: dict[str, str] = field(default_factory=dict)
    role_minutes: dict[str, int] = field(default_factory=lambda: {"people": 0, "records": 0})
    joint_minutes: int = 0
    split_segments: list[dict[str, Any]] = field(default_factory=list)
    path: list[str] = field(default_factory=list)
    steps: int = 0
    filed_without_accusation: bool = False
    rng_roll: int | None = None
    entry_cost_prepaid: bool = False
    pending_followup: str | None = None
    return_hub: str | None = None
    states_explored: int = 0

    def clone(self) -> "GameState":
        return copy.deepcopy(self)

    def has_clue(self, clue: str) -> bool:
        return clue in self.clues

    def has_flag(self, flag: str) -> bool:
        return flag in self.flags

    def grant_clue(self, clue: str) -> bool:
        if clue in self.clues:
            return False
        self.clues.add(clue)
        return True

    def grant_flag(self, flag: str) -> None:
        self.flags.add(flag)

    def apply_thresholds(self, adapter: dict[str, Any]) -> None:
        for th in adapter.get("thresholds", []):
            if self.clock >= th["clock_min"]:
                self.flags.add(th["id"])

    def compute_proof_tags(self, adapter: dict[str, Any]) -> dict[str, bool]:
        c = self.clues
        mw = "MOTIVE_WITNESS" in self.flags
        return {
            "PROOF_METHOD": ("C-01" in c and "C-04" in c) or "C-10" in c,
            "PROOF_MOTIVE": (
                "C-05" in c
                or "C-11" in c
                or (mw and ("C-05" in c or "C-11" in c or "C-14" in c))
            ),
            "PROOF_OPPORTUNITY": "C-06" in c and ("C-12" in c or "C-13" in c),
        }

    def can_complete_infer(self, infer_id: str, adapter: dict[str, Any]) -> bool:
        req = adapter["infer_requirements"].get(infer_id, {})
        if infer_id == "I-01":
            needed = set(req.get("clues", []))
            return needed.issubset(self.clues)
        if infer_id == "I-02":
            pool = req.get("min_of", [])
            count = req.get("count", 3)
            held = sum(
                1
                for item in pool
                if (item in self.clues or item in self.flags)
            )
            return held >= count
        if infer_id == "I-03":
            tags = self.compute_proof_tags(adapter)
            return all(tags.get(t) for t in req.get("requires_proof_tags", [])) and bool(
                self.accused
            )
        return False

    def snapshot(self) -> dict[str, Any]:
        tags = {k: v for k, v in self.compute_proof_tags({}).items()}
        return {
            "node": self.node,
            "clock": self.clock,
            "clock_fmt": _fmt_clock(self.clock),
            "clues": sorted(self.clues),
            "flags": sorted(self.flags),
            "infers": sorted(self.infers_done),
            "accused": self.accused,
            "joint_minutes": self.joint_minutes,
            "role_minutes": dict(self.role_minutes),
        }
