"""Player strategies — no access to hidden truth."""

from __future__ import annotations

import random
from typing import Any

from simulator.state import GameState

SUSPECTS = ["Diane Marsh", "James Holt", "Mira Kwan", "Tomás Reyes"]

CLUE_PRIORITY = {
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


def _new_clue_score(state: GameState, option: dict[str, Any]) -> int:
    clues = option.get("grants_clues", [])
    return sum(1 for c in clues if c not in state.clues)


def _filter_progress(state: GameState, options: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Drop options that only revisit exhausted leaf nodes."""
    viable = []
    for o in options:
        grants = _new_clue_score(state, o)
        if grants > 0 or o.get("id") in ("split1", "split2", "accuse", "decline", "manager_key"):
            viable.append(o)
        elif o.get("type") in ("split_launch", "infer"):
            viable.append(o)
        elif o.get("target", "").startswith("J-2") or o.get("target", "").startswith("J-4") or o.get("target", "").startswith("J-5"):
            viable.append(o)
        elif o.get("id") in ("park", "timeline", "rent", "logs", "invoices", "duplicates", "boot", "press"):
            viable.append(o)
    return viable or options


class Strategy:
    name = "base"
    adapter: dict[str, Any] | None = None

    def __init__(self, rng: random.Random, adapter: dict[str, Any] | None = None):
        self.rng = rng
        self.adapter = adapter

    def choose(self, state: GameState, options: list[dict[str, Any]], role: str) -> dict[str, Any]:
        if role == "accuse":
            return {"target": self.pick_accused(state)}
        if not options:
            return {"target": state.node, "minutes": 0}
        return _pick(self.rng, options)

    def pick_accused(self, state: GameState) -> str:
        tags = state.compute_proof_tags(self.adapter or {})
        if tags.get("PROOF_OPPORTUNITY") and "C-15" in state.clues:
            return "Tomás Reyes"
        if tags.get("PROOF_MOTIVE") and "C-07" in state.clues and len(state.clues) < 6:
            return "Mira Kwan"
        if "C-08" in state.clues and "C-13" not in state.clues:
            return "James Holt"
        return self.rng.choice(SUSPECTS)


class RandomStrategy(Strategy):
    name = "random"

    def choose(self, state: GameState, options: list[dict[str, Any]], role: str) -> dict[str, Any]:
        if role == "accuse":
            return {"target": self.pick_accused(state)}
        return _pick(self.rng, _filter_progress(state, options))


class ClueSeekingStrategy(Strategy):
    name = "clue-seeking"

    def choose(self, state: GameState, options: list[dict[str, Any]], role: str) -> dict[str, Any]:
        if role == "accuse":
            return {"target": self.pick_accused(state)}
        options = _filter_progress(state, options)
        if not options:
            return {"target": state.node, "minutes": 0}
        scored = sorted(
            options,
            key=lambda o: (_new_clue_score(state, o), CLUE_PRIORITY.get(o.get("id", ""), 1)),
            reverse=True,
        )
        top_score = (_new_clue_score(state, scored[0]), CLUE_PRIORITY.get(scored[0].get("id", ""), 1))
        best = [o for o in scored if (_new_clue_score(state, o), CLUE_PRIORITY.get(o.get("id", ""), 1)) == top_score]
        return _pick(self.rng, best)


class BroadExplorationStrategy(Strategy):
    name = "broad-exploration"

    def __init__(self, rng: random.Random, adapter: dict[str, Any] | None = None):
        super().__init__(rng, adapter)
        self.seen: set[str] = set()

    def choose(self, state: GameState, options: list[dict[str, Any]], role: str) -> dict[str, Any]:
        if role == "accuse":
            return {"target": self.pick_accused(state)}
        options = _filter_progress(state, options)
        novel = [o for o in options if o.get("id") not in self.seen]
        pick = _pick(self.rng, novel or options)
        self.seen.add(pick.get("id", pick["target"]))
        return pick


class TimeEfficientStrategy(Strategy):
    name = "time-efficient"

    def choose(self, state: GameState, options: list[dict[str, Any]], role: str) -> dict[str, Any]:
        if role == "accuse":
            return {"target": self.pick_accused(state)}
        options = _filter_progress(state, options)
        if state.clock >= 1320:
            acc = [o for o in options if o.get("id") == "accuse"]
            if acc:
                return acc[0]
        if state.clock >= 1260 and any(o.get("id") == "split2" for o in options):
            return next(o for o in options if o.get("id") == "split2")
        return min(options, key=lambda o: o.get("minutes", 0))


class CautiousStrategy(Strategy):
    name = "cautious"

    def choose(self, state: GameState, options: list[dict[str, Any]], role: str) -> dict[str, Any]:
        if role == "accuse":
            tags = state.compute_proof_tags(self.adapter or {})
            if all(tags.values()):
                return {"target": self.pick_accused(state)}
            return {"target": "Diane Marsh"}
        options = _filter_progress(state, options)
        safe = [o for o in options if o.get("id") not in ("press", "skim")]
        return _pick(self.rng, safe or options)


class RiskyStrategy(Strategy):
    name = "risky"

    def choose(self, state: GameState, options: list[dict[str, Any]], role: str) -> dict[str, Any]:
        if role == "accuse":
            return {"target": self.rng.choice(SUSPECTS)}
        options = _filter_progress(state, options)
        risky = [o for o in options if o.get("id") in ("press", "boot", "duplicates", "whereabouts")]
        return _pick(self.rng, risky or options)


class CooperationStrategy(Strategy):
    name = "cooperation-focused"

    def choose(self, state: GameState, options: list[dict[str, Any]], role: str) -> dict[str, Any]:
        if role == "accuse":
            return {"target": self.pick_accused(state)}
        options = _filter_progress(state, options)
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
            return {"target": self.rng.choice(["Mira Kwan", "James Holt", "Diane Marsh"])}
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
