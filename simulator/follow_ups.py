"""Adapter-driven follow-up actions (no keyword inference)."""

from __future__ import annotations

from typing import Any

from simulator.state import GameState


def legacy_keyword_follow_ups(adapter: dict[str, Any]) -> list[dict[str, Any]]:
    """Return legacy free-text follow-up rules that are not simulated."""
    legacy = adapter.get("follow_ups", [])
    if not legacy:
        return []
    # Only report keyword-style legacy entries
    return [r for r in legacy if r.get("keywords")]


def follow_up_actions(adapter: dict[str, Any]) -> list[dict[str, Any]]:
    return list(adapter.get("follow_up_actions", []))


def _hub_id_for_node(adapter: dict[str, Any], node: str) -> int | str | None:
    spec = adapter.get("nodes", {}).get(node, {})
    if spec.get("type") == "hub":
        return spec.get("hub_id", node)
    return None


def _eligible(state: GameState, action: dict[str, Any], hub_node: str, adapter: dict[str, Any]) -> bool:
    cond = action.get("eligible_when", {})
    sources = action.get("source_hubs", action.get("source_hub", []))
    if isinstance(sources, str):
        sources = [sources]
    if hub_node not in sources:
        return False

    action_id = action["id"]
    used = state.follow_up_use_counts.get(action_id, 0)
    max_uses = action.get("max_uses", 1)
    if used >= max_uses:
        return False

    global_max = adapter.get("follow_up_max", 2)
    if state.follow_ups_used >= global_max:
        return False

    for clue in cond.get("missing_clues", []):
        if clue in state.clues:
            return False
    for clue in cond.get("requires_clues", []):
        if clue not in state.clues:
            return False
    for flag in cond.get("requires_flags", []):
        if flag not in state.flags:
            return False
    for flag in cond.get("forbidden_flags", []):
        if flag in state.flags:
            return False
    if cond.get("requires_check_fail"):
        fail_flag = f"CHECK_FAIL_{cond['requires_check_fail']}"
        if fail_flag not in state.flags:
            return False
    return True


def eligible_follow_up_options(
    state: GameState,
    hub_node: str,
    adapter: dict[str, Any],
) -> list[dict[str, Any]]:
    """Public follow-up choices at a hub (no hidden grants)."""
    options: list[dict[str, Any]] = []
    for action in follow_up_actions(adapter):
        if not _eligible(state, action, hub_node, adapter):
            continue
        options.append(
            {
                "id": action["id"],
                "target": hub_node,
                "minutes": action.get("minutes", 0),
                "label": action.get("label", action["id"]),
                "type": "follow_up",
                "once_per_hub": False,
                "risky": False,
            }
        )
    return options


def apply_follow_up(
    state: GameState,
    action_id: str,
    adapter: dict[str, Any],
) -> int:
    """Apply follow-up effects; returns minutes consumed. Caller advances clock."""
    action = next((a for a in follow_up_actions(adapter) if a["id"] == action_id), None)
    if not action:
        return 0
    hub_node = state.node
    if not _eligible(state, action, hub_node, adapter):
        return 0

    minutes = action.get("minutes", 0)
    for clue in action.get("grants_clues_if_missing", []):
        state.grant_clue(clue)
    for flag in action.get("grants_flags", []):
        state.grant_flag(flag)
    dest = action.get("destination")
    if dest:
        state.node = dest
        state.path.append(dest)

    state.follow_ups_used += 1
    state.follow_up_use_counts[action_id] = state.follow_up_use_counts.get(action_id, 0) + 1
    state.path.append(f"{hub_node}:follow_up:{action_id}")
    return minutes
