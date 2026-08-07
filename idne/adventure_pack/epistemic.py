"""Build epistemic progression package from spec and generated PLAYER units."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from idne.epistemic_progression.eligibility import filter_eligible_actions
from idne.epistemic_progression.materialize import MaterializeStats, materialize_package
from idne.epistemic_progression.model import EpistemicState, PlayableEvent
from idne.epistemic_progression.serialize import event_to_dict
from idne.epistemic_progression.template_navigation import (
    UnresolvedDestinationError,
    build_template_choice_map,
    build_template_navigation_graph,
    resolve_template_destination,
)
from idne.gamebook_nav.extract import parse_player_units

from idne.adventure_pack.spec import AdventurePackSpec, write_json


def _norm(label: str) -> str:
    return re.sub(r"\s+", " ", label.strip().lower())


def _action_from_choice(
    label: str,
    dest: str,
    kind: str,
    *,
    requires=None,
    world=None,
    refs=None,
    inv=False,
    knowledge=None,
    interaction=None,
) -> dict[str, Any]:
    action: dict[str, Any] = {
        "action_id": f"ACT-{dest}",
        "action_type": kind if kind != "navigate" else "nav",
        "label": label,
        "destination_unit_id": dest,
        "requires_knowledge_ids": requires or [],
        "requires_world_state": world or {},
        "referenced_fact_ids": refs or [],
        "investigative": inv,
    }
    if knowledge:
        action["knowledge_delta"] = list(knowledge)
    if interaction:
        action["interaction_delta"] = interaction
    return action


def _event(unit_id: str, kind: str, actions: list, spec: AdventurePackSpec, **extra) -> dict[str, Any]:
    loc = extra.get("location_id") or _infer_location(unit_id, spec)
    return {
        "event_id": f"EVT-{unit_id}",
        "unit_id": unit_id,
        "template_unit_id": unit_id,
        "location_id": loc,
        "physical_location_id": extra.get("physical_location_id", loc),
        "event_kind": kind,
        "structured_actions": actions,
        **{k: v for k, v in extra.items() if k not in ("location_id", "physical_location_id")},
    }


def _infer_location(unit_id: str, spec: AdventurePackSpec) -> str:
    unit = spec.unit_by_id.get(unit_id)
    if unit and unit.get("linked_location_id"):
        return str(unit["linked_location_id"])
    for loc in spec.locations:
        hub = loc.get("hub_unit_id") or ""
        if hub and unit_id.startswith(hub.replace("-BASE", "")):
            return str(loc["location_id"])
    prefix_map = {loc["location_id"].split("-", 1)[-1]: loc["location_id"] for loc in spec.locations if "-" in loc["location_id"]}
    for key, loc_id in prefix_map.items():
        if key.upper() in unit_id.upper():
            return loc_id
    return spec.start_location_id


def _topic_interaction_delta(unit_id: str) -> dict[str, list[str]]:
    return {"completed_topics": [unit_id]}


def _topic_return_actions(unit_id: str, spec: AdventurePackSpec, knowledge: list[str] | None = None) -> list[dict]:
    profiles = spec.epistemic.get("topic_return_profiles") or []
    grants = spec.epistemic.get("topic_knowledge_grants") or {}
    knowledge = list(knowledge or grants.get(unit_id, []))
    for profile in profiles:
        prefix = profile.get("unit_prefix", "")
        if unit_id.startswith(prefix):
            actions = [
                {
                    "action_id": f"ACT-{unit_id}-HUB",
                    "action_type": "return",
                    "label": profile["hub_label"],
                    "destination_unit_id": profile["hub_unit_id"],
                    "investigative": False,
                    "interaction_delta": _topic_interaction_delta(unit_id),
                },
                {
                    "action_id": f"ACT-{unit_id}-EXIT",
                    "action_type": "return",
                    "label": profile["exit_label"],
                    "destination_unit_id": profile["exit_unit_id"],
                    "investigative": False,
                    "interaction_delta": _topic_interaction_delta(unit_id),
                },
            ]
            if knowledge:
                for action in actions:
                    action["knowledge_delta"] = list(knowledge)
                    action["investigative"] = True
                    action["purpose"] = "conversation testimony"
            return actions
    return []


def _load_check_dests(adventure_root: Path) -> dict[str, tuple[str, str]]:
    cap = json.loads((adventure_root / "DO_NOT_READ" / "capability_check_package.json").read_text(encoding="utf-8"))
    out: dict[str, tuple[str, str]] = {}
    for chk in cap.get("checks", []) or []:
        dest = chk.get("destinations", {}) or {}
        decl = dest.get("action_unit_id", "")
        ok = dest.get("success_destination", "")
        fail = dest.get("failure_destination", "")
        if decl and ok and fail:
            out[decl] = (ok, fail)
    return out


def _check_declaration_actions(uid: str, check_dests: dict[str, tuple[str, str]]) -> list[dict] | None:
    pair = check_dests.get(uid)
    if not pair:
        return None
    ok, fail = pair
    return [
        _action_from_choice("If your roll succeeds, go to the success section.", ok, "check_success"),
        _action_from_choice("If your roll fails, go to the failure section.", fail, "check_failure"),
    ]


def _hub_choice_overrides(spec: AdventurePackSpec) -> dict[tuple[str, str], tuple[str, str, str]]:
    local: dict[tuple[str, str], tuple[str, str, str]] = {}
    for hub in spec.epistemic.get("hub_definitions") or []:
        hub_id = hub["hub_unit_id"]
        for action in hub.get("actions") or []:
            local[(hub_id, _norm(action["label"]))] = (
                action["destination_unit_id"],
                action.get("action_type", "nav"),
                action["label"],
            )
    for override in spec.epistemic.get("hub_action_overrides") or []:
        hub_id = override["hub_unit_id"]
        for choice in override.get("deferred_choices") or []:
            local[(hub_id, _norm(choice["label"]))] = (
                choice["destination_unit_id"],
                choice.get("action_type", "nav"),
                choice["label"],
            )
    return local


def _resolve_kind(label: str, uid: str, choice_map: dict[tuple[str, str], tuple[str, str]]) -> str:
    _dest, kind = resolve_template_destination(uid, label, choice_map)
    if kind == "navigate":
        return "nav"
    return kind


def _resolve_dest(label: str, uid: str, choice_map: dict[tuple[str, str], tuple[str, str]], aliases: dict[str, str]) -> str:
    dest, _kind = resolve_template_destination(uid, label, choice_map)
    return aliases.get(dest, dest)


def build_epistemic_events(spec: AdventurePackSpec, adventure_root: Path, manifest: dict[str, Any]) -> list[dict]:
    events: list[dict] = []
    player_units = parse_player_units(adventure_root / "PLAYER")
    aliases = dict(spec.epistemic.get("destination_aliases") or {})
    hub_overrides = _hub_choice_overrides(spec)
    nav_graph = build_template_navigation_graph(adventure_root, player_units, hub_overrides=hub_overrides)
    choice_map = build_template_choice_map(
        adventure_root,
        player_units,
        extra_edges={(k, v[:2]) for k, v in hub_overrides.items()},
        graph=nav_graph,
    )
    check_dests = _load_check_dests(adventure_root)
    handled: set[str] = set()

    for hub in spec.epistemic.get("hub_definitions") or []:
        hub_id = hub["hub_unit_id"]
        actions = []
        seen_labels: set[str] = set()
        for action in hub.get("actions") or []:
            dest = action["destination_unit_id"]
            atype = action.get("action_type", "nav")
            if dest.endswith("-HUB") or "-HUB" in dest:
                atype = "approach_npc"
            elif "UNIT-TOPIC" in dest or atype == "conversation":
                atype = "dialogue_topic"
            if atype == "conversation":
                atype = "dialogue_topic"
            inv = bool(action.get("investigative")) and atype not in (
                "nav", "return", "dialogue_topic", "approach_npc", "approach"
            )
            actions.append(
                _action_from_choice(
                    action["label"],
                    dest,
                    atype,
                    requires=action.get("requires_knowledge_ids"),
                    world=action.get("requires_world_state"),
                    inv=inv,
                )
            )
            seen_labels.add(_norm(action["label"]))
        # Merge return/extra choices from player unit spec
        pu = spec.unit_by_id.get(hub_id, {})
        for choice in pu.get("choices") or []:
            if _norm(choice["label"]) in seen_labels:
                continue
            dest = choice["destination_unit_id"]
            atype = choice.get("action_type", "return" if "end" in choice["label"].lower() or "return" in choice["label"].lower() or "leave" in choice["label"].lower() else "nav")
            actions.append(_action_from_choice(choice["label"], dest, atype))
            seen_labels.add(_norm(choice["label"]))
        events.append(
            _event(
                hub["hub_unit_id"],
                hub.get("event_kind", "location_hub"),
                actions,
                spec,
                observable_entities=hub.get("observable_entities") or [],
                content_blocks=hub.get("content_blocks") or [],
                relevant_knowledge_dependencies=hub.get("relevant_knowledge_dependencies") or [],
                relevant_world_state_dependencies=hub.get("relevant_world_state_dependencies") or [],
                physical_location_id=hub.get("physical_location_id"),
            )
        )
        handled.add(hub["hub_unit_id"])

    for uid in sorted(player_units.keys()):
        if uid in handled:
            continue
        unit = spec.unit_by_id.get(uid, {})
        choices = player_units[uid].choices
        kind = unit.get("unit_kind") or _infer_kind(uid, unit)
        if not choices and not uid.startswith("END-"):
            if kind not in ("ending", "recovery"):
                continue
        topic_returns = _topic_return_actions(uid, spec)
        check_actions = _check_declaration_actions(uid, check_dests)
        if check_actions:
            actions = check_actions
        elif topic_returns and kind == "dialogue_topic":
            actions = topic_returns
        else:
            actions = []
            spec_choices = {c["label"]: c for c in (unit.get("choices") or [])}
            for label in choices:
                spec_choice = spec_choices.get(label, {})
                if spec_choice.get("destination_unit_id"):
                    dest = aliases.get(spec_choice["destination_unit_id"], spec_choice["destination_unit_id"])
                    ck = spec_choice.get("action_type") or "action"
                else:
                    try:
                        dest = _resolve_dest(label, uid, choice_map, aliases)
                        ck = _resolve_kind(label, uid, choice_map)
                    except UnresolvedDestinationError:
                        raise
                req = list(spec_choice.get("requires_knowledge_ids") or unit.get("choice_gates", {}).get(label, {}).get("requires_knowledge_ids") or [])
                for gate in spec.epistemic.get("inference_choice_gates") or []:
                    if gate.get("label_contains") and gate["label_contains"] in label:
                        req = list(gate.get("requires_knowledge_ids") or req)
                world = dict(spec_choice.get("requires_world_state") or {})
                knowledge = list(spec_choice.get("knowledge_delta") or [])
                interaction = spec_choice.get("interaction_delta")
                inv = bool(spec_choice.get("investigative")) and ck not in (
                    "nav", "return", "dialogue_topic", "approach_npc", "approach", "action"
                )
                if knowledge or spec_choice.get("world_state_delta"):
                    inv = True
                actions.append(
                    _action_from_choice(
                        label, dest, ck, requires=req, world=world, knowledge=knowledge, interaction=interaction,
                        inv=inv,
                    )
                )
        extra: dict[str, Any] = {}
        if unit.get("content_blocks"):
            extra["content_blocks"] = unit["content_blocks"]
        events.append(_event(uid, kind, actions, spec, **extra))
        handled.add(uid)

    return events


def _infer_kind(uid: str, unit: dict[str, Any] | None = None) -> str:
    if unit and unit.get("unit_kind"):
        return str(unit["unit_kind"])
    if uid.endswith("-BASE"):
        return "location_hub"
    if uid.startswith("INF-"):
        return "inference"
    if uid.startswith("SC-"):
        return "scene"
    if uid.startswith("END-"):
        return "ending"
    if uid.startswith("REC-"):
        return "recovery"
    if "HUB" in uid:
        return "npc_interaction"
    if uid.endswith("-DECL") and "CHK" in uid:
        return "check_declaration"
    if uid.endswith("-SUCCESS"):
        return "check_success"
    if uid.endswith("-FAIL"):
        return "check_failure"
    return "action"


def write_epistemic_package(spec: AdventurePackSpec, adventure_root: Path, manifest: dict[str, Any]) -> MaterializeStats:
    events = build_epistemic_events(spec, adventure_root, manifest)
    flow = json.loads((adventure_root / "DO_NOT_READ" / "investigation_flow_package.json").read_text(encoding="utf-8"))
    initial_world = dict(flow.get("state_model", {}).get("initial_state") or {})
    templates: dict[str, PlayableEvent] = {}
    for raw in events:
        raw.setdefault("template_unit_id", raw["unit_id"])
        templates[raw["unit_id"]] = PlayableEvent.from_dict(raw)

    initial = EpistemicState(
        player_knowledge=frozenset(spec.epistemic.get("initial_player_knowledge") or []),
        world_state=initial_world,
        interaction_state={"exhausted_actions": [], "completed_topics": []},
        observable_entities=frozenset(spec.epistemic.get("initial_observable_entities") or []),
        observable_objects=frozenset(spec.epistemic.get("initial_observable_objects") or []),
    )
    max_states = int(spec.epistemic.get("materialization", {}).get("max_states", 500000))
    materialized, stats = materialize_package(
        templates,
        start_template_unit=spec.start_unit_id,
        initial_state=initial,
        max_states=max_states,
    )
    materialized.adventure_id = spec.pack_id

    template_menu_catalog = {
        tpl_id: [a.label for a in tpl.structured_actions if a.label]
        for tpl_id, tpl in templates.items()
        if tpl.event_kind == "npc_interaction"
    }

    pkg = {
        "schema_version": "1.0",
        "adventure_id": spec.pack_id,
        "initial_player_knowledge": list(spec.epistemic.get("initial_player_knowledge") or []),
        "initial_world_state": initial_world,
        "initial_observable_entities": list(spec.epistemic.get("initial_observable_entities") or []),
        "materialization": stats.to_dict(),
        "template_menu_catalog": template_menu_catalog,
        "playable_events": [event_to_dict(e) for e in sorted(materialized.events_by_unit.values(), key=lambda e: e.unit_id)],
    }
    dnr = adventure_root / "DO_NOT_READ"
    write_json(dnr / "epistemic_progression_package.json", pkg)
    write_json(
        adventure_root / "epistemic_progression_manifest.json",
        {
            "schema_version": "1.0",
            "epistemic_progression_method": "canonical",
            "package_path": "DO_NOT_READ/epistemic_progression_package.json",
            "materialization": stats.to_dict(),
        },
    )
    return stats
