"""Deterministic RNG for Simulator v2."""

from __future__ import annotations

import random


class DeterministicRNG:
    """Seeded random number generator for reproducible check rolls."""

    def __init__(self, seed: int = 42) -> None:
        self._rng = random.Random(seed)
        self.seed = seed

    def d20(self) -> int:
        return self._rng.randint(1, 20)

    def roll_check(self, modifier: int = 5) -> int:
        return self.d20() + modifier

    def choice(self, options: list):
        return self._rng.choice(options)

    def random(self) -> float:
        return self._rng.random()
