"""Label and package reference resolution for gamebook navigation."""

from __future__ import annotations

import re
from typing import Iterable


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip().lower())


def tokens(s: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", norm(s)))


def match_label(choice: str, index: dict[str, str], *, min_score: float = 0.38) -> str | None:
    nchoice = norm(choice)
    if nchoice in index:
        return index[nchoice]

    ct = tokens(choice)
    best_dest = None
    best_score = 0.0
    for label, dest in index.items():
        if not dest:
            continue
        lt = tokens(label)
        if not lt:
            continue
        inter = len(ct & lt)
        score = inter / max(len(ct | lt), 1)
        if score > best_score:
            best_score = score
            best_dest = dest

    if best_score >= min_score:
        return best_dest

    for label, dest in index.items():
        if not dest or len(label) < 12:
            continue
        if label in nchoice or nchoice in label:
            return dest
    return None


def build_action_index(obj_pkg: dict, cap_pkg: dict | None = None) -> dict[str, str]:
    idx: dict[str, str] = {}
    check_decl: dict[str, str] = {}
    if cap_pkg:
        for chk in cap_pkg.get("checks", []) or []:
            cid = chk.get("check_id", "")
            decl = (chk.get("destinations", {}) or {}).get("action_unit_id", "")
            if cid and decl:
                check_decl[cid] = decl
    for act in obj_pkg.get("actions", []) or []:
        label = act.get("player_label", "")
        if not label:
            continue
        binding = act.get("check_binding") or {}
        check_id = binding.get("check_id", "")
        if check_id and check_id in check_decl:
            idx[norm(label)] = check_decl[check_id]
            continue
        dest = act.get("destination_unit", "")
        if dest:
            idx[norm(label)] = dest
    return idx


def build_object_name_index(obj_pkg: dict) -> dict[tuple[str, str], str]:
    """Map (location_id, normalized public object name) -> primary action destination."""
    objects = {o.get("object_id"): o for o in obj_pkg.get("objects", []) or []}
    primary: dict[tuple[str, str], str] = {}
    for act in obj_pkg.get("actions", []) or []:
        obj = objects.get(act.get("object_id", ""), {})
        if obj.get("parent_type") != "location":
            continue
        loc = obj.get("parent_id", "")
        pname = norm(obj.get("public_name", ""))
        dest = act.get("destination_unit", "")
        if loc and pname and dest and act.get("interaction_depth") in (None, "approached", "visible"):
            primary.setdefault((loc, pname), dest)
    return primary


def match_object_name(choice: str, location_id: str, name_index: dict[tuple[str, str], str]) -> str | None:
    nchoice = norm(choice)
    ct = tokens(choice)
    best = None
    best_score = 0.0
    for (loc, pname), dest in name_index.items():
        if loc != location_id:
            continue
        pt = tokens(pname)
        inter = len(ct & pt)
        score = inter / max(len(ct | pt), 1)
        if pname in nchoice or nchoice in pname:
            score = max(score, 0.55)
        if score > best_score:
            best_score = score
            best = dest
    if best_score >= 0.35:
        return best
    return None


def build_nav_index(env_pkg: dict, loc_bases: dict[str, str]) -> dict[tuple[str, str], str]:
    idx: dict[tuple[str, str], str] = {}
    for nav in env_pkg.get("navigation", []) or []:
        src = nav.get("source_location_id", "")
        dst = nav.get("destination_location_id", "")
        label = nav.get("player_label", "")
        if src and dst and label:
            idx[(src, norm(label))] = loc_bases.get(dst, "")
    return idx


def build_npc_index(npc_pkg: dict) -> dict[str, str]:
    idx: dict[str, str] = {}
    for conv in npc_pkg.get("conversation_graph", []) or []:
        for node in conv.get("nodes", []) or []:
            label = node.get("player_label", "")
            dest = node.get("npc_response_unit", "")
            if label and dest:
                idx[norm(label)] = dest
    return idx


def build_revisit_index(flow_pkg: dict) -> dict[str, str]:
    idx: dict[str, str] = {}
    for block in flow_pkg.get("location_revisits", []) or []:
        for rule in block.get("revisit_rules", []) or []:
            label = rule.get("player_label", "")
            scene = rule.get("unlocks_scene_unit_id", "")
            if label and scene:
                idx[norm(label)] = scene
    return idx
