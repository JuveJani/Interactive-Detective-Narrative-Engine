"""Investigation Flow & Ending System validation (Milestone 5C)."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

PERFECT_TYPES = frozenset({"perfect"})
IMPERFECT_TYPES = frozenset({"partial", "hidden", "deadline", "failure", "narrative_failure"})
TRUTH_REVEAL_COMPLETE = frozenset({"complete", "full"})


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


def load_flow_manifest(root: Path) -> dict[str, Any] | None:
    for name in ("investigation_flow_manifest.json", "INVESTIGATION_FLOW_MANIFEST.json"):
        path = root / name
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    gen = root / "generation_manifest.json"
    if gen.exists():
        data = json.loads(gen.read_text(encoding="utf-8"))
        flow = data.get("investigation_flow")
        if isinstance(flow, dict) and flow.get("enabled"):
            return {
                "schema_version": data.get("schema_version", "1.0"),
                "investigation_flow_method": "canonical",
                "package_path": flow.get(
                    "package_path", "DO_NOT_READ/investigation_flow_package.json"
                ),
            }
    return None


def load_package(root: Path, manifest: dict[str, Any]) -> dict[str, Any] | None:
    rel = manifest.get("package_path", "DO_NOT_READ/investigation_flow_package.json")
    path = root / rel
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def load_linked(root: Path, rel: str | None) -> dict[str, Any] | None:
    if not rel:
        return None
    path = root / rel
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _flag_names(state_model: dict[str, Any]) -> set[str]:
    flags = state_model.get("flags", []) or []
    names: set[str] = set()
    for f in flags:
        if isinstance(f, dict) and f.get("flag_id"):
            names.add(str(f["flag_id"]))
        elif isinstance(f, str):
            names.add(f)
    return names


def _counter_names(state_model: dict[str, Any]) -> set[str]:
    counters = state_model.get("counters", []) or []
    names: set[str] = set()
    for c in counters:
        if isinstance(c, dict) and c.get("counter_id"):
            names.add(str(c["counter_id"]))
        elif isinstance(c, str):
            names.add(c)
    return names


def _collect_state_keys(obj: Any, keys: set[str]) -> None:
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in ("flag", "flag_id", "counter", "counter_id"):
                keys.add(str(v))
            _collect_state_keys(v, keys)
    elif isinstance(obj, list):
        for item in obj:
            _collect_state_keys(item, keys)


def _knowledge_acquirable_before(
    know_id: str,
    knowledge_by_id: dict[str, dict[str, Any]],
    visited: set[str] | None = None,
) -> set[str]:
    """Return prerequisite knowledge ids for acquiring know_id (transitive)."""
    if visited is None:
        visited = set()
    if know_id in visited:
        return visited
    visited.add(know_id)
    item = knowledge_by_id.get(know_id)
    if not item:
        return visited
    acq = item.get("acquisition", {})
    src_type = acq.get("source_type")
    src_id = acq.get("source_id")
    if src_type == "synthesis" and src_id:
        hyp = None
        for k, v in knowledge_by_id.items():
            pass
        # synthesis source_id is hypothesis — handled via requires on hypotheses in core
    if src_type in ("observation", "physical_evidence", "testimony", "world_fact"):
        return visited
    if src_type == "hypothesis" and src_id:
        visited.add(str(src_id))
    return visited


def validate_investigation_flow(adventure_root: str | Path) -> ValidationResult:
    root = Path(adventure_root).resolve()
    result = ValidationResult(adventure_root=root, status="PASS")

    manifest = load_flow_manifest(root)
    if not manifest:
        result.status = "SKIP"
        result.warnings.append("no investigation_flow_manifest — not declared")
        return result

    if manifest.get("investigation_flow_method") != "canonical":
        result.status = "SKIP"
        result.warnings.append("investigation_flow_method not canonical")
        return result

    package = load_package(root, manifest)
    if not package:
        result.status = "FAIL"
        result.errors.append("investigation_flow_package missing")
        result.checks["FLOW-PKG-PRESENT"] = "FAIL"
        return result
    result.checks["FLOW-PKG-PRESENT"] = "PASS"

    state_model = package.get("state_model", {}) or {}
    flag_names = _flag_names(state_model)
    counter_names = _counter_names(state_model)
    initial = state_model.get("initial_state", {}) or {}

    inv_core = load_linked(
        root,
        package.get("investigation_core_links", {}).get("package_path"),
    )
    env_pkg = load_linked(
        root,
        package.get("environment_links", {}).get("package_path"),
    )

    know_ids: set[str] = set()
    conclusion_by_id: dict[str, dict[str, Any]] = {}
    proofs_by_conclusion: dict[str, list[dict[str, Any]]] = {}
    knowledge_by_id: dict[str, dict[str, Any]] = {}
    hypothesis_requires: dict[str, list[str]] = {}

    if inv_core:
        for k in inv_core.get("knowledge", []) or []:
            if k.get("knowledge_id"):
                kid = str(k["knowledge_id"])
                know_ids.add(kid)
                knowledge_by_id[kid] = k
        for c in inv_core.get("conclusions", []) or []:
            if c.get("conclusion_id"):
                conclusion_by_id[str(c["conclusion_id"])] = c
        for p in inv_core.get("proofs", []) or []:
            cid = p.get("conclusion_id")
            if cid:
                proofs_by_conclusion.setdefault(str(cid), []).append(p)
        for h in inv_core.get("hypotheses", []) or []:
            if h.get("hypothesis_id"):
                hypothesis_requires[str(h["hypothesis_id"])] = list(
                    h.get("requires_knowledge_ids", []) or []
                )
                if h.get("yields_knowledge_id"):
                    know_ids.add(str(h["yields_knowledge_id"]))

    loc_ids: set[str] = set()
    if env_pkg:
        for loc in env_pkg.get("locations", []) or []:
            if loc.get("location_id"):
                loc_ids.add(str(loc["location_id"]))

    endings = package.get("endings", []) or []
    ending_by_id = {str(e["ending_id"]): e for e in endings if e.get("ending_id")}
    ending_graph = package.get("ending_graph", {}) or {}
    graph_nodes = {str(n) for n in ending_graph.get("nodes", []) or []}
    eval_order = [str(x) for x in ending_graph.get("evaluation_order", []) or []]

    scene_chains = package.get("scene_chains", []) or []
    variants = package.get("world_state_variants", []) or []
    revisits = package.get("location_revisits", []) or []
    deadline = package.get("deadline", {}) or {}
    questionnaire = package.get("accusation_questionnaire", {}) or {}
    time_model = package.get("time_model", {}) or {}
    clocks = {str(c) for c in time_model.get("clocks", []) or []}

    # --- State model ---
    state_ok = True
    for key in initial.keys():
        if key not in flag_names and key not in counter_names:
            result.errors.append(f"initial_state key {key} not declared in state_model")
            state_ok = False
    result.checks["FLOW-STATE"] = "PASS" if state_ok else "FAIL"

    # --- Scene chains (time-dependent) ---
    chain_ok = True
    for chain in scene_chains:
        cid = chain.get("chain_id")
        from_clk = chain.get("active_from_clock")
        until_clk = chain.get("active_until_clock")
        if from_clk and clocks and str(from_clk) not in clocks:
            result.errors.append(f"scene_chain {cid} unknown active_from_clock {from_clk}")
            chain_ok = False
        if until_clk and clocks and str(until_clk) not in clocks:
            result.errors.append(f"scene_chain {cid} unknown active_until_clock {until_clk}")
            chain_ok = False
        steps = chain.get("steps", []) or []
        if not steps:
            result.errors.append(f"scene_chain {cid} has no steps")
            chain_ok = False
        for step in steps:
            for kid in step.get("requires_knowledge_ids", []) or []:
                if inv_core and str(kid) not in know_ids:
                    result.errors.append(f"scene_chain {cid} step unknown knowledge {kid}")
                    chain_ok = False
    result.checks["FLOW-SCENE-CHAIN"] = "PASS" if chain_ok else "FAIL"

    # --- World state variants ---
    variant_ok = True
    for var in variants:
        vid = var.get("variant_id")
        if not var.get("variants"):
            result.errors.append(f"world_state_variant {vid} has no variants")
            variant_ok = False
        for v in var.get("variants", []) or []:
            when = v.get("when_state", {}) or {}
            ref_keys: set[str] = set()
            _collect_state_keys(when, ref_keys)
            for fk in ref_keys:
                if fk not in flag_names and fk not in counter_names:
                    result.errors.append(f"variant {vid} references unknown state {fk}")
                    variant_ok = False
    result.checks["FLOW-WORLD-VARIANT"] = "PASS" if variant_ok else "FAIL"

    # --- Location revisits ---
    revisit_ok = True
    for rev in revisits:
        lid = rev.get("location_id")
        if env_pkg and lid and str(lid) not in loc_ids:
            result.errors.append(f"location_revisit unknown location {lid}")
            revisit_ok = False
        for rule in rev.get("revisit_rules", []) or []:
            for kid in rule.get("when_knowledge_held", []) or []:
                if inv_core and str(kid) not in know_ids:
                    result.errors.append(f"revisit rule unknown knowledge {kid}")
                    revisit_ok = False
    result.checks["FLOW-REVISIT"] = "PASS" if revisit_ok else "FAIL"

    # --- Deadline ---
    deadline_ok = True
    if deadline.get("enabled"):
        deid = deadline.get("deadline_ending_id")
        if not deid:
            result.errors.append("deadline enabled but no deadline_ending_id")
            deadline_ok = False
        elif str(deid) not in ending_by_id:
            result.errors.append(f"deadline_ending_id {deid} not in endings")
            deadline_ok = False
        else:
            de = ending_by_id[str(deid)]
            if de.get("ending_type") != "deadline":
                result.errors.append(f"deadline_ending {deid} must have ending_type deadline")
                deadline_ok = False
            if de.get("reveals_full_truth"):
                result.errors.append(f"deadline_ending {deid} must not reveals_full_truth")
                deadline_ok = False
        clk = deadline.get("deadline_clock") or time_model.get("deadline_clock")
        if clk and clocks and str(clk) not in clocks:
            result.errors.append(f"deadline_clock {clk} not in time_model.clocks")
            deadline_ok = False
    result.checks["FLOW-DEADLINE"] = "PASS" if deadline_ok else "FAIL"

    # --- Ending graph ---
    graph_ok = True
    if not endings:
        result.errors.append("endings empty")
        graph_ok = False
    for eid in graph_nodes:
        if eid not in ending_by_id:
            result.errors.append(f"ending_graph node {eid} not declared in endings")
            graph_ok = False
    for eid in ending_by_id:
        if graph_nodes and eid not in graph_nodes:
            result.errors.append(f"ending {eid} missing from ending_graph.nodes")
            graph_ok = False
    for eid in eval_order:
        if eid not in ending_by_id:
            result.errors.append(f"evaluation_order references unknown ending {eid}")
            graph_ok = False
    result.checks["FLOW-ENDING-GRAPH"] = "PASS" if graph_ok else "FAIL"

    # --- Truth leak (imperfect endings must not reveal full solution) ---
    leak_ok = True
    for ending in endings:
        eid = ending.get("ending_id")
        etype = ending.get("ending_type", "")
        reveals = ending.get("reveals_full_truth", False)
        scope = str(ending.get("truth_reveal_scope", "")).lower()
        if etype in IMPERFECT_TYPES or etype not in PERFECT_TYPES:
            if reveals:
                result.errors.append(f"ending {eid} ({etype}) reveals_full_truth forbidden")
                leak_ok = False
            if scope in TRUTH_REVEAL_COMPLETE:
                result.errors.append(f"ending {eid} ({etype}) truth_reveal_scope must not be complete")
                leak_ok = False
        if etype == "perfect" and not reveals and scope not in TRUTH_REVEAL_COMPLETE:
            result.warnings.append(f"perfect ending {eid} should reveal complete truth")
    result.checks["FLOW-TRUTH-LEAK"] = "PASS" if leak_ok else "FAIL"

    # --- State inconsistencies ---
    inconsist_ok = True
    declared_state = flag_names | counter_names
    for ending in endings:
        eid = ending.get("ending_id")
        trigger = ending.get("trigger", {}) or {}
        req_state = trigger.get("required_state", {}) or {}
        for fk in req_state.keys():
            if fk not in declared_state:
                result.errors.append(f"ending {eid} required_state unknown flag {fk}")
                inconsist_ok = False
        # contradictory required_state in same trigger
        if isinstance(req_state, dict):
            for k, v in req_state.items():
                if k.endswith("_not") and k[:-4] in req_state:
                    if req_state[k] == req_state[k[:-4]]:
                        result.errors.append(f"ending {eid} contradictory required_state on {k}")
                        inconsist_ok = False
    for chain in scene_chains:
        for step in chain.get("steps", []) or []:
            rs = step.get("requires_state", {}) or {}
            for fk in rs.keys():
                if fk not in declared_state:
                    result.errors.append(
                        f"scene_chain step {step.get('step_id')} unknown state {fk}"
                    )
                    inconsist_ok = False
    result.checks["FLOW-STATE-INCONSIST"] = "PASS" if inconsist_ok else "FAIL"

    # --- Impossible endings ---
    impossible_ok = True
    for ending in endings:
        eid = ending.get("ending_id")
        trigger = ending.get("trigger", {}) or {}
        req_acc = trigger.get("required_accusation", {}) or {}
        req_state = trigger.get("required_state", {}) or {}
        # Same trigger requires conflicting accusation answers
        if "Q-CULPRIT" in req_acc and req_state.get("accused_npc_id"):
            if str(req_acc["Q-CULPRIT"]) != str(req_state["accused_npc_id"]):
                result.errors.append(f"ending {eid} impossible accusation conflict")
                impossible_ok = False
        if trigger.get("type") == "deadline_expired" and trigger.get("required_knowledge_ids"):
            result.errors.append(f"ending {eid} deadline trigger cannot require knowledge")
            impossible_ok = False
        if trigger.get("impossible_by_design"):
            result.errors.append(f"ending {eid} marked impossible_by_design")
            impossible_ok = False
    result.checks["FLOW-IMPOSSIBLE"] = "PASS" if impossible_ok else "FAIL"

    # --- Unsupported accusations ---
    accuse_ok = True
    if questionnaire.get("required_before_ending_eval") and not questionnaire.get("questions"):
        result.errors.append("accusation_questionnaire required but questions empty")
        accuse_ok = False
    for q in questionnaire.get("questions", []) or []:
        qid = q.get("question_id")
        cid = q.get("conclusion_id")
        if inv_core and cid and str(cid) not in conclusion_by_id:
            result.errors.append(f"question {qid} conclusion {cid} not in investigation core")
            accuse_ok = False
        if inv_core and cid and not proofs_by_conclusion.get(str(cid)):
            result.errors.append(f"question {qid} conclusion {cid} has no proof route")
            accuse_ok = False
    # Perfect ending must align accusation with conclusions and cover at least one proof route
    for ending in endings:
        if ending.get("ending_type") != "perfect":
            continue
        eid = ending.get("ending_id")
        trigger = ending.get("trigger", {}) or {}
        req_know = {str(k) for k in trigger.get("required_knowledge_ids", []) or []}
        req_acc = trigger.get("required_accusation", {}) or {}
        for q in questionnaire.get("questions", []) or []:
            qid = q.get("question_id")
            cid = q.get("conclusion_id")
            if not cid or qid not in req_acc:
                continue
            answer = req_acc.get(qid)
            conc = conclusion_by_id.get(str(cid))
            if conc and answer and conc.get("answer_entity_id"):
                if str(answer) != str(conc.get("answer_entity_id")):
                    result.errors.append(f"perfect ending {eid} accusation mismatch for {cid}")
                    accuse_ok = False
        if inv_core and trigger.get("requires_full_proof"):
            culprit_cids = [
                str(c["conclusion_id"])
                for c in inv_core.get("conclusions", []) or []
                if c.get("category") == "culprit" and c.get("conclusion_id")
            ]
            for cid in culprit_cids:
                proofs = proofs_by_conclusion.get(cid, [])
                if proofs and req_know:
                    covered = any(
                        set(p.get("required_knowledge_ids", []) or []).issubset(req_know)
                        for p in proofs
                    )
                    if not covered:
                        result.errors.append(f"perfect ending {eid} lacks full proof for {cid}")
                        accuse_ok = False
    result.checks["FLOW-UNSUPPORTED-ACCUSATION"] = "PASS" if accuse_ok else "FAIL"

    # --- Unreachable chains / endings ---
    unreachable_ok = True
    for chain in scene_chains:
        cid = chain.get("chain_id")
        if chain.get("unreachable_by_design"):
            result.errors.append(f"scene_chain {cid} marked unreachable_by_design")
            unreachable_ok = False
        first_step = (chain.get("steps", []) or [])[0] if chain.get("steps") else None
        if first_step:
            for kid in first_step.get("requires_knowledge_ids", []) or []:
                if inv_core:
                    acq = knowledge_by_id.get(str(kid), {}).get("acquisition", {})
                    if acq.get("interaction_required") and not first_step.get("allows_prior_acquisition"):
                        result.errors.append(
                            f"scene_chain {cid} first step requires unobtainable-at-entry knowledge {kid}"
                        )
                        unreachable_ok = False
    for ending in endings:
        eid = ending.get("ending_id")
        if ending.get("unreachable_by_design"):
            result.errors.append(f"ending {eid} marked unreachable_by_design")
            unreachable_ok = False
        trigger = ending.get("trigger", {}) or {}
        if trigger.get("never_reachable"):
            result.errors.append(f"ending {eid} trigger never_reachable")
            unreachable_ok = False
    # Graph connectivity: each non-hidden ending should appear in evaluation_order or edges
    if eval_order and graph_nodes:
        reachable_from_eval = set(eval_order)
        for eid in ending_by_id:
            e = ending_by_id[eid]
            if not e.get("hidden") and eid not in reachable_from_eval:
                result.warnings.append(f"ending {eid} not in evaluation_order")
    result.checks["FLOW-UNREACHABLE"] = "PASS" if unreachable_ok else "FAIL"

    if result.errors:
        result.status = "FAIL"
    return result


def main(argv: list[str] | None = None) -> int:
    import sys

    args = argv or sys.argv[1:]
    if not args:
        print("Usage: python3 -m idne.investigation_flow_validate <adventure_root>")
        return 2
    res = validate_investigation_flow(args[0])
    print(json.dumps(res.to_dict(), indent=2))
    return 0 if res.status in ("PASS", "SKIP") else 1


if __name__ == "__main__":
    raise SystemExit(main())
