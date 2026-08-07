"""Project materialized epistemic snapshots into static delivery units."""

from __future__ import annotations

import json
from collections import deque
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from idne.epistemic_progression.fingerprint import template_unit_id
from idne.epistemic_progression.loader import load_epistemic_package
from idne.epistemic_progression.model import EpistemicPackage, PlayableEvent
from idne.gamebook_nav.extract import PlayerUnit
from idne.gamebook_nav.graph import ChoiceEdge, UnitNavigation, build_navigation_graph

# Scene/content aliases: delivery id -> template prose unit.
CONTENT_ALIASES: dict[str, str] = {
    "SC-IT-RECORDS-POLICY": "UNIT-IT-ARCHIVE-POLICY",
}


def is_materialized_epistemic_package(package: EpistemicPackage | None) -> bool:
    if not package:
        return False
    return any(e.state_snapshot for e in package.events.values())


def prose_template_id(unit_id: str, event: PlayableEvent | None = None) -> str:
    if event and event.template_unit_id:
        return event.template_unit_id
    return template_unit_id(unit_id)


def build_materialized_delivery_units(
    package: EpistemicPackage,
    template_units: dict[str, PlayerUnit],
) -> dict[str, PlayerUnit]:
    """Map each materialized event to a delivery unit using template prose aliases."""
    out: dict[str, PlayerUnit] = {}
    for unit_id, event in package.events_by_unit.items():
        tpl = prose_template_id(unit_id, event)
        source = _prose_source(tpl, template_units)
        if not source:
            continue
        out[unit_id] = PlayerUnit(
            unit_id=unit_id,
            file=source.file,
            title=source.title,
            body=source.body,
            meta_lines=list(source.meta_lines),
            choices=[],
        )
    return out


def build_materialized_navigation_graph(package: EpistemicPackage) -> dict[str, UnitNavigation]:
    """Navigation graph keyed by materialized unit id with exact structured actions."""
    graph: dict[str, UnitNavigation] = {}
    for unit_id, event in package.events_by_unit.items():
        graph[unit_id] = UnitNavigation(
            unit_id=unit_id,
            choices=[
                ChoiceEdge(
                    label=action.label,
                    destination_unit_id=action.destination_unit_id,
                    edge_kind=action.action_type,
                )
                for action in event.structured_actions
            ],
        )
    return graph


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def _check_dests(adventure_root: Path) -> dict[str, tuple[str, str]]:
    cap_pkg = _read_json(adventure_root / "DO_NOT_READ" / "capability_check_package.json")
    out: dict[str, tuple[str, str]] = {}
    for chk in cap_pkg.get("checks", []) or []:
        dest = chk.get("destinations", {}) or {}
        decl = dest.get("action_unit_id", "")
        ok = dest.get("success_destination", "")
        fail = dest.get("failure_destination", "")
        if decl and ok and fail:
            out[decl] = (ok, fail)
    return out


def _is_check_decl(unit_id: str) -> bool:
    tpl = template_unit_id(unit_id)
    return tpl.startswith("UNIT-CHK-") and tpl.endswith("-DECL")


def _prose_source(unit_id: str, template_units: dict[str, PlayerUnit]) -> PlayerUnit | None:
    if unit_id in template_units:
        return template_units[unit_id]
    tpl = template_unit_id(unit_id)
    if tpl in template_units:
        return template_units[tpl]
    alias = CONTENT_ALIASES.get(unit_id) or CONTENT_ALIASES.get(tpl)
    if alias and alias in template_units:
        return template_units[alias]
    return None


def apply_check_branches(
    graph: dict[str, UnitNavigation],
    check_dests: dict[str, tuple[str, str]],
) -> None:
    """Replace check-declaration placeholder loops with success/failure branches."""
    for uid, nav in list(graph.items()):
        if not _is_check_decl(uid):
            continue
        pair = check_dests.get(template_unit_id(uid))
        if not pair:
            continue
        ok, fail = pair
        placeholder = any(
            "success or failure" in e.label.lower() or e.destination_unit_id == uid
            for e in nav.choices
        )
        if not placeholder and nav.choices:
            kinds = {e.edge_kind for e in nav.choices}
            if "check_success" in kinds and "check_failure" in kinds:
                continue
        graph[uid] = UnitNavigation(
            unit_id=uid,
            choices=[
                ChoiceEdge(
                    "If your roll succeeds, go to the success section.",
                    ok,
                    "check_success",
                ),
                ChoiceEdge(
                    "If your roll fails, go to the failure section.",
                    fail,
                    "check_failure",
                ),
            ],
        )


def _materialized_template_ids(package: EpistemicPackage) -> set[str]:
    return {
        prose_template_id(event.unit_id, event)
        for event in package.events_by_unit.values()
    }


def _resolve_supplemental_nav(
    adventure_root: Path,
    unit_id: str,
    delivery_unit: PlayerUnit,
) -> UnitNavigation | None:
    single = build_navigation_graph(
        adventure_root,
        {unit_id: delivery_unit},
        manifest_units={},
    )
    return single.get(unit_id)


def supplement_referenced_templates(
    adventure_root: Path,
    package: EpistemicPackage,
    template_units: dict[str, PlayerUnit],
    delivery_units: dict[str, PlayerUnit],
    graph: dict[str, UnitNavigation],
) -> tuple[dict[str, PlayerUnit], dict[str, UnitNavigation]]:
    """Add only template-only units transitively referenced by the materialized graph."""
    check_dests = _check_dests(adventure_root)
    apply_check_branches(graph, check_dests)

    excluded_templates = _materialized_template_ids(package)
    pending: deque[str] = deque()
    seen: set[str] = set()

    for nav in graph.values():
        for edge in nav.choices:
            pending.append(edge.destination_unit_id)

    while pending:
        dest = pending.popleft()
        if dest in seen:
            continue
        seen.add(dest)

        if dest in delivery_units:
            for edge in graph.get(dest, UnitNavigation(dest)).choices:
                if edge.destination_unit_id not in seen:
                    pending.append(edge.destination_unit_id)
            continue

        tpl = template_unit_id(dest)
        if tpl in excluded_templates and dest == tpl:
            continue

        source = _prose_source(dest, template_units)
        if not source:
            continue

        delivery_units[dest] = PlayerUnit(
            unit_id=dest,
            file=source.file,
            title=source.title,
            body=source.body,
            meta_lines=list(source.meta_lines),
            choices=[],
        )

        if _is_check_decl(dest) and tpl in check_dests:
            ok, fail = check_dests[tpl]
            graph[dest] = UnitNavigation(
                unit_id=dest,
                choices=[
                    ChoiceEdge(
                        "If your roll succeeds, go to the success section.",
                        ok,
                        "check_success",
                    ),
                    ChoiceEdge(
                        "If your roll fails, go to the failure section.",
                        fail,
                        "check_failure",
                    ),
                ],
            )
        else:
            nav = _resolve_supplemental_nav(adventure_root, dest, delivery_units[dest])
            if nav:
                graph[dest] = nav

        for edge in graph.get(dest, UnitNavigation(dest)).choices:
            if edge.destination_unit_id not in seen:
                pending.append(edge.destination_unit_id)

    return delivery_units, graph


@dataclass
class DeliveryBuildStats:
    materialized_events: int = 0
    delivery_units: int = 0
    supplemental_templates: int = 0
    public_sections: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "materialized_events": self.materialized_events,
            "delivery_units": self.delivery_units,
            "supplemental_templates": self.supplemental_templates,
            "public_sections": self.public_sections,
        }


def load_materialized_delivery(
    adventure_root,
    template_units: dict[str, PlayerUnit],
    *,
    manifest_units: dict[str, dict] | None = None,
) -> tuple[EpistemicPackage, dict[str, PlayerUnit], dict[str, UnitNavigation], DeliveryBuildStats] | tuple[None, None, None, None]:
    _ = manifest_units  # reserved for future manifest-aware supplements
    adventure_root = Path(adventure_root)
    package = load_epistemic_package(adventure_root)
    if not is_materialized_epistemic_package(package):
        return None, None, None, None

    stats = DeliveryBuildStats(materialized_events=len(package.events_by_unit))
    delivery_units = build_materialized_delivery_units(package, template_units)
    graph = build_materialized_navigation_graph(package)
    before = len(delivery_units)
    delivery_units, graph = supplement_referenced_templates(
        adventure_root,
        package,
        template_units,
        delivery_units,
        graph,
    )
    stats.supplemental_templates = len(delivery_units) - before
    stats.delivery_units = len(delivery_units)
    return package, delivery_units, graph, stats
