"""Ending evaluation (uses hidden truth only here)."""

from __future__ import annotations

from typing import Any

from simulator.state import GameState


def evaluate_ending(state: GameState, adapter: dict[str, Any]) -> str:
    deadline = adapter.get("deadline_clock", 1380)
    truth = adapter.get("truth", {})
    culprit = truth.get("culprit")

    if state.clock >= deadline:
        return "E-904"
    if state.filed_without_accusation:
        return "E-905"

    tags = state.compute_proof_tags(adapter)
    all_proof = all(tags.values())
    any_proof = any(tags.values())

    if (
        "I-03" in state.infers_done
        and state.accused
        and all_proof
        and culprit
        and state.accused == culprit
    ):
        return "E-901"

    if state.accused and any_proof and not (
        all_proof and state.accused == culprit
    ):
        if all_proof and state.accused != culprit:
            return "E-902"
        return "E-902" if any_proof else "E-903"

    if state.accused:
        return "E-903"

    return "E-903"
