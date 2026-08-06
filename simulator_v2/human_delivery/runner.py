"""CLI command handlers for human-delivery simulation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from simulator_v2.human_delivery.engine import HumanDeliveryEngine
from simulator_v2.human_delivery.loader import HumanDeliveryLoadError, resolve_adventure_workspace
from simulator_v2.human_delivery.validate import validate_human_delivery


def cmd_delivery_validate(adventure_path: str | Path) -> dict[str, Any]:
    workspace = resolve_adventure_workspace(adventure_path)
    return validate_human_delivery(workspace)


def cmd_human_trace(
    adventure_path: str | Path,
    seed: int = 42,
    strategy: str = "human_random_legal",
) -> dict[str, Any]:
    workspace = resolve_adventure_workspace(adventure_path)
    engine = HumanDeliveryEngine(workspace)
    result = engine.run_trace(strategy=strategy, seed=seed)
    return {"simulation_layer": "human_delivery", "result": result.to_dict()}


def cmd_human_simulate(
    adventure_path: str | Path,
    runs: int = 100,
    seed: int = 42,
    strategy: str = "human_random_legal",
) -> dict[str, Any]:
    workspace = resolve_adventure_workspace(adventure_path)
    engine = HumanDeliveryEngine(workspace)
    mc = engine.monte_carlo(runs=runs, seed=seed, strategy=strategy)
    return {"simulation_layer": "human_delivery", "result": mc}
