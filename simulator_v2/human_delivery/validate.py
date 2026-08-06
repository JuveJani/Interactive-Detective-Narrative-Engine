"""Human-delivery validation findings."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from idne.gamebook_validate import validate_gamebook
from simulator_v2.human_delivery.loader import AdventureWorkspace
from simulator_v2.human_delivery.parse import extract_start_section, parse_gamebook
from simulator_v2.human_delivery.types import DeliveryDefectClass, DeliveryFinding


def _unit_to_section(manifest: dict) -> dict[str, int]:
    pub = manifest.get("public_sections") or {}
    if pub:
        return {uid: int(sec) for uid, sec in pub.items()}
    out: dict[str, int] = {}
    for uid, entry in (manifest.get("units") or {}).items():
        sec = entry.get("public_section")
        if sec is not None:
            out[uid] = int(sec)
    return out


def _section_to_unit(manifest: dict) -> dict[int, str]:
    return {sec: uid for uid, sec in _unit_to_section(manifest).items()}


def validate_human_delivery(workspace: AdventureWorkspace) -> dict[str, Any]:
    findings: list[DeliveryFinding] = []
    manifest = workspace.manifest
    static = manifest.get("static_book") or {}

    if not static.get("gamebook_path"):
        findings.append(
            DeliveryFinding("HD-MISSING-PLAYABLE-FILE", "missing or ambiguous playable filename")
        )
    if not static.get("start_section"):
        findings.append(
            DeliveryFinding("HD-MISSING-START-SECTION", "missing declared starting section")
        )

    start_file, start_section, start_unit = extract_start_section(manifest)
    sec_to_unit = _section_to_unit(manifest)
    unit_to_sec = _unit_to_section(manifest)
    parsed = parse_gamebook(workspace.gamebook_path, sec_to_unit)

    if start_section and start_section not in parsed:
        findings.append(
            DeliveryFinding(
                "HD-START-ABSENT-BOOK",
                f"starting section {start_section} absent from GAMEBOOK.md",
            )
        )
    if start_unit and start_unit not in (manifest.get("units") or {}):
        findings.append(
            DeliveryFinding(
                "HD-START-ABSENT-MANIFEST",
                f"starting unit {start_unit} absent from mapping manifest",
            )
        )

    nums = list(sec_to_unit.keys())
    if len(nums) != len(set(nums)):
        findings.append(DeliveryFinding("HD-DUPLICATE-SECTION", "duplicate public section numbers"))

    for uid in (manifest.get("units") or {}):
        if uid not in unit_to_sec:
            findings.append(
                DeliveryFinding(
                    "HD-UNNUMBERED-UNIT",
                    f"reachable unit without public section: {uid}",
                    context={"unit_id": uid},
                )
            )

    for sec, ps in parsed.items():
        if not ps.unit_id:
            findings.append(
                DeliveryFinding(
                    "HD-SECTION-NO-UNIT",
                    f"public section {sec} without manifest unit mapping",
                )
            )
        for choice in ps.choices:
            if choice.destination_section is None:
                findings.append(
                    DeliveryFinding(
                        "HD-DESTINATIONLESS-CHOICE",
                        f"destinationless visible choice in section {sec}",
                        context={"label": choice.label[:80]},
                    )
                )
            elif choice.destination_section not in sec_to_unit:
                findings.append(
                    DeliveryFinding(
                        "HD-DANGLING-DESTINATION",
                        f"dangling destination section {choice.destination_section} from section {sec}",
                    )
                )
            elif choice.destination_section in sec_to_unit:
                manifest_unit = (manifest.get("units") or {}).get(ps.unit_id, {})
                visible_dest_unit = sec_to_unit[choice.destination_section]
                manifest_dests = {
                    edge.get("destination_unit_id")
                    for edge in manifest_unit.get("choices") or []
                    if edge.get("destination_unit_id")
                }
                if manifest_dests and visible_dest_unit not in manifest_dests:
                    findings.append(
                        DeliveryFinding(
                            "HD-WRONG-INTERNAL-MAP",
                            f"section {choice.destination_section} maps to {visible_dest_unit} "
                            f"but manifest choices from {ps.unit_id} expect {sorted(manifest_dests)}",
                        )
                    )
                else:
                    manifest_dest = None
                    for edge in manifest_unit.get("choices") or []:
                        dest_uid = edge.get("destination_unit_id", "")
                        if dest_uid and unit_to_sec.get(choice.destination_section) == dest_uid:
                            manifest_dest = dest_uid
                            break
                    if manifest_dest and manifest_dest != visible_dest_unit:
                        findings.append(
                            DeliveryFinding(
                                "HD-WRONG-INTERNAL-MAP",
                                f"section {choice.destination_section} maps to {visible_dest_unit} "
                                f"but manifest expects {manifest_dest}",
                            )
                        )

        kinds = {c.branch_kind for c in ps.choices}
        if "check_success" in kinds and "check_failure" not in kinds:
            findings.append(
                DeliveryFinding(
                    "HD-CHECK-MISSING-FAILURE",
                    f"check success without failure branch in section {sec}",
                )
            )
        if "check_failure" in kinds and "check_success" not in kinds:
            findings.append(
                DeliveryFinding(
                    "HD-CHECK-MISSING-SUCCESS",
                    f"check failure without success branch in section {sec}",
                )
            )

    gb = validate_gamebook(workspace.adventure_root)
    if gb.status != "PASS":
        for err in gb.errors[:5]:
            findings.append(DeliveryFinding("HD-GAMEBOOK-NAV", err))

    gamebook_text = workspace.gamebook_path.read_text(encoding="utf-8")
    if "DO_NOT_READ" in gamebook_text or "DO NOT READ" in gamebook_text:
        findings.append(
            DeliveryFinding(
                "HD-AUTHOR-ONLY-DEPENDENCY",
                "GAMEBOOK.md references author-only DO_NOT_READ material",
            )
        )

    reachable_from_start = _reachable_sections(parsed, start_section) if start_section else set()
    manifest_incoming_endings = _manifest_incoming_endings(manifest)
    for end_uid, sources in manifest_incoming_endings.items():
        end_sec = unit_to_sec.get(end_uid)
        if end_sec and end_sec not in reachable_from_start:
            findings.append(
                DeliveryFinding(
                    "HD-ENDING-UNREACHABLE",
                    f"canonical ending {end_uid} (section {end_sec}) unreachable via visible navigation "
                    f"(manifest edges from {sources[:3]})",
                    defect_class=DeliveryDefectClass.DELIVERY,
                )
            )

    for sec, ps in parsed.items():
        if not ps.unit_id.startswith("END-"):
            continue
        for choice in ps.choices:
            if choice.destination_section and choice.destination_section not in reachable_from_start:
                findings.append(
                    DeliveryFinding(
                        "HD-ENDING-ROUTE-BLOCKED",
                        f"visible navigation from ending section {sec} references unreachable section "
                        f"{choice.destination_section}",
                    )
                )

    status = "PASS" if not findings else "FAIL"
    return {
        "status": status,
        "adventure_id": workspace.adventure_id,
        "start_file": start_file,
        "start_section": start_section,
        "start_unit_id": start_unit,
        "section_count": len(parsed),
        "findings": [f.to_dict() for f in findings],
        "gamebook_path": str(workspace.gamebook_path.relative_to(workspace.adventure_root)),
        "used_unpacked_directory": not workspace.used_idne,
    }


def _manifest_incoming_endings(manifest: dict) -> dict[str, list[str]]:
    """END units reachable via manifest choice edges from non-terminal units."""
    end_ids = {uid for uid in (manifest.get("units") or {}) if uid.startswith("END-")}
    incoming: dict[str, list[str]] = {}
    for uid, entry in (manifest.get("units") or {}).items():
        if uid.startswith("END-"):
            continue
        for edge in entry.get("choices") or []:
            dest = edge.get("destination_unit_id", "")
            if dest in end_ids:
                incoming.setdefault(dest, []).append(uid)
    return incoming


def _reachable_sections(parsed: dict[int, Any], start: int) -> set[int]:
    seen = {start}
    queue = [start]
    while queue:
        sec = queue.pop(0)
        ps = parsed.get(sec)
        if not ps:
            continue
        for choice in ps.choices:
            if choice.destination_section and choice.destination_section not in seen:
                seen.add(choice.destination_section)
                queue.append(choice.destination_section)
    return seen
