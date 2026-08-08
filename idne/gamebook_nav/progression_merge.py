"""Merge template progression paths into materialized public delivery."""

from __future__ import annotations

from pathlib import Path

from idne.epistemic_progression.fingerprint import template_unit_id
from idne.epistemic_progression.inference_wiring import load_template_progression_events
from idne.epistemic_progression.model import EpistemicPackage, PlayableEvent
from idne.gamebook_nav.extract import PlayerUnit
from idne.gamebook_nav.graph import ChoiceEdge, UnitNavigation, build_navigation_graph

PROGRESSION_PREFIXES = ("INF-", "END-", "SC-ACCUSATION", "REC-")


def _is_progression_template(uid: str) -> bool:
    tpl = template_unit_id(uid)
    return any(tpl.startswith(p) for p in PROGRESSION_PREFIXES)


def merge_progression_into_materialized_graph(
    adventure_root: Path,
    package: EpistemicPackage,
    graph: dict[str, UnitNavigation],
    template_units: dict[str, PlayerUnit],
) -> dict[str, UnitNavigation]:
    """Overlay inference, accusation, and ending edges from enriched templates onto materialized hubs."""
    templates = load_template_progression_events(adventure_root)
    if not templates:
        return graph

    template_graph = build_navigation_graph(adventure_root, template_units, manifest_units={})

    hub_units: dict[str, list[str]] = {}
    for mat_id in graph:
        tpl = template_unit_id(mat_id)
        if tpl.endswith("-BASE") or "HUB" in tpl:
            hub_units.setdefault(tpl, []).append(mat_id)

    for tpl_id, mat_ids in hub_units.items():
        tpl_event = templates.get(tpl_id)
        extra_edges: list[ChoiceEdge] = []
        if tpl_event:
            extra_edges = [
                ChoiceEdge(a.label, a.destination_unit_id, a.action_type)
                for a in tpl_event.structured_actions
                if a.action_type in {"inference_entry", "scene", "action"}
                and (
                    "inference worksheet" in a.label.lower()
                    or "accountability" in a.label.lower()
                )
            ]
        elif tpl_id in template_graph:
            extra_edges = [
                e
                for e in template_graph[tpl_id].choices
                if e.edge_kind in {"inference_entry", "scene", "action"}
                and (
                    "inference worksheet" in e.label.lower()
                    or "accountability" in e.label.lower()
                )
            ]
        for mat_id in mat_ids:
            nav = graph.get(mat_id)
            if not nav:
                continue
            existing = {(e.label, e.destination_unit_id) for e in nav.choices}
            merged = list(nav.choices)
            for edge in extra_edges:
                key = (edge.label, edge.destination_unit_id)
                if key not in existing:
                    merged.append(edge)
                    existing.add(key)
            graph[mat_id] = UnitNavigation(unit_id=mat_id, choices=merged)

    for uid, tpl_event in templates.items():
        if not _is_progression_template(uid):
            continue
        if uid in graph:
            continue
        edges = [
            ChoiceEdge(a.label, a.destination_unit_id, a.action_type)
            for a in tpl_event.structured_actions
        ]
        graph[uid] = UnitNavigation(unit_id=uid, choices=edges)

    for uid, nav in template_graph.items():
        if _is_progression_template(uid) and uid not in graph:
            graph[uid] = nav

    return graph


def supplement_progression_units(
    adventure_root: Path,
    template_units: dict[str, PlayerUnit],
    delivery_units: dict[str, PlayerUnit],
    graph: dict[str, UnitNavigation],
) -> tuple[dict[str, PlayerUnit], dict[str, UnitNavigation]]:
    from idne.gamebook_nav.delivery import _prose_source

    for uid in list(graph.keys()):
        if uid in delivery_units:
            continue
        if not _is_progression_template(uid):
            continue
        source = _prose_source(uid, template_units)
        if not source:
            continue
        delivery_units[uid] = PlayerUnit(
            unit_id=uid,
            file=source.file,
            title=source.title,
            body=source.body,
            meta_lines=list(source.meta_lines),
            choices=[],
        )
    return delivery_units, graph
