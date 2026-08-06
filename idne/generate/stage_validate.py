"""Run stage-specific validators."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from idne.epistemic_progression_validate import validate_epistemic_progression
from idne.capability_check_validate import validate_capability_check
from idne.dm_feeling_validate import validate_dm_feeling
from idne.environment_validate import validate_environment
from idne.investigation_core_validate import validate_investigation_core
from idne.investigation_flow_validate import validate_investigation_flow
from idne.npc_investigation_validate import validate_npc_investigation
from idne.object_interaction_validate import validate_object_interaction
from idne.playtime_validate import validate_playtime
from idne.story_validate import validate_story
from idne.validate_adventure.runner import validate_adventure
from idne.world_first_validate import validate_world_first


def run_stage_validator(validator_name: str | None, adventure_root: Path) -> dict[str, Any]:
    if not validator_name:
        return {"status": "PASS", "skipped": True}

    if validator_name == "integrated":
        res = validate_adventure(adventure_root)
        return res.to_dict()

    fn_map = {
        "world_first": validate_world_first,
        "environment": validate_environment,
        "object_interaction": validate_object_interaction,
        "investigation_core": validate_investigation_core,
        "npc_investigation": validate_npc_investigation,
        "investigation_flow": validate_investigation_flow,
        "epistemic_progression": validate_epistemic_progression,
        "capability_check": validate_capability_check,
        "story": validate_story,
        "playtime": validate_playtime,
        "dm_feeling": validate_dm_feeling,
    }
    fn = fn_map.get(validator_name)
    if not fn:
        return {"status": "PASS", "skipped": True}

    res = fn(adventure_root)
    status = getattr(res, "status", "FAIL")
    findings = []
    for f in getattr(res, "findings", []) or []:
        if hasattr(f, "to_dict"):
            findings.append(f.to_dict())
    errors = list(getattr(res, "errors", []) or [])
    return {
        "status": status,
        "findings": findings,
        "errors": errors,
        "tier_b_pending": list(getattr(res, "tier_b_pending", []) or []),
        "tier_c_complete": bool(getattr(res, "tier_c_complete", False)),
    }


def has_critical_or_major(findings: list[dict[str, Any]], errors: list[str]) -> bool:
    for f in findings:
        sev = str(f.get("severity", "")).upper()
        if sev in ("CRITICAL", "MAJOR"):
            return True
    return bool(errors)
