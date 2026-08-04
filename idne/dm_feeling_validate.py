"""DM Feeling Validator (Milestone 10)."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from idne.dm_feeling_categories import category_scores, CATEGORIES
from idne.dm_feeling_export import write_reports
from idne.story_player_extract import collect_player_files

BARE_NAV_RE = re.compile(
    r"(?:Go to|Choose|Continue to|Open)\s+[JPR]-\d{3}[a-z]?\b|page\s+\d+\s+or\s+\d+",
    re.I,
)


@dataclass
class Finding:
    finding_id: str
    severity: str
    confidence: str
    category: str
    mode: str
    source_file: str
    entity_id: str
    player_excerpt: str
    expected_rule: str
    observed_behavior: str
    affected_paths: list[str]
    review_owner: str
    human_approval_needed: bool
    tier: str = "A"

    def to_dict(self) -> dict[str, Any]:
        return {
            "finding_id": self.finding_id,
            "severity": self.severity,
            "confidence": self.confidence,
            "category": self.category,
            "mode": self.mode,
            "source_file": self.source_file,
            "entity_id": self.entity_id,
            "player_excerpt": self.player_excerpt[:200],
            "expected_rule": self.expected_rule,
            "observed_behavior": self.observed_behavior,
            "affected_paths": self.affected_paths,
            "review_owner": self.review_owner,
            "human_approval_needed": self.human_approval_needed,
            "tier": self.tier,
        }


@dataclass
class ValidationResult:
    adventure_root: Path
    status: str
    findings: list[Finding] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    checks: dict[str, str] = field(default_factory=dict)
    category_scores: dict[str, str] = field(default_factory=dict)
    tier_b_pending: list[str] = field(default_factory=list)
    tier_c_complete: bool = False
    player_files_scanned: list[str] = field(default_factory=list)
    report_paths: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "adventure_root": str(self.adventure_root),
            "status": self.status,
            "findings": [f.to_dict() for f in self.findings],
            "warnings": self.warnings,
            "checks": self.checks,
            "category_scores": self.category_scores,
            "tier_b_pending": self.tier_b_pending,
            "tier_c_complete": self.tier_c_complete,
            "player_files_scanned": self.player_files_scanned,
            "report_paths": self.report_paths,
        }


def load_manifest(root: Path) -> dict[str, Any] | None:
    for name in ("dm_feeling_validator_manifest.json", "DM_FEELING_VALIDATOR_MANIFEST.json"):
        path = root / name
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    gen = root / "generation_manifest.json"
    if gen.exists():
        data = json.loads(gen.read_text(encoding="utf-8"))
        df = data.get("dm_feeling_validator")
        if isinstance(df, dict) and df.get("enabled"):
            return {
                "schema_version": data.get("schema_version", "1.0"),
                "dm_feeling_validator_method": "canonical",
                "package_path": df.get("package_path", "DO_NOT_READ/dm_feeling_validator_package.json"),
            }
    return None


def load_package(root: Path, manifest: dict[str, Any]) -> dict[str, Any] | None:
    rel = manifest.get("package_path", "DO_NOT_READ/dm_feeling_validator_package.json")
    path = root / rel
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _add(
    result: ValidationResult,
    finding_id: str,
    category: str,
    entity_id: str,
    expected: str,
    observed: str,
    mode: str = "",
    paths: list[str] | None = None,
    source_file: str = "dm_feeling_validator_package.json",
    excerpt: str = "",
    tier: str = "A",
    owner: str = "script",
    human: bool = False,
    severity: str = "critical",
) -> None:
    result.findings.append(
        Finding(
            finding_id=finding_id,
            severity=severity,
            confidence="proven" if tier == "A" else "likely",
            category=category,
            mode=mode,
            source_file=source_file,
            entity_id=entity_id,
            player_excerpt=excerpt,
            expected_rule=expected,
            observed_behavior=observed,
            affected_paths=paths or [],
            review_owner=owner,
            human_approval_needed=human,
            tier=tier,
        )
    )


def _check_state_graph(package: dict[str, Any]) -> tuple[bool, bool]:
    cfg = package.get("state_graph_config", {}) or {}
    if cfg.get("forced_explosion"):
        return False, True
    max_states = int(cfg.get("max_states", 5000))
    explored = int(cfg.get("explored_states", 0))
    if explored > max_states:
        return False, True
    return True, False


def validate_dm_feeling(adventure_root: str | Path, write_report_files: bool = True) -> ValidationResult:
    root = Path(adventure_root).resolve()
    result = ValidationResult(adventure_root=root, status="PASS")
    play_modes = []

    manifest = load_manifest(root)
    if not manifest:
        result.status = "SKIP"
        result.warnings.append("no dm_feeling_validator_manifest — not declared")
        return result

    if manifest.get("dm_feeling_validator_method") != "canonical":
        result.status = "SKIP"
        result.warnings.append("dm_feeling_validator_method not canonical")
        return result

    package = load_package(root, manifest)
    if not package:
        result.status = "BLOCKED"
        result.checks["DF-PKG-PRESENT"] = "BLOCKED"
        _add(result, "DF-PKG-MISSING", "player_agency", "", "package present", "missing")
        return result
    result.checks["DF-PKG-PRESENT"] = "PASS"

    play_modes = package.get("play_modes", []) or []
    mode_str = play_modes[0] if play_modes else "single_investigator"
    audit = package.get("player_audit", {}) or {}
    player_files = audit.get("files", []) or []
    player_text = collect_player_files(root, player_files)
    result.player_files_scanned = list(player_text.keys())

    # State graph
    sg_ok, sg_blocked = _check_state_graph(package)
    if sg_blocked:
        result.checks["DF-STATE-GRAPH"] = "BLOCKED"
        _add(result, "DF-STATE-EXPLOSION", "world_responsiveness", "", "within state limits", "state limit hit")
    else:
        result.checks["DF-STATE-GRAPH"] = "PASS"

    # 1. Player agency
    agency_ok = True
    pa = package.get("player_agency", {}) or {}
    for choice in pa.get("choices", []) or []:
        cid = str(choice.get("choice_id", ""))
        label = choice.get("player_label", "")
        if choice.get("bare_code") or (label and BARE_NAV_RE.search(label)):
            agency_ok = False
            _add(result, "DF-BARE-CODE", "player_agency", cid, "diegetic action label", label or "bare code", mode_str)
        if choice.get("unexplained_choice"):
            agency_ok = False
            _add(result, "DF-UNEXPLAINED-CHOICE", "player_agency", cid, "basis for decision", "unexplained", mode_str)
        if choice.get("fake_branch"):
            agency_ok = False
            _add(result, "DF-FAKE-BRANCH", "player_agency", cid, "persistent branch effect", "fake branch", mode_str)
        if choice.get("immediate_reconverge_no_effect"):
            agency_ok = False
            _add(result, "DF-RECONVERGE", "player_agency", cid, "persistent effect", "reconverge no effect", mode_str)
    for rel, text in player_text.items():
        for i, line in enumerate(text.splitlines(), 1):
            if BARE_NAV_RE.search(line):
                agency_ok = False
                _add(
                    result, "DF-BARE-CODE", "player_agency", rel, "diegetic navigation",
                    f"{rel}:{i}", mode_str, source_file=rel, excerpt=line,
                )
    result.checks["DF-AGENCY"] = "PASS" if agency_ok else "FAIL"

    # 2. Discovery vs delivery
    disc_ok = True
    dd = package.get("discovery_delivery", {}) or {}
    if dd.get("mostly_passive_reading"):
        disc_ok = False
        _add(result, "DF-PASSIVE-READING", "discovery_delivery", "", "active discovery", "mostly passive reading", mode_str)
    for grant in dd.get("information_grants", []) or []:
        gid = str(grant.get("grant_id", ""))
        if grant.get("automatic_major_grant"):
            disc_ok = False
            _add(result, "DF-AUTO-MAJOR-GRANT", "discovery_delivery", gid, "earned discovery", "automatic major grant", mode_str)
        if grant.get("direct_solution_delivery"):
            disc_ok = False
            _add(result, "DF-DIRECT-DELIVERY", "discovery_delivery", gid, "player earns solution", "direct delivery", mode_str)
        if grant.get("hidden_exposed_too_early"):
            disc_ok = False
            _add(result, "DF-HIDDEN-EARLY", "discovery_delivery", gid, "timely reveal", "exposed too early", mode_str)
    result.checks["DF-DISCOVERY"] = "PASS" if disc_ok else "FAIL"

    # 3. Exploration depth
    expl_ok = True
    ed = package.get("exploration_depth", {}) or {}
    for loc in ed.get("locations", []) or []:
        lid = str(loc.get("location_id", ""))
        if loc.get("one_paragraph_only"):
            expl_ok = False
            _add(result, "DF-SHALLOW-LOCATION", "exploration_depth", lid, "layered location", "one paragraph", mode_str)
        if loc.get("important_objects_on_arrival"):
            expl_ok = False
            _add(result, "DF-OBJECTS-ON-ARRIVAL", "exploration_depth", lid, "discovery through interaction", "objects on arrival", mode_str)
        if loc.get("state_resets_on_revisit"):
            expl_ok = False
            _add(result, "DF-RESET-LOCATION", "exploration_depth", lid, "persistent state", "resets on revisit", mode_str)
    for obj in ed.get("objects", []) or []:
        oid = str(obj.get("object_id", ""))
        if obj.get("shallow_tree"):
            expl_ok = False
            _add(result, "DF-SHALLOW-OBJECT", "exploration_depth", oid, "interaction depth", "shallow tree", mode_str)
        if not obj.get("layered_discovery", True) and obj.get("mandatory"):
            expl_ok = False
            _add(result, "DF-NO-LAYERED-OBJECT", "exploration_depth", oid, "layered discovery", "flat object", mode_str)
    result.checks["DF-EXPLORATION"] = "PASS" if expl_ok else "FAIL"

    # 4. Inference quality
    infer_ok = True
    iq = package.get("inference_quality", {}) or {}
    for inf in iq.get("inferences", []) or []:
        iid = str(inf.get("inference_id", ""))
        if inf.get("checkbox_theatre"):
            infer_ok = False
            _add(result, "DF-INFERENCE-THEATRE", "inference_quality", iid, "meaningful reasoning", "checkbox theatre", mode_str)
        if inf.get("answer_embedded_in_question"):
            infer_ok = False
            _add(result, "DF-ANSWER-IN-QUESTION", "inference_quality", iid, "neutral question", "answer embedded", mode_str)
        if inf.get("single_fact_copy"):
            infer_ok = False
            _add(result, "DF-SINGLE-FACT-COPY", "inference_quality", iid, "multi-fact reasoning", "single fact copy", mode_str)
        if inf.get("no_consequence"):
            infer_ok = False
            _add(result, "DF-INFERENCE-NO-CONSEQUENCE", "inference_quality", iid, "inference consequence", "no consequence", mode_str)
        if inf.get("impossible_question"):
            infer_ok = False
            _add(result, "DF-IMPOSSIBLE-QUESTION", "inference_quality", iid, "answerable question", "impossible", mode_str)
    result.checks["DF-INFERENCE"] = "PASS" if infer_ok else "FAIL"

    # 5. Aha potential
    aha_ok = True
    ap = package.get("aha_potential", {}) or {}
    for conc in ap.get("conclusions", []) or []:
        cid = str(conc.get("conclusion_id", ""))
        if not conc.get("connection_structure") and not conc.get("explicitly_waived"):
            aha_ok = False
            _add(result, "DF-NO-AHA-STRUCTURE", "aha_potential", cid, "connection structure", "none authored", mode_str)
        if conc.get("direct_conclusion_delivery"):
            aha_ok = False
            _add(result, "DF-DIRECT-CONCLUSION", "aha_potential", cid, "earned connection", "direct delivery", mode_str)
    result.checks["DF-AHA"] = "PASS" if aha_ok else "FAIL"

    # 6. World responsiveness
    world_ok = True
    wr = package.get("world_responsiveness", {}) or {}
    for state in wr.get("state_effects", []) or []:
        sid = str(state.get("state_id", ""))
        if state.get("declared_but_inert"):
            world_ok = False
            _add(result, "DF-INERT-STATE", "world_responsiveness", sid, "visible PLAYER effect", "declared inert", mode_str)
        if state.get("time_threshold_inert"):
            world_ok = False
            _add(result, "DF-INERT-TIME", "world_responsiveness", sid, "time threshold effect", "inert threshold", mode_str)
    if wr.get("revisit_persistent") is False:
        world_ok = False
        _add(result, "DF-NO-PERSISTENT-REVISIT", "world_responsiveness", "", "persistent revisit", "not persistent", mode_str)
    result.checks["DF-WORLD"] = "PASS" if world_ok else "FAIL"

    # 7. Time pressure
    time_ok = True
    tp = package.get("time_pressure", {}) or {}
    if tp.get("deadline_irrelevant"):
        time_ok = False
        _add(result, "DF-IRRELEVANT-DEADLINE", "time_pressure", "", "deadline influences decisions", "irrelevant", mode_str)
    if tp.get("exhaustive_always_fits"):
        time_ok = False
        _add(result, "DF-EXHAUSTIVE-FITS", "time_pressure", "", "scarcity trade-off", "exhaustive always fits", mode_str)
    if tp.get("time_gated_unreachable"):
        time_ok = False
        _add(result, "DF-TIME-GATED-UNREACHABLE", "time_pressure", "", "reachable time gate", "unreachable", mode_str)
    # Delegate playtime if linked
    links = package.get("layer_links", {}) or {}
    if links.get("playtime_calibration"):
        pt_path = root / links["playtime_calibration"]
        if pt_path.exists() and (root / "playtime_calibration_manifest.json").exists():
            from idne.playtime_validate import validate_playtime

            pt_res = validate_playtime(root)
            result.checks["DF-PLAYTIME-DELEGATE"] = "PASS" if pt_res.status in ("PASS", "CONDITIONAL_PASS") else "FAIL"
            if pt_res.status == "FAIL":
                time_ok = False
                _add(result, "DF-PLAYTIME-FAIL", "time_pressure", "", "playtime scarcity valid", str(pt_res.status), mode_str)
        else:
            result.checks["DF-PLAYTIME-DELEGATE"] = "PASS"
    else:
        result.checks["DF-PLAYTIME-DELEGATE"] = "PASS"
    result.checks["DF-TIME"] = "PASS" if time_ok else "FAIL"

    # 8. Failure quality
    fail_ok = True
    fq = package.get("failure_quality", {}) or {}
    for fail in fq.get("failures", []) or []:
        fid = str(fail.get("failure_id", ""))
        if fail.get("meaningless_failure"):
            fail_ok = False
            _add(result, "DF-MEANINGLESS-FAILURE", "failure_quality", fid, "meaningful failure effect", "meaningless", mode_str)
        if fail.get("no_persistent_effect"):
            fail_ok = False
            _add(result, "DF-FAILURE-NO-EFFECT", "failure_quality", fid, "state/knowledge change", "no effect", mode_str)
        if fail.get("unfair_dead_end"):
            fail_ok = False
            _add(result, "DF-UNFAIR-DEAD-END", "failure_quality", fid, "recovery route", "unfair dead end", mode_str)
        if fail.get("changes_fixed_truth"):
            fail_ok = False
            _add(result, "DF-FAIL-CHANGES-TRUTH", "failure_quality", fid, "fixed truth invariant", "truth changed", mode_str)
        if fail.get("leaks_success_content"):
            fail_ok = False
            _add(result, "DF-FAIL-LEAK", "failure_quality", fid, "failure boundary", "leaks success", mode_str)
        if fail.get("free_retry"):
            fail_ok = False
            _add(result, "DF-FREE-RETRY", "failure_quality", fid, "one-attempt policy", "free retry", mode_str)
    result.checks["DF-FAILURE"] = "PASS" if fail_ok else "FAIL"

    # 9. Conversation agency
    conv_ok = True
    ca = package.get("conversation_agency", {}) or {}
    for npc in ca.get("npc_routes", []) or []:
        nid = str(npc.get("npc_id", ""))
        if npc.get("exposition_menu_only"):
            conv_ok = False
            _add(result, "DF-EXPOSITION-MENU", "conversation_agency", nid, "responsive dialogue", "exposition menu", mode_str)
        if npc.get("trust_declared_unused"):
            conv_ok = False
            _add(result, "DF-TRUST-UNUSED", "conversation_agency", nid, "trust affects dialogue", "trust unused", mode_str)
        if npc.get("identical_outcomes"):
            conv_ok = False
            _add(result, "DF-IDENTICAL-OUTCOMES", "conversation_agency", nid, "distinct outcomes", "identical outcomes", mode_str)
        if npc.get("dispenser_only"):
            conv_ok = False
            _add(result, "DF-DISPENSER-NPC", "conversation_agency", nid, "conversation agency", "dispenser only", mode_str)
        if not npc.get("responds_to_relationship", True) and npc.get("mandatory_route"):
            conv_ok = False
            _add(result, "DF-NPC-NOT-RESPONSIVE", "conversation_agency", nid, "responds to player", "not responsive", mode_str)
    result.checks["DF-CONVERSATION"] = "PASS" if conv_ok else "FAIL"

    # 10. Ending causality
    end_ok = True
    ec = package.get("ending_causality", {}) or {}
    for end in ec.get("endings", []) or []:
        eid = str(end.get("ending_id", ""))
        if end.get("final_choice_only"):
            end_ok = False
            _add(result, "DF-FINAL-CHOICE-ONLY", "ending_causality", eid, "investigation trace", "final choice only", mode_str)
        if end.get("unreachable") and not end.get("decorative"):
            end_ok = False
            _add(result, "DF-UNREACHABLE-ENDING", "ending_causality", eid, "reachable", "unreachable", mode_str)
        if end.get("truth_leak"):
            end_ok = False
            _add(result, "DF-ENDING-TRUTH-LEAK", "ending_causality", eid, "imperfect partial truth", "truth leak", mode_str)
        if end.get("auto_perfect_unlock"):
            end_ok = False
            _add(result, "DF-AUTO-PERFECT", "ending_causality", eid, "earned perfect ending", "auto unlock", mode_str)
        if not end.get("causal_trace") and not end.get("decorative"):
            end_ok = False
            _add(result, "DF-NON-CAUSAL-ENDING", "ending_causality", eid, "causal trace", "disconnected", mode_str)
    result.checks["DF-ENDING"] = "PASS" if end_ok else "FAIL"

    # 11. Mode-specific
    mode_ok = True
    ms = package.get("mode_specific", {}) or {}
    if "single_investigator" in play_modes:
        solo = ms.get("single_investigator", {}) or {}
        if solo.get("partner_dependency"):
            mode_ok = False
            _add(result, "DF-PARTNER-DEPENDENCY", "mode_specific", "", "solo without partner", "partner dependency", "single_investigator")
        if solo.get("artificial_split_remnants"):
            mode_ok = False
            _add(result, "DF-SPLIT-REMNANTS", "mode_specific", "", "no split remnants", "split remnants", "single_investigator")
    if "two_player" in play_modes:
        two = ms.get("two_player", {}) or {}
        if two.get("little_joint_investigation"):
            mode_ok = False
            _add(result, "DF-LITTLE-JOINT", "mode_specific", "", "meaningful joint play", "little joint investigation", "two_player")
        if two.get("high_idle_time"):
            mode_ok = False
            _add(result, "DF-HIGH-IDLE", "mode_specific", "", "low idle time", "high idle", "two_player", severity="major")
    result.checks["DF-MODE"] = "PASS" if mode_ok else "FAIL"

    # Tier B mandatory
    for item in package.get("tier_b_mandatory", []) or []:
        tid = str(item.get("review_id", ""))
        if not item.get("resolved"):
            result.tier_b_pending.append(tid)
            _add(
                result, f"DF-TIER-B-{tid}", item.get("category", "player_agency"), tid,
                item.get("expected", "tier B review"), "pending",
                tier="B", owner="tier_b", human=True, severity="major",
            )

    # Tier C playtest
    tier_c = package.get("tier_c_playtest", {}) or {}
    result.tier_c_complete = bool(tier_c.get("completed"))
    if tier_c.get("required") and not tier_c.get("completed"):
        _add(
            result, "DF-TIER-C-MISSING", "mode_specific", "", "human playtest evidence",
            "playtest not completed", mode_str, tier="C", owner="tier_c", human=True, severity="major",
        )

    # Local AI export
    lai = package.get("local_ai_export", {}) or {}
    if lai.get("required") and not lai.get("ready"):
        _add(result, "DF-AI-EXPORT-NOT-READY", "mode_specific", "", "offline export ready", "not ready", mode_str, severity="major")

    # Category scores
    result.category_scores = category_scores(result.findings)

    # Outcome
    proven_critical_a = [
        f for f in result.findings
        if f.tier == "A" and f.confidence == "proven" and f.severity == "critical"
    ]
    if sg_blocked:
        result.status = "BLOCKED"
    elif proven_critical_a:
        result.status = "FAIL"
    elif result.tier_b_pending or not result.tier_c_complete and tier_c.get("required"):
        result.status = "CONDITIONAL_PASS"
    elif any(f.tier in ("B", "C") for f in result.findings):
        result.status = "CONDITIONAL_PASS"
    elif any(f.severity == "major" for f in result.findings):
        result.status = "CONDITIONAL_PASS"
    else:
        result.status = "PASS"

    if write_report_files and package.get("local_ai_export", {}).get("write_reports", True):
        try:
            result.report_paths = write_reports(root, result, package, result.category_scores, player_text)
        except OSError as e:
            result.warnings.append(f"report write failed: {e}")

    return result


def main(argv: list[str] | None = None) -> int:
    import sys

    args = argv or sys.argv[1:]
    if not args:
        print("Usage: python3 -m idne.dm_feeling_validate <adventure_root>")
        return 2
    res = validate_dm_feeling(args[0])
    print(json.dumps(res.to_dict(), indent=2))
    if res.status == "BLOCKED":
        return 2
    return 0 if res.status in ("PASS", "SKIP", "CONDITIONAL_PASS") else 1


if __name__ == "__main__":
    raise SystemExit(main())
