"""Runtime limits tuned for Termux on Google Pixel 10 Pro."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SimConfig:
    max_runs: int = 50_000
    max_states: int = 500_000
    max_path_steps: int = 500
    max_recursion_depth: int = 64
    timeout_seconds: int = 600
    progress_interval: int = 250
    default_seed: int = 42
    memory_guard_mb: int = 256
    partial_save_on_interrupt: bool = True


DEFAULT_CONFIG = SimConfig()

LAYERS = (
    "ENGINE",
    "ADVENTURE",
    "DELIVERY_ADAPTER",
    "PLAYER_PACKAGE",
    "VALIDATOR",
    "SIMULATOR",
    "HUMAN_PLAYTEST",
)

SEVERITIES = ("critical", "major", "minor", "info")
