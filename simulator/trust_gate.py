"""Structural trust invariants — adapter must satisfy canonical semantics, not just empty ambiguities."""

from __future__ import annotations

from typing import Any

from simulator.follow_ups import follow_up_actions, legacy_keyword_follow_ups
from simulator.graph import unreachable_nodes

# Required top-level adapter fields (must exist; empty list/dict allowed where noted).
REQUIRED_ADAPTER_FIELDS = (
    "schema_version",
    "adventure_id",
    "start_node",
    "start_clock",
    "deadline_clock",
    "follow_up_max",
    "follow_up_actions",
    "proof_rules",
    "infer_requirements",
    "splits",
    "nodes",
    "ambiguities",
)

# Harborview explicit follow-up actions required for simulation.
REQUIRED_FOLLOW_UP_IDS = ("FU_GYM_ALIBI", "FU_VENDOR_LOG")

# PLAYER J-410 authoritative infer scene cost (see sim_adapter description + JOINT_SCENES).
J410_PLAYER_MINUTES = 10


def validate_trust_invariants(adapter: dict[str, Any]) -> list[str]:
    """Return blockers when required canonical adapter invariants are missing or regressed."""
    blockers: list[str] = []

    for field in REQUIRED_ADAPTER_FIELDS:
        if field not in adapter:
            blockers.append(f"required adapter field missing: {field}")

    if adapter.get("follow_up_max", 0) < 1:
        blockers.append("follow_up_max must be a positive integer")

    actions = follow_up_actions(adapter)
    if not actions:
        blockers.append("follow_up_actions must be a non-empty list")
    else:
        action_ids = {a.get("id") for a in actions}
        for fid in REQUIRED_FOLLOW_UP_IDS:
            if fid not in action_ids:
                blockers.append(f"required follow_up_action missing: {fid}")

    if legacy_keyword_follow_ups(adapter):
        blockers.append("legacy keyword follow_ups remain active in adapter")

    blockers.extend(_check_p112_invariants(adapter))
    blockers.extend(_check_j410_i02_invariants(adapter))
    blockers.extend(_check_r212b_invariants(adapter))

    unreachable = unreachable_nodes(adapter)
    if unreachable:
        blockers.append(f"deterministic reachability failed: {sorted(unreachable)}")

    return blockers


def _check_p112_invariants(adapter: dict[str, Any]) -> list[str]:
    blockers: list[str] = []
    p112 = adapter.get("nodes", {}).get("P-112")
    if not p112:
        blockers.append("P-112 node missing from adapter")
        return blockers

    if "ACCESS_MANAGER_KEY" in p112.get("flags", []):
        blockers.append(
            "P-112 must not grant ACCESS_MANAGER_KEY unconditionally; use partner_conditional_flags"
        )

    rules = p112.get("partner_conditional_flags", [])
    if not rules:
        blockers.append("P-112 missing partner_conditional_flags for ACCESS_MANAGER_KEY eligibility")
        return blockers

    key_rule = next((r for r in rules if r.get("flag") == "ACCESS_MANAGER_KEY"), None)
    if not key_rule:
        blockers.append("P-112 partner_conditional_flags missing ACCESS_MANAGER_KEY rule")
    else:
        if key_rule.get("when_partner_lacks") != "ACCESS_MANAGER_KEY":
            blockers.append("P-112 key rule when_partner_lacks must be ACCESS_MANAGER_KEY")
        if key_rule.get("partner_role") != "records":
            blockers.append("P-112 key rule partner_role must be records")

    return blockers


def _check_j410_i02_invariants(adapter: dict[str, Any]) -> list[str]:
    blockers: list[str] = []
    j410 = adapter.get("nodes", {}).get("J-410")
    if not j410:
        blockers.append("J-410 node missing from adapter")
        return blockers

    if j410.get("type") != "infer" or j410.get("infer") != "I-02":
        blockers.append("J-410 must be infer node for I-02")

    blocked_return = j410.get("blocked_return")
    blocked_minutes = j410.get("blocked_minutes")
    minutes = j410.get("minutes")

    if not blocked_return:
        blockers.append("J-410 missing blocked_return for incomplete I-02")
    if blocked_minutes is None:
        blockers.append("J-410 missing blocked_minutes for incomplete I-02")
    elif not isinstance(blocked_minutes, (int, float)) or blocked_minutes <= 0:
        blockers.append("J-410 blocked_minutes must be a positive number")

    if minutes is None:
        blockers.append("J-410 missing minutes for infer scene")
    elif blocked_minutes is not None and minutes != blocked_minutes:
        blockers.append(
            f"J-410 minutes ({minutes}) must match blocked_minutes ({blocked_minutes})"
        )

    resolution = j410.get("minutes_cost_resolution")
    if not resolution:
        blockers.append("J-410 missing minutes_cost_resolution documenting authoritative cost")
    elif resolution.get("authoritative_minutes") != J410_PLAYER_MINUTES:
        blockers.append("J-410 minutes_cost_resolution authoritative_minutes must be 10 (PLAYER)")
    elif resolution.get("unresolved"):
        blockers.append("J-410 minutes_cost_resolution marked unresolved")

    if minutes != J410_PLAYER_MINUTES:
        blockers.append(
            f"J-410 minutes ({minutes}) must equal PLAYER-authoritative cost ({J410_PLAYER_MINUTES})"
        )

    return blockers


def _check_r212b_invariants(adapter: dict[str, Any]) -> list[str]:
    blockers: list[str] = []
    r212 = adapter.get("nodes", {}).get("R-212")
    r212b = adapter.get("nodes", {}).get("R-212b")
    if not r212b:
        blockers.append("R-212b node missing from adapter")
        return blockers

    next_opts = r212b.get("next_options", [])
    if not next_opts:
        blockers.append(
            "R-212b must use next_options per PLAYER (R-212/R-214); auto next causes loop"
        )
    elif set(next_opts) != {"R-212", "R-214"}:
        blockers.append(f"R-212b next_options must be [R-212, R-214]; got {next_opts}")

    if r212b.get("next") and not next_opts:
        blockers.append("R-212b must not use unconditional next without next_options")

    skim = next((c for c in (r212 or {}).get("choices", []) if c.get("id") == "skim"), None)
    if not skim:
        blockers.append("R-212 skim choice missing from adapter")
    elif not skim.get("once_per_role_path"):
        blockers.append("R-212 skim choice must set once_per_role_path per PLAYER skim-and-move-on")

    return blockers
