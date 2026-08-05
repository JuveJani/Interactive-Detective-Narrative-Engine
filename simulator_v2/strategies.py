"""Adventure-independent simulation strategies."""

from __future__ import annotations

from abc import ABC, abstractmethod

from simulator_v2.actions import ActionKind, LegalAction
from simulator_v2.player_view import PlayerView
from simulator_v2.rng import DeterministicRNG

TWO_PLAYER_ONLY_STRATEGIES = frozenset({"cooperative_two_player"})


def strategy_compatible(play_mode: str, strategy_name: str) -> bool:
    if strategy_name in TWO_PLAYER_ONLY_STRATEGIES:
        return play_mode == "two_player"
    return True


def terminal_fallback(legal: list[LegalAction]) -> LegalAction | None:
    """Deterministic time/progress fallback using only player-visible legal actions."""
    if not legal:
        return None
    for kind in (
        ActionKind.ADVANCE_TIME,
        ActionKind.NAVIGATE,
        ActionKind.OBJECT,
        ActionKind.NPC,
        ActionKind.HYPOTHESIS,
        ActionKind.REVISIT,
    ):
        opts = sorted([a for a in legal if a.kind == kind], key=lambda a: a.action_id)
        if opts:
            return opts[0]
    return sorted(legal, key=lambda a: a.action_id)[0]


class Strategy(ABC):
    name: str = "base"

    @abstractmethod
    def choose(self, view: PlayerView, legal: list[LegalAction], rng: DeterministicRNG) -> LegalAction | None:
        raise NotImplementedError


class RandomLegalStrategy(Strategy):
    name = "random_legal"

    def choose(self, view: PlayerView, legal: list[LegalAction], rng: DeterministicRNG) -> LegalAction | None:
        return rng.choice(legal) if legal else None


class BroadExplorerStrategy(Strategy):
    name = "broad_explorer"

    def choose(self, view: PlayerView, legal: list[LegalAction], rng: DeterministicRNG) -> LegalAction | None:
        nav = [a for a in legal if a.kind == ActionKind.NAVIGATE]
        if nav:
            return nav[0]
        return legal[0] if legal else None


class TimeConservingStrategy(Strategy):
    name = "time_conserving"

    def choose(self, view: PlayerView, legal: list[LegalAction], rng: DeterministicRNG) -> LegalAction | None:
        if not legal:
            return None
        return min(legal, key=lambda a: a.time_cost_minutes)


class ObjectFocusedStrategy(Strategy):
    name = "object_focused"

    def choose(self, view: PlayerView, legal: list[LegalAction], rng: DeterministicRNG) -> LegalAction | None:
        objs = [a for a in legal if a.kind == ActionKind.OBJECT]
        if objs:
            return objs[0]
        return legal[0] if legal else None


class NpcFocusedStrategy(Strategy):
    name = "npc_focused"

    def choose(self, view: PlayerView, legal: list[LegalAction], rng: DeterministicRNG) -> LegalAction | None:
        npcs = [a for a in legal if a.kind == ActionKind.NPC]
        if npcs:
            return npcs[0]
        return legal[0] if legal else None


class InformationSeekingStrategy(Strategy):
    name = "information_seeking"

    def choose(self, view: PlayerView, legal: list[LegalAction], rng: DeterministicRNG) -> LegalAction | None:
        for kind in (ActionKind.OBJECT, ActionKind.NPC, ActionKind.HYPOTHESIS):
            opts = [a for a in legal if a.kind == kind]
            if opts:
                return opts[0]
        return legal[0] if legal else None


class ProofSeekingStrategy(Strategy):
    name = "proof_seeking"

    def choose(self, view: PlayerView, legal: list[LegalAction], rng: DeterministicRNG) -> LegalAction | None:
        hyps = [a for a in legal if a.kind == ActionKind.HYPOTHESIS]
        if hyps:
            return hyps[0]
        objs = [a for a in legal if a.kind == ActionKind.OBJECT]
        if objs:
            return objs[0]
        return legal[0] if legal else None


class CautiousStrategy(Strategy):
    name = "cautious"

    def choose(self, view: PlayerView, legal: list[LegalAction], rng: DeterministicRNG) -> LegalAction | None:
        safe = [a for a in legal if a.kind not in (ActionKind.CHECK, ActionKind.ACCUSATION)]
        if safe:
            return safe[0]
        return legal[0] if legal else None


class RiskTakingStrategy(Strategy):
    name = "risk_taking"

    def choose(self, view: PlayerView, legal: list[LegalAction], rng: DeterministicRNG) -> LegalAction | None:
        risky = [a for a in legal if a.kind in (ActionKind.OBJECT, ActionKind.ACCUSATION)]
        if risky:
            return risky[0]
        return legal[0] if legal else None


class PoorBaselineStrategy(Strategy):
    name = "poor_baseline"

    def choose(self, view: PlayerView, legal: list[LegalAction], rng: DeterministicRNG) -> LegalAction | None:
        time_adv = [a for a in legal if a.kind == ActionKind.ADVANCE_TIME]
        if time_adv:
            return time_adv[0]
        return legal[-1] if legal else None


class CooperativeTwoPlayerStrategy(Strategy):
    name = "cooperative_two_player"

    def choose(self, view: PlayerView, legal: list[LegalAction], rng: DeterministicRNG) -> LegalAction | None:
        if not view.split_active:
            split = [a for a in legal if a.kind == ActionKind.SPLIT]
            if split:
                return split[0]
        regroup = [a for a in legal if a.kind == ActionKind.REGROUP]
        if view.split_active and regroup and len(view.player_knowledge) >= 1:
            return regroup[0]
        return InformationSeekingStrategy().choose(view, legal, rng)


STRATEGIES: dict[str, type[Strategy]] = {
    RandomLegalStrategy.name: RandomLegalStrategy,
    BroadExplorerStrategy.name: BroadExplorerStrategy,
    TimeConservingStrategy.name: TimeConservingStrategy,
    ObjectFocusedStrategy.name: ObjectFocusedStrategy,
    NpcFocusedStrategy.name: NpcFocusedStrategy,
    InformationSeekingStrategy.name: InformationSeekingStrategy,
    ProofSeekingStrategy.name: ProofSeekingStrategy,
    CautiousStrategy.name: CautiousStrategy,
    RiskTakingStrategy.name: RiskTakingStrategy,
    PoorBaselineStrategy.name: PoorBaselineStrategy,
    CooperativeTwoPlayerStrategy.name: CooperativeTwoPlayerStrategy,
}


def create_strategy(name: str) -> Strategy:
    cls = STRATEGIES.get(name, RandomLegalStrategy)
    return cls()
