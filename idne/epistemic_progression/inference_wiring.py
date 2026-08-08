"""Wire inference, accusation, and endings into epistemic template events."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from idne.ending_resolution import ending_submit_actions
from idne.epistemic_progression.knowledge_wiring import apply_inbound_knowledge_grants, build_unit_knowledge_map


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def hypothesis_yields(core_pkg: dict[str, Any]) -> dict[str, str]:
    out: dict[str, str] = {}
    for hyp in core_pkg.get("hypotheses") or []:
        hid = str(hyp.get("hypothesis_id", ""))
        kid = str(hyp.get("yields_knowledge_id", ""))
        if hid.startswith("HYP-") and kid:
            out[hid.replace("HYP-", "INF-", 1)] = kid
    return out


def _recovery_return_target(flow_pkg: dict[str, Any], recovery_id: str) -> str:
    for route in flow_pkg.get("recovery_routes") or []:
        if route.get("route_id") == recovery_id:
            ref = route.get("destination_ref", "")
            if ref.startswith("LOC-"):
                return f"UNIT-{ref.replace('LOC-', '')}-BASE"
    return "UNIT-DOCK-BASE"


def build_inference_actions(
    inf_id: str,
    *,
    flow_pkg: dict[str, Any],
    yields: dict[str, str],
) -> list[dict[str, Any]]:
    gates = {g["inference_id"]: g for g in flow_pkg.get("inference_flow_gates") or [] if g.get("inference_id")}
    gate = gates.get(inf_id, {})
    req_k = list(gate.get("required_knowledge_ids") or [])
    success_ws = dict(gate.get("success_state_updates") or {})
    kid = yields.get(inf_id, "")
    recovery = (gate.get("recovery_routes") or ["REC-REVISIT-ANY-UNRESOLVED-SOURCE"])[0]
    return [
        {
            "action_id": f"ACT-{inf_id}-COMPLETE",
            "action_type": "inference",
            "label": "Mark synthesis complete if your answer is supported.",
            "destination_unit_id": _recovery_return_target(flow_pkg, recovery),
            "requires_knowledge_ids": req_k,
            "world_state_delta": success_ws,
            "knowledge_delta": [kid] if kid else [],
            "investigative": True,
            "purpose": "inference synthesis",
        },
        {
            "action_id": f"ACT-{inf_id}-INCOMPLETE",
            "action_type": "inference",
            "label": "Mark synthesis incomplete and follow a recovery prompt in the recovery file.",
            "destination_unit_id": recovery,
            "requires_knowledge_ids": req_k,
            "investigative": False,
        },
    ]


def inference_entry_actions(player_units: dict[str, Any], *, flow_pkg: dict[str, Any]) -> list[dict[str, Any]]:
    actions: list[dict[str, Any]] = []
    for gate in flow_pkg.get("inference_flow_gates") or []:
        inf_id = gate.get("inference_id", "")
        if not inf_id or inf_id not in player_units:
            continue
        title = player_units[inf_id].title
        actions.append(
            {
                "action_id": f"ACT-OPEN-{inf_id}",
                "action_type": "inference_entry",
                "label": f"Open inference worksheet: {title}.",
                "destination_unit_id": inf_id,
                "requires_knowledge_ids": list(gate.get("required_knowledge_ids") or []),
                "investigative": True,
                "purpose": "inference access",
            }
        )
    return actions


def enrich_location_hub_actions(
    actions: list[dict[str, Any]],
    hub_unit_id: str,
    player_units: dict[str, Any],
    flow_pkg: dict[str, Any],
) -> list[dict[str, Any]]:
    if not hub_unit_id.endswith("-BASE"):
        return actions
    existing = {a.get("label", "") for a in actions}
    out = list(actions)
    for action in inference_entry_actions(player_units, flow_pkg=flow_pkg):
        if action["label"] not in existing:
            out.append(action)
    return out


def build_cold_storage_template_events(adventure_root: Path, player_units: dict[str, Any]) -> list[dict[str, Any]]:
    """Build enriched template events for Cold Storage progression wiring."""
    import sys

    root = Path(__file__).resolve().parents[2]
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    from scripts.build_cold_storage_epistemic import build_epistemic_events, _load_manifest

    return enrich_epistemic_templates(build_epistemic_events(_load_manifest()), adventure_root, player_units)


def enrich_epistemic_templates(
    events: list[dict[str, Any]],
    adventure_root: Path,
    player_units: dict[str, Any],
) -> list[dict[str, Any]]:
    dnr = adventure_root / "DO_NOT_READ"
    flow_pkg = _read_json(dnr / "investigation_flow_package.json")
    core_pkg = _read_json(dnr / "investigation_core_package.json")
    yields = hypothesis_yields(core_pkg)
    by_id = {e["unit_id"]: e for e in events}

    for inf_id in sorted(uid for uid in player_units if uid.startswith("INF-")):
        if inf_id in by_id:
            by_id[inf_id]["structured_actions"] = build_inference_actions(inf_id, flow_pkg=flow_pkg, yields=yields)
            by_id[inf_id]["event_kind"] = "inference"

    submit_actions = ending_submit_actions(flow_pkg)
    if "SC-ACCUSATION-PREP" in by_id:
        by_id["SC-ACCUSATION-PREP"]["structured_actions"] = [
            {
                "action_id": "ACT-ACCUSATION-SUBMIT-MENU",
                "action_type": "scene",
                "label": "Continue this scene thread.",
                "destination_unit_id": "SC-ACCUSATION-SUBMIT",
                "requires_world_state": {"ready_to_accuse": True},
            },
            {
                "action_id": "ACT-ACCUSATION-PREP-RETURN",
                "action_type": "return",
                "label": "Return to the location base section for this area.",
                "destination_unit_id": "UNIT-DOCK-BASE",
            },
        ]
    by_id["SC-ACCUSATION-SUBMIT"] = {
        "event_id": "EVT-SC-ACCUSATION-SUBMIT",
        "unit_id": "SC-ACCUSATION-SUBMIT",
        "template_unit_id": "SC-ACCUSATION-SUBMIT",
        "location_id": "LOC-DOCK",
        "physical_location_id": "LOC-DOCK",
        "event_kind": "accusation",
        "structured_actions": submit_actions,
        "required_world_state": {"ready_to_accuse": True},
    }

    for uid, event in list(by_id.items()):
        if event.get("event_kind") == "location_hub" or uid.endswith("-BASE"):
            event["structured_actions"] = enrich_location_hub_actions(
                list(event.get("structured_actions") or []),
                uid,
                player_units,
                flow_pkg,
            )

    for uid in player_units:
        if uid.startswith("END-") and uid in by_id:
            by_id[uid]["structured_actions"] = []
            by_id[uid]["event_kind"] = "ending"

    result = list(by_id.values())
    unit_knowledge = build_unit_knowledge_map(adventure_root)
    apply_inbound_knowledge_grants(result, unit_knowledge)
    return result


def load_template_progression_events(adventure_root: Path) -> dict[str, Any]:
    """Load template progression events keyed by unit_id (PlayableEvent dicts as StructuredAction sources)."""
    from idne.epistemic_progression.model import PlayableEvent
    from idne.gamebook_nav.extract import parse_player_units

    player_units = parse_player_units(adventure_root / "PLAYER")
    adv_id = adventure_root.parent.name
    if adv_id == "The_Cold_Storage_Alarm":
        raw = build_cold_storage_template_events(adventure_root, player_units)
    else:
        from idne.adventure_pack.epistemic import build_epistemic_events
        from idne.adventure_pack.spec import load_pack_spec

        spec_path = adventure_root.parent / "pack_spec.json"
        if not spec_path.exists():
            return {}
        spec = load_pack_spec(spec_path)
        raw = enrich_epistemic_templates(build_epistemic_events(spec, adventure_root, {}), adventure_root, player_units)

    return {e["unit_id"]: PlayableEvent.from_dict(e) for e in raw}
