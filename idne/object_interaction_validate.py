"""Object Interaction System validation (Milestone 4)."""

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
BARE_OR_CHOICE_RE = re.compile(
    r"[JPR]-\d{3}[a-z]?\s+or\s+[JPR]-\d{3}[a-z]?",
    re.I,
)
ONLY_OBJ_CODE_RE = re.compile(r"^\s*OBJ-[A-Z0-9-]+\s*$")
PASS_FAIL_SAME_UNIT_RE = re.compile(
    r"(success|succeeded|found the|you find|reveals?).*(fail|failed|missed|nothing)",
    re.I | re.S,
)


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


def load_object_manifest(root: Path) -> dict[str, Any] | None:
    for name in ("object_interaction_manifest.json", "OBJECT_INTERACTION_MANIFEST.json"):
        path = root / name
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    gen = root / "generation_manifest.json"
    if gen.exists():
        data = json.loads(gen.read_text(encoding="utf-8"))
        oi = data.get("object_interaction")
        if isinstance(oi, dict) and oi.get("enabled"):
            return {
                "schema_version": data.get("schema_version", "1.0"),
                "object_interaction_method": "canonical",
                "package_path": oi.get(
                    "package_path", "DO_NOT_READ/object_interaction_package.json"
                ),
            }
    return None


def load_package(root: Path, manifest: dict[str, Any]) -> dict[str, Any] | None:
    rel = manifest.get("package_path", "DO_NOT_READ/object_interaction_package.json")
    path = root / rel
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def load_world_truth(root: Path, package: dict[str, Any]) -> dict[str, Any] | None:
    rel = package.get("world_first_links", {}).get("truth_package_path")
    if not rel:
        return None
    path = root / rel
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _scan_player_content(root: Path, package: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    refs = package.get("player_content_refs", {})
    paths = [root / p for p in refs.get("files", []) or []]
    for path in paths:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for i, line in enumerate(text.splitlines(), 1):
            if BARE_NODE_RE.search(line) or BARE_OR_CHOICE_RE.search(line):
                errors.append(f"bare ID choice: {path.name}:{i}: {line.strip()}")
            if ONLY_OBJ_CODE_RE.match(line):
                errors.append(f"OBJ code choice: {path.name}:{i}")
            if PASS_FAIL_SAME_UNIT_RE.search(line):
                errors.append(f"pass/fail in same unit: {path.name}:{i}")
    for unit in refs.get("action_units", []) or []:
        if unit.get("exposes_success_content") and unit.get("exposes_failure_content"):
            errors.append(f"action unit {unit.get('unit_id')} exposes both outcomes")
        body = unit.get("body", "")
        if body and PASS_FAIL_SAME_UNIT_RE.search(body):
            errors.append(f"action unit {unit.get('unit_id')} pass/fail prose together")
    return errors


def validate_object_interaction(adventure_root: str | Path) -> ValidationResult:
    root = Path(adventure_root).resolve()
    result = ValidationResult(adventure_root=root, status="PASS")

    manifest = load_object_manifest(root)
    if not manifest:
        result.status = "SKIP"
        result.warnings.append("no object_interaction_manifest — not declared")
        return result

    if manifest.get("object_interaction_method") != "canonical":
        result.status = "SKIP"
        result.warnings.append("object_interaction_method not canonical")
        return result

    package = load_package(root, manifest)
    if not package:
        result.status = "FAIL"
        result.errors.append("object_interaction_package missing")
        result.checks["OBJ-PKG-PRESENT"] = "FAIL"
        return result
    result.checks["OBJ-PKG-PRESENT"] = "PASS"

    objects = package.get("objects", [])
    actions = package.get("actions", [])
    result_units = package.get("result_units", [])
    transitions = package.get("state_transitions", [])
    items = {str(i["item_id"]) for i in package.get("items_registry", []) if i.get("item_id")}
    obj_by_id = {str(o["object_id"]): o for o in objects if o.get("object_id")}
    unit_by_id = {str(u["unit_id"]): u for u in result_units if u.get("unit_id")}
    loc_ids = set()
    env_link = package.get("environment_links", {}).get("package_path")
    if env_link and (root / env_link).exists():
        env = json.loads((root / env_link).read_text(encoding="utf-8"))
        loc_ids = {str(l["location_id"]) for l in env.get("locations", []) if l.get("location_id")}

    # --- Object declared / parent valid ---
    obj_ok = True
    for obj in objects:
        oid = str(obj.get("object_id", ""))
        parent = obj.get("parent_id")
        ptype = obj.get("parent_type", "location")
        if ptype == "location" and str(parent) not in loc_ids and not obj.get("allow_no_env_link"):
            result.errors.append(f"object {oid} parent location {parent} not in environment")
            obj_ok = False
        if ptype == "object" and str(parent) not in obj_by_id:
            result.errors.append(f"object {oid} parent object {parent} not declared")
            obj_ok = False
    for ref in package.get("object_refs", []) or []:
        if str(ref) not in obj_by_id:
            result.errors.append(f"referenced object {ref} not declared")
            obj_ok = False
    result.checks["OBJ-DECLARED"] = "PASS" if obj_ok else "FAIL"

    # --- Cyclic containment ---
    cycle_ok = True
    def _ancestors(oid: str, seen: set[str]) -> bool:
        if oid in seen:
            return False
        seen.add(oid)
        o = obj_by_id.get(oid)
        if not o or o.get("parent_type") != "object":
            return True
        pid = str(o.get("parent_id", ""))
        if pid in obj_by_id:
            return _ancestors(pid, seen)
        return True

    for oid in obj_by_id:
        if not _ancestors(oid, set()):
            result.errors.append(f"cyclic containment involving {oid}")
            cycle_ok = False
    result.checks["OBJ-NO-CYCLE"] = "PASS" if cycle_ok else "FAIL"

    # --- Child visible before parent ---
    child_vis_ok = True
    for obj in objects:
        if obj.get("parent_type") == "object":
            parent = obj_by_id.get(str(obj.get("parent_id", "")))
            vis = obj.get("visibility_requirement", "")
            if parent and vis in ("on_arrival", "known_remotely", "visible"):
                if parent.get("interaction_depth_required") and obj.get("visible_before_parent_access"):
                    result.errors.append(f"object {obj.get('object_id')} visible before parent accessed")
                    child_vis_ok = False
            if obj.get("visible_before_parent_access"):
                result.errors.append(f"object {obj.get('object_id')} marked visible before parent access")
                child_vis_ok = False
    result.checks["OBJ-CHILD-VIS"] = "PASS" if child_vis_ok else "FAIL"

    # --- Hidden info in parent description ---
    hidden_ok = True
    for obj in objects:
        if obj.get("parent_description_reveals_hidden_children"):
            result.errors.append(f"object {obj.get('object_id')} parent description reveals hidden children")
            hidden_ok = False
    result.checks["OBJ-HIDDEN-PARENT"] = "PASS" if hidden_ok else "FAIL"

    # --- Actions destinations and checks ---
    act_ok = True
    check_attempts: dict[str, int] = {}
    for act in actions:
        aid = act.get("action_id")
        if not act.get("destination_unit") and not act.get("check_binding"):
            result.errors.append(f"action {aid} no destination")
            act_ok = False
        cb = act.get("check_binding")
        if cb:
            chk = str(cb.get("check_id", ""))
            if cb.get("changes_world_truth"):
                result.errors.append(f"check {chk} changes world truth")
                act_ok = False
            if cb.get("determines_document_contents"):
                result.errors.append(f"check {chk} determines document contents")
                act_ok = False
            if cb.get("creates_evidence"):
                result.errors.append(f"check {chk} creates evidence")
                act_ok = False
            succ = str(cb.get("success_destination", ""))
            fail = str(cb.get("failure_destination", ""))
            if succ and succ not in unit_by_id:
                result.errors.append(f"action {aid} success destination {succ} missing")
                act_ok = False
            if fail and fail not in unit_by_id:
                result.errors.append(f"action {aid} failure destination {fail} missing")
                act_ok = False
            if succ == fail and not cb.get("same_destination_justification"):
                result.errors.append(f"action {aid} pass/fail same destination without justification")
                act_ok = False
            if cb.get("one_attempt"):
                check_attempts[chk] = check_attempts.get(chk, 0) + 1
                if check_attempts[chk] > 1 and not act.get("repeat_policy_override"):
                    result.errors.append(f"check {chk} repeated beyond one-attempt default")
                    act_ok = False
            fail_unit = unit_by_id.get(fail, {})
            succ_unit = unit_by_id.get(succ, {})
            succ_info = set(str(x) for x in (cb.get("information_on_success", []) or []))
            fail_info = set(str(x) for x in (fail_unit.get("reveals_information", []) or []))
            if fail_info & succ_info:
                result.errors.append(f"failure unit {fail} reveals same information as success")
                act_ok = False
            if fail_unit.get("hints_missed_content") or fail_unit.get("reveals_information"):
                if cb.get("information_on_failure"):
                    result.errors.append(f"failure unit {fail} reveals missed information")
                    act_ok = False
            if act.get("cost_applied_count", 1) > 1 and act.get("cost_applied_once"):
                result.errors.append(f"action {aid} cost applied more than once")
                act_ok = False
        label = act.get("player_label", "")
        if not label or BARE_NODE_RE.search(label) or ONLY_OBJ_CODE_RE.match(label):
            result.errors.append(f"action {aid} invalid player_label")
            act_ok = False
        inv = act.get("inventory_requirement", {})
        if inv.get("item_id") and str(inv["item_id"]) not in items:
            result.errors.append(f"action {aid} inventory ref {inv.get('item_id')} not in registry")
            act_ok = False
        if inv.get("impossible"):
            result.errors.append(f"action {aid} impossible inventory requirement")
            act_ok = False
    result.checks["OBJ-ACTION"] = "PASS" if act_ok else "FAIL"

    # --- Return routes ---
    ret_ok = True
    for act in actions:
        if not act.get("return_destination") and act.get("requires_return"):
            result.errors.append(f"action {act.get('action_id')} missing return")
            ret_ok = False
    for unit in result_units:
        if unit.get("requires_return") and not unit.get("return_destination"):
            result.errors.append(f"unit {unit.get('unit_id')} missing return")
            ret_ok = False
    result.checks["OBJ-RETURN"] = "PASS" if ret_ok else "FAIL"

    # --- State transitions ---
    trans_ok = True
    for tr in transitions:
        if not tr.get("cause"):
            result.errors.append(f"transition {tr.get('transition_id')} no cause")
            trans_ok = False
        if tr.get("resets_on_revisit") and tr.get("persists_on_revisit"):
            result.errors.append(f"transition {tr.get('transition_id')} revisit conflict")
            trans_ok = False
    revisit = package.get("revisit_rules", {})
    if revisit.get("persist_object_states") and revisit.get("reset_states_on_revisit"):
        result.errors.append("revisit_rules object state reset conflict")
        trans_ok = False
    result.checks["OBJ-STATE"] = "PASS" if trans_ok else "FAIL"

    # --- Collected items still present ---
    coll_ok = True
    for rec in package.get("collected_item_conflicts", []) or []:
        result.errors.append(f"collected item {rec} still present at source")
        coll_ok = False
    if package.get("collected_item_still_present"):
        result.errors.append("collected object still present in location")
        coll_ok = False
    result.checks["OBJ-COLLECTED"] = "PASS" if coll_ok else "FAIL"

    # --- Mandatory information accessible ---
    mand_ok = True
    grant_units = set()
    for unit in result_units:
        for info in unit.get("reveals_information", []) or []:
            grant_units.add(str(info))
    for act in actions:
        cb = act.get("check_binding") or {}
        for info in cb.get("information_on_success", []) or []:
            grant_units.add(str(info))
    for mand in package.get("mandatory_information", []) or []:
        iid = str(mand.get("info_id", ""))
        if mand.get("required_for_conclusion") and iid not in grant_units:
            if not mand.get("accessible_via_interaction"):
                result.errors.append(f"mandatory info {iid} not accessible via interaction")
                mand_ok = False
    result.checks["OBJ-MANDATORY"] = "PASS" if mand_ok else "FAIL"

    # --- World-First ---
    wf_ok = True
    if package.get("contradicts_world_truth"):
        result.errors.append("package contradicts world_truth")
        wf_ok = False
    truth = load_world_truth(root, package)
    if truth and package.get("objects"):
        wf_facts = {
            str(f.get("fact_id"))
            for f in truth.get("fixed_truth", {}).get("immutable_facts", [])
        }
        for obj in objects:
            if obj.get("contradicts_fact_id") and str(obj["contradicts_fact_id"]) in wf_facts:
                result.errors.append(f"object {obj.get('object_id')} contradicts WF fact")
                wf_ok = False
    result.checks["OBJ-WF"] = "PASS" if wf_ok else "FAIL"

    # --- Player content scan ---
    player_errors = _scan_player_content(root, package)
    if player_errors:
        result.errors.extend(player_errors)
    result.checks["OBJ-BARE-CODE"] = "PASS" if not any("bare" in e or "OBJ code" in e for e in player_errors) else "FAIL"
    result.checks["OBJ-PASS-FAIL-UNIT"] = "PASS" if not any("pass/fail" in e for e in player_errors) else "FAIL"

    if result.errors:
        result.status = "FAIL"
    return result


def main(argv: list[str] | None = None) -> int:
    import sys

    args = argv or sys.argv[1:]
    if not args:
        print("Usage: python3 -m idne.object_interaction_validate <adventure_root>")
        return 2
    res = validate_object_interaction(args[0])
    print(json.dumps(res.to_dict(), indent=2))
    return 0 if res.status in ("PASS", "SKIP") else 1


if __name__ == "__main__":
    raise SystemExit(main())
