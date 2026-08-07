"""Validate static gamebook navigation."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from idne.gamebook_nav.extract import PlayerUnit, parse_player_units, resolve_manifest_aliases
from idne.gamebook_nav.constants import DEFAULT_START_UNIT
from idne.gamebook_nav.graph import UnitNavigation, build_navigation_graph
from idne.gamebook_nav.sections import ANCHOR_TAG, LEGACY_BOLD_TURN, SECTION_HEADING, SECTION_LINK


@dataclass
class GamebookValidationResult:
    adventure_root: Path
    status: str  # PASS | FAIL | SKIP
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    checks: dict[str, str] = field(default_factory=dict)
    findings: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "adventure_root": str(self.adventure_root),
            "status": self.status,
            "errors": self.errors,
            "warnings": self.warnings,
            "checks": self.checks,
            "findings": self.findings,
        }


def validate_gamebook_navigation(
    adventure_root: Path,
    *,
    manifest: dict[str, Any] | None = None,
    player_units: dict[str, PlayerUnit] | None = None,
    graph: dict[str, UnitNavigation] | None = None,
    section_map: dict[str, int] | None = None,
    start_unit_id: str | None = None,
    gamebook_text: str | None = None,
) -> GamebookValidationResult:
    root = Path(adventure_root).resolve()
    result = GamebookValidationResult(adventure_root=root, status="PASS")

    play_manifest_path = root / "play_manifest.json"
    if not play_manifest_path.exists():
        result.status = "SKIP"
        result.warnings.append("no play_manifest.json")
        return result

    delivery = {}
    if manifest is None:
        import json

        mapping_path = root.parent / "player_mapping_manifest.json"
        if not mapping_path.exists():
            mapping_path = root / "player_mapping_manifest.json"
        if mapping_path.exists():
            manifest = json.loads(mapping_path.read_text(encoding="utf-8"))
    if manifest:
        delivery = manifest.get("static_book", {}) or {}
        start_unit_id = start_unit_id or delivery.get("start_unit_id")
        section_map = section_map or manifest.get("public_sections", {})
        manifest_units = manifest.get("units", {})

    if player_units is None:
        manifest_units = manifest.get("units", {}) if manifest else {}
        known = set(manifest_units.keys()) if manifest_units else None
        player_units = parse_player_units(root / "PLAYER", known)
        player_units = resolve_manifest_aliases(player_units, manifest_units)

    if graph is None:
        graph = build_navigation_graph(
            root,
            player_units,
            manifest_units=manifest.get("units") if manifest else None,
        )

    reachable = set(player_units.keys())
    if not start_unit_id:
        start_unit_id = delivery.get("start_unit_id") or DEFAULT_START_UNIT

    # GB-START
    start_section = section_map.get(start_unit_id) if section_map else None
    if start_unit_id not in reachable:
        result.errors.append(f"missing start section unit: {start_unit_id}")
        result.checks["GB-START"] = "FAIL"
    elif not start_section:
        result.errors.append(f"start unit {start_unit_id} has no public section number")
        result.checks["GB-START"] = "FAIL"
    else:
        result.checks["GB-START"] = "PASS"

    if not section_map:
        result.errors.append("missing public_sections mapping")
        result.checks["GB-SECTIONS"] = "FAIL"
    else:
        nums = list(section_map.values())
        if len(nums) != len(set(nums)):
            result.errors.append("duplicate public section numbers")
            result.checks["GB-DUPLICATE"] = "FAIL"
        else:
            result.checks["GB-DUPLICATE"] = "PASS"
        missing = reachable - set(section_map.keys())
        extra = set(section_map.keys()) - reachable
        if missing:
            result.errors.append(f"unnumbered reachable units: {sorted(missing)[:5]}")
            result.checks["GB-UNNUMBERED"] = "FAIL"
        else:
            result.checks["GB-UNNUMBERED"] = "PASS"
        if extra:
            result.warnings.append(f"sections for non-reachable units: {len(extra)}")
            result.checks["GB-ORPHAN-SECTIONS"] = "FAIL"
            result.errors.append(f"orphaned public sections: {sorted(extra)[:5]}")
        else:
            result.checks["GB-ORPHAN-SECTIONS"] = "PASS"
        result.checks["GB-SECTIONS"] = "PASS" if not missing else "FAIL"

    # dangling destinations & destinationless choices
    dangling: list[str] = []
    destless: list[str] = []
    check_pairs_missing: list[str] = []
    referenced_sections: set[int] = set()
    for uid, nav in graph.items():
        if uid not in reachable:
            continue
        pu = player_units.get(uid)
        if pu and pu.choices and not nav.choices:
            destless.append(uid)
        if not nav.choices and uid.startswith("END-"):
            continue
        for edge in nav.choices:
            if edge.destination_unit_id not in reachable:
                dangling.append(f"{uid} -> {edge.destination_unit_id} ({edge.label[:40]})")
            dest_sec = section_map.get(edge.destination_unit_id) if section_map else None
            if dest_sec is not None:
                referenced_sections.add(dest_sec)
            elif section_map:
                result.errors.append(
                    f"choice from {uid} references unmapped destination {edge.destination_unit_id}"
                )
        if uid.startswith("UNIT-CHK-") or (uid.endswith("-DECL") and "CHK" in uid):
            kinds = {e.edge_kind for e in nav.choices}
            pu = player_units.get(uid)
            placeholder = pu and any("success or failure" in c.lower() for c in pu.choices)
            if placeholder:
                continue
            if "check_success" not in kinds or "check_failure" not in kinds:
                check_pairs_missing.append(uid)

    if destless:
        result.errors.append(f"destinationless choices: {destless[:5]}")
        result.checks["GB-DESTLESS"] = "FAIL"
    else:
        result.checks["GB-DESTLESS"] = "PASS"

    if dangling:
        result.errors.append(f"dangling destinations: {dangling[:5]}")
        result.checks["GB-DANGLING"] = "FAIL"
    else:
        result.checks["GB-DANGLING"] = "PASS"

    if check_pairs_missing:
        result.errors.append(f"checks missing success/failure sections: {check_pairs_missing}")
        result.checks["GB-CHECK-SPLIT"] = "FAIL"
    else:
        result.checks["GB-CHECK-SPLIT"] = "PASS"

    if section_map and graph:
        from collections import deque

        from idne.epistemic_progression.loader import load_epistemic_package, initial_epistemic_state
        from idne.epistemic_progression.eligibility import action_eligible, event_enterable

        ep_pkg = load_epistemic_package(root)
        reachable_graph: set[str] = set()
        if start_unit_id in player_units:
            if ep_pkg:
                from idne.epistemic_progression.eligibility import filter_eligible_actions

                q: deque[tuple[str, Any]] = deque([(start_unit_id, initial_epistemic_state(ep_pkg))])
                reachable_graph = {start_unit_id}
                seen: set[tuple[str, frozenset[str], frozenset[str]]] = set()
                while q:
                    cur, state = q.popleft()
                    event = ep_pkg.events_by_unit.get(cur)
                    if not event:
                        for edge in graph.get(cur, UnitNavigation(cur)).choices:
                            dest = edge.destination_unit_id
                            if dest in player_units:
                                reachable_graph.add(dest)
                        continue
                    state_key = (
                        cur,
                        state.player_knowledge,
                        frozenset(state.world_state.items()),
                    )
                    if state_key in seen:
                        continue
                    seen.add(state_key)
                    for action, ok, _ in filter_eligible_actions(event, state):
                        if not ok:
                            continue
                        dest = action.destination_unit_id
                        if dest not in player_units:
                            continue
                        reachable_graph.add(dest)
                        q.append((dest, state.apply_action_deltas(action)))
            else:
                q = deque([start_unit_id])
                reachable_graph = {start_unit_id}
                while q:
                    cur = q.popleft()
                    for edge in graph.get(cur, UnitNavigation(cur)).choices:
                        if edge.destination_unit_id in player_units and edge.destination_unit_id not in reachable_graph:
                            reachable_graph.add(edge.destination_unit_id)
                            q.append(edge.destination_unit_id)
        non_terminal = {
            uid
            for uid in player_units
            if not uid.startswith("END-")
        }
        unreachable_units = sorted(non_terminal - reachable_graph)
        gated_ok = False
        if ep_pkg:
            from idne.epistemic_progression_validate import validate_epistemic_progression

            ep_res = validate_epistemic_progression(root)
            gated_ok = ep_res.status == "PASS"
        if unreachable_units and not gated_ok:
            result.errors.append(
                f"units unreachable from start via choices: {unreachable_units[:5]}"
            )
            result.checks["GB-REACHABILITY"] = "FAIL"
        else:
            result.checks["GB-REACHABILITY"] = "PASS"

    if gamebook_text is not None:
        for uid in reachable:
            sec = section_map.get(uid)
            if sec and f"## Section {sec}" not in gamebook_text and f"Section {sec}\n" not in gamebook_text:
                result.errors.append(f"gamebook missing section {sec} for {uid}")
                result.checks["GB-BOOK-COVERAGE"] = "FAIL"
                break
        else:
            result.checks["GB-BOOK-COVERAGE"] = "PASS"

        if section_map:
            anchor_ids = [int(m.group(1)) for m in ANCHOR_TAG.finditer(gamebook_text)]
            heading_ids = [int(m.group(1)) for m in SECTION_HEADING.finditer(gamebook_text)]
            expected = sorted(section_map.values())
            if sorted(anchor_ids) != expected:
                missing = sorted(set(expected) - set(anchor_ids))[:5]
                extra = sorted(set(anchor_ids) - set(expected))[:5]
                result.errors.append(
                    f"section anchor mismatch: missing={missing} extra={extra}"
                )
                result.checks["GB-ANCHORS"] = "FAIL"
            elif len(anchor_ids) != len(set(anchor_ids)):
                result.errors.append("duplicate section anchors in gamebook")
                result.checks["GB-ANCHORS"] = "FAIL"
            else:
                result.checks["GB-ANCHORS"] = "PASS"

            if sorted(heading_ids) != expected:
                result.errors.append("section headings do not match public_sections")
                result.checks["GB-HEADINGS"] = "FAIL"
            else:
                result.checks["GB-HEADINGS"] = "PASS"

            broken_links: list[str] = []
            for match in SECTION_LINK.finditer(gamebook_text):
                label, target = int(match.group(1)), int(match.group(2))
                if label != target:
                    broken_links.append(f"{label}->{target}")
                elif target not in section_map.values():
                    broken_links.append(str(target))
            if broken_links:
                result.errors.append(f"broken section links: {broken_links[:5]}")
                result.checks["GB-LINKS"] = "FAIL"
            else:
                result.checks["GB-LINKS"] = "PASS"

            legacy = LEGACY_BOLD_TURN.findall(gamebook_text)
            if legacy:
                result.warnings.append(f"non-clickable legacy section refs: {legacy[:5]}")
                result.checks["GB-CLICKABLE"] = "WARN"
            else:
                result.checks["GB-CLICKABLE"] = "PASS"

    if result.errors:
        result.status = "FAIL"
    return result
