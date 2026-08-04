"""Capability Check System validation (Milestone 6)."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

BARE_NODE_RE = re.compile(
    r"(?:Go to|Choose|Continue to|Open)\s+[JPR]-\d{3}[a-z]?\b|Choose\s+OBJ-\w+",
    re.I,
)
ONLY_CODE_RE = re.compile(r"^\s*(?:[JPR]-\d{3}[a-z]?|OBJ-[A-Z0-9-]+)\s*$")
PASS_FAIL_SAME_RE = re.compile(
    r"(success|succeeded|you find|found the|reveals?).*(fail|failed|missed|nothing|no useful)",
    re.I | re.S,
)
HIDDEN_LEAK_RE = re.compile(
    r"(hidden|missed|failed to notice|did not see|key under|concealed)",
    re.I,
)

CAPABILITY_CATEGORIES = frozenset(
    {
        "perception_observation",
        "reasoning_interpretation",
        "technical_operation",
        "physical_strength",
        "agility",
        "social_persuasion",
        "social_intimidation",
        "social_deception",
    }
)
ACTION_CAPABILITY_MAP = {
    "perceive": "perception_observation",
    "search": "perception_observation",
    "observe": "perception_observation",
    "interpret": "reasoning_interpretation",
    "analyze": "reasoning_interpretation",
    "operate": "technical_operation",
    "login": "technical_operation",
    "technical": "technical_operation",
    "lift": "physical_strength",
    "force": "physical_strength",
    "climb": "agility",
    "sneak": "agility",
    "persuade": "social_persuasion",
    "intimidate": "social_intimidation",
    "deceive": "social_deception",
    "bluff": "social_deception",
}
SOCIAL_CATEGORIES = frozenset(
    {"social_persuasion", "social_intimidation", "social_deception"}
)
ATTEMPT_STATES = frozenset({"NOT_ATTEMPTED", "SUCCEEDED", "FAILED"})


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


def load_manifest(root: Path) -> dict[str, Any] | None:
    for name in ("capability_check_manifest.json", "CAPABILITY_CHECK_MANIFEST.json"):
        path = root / name
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    gen = root / "generation_manifest.json"
    if gen.exists():
        data = json.loads(gen.read_text(encoding="utf-8"))
        cc = data.get("capability_check")
        if isinstance(cc, dict) and cc.get("enabled"):
            return {
                "schema_version": data.get("schema_version", "1.0"),
                "capability_check_method": "canonical",
                "package_path": cc.get(
                    "package_path", "DO_NOT_READ/capability_check_package.json"
                ),
            }
    return None


def load_package(root: Path, manifest: dict[str, Any]) -> dict[str, Any] | None:
    rel = manifest.get("package_path", "DO_NOT_READ/capability_check_package.json")
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


def _scan_player_content(root: Path, package: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    refs = package.get("player_content_refs", {})
    for rel in refs.get("files", []) or []:
        path = root / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for i, line in enumerate(text.splitlines(), 1):
            if BARE_NODE_RE.search(line) or ONLY_CODE_RE.match(line):
                errors.append(f"bare code choice: {path.name}:{i}")
            if PASS_FAIL_SAME_RE.search(line):
                errors.append(f"pass/fail same unit: {path.name}:{i}")
    for unit in refs.get("action_units", []) or []:
        uid = unit.get("unit_id")
        if unit.get("exposes_success_content") and unit.get("exposes_failure_content"):
            errors.append(f"action unit {uid} exposes both outcomes")
        body = unit.get("body", "")
        if body and PASS_FAIL_SAME_RE.search(body):
            errors.append(f"action unit {uid} pass/fail prose together")
    return errors


def validate_capability_check(adventure_root: str | Path) -> ValidationResult:
    root = Path(adventure_root).resolve()
    result = ValidationResult(adventure_root=root, status="PASS")

    manifest = load_manifest(root)
    if not manifest:
        result.status = "SKIP"
        result.warnings.append("no capability_check_manifest — not declared")
        return result

    if manifest.get("capability_check_method") != "canonical":
        result.status = "SKIP"
        result.warnings.append("capability_check_method not canonical")
        return result

    package = load_package(root, manifest)
    if not package:
        result.status = "FAIL"
        result.errors.append("capability_check_package missing")
        result.checks["CAP-PKG-PRESENT"] = "FAIL"
        return result
    result.checks["CAP-PKG-PRESENT"] = "PASS"

    checks = package.get("checks", []) or []
    modifiers = package.get("modifier_sources", []) or []
    play_modes = package.get("play_modes", ["single_investigator", "two_player"])
    modifier_ids = {str(m["modifier_id"]) for m in modifiers if m.get("modifier_id")}
    check_ids_seen: dict[str, int] = {}

    inv_core = load_linked(
        root, package.get("investigation_core_links", {}).get("package_path")
    )
    obj_pkg = load_linked(
        root, package.get("object_interaction_links", {}).get("package_path")
    )
    npc_pkg = load_linked(
        root, package.get("npc_investigation_links", {}).get("package_path")
    )
    env_pkg = load_linked(
        root, package.get("environment_links", {}).get("package_path")
    )

    know_ids: set[str] = set()
    conclusion_ids: set[str] = set()
    if inv_core:
        know_ids = {str(k["knowledge_id"]) for k in inv_core.get("knowledge", []) if k.get("knowledge_id")}
        conclusion_ids = {str(c["conclusion_id"]) for c in inv_core.get("conclusions", []) if c.get("conclusion_id")}

    obj_states: dict[str, str] = {}
    if obj_pkg:
        for o in obj_pkg.get("objects", []) or []:
            if o.get("object_id"):
                obj_states[str(o["object_id"])] = str(o.get("current_state", o.get("initial_state", "")))

    npc_ids: set[str] = set()
    if npc_pkg:
        npc_ids = {str(n["npc_id"]) for n in npc_pkg.get("npcs", []) if n.get("npc_id")}

    dest_units = {str(u["unit_id"]) for u in package.get("destination_units", []) if u.get("unit_id")}
    fail_units_by_id = {
        str(u["unit_id"]): u for u in package.get("destination_units", []) if u.get("unit_id")
    }

    truth_ok = True
    doc_ok = True
    evidence_ok = True
    cap_mismatch_ok = True
    meaningless_ok = True
    fail_leak_ok = True
    repeat_ok = True
    free_retry_ok = True
    unrelated_ok = True
    only_route_ok = True
    dest_ok = True
    same_dest_ok = True
    dup_cost_ok = True
    npc_unknown_ok = True
    intimidation_ok = True
    provenance_ok = True
    dc_just_ok = True
    guaranteed_ok = True
    modifier_ok = True
    solo_p2_ok = True
    state_ok = True

    for chk in checks:
        cid = str(chk.get("check_id", ""))
        check_ids_seen[cid] = check_ids_seen.get(cid, 0) + 1

        invariants = chk.get("fixed_truth_invariants", {}) or {}
        if invariants.get("changes_evidence_existence"):
            result.errors.append(f"check {cid} changes evidence existence")
            evidence_ok = False
        if invariants.get("changes_document_contents"):
            result.errors.append(f"check {cid} changes document contents")
            doc_ok = False
        if invariants.get("changes_fixed_truth"):
            result.errors.append(f"check {cid} changes fixed truth")
            truth_ok = False

        action_type = str(chk.get("parent_action_type", "")).lower()
        cap_cat = chk.get("capability_category", "")
        if action_type and cap_cat and ACTION_CAPABILITY_MAP.get(action_type):
            expected = ACTION_CAPABILITY_MAP[action_type]
            if cap_cat != expected and not chk.get("capability_mismatch_justified"):
                result.errors.append(f"check {cid} capability {cap_cat} mismatches action {action_type}")
                cap_mismatch_ok = False

        if chk.get("meaningless_check") or chk.get("guaranteed_action") and chk.get("requires_roll"):
            result.errors.append(f"check {cid} meaningless or guaranteed incorrectly gated")
            meaningless_ok = False
        if chk.get("guaranteed_action") and not chk.get("no_check_required"):
            result.errors.append(f"check {cid} gates ordinary guaranteed action")
            guaranteed_ok = False

        dest = chk.get("destinations", {}) or {}
        succ = str(dest.get("success_destination", ""))
        fail = str(dest.get("failure_destination", ""))
        if not succ:
            result.errors.append(f"check {cid} missing success destination")
            dest_ok = False
        if not fail:
            result.errors.append(f"check {cid} missing failure destination")
            dest_ok = False
        if succ and dest_units and succ not in dest_units:
            result.errors.append(f"check {cid} success destination {succ} not declared")
            dest_ok = False
        if fail and dest_units and fail not in dest_units:
            result.errors.append(f"check {cid} failure destination {fail} not declared")
            dest_ok = False
        if succ == fail and not chk.get("same_destination_justification"):
            result.errors.append(f"check {cid} same success/failure destination")
            same_dest_ok = False

        policy = chk.get("attempt_policy", {}) or {}
        if policy.get("default") != "one_attempt" and not policy.get("retry_extension_point"):
            result.warnings.append(f"check {cid} non-default attempt policy without extension point")
        if check_ids_seen[cid] > 1 and not chk.get("repeat_policy_override"):
            result.errors.append(f"check {cid} repeated beyond one-attempt default")
            repeat_ok = False

        eligibility = chk.get("eligibility", {}) or {}
        if "single_investigator" in play_modes and eligibility.get("requires_player_2"):
            result.errors.append(f"check {cid} requires Player 2 in solo mode")
            solo_p2_ok = False
        coop = eligibility.get("cooperative_policy", {}) or {}
        if coop.get("free_second_player_retry") and not coop.get("explicit_joint_attempt_allowed"):
            result.errors.append(f"check {cid} free second-player retry without cooperative policy")
            free_retry_ok = False

        mod_src = chk.get("modifier_source_id", "")
        if mod_src and modifier_ids and str(mod_src) not in modifier_ids:
            result.errors.append(f"check {cid} modifier source {mod_src} unavailable")
            modifier_ok = False
        if cap_cat and cap_cat not in CAPABILITY_CATEGORIES:
            result.errors.append(f"check {cid} invalid capability category {cap_cat}")
            modifier_ok = False

        if not chk.get("dc_justification"):
            result.errors.append(f"check {cid} missing dc_justification")
            dc_just_ok = False

        succ_eff = chk.get("success_effects", {}) or {}
        fail_eff = chk.get("failure_effects", {}) or {}
        succ_info = set(str(x) for x in succ_eff.get("reveals_information_ids", []) or [])
        fail_info = set(str(x) for x in fail_eff.get("reveals_information_ids", []) or [])
        if fail_info & succ_info:
            result.errors.append(f"check {cid} failure reveals success information")
            fail_leak_ok = False

        fail_unit = fail_units_by_id.get(fail, {})
        if fail_unit.get("hints_missed_content") or fail_unit.get("reveals_hidden_object"):
            result.errors.append(f"check {cid} failure unit leaks hidden content")
            fail_leak_ok = False
        fail_text = fail_unit.get("player_text", "") or fail_unit.get("body", "")
        if fail_text and HIDDEN_LEAK_RE.search(fail_text):
            result.errors.append(f"check {cid} failure text leaks missed content")
            fail_leak_ok = False

        grants = succ_eff.get("grants_conclusion_ids", []) or []
        if grants and conclusion_ids and set(str(g) for g in grants) == conclusion_ids:
            result.errors.append(f"check {cid} success grants full conclusion set")
            unrelated_ok = False
        if succ_eff.get("grants_complete_solution"):
            result.errors.append(f"check {cid} success grants complete solution")
            unrelated_ok = False

        if not chk.get("alternate_route_exists") and chk.get("mandatory_for_fair_path"):
            result.errors.append(f"check {cid} failure removes only fair route")
            only_route_ok = False

        trace = chk.get("information_trace", {}) or {}
        reveals = succ_eff.get("grants_knowledge_ids", []) or []
        for kid in reveals:
            if not trace.get("fixed_truth_ref") and not trace.get("source_id"):
                result.errors.append(f"check {cid} knowledge {kid} without provenance trace")
                provenance_ok = False
            if inv_core and str(kid) not in know_ids:
                result.errors.append(f"check {cid} grants unknown knowledge {kid}")
                provenance_ok = False

        social = succ_eff.get("npc_social_effects", []) or []
        for eff in social:
            npc_id = str(eff.get("npc_id", ""))
            if eff.get("reveals_information_npc_did_not_know"):
                result.errors.append(f"check {cid} NPC {npc_id} reveals unknown information")
                npc_unknown_ok = False
            if npc_id and npc_pkg and npc_id not in npc_ids:
                result.errors.append(f"check {cid} NPC {npc_id} not declared")
                npc_unknown_ok = False
            if cap_cat == "social_intimidation" and eff.get("trust_delta", 0) > 0 and not eff.get("intimidation_not_trust_justified"):
                result.errors.append(f"check {cid} intimidation treated as trust increase")
                intimidation_ok = False

        cost = chk.get("time_cost_minutes", 0) or 0
        fail_cost = chk.get("failure_time_cost_minutes", 0) or 0
        if chk.get("cost_applied_count", 1) > 1:
            result.errors.append(f"check {cid} duplicated action cost")
            dup_cost_ok = False
        if fail_cost and chk.get("failure_cost_applied_count", 1) > 1:
            result.errors.append(f"check {cid} duplicated failure cost")
            dup_cost_ok = False

        state_req = chk.get("requires_object_state", {}) or {}
        for oid, required in state_req.items():
            actual = obj_states.get(str(oid))
            if actual and str(required) != actual and chk.get("state_contradiction"):
                result.errors.append(f"check {cid} contradicts object state {oid}")
                state_ok = False

        if not chk.get("why_check_exists"):
            result.warnings.append(f"check {cid} missing why_check_exists")

    result.checks["CAP-FIXED-TRUTH"] = "PASS" if truth_ok else "FAIL"
    result.checks["CAP-DOC-CONTENTS"] = "PASS" if doc_ok else "FAIL"
    result.checks["CAP-EVIDENCE-EXIST"] = "PASS" if evidence_ok else "FAIL"
    result.checks["CAP-CAP-MISMATCH"] = "PASS" if cap_mismatch_ok else "FAIL"
    result.checks["CAP-MEANINGLESS"] = "PASS" if meaningless_ok else "FAIL"
    result.checks["CAP-FAIL-LEAK"] = "PASS" if fail_leak_ok else "FAIL"
    result.checks["CAP-REPEAT"] = "PASS" if repeat_ok else "FAIL"
    result.checks["CAP-FREE-RETRY"] = "PASS" if free_retry_ok else "FAIL"
    result.checks["CAP-UNRELATED-CONCLUSION"] = "PASS" if unrelated_ok else "FAIL"
    result.checks["CAP-ONLY-ROUTE"] = "PASS" if only_route_ok else "FAIL"
    result.checks["CAP-DESTINATIONS"] = "PASS" if dest_ok else "FAIL"
    result.checks["CAP-SAME-DEST"] = "PASS" if same_dest_ok else "FAIL"
    result.checks["CAP-DUP-COST"] = "PASS" if dup_cost_ok else "FAIL"
    result.checks["CAP-NPC-UNKNOWN"] = "PASS" if npc_unknown_ok else "FAIL"
    result.checks["CAP-INTIMIDATION-TRUST"] = "PASS" if intimidation_ok else "FAIL"
    result.checks["CAP-PROVENANCE"] = "PASS" if provenance_ok else "FAIL"
    result.checks["CAP-DC-JUST"] = "PASS" if dc_just_ok else "FAIL"
    result.checks["CAP-GUARANTEED"] = "PASS" if guaranteed_ok else "FAIL"
    result.checks["CAP-MODIFIER"] = "PASS" if modifier_ok else "FAIL"
    result.checks["CAP-SOLO-P2"] = "PASS" if solo_p2_ok else "FAIL"
    result.checks["CAP-STATE-CONFLICT"] = "PASS" if state_ok else "FAIL"

    player_errors = _scan_player_content(root, package)
    bare_fail = any("bare code" in e for e in player_errors)
    unit_fail = any("pass/fail" in e for e in player_errors)
    if player_errors:
        result.errors.extend(player_errors)
    result.checks["CAP-BARE-CODE"] = "PASS" if not bare_fail else "FAIL"
    result.checks["CAP-PASS-FAIL-UNIT"] = "PASS" if not unit_fail else "FAIL"

    if result.errors:
        result.status = "FAIL"
    return result


def main(argv: list[str] | None = None) -> int:
    import sys

    args = argv or sys.argv[1:]
    if not args:
        print("Usage: python3 -m idne.capability_check_validate <adventure_root>")
        return 2
    res = validate_capability_check(args[0])
    print(json.dumps(res.to_dict(), indent=2))
    return 0 if res.status in ("PASS", "SKIP") else 1


if __name__ == "__main__":
    raise SystemExit(main())
