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

# Choices that require knowledge or world state before appearing on dock hub variants
DOCK_DEFERRED = {
    "Head inside to the staff break room.": ("nav", "UNIT-BREAK-BASE", []),
    "Cut through the warehouse corridor to the security office.": ("nav", "UNIT-SECURITY-BASE", []),
    "Take the office wing corridor to the warehouse manager office.": ("nav", "UNIT-MANAGER-BASE", []),
    "Review the supervisor briefing area.": ("action", "UNIT-DOCK-BRIEFING-MENU", []),
    "Request escort clearance to the automation control room.": ("action", "UNIT-ESCORT-GRANTED", ["KNOW-OPEN-ORIENT"]),
    "Receive supervisor briefing at the loading dock.": ("scene", "SC-DOCK-ARRIVAL", []),
    "Survey the dock and adjacent corridors.": ("scene", "SC-DOCK-INITIAL-SURVEY", []),
    "Work under supervisor dock restriction enforcement.": ("scene", "SC-DOCK-RESTRICTED", [], {"dock_restricted_active": True}),
    "Prepare final accountability documentation before the compliance threshold.": ("scene", "SC-ACCUSATION-PREP", [], {"ready_to_accuse": True}),
}

INFERENCE_PREFIX = "Open inference worksheet:"


def _norm(label: str) -> str:
    return re.sub(r"\s+", " ", label.strip().lower())


def _load_canonical_choice_map() -> dict[tuple[str, str], tuple[str, str]]:
    """Load label->destination map from committed manifest before epistemic migration."""
    import subprocess

    raw = subprocess.check_output(
        ["git", "show", "HEAD:adventures/The_Cold_Storage_Alarm/player_mapping_manifest.json"],
        cwd=ROOT,
        text=True,
    )
    manifest = json.loads(raw)
    out: dict[tuple[str, str], tuple[str, str]] = {}
    for uid, entry in (manifest.get("units") or {}).items():
        for c in entry.get("choices") or []:
            out[(uid, _norm(c.get("label", "")))] = (c["destination_unit_id"], c.get("kind", "navigate"))
    return out


def _guess_dest(label: str, uid: str, manifest: dict, choice_map: dict) -> str:
    key = (uid, _norm(label))
    if key in choice_map:
        return choice_map[key][0]
    # New opening hub routes
    local = {
        _norm("Talk to Elena Morales."): "UNIT-DOCK-ELENA-HUB",
        _norm("Talk to a dock worker."): "UNIT-DOCK-WORKER-HUB",
        _norm("Ask where the investigation should begin."): "UNIT-ELENA-BEGIN",
        _norm("Ask whether a map or site overview is available."): "UNIT-ELENA-MAP",
        _norm("Ask who was still on site working late."): "UNIT-ELENA-STAFF",
        _norm("Ask what they know about the incident."): "UNIT-PAT-DOOR",
        _norm("Ask their name and role on site."): "UNIT-WORKER-ROLE",
        _norm("Ask how long they have worked here."): "UNIT-WORKER-TENURE",
        _norm("Ask who or what they know locally."): "UNIT-WORKER-LOCAL",
        _norm("Return to the loading dock."): "UNIT-DOCK-BASE",
        _norm("Return to the Elena conversation menu."): "UNIT-DOCK-ELENA-HUB",
        _norm("Return to the dock worker conversation menu."): "UNIT-DOCK-WORKER-HUB",
    }
    if _norm(label) in local:
        return local[_norm(label)]
    if "return" in label.lower():
        return uid
    return uid


def _guess_kind(label: str, uid: str, choice_map: dict) -> str:
    key = (uid, _norm(label))
    if key in choice_map:
        return choice_map[key][1]
    if "Talk to" in label:
        return "approach_npc"
    if label.lower().startswith("ask "):
        return "dialogue_topic"
    if "return" in label.lower():
        return "return"
    if "Walk" in label or "Head" in label or "Cut through" in label or "Take the" in label:
        return "nav"
    return "action"


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


def build_epistemic_events(manifest: dict) -> list[dict]:
    events: list[dict] = []
    player_units = parse_player_units(ADVENTURE / "PLAYER")
    choice_map = _load_canonical_choice_map()

    events.append(
        _event(
            "UNIT-DOCK-BASE",
            "location_hub",
            OPENING_HUB_ACTIONS,
            required_knowledge_ids=[],
            relevant_knowledge_dependencies=[],
            relevant_world_state_dependencies=["dock_restricted_active", "ready_to_accuse"],
            observable_entities=["NPC-ELENA", "NPC-DEV", "NPC-PAT"],
        )
    )
    events.append(_event("UNIT-DOCK-ELENA-HUB", "npc_interaction", ELENA_HUB_ACTIONS, observable_entities=["NPC-ELENA"]))
    events.append(_event("UNIT-DOCK-WORKER-HUB", "npc_interaction", WORKER_HUB_ACTIONS, observable_entities=["NPC-PAT", "NPC-DEV"]))

    # Expanded dock hub after initial survey / briefing
    survey_actions = list(OPENING_HUB_ACTIONS)
    for label, spec in DOCK_DEFERRED.items():
        if "restriction" in label.lower():
            continue
        kind, dest, req = spec[0], spec[1], spec[2]
        world = spec[3] if len(spec) > 3 else {}
        survey_actions.append(_action_from_choice(label, dest, kind, requires=req, world=world))
    events.append(
        _event(
            "UNIT-DOCK-BASE-SURVEYED",
            "location_hub",
            survey_actions,
            variant_of="UNIT-DOCK-BASE",
            supersedes_unit_id="UNIT-DOCK-BASE",
            required_knowledge_ids=["KNOW-OPEN-ORIENT"],
            relevant_knowledge_dependencies=["KNOW-OPEN-ORIENT", "KNOW-BMS-COMMAND"],
            relevant_world_state_dependencies=["dock_restricted_active", "control_escort_cleared"],
            physical_location_id="LOC-DOCK",
        )
    )

    dock_restricted_actions = [a for a in survey_actions if "restriction" not in a["label"].lower()]
    dock_restricted_actions.extend(
        [
            _action_from_choice(
                "Review the supervisor briefing area.",
                "UNIT-DOCK-BRIEFING-MENU",
                "action",
            ),
            _action_from_choice(
                "Request escort clearance to the automation control room.",
                "UNIT-ESCORT-GRANTED",
                "action",
                requires=["KNOW-OPEN-ORIENT"],
            ),
            _action_from_choice(
                "Receive supervisor briefing at the loading dock.",
                "SC-DOCK-ARRIVAL",
                "scene",
            ),
            _action_from_choice(
                "Survey the dock and adjacent corridors.",
                "SC-DOCK-INITIAL-SURVEY",
                "scene",
            ),
            _action_from_choice(
                "Prepare final accountability documentation before the compliance threshold.",
                "SC-ACCUSATION-PREP",
                "scene",
                world={"ready_to_accuse": True},
            ),
            _action_from_choice(
                "Work under supervisor dock restriction enforcement.",
                "SC-DOCK-RESTRICTED",
                "scene",
                world={"dock_restricted_active": True},
            ),
        ]
    )
    events.append(
        _event(
            "UNIT-DOCK-BASE-RESTRICTED",
            "location_hub",
            dock_restricted_actions,
            variant_of="UNIT-DOCK-BASE",
            required_world_state={"dock_restricted_active": True},
            relevant_world_state_dependencies=["dock_restricted_active"],
            physical_location_id="LOC-DOCK",
        )
    )

    handled = {
        "UNIT-DOCK-BASE",
        "UNIT-DOCK-ELENA-HUB",
        "UNIT-DOCK-WORKER-HUB",
        "UNIT-DOCK-BASE-SURVEYED",
        "UNIT-DOCK-BASE-RESTRICTED",
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
        elif "ELENA-HUB" in uid or "WORKER-HUB" in uid:
            kind = "npc_interaction"
        elif uid.startswith("UNIT-ELENA") or uid.startswith("UNIT-DEV") or uid.startswith("UNIT-PAT") or uid.startswith("UNIT-LORI") or uid.startswith("UNIT-MARCUS") or uid.startswith("UNIT-WORKER"):
            kind = "dialogue_topic"
        actions = []
        for label in choices:
            dest = _guess_dest(label, uid, manifest, choice_map)
            ck = _guess_kind(label, uid, choice_map)
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

    # New general topic units referenced by hubs
    for uid, body, title in [
        (
            "UNIT-ELENA-BEGIN",
            "Elena taps the incident timeline on her clipboard. "
            '"Start with cold storage and staging control. Security can pull badge records after the archive sync if you need access history."',
            "Where to begin",
        ),
        (
            "UNIT-ELENA-MAP",
            "Elena pulls a folded site map from the briefing table and marks the cold hall, security office, and manager wing. "
            '"Use this for corridors you have not walked yet. I can escort you to control if engineering access is required."',
            "Site overview",
        ),
        (
            "UNIT-WORKER-ROLE",
            "Pat Nguyen sets the mop cart aside. "
            '"Pat Nguyen — dock sanitation and floor prep. I am on the late crew when receiving runs long."',
            "Name and role",
        ),
        (
            "UNIT-WORKER-TENURE",
            "Pat thinks for a moment. "
            '"About three years on this dock. I know the cold hall doors and which bays stay open after midnight."',
            "Time on site",
        ),
        (
            "UNIT-WORKER-LOCAL",
            "Pat nods toward the office wing and the break room corridor. "
            '"Elena runs the shift. Lori stays at receiving when manifests jam. Marcus does rounds from security."',
            "Local contacts",
        ),
    ]:
        if uid not in handled:
            events.append(
                _event(
                    uid,
                    "dialogue_topic",
                    [{"action_id": f"ACT-{uid}-RET", "action_type": "return", "label": "Return to the dock worker conversation menu.", "destination_unit_id": "UNIT-DOCK-WORKER-HUB"}],
                )
            )
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


def write_epistemic_package(events: list[dict]) -> None:
    flow = _load_flow()
    initial_state = dict(flow.get("state_model", {}).get("initial_state") or {})
    pkg = {
        "schema_version": "1.0",
        "adventure_id": "The_Cold_Storage_Alarm",
        "initial_player_knowledge": INITIAL_KNOWLEDGE,
        "initial_world_state": initial_state,
        "initial_observable_entities": INITIAL_OBSERVABLE,
        "playable_events": events,
    }
    (DNR / "epistemic_progression_package.json").write_text(json.dumps(pkg, indent=2) + "\n", encoding="utf-8")
    manifest = {
        "schema_version": "1.0",
        "epistemic_progression_method": "canonical",
        "package_path": "DO_NOT_READ/epistemic_progression_package.json",
    }
    (ADVENTURE / "epistemic_progression_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    gen_path = ADV / ".generation" / "generation_state.json"
    if gen_path.exists():
        gen = json.loads(gen_path.read_text(encoding="utf-8"))
        gen.setdefault("validator_results", {})["epistemic_progression"] = {"status": "PENDING"}
        gen_path.write_text(json.dumps(gen, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    manifest = _load_manifest()
    events = build_epistemic_events(manifest)
    write_epistemic_package(events)
    print(f"Wrote epistemic package with {len(events)} playable events")


if __name__ == "__main__":
    main()
