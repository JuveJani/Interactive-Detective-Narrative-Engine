"""Static validation and cross-layer checks."""

from __future__ import annotations

import re
from typing import Any

from simulator.graph import build_edges, graph_stats, unreachable_nodes
from simulator.models import Finding


def validate_static(package: dict[str, Any]) -> list[Finding]:
    adapter = package["adapter"]
    player = package.get("player_text", {})
    findings: list[Finding] = []

    stats = graph_stats(adapter)
    for node in stats["unreachable"]:
        findings.append(
            Finding(
                id=f"VAL-UNREACH-{node}",
                severity="major",
                confidence="high",
                evidence=f"Node {node} not reachable from {adapter['start_node']}",
                file="sim_adapter.json",
                identifier=node,
                expected_rule="All playable nodes reachable",
                layer="ADVENTURE",
                auto_fix_possible=False,
                human_approval_required=True,
            )
        )

    for node in stats["dead_ends"]:
        if not node.startswith("E-"):
            findings.append(
                Finding(
                    id=f"VAL-DEAD-{node}",
                    severity="major",
                    confidence="high",
                    evidence=f"No outgoing edges from {node}",
                    file="sim_adapter.json",
                    identifier=node,
                    expected_rule="Every non-terminal node has continue path",
                    layer="ADVENTURE",
                    auto_fix_possible=False,
                    human_approval_required=True,
                )
            )

    joint = player.get("joint", "")
    for code in re.findall(r"J-\d{3}", joint):
        if code not in adapter["nodes"]:
            findings.append(
                Finding(
                    id=f"VAL-MISS-J-{code}",
                    severity="major",
                    confidence="medium",
                    evidence=f"JOINT_SCENES references {code} missing from adapter",
                    file="PLAYER/JOINT_SCENES.md",
                    identifier=code,
                    expected_rule="Adapter covers all joint scene codes",
                    layer="DELIVERY_ADAPTER",
                    auto_fix_possible=True,
                    human_approval_required=False,
                )
            )

    case = player.get("case_file", "")
    adapter_clues = set()
    for spec in adapter["nodes"].values():
        adapter_clues.update(spec.get("clues", []))
    for m in re.findall(r"C-\d{2}", case):
        if m not in adapter_clues and m not in {"C-01", "C-02", "C-03", "C-04", "C-05", "C-06", "C-07", "C-08", "C-09", "C-10", "C-11", "C-12", "C-13", "C-14", "C-15"}:
            pass

    dispatch = joint[joint.find("## J-600"):] if "## J-600" in joint else ""
    if re.search(r"Tomás Reyes", dispatch, re.I):
        findings.append(
            Finding(
                id="VAL-SPOILER-J600",
                severity="critical",
                confidence="high",
                evidence="Culprit name in J-600 player text",
                file="PLAYER/JOINT_SCENES.md",
                identifier="J-600",
                expected_rule="Ending dispatch must not name culprit",
                layer="PLAYER_PACKAGE",
                auto_fix_possible=False,
                human_approval_required=True,
            )
        )

    if "(Accident" in joint:
        findings.append(
            Finding(
                id="VAL-ANSWERED-INFER",
                severity="critical",
                confidence="high",
                evidence="Answered infer parenthetical in joint scenes",
                file="PLAYER/JOINT_SCENES.md",
                identifier="I-01",
                expected_rule="Infer prompts must not embed answers",
                layer="PLAYER_PACKAGE",
                auto_fix_possible=False,
                human_approval_required=True,
            )
        )

    edges = build_edges(adapter)
    refs = {e.target for e in edges}
    for e in edges:
        if e.target not in adapter["nodes"]:
            findings.append(
                Finding(
                    id=f"VAL-BROKEN-{e.source}->{e.target}",
                    severity="critical",
                    confidence="high",
                    evidence=f"Broken link to unknown node {e.target}",
                    file="sim_adapter.json",
                    identifier=e.target,
                    expected_rule="All edge targets must exist",
                    layer="SIMULATOR",
                    auto_fix_possible=True,
                    human_approval_required=False,
                )
            )

    return findings
