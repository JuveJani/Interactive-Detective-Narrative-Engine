"""Player strategies — blind to simulator truth and future clues."""

from __future__ import annotations

import random
from typing import Any

from simulator.state import GameState

ACTION_PRIORITY = {
    "stairwell": 4,
    "split1": 6,
    "split2": 6,
    "park": 3,
    "duplicates": 5,
    "boot": 4,
    "press": 3,
    "rent": 3,
    "logs": 3,
    "invoices": 3,
    "accuse": 5,
    "decline": 0,
    "notes": 1,
    "timeline": 2,
    "manager_key": 4,
    "stairwell_revisit": 1,
    "relationship": 1,
    "whereabouts": 2,
    "skim": 0,
    "invoice_box": 2,
}


def _pick(rng: random.Random, options: list[dict[str, Any]]) -> dict[str, Any]:
    return rng.choice(options) if options else {"target": "J-120", "id": "fallback", "minutes": 0}


def _proof_count(state: GameState, adapter: dict[str, Any]) -> int:
    return sum(1 for v in state.compute_proof_tags(adapter).values() if v)


class Strategy:
    name = "base"

    def __init__(self, rng: random.Random, adapter: dict[str, Any] | None = None):
        self.rng = rng
        self.adapter = adapter or {}
        self.suspects = list(self.adapter.get("suspects", []))

    def choose(self, state: GameState, options: list[dict[str, Any]], role: str) -> dict[str, Any]:
        if role == "accuse":
            return {"target": self.pick_accused(state)}
        if not options:
            return {"target": state.node, "minutes": 0}
        return _pick(self.rng, options)

    def pick_accused(self, state: GameState) -> str:
        """Choose from public suspect list using proof tags only — no truth/culprit access."""
        tags = state.compute_proof_tags(self.adapter)
        if self.suspects:
            if all(tags.values()):
                return self.rng.choice(self.suspects)
            return self.rng.choice(self.suspects)
        return "Unknown"


class RandomStrategy(Strategy):
    name = "random"

    def choose(self, state: GameState, options: list[dict[str, Any]], role: str) -> dict[str, Any]:
        if role == "accuse":
            return {"target": self.pick_accused(state)}
        return _pick(self.rng, options)


class ClueSeekingStrategy(Strategy):
    name = "clue-seeking"

    def choose(self, state: GameState, options: list[dict[str, Any]], role: str) -> dict[str, Any]:
        if role == "accuse":
            return {"target": self.pick_accused(state)}
        if not options:
            return {"target": state.node, "minutes": 0}
        scored = sorted(
            options,
            key=lambda o: (ACTION_PRIORITY.get(o.get("id", ""), 1), -o.get("minutes", 0)),
            reverse=True,
        )
        top = ACTION_PRIORITY.get(scored[0].get("id", ""), 1)
        best = [o for o in scored if ACTION_PRIORITY.get(o.get("id", ""), 1) == top]
        return _pick(self.rng, best)


class BroadExplorationStrategy(Strategy):
    name = "broad-exploration"

    def __init__(self, rng: random.Random, adapter: dict[str, Any] | None = None):
        super().__init__(rng, adapter)
        self.seen: set[str] = set()

    def choose(self, state: GameState, options: list[dict[str, Any]], role: str) -> dict[str, Any]:
        if role == "accuse":
            return {"target": self.pick_accused(state)}
        novel = [o for o in options if o.get("id") not in self.seen]
        pick = _pick(self.rng, novel or options)
        self.seen.add(pick.get("id", pick["target"]))
        return pick


class TimeEfficientStrategy(Strategy):
    name = "time-efficient"

    def choose(self, state: GameState, options: list[dict[str, Any]], role: str) -> dict[str, Any]:
        if role == "accuse":
            return {"target": self.pick_accused(state)}
        deadline = self.adapter.get("deadline_clock", 1380)
        if state.clock >= deadline - 60:
            acc = [o for o in options if o.get("id") == "accuse"]
            if acc:
                return acc[0]
        if state.clock >= deadline - 120 and any(o.get("id") == "split2" for o in options):
            return next(o for o in options if o.get("id") == "split2")
        return min(options, key=lambda o: o.get("minutes", 0))


class CautiousStrategy(Strategy):
    name = "cautious"

    def choose(self, state: GameState, options: list[dict[str, Any]], role: str) -> dict[str, Any]:
        if role == "accuse":
            tags = state.compute_proof_tags(self.adapter)
            if all(tags.values()):
                return {"target": self.pick_accused(state)}
            if self.suspects:
                return {"target": self.suspects[0]}
            return {"target": "Unknown"}
        safe = [o for o in options if not o.get("risky")]
        return _pick(self.rng, safe or options)


class RiskyStrategy(Strategy):
    name = "risky"

    def choose(self, state: GameState, options: list[dict[str, Any]], role: str) -> dict[str, Any]:
        if role == "accuse":
            return {"target": self.pick_accused(state)}
        risky = [o for o in options if o.get("risky")]
        return _pick(self.rng, risky or options)


class CooperationStrategy(Strategy):
    name = "cooperation-focused"

    def choose(self, state: GameState, options: list[dict[str, Any]], role: str) -> dict[str, Any]:
        if role == "accuse":
            return {"target": self.pick_accused(state)}
        if role == "people":
            prefer = [o for o in options if o.get("id") in ("rent", "press", "relationship")]
        elif role == "records":
            prefer = [o for o in options if o.get("id") in ("logs", "duplicates", "boot", "invoices")]
        else:
            prefer = [o for o in options if o.get("id") in ("split1", "split2", "park")]
        return _pick(self.rng, prefer or options)


class PoorDecisionsStrategy(Strategy):
    name = "poor-decisions"

    def choose(self, state: GameState, options: list[dict[str, Any]], role: str) -> dict[str, Any]:
        if role == "accuse":
            if len(self.suspects) > 1:
                return {"target": self.rng.choice(self.suspects[:-1])}
            return {"target": self.pick_accused(state)}
        bad = [o for o in options if o.get("id") in ("notes", "skim", "decline", "relationship", "invoice_box")]
        return _pick(self.rng, bad or options)


STRATEGIES = {
    "random": RandomStrategy,
    "clue-seeking": ClueSeekingStrategy,
    "broad-exploration": BroadExplorationStrategy,
    "time-efficient": TimeEfficientStrategy,
    "cautious": CautiousStrategy,
    "risky": RiskyStrategy,
    "cooperation-focused": CooperationStrategy,
    "poor-decisions": PoorDecisionsStrategy,
}


def get_strategy(name: str, rng: random.Random, adapter: dict[str, Any] | None = None) -> Strategy:
    cls = STRATEGIES.get(name, RandomStrategy)
    return cls(rng, adapter)
