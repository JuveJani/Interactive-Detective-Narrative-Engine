"""Human-delivery player view — restricted information boundary."""

from __future__ import annotations

from dataclasses import dataclass, field

from simulator_v2.human_delivery.types import ParsedSection, VisibleChoice


class HiddenInformationAccessError(RuntimeError):
    """Raised when a strategy attempts to use non-player-visible data."""


@dataclass
class HumanDeliveryPlayerView:
    """Adventure-independent player-visible snapshot for static gamebook play."""

    start_filename: str
    start_section: int
    current_section: ParsedSection
    visited_sections: frozenset[int] = frozenset()
    in_world_clock: str = ""
    in_world_minutes: int = 0
    player_knowledge: frozenset[str] = frozenset()
    items: frozenset[str] = frozenset()
    observations: frozenset[str] = frozenset()
    _blocked_attrs: frozenset[str] = field(
        default_factory=lambda: frozenset(
            {
                "canonical_graph",
                "hidden_truth",
                "ending_requirements",
                "proof_requirements",
                "npc_hidden_knowledge",
                "future_sections",
                "internal_destination_ids",
                "author_files",
            }
        ),
        repr=False,
    )

    @property
    def visible_choices(self) -> list[VisibleChoice]:
        return list(self.current_section.choices)

    @property
    def visible_choice_labels(self) -> list[str]:
        return [c.label for c in self.current_section.choices]

    @property
    def current_section_number(self) -> int:
        return self.current_section.section_number

    def __getattr__(self, name: str):
        if name in self._blocked_attrs or name.startswith("_canonical"):
            raise HiddenInformationAccessError(
                f"strategy attempted hidden-information access: {name}"
            )
        raise AttributeError(name)

    def attempt_author_file_access(self, path: str) -> None:
        raise HiddenInformationAccessError(f"author-only file access rejected: {path}")

    def attempt_internal_id_access(self, unit_id: str) -> None:
        raise HiddenInformationAccessError(f"internal destination id access rejected: {unit_id}")

    def snapshot_state(self) -> dict:
        return {
            "public_section": self.current_section_number,
            "visited_sections": sorted(self.visited_sections),
            "in_world_clock": self.in_world_clock,
            "in_world_minutes": self.in_world_minutes,
            "player_knowledge": sorted(self.player_knowledge),
            "items": sorted(self.items),
            "observations": sorted(self.observations),
        }
