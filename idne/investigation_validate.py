"""Integrated Investigation Validator (Milestone 7)."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from idne.investigation_state_graph import build_investigation_state_graph

BARE_NAV_RE = re.compile(
    r"(?:Go to|Choose|Continue to|Open)\s+[JPR]-\d{3}[a-z]?\b|page\s+\d+\s+or\s+\d+",
    re.I,
)
VAGUE_RECOVERY_RE = re.compile(
    r"investigate again|find more clues|look around more",
    re.I,
)
PASS_FAIL_UNIT_RE = re.compile(
    r"(success|you find|found).*(fail|nothing|missed)",
    re.I | re.S,
)

REQUIRED_CHAIN_LAYERS = frozenset(
    {
        "fixed_truth",
        "location",
        "player_action",
        "knowledge",
        "conclusion",
        "proof",
    }
)


@dataclass
class Finding:
    finding_id: str
    severity: str
    confidence: str
    layer: str
    source_file: str
    canonical_id: str
    broken_trace: list[str]
    expected_rule: str
    actual_state: str
    affected_conclusions: list[str]
    affected_endings: list[str]
    suggested_review_action: str
    automatically_fixable: bool
    human_approval_needed: bool
    tier: str = "A"

    def to_dict(self) -> dict[str, Any]:
        return {
            "finding_id": self.finding_id,
            "severity": self.severity,
            "confidence": self.confidence,
            "layer": self.layer,
            "source_file": self.source_file,
            "canonical_id": self.canonical_id,
            "broken_trace": self.broken_trace,
            "expected_rule": self.expected_rule,
            "actual_state": self.actual_state,
            "affected_conclusions": self.affected_conclusions,
            "affected_endings": self.affected_endings,
            "suggested_review_action": self.suggested_review_action,
            "automatically_fixable": self.automatically_fixable,
            "human_approval_needed": self.human_approval_needed,
            "tier": self.tier,
        }


@dataclass
class ValidationResult:
    adventure_root: Path
    status: str  # PASS | FAIL | CONDITIONAL_PASS | BLOCKED | SKIP
    findings: list[Finding] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    checks: dict[str, str] = field(default_factory=dict)
    tier_b_pending: list[str] = field(default_factory=list)
    state_graph: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "adventure_root": str(self.adventure_root),
            "status": self.status,
            "findings": [f.to_dict() for f in self.findings],
            "warnings": self.warnings,
            "checks": self.checks,
            "tier_b_pending": self.tier_b_pending,
            "state_graph": self.state_graph,
        }


def load_manifest(root: Path) -> dict[str, Any] | None:
    for name in ("investigation_validator_manifest.json", "INVESTIGATION_VALIDATOR_MANIFEST.json"):
        path = root / name
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    gen = root / "generation_manifest.json"
    if gen.exists():
        data = json.loads(gen.read_text(encoding="utf-8"))
        iv = data.get("investigation_validator")
        if isinstance(iv, dict) and iv.get("enabled"):
            return {
                "schema_version": data.get("schema_version", "1.0"),
                "investigation_validator_method": "canonical",
                "package_path": iv.get(
                    "package_path", "DO_NOT_READ/investigation_validator_package.json"
                ),
            }
    return None


def load_package(root: Path, manifest: dict[str, Any]) -> dict[str, Any] | None:
    rel = manifest.get("package_path", "DO_NOT_READ/investigation_validator_package.json")
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


def _add_finding(
    result: ValidationResult,
    finding_id: str,
    layer: str,
    canonical_id: str,
    expected: str,
    actual: str,
    conclusions: list[str] | None = None,
    endings: list[str] | None = None,
    confidence: str = "proven",
    tier: str = "A",
    human: bool = False,
) -> None:
    result.findings.append(
        Finding(
            finding_id=finding_id,
            severity="critical",
            confidence=confidence,
            layer=layer,
            source_file="investigation_validator_package.json",
            canonical_id=canonical_id,
            broken_trace=[],
            expected_rule=expected,
            actual_state=actual,
            affected_conclusions=conclusions or [],
            affected_endings=endings or [],
            suggested_review_action="Fix canonical package or linked layer",
            automatically_fixable=False,
            human_approval_needed=human,
            tier=tier,
        )
    )


def validate_investigation(adventure_root: str | Path) -> ValidationResult:
    root = Path(adventure_root).resolve()
    result = ValidationResult(adventure_root=root, status="PASS")

    manifest = load_manifest(root)
    if not manifest:
        result.status = "SKIP"
        result.warnings.append("no investigation_validator_manifest — not declared")
        return result

    if manifest.get("investigation_validator_method") != "canonical":
        result.status = "SKIP"
        result.warnings.append("investigation_validator_method not canonical")
        return result

    package = load_package(root, manifest)
    if not package:
        result.status = "FAIL"
        result.checks["IV-PKG-PRESENT"] = "FAIL"
        _add_finding(result, "IV-PKG-MISSING", "validator", "", "package present", "missing")
        return result
    result.checks["IV-PKG-PRESENT"] = "PASS"

    links = package.get("layer_links", {}) or {}
    inv_core = load_linked(root, links.get("investigation_core"))
    know_ids: set[str] = set()
    conclusion_ids: set[str] = set()
    if inv_core:
        know_ids = {str(k["knowledge_id"]) for k in inv_core.get("knowledge", []) if k.get("knowledge_id")}
        conclusion_ids = {str(c["conclusion_id"]) for c in inv_core.get("conclusions", []) if c.get("conclusion_id")}

    # Delegate capability check validator when declared
    cap_manifest = root / "capability_check_manifest.json"
    if cap_manifest.exists() and (root / "DO_NOT_READ/capability_check_package.json").exists():
        from idne.capability_check_validate import validate_capability_check

        cap_res = validate_capability_check(root)
        result.checks["IV-CAPABILITY-DELEGATE"] = "PASS" if cap_res.status == "PASS" else "FAIL"
        if cap_res.status == "FAIL":
            _add_finding(
                result,
                "IV-CAPABILITY-FAIL",
                "capability_check",
                "",
                "capability_check_validate PASS",
                f"FAIL: {cap_res.errors[:3]}",
            )
    else:
        result.checks["IV-CAPABILITY-DELEGATE"] = "PASS"

    # --- Conclusion traces ---
    trace_ok = True
    for trace in package.get("conclusion_traces", []) or []:
        cid = str(trace.get("conclusion_id", ""))
        chain = trace.get("chain", []) or []
        layers = {str(s.get("layer")) for s in chain}
        missing = REQUIRED_CHAIN_LAYERS - layers
        if missing:
            trace_ok = False
            _add_finding(
                result,
                "IV-TRACE-BROKEN",
                "conclusion_trace",
                cid,
                f"chain includes {sorted(REQUIRED_CHAIN_LAYERS)}",
                f"missing layers {sorted(missing)}",
                conclusions=[cid],
            )
        if inv_core and cid and cid not in conclusion_ids:
            trace_ok = False
            _add_finding(result, "IV-TRACE-CONCLUSION", "investigation_core", cid, "conclusion exists", "orphan")
    result.checks["IV-TRACE"] = "PASS" if trace_ok else "FAIL"

    # --- Inference answerability ---
    infer_ok = True
    for inf in package.get("inference_questions", []) or []:
        qid = str(inf.get("question_id", ""))
        undefined = inf.get("undefined_terms", []) or []
        if undefined:
            infer_ok = False
            _add_finding(result, "IV-UNDEFINED-TERM", "inference", qid, "all terms defined", str(undefined))
        for kid in inf.get("required_knowledge_ids", []) or []:
            if inv_core and str(kid) not in know_ids:
                infer_ok = False
                _add_finding(result, "IV-INFERENCE-MISSING-INFO", "inference", qid, "knowledge obtainable", f"missing {kid}")
        if not inf.get("available_before_question"):
            infer_ok = False
            _add_finding(result, "IV-INFO-AFTER-INFERENCE", "inference", qid, "facts before question", "available_after")
        alts = inf.get("equally_supported_alternatives", []) or []
        if alts and not inf.get("intentionally_ambiguous"):
            infer_ok = False
            _add_finding(result, "IV-EQUAL-ALTERNATIVES", "inference", qid, "single supported answer", str(alts))
        if inf.get("question_reveals_answer"):
            infer_ok = False
            _add_finding(result, "IV-QUESTION-LEAK", "inference", qid, "question neutral", "reveals answer")
        if inf.get("requires_internal_ids"):
            infer_ok = False
            _add_finding(result, "IV-INTERNAL-ID-QUESTION", "inference", qid, "no internal IDs", "requires IDs")
    result.checks["IV-INFERENCE"] = "PASS" if infer_ok else "FAIL"

    # --- Information sufficiency ---
    suff_ok = True
    for entry in package.get("information_sufficiency", []) or []:
        iid = str(entry.get("inference_id", ""))
        for src in entry.get("sources", []) or []:
            kid = str(src.get("knowledge_id", ""))
            if not src.get("accessible"):
                suff_ok = False
                _add_finding(result, "IV-SOURCE-INACCESSIBLE", "information", kid, "accessible source", "inaccessible")
            if not src.get("before_inference"):
                suff_ok = False
                _add_finding(result, "IV-SOURCE-LATE", "information", kid, "before inference", "after inference")
            if src.get("only_failed_route"):
                suff_ok = False
                _add_finding(result, "IV-SOURCE-FAILED-ONLY", "information", kid, "fair route", "failed only")
            if src.get("duplicate_independence"):
                suff_ok = False
                _add_finding(result, "IV-DUP-INDEPENDENCE", "information", kid, "independent sources", "duplicated")
            if src.get("requires_hidden_truth"):
                suff_ok = False
                _add_finding(result, "IV-HIDDEN-TRUTH-SOURCE", "information", kid, "player-accessible", "hidden truth")
    result.checks["IV-SUFFICIENCY"] = "PASS" if suff_ok else "FAIL"

    # --- Recovery routes ---
    recovery_ok = True
    for route in package.get("recovery_routes", []) or []:
        rid = str(route.get("route_id", ""))
        label = route.get("player_action_label", "")
        if route.get("vague_instruction") or (label and VAGUE_RECOVERY_RE.search(label)):
            recovery_ok = False
            _add_finding(result, "IV-VAGUE-RECOVERY", "recovery", rid, "named in-world action", label or "vague")
        if route.get("bare_page_code") or (label and BARE_NAV_RE.search(label)):
            recovery_ok = False
            _add_finding(result, "IV-RECOVERY-BARE-CODE", "recovery", rid, "diegetic label", label)
        if not route.get("destination_legal"):
            recovery_ok = False
            _add_finding(result, "IV-RECOVERY-ILLEGAL", "recovery", rid, "legal destination", "illegal")
        if route.get("zero_cost_loop"):
            recovery_ok = False
            _add_finding(result, "IV-ZERO-COST-LOOP", "recovery", rid, "no zero-cost loop", "loop flagged")
        if not route.get("changes_knowledge_or_access") and not route.get("changes_state"):
            recovery_ok = False
            _add_finding(result, "IV-RECOVERY-NO-CHANGE", "recovery", rid, "state change", "no change")
    result.checks["IV-RECOVERY"] = "PASS" if recovery_ok else "FAIL"

    # --- Access solvability ---
    access_ok = True
    for acc in package.get("access_requirements", []) or []:
        aid = str(acc.get("requirement_id", ""))
        if acc.get("requires_own_key"):
            access_ok = False
            _add_finding(result, "IV-KEY-OWN-LOCK", "access", aid, "key not behind own lock", "requires_own_key")
        if acc.get("mandatory") and acc.get("type") != "password" and not acc.get("discovery_route_exists"):
            access_ok = False
            _add_finding(result, "IV-ACCESS-NO-ROUTE", "access", aid, "discovery route", "none")
        if acc.get("type") == "password" and acc.get("mandatory") and not acc.get("derivation_route_exists"):
            access_ok = False
            _add_finding(result, "IV-PASSWORD-NO-ROUTE", "access", aid, "password derivation", "none")
        if acc.get("consumed_before_use"):
            access_ok = False
            _add_finding(result, "IV-ITEM-CONSUMED-EARLY", "access", aid, "item available at use", "consumed early")
    result.checks["IV-ACCESS"] = "PASS" if access_ok else "FAIL"

    # --- Mandatory check fairness ---
    check_ok = True
    for chk in package.get("mandatory_check_fairness", []) or []:
        cid = str(chk.get("check_id", ""))
        if chk.get("mandatory_path") and chk.get("failure_destroys_all_routes"):
            check_ok = False
            _add_finding(result, "IV-CHECK-DESTROYS-ROUTES", "capability_check", cid, "alternate on failure", "all routes destroyed")
        if chk.get("mandatory_path") and not chk.get("alternate_route_on_failure"):
            if not chk.get("failure_destroys_all_routes"):
                pass
            else:
                check_ok = False
    result.checks["IV-CHECK-FAIRNESS"] = "PASS" if check_ok else "FAIL"

    # --- NPC disclosure ---
    npc_ok = True
    for route in package.get("npc_disclosure_routes", []) or []:
        rid = str(route.get("route_id", ""))
        if not route.get("npc_holds_information"):
            npc_ok = False
            _add_finding(result, "IV-NPC-NO-INFO", "npc", rid, "NPC holds info", "does not hold")
        if not route.get("disclosure_route_exists"):
            npc_ok = False
            _add_finding(result, "IV-NPC-UNREACHABLE", "npc", rid, "disclosure route", "missing")
        if route.get("undefined_trust_condition"):
            npc_ok = False
            _add_finding(result, "IV-UNDEFINED-TRUST", "npc", rid, "defined trust gate", "undefined")
        if route.get("npc_leaves_before_mandatory"):
            npc_ok = False
            _add_finding(result, "IV-NPC-LEAVES-EARLY", "npc", rid, "NPC available", "leaves early")
        if route.get("impossible_social_check"):
            npc_ok = False
            _add_finding(result, "IV-NPC-IMPOSSIBLE-SOCIAL", "npc", rid, "fair social check", "impossible")
    result.checks["IV-NPC"] = "PASS" if npc_ok else "FAIL"

    # --- Time validation ---
    time_ok = True
    tv = package.get("time_validation", {}) or {}
    if not tv.get("mandatory_paths_fit_deadline"):
        time_ok = False
        _add_finding(result, "IV-DEADLINE-EXCEEDED", "time", tv.get("deadline_clock", ""), "paths fit deadline", "exceeded")
    if not tv.get("revisit_uses_current_variant"):
        time_ok = False
        _add_finding(result, "IV-TIME-VARIANT", "time", "", "revisit uses variant", "variant not used")
    if tv.get("zero_cost_investigation_loop"):
        time_ok = False
        _add_finding(result, "IV-TIME-ZERO-LOOP", "time", "", "no zero-cost loop", "loop exists")
    if tv.get("mutually_impossible_clocks"):
        time_ok = False
        _add_finding(result, "IV-TIME-CONFLICT", "time", "", "consistent clocks", "impossible clocks")
    result.checks["IV-TIME"] = "PASS" if time_ok else "FAIL"

    # --- Ending reachability ---
    ending_ok = True
    for end in package.get("ending_reachability", []) or []:
        eid = str(end.get("ending_id", ""))
        if not end.get("reachable") and not end.get("decorative"):
            ending_ok = False
            _add_finding(result, "IV-UNREACHABLE-ENDING", "ending", eid, "reachable", "unreachable", endings=[eid])
        if end.get("decorative") and end.get("impossible_trigger"):
            ending_ok = False
            _add_finding(result, "IV-DECORATIVE-IMPOSSIBLE", "ending", eid, "decorative optional", "impossible trigger")
        etype = end.get("ending_type", "")
        if etype in ("partial", "hidden", "deadline") and end.get("reveals_full_truth"):
            ending_ok = False
            _add_finding(result, "IV-ENDING-TRUTH-LEAK", "ending", eid, "imperfect no full truth", "leaks", endings=[eid])
    acc_fair = package.get("accusation_fairness", {}) or {}
    if acc_fair.get("reveal_correct_answer"):
        ending_ok = False
        _add_finding(result, "IV-ACCUSATION-REVEALS", "ending", "accusation", "neutral options", "reveals answer")
    if not acc_fair.get("options_neutral", True):
        ending_ok = False
        _add_finding(result, "IV-ACCUSATION-BIAS", "ending", "accusation", "neutral suspects", "biased")
    result.checks["IV-ENDING"] = "PASS" if ending_ok else "FAIL"

    # --- Play mode ---
    mode_ok = True
    pm = package.get("play_mode_constraints", {}) or {}
    play_modes = package.get("play_modes", []) or []
    if "single_investigator" in play_modes and not pm.get("single_investigator_valid", True):
        mode_ok = False
        _add_finding(result, "IV-SOLO-INVALID", "play_mode", "", "solo valid", "invalid")
    if pm.get("solo_requires_player_2"):
        mode_ok = False
        _add_finding(result, "IV-SOLO-REQUIRES-P2", "play_mode", "", "solo without P2", "requires player 2")
    if "two_player" in play_modes and pm.get("two_player_private_unshared"):
        mode_ok = False
        _add_finding(result, "IV-TWO-PLAYER-PRIVATE", "play_mode", "", "shareable info", "private unshared")
    result.checks["IV-PLAY-MODE"] = "PASS" if mode_ok else "FAIL"

    # --- Player audit ---
    player_ok = True
    audit = package.get("player_audit", {}) or {}
    for rel in audit.get("files", []) or []:
        path = root / rel
        if path.exists():
            text = path.read_text(encoding="utf-8")
            for i, line in enumerate(text.splitlines(), 1):
                if BARE_NAV_RE.search(line):
                    player_ok = False
                    _add_finding(result, "IV-PLAYER-BARE-CODE", "player", rel, "diegetic navigation", f"{rel}:{i}")
                if PASS_FAIL_UNIT_RE.search(line):
                    player_ok = False
                    _add_finding(result, "IV-PASS-FAIL-LEAK", "player", rel, "separate units", f"{rel}:{i}")
    for entry in audit.get("information_entries", []) or []:
        if entry.get("orphan_in_player"):
            player_ok = False
            _add_finding(result, "IV-PLAYER-NO-SOURCE", "player", entry.get("info_id", ""), "canonical source", "orphan")
    for act in audit.get("canonical_actions", []) or []:
        if not act.get("present_in_player"):
            player_ok = False
            _add_finding(result, "IV-PLAYER-MISSING-ACTION", "player", act.get("canonical_ref", ""), "in PLAYER", "missing")
    for dest in audit.get("destination_refs", []) or []:
        if not dest.get("exists"):
            player_ok = False
            _add_finding(result, "IV-DESTINATION-MISSING", "player", dest.get("destination_id", ""), "destination exists", "missing")
    if audit.get("location_reset_on_return"):
        player_ok = False
        _add_finding(result, "IV-LOCATION-RESET", "player", "", "persist location state", "resets")
    if audit.get("ending_contradicts_truth"):
        player_ok = False
        _add_finding(result, "IV-ENDING-CONTRADICTS", "player", "", "ending matches truth", "contradicts")
    result.checks["IV-PLAYER"] = "PASS" if player_ok else "FAIL"

    # --- Tier B mandatory ---
    for item in package.get("tier_b_mandatory", []) or []:
        tid = str(item.get("review_id", ""))
        if not item.get("resolved"):
            result.tier_b_pending.append(tid)
            _add_finding(
                result,
                f"IV-TIER-B-{tid}",
                "tier_b",
                tid,
                item.get("expected", "human review"),
                "pending",
                confidence="likely",
                tier="B",
                human=True,
            )

    # --- State graph ---
    graph = build_investigation_state_graph(package)
    result.state_graph = {
        "explored_states": graph.explored_states,
        "max_depth_reached": graph.max_depth_reached,
        "truncated": graph.truncated,
        "blocked": graph.blocked,
        "reason": graph.reason,
        "unique_states_explored": graph.unique_states_explored,
        "states_scheduled": graph.states_scheduled,
        "attempted_transitions": graph.attempted_transitions,
        "duplicate_states_skipped": graph.duplicate_states_skipped,
        "peak_queue_size": graph.peak_queue_size,
        "maximum_depth": graph.maximum_depth,
        "elapsed_seconds": graph.elapsed_seconds,
        "complete": graph.complete,
        "termination_reason": graph.termination_reason,
        "exceeded_limit": graph.exceeded_limit,
        "transition_counts_by_type": dict(graph.transition_counts_by_type),
    }
    if graph.blocked:
        result.checks["IV-STATE-GRAPH"] = "BLOCKED"
        _add_finding(
            result,
            "IV-STATE-EXPLOSION",
            "state_graph",
            "",
            "exploration within limits",
            graph.reason or "state explosion",
            confidence="proven",
        )
    else:
        result.checks["IV-STATE-GRAPH"] = "PASS"

    # --- Outcome ---
    proven_critical = [f for f in result.findings if f.confidence == "proven" and f.tier == "A"]
    if graph.blocked:
        result.status = "BLOCKED"
    elif proven_critical:
        result.status = "FAIL"
    elif result.tier_b_pending:
        result.status = "CONDITIONAL_PASS"
    elif result.findings:
        result.status = "CONDITIONAL_PASS"
    else:
        result.status = "PASS"

    return result


def main(argv: list[str] | None = None) -> int:
    import sys

    args = argv or sys.argv[1:]
    if not args:
        print("Usage: python3 -m idne.investigation_validate <adventure_root>")
        return 2
    res = validate_investigation(args[0])
    print(json.dumps(res.to_dict(), indent=2))
    if res.status == "BLOCKED":
        return 2
    return 0 if res.status in ("PASS", "SKIP", "CONDITIONAL_PASS") else 1


if __name__ == "__main__":
    raise SystemExit(main())
