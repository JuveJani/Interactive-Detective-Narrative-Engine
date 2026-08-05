"""Repair classification and limited automatic repair."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from idne.generate.stages import STORY_CRITICAL_FIELDS


AUTO_REPAIRABLE_IDS = frozenset(
    {
        "SCHEMA",
        "BROKEN_REFERENCE",
        "FORMATTING",
        "MISSING_FIELD",
        "LOCAL_CONSISTENCY",
    }
)


def classify_finding(finding: dict[str, Any]) -> str:
    fid = str(finding.get("finding_id", "")).upper()
    layer = str(finding.get("layer", "")).lower()
    if any(x in fid for x in ("SCHEMA", "FORMAT", "MISSING")):
        return "SCHEMA"
    if "REFERENCE" in fid or "ORPHAN" in fid:
        return "BROKEN_REFERENCE"
    if layer in STORY_CRITICAL_FIELDS or any(
        x in fid for x in ("CULPRIT", "MOTIVE", "METHOD", "TIMELINE", "ENDING")
    ):
        return "STORY_CRITICAL"
    if finding.get("human_approval_needed"):
        return "STORY_CRITICAL"
    return "LOCAL_CONSISTENCY"


def can_auto_repair(finding: dict[str, Any]) -> bool:
    category = classify_finding(finding)
    return category in AUTO_REPAIRABLE_IDS


def attempt_schema_repair(path: Path, finding: dict[str, Any]) -> bool:
    """Repair simple schema/format issues without changing story truth."""
    if not path.exists():
        return False
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return False

    fid = str(finding.get("finding_id", ""))
    changed = False

    if "MISSING" in fid.upper() and isinstance(data, dict):
        if "schema_version" not in data:
            data["schema_version"] = "1.0"
            changed = True

    if changed:
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        return True
    return False


def repair_request_payload(
    stage_id: str,
    findings: list[dict[str, Any]],
    source_context: dict[str, Any],
) -> dict[str, Any]:
    auto = [f for f in findings if can_auto_repair(f)]
    manual = [f for f in findings if not can_auto_repair(f)]
    return {
        "stage_id": stage_id,
        "auto_repairable": auto,
        "requires_human_approval": manual,
        "source_context": source_context,
    }


def would_change_fixed_truth(field_name: str) -> bool:
    return field_name in STORY_CRITICAL_FIELDS or field_name in (
        "culprit_id",
        "motive",
        "method",
        "immutable_facts",
    )
