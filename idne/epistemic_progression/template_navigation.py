"""Canonical template-level choice destination resolution for epistemic builds."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from idne.gamebook_nav.extract import PlayerUnit
from idne.gamebook_nav.graph import ChoiceEdge, UnitNavigation, build_navigation_graph
from idne.gamebook_nav.resolve import norm


class UnresolvedDestinationError(ValueError):
    """Raised when a PLAYER choice lacks a canonical template destination."""

    def __init__(self, unit_id: str, label: str) -> None:
        self.unit_id = unit_id
        self.label = label
        super().__init__(
            f"Unresolved template destination for choice {label!r} on unit {unit_id!r}"
        )


def build_template_navigation_graph(
    adventure_root: Path,
    player_units: dict[str, PlayerUnit],
    *,
    hub_overrides: dict[tuple[str, str], tuple[str, str, str]] | None = None,
) -> dict[str, UnitNavigation]:
    """Build unit navigation from canonical packages plus optional epistemic hub edges."""
    graph = build_navigation_graph(adventure_root, player_units)
    if hub_overrides:
        apply_hub_overrides(graph, hub_overrides)
    return graph


def apply_hub_overrides(
    graph: dict[str, UnitNavigation],
    hub_overrides: dict[tuple[str, str], tuple[str, str, str]],
) -> None:
    """Replace or add epistemic hub edges. Values are (destination, kind, original_label)."""
    for (uid, nlabel), (dest, kind, label) in hub_overrides.items():
        nav = graph.setdefault(uid, UnitNavigation(unit_id=uid))
        nav.choices = [e for e in nav.choices if norm(e.label) != nlabel]
        nav.choices.append(ChoiceEdge(label, dest, kind))


def build_template_choice_map(
    adventure_root: Path,
    player_units: dict[str, PlayerUnit],
    *,
    extra_edges: dict[tuple[str, str], tuple[str, str]] | None = None,
    graph: dict[str, UnitNavigation] | None = None,
) -> dict[tuple[str, str], tuple[str, str]]:
    """Build (unit_id, normalized_label) -> (destination_unit_id, edge_kind) from canonical packages."""
    if graph is None:
        graph = build_navigation_graph(adventure_root, player_units)
    out: dict[tuple[str, str], tuple[str, str]] = {}
    for uid, nav in graph.items():
        for edge in nav.choices:
            out[(uid, norm(edge.label))] = (edge.destination_unit_id, edge.edge_kind)
    if extra_edges:
        out.update(extra_edges)
    return out


def resolve_template_destination(
    unit_id: str,
    label: str,
    choice_map: dict[tuple[str, str], tuple[str, str]],
    *,
    intentional_self_loops: frozenset[tuple[str, str]] | None = None,
) -> tuple[str, str]:
    """Resolve a PLAYER choice label to (destination_unit_id, edge_kind).

    Raises UnresolvedDestinationError when no mapping exists.
    Self-loops are allowed only when explicitly listed in intentional_self_loops.
    """
    key = (unit_id, norm(label))
    intentional_self_loops = intentional_self_loops or frozenset()
    if key in choice_map:
        dest, kind = choice_map[key]
        if dest == unit_id and key not in intentional_self_loops:
            raise UnresolvedDestinationError(unit_id, label)
        return dest, kind
    raise UnresolvedDestinationError(unit_id, label)


def template_navigation_edges(events: list[dict]) -> list[tuple[str, str, str, str]]:
    """Extract sorted template-level navigation edges for structural comparison."""
    edges: list[tuple[str, str, str, str]] = []
    for event in events:
        uid = event.get("unit_id", "")
        if not uid or "--S-" in uid:
            continue
        for action in event.get("structured_actions") or []:
            edges.append(
                (
                    uid,
                    str(action.get("label", "")),
                    str(action.get("destination_unit_id", "")),
                    str(action.get("action_type", action.get("kind", "action"))),
                )
            )
    return sorted(edges)


def template_navigation_digest(events: list[dict]) -> str:
    """Deterministic digest of template-level navigation structure."""
    payload = template_navigation_edges(events)
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()


def materialized_transition_edges(package: dict) -> list[tuple[str, str, str]]:
    """Extract sorted materialized snapshot transitions."""
    edges: list[tuple[str, str, str]] = []
    for event in package.get("playable_events") or []:
        if not event.get("state_snapshot"):
            continue
        uid = event.get("unit_id", "")
        for action in event.get("structured_actions") or []:
            edges.append((uid, str(action.get("label", "")), str(action.get("destination_unit_id", ""))))
    return sorted(edges)


def materialized_navigation_digest(package: dict) -> str:
    """Deterministic digest of the materialized epistemic transition graph."""
    payload = materialized_transition_edges(package)
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()


def epistemic_package_digest(package: dict) -> str:
    """Combined structural digest: templates + materialized transitions + materialization stats."""
    templates = [e for e in package.get("playable_events") or [] if "--S-" not in e.get("unit_id", "")]
    payload = {
        "template_navigation": template_navigation_edges(templates),
        "materialized_transitions": materialized_transition_edges(package),
        "materialization": package.get("materialization") or {},
        "initial_player_knowledge": sorted(package.get("initial_player_knowledge") or []),
        "initial_world_state": package.get("initial_world_state") or {},
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode()).hexdigest()
