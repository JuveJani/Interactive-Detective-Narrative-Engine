"""Human-delivery simulation strategies."""

from __future__ import annotations

from abc import ABC, abstractmethod

from simulator_v2.human_delivery.player_view import HumanDeliveryPlayerView
from simulator_v2.human_delivery.types import VisibleChoice
from simulator_v2.rng import DeterministicRNG


class HumanDeliveryStrategy(ABC):
    name: str = "base"

    @abstractmethod
    def choose(
        self,
        view: HumanDeliveryPlayerView,
        rng: DeterministicRNG,
    ) -> VisibleChoice | None:
        raise NotImplementedError


class HumanRandomLegalStrategy(HumanDeliveryStrategy):
    name = "human_random_legal"

    def choose(self, view: HumanDeliveryPlayerView, rng: DeterministicRNG) -> VisibleChoice | None:
        legal = [c for c in view.visible_choices if c.destination_section is not None]
        return rng.choice(legal) if legal else None


class HumanFirstChoiceStrategy(HumanDeliveryStrategy):
    name = "human_first_choice"

    def choose(self, view: HumanDeliveryPlayerView, rng: DeterministicRNG) -> VisibleChoice | None:
        for choice in view.visible_choices:
            if choice.destination_section is not None:
                return choice
        return None


class HumanCheckAwareStrategy(HumanDeliveryStrategy):
    """Roll d20 visibly and pick success/failure branch when present."""

    name = "human_check_aware"

    def choose(self, view: HumanDeliveryPlayerView, rng: DeterministicRNG) -> VisibleChoice | None:
        legal = [c for c in view.visible_choices if c.destination_section is not None]
        if not legal:
            return None
        branches = {c.branch_kind: c for c in legal}
        if "check_success" in branches or "check_failure" in branches:
            roll = rng.d20()
            if roll >= 10 and "check_success" in branches:
                return branches["check_success"]
            if "check_failure" in branches:
                return branches["check_failure"]
        return legal[0]


class HiddenAccessProbeStrategy(HumanDeliveryStrategy):
    """Deliberately attempts hidden access — must fail loudly in tests."""

    name = "hidden_access_probe"

    def choose(self, view: HumanDeliveryPlayerView, rng: DeterministicRNG) -> VisibleChoice | None:
        view.attempt_internal_id_access("UNIT-HIDDEN")
        return None


HUMAN_STRATEGIES: dict[str, type[HumanDeliveryStrategy]] = {
    HumanRandomLegalStrategy.name: HumanRandomLegalStrategy,
    HumanFirstChoiceStrategy.name: HumanFirstChoiceStrategy,
    HumanCheckAwareStrategy.name: HumanCheckAwareStrategy,
    HiddenAccessProbeStrategy.name: HiddenAccessProbeStrategy,
}


def create_human_strategy(name: str) -> HumanDeliveryStrategy:
    cls = HUMAN_STRATEGIES.get(name, HumanRandomLegalStrategy)
    return cls()
