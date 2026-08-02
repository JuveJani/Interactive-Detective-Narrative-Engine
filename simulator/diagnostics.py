"""Simulation metrics and diagnostic findings."""

from __future__ import annotations

import statistics
from collections import Counter, defaultdict
from typing import Any

from simulator.engine import SimulationEngine
from simulator.graph import build_edges, fake_choices, graph_stats
from simulator.models import Finding, RunResult
from simulator.state import GameState
from simulator.strategies import STRATEGIES, get_strategy


def _clue_grants(adapter: dict[str, Any]) -> dict[str, list[str]]:
    grants: dict[str, list[str]] = defaultdict(list)
    for nid, spec in adapter["nodes"].items():
        for c in spec.get("clues", []):
            grants[c].append(nid)
    return grants


def analyze_simulation(
    package: dict[str, Any],
    runs: list[RunResult],
    static_findings: list[Finding],
) -> tuple[list[Finding], dict[str, Any]]:
    adapter = package["adapter"]
    findings = list(static_findings)
    stats = graph_stats(adapter)

    ending_counts = Counter(r.ending for r in runs)
    total = max(len(runs), 1)

    e901 = ending_counts.get("E-901", 0) / total
    if runs and e901 == 0:
        findings.append(
            Finding(
                id="SIM-NO-WIN",
                severity="major",
                confidence="medium",
                evidence=f"0/{len(runs)} runs reached E-901",
                file="sim_adapter.json",
                identifier="E-901",
                expected_rule="Correct ending reachable on legal paths",
                layer="ADVENTURE",
                auto_fix_possible=False,
                human_approval_required=True,
            )
        )

  # solo solve check
    people_only = _solo_role_clues(adapter, "people")
    records_only = _solo_role_clues(adapter, "records")
    proof = adapter["proof_rules"]
    if _can_solo_prove(people_only, proof):
        findings.append(
            Finding(
                id="SIM-SOLO-PEOPLE",
                severity="major",
                confidence="medium",
                evidence=f"People role clues alone may complete proof: {sorted(people_only)}",
                file="sim_adapter.json",
                identifier="people",
                expected_rule="One role should not solo-solve",
                layer="ADVENTURE",
                auto_fix_possible=False,
                human_approval_required=True,
            )
        )
    if _can_solo_prove(records_only, proof):
        findings.append(
            Finding(
                id="SIM-SOLO-RECORDS",
                severity="minor",
                confidence="medium",
                evidence=f"Records path may approach full proof alone: {sorted(records_only)}",
                file="sim_adapter.json",
                identifier="records",
                expected_rule="Cooperative proof requires both roles",
                layer="ADVENTURE",
                auto_fix_possible=False,
                human_approval_required=True,
            )
        )

    grants = _clue_grants(adapter)
    for clue, sources in grants.items():
        if len(sources) > 1:
            findings.append(
                Finding(
                    id=f"SIM-DUP-{clue}",
                    severity="minor",
                    confidence="high",
                    evidence=f"{clue} granted at {sources}",
                    file="sim_adapter.json",
                    identifier=clue,
                    expected_rule="Clue idempotence — duplicate grant paths",
                    layer="ADVENTURE",
                    auto_fix_possible=False,
                    human_approval_required=False,
                )
            )

    bottlenecks = [c for c, s in grants.items() if len(s) == 1]
    for c in bottlenecks:
        if c in {"C-06", "C-05", "C-12"}:
            findings.append(
                Finding(
                    id=f"SIM-BOTTLENECK-{c}",
                    severity="info",
                    confidence="high",
                    evidence=f"Single source for {c}: {grants[c]}",
                    file="sim_adapter.json",
                    identifier=c,
                    expected_rule="Critical clues should have redundancy",
                    layer="ADVENTURE",
                    auto_fix_possible=False,
                    human_approval_required=True,
                )
            )

    fake = fake_choices(adapter)
    for nid in fake:
        findings.append(
            Finding(
                id=f"SIM-FAKE-{nid}",
                severity="minor",
                confidence="medium",
                evidence=f"Low-impact or retry loop at {nid}",
                file="sim_adapter.json",
                identifier=nid,
                expected_rule="Meaningful hub choices",
                layer="ADVENTURE",
                auto_fix_possible=False,
                human_approval_required=True,
            )
        )

    split_waits = []
    for r in runs:
        if r.split_minutes:
            split_waits.append(abs(r.joint_minutes - r.wall_minutes))
    impactful_pct = _impactful_decision_pct(adapter)

    metrics = {
        "graph": stats,
        "ending_distribution": dict(ending_counts),
        "ending_rates": {k: v / total for k, v in ending_counts.items()},
        "runs": len(runs),
        "avg_wall_minutes": statistics.mean([r.wall_minutes for r in runs]) if runs else 0,
        "avg_clues": statistics.mean([len(r.clues) for r in runs]) if runs else 0,
        "path_diversity": len({tuple(r.path) for r in runs}),
        "impactful_decision_pct": impactful_pct,
        "clue_bottlenecks": bottlenecks,
        "fake_choices": fake,
        "split_balance": _split_balance_stats(runs),
    }
    return findings, metrics


def _solo_role_clues(adapter: dict[str, Any], role: str) -> set[str]:
    clues: set[str] = set()
    for nid, spec in adapter["nodes"].items():
        if spec.get("role") == role:
            clues.update(spec.get("clues", []))
    return clues


def _can_solo_prove(clues: set[str], proof: dict[str, str]) -> bool:
    method = ("C-01" in clues and "C-04" in clues) or "C-10" in clues
    motive = "C-05" in clues or "C-11" in clues
    opp = "C-06" in clues and ("C-12" in clues or "C-13" in clues)
    return method and motive and opp


def _impactful_decision_pct(adapter: dict[str, Any]) -> float:
    nodes = adapter["nodes"]
    decision = 0
    impactful = 0
    for nid, spec in nodes.items():
        if spec.get("choices") or spec.get("type") == "hub":
            decision += 1
            if spec.get("clues") or spec.get("check") or spec.get("infer"):
                impactful += 1
            for ch in spec.get("choices", []):
                tgt = nodes.get(ch.get("target", ""), {})
                if tgt.get("clues") or tgt.get("check"):
                    impactful += 1
                    break
    return round(100 * impactful / max(decision, 1), 1)


def _split_balance_stats(runs: list[RunResult]) -> dict[str, Any]:
    if not runs:
        return {}
    people = [r.joint_minutes for r in runs]
    return {
        "avg_joint_minutes": statistics.mean(people),
        "sample_size": len(runs),
    }


def run_batch(
    package: dict[str, Any],
    strategy_name: str,
    runs: int,
    seed: int,
) -> list[RunResult]:
    import random

    results: list[RunResult] = []
    for i in range(runs):
        rng = random.Random(seed + i)
        strat = get_strategy(strategy_name, rng, package["adapter"])
        engine = SimulationEngine(package, rng)

        def choose(state: GameState, options: list, role: str):
            return strat.choose(state, options, role)

        final = engine.run(choose)
        tags = [k for k, v in final.compute_proof_tags(package["adapter"]).items() if v]
        parallel = sum(s.get("wall_minutes", 0) for s in final.split_segments)
        results.append(
            RunResult(
                seed=seed + i,
                strategy=strategy_name,
                ending=final.node,
                steps=final.steps,
                joint_minutes=final.joint_minutes,
                split_minutes=parallel,
                wall_minutes=final.joint_minutes,
                clues=sorted(final.clues),
                flags=sorted(final.flags),
                proof_tags=tags,
                accused=final.accused,
                path=final.path,
            )
        )
    return results
