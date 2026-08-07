"""Epistemic Progression Validator — knowledge- and world-state-gated scene progression."""

from __future__ import annotations

import json
import re
from collections import deque
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from idne.epistemic_progression.eligibility import action_eligible, event_enterable
from idne.epistemic_progression.fingerprint import StateFingerprint, template_unit_id
from idne.epistemic_progression.loader import (
    initial_epistemic_state,
    load_epistemic_manifest,
    load_epistemic_package,
)
from idne.epistemic_progression.model import (
    DIALOGUE_TOPIC_KINDS,
    ENDING_KINDS,
    HUB_KINDS,
    LOCATION_HUB_KINDS,
    NPC_INTERACTION_KINDS,
    EpistemicState,
    PlayableEvent,
    StructuredAction,
)
from idne.epistemic_progression.resolve import resolve_playable_unit
from idne.epistemic_progression.signatures import reuse_signature
from idne.gamebook_nav.extract import parse_player_units

DIALOGUE_TOPIC_ACTION_TYPES = frozenset({"dialogue_topic", "npc_topic", "topic"})
NPC_APPROACH_TYPES = frozenset({"approach_npc", "npc_interaction", "talk_npc"})
PSEUDO_RETURN_PHRASE = re.compile(
    r"return to your current location menu or continue the conversation",
    re.I,
)
UNRESOLVED_TIME_COST = re.compile(r"varies by topic", re.I)
TERMINAL_EVENT_KINDS = frozenset({"ending", "recovery"})

LOCATION_NPC_CONVERSATION_HUBS: dict[str, str] = {
    "UNIT-MARCUS-": "UNIT-SECURITY-BASE",
    "UNIT-LORI-": "UNIT-MANAGER-BASE",
}


@dataclass
class Finding:
    finding_id: str
    severity: str
    confidence: str
    layer: str
    source_file: str
    canonical_id: str
    expected_rule: str
    actual_state: str
    tier: str = "A"

    def to_dict(self) -> dict[str, Any]:
        return {
            "finding_id": self.finding_id,
            "severity": self.severity,
            "confidence": self.confidence,
            "layer": self.layer,
            "source_file": self.source_file,
            "canonical_id": self.canonical_id,
            "expected_rule": self.expected_rule,
            "actual_state": self.actual_state,
            "tier": self.tier,
        }


@dataclass
class ValidationResult:
    adventure_root: Path
    status: str
    findings: list[Finding] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    checks: dict[str, str] = field(default_factory=dict)
    tier_b_pending: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "adventure_root": str(self.adventure_root),
            "status": self.status,
            "findings": [f.to_dict() for f in self.findings],
            "warnings": self.warnings,
            "checks": self.checks,
            "tier_b_pending": self.tier_b_pending,
        }


def _add(
    result: ValidationResult,
    finding_id: str,
    canonical_id: str,
    expected: str,
    actual: str,
    *,
    source: str = "",
    layer: str = "epistemic_progression",
) -> None:
    result.findings.append(
        Finding(
            finding_id=finding_id,
            severity="error",
            confidence="proven",
            layer=layer,
            source_file=source,
            canonical_id=canonical_id,
            expected_rule=expected,
            actual_state=actual,
        )
    )


def _norm_label(label: str) -> str:
    return re.sub(r"\s+", " ", label.strip().lower())


def _load_player_manifest(root: Path) -> dict[str, Any]:
    for candidate in (root.parent / "player_mapping_manifest.json", root / "player_mapping_manifest.json"):
        if candidate.exists():
            return json.loads(candidate.read_text(encoding="utf-8"))
    return {}


def _load_flow_initial(root: Path) -> dict[str, Any]:
    path = root / "DO_NOT_READ" / "investigation_flow_package.json"
    if not path.exists():
        return {}
    pkg = json.loads(path.read_text(encoding="utf-8"))
    return dict(pkg.get("state_model", {}).get("initial_state") or {})


def _all_knowledge_ids(root: Path) -> set[str]:
    path = root / "DO_NOT_READ" / "investigation_core_package.json"
    if not path.exists():
        return set()
    pkg = json.loads(path.read_text(encoding="utf-8"))
    ids: set[str] = set()
    for k in pkg.get("knowledge", []) or []:
        if k.get("knowledge_id"):
            ids.add(str(k["knowledge_id"]))
    return ids


def _is_materialized_package(package) -> bool:
    return any(e.state_snapshot for e in package.events.values())


def _state_from_event_snapshot(event: PlayableEvent, package) -> EpistemicState:
    if not event.state_snapshot:
        return initial_epistemic_state(package)
    snap = event.state_snapshot
    return EpistemicState(
        player_knowledge=frozenset(snap.get("player_knowledge") or []),
        world_state=dict(snap.get("world_state") or {}),
        interaction_state={
            "completed_topics": list(snap.get("completed_topics") or []),
            "exhausted_actions": [],
        },
        observable_entities=package.initial_observable_entities,
        observable_objects=package.initial_observable_objects,
    )


def _structured_labels_for_template(package, template_id: str) -> set[str]:
    labels: set[str] = set()
    for event in package.events.values():
        if _prose_template_id(event) == template_id:
            labels.update(_norm_label(a.label) for a in event.structured_actions if a.label)
    return labels


def _validate_event_prerequisites(result: ValidationResult, package) -> None:
    for event in package.events.values():
        probe_base = _state_from_event_snapshot(event, package)
        for action in event.structured_actions:
            dest = package.events_by_unit.get(action.destination_unit_id)
            if not dest:
                continue
            probe = probe_base.apply_action_deltas(action)
            ok, reason = event_enterable(dest, probe)
            if not ok:
                _add(
                    result,
                    "EP-DEST-PREREQ-MISMATCH",
                    action.action_id,
                    "destination event enterable after action deltas",
                    reason,
                )


def _validate_hub_flattening(result: ValidationResult, package) -> None:
    for event in package.events.values():
        if event.event_kind not in HUB_KINDS:
            continue
        topic_actions = [
            a for a in event.structured_actions if a.action_type in DIALOGUE_TOPIC_ACTION_TYPES
        ]
        if topic_actions:
            _add(
                result,
                "EP-HUB-FLATTENED-DIALOGUE",
                event.unit_id,
                "location hub offers only immediate actions, not dialogue topics",
                f"hub contains {len(topic_actions)} dialogue topic action(s)",
            )
        for action in event.structured_actions:
            if action.action_type in DIALOGUE_TOPIC_ACTION_TYPES:
                continue
            dest = package.events_by_unit.get(action.destination_unit_id)
            if dest and dest.event_kind in DIALOGUE_TOPIC_KINDS:
                _add(
                    result,
                    "EP-HUB-FLATTENED-DIALOGUE",
                    event.unit_id,
                    "approach NPC before choosing dialogue topics",
                    f"hub action {action.action_id} jumps directly to topic event {dest.unit_id}",
                )


def _validate_action_knowledge_refs(result: ValidationResult, package, state: EpistemicState) -> None:
    for event in package.events.values():
        ok, _ = event_enterable(event, state)
        if not ok:
            continue
        for action in event.structured_actions:
            eligible, reason = action_eligible(action, state)
            if not eligible and "unknown facts" in reason:
                _add(
                    result,
                    "EP-CHOICE-UNKNOWN-FACT",
                    action.action_id,
                    "choice must not reference unknown facts",
                    reason,
                )
            if not eligible and "entity/object not observable" in reason:
                _add(
                    result,
                    "EP-CHOICE-UNKNOWN-ENTITY",
                    action.action_id,
                    "choice must not reference unknown entities",
                    reason,
                )
            missing = action.requires_knowledge_ids - state.player_knowledge
            if missing and action.label and any(k.lower().replace("know-", "") in action.label.lower() for k in missing):
                _add(
                    result,
                    "EP-CHOICE-UNKNOWN-FACT",
                    action.action_id,
                    "choice label must not name undiscovered facts",
                    f"label references knowledge not yet held: {sorted(missing)}",
                )


def _validate_later_state_actions(result: ValidationResult, package, state: EpistemicState) -> None:
    for event in package.events.values():
        if event.required_knowledge_ids or event.required_world_state:
            continue
        ok, _ = event_enterable(event, state)
        if not ok:
            continue
        for action in event.structured_actions:
            if action.requires_knowledge_ids and not action.requires_knowledge_ids <= state.player_knowledge:
                _add(
                    result,
                    "EP-ACTION-LATER-STATE",
                    f"{event.unit_id}:{action.action_id}",
                    "later-state action must not appear in earlier scene",
                    f"requires {sorted(action.requires_knowledge_ids)} at {event.unit_id}",
                )


NON_PROGRESS_ACTION_TYPES = frozenset(
    {"nav", "return", "travel", "approach", "approach_npc", "recovery", "inference_entry", "inference"}
)


def _validate_investigative_progress(result: ValidationResult, package) -> None:
    for event in package.events.values():
        for action in event.structured_actions:
            if not action.investigative:
                continue
            if action.action_type in NON_PROGRESS_ACTION_TYPES:
                continue
            if action.exhaustion in ("ambient", "recovery"):
                continue
            has_progress = bool(
                action.knowledge_delta
                or action.world_state_delta
                or action.interaction_delta
                or action.purpose
            )
            if not has_progress:
                _add(
                    result,
                    "EP-NO-PROGRESS",
                    action.action_id,
                    "investigative action must produce progress or declare purpose",
                    "no knowledge/world/interaction delta or purpose",
                )


def _validate_same_unit_knowledge_reuse(result: ValidationResult, package) -> None:
    for event in package.events.values():
        for action in event.structured_actions:
            if not action.knowledge_delta:
                continue
            dest_event = package.events_by_unit.get(action.destination_unit_id)
            if dest_event and dest_event.unit_id == event.unit_id:
                _add(
                    result,
                    "EP-SCENE-REUSE-KNOWLEDGE",
                    event.unit_id,
                    "knowledge-changing action must not return to the same event variant",
                    f"action {action.action_id} returns to {event.unit_id} after knowledge delta",
                )
            elif action.destination_unit_id == event.unit_id:
                _add(
                    result,
                    "EP-SCENE-REUSE-KNOWLEDGE",
                    event.unit_id,
                    "knowledge-changing action must not return to the same event variant",
                    f"action {action.action_id} returns to same unit after knowledge delta",
                )


def _validate_event_reuse(result: ValidationResult, package) -> None:
    by_physical: dict[str, list[PlayableEvent]] = {}
    for event in package.events.values():
        loc = event.physical_location_id or event.location_id
        by_physical.setdefault(loc, []).append(event)
    for loc, events in by_physical.items():
        variants = [e for e in events if e.variant_of or e.supersedes_unit_id]
        if len(variants) < 2:
            continue
        sigs: dict[tuple[Any, ...], str] = {}
        for event in variants:
            probe = initial_epistemic_state(package)
            sig = reuse_signature(event, probe)
            if sig in sigs and sigs[sig] != event.unit_id:
                _add(
                    result,
                    "EP-SCENE-REUSE-KNOWLEDGE",
                    event.unit_id,
                    "distinct variant required when relevant state differs",
                    f"same reuse signature as {sigs[sig]} at {loc}",
                )
            sigs[sig] = event.unit_id


def _validate_exhausted_actions(result: ValidationResult, package) -> None:
    state = initial_epistemic_state(package)
    for event in package.events.values():
        by_id: dict[str, list[StructuredAction]] = {}
        for action in event.structured_actions:
            if action.action_id:
                by_id.setdefault(action.action_id, []).append(action)
        for action in event.structured_actions:
            if action.exhaustion not in ("one_time", "exhaustible"):
                continue
            siblings = by_id.get(action.action_id, [])
            if len(siblings) > 1 and any(s.exhaustion == "repeatable" for s in siblings):
                _add(
                    result,
                    "EP-ONETIME-STILL-VISIBLE",
                    action.action_id,
                    "one-time action must not have repeatable duplicate in same event",
                    f"duplicate action_id {action.action_id} in {event.unit_id}",
                )
            after = state.apply_action_deltas(action)
            again, reason = action_eligible(action, after)
            if again:
                _add(
                    result,
                    "EP-ONETIME-STILL-VISIBLE",
                    action.action_id,
                    "one-time or exhaustible action must not remain eligible after use",
                    reason,
                )


def _validate_player_delivery_alignment(
    result: ValidationResult,
    root: Path,
    package,
    manifest: dict[str, Any],
) -> None:
    player_root = root / "PLAYER"
    known = set(manifest.get("units", {}).keys())
    player_units = parse_player_units(player_root, known or None)
    materialized = _is_materialized_package(package)

    if materialized:
        for tpl_id, pu in player_units.items():
            structured = _structured_labels_for_template(package, tpl_id)
            if not structured:
                continue
            player_labels = {_norm_label(c) for c in pu.choices}
            return_aliases = {
                _norm_label("Return to your current location menu or continue the conversation."),
                _norm_label("Return to the Elena conversation menu."),
                _norm_label("Return to the dock worker conversation menu."),
            }
            for label in structured:
                if label and label not in player_labels and label not in return_aliases:
                    _add(
                        result,
                        "EP-STRUCT-MISSING-CHOICE",
                        tpl_id,
                        "structured eligible action must appear in PLAYER delivery",
                        f"missing choice: {label[:80]}",
                        source=str(pu.file),
                    )
        return

    structured_by_unit: dict[str, set[str]] = {}
    for event in package.events.values():
        structured_by_unit[event.unit_id] = {_norm_label(a.label) for a in event.structured_actions}

    for uid, event in package.events_by_unit.items():
        prose_id = _prose_template_id(event)
        pu = player_units.get(prose_id)
        if not pu:
            continue
        structured = structured_by_unit.get(uid, set())
        player_labels = {_norm_label(c) for c in pu.choices}
        return_aliases = {
            _norm_label("Return to your current location menu or continue the conversation."),
            _norm_label("Return to the Elena conversation menu."),
            _norm_label("Return to the dock worker conversation menu."),
        }
        for label in player_labels:
            if label and label not in structured and label not in return_aliases:
                _add(
                    result,
                    "EP-PROSE-EXTRA-CHOICE",
                    uid,
                    "PLAYER choice must exist in structured action set",
                    f"extra choice: {label[:80]}",
                    source=str(pu.file),
                )
        for label in structured:
            if label and label not in player_labels:
                _add(
                    result,
                    "EP-STRUCT-MISSING-CHOICE",
                    uid,
                    "structured eligible action must appear in PLAYER delivery",
                    f"missing choice: {label[:80]}",
                    source=str(pu.file),
                )

    manifest_units = manifest.get("units") or {}
    for uid, event in package.events_by_unit.items():
        entry = manifest_units.get(uid, {})
        manifest_labels = {_norm_label(c.get("label", "")) for c in entry.get("choices") or []}
        structured = structured_by_unit.get(uid, set())
        state = initial_epistemic_state(package)
        ok, _ = event_enterable(event, state)
        if not ok:
            continue
        for action in event.structured_actions:
            eligible, reason = action_eligible(action, state)
            if not eligible:
                continue
            if _norm_label(action.label) in manifest_labels:
                continue
            _add(
                result,
                "EP-STRUCT-MISSING-CHOICE",
                uid,
                "manifest must expose eligible structured actions",
                f"missing manifest choice for {action.action_id}: {reason}",
            )


def _validate_content_blocks(result: ValidationResult, package, state: EpistemicState) -> None:
    for event in package.events.values():
        ok, _ = event_enterable(event, state)
        if not ok:
            continue
        for block in event.content_blocks:
            if block.provenance in ("observation", "atmosphere"):
                continue
            missing = block.requires_knowledge_ids - state.player_knowledge
            if missing and block.fact_ids:
                _add(
                    result,
                    "EP-FACT-BEFORE-REQ",
                    block.block_id,
                    "factual content requires satisfied knowledge prerequisites",
                    f"missing {sorted(missing)}",
                )


def _validate_impossible_prerequisites(result: ValidationResult, package, all_know: set[str]) -> None:
    acquirable: set[str] = set(package.initial_player_knowledge)
    for event in package.events.values():
        for action in event.structured_actions:
            acquirable.update(action.knowledge_delta)
    for event in package.events.values():
        unknown = event.required_knowledge_ids - all_know - acquirable
        if unknown:
            _add(
                result,
                "EP-PREREQ-IMPOSSIBLE",
                event.unit_id,
                "required knowledge must be acquirable or initial",
                f"unknown required knowledge: {sorted(unknown)}",
            )


def _validate_pseudo_choices(result: ValidationResult, package) -> None:
    for event in package.events.values():
        if event.event_kind in ENDING_KINDS or event.event_kind in TERMINAL_EVENT_KINDS:
            continue
        actions = event.structured_actions
        if not actions:
            continue
        dests = {a.destination_unit_id for a in actions}
        if len(dests) >= 2:
            continue
        if event.event_kind in DIALOGUE_TOPIC_KINDS:
            _add(
                result,
                "EP-PSEUDO-CHOICE",
                event.unit_id,
                "dialogue topic response must offer genuine branching (hub return and explicit exit)",
                f"only one destination: {sorted(dests)}",
            )
            continue
        for action in actions:
            if PSEUDO_RETURN_PHRASE.search(action.label):
                _add(
                    result,
                    "EP-PSEUDO-CHOICE",
                    event.unit_id,
                    "choice must not use pseudo-branch wording for a single target",
                    action.label[:80],
                )


def _validate_conversation_returns(result: ValidationResult, package) -> None:
    for event in package.events.values():
        if event.event_kind not in DIALOGUE_TOPIC_KINDS:
            continue
        hub_returns: list[str] = []
        location_hub = next(
            (hub for prefix, hub in LOCATION_NPC_CONVERSATION_HUBS.items() if event.unit_id.startswith(prefix)),
            None,
        )
        for action in event.structured_actions:
            dest = package.events_by_unit.get(action.destination_unit_id)
            if dest and dest.event_kind in NPC_INTERACTION_KINDS:
                hub_returns.append(action.destination_unit_id)
            elif (
                location_hub
                and action.destination_unit_id == location_hub
                and dest
                and dest.event_kind in LOCATION_HUB_KINDS
            ):
                hub_returns.append(action.destination_unit_id)
        if not hub_returns:
            _add(
                result,
                "EP-CONVERSATION-NO-HUB-RETURN",
                event.unit_id,
                "dialogue topic response must return to a conversation hub or hosting location menu",
                "no structured action targets npc_interaction or hosting location hub",
            )


def _prose_template_id(event: PlayableEvent) -> str:
    return event.template_unit_id or template_unit_id(event.unit_id)


def _snapshot_knowledge(event: PlayableEvent) -> frozenset[str]:
    if not event.state_snapshot:
        return frozenset()
    return frozenset(event.state_snapshot.get("player_knowledge") or [])


def _snapshot_completed_topics(event: PlayableEvent) -> frozenset[str]:
    if not event.state_snapshot:
        return frozenset()
    return frozenset(str(x) for x in (event.state_snapshot.get("completed_topics") or []))


def _validate_materialized_state_graph(
    result: ValidationResult,
    package,
    *,
    start_unit_id: str = "UNIT-DOCK-BASE",
    max_states: int = 500_000,
) -> dict[str, int]:
    """BFS reachable materialized states; reject stale or missing post-change snapshots."""
    initial = initial_epistemic_state(package)
    if start_unit_id not in package.events_by_unit:
        for uid in package.events_by_unit:
            if template_unit_id(uid) == uid and uid.endswith("-BASE"):
                start_unit_id = uid
                break

    stats = {
        "reachable_states": 0,
        "attempted_transitions": 0,
        "regressions": 0,
        "missing_snapshots": 0,
    }
    if start_unit_id not in package.events_by_unit:
        return stats

    q: deque[tuple[str, EpistemicState]] = deque([(start_unit_id, initial)])
    seen: set[tuple[str, StateFingerprint]] = set()

    while q:
        if stats["reachable_states"] >= max_states:
            result.warnings.append(f"state graph BFS truncated at {max_states} states")
            break

        cur_id, state = q.popleft()
        fp = StateFingerprint.from_state(state)
        visit_key = (cur_id, fp)
        if visit_key in seen:
            continue
        seen.add(visit_key)
        stats["reachable_states"] += 1

        event = package.events_by_unit.get(cur_id)
        if not event:
            stats["missing_snapshots"] += 1
            _add(
                result,
                "EP-MISSING-STATE-SNAPSHOT",
                cur_id,
                "reachable state must have a materialized event snapshot",
                f"no event for state {fp.key()}",
            )
            continue

        if event.state_snapshot:
            enterable, reason = event_enterable(event, state)
            if not enterable:
                _add(
                    result,
                    "EP-SNAPSHOT-MISMATCH",
                    cur_id,
                    "materialized event snapshot must match player epistemic state",
                    reason,
                )

        pre_knowledge = state.player_knowledge
        pre_topics = frozenset(str(x) for x in (state.interaction_state.get("completed_topics") or []))

        for action in event.structured_actions:
            eligible, _ = action_eligible(action, state)
            if not eligible:
                continue

            stats["attempted_transitions"] += 1
            next_state = state.apply_action_deltas(action)
            post_knowledge = next_state.player_knowledge
            post_topics = frozenset(str(x) for x in (next_state.interaction_state.get("completed_topics") or []))
            knowledge_changed = post_knowledge != pre_knowledge
            topics_changed = post_topics != pre_topics
            state_changed = knowledge_changed or topics_changed or bool(action.world_state_delta)

            dest_id = action.destination_unit_id
            dest = package.events_by_unit.get(dest_id)
            if not dest:
                stats["missing_snapshots"] += 1
                _add(
                    result,
                    "EP-MISSING-STATE-SNAPSHOT",
                    dest_id,
                    "action destination must reference an existing materialized event",
                    f"{action.action_id} from {cur_id} targets missing {dest_id}",
                )
                continue

            dest_topics = _snapshot_completed_topics(dest)

            if state_changed and dest.state_snapshot:
                dest_know = _snapshot_knowledge(dest)
                if dest_know != post_knowledge:
                    stats["regressions"] += 1
                    _add(
                        result,
                        "EP-STATE-REGRESSION",
                        action.action_id,
                        "post-change destination must represent full acquired knowledge",
                        f"dest {dest_id} knowledge {sorted(dest_know)} != post-action {sorted(post_knowledge)}",
                    )
                if dest_topics != post_topics:
                    stats["regressions"] += 1
                    _add(
                        result,
                        "EP-TOPIC-HUB-NOT-UPDATED",
                        action.action_id,
                        "post-topic destination must record completed conversation topics",
                        f"dest {dest_id} topics {sorted(dest_topics)} != post-action {sorted(post_topics)}",
                    )

            if event.event_kind in DIALOGUE_TOPIC_KINDS and topics_changed:
                dest_tpl = template_unit_id(dest_id)
                if dest_id == cur_id:
                    _add(
                        result,
                        "EP-TOPIC-SAME-HUB",
                        action.action_id,
                        "completed conversation topic must not return to the same pre-topic event",
                        f"topic {cur_id} returns to itself",
                    )
                elif dest.event_kind in NPC_INTERACTION_KINDS and dest.state_snapshot and dest_topics == pre_topics:
                    _add(
                        result,
                        "EP-TOPIC-SAME-HUB",
                        action.action_id,
                        "completed conversation topic must transition to an updated conversation hub",
                        f"hub {dest_id} still represents pre-topic state",
                    )

            if knowledge_changed and dest.state_snapshot:
                if _snapshot_knowledge(dest) == pre_knowledge:
                    stats["regressions"] += 1
                    _add(
                        result,
                        "EP-STATE-REGRESSION",
                        action.action_id,
                        "knowledge-changing action must not target a pre-knowledge event snapshot",
                        f"dest {dest_id} still at {sorted(pre_knowledge)} after gaining {sorted(action.knowledge_delta)}",
                    )

            expected = resolve_playable_unit(package, next_state, template_unit_id(dest_id), initial_state=initial)
            if expected != dest_id:
                _add(
                    result,
                    "EP-DEST-VARIANT-MISMATCH",
                    action.action_id,
                    "action destination must be the exact post-state materialized unit",
                    f"declared {dest_id}, expected {expected}",
                )

            q.append((dest_id, next_state))

    return stats


def _validate_knowledge_destination_variants(result: ValidationResult, package) -> None:
    """Legacy hand-crafted variant check — skipped when package uses state snapshots."""
    if any(e.state_snapshot for e in package.events.values()):
        return
    for event in package.events.values():
        for action in event.structured_actions:
            if not action.knowledge_delta:
                continue
            probe = initial_epistemic_state(package).apply_action_deltas(action)
            resolved = resolve_playable_unit(package, probe, action.destination_unit_id)
            if resolved != action.destination_unit_id:
                _add(
                    result,
                    "EP-DEST-VARIANT-MISMATCH",
                    action.action_id,
                    "knowledge-changing action must target enterable scene variant after deltas",
                    f"declared {action.destination_unit_id}, expected {resolved} after {sorted(action.knowledge_delta)}",
                )


def _validate_resolved_time_costs(
    result: ValidationResult,
    root: Path,
    package,
) -> None:
    player_root = root / "PLAYER"
    known = {e.unit_id for e in package.events.values()}
    player_units = parse_player_units(player_root, known or None)
    for event in package.events.values():
        if event.event_kind not in DIALOGUE_TOPIC_KINDS:
            continue
        pu = player_units.get(_prose_template_id(event))
        if not pu:
            continue
        for meta in pu.meta_lines:
            if UNRESOLVED_TIME_COST.search(meta):
                _add(
                    result,
                    "EP-TIME-COST-UNRESOLVED",
                    event.unit_id,
                    "resolved dialogue topic must not use unresolved time-cost placeholder",
                    meta,
                    source=str(pu.file),
                )


def _simulate_routes(result: ValidationResult, package, manifest: dict[str, Any]) -> None:
    """Bounded route check from opening state."""
    start = manifest.get("static_book", {}).get("start_unit_id", "")
    if not start or start not in package.events_by_unit:
        return
    state = initial_epistemic_state(package)
    event = package.events_by_unit[start]
    ok, reason = event_enterable(event, state)
    if not ok:
        _add(
            result,
            "EP-SIM-ROUTE-PREREQ",
            start,
            "starting event must be enterable in initial player state",
            reason,
        )


def validate_epistemic_progression(adventure_root: str | Path) -> ValidationResult:
    root = Path(adventure_root).resolve()
    result = ValidationResult(adventure_root=root, status="PASS")

    manifest = load_epistemic_manifest(root)
    if not manifest:
        result.status = "SKIP"
        result.warnings.append("no epistemic_progression_manifest — not declared")
        return result

    if manifest.get("epistemic_progression_method") != "canonical":
        result.status = "SKIP"
        result.warnings.append("epistemic_progression_method not canonical")
        return result

    package = load_epistemic_package(root, manifest)
    if not package:
        result.status = "FAIL"
        result.checks["EP-PKG-PRESENT"] = "FAIL"
        _add(result, "EP-PKG-PRESENT", "package", "epistemic_progression_package required", "missing")
        return result
    result.checks["EP-PKG-PRESENT"] = "PASS"

    player_manifest = _load_player_manifest(root)
    all_know = _all_knowledge_ids(root)
    state = initial_epistemic_state(package)
    flow_initial = _load_flow_initial(root)
    if flow_initial and not state.world_state:
        state.world_state = dict(flow_initial)

    _validate_impossible_prerequisites(result, package, all_know)
    _validate_event_prerequisites(result, package)
    _validate_hub_flattening(result, package)
    _validate_action_knowledge_refs(result, package, state)
    _validate_later_state_actions(result, package, state)
    _validate_investigative_progress(result, package)
    _validate_same_unit_knowledge_reuse(result, package)
    _validate_event_reuse(result, package)
    _validate_exhausted_actions(result, package)
    _validate_content_blocks(result, package, state)
    _validate_pseudo_choices(result, package)
    _validate_conversation_returns(result, package)
    _validate_knowledge_destination_variants(result, package)
    graph_stats = _validate_materialized_state_graph(
        result,
        package,
        start_unit_id=player_manifest.get("static_book", {}).get("start_unit_id", "UNIT-DOCK-BASE"),
    )
    result.checks["EP-STATE-GRAPH-REACHABLE"] = str(graph_stats.get("reachable_states", 0))
    _validate_resolved_time_costs(result, root, package)
    _validate_player_delivery_alignment(result, root, package, player_manifest)
    _simulate_routes(result, package, player_manifest)

    result.checks["EP-EVENT-GATES"] = "FAIL" if any(f.finding_id.startswith("EP-PREREQ") for f in result.findings) else "PASS"
    result.checks["EP-KNOWLEDGE-BOUNDARY"] = (
        "FAIL"
        if any(f.finding_id.startswith("EP-CHOICE") or f.finding_id == "EP-FACT-BEFORE-REQ" for f in result.findings)
        else "PASS"
    )
    result.checks["EP-HUB-DEPTH"] = (
        "FAIL" if any(f.finding_id == "EP-HUB-FLATTENED-DIALOGUE" for f in result.findings) else "PASS"
    )
    result.checks["EP-REUSE-RULES"] = (
        "FAIL"
        if any(f.finding_id.startswith("EP-SCENE-REUSE") or f.finding_id == "EP-ONETIME-STILL-VISIBLE" for f in result.findings)
        else "PASS"
    )
    result.checks["EP-CONVERSATION-FLOW"] = (
        "FAIL"
        if any(
            f.finding_id in ("EP-PSEUDO-CHOICE", "EP-CONVERSATION-NO-HUB-RETURN", "EP-TIME-COST-UNRESOLVED")
            for f in result.findings
        )
        else "PASS"
    )
    result.checks["EP-VARIANT-DEST"] = (
        "FAIL"
        if any(
            f.finding_id
            in (
                "EP-DEST-VARIANT-MISMATCH",
                "EP-STATE-REGRESSION",
                "EP-MISSING-STATE-SNAPSHOT",
                "EP-TOPIC-SAME-HUB",
                "EP-TOPIC-HUB-NOT-UPDATED",
                "EP-SNAPSHOT-MISMATCH",
            )
            for f in result.findings
        )
        else "PASS"
    )
    result.checks["EP-DELIVERY-ALIGN"] = (
        "FAIL"
        if any(f.finding_id.startswith("EP-PROSE") or f.finding_id.startswith("EP-STRUCT") for f in result.findings)
        else "PASS"
    )
    result.checks["EP-ROUTE-PREREQ"] = (
        "FAIL" if any(f.finding_id == "EP-SIM-ROUTE-PREREQ" for f in result.findings) else "PASS"
    )

    if result.findings:
        result.status = "FAIL"
    return result
