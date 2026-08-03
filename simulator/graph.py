"""Investigation graph construction and analysis."""

from __future__ import annotations

from collections import defaultdict, deque
from typing import Any

from simulator.models import GraphEdge


def build_edges(adapter: dict[str, Any]) -> list[GraphEdge]:
    nodes = adapter["nodes"]
    edges: list[GraphEdge] = []
    for nid, spec in nodes.items():
        ntype = spec.get("type")
        role = spec.get("role")
        if ntype == "hub":
            for ch in spec.get("choices", []):
                edges.append(
                    GraphEdge(nid, ch["target"], ch.get("id", ""), ch.get("minutes", 0), None)
                )
        elif "choices" in spec:
            for ch in spec["choices"]:
                edges.append(GraphEdge(nid, ch["target"], ch.get("id", ""), 0, role))
        if "next" in spec:
            edges.append(GraphEdge(nid, spec["next"], "auto", spec.get("minutes", 0), role))
        for tgt in spec.get("next_options", []):
            edges.append(GraphEdge(nid, tgt, "option", spec.get("minutes", 0), role))
        if spec.get("early_finish") and spec.get("sync"):
            edges.append(
                GraphEdge(nid, spec["sync"], "early_finish", spec.get("minutes", 0), role)
            )
        if ntype == "split_launch":
            sp = adapter["splits"][spec["split"]]
            edges.append(GraphEdge(nid, sp["people_start"], "people_branch", 0, "people"))
            edges.append(GraphEdge(nid, sp["records_start"], "records_branch", 0, "records"))
        if ntype == "regroup":
            edges.append(
                GraphEdge(nid, spec["next"], "regroup", spec.get("minutes_overhead", 5), None)
            )
        if ntype == "infer" and "next" in spec:
            edges.append(GraphEdge(nid, spec["next"], "infer", spec.get("minutes", 0), None))
        if ntype == "ending_dispatch":
            for code in ("E-901", "E-902", "E-903", "E-904", "E-905"):
                edges.append(GraphEdge(nid, code, "ending", 0, None))
    return edges


def reachable_nodes(adapter: dict[str, Any]) -> set[str]:
    start = adapter["start_node"]
    edges = build_edges(adapter)
    adj: dict[str, set[str]] = defaultdict(set)
    for e in edges:
        adj[e.source].add(e.target)
    seen = {start}
    q = deque([start])
    while q:
        n = q.popleft()
        for t in adj.get(n, ()):
            if t not in seen:
                seen.add(t)
                q.append(t)
    return seen


def unreachable_nodes(adapter: dict[str, Any]) -> list[str]:
    all_nodes = set(adapter["nodes"])
    return sorted(all_nodes - reachable_nodes(adapter))


def nodes_without_outgoing(adapter: dict[str, Any]) -> list[str]:
    edges = build_edges(adapter)
    outgoing = {e.source for e in edges}
    terminals = []
    for nid, spec in adapter["nodes"].items():
        if spec.get("type") == "ending":
            continue
        if nid not in outgoing and spec.get("type") != "ending_dispatch":
            terminals.append(nid)
    return terminals


def fake_choices(adapter: dict[str, Any]) -> list[str]:
    return [
        nid
        for nid, spec in adapter["nodes"].items()
        if spec.get("fake_choice") or (
            spec.get("type") == "hub"
            and len({c["target"] for c in spec.get("choices", [])}) < len(spec.get("choices", []))
        )
    ]


def graph_stats(adapter: dict[str, Any]) -> dict[str, Any]:
    edges = build_edges(adapter)
    nodes = set(adapter["nodes"])
    reach = reachable_nodes(adapter)
    out_deg: dict[str, int] = defaultdict(int)
    in_deg: dict[str, int] = defaultdict(int)
    for e in edges:
        out_deg[e.source] += 1
        in_deg[e.target] += 1
    branching = [n for n, d in out_deg.items() if d > 1]
    return {
        "node_count": len(nodes),
        "edge_count": len(edges),
        "reachable_count": len(reach),
        "unreachable": unreachable_nodes(adapter),
        "dead_ends": nodes_without_outgoing(adapter),
        "branching_nodes": len(branching),
        "fake_choices": fake_choices(adapter),
    }
