"""Runner configuration for Simulator v2."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class RunnerConfig:
    """Bounded defaults suitable for Acer Swift Go 14 (32 GB RAM, no GPU)."""

    output_base: str = "simulation_output_v2"
    memory_guard_mb: int = 4096
    max_runs: int = 10000
    max_states: int = 200_000
    exhaustive_timeout_seconds: float = 300.0
    monte_carlo_runs: int = 1000
    compare_runs_per_strategy: int = 100
    workers: int = 1
    progress_interval: int = 50
    deterministic: bool = True
    seed: int = 42
    strategy: str = "random_legal"
    resume_checkpoint: str = ""
    cancel_flag_path: str = ""

    def to_dict(self) -> dict:
        return {
            "output_base": self.output_base,
            "memory_guard_mb": self.memory_guard_mb,
            "max_runs": self.max_runs,
            "max_states": self.max_states,
            "exhaustive_timeout_seconds": self.exhaustive_timeout_seconds,
            "monte_carlo_runs": self.monte_carlo_runs,
            "compare_runs_per_strategy": self.compare_runs_per_strategy,
            "workers": self.workers,
            "progress_interval": self.progress_interval,
            "deterministic": self.deterministic,
            "seed": self.seed,
            "strategy": self.strategy,
        }
