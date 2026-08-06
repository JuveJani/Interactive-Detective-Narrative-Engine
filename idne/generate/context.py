"""Stage-specific prompt and context builder."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

SPEC_ROOT = Path(__file__).resolve().parents[2]

STAGE_SPEC_MAP: dict[str, list[str]] = {
    "fixed_truth": ["WORLD_FIRST_GENERATION_SPEC.md"],
    "causal_timeline": ["WORLD_FIRST_GENERATION_SPEC.md"],
    "world_state_timeline": ["WORLD_FIRST_GENERATION_SPEC.md"],
    "npcs": ["WORLD_FIRST_GENERATION_SPEC.md", "NPC_INVESTIGATION_SYSTEM_SPEC.md"],
    "environment": ["ENVIRONMENT_SYSTEM_SPEC.md"],
    "objects": ["OBJECT_INTERACTION_SYSTEM_SPEC.md"],
    "investigation_core": ["INVESTIGATION_CORE_SPEC.md"],
    "npc_conversation": ["NPC_INVESTIGATION_SYSTEM_SPEC.md"],
    "investigation_flow": ["INVESTIGATION_FLOW_SPEC.md", "ENDING_SYSTEM_SPEC.md"],
    "capability_checks": ["CAPABILITY_CHECK_SYSTEM_SPEC.md"],
    "story_player": ["STORY_VALIDATOR_SPEC.md", "INVESTIGATION_FLOW_SPEC.md", "EPISTEMIC_PROGRESSION_SPEC.md"],
    "playtime": ["PLAYTIME_CALIBRATION_SPEC.md"],
    "dm_feeling": ["DM_FEELING_VALIDATOR_SPEC.md"],
}


@dataclass
class ContextPackage:
    stage_id: str
    system_prompt: str
    user_prompt: str
    estimated_tokens: int
    blocked: bool
    block_reason: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "stage_id": self.stage_id,
            "estimated_tokens": self.estimated_tokens,
            "blocked": self.blocked,
            "block_reason": self.block_reason,
        }


def _read_spec_excerpt(spec_name: str, max_chars: int = 4000) -> str:
    path = SPEC_ROOT / spec_name
    if not path.exists():
        return f"(spec {spec_name} not found)"
    text = path.read_text(encoding="utf-8")
    return text[:max_chars]


def build_context(
    stage_id: str,
    brief: dict[str, Any],
    context_budget: int,
    prior_outputs: dict[str, Any] | None = None,
) -> ContextPackage:
    specs = STAGE_SPEC_MAP.get(stage_id, [])
    spec_text = "\n\n".join(_read_spec_excerpt(s) for s in specs)
    prior = prior_outputs or {}

    system_prompt = (
        f"You are generating stage '{stage_id}' for an IDNE adventure. "
        "Respond with machine-readable JSON only. "
        "Do not invent irreversible story changes without approval."
    )
    user_parts = [
        "## Adventure brief (parameters only)",
        str(brief),
        "## Relevant spec excerpts",
        spec_text,
        "## Prior stage summaries",
        str({k: prior.get(k, {}) for k in list(prior.keys())[:5]}),
        f"## Task\nProduce JSON output for stage: {stage_id}",
    ]
    user_prompt = "\n\n".join(user_parts)
    estimated = max(1, (len(system_prompt) + len(user_prompt)) // 4)
    blocked = estimated > context_budget
    return ContextPackage(
        stage_id=stage_id,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        estimated_tokens=estimated,
        blocked=blocked,
        block_reason="context budget exceeded" if blocked else "",
    )
