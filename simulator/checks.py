"""D20 check resolution."""

from __future__ import annotations

import random
from typing import Any

from simulator.state import GameState


def roll_check(rng: random.Random, role: str, dc: int) -> tuple[bool, int]:
    focus = 2 if role == "people" else 2
    roll = rng.randint(1, 20) + focus
    return roll >= dc, roll


def apply_check_outcome(
    state: GameState,
    check_id: str,
    passed: bool,
    checks: dict[str, Any],
) -> int:
    spec = checks[check_id]
    extra = 0
    branch = spec["pass"] if passed else spec["fail"]
    for clue in branch.get("clues", []):
        state.grant_clue(clue)
    for clue in branch.get("partial_clues", []):
        state.grant_clue(clue)
    for flag in branch.get("flags", []):
        state.grant_flag(flag)
    extra = branch.get("extra_minutes", 0)
    return extra
