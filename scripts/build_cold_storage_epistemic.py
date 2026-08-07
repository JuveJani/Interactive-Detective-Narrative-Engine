#!/usr/bin/env python3
"""Build epistemic progression package and opening hub split for The Cold Storage Alarm."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from idne.gamebook_nav.extract import parse_player_units
from idne.epistemic_progression.loader import initial_epistemic_state
from idne.epistemic_progression.materialize import MaterializeStats, materialize_package
from idne.epistemic_progression.model import EpistemicState, PlayableEvent
from idne.epistemic_progression.serialize import event_to_dict
from idne.epistemic_progression.template_navigation import (
    UnresolvedDestinationError,
    build_template_choice_map,
    build_template_navigation_graph,
    resolve_template_destination,
)

ADV = ROOT / "adventures" / "The_Cold_Storage_Alarm"
ADVENTURE = ADV / "adventure"
DNR = ADVENTURE / "DO_NOT_READ"

INITIAL_KNOWLEDGE = [
    "KNOW-OPEN-ALARM",
    "KNOW-OPEN-CZ1-FAULT",
    "KNOW-OPEN-DEADLINE",
    "KNOW-OPEN-ROLE",
]

INITIAL_OBSERVABLE = ["NPC-ELENA", "NPC-DEV", "NPC-PAT", "LOC-DOCK", "LOC-COLD"]

OPENING_HUB_ACTIONS = [
    {
        "action_id": "ACT-DOCK-TALK-ELENA",
        "action_type": "approach_npc",
        "label": "Talk to Elena Morales.",
        "destination_unit_id": "UNIT-DOCK-ELENA-HUB",
        "requires_observable": ["NPC-ELENA"],
    },
    {
        "action_id": "ACT-DOCK-GO-COLD",
        "action_type": "nav",
        "label": "Walk through the dock corridor to the cold storage hall.",
        "destination_unit_id": "UNIT-COLD-BASE",
    },
    {
        "action_id": "ACT-DOCK-TALK-WORKER",
        "action_type": "approach_npc",
        "label": "Talk to a dock worker.",
        "destination_unit_id": "UNIT-DOCK-WORKER-HUB",
        "requires_observable": ["NPC-PAT", "NPC-DEV"],
    },
]

ELENA_HUB_ACTIONS = [
    {
        "action_id": "ACT-ELENA-BEGIN",
        "action_type": "dialogue_topic",
        "label": "Ask where the investigation should begin.",
        "destination_unit_id": "UNIT-ELENA-BEGIN",
    },
    {
        "action_id": "ACT-ELENA-MAP",
        "action_type": "dialogue_topic",
        "label": "Ask whether a map or site overview is available.",
        "destination_unit_id": "UNIT-ELENA-MAP",
    },
    {
        "action_id": "ACT-ELENA-STAFF",
        "action_type": "dialogue_topic",
        "label": "Ask who was still on site working late.",
        "destination_unit_id": "UNIT-ELENA-STAFF",
    },
    {
        "action_id": "ACT-ELENA-RETURN",
        "action_type": "return",
        "label": "Return to the loading dock.",
        "destination_unit_id": "UNIT-DOCK-BASE",
        "exhaustion": "repeatable",
    },
]

WORKER_HUB_ACTIONS = [
    {
        "action_id": "ACT-WORKER-INCIDENT",
        "action_type": "dialogue_topic",
        "label": "Ask what they know about the incident.",
        "destination_unit_id": "UNIT-PAT-DOOR",
    },
    {
        "action_id": "ACT-WORKER-ROLE",
        "action_type": "dialogue_topic",
        "label": "Ask their name and role on site.",
        "destination_unit_id": "UNIT-WORKER-ROLE",
    },
    {
        "action_id": "ACT-WORKER-TENURE",
        "action_type": "dialogue_topic",
        "label": "Ask how long they have worked here.",
        "destination_unit_id": "UNIT-WORKER-TENURE",
    },
    {
        "action_id": "ACT-WORKER-LOCAL",
        "action_type": "dialogue_topic",
        "label": "Ask who or what they know locally.",
        "destination_unit_id": "UNIT-WORKER-LOCAL",
    },
    {
        "action_id": "ACT-WORKER-RETURN",
        "action_type": "return",
        "label": "Return to the loading dock.",
        "destination_unit_id": "UNIT-DOCK-BASE",
        "exhaustion": "repeatable",
    },
]

LORI_HUB_ACTIONS = [
    {
        "action_id": "ACT-LORI-DENY-COLD",
        "action_type": "dialogue_topic",
        "label": "Ask whether you entered cold storage after hours.",
        "destination_unit_id": "UNIT-LORI-DENY-COLD",
    },
    {
        "action_id": "ACT-LORI-CONTROL-MIN",
        "action_type": "dialogue_topic",
        "label": "Ask about your control room visit around 23:20.",
        "destination_unit_id": "UNIT-LORI-CONTROL-MIN",
        "requires_knowledge_ids": ["KNOW-CONTROL-ENTRY"],
    },
    {
        "action_id": "ACT-LORI-PRESSURE",
        "action_type": "dialogue_topic",
        "label": "Confront with manifest exception evidence from MNF-IN-4471.",
        "destination_unit_id": "UNIT-LORI-PRESSURE",
        "requires_knowledge_ids": ["KNOW-MANIFEST-GAP"],
    },
    {
        "action_id": "ACT-LORI-LABEL",
        "action_type": "dialogue_topic",
        "label": "Press about label residue found in aisle C.",
        "destination_unit_id": "UNIT-LORI-LABEL",
        "requires_knowledge_ids": ["KNOW-LABEL-RESIDUE"],
    },
    {
        "action_id": "ACT-LORI-RETURN-MANAGER",
        "action_type": "return",
        "label": "Return to the warehouse manager office.",
        "destination_unit_id": "UNIT-MANAGER-BASE",
        "exhaustion": "repeatable",
    },
]

# Choices that require knowledge or world state before appearing on dock hub variants
DOCK_DEFERRED = {
    "Head inside to the staff break room.": ("nav", "UNIT-BREAK-BASE", ["KNOW-OPEN-ORIENT"]),
    "Cut through the warehouse corridor to the security office.": ("nav", "UNIT-SECURITY-BASE", ["KNOW-OPEN-ORIENT"]),
    "Take the office wing corridor to the warehouse manager office.": ("nav", "UNIT-MANAGER-BASE", ["KNOW-OPEN-ORIENT"]),
    "Review the supervisor briefing area.": ("action", "UNIT-DOCK-BRIEFING-MENU", ["KNOW-OPEN-ORIENT"]),
    "Request escort clearance to the automation control room.": ("action", "UNIT-ESCORT-GRANTED", ["KNOW-OPEN-ORIENT"]),
    "Work under supervisor dock restriction enforcement.": ("scene", "SC-DOCK-RESTRICTED", [], {"dock_restricted_active": True}),
    "Prepare final accountability documentation before the compliance threshold.": ("scene", "SC-ACCUSATION-PREP", [], {"ready_to_accuse": True}),
}

INFERENCE_PREFIX = "Open inference worksheet:"

DEFAULT_TOPIC_TIME_MIN = 2

# Conversation hub return profiles: (unit prefix, hub_id, hub_label, exit_dest, exit_label)
TOPIC_RETURN_PROFILES: tuple[tuple[str, str, str, str, str], ...] = (
    ("UNIT-ELENA-", "UNIT-DOCK-ELENA-HUB", "Return to the Elena conversation menu.", "UNIT-DOCK-BASE", "Return to the loading dock."),
    ("UNIT-WORKER-", "UNIT-DOCK-WORKER-HUB", "Return to the dock worker conversation menu.", "UNIT-DOCK-BASE", "Return to the loading dock."),
    ("UNIT-PAT-", "UNIT-DOCK-WORKER-HUB", "Return to the dock worker conversation menu.", "UNIT-DOCK-BASE", "Return to the loading dock."),
    ("UNIT-DEV-", "UNIT-DOCK-WORKER-HUB", "Return to the dock worker conversation menu.", "UNIT-DOCK-BASE", "Return to the loading dock."),
    ("UNIT-MARCUS-", "UNIT-SECURITY-BASE", "Return to the security office.", "UNIT-DOCK-BASE", "Return to the loading dock."),
    ("UNIT-LORI-", "UNIT-MANAGER-LORI-HUB", "Return to the Lori conversation menu.", "UNIT-MANAGER-BASE", "Return to the warehouse manager office."),
)

TOPIC_KNOWLEDGE_GRANTS: dict[str, list[str]] = {
    "UNIT-ELENA-MAP": ["KNOW-OPEN-ORIENT"],
}


def _topic_interaction_delta(unit_id: str) -> dict:
    return {"completed_topics": [unit_id]}


def _norm(label: str) -> str:
    return re.sub(r"\s+", " ", label.strip().lower())


DESTINATION_ALIASES = {
    "UNIT-DOCK-BASE-SURVEYED": "UNIT-DOCK-BASE",
    "UNIT-DOCK-BASE-RESTRICTED": "UNIT-DOCK-BASE",
}


def _hub_choice_overrides() -> dict[tuple[str, str], tuple[str, str, str]]:
    """Epistemic-only hub split routes not represented in canonical PLAYER hub menus."""
    local: dict[tuple[str, str], tuple[str, str, str]] = {}
    for action in OPENING_HUB_ACTIONS:
        local[("UNIT-DOCK-BASE", _norm(action["label"]))] = (
            action["destination_unit_id"],
            action["action_type"],
            action["label"],
        )
    for action in ELENA_HUB_ACTIONS:
        local[("UNIT-DOCK-ELENA-HUB", _norm(action["label"]))] = (
            action["destination_unit_id"],
            action["action_type"],
            action["label"],
        )
    for action in WORKER_HUB_ACTIONS:
        local[("UNIT-DOCK-WORKER-HUB", _norm(action["label"]))] = (
            action["destination_unit_id"],
            action["action_type"],
            action["label"],
        )
    for action in LORI_HUB_ACTIONS:
        local[("UNIT-MANAGER-LORI-HUB", _norm(action["label"]))] = (
            action["destination_unit_id"],
            action["action_type"],
            action["label"],
        )
    local[("UNIT-MANAGER-BASE", _norm("Speak with Lori Okonkwo about receiving and access topics you have unlocked."))] = (
        "UNIT-MANAGER-LORI-HUB",
        "approach_npc",
        "Speak with Lori Okonkwo about receiving and access topics you have unlocked.",
    )
    topic_units = (
        "UNIT-ELENA-BEGIN",
        "UNIT-ELENA-MAP",
        "UNIT-ELENA-STAFF",
        "UNIT-WORKER-ROLE",
        "UNIT-WORKER-TENURE",
        "UNIT-WORKER-LOCAL",
        "UNIT-PAT-DOOR",
        "UNIT-DEV-EXIT",
    )
    for uid in topic_units:
        for prefix, hub, hub_label, exit_dest, exit_label in TOPIC_RETURN_PROFILES:
            if uid.startswith(prefix):
                local[(uid, _norm(hub_label))] = (hub, "return", hub_label)
                local[(uid, _norm(exit_label))] = (exit_dest, "return", exit_label)
                break
    return local


def _load_check_dests() -> dict[str, tuple[str, str]]:
    cap = json.loads((DNR / "capability_check_package.json").read_text(encoding="utf-8"))
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
        _action_from_choice(
            "If your roll succeeds, go to the success section.",
            ok,
            "check_success",
        ),
        _action_from_choice(
            "If your roll fails, go to the failure section.",
            fail,
            "check_failure",
        ),
    ]


def _normalize_dest(dest: str) -> str:
    return DESTINATION_ALIASES.get(dest, dest)


def _resolve_dest(label: str, uid: str, choice_map: dict[tuple[str, str], tuple[str, str]]) -> str:
    dest, _kind = resolve_template_destination(uid, label, choice_map)
    return _normalize_dest(dest)


def _resolve_kind(label: str, uid: str, choice_map: dict[tuple[str, str], tuple[str, str]]) -> str:
    _dest, kind = resolve_template_destination(uid, label, choice_map)
    if kind == "navigate":
        return "nav"
    return kind


def _load_npc_metadata() -> tuple[dict[str, int], dict[str, str]]:
    npc = json.loads((DNR / "npc_investigation_package.json").read_text(encoding="utf-8"))
    times: dict[str, int] = {}
    grants: dict[str, str] = {}
    for conv in npc.get("conversation_graph", []) or []:
        for node in conv.get("nodes", []) or []:
            uid = node.get("npc_response_unit", "")
            if not uid:
                continue
            if node.get("time_cost_minutes") is not None:
                times[uid] = int(node["time_cost_minutes"])
            kid = node.get("grants_knowledge_id")
            if kid:
                grants[uid] = kid
    return times, grants


def _topic_return_actions(unit_id: str, *, knowledge: list[str] | None = None) -> list[dict]:
    knowledge = list(knowledge or TOPIC_KNOWLEDGE_GRANTS.get(unit_id, []))
    for prefix, hub, hub_label, exit_dest, exit_label in TOPIC_RETURN_PROFILES:
        if unit_id.startswith(prefix):
            actions = [
                {
                    "action_id": f"ACT-{unit_id}-HUB",
                    "action_type": "return",
                    "label": hub_label,
                    "destination_unit_id": hub,
                    "investigative": False,
                    "interaction_delta": _topic_interaction_delta(unit_id),
                },
                {
                    "action_id": f"ACT-{unit_id}-EXIT",
                    "action_type": "return",
                    "label": exit_label,
                    "destination_unit_id": exit_dest,
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


def _load_manifest() -> dict:
    return json.loads((ADV / "player_mapping_manifest.json").read_text(encoding="utf-8"))


def _load_flow() -> dict:
    return json.loads((DNR / "investigation_flow_package.json").read_text(encoding="utf-8"))


def _action_from_choice(label: str, dest: str, kind: str, *, requires=None, world=None, refs=None, inv=False):
    return {
        "action_id": f"ACT-{dest}",
        "action_type": kind if kind != "navigate" else "nav",
        "label": label,
        "destination_unit_id": dest,
        "requires_knowledge_ids": requires or [],
        "requires_world_state": world or {},
        "referenced_fact_ids": refs or [],
        "investigative": inv,
    }


def _content_block(
    block_id: str,
    text: str,
    *,
    provenance: str = "prior_knowledge",
    requires=None,
    forbidden=None,
    world=None,
    forbidden_world=None,
    order: int = 0,
) -> dict:
    return {
        "block_id": block_id,
        "text": text,
        "provenance": provenance,
        "requires_knowledge_ids": requires or [],
        "forbidden_knowledge_ids": forbidden or [],
        "requires_world_state": world or {},
        "forbidden_world_state": forbidden_world or {},
        "presentation_order": order,
    }


DOCK_NARRATIVE_BLOCKS = [
    _content_block(
        "CTX-DOCK-NO-ORIENT",
        "Beyond the immediate dock and cold corridor, the office wing and warehouse routes are not yet marked in your notes.",
        forbidden=["KNOW-OPEN-ORIENT"],
        order=10,
    ),
    _content_block(
        "CTX-DOCK-ORIENT-KNOWN",
        "The folded site map is in your notes, and the corridors to the break room, security office, and manager wing are clear.",
        requires=["KNOW-OPEN-ORIENT"],
        forbidden_world={"dock_restricted_active": True},
        order=10,
    ),
    _content_block(
        "CTX-DOCK-RESTRICTED",
        "Elena has tightened dock access: movement beyond approved routes requires her clearance until the restriction lifts.",
        world={"dock_restricted_active": True},
        order=20,
    ),
    _content_block(
        "CTX-DOCK-ACCUSATION-READY",
        "The compliance threshold is approaching. Final accountability documentation could still be prepared before time runs out.",
        world={"ready_to_accuse": True},
        order=30,
    ),
]

ELENA_HUB_NARRATIVE_BLOCKS = [
    _content_block(
        "CTX-ELENA-MAP-AVAILABLE",
        "A folded site map rests on the briefing table for anyone who still needs a layout overview.",
        forbidden=["KNOW-OPEN-ORIENT"],
        provenance="atmosphere",
        order=10,
    ),
    _content_block(
        "CTX-ELENA-ORIENT-KNOWN",
        "The site map from her briefing table is already folded into your notes when you need to confirm a corridor name.",
        requires=["KNOW-OPEN-ORIENT"],
        order=10,
    ),
]

SECURITY_NARRATIVE_BLOCKS = [
    _content_block(
        "CTX-SECURITY-ORIENT",
        "With the site layout noted, the warehouse corridors back toward the dock and manager wing are easy to retrace from here.",
        requires=["KNOW-OPEN-ORIENT"],
        order=10,
    ),
]


def _event(unit_id: str, kind: str, actions: list, **extra) -> dict:
    loc = "LOC-DOCK" if "DOCK" in unit_id else ""
    if unit_id.startswith("UNIT-COLD"):
        loc = "LOC-COLD"
    elif unit_id.startswith("UNIT-SECURITY"):
        loc = "LOC-SECURITY"
    elif unit_id.startswith("UNIT-MANAGER"):
        loc = "LOC-MANAGER"
    elif unit_id.startswith("UNIT-BREAK"):
        loc = "LOC-BREAK"
    elif unit_id.startswith("UNIT-CONTROL"):
        loc = "LOC-CONTROL"
    return {
        "event_id": f"EVT-{unit_id}",
        "unit_id": unit_id,
        "location_id": loc or extra.get("location_id", "LOC-DOCK"),
        "physical_location_id": extra.get("physical_location_id", loc or "LOC-DOCK"),
        "event_kind": kind,
        "structured_actions": actions,
        **{k: v for k, v in extra.items() if k not in ("location_id", "physical_location_id")},
    }


def _build_consolidated_dock_actions() -> list[dict]:
    """Single dock template: actions gated by knowledge/world-state prerequisites."""
    actions = list(OPENING_HUB_ACTIONS)
    for label, spec in DOCK_DEFERRED.items():
        kind, dest, req = spec[0], spec[1], spec[2]
        world = spec[3] if len(spec) > 3 else {}
        actions.append(_action_from_choice(label, dest, kind, requires=req, world=world))
    return actions


def _build_manager_base_actions() -> list[dict]:
    """Location hub only — Lori dialogue lives on UNIT-MANAGER-LORI-HUB."""
    return [
        _action_from_choice(
            "Review the open receiving reconciliation screen.",
            "UNIT-MANIFEST-MENU",
            "action",
        ),
        {
            "action_id": "ACT-MANAGER-TALK-LORI",
            "action_type": "approach_npc",
            "label": "Speak with Lori Okonkwo about receiving and access topics you have unlocked.",
            "destination_unit_id": "UNIT-MANAGER-LORI-HUB",
        },
        _action_from_choice("Return to the loading dock.", "UNIT-DOCK-BASE", "return"),
        _action_from_choice("Return to the break room.", "UNIT-BREAK-BASE", "return"),
    ]


def build_epistemic_events(manifest: dict) -> list[dict]:
    events: list[dict] = []
    player_units = parse_player_units(ADVENTURE / "PLAYER")
    hub_overrides = _hub_choice_overrides()
    nav_graph = build_template_navigation_graph(ADVENTURE, player_units, hub_overrides=hub_overrides)
    choice_map = build_template_choice_map(
        ADVENTURE,
        player_units,
        extra_edges={(k, v[:2]) for k, v in hub_overrides.items()},
        graph=nav_graph,
    )
    check_dests = _load_check_dests()
    _topic_times, npc_grants = _load_npc_metadata()
    TOPIC_KNOWLEDGE_GRANTS.update({uid: [kid] for uid, kid in npc_grants.items() if uid not in TOPIC_KNOWLEDGE_GRANTS})

    events.append(
        _event(
            "UNIT-DOCK-BASE",
            "location_hub",
            _build_consolidated_dock_actions(),
            required_knowledge_ids=[],
            relevant_knowledge_dependencies=["KNOW-OPEN-ORIENT", "KNOW-BMS-COMMAND"],
            relevant_world_state_dependencies=["dock_restricted_active", "ready_to_accuse", "control_escort_cleared"],
            observable_entities=["NPC-ELENA", "NPC-DEV", "NPC-PAT"],
            physical_location_id="LOC-DOCK",
            content_blocks=DOCK_NARRATIVE_BLOCKS,
        )
    )
    events.append(
        _event(
            "UNIT-DOCK-ELENA-HUB",
            "npc_interaction",
            ELENA_HUB_ACTIONS,
            observable_entities=["NPC-ELENA"],
            content_blocks=ELENA_HUB_NARRATIVE_BLOCKS,
        )
    )
    events.append(_event("UNIT-DOCK-WORKER-HUB", "npc_interaction", WORKER_HUB_ACTIONS, observable_entities=["NPC-PAT", "NPC-DEV"]))
    events.append(
        _event(
            "UNIT-MANAGER-BASE",
            "location_hub",
            _build_manager_base_actions(),
            observable_entities=["NPC-LORI"],
            physical_location_id="LOC-MANAGER",
        )
    )
    events.append(
        _event(
            "UNIT-MANAGER-LORI-HUB",
            "npc_interaction",
            LORI_HUB_ACTIONS,
            observable_entities=["NPC-LORI"],
            physical_location_id="LOC-MANAGER",
        )
    )

    handled = {
        "UNIT-DOCK-BASE",
        "UNIT-DOCK-ELENA-HUB",
        "UNIT-DOCK-WORKER-HUB",
        "UNIT-MANAGER-BASE",
        "UNIT-MANAGER-LORI-HUB",
    }

    for uid in sorted(player_units.keys()):
        if uid in handled:
            continue
        unit = player_units[uid]
        choices = unit.choices
        if not choices and uid not in {"END-PERFECT", "END-PARTIAL-INCOMPLETE"}:
            # endings and leaf nodes may have no forward choices
            if not uid.startswith("END-"):
                continue
        kind = "location_hub" if uid.endswith("-BASE") or uid.endswith("-BASE-SURVEYED") or uid.endswith("-BASE-RESTRICTED") else "action"
        if uid.startswith("INF-"):
            kind = "inference"
        elif uid.startswith("SC-"):
            kind = "scene"
        elif uid.startswith("END-"):
            kind = "ending"
        elif uid.startswith("REC-"):
            kind = "recovery"
        elif "ELENA-HUB" in uid or "WORKER-HUB" in uid or "LORI-HUB" in uid:
            kind = "npc_interaction"
        elif uid.startswith("UNIT-ELENA") or uid.startswith("UNIT-DEV") or uid.startswith("UNIT-PAT") or uid.startswith("UNIT-LORI") or uid.startswith("UNIT-MARCUS") or uid.startswith("UNIT-WORKER"):
            kind = "dialogue_topic"
        topic_returns = _topic_return_actions(uid)
        check_actions = _check_declaration_actions(uid, check_dests)
        if check_actions:
            actions = check_actions
        elif topic_returns and kind == "dialogue_topic":
            actions = topic_returns
        else:
            actions = []
            for label in choices:
                try:
                    dest = _normalize_dest(_resolve_dest(label, uid, choice_map))
                    ck = _resolve_kind(label, uid, choice_map)
                except UnresolvedDestinationError as exc:
                    raise UnresolvedDestinationError(exc.unit_id, exc.label) from exc
                req: list[str] = []
                refs: list[str] = []
                if INFERENCE_PREFIX in label:
                    req = _inference_gate_requirements(label)
                if "CLO-1847" in label:
                    req = ["KNOW-MAINT-SESSION"]
                if "contractor badge" in label.lower():
                    req = ["KNOW-EXIT-SCAN"]
                if "CTRL-TERM-02" in label or "maintenance session" in label.lower():
                    req = ["KNOW-MAINT-SESSION"]
                if "manifest exception" in label.lower():
                    req = ["KNOW-MANIFEST-GAP"]
                if "label residue" in label.lower():
                    req = ["KNOW-LABEL-RESIDUE"]
                if "dock access restriction" in label.lower():
                    req = ["KNOW-DOCK-RESTRICT"]
                if "escort clearance" in label.lower():
                    req = ["KNOW-OPEN-ORIENT"]
                actions.append(_action_from_choice(label, dest, ck, requires=req, refs=refs, inv=False))
        extra: dict = {}
        if uid.endswith("-BASE") or "DOCK-BASE" in uid:
            extra["relevant_knowledge_dependencies"] = _infer_relevant_knowledge(actions)
            extra["physical_location_id"] = "LOC-DOCK"
        if uid == "SC-DOCK-INITIAL-SURVEY":
            for action in actions:
                action["knowledge_delta"] = ["KNOW-OPEN-ORIENT"]
                action["world_state_delta"] = {"investigation_phase": 1}
                action["investigative"] = True
                action["purpose"] = "initial orientation"
        if uid == "SC-DOCK-ARRIVAL":
            for action in actions:
                if "Return" in action.get("label", ""):
                    continue
                action["knowledge_delta"] = list(set(list(action.get("knowledge_delta", [])) + ["KNOW-OPEN-ORIENT"]))
                action["investigative"] = True
                action["purpose"] = "supervisor briefing"
        if uid == "SC-IT-RECORDS-POLICY":
            actions.append(
                _action_from_choice(
                    "Return to the security office.",
                    "UNIT-SECURITY-BASE",
                    "return",
                )
            )
        if uid == "UNIT-SECURITY-BASE":
            extra["content_blocks"] = SECURITY_NARRATIVE_BLOCKS
        events.append(_event(uid, kind, actions, **extra))
        handled.add(uid)

    events.append(
        _event(
            "SC-IT-RECORDS-POLICY",
            "scene",
            [
                _action_from_choice(
                    "Review the archive sync policy notice.",
                    "UNIT-IT-ARCHIVE-POLICY",
                    "alias",
                )
            ],
        )
    )
    handled.add("SC-IT-RECORDS-POLICY")

    # New general topic units referenced by hubs (player prose generated in build_cold_storage_player.py)
    for uid in (
        "UNIT-ELENA-BEGIN",
        "UNIT-ELENA-MAP",
        "UNIT-WORKER-ROLE",
        "UNIT-WORKER-TENURE",
        "UNIT-WORKER-LOCAL",
    ):
        if uid not in handled:
            returns = _topic_return_actions(uid)
            if returns:
                events.append(_event(uid, "dialogue_topic", returns))
                handled.add(uid)

    return events


def _inference_gate_requirements(label: str) -> list[str]:
    gates = {
        "Badge misattributed": ["KNOW-BADGE-COLD-ENTRY", "KNOW-EXIT-SCAN"],
        "Staging root cause": ["KNOW-STAGING-SUSPEND", "KNOW-TEMP-TREND"],
        "Relabel fraud": ["KNOW-LABEL-RESIDUE", "KNOW-MANIFEST-GAP"],
        "Control access mismatch": ["KNOW-CONTROL-ENTRY", "KNOW-BMS-COMMAND"],
        "Culprit supported": ["KNOW-BADGE-COLD-ENTRY", "KNOW-MANIFEST-GAP", "KNOW-CONTROL-ENTRY"],
        "Perfect reconstruction": ["KNOW-BMS-COMMAND", "KNOW-LABEL-TIMESTAMP", "KNOW-STAGING-SUSPEND"],
    }
    for key, req in gates.items():
        if key in label:
            return req
    return ["KNOW-BMS-COMMAND"]


def _infer_relevant_knowledge(actions: list) -> list[str]:
    deps: set[str] = set()
    for a in actions:
        deps.update(a.get("requires_knowledge_ids") or [])
        deps.update(a.get("referenced_fact_ids") or [])
    return sorted(deps)


def write_epistemic_package(events: list[dict]) -> MaterializeStats:
    flow = _load_flow()
    initial_world = dict(flow.get("state_model", {}).get("initial_state") or {})
    templates: dict[str, PlayableEvent] = {}
    for raw in events:
        raw.setdefault("template_unit_id", raw["unit_id"])
        templates[raw["unit_id"]] = PlayableEvent.from_dict(raw)

    initial = EpistemicState(
        player_knowledge=frozenset(INITIAL_KNOWLEDGE),
        world_state=initial_world,
        interaction_state={"exhausted_actions": [], "completed_topics": []},
        observable_entities=frozenset(INITIAL_OBSERVABLE),
        observable_objects=frozenset(),
    )
    materialized, stats = materialize_package(
        templates,
        start_template_unit="UNIT-DOCK-BASE",
        initial_state=initial,
    )
    materialized.adventure_id = "The_Cold_Storage_Alarm"

    template_menu_catalog = {
        tpl_id: [a.label for a in tpl.structured_actions if a.label]
        for tpl_id, tpl in templates.items()
        if tpl.event_kind == "npc_interaction"
    }

    pkg = {
        "schema_version": "1.0",
        "adventure_id": "The_Cold_Storage_Alarm",
        "initial_player_knowledge": INITIAL_KNOWLEDGE,
        "initial_world_state": initial_world,
        "initial_observable_entities": INITIAL_OBSERVABLE,
        "materialization": stats.to_dict(),
        "template_menu_catalog": template_menu_catalog,
        "playable_events": [event_to_dict(e) for e in sorted(materialized.events_by_unit.values(), key=lambda e: e.unit_id)],
    }
    (DNR / "epistemic_progression_package.json").write_text(json.dumps(pkg, indent=2) + "\n", encoding="utf-8")
    manifest = {
        "schema_version": "1.0",
        "epistemic_progression_method": "canonical",
        "package_path": "DO_NOT_READ/epistemic_progression_package.json",
        "materialization": stats.to_dict(),
    }
    (ADVENTURE / "epistemic_progression_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    gen_path = ADV / ".generation" / "generation_state.json"
    if gen_path.exists():
        gen = json.loads(gen_path.read_text(encoding="utf-8"))
        gen.setdefault("validator_results", {})["epistemic_progression"] = {"status": "PENDING"}
        gen_path.write_text(json.dumps(gen, indent=2) + "\n", encoding="utf-8")
    return stats


def main() -> None:
    manifest = _load_manifest()
    events = build_epistemic_events(manifest)
    stats = write_epistemic_package(events)
    print(
        f"Wrote materialized epistemic package: "
        f"{stats.template_count} templates -> {stats.materialized_count} events, "
        f"{stats.reachable_states} reachable states, peak queue {stats.peak_queue_size}"
    )


if __name__ == "__main__":
    main()
