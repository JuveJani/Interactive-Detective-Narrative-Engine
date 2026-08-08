"""Map canonical knowledge grants onto template actions (no materialization)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from idne.epistemic_progression.model import StructuredAction


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def _resolve_knowledge(placeholder: str, core_pkg: dict[str, Any]) -> str:
    resolution = (core_pkg.get("placeholder_resolution") or {}).get(placeholder)
    if resolution:
        return str(resolution)
    info_map = (core_pkg.get("object_interaction_links") or {}).get("info_id_to_knowledge_id") or {}
    if placeholder in info_map:
        return str(info_map[placeholder])
    if placeholder.startswith("KNOW-"):
        return placeholder
    return ""


def build_unit_knowledge_map(adventure_root: Path) -> dict[str, str]:
    """Template unit id -> canonical knowledge id granted when content is acquired."""
    dnr = adventure_root / "DO_NOT_READ"
    core_pkg = _read_json(dnr / "investigation_core_package.json")
    obj_pkg = _read_json(dnr / "object_interaction_package.json")
    npc_pkg = _read_json(dnr / "npc_investigation_package.json")
    out: dict[str, str] = {}

    for ru in obj_pkg.get("result_units") or []:
        uid = ru.get("unit_id", "")
        ph = ru.get("player_knowledge_placeholder", "")
        if ph and uid:
            kid = _resolve_knowledge(str(ph), core_pkg)
            if kid:
                out[uid] = kid
        for info in ru.get("reveals_information") or []:
            kid = _resolve_knowledge(str(info), core_pkg)
            if kid and uid:
                out.setdefault(uid, kid)

    for act in obj_pkg.get("actions") or []:
        dest = act.get("destination_unit", "")
        ph = act.get("player_knowledge_placeholder", "")
        if dest and ph:
            kid = _resolve_knowledge(str(ph), core_pkg)
            if kid:
                out[dest] = kid

    for conv in npc_pkg.get("conversation_graph") or []:
        for node in conv.get("nodes") or []:
            uid = node.get("npc_response_unit", "")
            kid = node.get("grants_knowledge_id", "")
            if uid and kid:
                out[uid] = str(kid)

    return out


def apply_inbound_knowledge_grants(
    events: list[dict[str, Any]],
    unit_knowledge: dict[str, str],
) -> None:
    """Add knowledge_delta to actions navigating to knowledge-granting units (template only)."""
    for event in events:
        for action in event.get("structured_actions") or []:
            dest = str(action.get("destination_unit_id", "")).split("--S-")[0]
            kid = unit_knowledge.get(dest)
            if not kid:
                continue
            existing = list(action.get("knowledge_delta") or [])
            if kid not in existing:
                action["knowledge_delta"] = existing + [kid]
                action["investigative"] = True
                if not action.get("purpose"):
                    action["purpose"] = "evidence acquisition"


def augment_action_knowledge(action: StructuredAction, unit_knowledge: dict[str, str]) -> StructuredAction:
    """Return action with inbound knowledge grant if destination acquires knowledge."""
    from idne.epistemic_progression.fingerprint import template_unit_id

    dest = template_unit_id(action.destination_unit_id)
    kid = unit_knowledge.get(dest)
    if not kid or kid in action.knowledge_delta:
        return action
    return StructuredAction(
        action_id=action.action_id,
        action_type=action.action_type,
        label=action.label,
        destination_unit_id=action.destination_unit_id,
        requires_knowledge_ids=action.requires_knowledge_ids,
        forbidden_knowledge_ids=action.forbidden_knowledge_ids,
        requires_world_state=dict(action.requires_world_state),
        forbidden_world_state=dict(action.forbidden_world_state),
        requires_observable=action.requires_observable,
        referenced_fact_ids=action.referenced_fact_ids,
        referenced_entity_ids=action.referenced_entity_ids,
        exhaustion=action.exhaustion,
        knowledge_delta=list(action.knowledge_delta) + [kid],
        world_state_delta=dict(action.world_state_delta),
        interaction_delta=dict(action.interaction_delta),
        investigative=True,
        purpose=action.purpose or "evidence acquisition",
    )
