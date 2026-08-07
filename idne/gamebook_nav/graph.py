"""Build choice destination graph from logic packages and PLAYER units."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

from idne.gamebook_nav.extract import PlayerUnit
from idne.epistemic_progression.loader import load_epistemic_package
from idne.epistemic_progression.fingerprint import template_unit_id
from idne.gamebook_nav.resolve import (
    build_action_index,
    build_nav_index,
    build_npc_index,
    build_object_name_index,
    build_revisit_index,
    match_label,
    match_object_name,
    norm,
)

LOC_BASE_SUFFIX = "-BASE"

SCENE_CONTINUE_OVERRIDES: dict[str, str] = {
    "SC-COLD-LABEL-DETAIL": "UNIT-LABEL-DETAIL",
    "SC-IT-RECORDS-POLICY": "UNIT-IT-ARCHIVE-POLICY",
    "SC-BREAK-LOCKER-BRANCH": "UNIT-LOCKER-MENU",
}

CONTROL_APPROACH_UNIT = "SC-CONTROL-APPROACH"


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


@dataclass
class ChoiceEdge:
    label: str
    destination_unit_id: str
    edge_kind: str = "navigate"


@dataclass
class UnitNavigation:
    unit_id: str
    choices: list[ChoiceEdge] = field(default_factory=list)


def _build_loc_bases(obj_pkg: dict) -> dict[str, str]:
    bases: dict[str, str] = {}
    for ru in obj_pkg.get("result_units", []) or []:
        uid = ru.get("unit_id", "")
        if uid.endswith(LOC_BASE_SUFFIX):
            for loc in ("LOC-DOCK", "LOC-COLD", "LOC-CONTROL", "LOC-SECURITY", "LOC-MANAGER", "LOC-BREAK"):
                if loc.replace("LOC-", "") in uid:
                    bases[loc] = uid
    mapping = {
        "LOC-DOCK": "UNIT-DOCK-BASE",
        "LOC-COLD": "UNIT-COLD-BASE",
        "LOC-CONTROL": "UNIT-CONTROL-BASE",
        "LOC-SECURITY": "UNIT-SECURITY-BASE",
        "LOC-MANAGER": "UNIT-MANAGER-BASE",
        "LOC-BREAK": "UNIT-BREAK-BASE",
    }
    bases.update(mapping)
    return bases


def _return_dest(result_units: dict[str, dict], unit_id: str) -> str:
    ru = result_units.get(unit_id, {})
    return str(ru.get("return_destination", ""))


def _index_result_units(obj_pkg: dict) -> dict[str, dict]:
    return {ru["unit_id"]: ru for ru in obj_pkg.get("result_units", []) or [] if ru.get("unit_id")}


def _scene_locations(flow_pkg: dict) -> dict[str, str]:
    locs: dict[str, str] = {}
    for step in flow_pkg.get("timeline", {}).get("steps", []) or []:
        sid = step.get("scene_unit_id", "")
        loc = step.get("location_id", "")
        if sid and loc:
            locs[sid] = loc
    for chain in flow_pkg.get("scene_chains", []) or []:
        for step in chain.get("steps", []) or []:
            sid = step.get("scene_unit_id", "")
            loc = step.get("location_id", "")
            if sid and loc:
                locs[sid] = loc
    for block in flow_pkg.get("world_state_variants", []) or []:
        base = block.get("base_scene_unit_id", "")
        loc = block.get("location_id", "")
        if base and loc and base not in locs:
            locs[base] = loc
    return locs


def _npc_home_bases(npc_pkg: dict, loc_bases: dict[str, str]) -> dict[str, str]:
    homes: dict[str, str] = {}
    for entry in npc_pkg.get("presence_schedule", []) or []:
        npc = entry.get("npc_id", "")
        loc = entry.get("location_id", "")
        if npc and loc and loc in loc_bases:
            homes.setdefault(npc, loc_bases[loc])
    defaults = {
        "NPC-MARCUS": loc_bases["LOC-SECURITY"],
        "NPC-DEV": loc_bases["LOC-DOCK"],
        "NPC-LORI": loc_bases["LOC-MANAGER"],
        "NPC-ELENA": loc_bases["LOC-DOCK"],
        "NPC-PAT": loc_bases["LOC-BREAK"],
    }
    for k, v in defaults.items():
        homes.setdefault(k, v)
    return homes


def _recovery_dest(flow_pkg: dict, loc_bases: dict[str, str]) -> dict[str, str]:
    out: dict[str, str] = {}
    for route in flow_pkg.get("recovery_routes", []) or []:
        rid = route.get("route_id", "")
        loc = route.get("destination_ref", "")
        if rid and loc:
            out[rid] = loc_bases.get(loc, "")
    return out


def _check_dests(cap_pkg: dict) -> dict[str, tuple[str, str]]:
    out: dict[str, tuple[str, str]] = {}
    for chk in cap_pkg.get("checks", []) or []:
        dest = chk.get("destinations", {}) or {}
        decl = dest.get("action_unit_id", "")
        ok = dest.get("success_destination", "")
        fail = dest.get("failure_destination", "")
        if decl:
            out[decl] = (ok, fail)
    return out


def _unit_location(unit_id: str, scene_locs: dict[str, str], loc_bases: dict[str, str]) -> str:
    if unit_id in scene_locs:
        return scene_locs[unit_id]
    for loc, base in loc_bases.items():
        token = loc.replace("LOC-", "")
        if token in unit_id:
            return loc
    return ""


def _scene_chain_entries(flow_pkg: dict) -> dict[str, str]:
    """Map scene step player_label -> scene unit for opening chain steps."""
    idx: dict[str, str] = {}
    for chain in flow_pkg.get("scene_chains", []) or []:
        for step in chain.get("steps", []) or []:
            label = step.get("player_label", "")
            sid = step.get("scene_unit_id", "")
            if label and sid:
                idx[norm(label)] = sid
    return idx


def _add_inference_access(
    graph: dict[str, UnitNavigation],
    player_units: dict[str, PlayerUnit],
    loc_bases: dict[str, str],
) -> None:
    """Allow inference worksheets to be opened from any location base menu."""
    inference_ids = sorted(uid for uid in player_units if uid.startswith("INF-"))
    base_ids = [uid for uid in player_units if uid.endswith(LOC_BASE_SUFFIX) or uid in loc_bases.values()]
    for base_id in base_ids:
        nav = graph.setdefault(base_id, UnitNavigation(unit_id=base_id))
        existing = {norm(e.label) for e in nav.choices}
        for inf_id in inference_ids:
            title = player_units[inf_id].title
            label = f"Open inference worksheet: {title}."
            if norm(label) in existing:
                continue
            nav.choices.append(ChoiceEdge(label, inf_id, "inference_entry"))


def _add_inference_recovery(
    graph: dict[str, UnitNavigation],
    flow_pkg: dict,
) -> None:
    for gate in flow_pkg.get("inference_flow_gates", []) or []:
        inf_id = gate.get("inference_id", "")
        if not inf_id or inf_id not in graph:
            continue
        for rec_id in gate.get("recovery_routes", []) or []:
            label = f"Follow recovery route {rec_id} after incomplete synthesis."
            nav = graph[inf_id]
            if rec_id not in {e.destination_unit_id for e in nav.choices}:
                nav.choices.append(ChoiceEdge(label, rec_id, "recovery"))


def _add_opening_scenes(
    graph: dict[str, UnitNavigation],
    flow_pkg: dict,
    loc_bases: dict[str, str],
) -> None:
    for chain in flow_pkg.get("scene_chains", []) or []:
        steps = chain.get("steps", []) or []
        if not steps:
            continue
        first = steps[0]
        loc = first.get("location_id", "")
        scene_id = first.get("scene_unit_id", "")
        label = first.get("player_label", "")
        base = loc_bases.get(loc, "")
        if not base or not scene_id or base not in graph:
            continue
        nav = graph[base]
        if scene_id not in {e.destination_unit_id for e in nav.choices}:
            nav.choices.append(ChoiceEdge(label or f"Begin scene {scene_id}.", scene_id, "scene"))


def _add_timeline_scene_access(
    graph: dict[str, UnitNavigation],
    flow_pkg: dict,
    loc_bases: dict[str, str],
) -> None:
    for chain in flow_pkg.get("scene_chains", []) or []:
        for step in chain.get("steps", []) or []:
            loc = step.get("location_id", "")
            scene_id = step.get("scene_unit_id", "")
            label = step.get("player_label", "")
            base = loc_bases.get(loc, "")
            if not base or not scene_id or base not in graph:
                continue
            nav = graph[base]
            if scene_id in {e.destination_unit_id for e in nav.choices}:
                continue
            nav.choices.append(ChoiceEdge(label or f"Begin scene {scene_id}.", scene_id, "scene"))


def _add_npc_conversation_access(
    graph: dict[str, UnitNavigation],
    npc_pkg: dict,
    npc_homes: dict[str, str],
) -> None:
    for conv in npc_pkg.get("conversation_graph", []) or []:
        npc_id = conv.get("npc_id", "")
        home = npc_homes.get(npc_id, "")
        if not home or home not in graph:
            continue
        nav = graph[home]
        existing = {norm(e.label) for e in nav.choices}
        for node in conv.get("nodes", []) or []:
            label = node.get("player_label", "")
            dest = node.get("npc_response_unit", "")
            if label and dest and norm(label) not in existing:
                nav.choices.append(ChoiceEdge(label, dest, "npc"))
                existing.add(norm(label))


def _add_scene_revisit_access(
    graph: dict[str, UnitNavigation],
    flow_pkg: dict,
    loc_bases: dict[str, str],
) -> None:
    for block in flow_pkg.get("location_revisits", []) or []:
        loc = block.get("location_id", "")
        base = loc_bases.get(loc, "")
        if not base or base not in graph:
            continue
        nav = graph[base]
        existing = {e.destination_unit_id for e in nav.choices}
        for rule in block.get("revisit_rules", []) or []:
            scene = rule.get("unlocks_scene_unit_id", "")
            label = rule.get("player_label", "")
            if scene and scene not in existing:
                nav.choices.append(
                    ChoiceEdge(label or f"Continue scene {scene}.", scene, "scene")
                )
                existing.add(scene)


def _add_world_state_scene_variants(
    graph: dict[str, UnitNavigation],
    flow_pkg: dict,
    loc_bases: dict[str, str],
) -> None:
    for variant in flow_pkg.get("world_state_variants", []) or []:
        base_scene = variant.get("base_scene_unit_id", "")
        if base_scene not in graph:
            continue
        nav = graph[base_scene]
        existing = {e.destination_unit_id for e in nav.choices}
        for option in variant.get("variants", []) or []:
            scene = option.get("scene_unit_id", "")
            if scene and scene not in existing:
                nav.choices.append(ChoiceEdge(f"Continue to scene {scene}.", scene, "scene_variant"))
                existing.add(scene)
        if not nav.choices:
            # approach gate with no player choices — link variants directly
            for option in variant.get("variants", []) or []:
                scene = option.get("scene_unit_id", "")
                if scene and scene not in existing:
                    nav.choices.append(ChoiceEdge(f"Proceed to {scene}.", scene, "scene_variant"))
                    existing.add(scene)
    for variant in flow_pkg.get("world_state_variants", []) or []:
        loc = variant.get("location_id", "")
        base = loc_bases.get(loc, "")
        base_scene = variant.get("base_scene_unit_id", "")
        if base and base in graph and base_scene:
            nav = graph[base]
            if base_scene not in {e.destination_unit_id for e in nav.choices}:
                nav.choices.append(ChoiceEdge(f"Enter scene {base_scene}.", base_scene, "scene"))


def _add_content_alias_links(graph: dict[str, UnitNavigation]) -> None:
    pairs = {
        "SC-IT-RECORDS-POLICY": "UNIT-IT-ARCHIVE-POLICY",
    }
    for src, dst in pairs.items():
        nav = graph.get(src)
        if not nav or dst in {e.destination_unit_id for e in nav.choices}:
            continue
        nav.choices.append(ChoiceEdge("Review the archive sync policy notice.", dst, "alias"))


def _add_accusation_endings(flow_pkg: dict, graph: dict[str, UnitNavigation]) -> None:
    """Endings are resolved from accusation questionnaire state, not direct menu picks."""
    return


def _graph_from_epistemic_package(
    adventure_root: Path,
    player_units: dict[str, PlayerUnit],
    manifest_units: dict[str, dict],
) -> dict[str, UnitNavigation] | None:
    """When epistemic progression is declared, build navigation from structured actions only."""
    package = load_epistemic_package(adventure_root)
    if not package:
        return None
    materialized = any(e.state_snapshot for e in package.events.values())
    graph: dict[str, UnitNavigation] = {}
    for uid, entry in manifest_units.items():
        event = package.events_by_unit.get(uid)
        if not event and materialized:
            for ev in package.events_by_unit.values():
                tpl = ev.template_unit_id or template_unit_id(ev.unit_id)
                if tpl == uid:
                    event = ev
                    break
        if event:
            graph[uid] = UnitNavigation(
                unit_id=uid,
                choices=[
                    ChoiceEdge(
                        label=a.label,
                        destination_unit_id=template_unit_id(a.destination_unit_id)
                        if materialized
                        else a.destination_unit_id,
                        edge_kind=a.action_type,
                    )
                    for a in event.structured_actions
                ],
            )
            continue
        raw_choices = entry.get("choices") or []
        pu = player_units.get(uid)
        if raw_choices and all(isinstance(c, dict) and c.get("destination_unit_id") for c in raw_choices):
            graph[uid] = UnitNavigation(
                unit_id=uid,
                choices=[
                    ChoiceEdge(
                        label=c.get("label", ""),
                        destination_unit_id=c["destination_unit_id"],
                        edge_kind=c.get("kind", "navigate"),
                    )
                    for c in raw_choices
                ],
            )
        elif pu and pu.choices:
            graph[uid] = UnitNavigation(unit_id=uid, choices=[])
    return graph


def build_navigation_graph(
    adventure_root: Path,
    player_units: dict[str, PlayerUnit],
    *,
    manifest_units: dict[str, dict] | None = None,
) -> dict[str, UnitNavigation]:
    """Resolve choice destinations for each playable unit."""
    dnr = adventure_root / "DO_NOT_READ"
    env_pkg = _read_json(dnr / "environment_package.json")
    obj_pkg = _read_json(dnr / "object_interaction_package.json")
    npc_pkg = _read_json(dnr / "npc_investigation_package.json")
    flow_pkg = _read_json(dnr / "investigation_flow_package.json")
    cap_pkg = _read_json(dnr / "capability_check_package.json")

    loc_bases = _build_loc_bases(obj_pkg)
    result_units = _index_result_units(obj_pkg)
    scene_locs = _scene_locations(flow_pkg)
    npc_homes = _npc_home_bases(npc_pkg, loc_bases)
    recovery_map = _recovery_dest(flow_pkg, loc_bases)
    check_dests = _check_dests(cap_pkg)
    action_labels = build_action_index(obj_pkg, cap_pkg)
    object_names = build_object_name_index(obj_pkg)
    nav_labels = build_nav_index(env_pkg, loc_bases)
    npc_labels = build_npc_index(npc_pkg)
    revisit_labels = build_revisit_index(flow_pkg)
    scene_entries = _scene_chain_entries(flow_pkg)
    ep_graph: dict[str, UnitNavigation] | None = None

    if manifest_units:
        ep_graph = _graph_from_epistemic_package(adventure_root, player_units, manifest_units)

    graph: dict[str, UnitNavigation] = {}

    for uid, unit in player_units.items():
        edges: list[ChoiceEdge] = []
        loc = _unit_location(uid, scene_locs, loc_bases)
        ret_default = _return_dest(result_units, uid)

        for choice in unit.choices:
            nchoice = norm(choice)

            if nchoice.startswith("proceed to the success or failure"):
                pair = check_dests.get(uid)
                if pair:
                    ok, fail = pair
                    edges.append(ChoiceEdge("If your roll succeeds, go to the success section.", ok, "check_success"))
                    edges.append(ChoiceEdge("If your roll fails, go to the failure section.", fail, "check_failure"))
                continue

            if nchoice.startswith("go to the named location"):
                dest = recovery_map.get(uid) or recovery_map.get(uid.replace("_", "-"))
                if dest:
                    edges.append(ChoiceEdge(choice, dest, "recovery"))
                continue

            if "return to the location base section" in nchoice:
                base = loc_bases.get(scene_locs.get(uid, loc), "")
                if base:
                    edges.append(ChoiceEdge(choice, base, "return"))
                continue

            if "return to your current location menu" in nchoice:
                matched = False
                for npc_id, home in npc_homes.items():
                    if npc_id.replace("NPC-", "") in uid:
                        edges.append(ChoiceEdge(choice, home, "return"))
                        matched = True
                        break
                if not matched and ret_default:
                    edges.append(ChoiceEdge(choice, ret_default, "return"))
                continue

            if nchoice.startswith("continue this scene thread"):
                override = SCENE_CONTINUE_OVERRIDES.get(uid)
                if override:
                    edges.append(ChoiceEdge(choice, override, "scene_continue"))
                    continue
                base = loc_bases.get(scene_locs.get(uid, loc), "")
                if base:
                    edges.append(ChoiceEdge(choice, base, "scene_continue"))
                continue

            if nchoice.startswith("mark synthesis complete"):
                edges.append(ChoiceEdge(choice, "END-NARRATIVE-CONTINUE", "inference"))
                continue

            if nchoice.startswith("mark synthesis incomplete"):
                edges.append(ChoiceEdge(choice, "REC-REVISIT-ANY-UNRESOLVED-SOURCE", "inference"))
                continue

            if nchoice.startswith("return to the security office") and uid == "UNIT-IT-ARCHIVE-POLICY":
                edges.append(ChoiceEdge(choice, loc_bases["LOC-SECURITY"], "return"))
                continue

            if nchoice.startswith("return to"):
                # Location navigation from environment_package takes precedence over
                # result_unit return_destination (location bases use self as menu hub).
                if loc:
                    nav_dest = nav_labels.get((loc, nchoice))
                    if nav_dest:
                        edges.append(ChoiceEdge(choice, nav_dest, "return"))
                        continue
                if ret_default and ret_default != uid:
                    edges.append(ChoiceEdge(choice, ret_default, "return"))
                    continue
                for (src, lbl), dest in nav_labels.items():
                    if lbl == nchoice and dest:
                        edges.append(ChoiceEdge(choice, dest, "return"))
                        break
                if edges and edges[-1].label == choice:
                    continue

            if "request escort clearance" in nchoice:
                dest = match_label(choice, action_labels, min_score=0.33)
                if dest:
                    edges.append(ChoiceEdge(choice, dest, "action"))
                    continue

            if nchoice in action_labels:
                edges.append(ChoiceEdge(choice, action_labels[nchoice], "action"))
                continue

            dest = match_label(choice, npc_labels)
            if dest:
                edges.append(ChoiceEdge(choice, dest, "npc"))
                continue

            if loc:
                dest = nav_labels.get((loc, nchoice))
                if dest:
                    if dest == loc_bases.get("LOC-CONTROL") and CONTROL_APPROACH_UNIT in player_units:
                        edges.append(ChoiceEdge(choice, CONTROL_APPROACH_UNIT, "nav"))
                    else:
                        edges.append(ChoiceEdge(choice, dest, "nav"))
                    continue
                nav_flat = {lbl: d for (src, lbl), d in nav_labels.items() if src == loc}
                dest = match_label(choice, nav_flat)
                if dest:
                    if dest == loc_bases.get("LOC-CONTROL") and CONTROL_APPROACH_UNIT in player_units:
                        edges.append(ChoiceEdge(choice, CONTROL_APPROACH_UNIT, "nav"))
                    else:
                        edges.append(ChoiceEdge(choice, dest, "nav"))
                    continue

                dest = match_object_name(choice, loc, object_names)
                if dest:
                    edges.append(ChoiceEdge(choice, dest, "action"))
                    continue

            dest = match_label(choice, action_labels, min_score=0.33)
            if dest:
                edges.append(ChoiceEdge(choice, dest, "action"))
                continue

            dest = match_label(choice, revisit_labels)
            if dest:
                edges.append(ChoiceEdge(choice, dest, "scene"))
                continue

            dest = match_label(choice, scene_entries)
            if dest:
                edges.append(ChoiceEdge(choice, dest, "scene"))
                continue

            if uid.endswith(LOC_BASE_SUFFIX) or "-BASE" in uid:
                nav_flat = {lbl: d for (_, lbl), d in nav_labels.items()}
                dest = match_label(choice, nav_flat)
                if dest:
                    edges.append(ChoiceEdge(choice, dest, "nav"))
                    continue

        graph[uid] = UnitNavigation(unit_id=uid, choices=edges)

    if ep_graph is not None:
        for uid, nav in ep_graph.items():
            if nav.choices:
                graph[uid] = nav

    _add_inference_access(graph, player_units, loc_bases)
    _add_inference_recovery(graph, flow_pkg)
    _add_opening_scenes(graph, flow_pkg, loc_bases)
    _add_timeline_scene_access(graph, flow_pkg, loc_bases)
    _add_npc_conversation_access(graph, npc_pkg, npc_homes)
    _add_scene_revisit_access(graph, flow_pkg, loc_bases)
    _add_world_state_scene_variants(graph, flow_pkg, loc_bases)
    _add_content_alias_links(graph)
    _add_accusation_endings(flow_pkg, graph)
    return graph
