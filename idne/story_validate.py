"""Story Validator (Milestone 8)."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from idne.story_player_extract import (
    collect_player_files,
    opening_communicates_frame,
    scan_plain_language,
)

QUOTATION_EMPHASIS_RE = re.compile(r"[\"'][\w\s]{3,30}[\"']")
LOADED_ADJ_RE = re.compile(
    r"\b(strangely|suspiciously|oddly|clearly guilty|obviously innocent)\b",
    re.I,
)


@dataclass
class Finding:
    finding_id: str
    severity: str
    confidence: str
    layer: str
    source_file: str
    entity_id: str
    player_excerpt: str
    expected_canonical: str
    observed_issue: str
    affected_question: str
    affected_conclusion: str
    affected_ending: str
    script_detectable: bool
    tier: str
    suggested_review_action: str
    human_approval_needed: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "finding_id": self.finding_id,
            "severity": self.severity,
            "confidence": self.confidence,
            "layer": self.layer,
            "source_file": self.source_file,
            "entity_id": self.entity_id,
            "player_excerpt": self.player_excerpt,
            "expected_canonical": self.expected_canonical,
            "observed_issue": self.observed_issue,
            "affected_question": self.affected_question,
            "affected_conclusion": self.affected_conclusion,
            "affected_ending": self.affected_ending,
            "script_detectable": self.script_detectable,
            "tier": self.tier,
            "suggested_review_action": self.suggested_review_action,
            "human_approval_needed": self.human_approval_needed,
        }


@dataclass
class ValidationResult:
    adventure_root: Path
    status: str
    findings: list[Finding] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    checks: dict[str, str] = field(default_factory=dict)
    tier_b_pending: list[str] = field(default_factory=list)
    player_files_scanned: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "adventure_root": str(self.adventure_root),
            "status": self.status,
            "findings": [f.to_dict() for f in self.findings],
            "warnings": self.warnings,
            "checks": self.checks,
            "tier_b_pending": self.tier_b_pending,
            "player_files_scanned": self.player_files_scanned,
        }


def load_manifest(root: Path) -> dict[str, Any] | None:
    for name in ("story_validator_manifest.json", "STORY_VALIDATOR_MANIFEST.json"):
        path = root / name
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    gen = root / "generation_manifest.json"
    if gen.exists():
        data = json.loads(gen.read_text(encoding="utf-8"))
        sv = data.get("story_validator")
        if isinstance(sv, dict) and sv.get("enabled"):
            return {
                "schema_version": data.get("schema_version", "1.0"),
                "story_validator_method": "canonical",
                "package_path": sv.get("package_path", "DO_NOT_READ/story_validator_package.json"),
            }
    return None


def load_package(root: Path, manifest: dict[str, Any]) -> dict[str, Any] | None:
    rel = manifest.get("package_path", "DO_NOT_READ/story_validator_package.json")
    path = root / rel
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _add(
    result: ValidationResult,
    finding_id: str,
    layer: str,
    entity_id: str,
    expected: str,
    observed: str,
    source_file: str = "story_validator_package.json",
    excerpt: str = "",
    question: str = "",
    conclusion: str = "",
    ending: str = "",
    tier: str = "A",
    confidence: str = "proven",
    human: bool = False,
) -> None:
    result.findings.append(
        Finding(
            finding_id=finding_id,
            severity="critical",
            confidence=confidence,
            layer=layer,
            source_file=source_file,
            entity_id=entity_id,
            player_excerpt=excerpt[:200],
            expected_canonical=expected,
            observed_issue=observed,
            affected_question=question,
            affected_conclusion=conclusion,
            affected_ending=ending,
            script_detectable=tier == "A",
            tier=tier,
            suggested_review_action="Fix story package or PLAYER prose",
            human_approval_needed=human,
        )
    )


def validate_story(adventure_root: str | Path) -> ValidationResult:
    root = Path(adventure_root).resolve()
    result = ValidationResult(adventure_root=root, status="PASS")

    manifest = load_manifest(root)
    if not manifest:
        result.status = "SKIP"
        result.warnings.append("no story_validator_manifest — not declared")
        return result

    if manifest.get("story_validator_method") != "canonical":
        result.status = "SKIP"
        result.warnings.append("story_validator_method not canonical")
        return result

    package = load_package(root, manifest)
    if not package:
        result.status = "FAIL"
        result.checks["SV-PKG-PRESENT"] = "FAIL"
        _add(result, "SV-PKG-MISSING", "validator", "", "package present", "missing")
        return result
    result.checks["SV-PKG-PRESENT"] = "PASS"

    audit = package.get("player_audit", {}) or {}
    player_files = audit.get("files", []) or []
    player_text = collect_player_files(root, player_files)
    result.player_files_scanned = list(player_text.keys())

    blocked_missing_player = audit.get("player_text_absent", False) or (
        player_files and not player_text
    )
    if blocked_missing_player:
        result.checks["SV-PLAYER-PRESENT"] = "BLOCKED"
        _add(
            result,
            "SV-PLAYER-ABSENT",
            "player",
            "",
            "PLAYER text available",
            "missing or absent",
            tier="A",
        )
    else:
        result.checks["SV-PLAYER-PRESENT"] = "PASS"

    # --- Story frame ---
    frame_ok = True
    frame = package.get("story_frame", {}) or {}
    required_frame = (
        "investigation_starts_where",
        "investigation_starts_when",
        "incident_description",
        "incident_when",
        "investigator_involvement",
        "deadline_or_constraint",
    )
    for key in required_frame:
        if not frame.get(key):
            frame_ok = False
            _add(result, "SV-FRAME-MISSING", "story_frame", key, "frame field present", "missing")
    for spoiler_key in (
        "reveals_culprit",
        "reveals_motive",
        "reveals_hidden_relationships",
        "reveals_correct_priority",
    ):
        if frame.get(spoiler_key):
            frame_ok = False
            _add(result, "SV-FRAME-SPOILER", "story_frame", spoiler_key, "spoiler-safe frame", "reveals spoiler")
    opening_rel = audit.get("opening_file")
    if opening_rel and opening_rel in player_text and frame:
        if not audit.get("story_frame_communicated", True):
            frame_ok = False
            _add(result, "SV-OPENING-LACKS-CONTEXT", "opening", opening_rel, "opening communicates frame", "not communicated")
        elif not opening_communicates_frame(player_text[opening_rel], frame):
            frame_ok = False
            _add(
                result,
                "SV-OPENING-LACKS-CONTEXT",
                "opening",
                opening_rel,
                "opening communicates frame",
                "keywords missing in PLAYER opening",
                source_file=opening_rel,
                excerpt=player_text[opening_rel][:120],
            )
    result.checks["SV-FRAME"] = "PASS" if frame_ok else "FAIL"

    # --- Timeline ---
    timeline_ok = True
    tl = package.get("timeline", {}) or {}
    if tl.get("investigation_confused_with_incident"):
        timeline_ok = False
        _add(result, "SV-START-INCIDENT-CONFUSED", "timeline", "", "distinct start vs incident", "confused")
    if tl.get("impossible_ordering"):
        timeline_ok = False
        _add(result, "SV-TIMELINE-IMPOSSIBLE", "timeline", "", "possible ordering", "impossible ordering")
    for evt in tl.get("events", []) or []:
        eid = str(evt.get("event_id", ""))
        if evt.get("ambiguous_day"):
            timeline_ok = False
            _add(result, "SV-AMBIGUOUS-DAY", "timeline", eid, "clear day", "ambiguous day")
        if evt.get("relative_without_anchor"):
            timeline_ok = False
            _add(result, "SV-RELATIVE-NO-ANCHOR", "timeline", eid, "anchored relative reference", "no anchor")
        if evt.get("silent_time_switch"):
            timeline_ok = False
            _add(result, "SV-SILENT-TIME-SWITCH", "timeline", eid, "explicit time frame", "silent switch")
        for contra in evt.get("contradicts", []) or []:
            timeline_ok = False
            _add(result, "SV-CONTRADICTORY-TIMELINE", "timeline", eid, "consistent timeline", f"contradicts {contra}")
    for ref in tl.get("temporal_references", []) or []:
        rid = str(ref.get("ref_id", ""))
        if not ref.get("day_clear") and ref.get("text_fragment"):
            timeline_ok = False
            _add(result, "SV-AMBIGUOUS-DAY", "timeline", rid, "clear day for time", ref.get("text_fragment", ""))
        if ref.get("contradictory"):
            timeline_ok = False
            _add(result, "SV-CONTRADICTORY-TIMELINE", "timeline", rid, "no contradiction", "contradictory")
        if not ref.get("maps_to_anchor"):
            timeline_ok = False
            _add(result, "SV-RELATIVE-NO-ANCHOR", "timeline", rid, "maps to anchor", "unmapped")
    result.checks["SV-TIMELINE"] = "PASS" if timeline_ok else "FAIL"

    # --- Causal coherence ---
    causal_ok = True
    for evt in package.get("causal_events", []) or []:
        eid = str(evt.get("event_id", ""))
        if evt.get("missing_cause"):
            causal_ok = False
            _add(result, "SV-MISSING-CAUSE", "causal", eid, "cause declared", "missing cause")
        if evt.get("orphan_consequence"):
            causal_ok = False
            _add(result, "SV-ORPHAN-CONSEQUENCE", "causal", eid, "sourced consequence", "orphan")
        if not evt.get("motive_connected", True):
            causal_ok = False
            _add(result, "SV-MOTIVE-DISCONNECTED", "causal", eid, "motive connected", "disconnected")
        if not evt.get("method_compatible_with_world", True):
            causal_ok = False
            _add(result, "SV-METHOD-INCOMPATIBLE", "causal", eid, "compatible method", "incompatible")
        if not evt.get("action_consistent_with_knowledge", True):
            causal_ok = False
            _add(result, "SV-ACTION-KNOWLEDGE", "causal", eid, "consistent action", "inconsistent")
        if not evt.get("ending_supported", True):
            causal_ok = False
            _add(result, "SV-ENDING-UNSUPPORTED", "causal", eid, "ending supported", "unsupported")
    result.checks["SV-CAUSAL"] = "PASS" if causal_ok else "FAIL"

    # --- Information introduction ---
    info_ok = True
    for fact in package.get("information_facts", []) or []:
        fid = str(fact.get("fact_id", ""))
        if fact.get("half_information"):
            info_ok = False
            _add(result, "SV-HALF-INFORMATION", "information", fid, "complete introduction", "half-information")
        if fact.get("undefined_term") or fact.get("undefined_entity"):
            info_ok = False
            _add(result, "SV-UNDEFINED-ENTITY", "information", fid, "defined term", "undefined")
        if fact.get("used_before_introduction"):
            info_ok = False
            _add(result, "SV-FACT-BEFORE-INTRO", "information", fid, "intro before use", "used before intro")
        if fact.get("explained_after_required_use"):
            info_ok = False
            _add(result, "SV-LATE-EXPLANATION", "information", fid, "explain before use", "late explanation")
        if fact.get("appears_from_nowhere"):
            info_ok = False
            _add(result, "SV-FROM-NOWHERE", "information", fid, "sourced introduction", "from nowhere")
        if fact.get("unexplained_pronoun"):
            info_ok = False
            _add(result, "SV-UNEXPLAINED-PRONOUN", "information", fid, "clear reference", "unexplained pronoun")
        if fact.get("conflicting_duplicates"):
            info_ok = False
            _add(result, "SV-CONFLICTING-FACT", "information", fid, "consistent wording", "conflicting duplicates")
    result.checks["SV-INFORMATION"] = "PASS" if info_ok else "FAIL"

    # --- Knowledge order ---
    know_ok = True
    for scene in package.get("knowledge_order", []) or []:
        sid = str(scene.get("scene_id", scene.get("unit_id", "")))
        if scene.get("assumes_undiscovered_event"):
            know_ok = False
            _add(result, "SV-ASSUMES-UNAVAILABLE-KNOWLEDGE", "knowledge_order", sid, "only known facts", "undiscovered event")
        if scene.get("inference_terms_not_introduced"):
            know_ok = False
            _add(result, "SV-INFERENCE-UNDEFINED-TERM", "inference", sid, "terms introduced", "terms not introduced")
        if scene.get("npc_assumes_unformulated_question"):
            know_ok = False
            _add(result, "SV-NPC-UNFORMULATED", "knowledge_order", sid, "formulable question", "unformulated")
        if scene.get("object_uses_hidden_background"):
            know_ok = False
            _add(result, "SV-OBJECT-HIDDEN-BG", "knowledge_order", sid, "player-visible description", "hidden background")
        if scene.get("ending_relies_on_unavailable_info"):
            know_ok = False
            _add(result, "SV-ENDING-UNAVAILABLE-INFO", "knowledge_order", sid, "available info on path", "unavailable")
        req = set(scene.get("required_knowledge_ids", []) or [])
        prior = set(scene.get("possible_prior_knowledge_ids", []) or [])
        if req and not req.issubset(prior):
            know_ok = False
            _add(
                result,
                "SV-ASSUMES-UNAVAILABLE-KNOWLEDGE",
                "knowledge_order",
                sid,
                "prior knowledge covers required",
                f"missing {sorted(req - prior)}",
            )
    result.checks["SV-KNOWLEDGE-ORDER"] = "PASS" if know_ok else "FAIL"

    # --- NPC consistency ---
    npc_ok = True
    for npc in package.get("npc_consistency", []) or []:
        nid = str(npc.get("npc_id", ""))
        if not npc.get("testimony_within_knowledge", True):
            npc_ok = False
            _add(result, "SV-NPC-BEYOND-KNOWLEDGE", "npc", nid, "testimony within knowledge", "beyond knowledge")
        if not npc.get("actions_match_motivation", True):
            npc_ok = False
            _add(result, "SV-NPC-MOTIVATION", "npc", nid, "motivation-consistent action", "contradicts motivation")
        if not npc.get("dialogue_within_knowledge", True):
            npc_ok = False
            _add(result, "SV-NPC-BEYOND-KNOWLEDGE", "npc", nid, "dialogue within knowledge", "beyond knowledge")
        if npc.get("drama_only_behavior"):
            npc_ok = False
            _add(result, "SV-NPC-DRAMA-ONLY", "npc", nid, "believable behaviour", "drama only")
        if npc.get("sudden_cooperation_unexplained"):
            npc_ok = False
            _add(result, "SV-NPC-SUDDEN-SHIFT", "npc", nid, "explained cooperation shift", "unexplained")
        if not npc.get("suspicious_innocent_believable", True):
            npc_ok = False
            _add(result, "SV-SUSPICIOUS-INNOCENT", "npc", nid, "believable innocent behaviour", "unexplained suspicious")
        if not npc.get("guilty_not_highlighted_by_wording", True):
            npc_ok = False
            _add(result, "SV-GUILTY-HIGHLIGHTED", "npc", nid, "neutral wording", "guilty highlighted", tier="B", confidence="likely", human=True)
    result.checks["SV-NPC"] = "PASS" if npc_ok else "FAIL"

    # --- Location / object continuity ---
    loc_ok = True
    for ent in package.get("location_object_continuity", []) or []:
        eid = str(ent.get("entity_id", ""))
        if not ent.get("introduced", True):
            loc_ok = False
            _add(result, "SV-OBJECT-NO-INTRO", "continuity", eid, "object introduced", "not introduced")
        if ent.get("moved_without_event"):
            loc_ok = False
            _add(result, "SV-OBJECT-MOVES", "continuity", eid, "movement has event", "moved without event")
        if ent.get("layout_changes_without_cause"):
            loc_ok = False
            _add(result, "SV-LAYOUT-CHANGE", "continuity", eid, "caused layout change", "unchanged cause")
        if ent.get("removed_item_reappears"):
            loc_ok = False
            _add(result, "SV-ITEM-REAPPEARS", "continuity", eid, "removed stays removed", "reappears")
        if ent.get("locked_described_open"):
            loc_ok = False
            _add(result, "SV-LOCKED-OPEN", "continuity", eid, "locked state consistent", "locked described open")
        if ent.get("references_inaccessible_area"):
            loc_ok = False
            _add(result, "SV-INACCESSIBLE-AREA", "continuity", eid, "accessible reference", "inaccessible area")
        if ent.get("revisit_ignores_changes"):
            loc_ok = False
            _add(result, "SV-REVISIT-IGNORES-STATE", "continuity", eid, "revisit reflects state", "ignores changes")
        if ent.get("time_variant_not_reflected"):
            loc_ok = False
            _add(result, "SV-TIME-VARIANT-TEXT", "continuity", eid, "time variant in text", "not reflected")
    result.checks["SV-CONTINUITY"] = "PASS" if loc_ok else "FAIL"

    # --- Narrative neutrality (Tier B) ---
    neutrality_ok = True
    for entry in package.get("narrative_neutrality", []) or []:
        eid = str(entry.get("entity_id", ""))
        if entry.get("suspicious_quotation_marks"):
            neutrality_ok = False
            _add(
                result,
                "SV-QUOTATION-EMPHASIS",
                "neutrality",
                eid,
                "neutral presentation",
                "suspicious quotation emphasis",
                tier="B",
                confidence="likely",
                human=True,
            )
        if entry.get("loaded_adjectives") or entry.get("loaded_description"):
            neutrality_ok = False
            _add(
                result,
                "SV-LOADED-DESCRIPTION",
                "neutrality",
                eid,
                "neutral suspect description",
                "loaded description",
                tier="B",
                confidence="likely",
                human=True,
            )
        if entry.get("asymmetric_detail") or entry.get("emphasis_spotlight"):
            neutrality_ok = False
            _add(
                result,
                "SV-SUSPECT-SPOTLIGHT",
                "neutrality",
                eid,
                "balanced suspect detail",
                "spotlight on one suspect",
                tier="B",
                confidence="likely",
                human=True,
            )
        if entry.get("tier_b_review_required"):
            neutrality_ok = False
            _add(
                result,
                "SV-NEUTRALITY-REVIEW",
                "neutrality",
                eid,
                "neutral narrative",
                "tier B review required",
                tier="B",
                confidence="likely",
                human=True,
            )
    # Scan PLAYER for loaded language when files present
    for rel, text in player_text.items():
        if LOADED_ADJ_RE.search(text):
            neutrality_ok = False
            _add(
                result,
                "SV-LOADED-DESCRIPTION",
                "neutrality",
                rel,
                "neutral prose",
                "loaded adjective in PLAYER",
                source_file=rel,
                excerpt=text[:120],
                tier="B",
                confidence="likely",
                human=True,
            )
        if QUOTATION_EMPHASIS_RE.search(text) and "strangely" in text.lower():
            neutrality_ok = False
            _add(
                result,
                "SV-QUOTATION-EMPHASIS",
                "neutrality",
                rel,
                "neutral quotation use",
                "emphasis quotation in PLAYER",
                source_file=rel,
                tier="B",
                confidence="likely",
                human=True,
            )
    result.checks["SV-NEUTRALITY"] = "PASS" if neutrality_ok else "FAIL"

    # --- Inference questions ---
    infer_ok = True
    for q in package.get("inference_questions", []) or []:
        qid = str(q.get("question_id", ""))
        if not q.get("terms_defined", True) or q.get("undefined_terms"):
            infer_ok = False
            _add(
                result,
                "SV-INFERENCE-UNDEFINED-TERM",
                "inference",
                qid,
                "defined terms",
                str(q.get("undefined_terms", [])),
                question=qid,
            )
        if not q.get("grammatically_clear", True) or q.get("grammatically_unclear"):
            infer_ok = False
            _add(result, "SV-INFERENCE-UNCLEAR", "inference", qid, "clear grammar", "unclear", question=qid)
        if not q.get("facts_communicated_not_just_canonical", True):
            infer_ok = False
            _add(result, "SV-INFERENCE-NOT-COMMUNICATED", "inference", qid, "facts in prose", "canonical only", question=qid)
        if q.get("presupposes_answer"):
            infer_ok = False
            _add(result, "SV-INFERENCE-PRESUPPOSES", "inference", qid, "neutral question", "presupposes answer", question=qid)
        if q.get("options_reveal_solution"):
            infer_ok = False
            _add(result, "SV-INFERENCE-OPTIONS-LEAK", "inference", qid, "neutral options", "reveals solution", question=qid)
    result.checks["SV-INFERENCE"] = "PASS" if infer_ok else "FAIL"

    # --- Opening and transitions ---
    trans_ok = True
    for tr in package.get("opening_transitions", []) or []:
        tid = str(tr.get("transition_id", tr.get("scene_id", "")))
        if tr.get("opening_lacks_incident_context"):
            trans_ok = False
            _add(result, "SV-OPENING-LACKS-CONTEXT", "opening", tid, "incident context", "lacks context")
        if tr.get("no_causal_explanation") or not tr.get("causal_transition", True):
            if tr.get("no_causal_explanation"):
                trans_ok = False
                _add(result, "SV-TRANSITION-NO-CAUSE", "transition", tid, "causal transition", "no explanation")
        if tr.get("unexplained_exposition"):
            trans_ok = False
            _add(result, "SV-UNEXPLAINED-EXPOSITION", "transition", tid, "explained exposition", "unexplained")
        if tr.get("unexplained_jump"):
            trans_ok = False
            _add(result, "SV-UNEXPLAINED-JUMP", "transition", tid, "causal jump", "unexplained jump")
    result.checks["SV-TRANSITIONS"] = "PASS" if trans_ok else "FAIL"

    # --- Ending story ---
    ending_ok = True
    for end in package.get("ending_story", []) or []:
        eid = str(end.get("ending_id", ""))
        if end.get("contradicts_fixed_truth"):
            ending_ok = False
            _add(result, "SV-ENDING-CONTRADICTS-TRUTH", "ending", eid, "matches Fixed Truth", "contradicts", ending=eid)
        if end.get("contradicts_timeline"):
            ending_ok = False
            _add(result, "SV-ENDING-TIMELINE", "ending", eid, "matches timeline", "contradicts timeline", ending=eid)
        if end.get("imperfect_leaks_full_truth"):
            ending_ok = False
            _add(result, "SV-IMPERFECT-LEAK", "ending", eid, "imperfect partial truth", "leaks full truth", ending=eid)
        if not end.get("causal_sequence", True):
            ending_ok = False
            _add(result, "SV-ENDING-NON-CAUSAL", "ending", eid, "causal sequence", "non-causal", ending=eid)
        if end.get("claims_unsupported_certainty"):
            ending_ok = False
            _add(result, "SV-ENDING-UNSUPPORTED", "ending", eid, "supported certainty", "unsupported", ending=eid)
        et = end.get("ending_type", "")
        if et == "perfect" and not end.get("coherently_explains_truth", True):
            ending_ok = False
            _add(result, "SV-PERFECT-NOT-COHERENT", "ending", eid, "coherent full explanation", "incoherent", ending=eid)
        if et in ("partial", "imperfect") and not end.get("intentionally_uncertain", True):
            if end.get("ending_type") == "imperfect" and not end.get("intentionally_uncertain"):
                ending_ok = False
                _add(result, "SV-IMPERFECT-NOT-UNCERTAIN", "ending", eid, "intentional uncertainty", "over-confident", ending=eid)
    result.checks["SV-ENDING"] = "PASS" if ending_ok else "FAIL"

    # --- Plain language (package flags + PLAYER scan) ---
    plain_ok = True
    pl = package.get("plain_language", {}) or {}
    known_acronyms = set(pl.get("known_acronyms", []) or [])
    aliases = pl.get("entity_name_aliases", {}) or {}
    jargon_terms = set(pl.get("jargon_terms", []) or [])

    for entry in pl.get("entries", []) or []:
        ref = str(entry.get("source_ref", ""))
        if entry.get("very_long_sentences"):
            plain_ok = False
            _add(result, "SV-LONG-SENTENCE", "plain_language", ref, "readable sentence length", "very long")
        if entry.get("undefined_acronyms"):
            plain_ok = False
            _add(result, "SV-UNDEFINED-ACRONYM", "plain_language", ref, "defined acronyms", str(entry.get("undefined_acronyms")))
        if entry.get("excessive_jargon"):
            plain_ok = False
            _add(result, "SV-EXCESSIVE-JARGON", "plain_language", ref, "accessible language", "excessive jargon")
        if entry.get("inconsistent_entity_names"):
            plain_ok = False
            _add(result, "SV-INCONSISTENT-NAMING", "plain_language", ref, "consistent names", str(entry.get("inconsistent_entity_names")))
        if entry.get("ambiguous_pronouns"):
            plain_ok = False
            _add(result, "SV-AMBIGUOUS-PRONOUN", "plain_language", ref, "clear pronouns", "ambiguous")

    for rel, text in player_text.items():
        scan = scan_plain_language(text, known_acronyms, aliases)
        if scan["very_long_sentences"]:
            plain_ok = False
            _add(
                result,
                "SV-LONG-SENTENCE",
                "plain_language",
                rel,
                "readable sentence length",
                "scan: long sentences",
                source_file=rel,
            )
        if scan["undefined_acronyms"]:
            plain_ok = False
            _add(
                result,
                "SV-UNDEFINED-ACRONYM",
                "plain_language",
                rel,
                "defined acronyms",
                str(scan["undefined_acronyms"]),
                source_file=rel,
            )
        if scan["inconsistent_entity_names"]:
            plain_ok = False
            _add(
                result,
                "SV-INCONSISTENT-NAMING",
                "plain_language",
                rel,
                "consistent entity names",
                str(scan["inconsistent_entity_names"]),
                source_file=rel,
            )
        jargon_hits = [t for t in jargon_terms if t.lower() in text.lower()]
        if len(jargon_hits) >= 3:
            plain_ok = False
            _add(result, "SV-EXCESSIVE-JARGON", "plain_language", rel, "accessible language", str(jargon_hits), source_file=rel)

    result.checks["SV-PLAIN-LANGUAGE"] = "PASS" if plain_ok else "FAIL"

    # --- Play mode ---
    pm = package.get("play_mode_constraints", {}) or {}
    play_modes = package.get("play_modes", []) or []
    mode_ok = True
    if "single_investigator" in play_modes and not pm.get("single_investigator_valid", True):
        mode_ok = False
        _add(result, "SV-SOLO-INVALID", "play_mode", "", "solo valid", "invalid")
    if "two_player" in play_modes and not pm.get("two_player_valid", True):
        mode_ok = False
        _add(result, "SV-TWO-PLAYER-INVALID", "play_mode", "", "two-player valid", "invalid")
    result.checks["SV-PLAY-MODE"] = "PASS" if mode_ok else "FAIL"

    # --- Tier B mandatory ---
    for item in package.get("tier_b_mandatory", []) or []:
        tid = str(item.get("review_id", ""))
        if not item.get("resolved"):
            result.tier_b_pending.append(tid)
            _add(
                result,
                f"SV-TIER-B-{tid}",
                "tier_b",
                tid,
                item.get("expected", "human review"),
                "pending",
                tier="B",
                confidence="likely",
                human=True,
            )

    # --- Outcome ---
    proven_a = [f for f in result.findings if f.tier == "A" and f.confidence == "proven"]
    if blocked_missing_player:
        result.status = "BLOCKED"
    elif proven_a:
        result.status = "FAIL"
    elif result.tier_b_pending or any(f.tier == "B" for f in result.findings):
        result.status = "CONDITIONAL_PASS"
    else:
        result.status = "PASS"

    return result


def main(argv: list[str] | None = None) -> int:
    import sys

    args = argv or sys.argv[1:]
    if not args:
        print("Usage: python3 -m idne.story_validate <adventure_root>")
        return 2
    res = validate_story(args[0])
    print(json.dumps(res.to_dict(), indent=2))
    if res.status == "BLOCKED":
        return 2
    return 0 if res.status in ("PASS", "SKIP", "CONDITIONAL_PASS") else 1


if __name__ == "__main__":
    raise SystemExit(main())
