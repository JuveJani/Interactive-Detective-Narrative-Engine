"""Environment System validation (Milestone 3)."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

BARE_NODE_CHOICE_RE = re.compile(
    r"(?:Go to|Choose scene|Choose|Continue to|Open scene|Open)\s+[JPR]-\d{3}[a-z]?\b",
    re.I,
)
ONLY_CODE_LABEL_RE = re.compile(r"^\s*[JPR]-\d{3}[a-z]?\s*$")
SCENE_HEADING_CODE_RE = re.compile(r"^\s*[JPR]-\d{3}[a-z]?\s*[—\-]")
ACCESS_IMPOSSIBLE = "impossible"


@dataclass
class ValidationResult:
    adventure_root: Path
    status: str  # PASS | FAIL | SKIP
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


def load_environment_manifest(root: Path) -> dict[str, Any] | None:
    for name in ("environment_manifest.json", "ENVIRONMENT_MANIFEST.json"):
        path = root / name
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    gen = root / "generation_manifest.json"
    if gen.exists():
        data = json.loads(gen.read_text(encoding="utf-8"))
        env = data.get("environment")
        if isinstance(env, dict) and env.get("enabled"):
            return {
                "schema_version": data.get("schema_version", "1.0"),
                "environment_method": "canonical",
                "package_path": env.get("package_path", "DO_NOT_READ/environment_package.json"),
            }
    return None


def load_environment_package(root: Path, manifest: dict[str, Any]) -> dict[str, Any] | None:
    rel = manifest.get("package_path", "DO_NOT_READ/environment_package.json")
    path = root / rel
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def load_world_truth_for_link(root: Path, package: dict[str, Any]) -> dict[str, Any] | None:
    link = package.get("world_first_links", {})
    rel = link.get("truth_package_path")
    if not rel:
        return None
    path = root / rel
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _scan_player_bare_codes(root: Path, player_paths: list[str] | None) -> list[str]:
    errors: list[str] = []
    paths: list[Path] = []
    if player_paths:
        for rel in player_paths:
            paths.append(root / rel)
    else:
        player_dir = root / "PLAYER"
        if player_dir.is_dir():
            paths.extend(player_dir.rglob("*.md"))
    for path in paths:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for i, line in enumerate(text.splitlines(), 1):
            if BARE_NODE_CHOICE_RE.search(line):
                errors.append(f"bare node code in player choice: {path.name}:{i}: {line.strip()}")
            if "|" in line:
                for cell in line.split("|"):
                    if ONLY_CODE_LABEL_RE.match(cell):
                        errors.append(
                            f"player choice label is only a code: {path.name}:{i}: {cell.strip()}"
                        )
    return errors


def validate_environment(adventure_root: str | Path) -> ValidationResult:
    """Run Environment System validation when manifest declares canonical environment."""
    root = Path(adventure_root).resolve()
    result = ValidationResult(adventure_root=root, status="PASS")

    manifest = load_environment_manifest(root)
    if not manifest:
        result.status = "SKIP"
        result.warnings.append("no environment_manifest — Environment System not declared")
        return result

    if manifest.get("environment_method") != "canonical":
        result.status = "SKIP"
        result.warnings.append(
            f"environment_method={manifest.get('environment_method')} — not applicable"
        )
        return result

    package = load_environment_package(root, manifest)
    if not package:
        result.status = "FAIL"
        result.errors.append("environment_package missing or unreadable")
        result.checks["ENV-PKG-PRESENT"] = "FAIL"
        return result
    result.checks["ENV-PKG-PRESENT"] = "PASS"

    locations = package.get("locations", [])
    loc_ids = {str(l["location_id"]) for l in locations if l.get("location_id")}
    if not loc_ids:
        result.errors.append("locations empty")
        result.checks["ENV-LOC-DECLARED"] = "FAIL"
    else:
        result.checks["ENV-LOC-DECLARED"] = "PASS"

    features = package.get("features", [])
    location_states = package.get("location_states", [])
    navigation = package.get("navigation", [])
    transitions = package.get("state_transitions", [])
    revisit = package.get("revisit_rules", {})

    # --- Features bound to locations ---
    feat_ok = True
    for feat in features:
        fid = feat.get("feature_id")
        lid = feat.get("location_id")
        if not lid or str(lid) not in loc_ids:
            result.errors.append(f"feature {fid} bound to invalid/missing location {lid}")
            feat_ok = False
    result.checks["ENV-FEAT-LOC"] = "PASS" if feat_ok else "FAIL"

    # --- Location states have causes ---
    state_ok = True
    for st in location_states:
        sid = st.get("state_id")
        cause = st.get("cause")
        if not cause or not cause.get("type"):
            result.errors.append(f"location state {sid} missing cause")
            state_ok = False
        if st.get("location_id") and str(st.get("location_id")) not in loc_ids:
            result.errors.append(f"location state {sid} references undeclared location")
            state_ok = False
        trigger_clock = st.get("active_from_clock")
        trigger_event = st.get("trigger_event_id")
        if trigger_clock or trigger_event:
            if not cause or cause.get("type") not in ("world_time", "timeline_event", "player_action"):
                result.errors.append(f"location state {sid} time-dependent without valid cause type")
                state_ok = False
    result.checks["ENV-STATE-CAUSE"] = "PASS" if state_ok else "FAIL"

    # --- Navigation: declared destinations, labels, access ---
    nav_ok = True
    nav_by_id: dict[str, dict[str, Any]] = {}
    dest_refs: set[str] = set()
    for nav in navigation:
        nid = str(nav.get("nav_id", ""))
        nav_by_id[nid] = nav
        src = str(nav.get("source_location_id", ""))
        dst = str(nav.get("destination_location_id", ""))
        dest_refs.add(dst)
        if src not in loc_ids:
            result.errors.append(f"navigation {nid} source {src} not declared")
            nav_ok = False
        if dst not in loc_ids:
            result.errors.append(f"navigation {nid} destination {dst} undeclared")
            nav_ok = False
        label = nav.get("player_label", "")
        if not label or ONLY_CODE_LABEL_RE.match(label) or BARE_NODE_CHOICE_RE.search(label):
            result.errors.append(f"navigation {nid} invalid player_label: {label!r}")
            nav_ok = False
        access = nav.get("access_condition", {})
        if access.get("type") == ACCESS_IMPOSSIBLE and nav.get("mandatory"):
            result.errors.append(f"mandatory navigation {nid} has impossible access")
            nav_ok = False
        if access and access.get("type") not in (None, ACCESS_IMPOSSIBLE):
            if not access.get("type"):
                result.errors.append(f"navigation {nid} access_condition without type")
                nav_ok = False
    result.checks["ENV-NAV-DECLARED"] = "PASS" if nav_ok else "FAIL"

    # --- Return navigation ---
    return_ok = True
    for nav in navigation:
        ret_id = nav.get("return_nav_id")
        if ret_id:
            if str(ret_id) not in nav_by_id:
                result.errors.append(f"navigation {nav.get('nav_id')} broken return_nav_id {ret_id}")
                return_ok = False
        elif nav.get("requires_return_route") and not nav.get("one_way_justification"):
            result.errors.append(
                f"navigation {nav.get('nav_id')} one-way without one_way_justification"
            )
            return_ok = False
    result.checks["ENV-NAV-RETURN"] = "PASS" if return_ok else "FAIL"

    # --- State transitions ---
    trans_ok = True
    for tr in transitions:
        tid = tr.get("transition_id")
        cause = tr.get("cause")
        if not cause or not cause.get("type"):
            result.errors.append(f"state transition {tid} missing cause")
            trans_ok = False
        if str(tr.get("location_id", "")) not in loc_ids:
            result.errors.append(f"transition {tid} undeclared location")
            trans_ok = False
    result.checks["ENV-TRANS-CAUSE"] = "PASS" if trans_ok else "FAIL"

    # --- Revisit: no silent reset ---
    revisit_ok = True
    if revisit.get("persist_physical_changes") and revisit.get("reset_to_initial_on_revisit"):
        result.errors.append("revisit_rules conflict: persist_physical_changes vs reset_to_initial")
        revisit_ok = False
    for tr in transitions:
        if tr.get("resets_on_revisit") and tr.get("persists_on_revisit"):
            result.errors.append(f"transition {tr.get('transition_id')} contradicts revisit persistence")
            revisit_ok = False
        if tr.get("resets_on_revisit") and not tr.get("cause"):
            result.errors.append(f"transition {tr.get('transition_id')} resets on revisit without cause")
            revisit_ok = False
    result.checks["ENV-REVISIT-PERSIST"] = "PASS" if revisit_ok else "FAIL"

    # --- Hidden features not exposed in player_content ---
    hidden_ok = True
    hidden_feats = {
        str(f["feature_id"])
        for f in features
        if f.get("visibility") in ("hidden_until_interaction", "approach_feature")
        and f.get("broad_state") == "hidden"
    }
    player_refs = package.get("player_content_refs", {})
    for ref in player_refs.get("exposed_feature_ids", []) or []:
        if str(ref) in hidden_feats:
            result.errors.append(f"hidden feature {ref} exposed in player_content_refs")
            hidden_ok = False
    result.checks["ENV-VIS-HIDDEN"] = "PASS" if hidden_ok else "FAIL"

    # --- Mandatory evidence access ---
    access_ok = True
    for loc in package.get("mandatory_locations", []) or []:
        lid = str(loc.get("location_id", ""))
        if lid not in loc_ids:
            result.errors.append(f"mandatory location {lid} not declared")
            access_ok = False
        if loc.get("access") == ACCESS_IMPOSSIBLE:
            result.errors.append(f"mandatory evidence at {lid} behind impossible access")
            access_ok = False
    result.checks["ENV-MANDATORY-ACCESS"] = "PASS" if access_ok else "FAIL"

    # --- Reachability from start ---
    start = package.get("start_location_id")
    reach_ok = True
    if start and str(start) not in loc_ids:
        result.errors.append(f"start_location_id {start} not declared")
        reach_ok = False
    else:
        graph: dict[str, set[str]] = {lid: set() for lid in loc_ids}
        for nav in navigation:
            if nav.get("access_condition", {}).get("type") != ACCESS_IMPOSSIBLE:
                s = str(nav.get("source_location_id", ""))
                d = str(nav.get("destination_location_id", ""))
                if s in graph:
                    graph[s].add(d)
        mandatory_ids = {
            str(m.get("location_id"))
            for m in package.get("mandatory_locations", []) or []
        }
        if start and mandatory_ids:
            reachable: set[str] = set()
            stack = [str(start)]
            while stack:
                cur = stack.pop()
                if cur in reachable:
                    continue
                reachable.add(cur)
                for nxt in graph.get(cur, set()):
                    stack.append(nxt)
            for mid in mandatory_ids:
                if mid and mid not in reachable:
                    result.errors.append(f"mandatory location {mid} unreachable from {start}")
                    reach_ok = False
    result.checks["ENV-MANDATORY-REACH"] = "PASS" if reach_ok else "FAIL"

    # --- World-First linkage ---
    wf_ok = True
    truth = load_world_truth_for_link(root, package)
    if truth:
        wf_events = truth.get("causal_timeline", {}).get("events", [])
        wf_locations = set()
        for ev in wf_events:
            if ev.get("location_id"):
                wf_locations.add(str(ev["location_id"]))
        for loc in locations:
            lid = str(loc.get("location_id", ""))
            prov = loc.get("world_first_provenance", {})
            has_prov = (
                prov.get("event_ids")
                or prov.get("fact_ids")
                or prov.get("explicit_adventure_extension")
                or lid in wf_locations
            )
            if not has_prov:
                result.errors.append(f"location {lid} missing world_first_provenance")
                wf_ok = False
        # Contradiction: environment asserts location state incompatible with snapshot
        for loc in package.get("world_first_contradictions", []) or []:
            result.errors.append(f"test contradiction marker: {loc}")
            wf_ok = False
        if package.get("contradicts_world_truth"):
            result.errors.append("environment_package.contradicts_world_truth is true")
            wf_ok = False
        for ev in wf_events:
            eid = str(ev.get("event_id", ""))
            eloc = str(ev.get("location_id", ""))
            for snap in truth.get("world_state_timeline", {}).get("snapshots", []):
                if str(snap.get("at_event_id")) == eid:
                    for npc, sloc in (snap.get("people_locations") or {}).items():
                        env_loc = package.get("location_truth_assertions", {}).get(eloc)
                        if env_loc and env_loc.get("forbidden_occupants"):
                            if str(npc) in env_loc["forbidden_occupants"]:
                                result.errors.append(
                                    f"environment contradicts WF: {npc} at {eloc} at {eid}"
                                )
                                wf_ok = False
    result.checks["ENV-WF-LINK"] = "PASS" if wf_ok else "FAIL"

    # --- Bare page codes in PLAYER ---
    player_paths = package.get("player_content_refs", {}).get("files")
    bare_errors = _scan_player_bare_codes(root, player_paths)
    if bare_errors:
        result.errors.extend(bare_errors)
    result.checks["ENV-BARE-CODE"] = "PASS" if not bare_errors else "FAIL"

    if result.errors:
        result.status = "FAIL"
    return result


def main(argv: list[str] | None = None) -> int:
    import sys

    args = argv or sys.argv[1:]
    if not args:
        print("Usage: python3 -m idne.environment_validate <adventure_root>")
        return 2
    res = validate_environment(args[0])
    print(json.dumps(res.to_dict(), indent=2))
    return 0 if res.status in ("PASS", "SKIP") else 1


if __name__ == "__main__":
    raise SystemExit(main())
