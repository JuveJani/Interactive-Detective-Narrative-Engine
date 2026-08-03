"""Simulation metrics and diagnostic findings."""

from __future__ import annotations

import statistics
from collections import Counter, defaultdict
from typing import Any

from simulator.engine import SimulationEngine
from simulator.endings import evaluate_ending
from simulator.graph import build_edges, fake_choices, graph_stats
from simulator.models import Finding, RunResult
from simulator.self_check import SimulatorSelfCheck, simulator_trustworthy
from simulator.state import GameState
from simulator.strategies import STRATEGIES, get_strategy


def _clue_grants(adapter: dict[str, Any]) -> dict[str, list[str]]:
    grants: dict[str, list[str]] = defaultdict(list)
    for nid, spec in adapter["nodes"].items():
        for c in spec.get("clues", []):
            grants[c].append(nid)
    return grants


def _engine_e901_reachable(package: dict[str, Any]) -> bool:
    """Verify engine can mark I-03 and reach E-901 with valid play state."""
    adapter = package["adapter"]
    rng = __import__("random").Random(0)
    engine = SimulationEngine(package, rng)
    st = GameState(node="J-510", clock=1300)
    st.clues = {"C-01", "C-04", "C-05", "C-06", "C-12"}
    st.flags = {"MOTIVE_WITNESS"}
    st.infers_done = {"I-01", "I-02"}

    def accuse(s, o, r):
        return {"target": adapter["truth"]["culprit"]}

    st2 = engine.step(st, accuse)
    if "I-03" not in st2.infers_done:
        return False
    st2.node = "J-600"
    return evaluate_ending(st2, adapter) == "E-901"


def analyze_simulation(
    package: dict[str, Any],
    runs: list[RunResult],
    static_findings: list[Finding],
) -> tuple[list[Finding], dict[str, Any]]:
    adapter = package["adapter"]
    findings = list(static_findings)
    stats = graph_stats(adapter)

    precheck = SimulatorSelfCheck(package)
    precheck_ok = precheck.run_all()
    findings.extend(precheck.findings())

    trustworthy, trust_blockers = simulator_trustworthy(adapter)
    if not trustworthy:
        findings.append(
            Finding(
                id="SIM-TRUST-DOWNGRADE",
                severity="major",
                confidence="high",
                evidence="; ".join(trust_blockers),
                file="sim_adapter.json",
                identifier="ambiguities",
                expected_rule="Monte Carlo metrics require resolved adapter semantics",
                layer="UNDETERMINED",
                auto_fix_possible=False,
                human_approval_required=True,
            )
        )

    engine_ok = _engine_e901_reachable(package)
    if not engine_ok:
        findings.append(
            Finding(
                id="SIM-ENGINE-E901",
                severity="critical",
                confidence="high",
                evidence="Engine cannot reach E-901 via J-510 step with valid proof state",
                file="simulator/engine.py",
                identifier="E-901",
                expected_rule="Correct ending reachable when conditions satisfied",
                layer="SIMULATOR",
                auto_fix_possible=True,
                human_approval_required=False,
            )
        )

    ending_counts = Counter(r.ending for r in runs)
    total = max(len(runs), 1)

    e901 = ending_counts.get("E-901", 0) / total
    if runs and e901 == 0 and precheck_ok and engine_ok and trustworthy:
        findings.append(
            Finding(
                id="SIM-NO-WIN",
                severity="major",
                confidence="medium",
                evidence=f"0/{len(runs)} runs reached E-901 (simulator prechecks passed)",
                file="sim_adapter.json",
                identifier="E-901",
                expected_rule="Correct ending reachable on legal paths",
                layer="UNDETERMINED",
                auto_fix_possible=False,
                human_approval_required=True,
            )
        )
    elif runs and e901 == 0 and not (precheck_ok and engine_ok):
        findings.append(
            Finding(
                id="SIM-NO-WIN-SUPPRESSED",
                severity="info",
                confidence="high",
                evidence=f"0/{len(runs)} E-901 but simulator prechecks failed — not attributed to adventure",
                file="simulator/diagnostics.py",
                identifier="E-901",
                expected_rule="Do not blame adventure when simulator suspect",
                layer="SIMULATOR",
                auto_fix_possible=False,
                human_approval_required=False,
            )
        )

    people_only = _solo_role_clues(adapter, "people")
    records_only = _solo_role_clues(adapter, "records")
    if _can_solo_prove(people_only):
        findings.append(
            Finding(
                id="SIM-SOLO-PEOPLE",
                severity="major",
                confidence="medium",
                evidence=f"People role clues alone may complete proof: {sorted(people_only)}",
                file="sim_adapter.json",
                identifier="people",
                expected_rule="One role should not solo-solve",
                layer="UNDETERMINED" if not trustworthy else "ADVENTURE",
                auto_fix_possible=False,
                human_approval_required=True,
            )
        )
    if _can_solo_prove(records_only):
        findings.append(
            Finding(
                id="SIM-SOLO-RECORDS",
                severity="minor",
                confidence="medium",
                evidence=f"Records path may approach full proof alone: {sorted(records_only)}",
                file="sim_adapter.json",
                identifier="records",
                expected_rule="Cooperative proof requires both roles",
                layer="UNDETERMINED" if not trustworthy else "ADVENTURE",
                auto_fix_possible=False,
                human_approval_required=True,
            )
        )

    grants = _clue_grants(adapter)
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
                    layer="UNDETERMINED" if not trustworthy else "ADVENTURE",
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

    impactful_pct = _impactful_decision_pct(adapter)
    split_deltas = []
    for r in runs:
        for seg in getattr(r, "split_segments", []) or []:
            split_deltas.append(abs(seg.get("people_minutes", 0) - seg.get("records_minutes", 0)))

    metrics = {
        "graph": stats,
        "ending_distribution": dict(ending_counts),
        "ending_rates": {k: v / total for k, v in ending_counts.items()},
        "runs": len(runs),
        "fiction_minutes_avg": statistics.mean([r.fiction_minutes for r in runs]) if runs else 0,
        "avg_clues": statistics.mean([len(r.clues) for r in runs]) if runs else 0,
        "path_diversity": len({tuple(r.path) for r in runs}),
        "impactful_decision_pct": impactful_pct,
        "clue_bottlenecks": bottlenecks,
        "fake_choices": fake,
        "split_balance": _split_balance_stats(runs),
        "simulator_precheck_ok": precheck_ok,
        "simulator_engine_e901_ok": engine_ok,
        "simulator_trustworthy": trustworthy,
        "trust_blockers": trust_blockers,
    }
    return findings, metrics


def _solo_role_clues(adapter: dict[str, Any], role: str) -> set[str]:
    clues: set[str] = set()
    for nid, spec in adapter["nodes"].items():
        if spec.get("role") == role:
            clues.update(spec.get("clues", []))
    return clues


def _can_solo_prove(clues: set[str]) -> bool:
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
    deltas = []
    for r in runs:
        for seg in r.split_segments:
            deltas.append(abs(seg.get("people_minutes", 0) - seg.get("records_minutes", 0)))
    return {
        "avg_role_delta_minutes": statistics.mean(deltas) if deltas else 0,
        "max_role_delta_minutes": max(deltas) if deltas else 0,
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
                fiction_minutes=final.clock - package["adapter"].get("start_clock", 1140),
                clues=sorted(final.clues),
                flags=sorted(final.flags),
                proof_tags=tags,
                accused=final.accused,
                path=final.path,
                split_segments=list(final.split_segments),
            )
        )
    return results
