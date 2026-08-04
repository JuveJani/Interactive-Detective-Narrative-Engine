"""World-First Generation validation (Milestone 2)."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

AMBIGUOUS_TIME_RE = re.compile(
    r"\b(later|earlier|sometime|eventually|soon|evening|morning|afternoon|night)\b",
    re.I,
)
ISO_TS_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(:\d{2})?$"
)


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


def load_generation_manifest(root: Path) -> dict[str, Any] | None:
    for name in ("generation_manifest.json", "GENERATION_MANIFEST.json"):
        path = root / name
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    return None


def load_world_truth_package(root: Path, manifest: dict[str, Any]) -> dict[str, Any] | None:
    rel = manifest.get("package_path", "DO_NOT_READ/world_truth_package.json")
    path = root / rel
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _parse_timestamp(ts: str) -> datetime | None:
    if not ts or AMBIGUOUS_TIME_RE.search(ts):
        return None
    for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M"):
        try:
            return datetime.strptime(ts, fmt)
        except ValueError:
            continue
    return None


def _event_facts(event: dict[str, Any]) -> set[str]:
    facts: set[str] = set()
    for key in ("reveals_facts", "effects"):
        val = event.get(key, [])
        if isinstance(val, list):
            facts.update(str(x) for x in val)
    return facts


def validate_world_first(adventure_root: str | Path) -> ValidationResult:
    """Run World-First validation when generation_manifest declares world_first."""
    root = Path(adventure_root).resolve()
    result = ValidationResult(adventure_root=root, status="PASS")

    manifest = load_generation_manifest(root)
    if not manifest:
        result.status = "SKIP"
        result.warnings.append("no generation_manifest.json — world-first not declared")
        return result

    if manifest.get("generation_method") != "world_first":
        result.status = "SKIP"
        result.warnings.append(
            f"generation_method={manifest.get('generation_method')} — world-first not declared"
        )
        return result

    package = load_world_truth_package(root, manifest)
    if not package:
        result.status = "FAIL"
        result.errors.append("world_truth_package.json missing or unreadable")
        result.checks["WF-PKG-PRESENT"] = "FAIL"
        return result
    result.checks["WF-PKG-PRESENT"] = "PASS"

    # --- G-WF1 Fixed Truth ---
    fixed = package.get("fixed_truth", {})
    wf1_fields = ("culprit_id", "motive", "method", "opportunity")
    wf1_ok = True
    for f in wf1_fields:
        if not fixed.get(f):
            result.errors.append(f"fixed_truth.{f} missing")
            wf1_ok = False
    immutable = fixed.get("immutable_facts", [])
    if not isinstance(immutable, list) or not immutable:
        result.errors.append("fixed_truth.immutable_facts must be a non-empty list")
        wf1_ok = False
    else:
        for item in immutable:
            if not isinstance(item, dict) or not item.get("fact_id"):
                result.errors.append("immutable_facts entry missing fact_id")
                wf1_ok = False
    result.checks["G-WF1"] = "PASS" if wf1_ok else "FAIL"

    all_fact_ids = {str(i.get("fact_id")) for i in immutable if isinstance(i, dict) and i.get("fact_id")}

    # --- G-WF2 Causal timeline ---
    timeline = package.get("causal_timeline", {})
    events = timeline.get("events", [])
    event_by_id: dict[str, dict[str, Any]] = {}
    wf2_ok = True
    ambiguous_dates: list[str] = []

    if not events:
        result.errors.append("causal_timeline.events empty")
        wf2_ok = False

    for ev in events:
        eid = ev.get("event_id")
        if not eid:
            result.errors.append("timeline event missing event_id")
            wf2_ok = False
            continue
        event_by_id[str(eid)] = ev
        ts = ev.get("timestamp", "")
        if not ts or _parse_timestamp(str(ts)) is None:
            ambiguous_dates.append(str(eid))
            result.errors.append(f"ambiguous or missing timestamp on event {eid}: {ts!r}")
            wf2_ok = False
        if not ev.get("day_label") and not str(ts).startswith("20"):
            result.errors.append(f"event {eid} missing day_label for non-ISO timestamp")
            wf2_ok = False
        all_fact_ids.update(_event_facts(ev))

    event_times: dict[str, datetime] = {}
    for eid, ev in event_by_id.items():
        parsed = _parse_timestamp(str(ev.get("timestamp", "")))
        if parsed:
            event_times[eid] = parsed

    for eid, ev in event_by_id.items():
        causes = ev.get("causes", []) or []
        for cause_id in causes:
            cid = str(cause_id)
            if cid not in event_by_id:
                result.errors.append(f"event {eid} references missing cause {cid}")
                wf2_ok = False
            elif eid in event_times and cid in event_times and event_times[eid] < event_times[cid]:
                result.errors.append(
                    f"timeline contradiction: {eid} occurs before its cause {cid}"
                )
                wf2_ok = False

    result.checks["G-WF2"] = "PASS" if wf2_ok else "FAIL"
    result.checks["WF-TIME-AMBIGUOUS"] = "FAIL" if ambiguous_dates else "PASS"

    # --- G-WF3 World state timeline ---
    wf3 = package.get("world_state_timeline", {})
    snapshots = wf3.get("snapshots", [])
    wf3_ok = True
    if not snapshots:
        result.errors.append("world_state_timeline.snapshots empty")
        wf3_ok = False
    for snap in snapshots:
        at = snap.get("at_event_id")
        if not at or str(at) not in event_by_id:
            result.errors.append(f"snapshot references missing event {at}")
            wf3_ok = False
        people = snap.get("people_locations", {}) or {}
        for npc_id, loc in people.items():
            participants = set()
            if at and str(at) in event_by_id:
                participants = {str(p) for p in event_by_id[str(at)].get("participants", [])}
            if str(npc_id) not in participants and participants:
                # presence mismatch unless travel event documented
                travel_ok = any(
                    str(e.get("event_id")) in (ev.get("causes") or [])
                    for eid, ev in event_by_id.items()
                    if str(ev.get("event_id")) == str(at)
                )
                if not travel_ok:
                    result.errors.append(
                        f"presence mismatch: {npc_id} at {loc} in snapshot {at} but not participant"
                    )
                    wf3_ok = False
    result.checks["G-WF3"] = "PASS" if wf3_ok else "FAIL"
    result.checks["WF-TRAVEL-PRESENCE"] = "PASS" if wf3_ok else "FAIL"

    # --- G-WF4 NPC knowledge ---
    npc_block = package.get("npc_knowledge", {})
    npcs = npc_block.get("npcs", [])
    witnessed_facts: dict[str, set[str]] = {}
    for ev in events:
        eid = str(ev.get("event_id", ""))
        for p in ev.get("participants", []) or []:
            pid = str(p)
            witnessed_facts.setdefault(pid, set()).update(_event_facts(ev))

    wf4_ok = True
    for npc in npcs:
        nid = str(npc.get("npc_id", ""))
        knows = {str(k) for k in npc.get("knows", []) or []}
        witnessed = {str(w) for w in npc.get("witnessed_events", []) or []}
        derivable: set[str] = set()
        for we in witnessed:
            if we in event_by_id:
                derivable.update(_event_facts(event_by_id[we]))
        for fact in knows:
            if fact not in derivable and fact not in all_fact_ids:
                # allow facts established in immutable_truth only if witnessed path exists
                pass
            if fact not in derivable:
                result.errors.append(f"NPC {nid} knows {fact} without witness/access chain")
                wf4_ok = False
    result.checks["G-WF4"] = "PASS" if wf4_ok else "FAIL"
    result.checks["WF-NPC-OVERKNOW"] = "PASS" if wf4_ok else "FAIL"

    # --- G-WF5 Evidence provenance ---
    evid_block = package.get("evidence_provenance", {})
    evidence_list = evid_block.get("evidence", [])
    wf5_ok = True
    established_by_evidence: set[str] = set()
    for evd in evidence_list:
        eid = evd.get("evidence_id")
        src = evd.get("source_event_id")
        if not src or str(src) not in event_by_id:
            result.errors.append(f"evidence {eid} missing or invalid source_event_id {src}")
            wf5_ok = False
        for fid in evd.get("establishes_fact_ids", []) or []:
            established_by_evidence.add(str(fid))
            all_fact_ids.add(str(fid))
    result.checks["G-WF5"] = "PASS" if wf5_ok else "FAIL"
    result.checks["WF-EVIDENCE-SOURCE"] = "PASS" if wf5_ok else "FAIL"

    # --- G-WF6 Conclusion requirements ---
    concl = package.get("conclusion_requirements", {})
    questions = concl.get("questions", [])
    observable = package.get("observable_information", {})
    observations = observable.get("observations", [])
    learnable: set[str] = {str(o.get("learnable_fact_id")) for o in observations if o.get("learnable_fact_id")}
    learnable.update(established_by_evidence)
    for ev in events:
        learnable.update(_event_facts(ev))

    wf6_ok = True
    for q in questions:
        qid = q.get("question_id")
        required = {str(r) for r in q.get("required_fact_ids", []) or []}
        missing = required - learnable - all_fact_ids
        if missing:
            result.errors.append(
                f"conclusion {qid} requires unobtainable facts: {sorted(missing)}"
            )
            wf6_ok = False
        if q.get("answer_entity_id"):
            pass  # answer tracked for future uniqueness checks
    if not questions:
        result.errors.append("conclusion_requirements.questions empty")
        wf6_ok = False
    result.checks["G-WF6"] = "PASS" if wf6_ok else "FAIL"
    result.checks["WF-CONCLUSION-COVERAGE"] = "PASS" if wf6_ok else "FAIL"

    # --- G-WF7 Narrative construction gate ---
    gates = manifest.get("gates", {}) or {}
    required_gates = ("G-WF1", "G-WF2", "G-WF3", "G-WF4", "G-WF5", "G-WF6")
    gates_ok = all(
        (gates.get(g, {}).get("status") == "PASS" or result.checks.get(g) == "PASS")
        for g in required_gates
    )
    narrative = package.get("narrative_construction", {})
    scenes = narrative.get("scenes", [])
    wf7_ok = True
    culprit_id = str(fixed.get("culprit_id", ""))
    for scene in scenes:
        for fid in scene.get("asserted_fact_ids", []) or []:
            if str(fid) not in all_fact_ids and str(fid) not in learnable:
                result.errors.append(
                    f"scene {scene.get('scene_id')} asserts fact {fid} not in fixed truth"
                )
                wf7_ok = False
        if scene.get("asserted_culprit_id") and str(scene.get("asserted_culprit_id")) != culprit_id:
            result.errors.append(
                f"scene {scene.get('scene_id')} contradicts fixed_truth culprit"
            )
            wf7_ok = False
    if scenes and not gates_ok:
        result.errors.append("narrative scenes present but prerequisite gates not PASS")
        wf7_ok = False
    result.checks["G-WF7"] = "PASS" if wf7_ok else "FAIL"
    result.checks["WF-SCENE-TRUTH"] = "PASS" if wf7_ok else "FAIL"

    # Ending claims in package (if present)
    endings = package.get("ending_claims", []) or []
    wf_end_ok = True
    for ending in endings:
        for fid in ending.get("asserted_fact_ids", []) or []:
            if str(fid) not in all_fact_ids:
                result.errors.append(f"ending {ending.get('ending_id')} asserts unestablished fact {fid}")
                wf_end_ok = False
    result.checks["WF-ENDING-TRUTH"] = "PASS" if wf_end_ok else "FAIL"

    if not wf_end_ok:
        wf7_ok = False

    if result.errors:
        result.status = "FAIL"
    return result


def main(argv: list[str] | None = None) -> int:
    import sys

    args = argv or sys.argv[1:]
    if not args:
        print("Usage: python3 -m idne.world_first_validate <adventure_root>")
        return 2
    res = validate_world_first(args[0])
    print(json.dumps(res.to_dict(), indent=2))
    return 0 if res.status in ("PASS", "SKIP") else 1


if __name__ == "__main__":
    raise SystemExit(main())
