"""Player strategies — blind to simulator truth and future clues."""

from __future__ import annotations

import random
from typing import Any

from simulator.state import GameState

ACTION_PRIORITY_DEFAULT = {
    "stairwell": 4,
    "split1": 6,
    "split2": 6,
    "park": 3,
    "accuse": 5,
    "decline": 0,
    "notes": 1,
    "timeline": 2,
    "manager_key": 4,
    "stairwell_revisit": 1,
}


def _action_priority(adapter: dict[str, Any]) -> dict[str, int]:
    hints = adapter.get("strategy_hints", {})
    base = dict(ACTION_PRIORITY_DEFAULT)
    base.update(hints.get("action_priority", {}))
    for nid, spec in adapter.get("nodes", {}).items():
        if spec.get("type") == "hub":
            for ch in spec.get("choices", []):
                cid = ch.get("id", "")
                if cid and cid not in base:
                    base[cid] = 2
        elif "choices" in spec:
            for ch in spec["choices"]:
                cid = ch.get("id", "")
                if cid and cid not in base:
                    base[cid] = 2
    return base


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
        self.action_priority = _action_priority(self.adapter)

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
            key=lambda o: (self.action_priority.get(o.get("id", ""), 1), -o.get("minutes", 0)),
            reverse=True,
        )
        top = self.action_priority.get(scored[0].get("id", ""), 1)
        best = [o for o in scored if self.action_priority.get(o.get("id", ""), 1) == top]
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
                return {"target": self.rng.choice(self.suspects[1:])}
            return {"target": self.pick_accused(state)}
        low = sorted(options, key=lambda o: self.action_priority.get(o.get("id", ""), 1))
        worst = [o for o in low if self.action_priority.get(o.get("id", ""), 1) <= 1]
        return _pick(self.rng, worst or options)


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
