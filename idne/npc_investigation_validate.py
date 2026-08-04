"""NPC Investigation System validation (Milestone 5B)."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

STATIC_PROPERTIES = frozenset(
    {"motivation", "honesty", "deception", "manipulation", "loyalty", "fear"}
)
DYNAMIC_STATE_FIELDS = frozenset(
    {"trust", "information_known", "revealed_topics", "suspicion", "pressure"}
)
UNLOCK_TYPES = frozenset(
    {
        "trust_threshold",
        "knowledge_held",
        "player_action",
        "world_state",
        "world_time",
        "object_discovered",
        "information_known",
    }
)
ROUTE_TYPES = frozenset({"trust", "information", "player_action", "world_state", "world_time", "object_discovered"})


@dataclass
class ValidationResult:
    adventure_root: Path
    status: str
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    checks: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "adventure_root": str(self.adventure_root),
            "status": self.status,
            "errors": self.errors,
            "warnings": self.warnings,
            "checks": self.checks,
        }


def load_npc_manifest(root: Path) -> dict[str, Any] | None:
    for name in ("npc_investigation_manifest.json", "NPC_INVESTIGATION_MANIFEST.json"):
        path = root / name
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    gen = root / "generation_manifest.json"
    if gen.exists():
        data = json.loads(gen.read_text(encoding="utf-8"))
        npc = data.get("npc_investigation")
        if isinstance(npc, dict) and npc.get("enabled"):
            return {
                "schema_version": data.get("schema_version", "1.0"),
                "npc_investigation_method": "canonical",
                "package_path": npc.get(
                    "package_path", "DO_NOT_READ/npc_investigation_package.json"
                ),
            }
    return None


def load_package(root: Path, manifest: dict[str, Any]) -> dict[str, Any] | None:
    rel = manifest.get("package_path", "DO_NOT_READ/npc_investigation_package.json")
    path = root / rel
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def load_investigation_core(root: Path, package: dict[str, Any]) -> dict[str, Any] | None:
    rel = package.get("investigation_core_links", {}).get("package_path")
    if not rel:
        return None
    path = root / rel
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def validate_npc_investigation(adventure_root: str | Path) -> ValidationResult:
    root = Path(adventure_root).resolve()
    result = ValidationResult(adventure_root=root, status="PASS")

    manifest = load_npc_manifest(root)
    if not manifest:
        result.status = "SKIP"
        result.warnings.append("no npc_investigation_manifest — not declared")
        return result

    if manifest.get("npc_investigation_method") != "canonical":
        result.status = "SKIP"
        result.warnings.append("npc_investigation_method not canonical")
        return result

    package = load_package(root, manifest)
    if not package:
        result.status = "FAIL"
        result.errors.append("npc_investigation_package missing")
        result.checks["NPC-PKG-PRESENT"] = "FAIL"
        return result
    result.checks["NPC-PKG-PRESENT"] = "PASS"

    npcs = package.get("npcs", [])
    npc_ids = {str(n["npc_id"]) for n in npcs if n.get("npc_id")}
    topics = package.get("topics", [])
    topic_ids = {str(t["topic_id"]) for t in topics if t.get("topic_id")}
    info_known = package.get("information_known_model", [])
    conversations = package.get("conversation_graph", [])
    trust_model = package.get("trust_model", {})
    reactions = package.get("relationship_reactions", [])
    npc_graph = package.get("npc_graph", {})

    inv_core = load_investigation_core(root, package)
    know_ids: set[str] = set()
    test_ids: set[str] = set()
    if inv_core:
        know_ids = {str(k["knowledge_id"]) for k in inv_core.get("knowledge", []) if k.get("knowledge_id")}
        test_ids = {str(t["testimony_id"]) for t in inv_core.get("testimony", []) if t.get("testimony_id")}

    # --- NPC static properties ---
    static_ok = True
    if not npcs:
        result.errors.append("npcs empty")
        static_ok = False
    for npc in npcs:
        nid = npc.get("npc_id")
        sp = npc.get("static_properties", {})
        missing = STATIC_PROPERTIES - set(sp.keys())
        if missing:
            result.errors.append(f"NPC {nid} missing static properties: {sorted(missing)}")
            static_ok = False
        ds = npc.get("initial_dynamic_state", {})
        missing_ds = DYNAMIC_STATE_FIELDS - set(ds.keys())
        if missing_ds:
            result.errors.append(f"NPC {nid} missing dynamic state fields: {sorted(missing_ds)}")
            static_ok = False
    result.checks["NPC-STATIC"] = "PASS" if static_ok else "FAIL"

    # --- NPC graph ---
    graph_ok = True
    for node in npc_graph.get("nodes", []) or []:
        if str(node) not in npc_ids:
            result.errors.append(f"npc_graph node {node} not declared")
            graph_ok = False
    for edge in npc_graph.get("edges", []) or []:
        for key in ("from_npc_id", "to_npc_id"):
            if str(edge.get(key, "")) not in npc_ids:
                result.errors.append(f"npc_graph edge invalid {key}={edge.get(key)}")
                graph_ok = False
    result.checks["NPC-GRAPH"] = "PASS" if graph_ok else "FAIL"

    # --- InformationKnown model ---
    info_ok = True
    for entry in info_known:
        iid = entry.get("info_id")
        if str(entry.get("npc_id", "")) not in npc_ids:
            result.errors.append(f"information_known {iid} invalid npc_id")
            info_ok = False
        kid = entry.get("knowledge_id")
        if inv_core and kid and str(kid) not in know_ids:
            result.errors.append(f"information_known {iid} knowledge_id {kid} not in investigation core")
            info_ok = False
        if entry.get("topic_id") and str(entry["topic_id"]) not in topic_ids:
            result.errors.append(f"information_known {iid} invalid topic_id")
            info_ok = False
    result.checks["NPC-INFO-KNOWN"] = "PASS" if info_ok else "FAIL"

    # --- Topics and unlocking ---
    topic_ok = True
    for topic in topics:
        tid = topic.get("topic_id")
        unlocks = topic.get("unlock_conditions", [])
        if not unlocks:
            result.errors.append(f"topic {tid} has no unlock_conditions")
            topic_ok = False
        for cond in unlocks:
            if cond.get("type") not in UNLOCK_TYPES:
                result.errors.append(f"topic {tid} invalid unlock type {cond.get('type')}")
                topic_ok = False
    result.checks["NPC-TOPIC-UNLOCK"] = "PASS" if topic_ok else "FAIL"

    # --- Conversation graph ---
    conv_ok = True
    for conv in conversations:
        cid = conv.get("conversation_id")
        if str(conv.get("npc_id", "")) not in npc_ids:
            result.errors.append(f"conversation {cid} invalid npc_id")
            conv_ok = False
        routes = conv.get("route_conditions", []) or []
        if not routes:
            result.errors.append(f"conversation {cid} missing route_conditions")
            conv_ok = False
        for route in routes:
            if route.get("type") not in ROUTE_TYPES:
                result.errors.append(f"conversation {cid} invalid route type")
                conv_ok = False
        nodes = conv.get("nodes", []) or []
        if not nodes:
            result.errors.append(f"conversation {cid} has no nodes")
            conv_ok = False
        for node in nodes:
            if not node.get("player_label"):
                result.errors.append(f"conversation node {node.get('node_id')} missing player_label")
                conv_ok = False
            if not node.get("npc_response_unit"):
                result.errors.append(f"conversation node {node.get('node_id')} missing response unit")
                conv_ok = False
    result.checks["NPC-CONVERSATION"] = "PASS" if conv_ok else "FAIL"

    # --- Trust model not globally positive ---
    trust_ok = True
    modifiers = trust_model.get("modifiers", []) or []
    if trust_model.get("not_globally_positive") and not any(
        m.get("relationship_reaction", {}).get("trust_delta", 0) < 0 for m in modifiers
    ):
        if not trust_model.get("negative_trust_documented"):
            result.errors.append("trust_model lacks negative trust modifiers")
            trust_ok = False
    for mod in modifiers:
        if mod.get("trigger") == "player_accuses_npc" and not mod.get("relationship_reaction"):
            result.errors.append(f"trust modifier {mod.get('modifier_id')} missing relationship_reaction")
            trust_ok = False
    result.checks["NPC-TRUST"] = "PASS" if trust_ok else "FAIL"

    # --- Relationship reactions ---
    react_ok = True
    for react in reactions:
        rid = react.get("reaction_id")
        for key in ("actor_npc_id", "target_npc_id"):
            if str(react.get(key, "")) not in npc_ids:
                result.errors.append(f"relationship_reaction {rid} invalid {key}")
                react_ok = False
        if react.get("trust_delta") is None and react.get("suspicion_delta") is None:
            result.errors.append(f"relationship_reaction {rid} has no effect")
            react_ok = False
    result.checks["NPC-RELATION-REACT"] = "PASS" if react_ok else "FAIL"

    # --- Testimony links ---
    link_ok = True
    for link in package.get("testimony_links", []) or []:
        if link.get("testimony_id") and inv_core and str(link["testimony_id"]) not in test_ids:
            result.errors.append(f"testimony_link {link.get('testimony_id')} not in investigation core")
            link_ok = False
        if link.get("grants_knowledge_id") and inv_core and str(link["grants_knowledge_id"]) not in know_ids:
            result.errors.append(f"testimony_link grants unknown knowledge")
            link_ok = False
    result.checks["NPC-TESTIMONY-LINK"] = "PASS" if link_ok else "FAIL"

    if result.errors:
        result.status = "FAIL"
    return result


def main(argv: list[str] | None = None) -> int:
    import sys

    args = argv or sys.argv[1:]
    if not args:
        print("Usage: python3 -m idne.npc_investigation_validate <adventure_root>")
        return 2
    res = validate_npc_investigation(args[0])
    print(json.dumps(res.to_dict(), indent=2))
    return 0 if res.status in ("PASS", "SKIP") else 1


if __name__ == "__main__":
    raise SystemExit(main())
