"""Deterministic prompt builder for Local AI tasks."""

from __future__ import annotations

from idne.local_ai.context_builder import ContextBuildResult
from idne.local_ai.task_model import LocalAITask

SEMANTIC_RESPONSE_FIELDS = (
    "working_title",
    "premise",
    "setting",
    "universe",
    "genre",
    "realism_level",
    "player_mode",
    "investigator_character",
    "opening_situation",
    "initial_observable_facts",
    "tone",
    "difficulty",
    "location_scale",
    "target_playtime_minutes",
    "in_world_duration",
    "content_boundaries",
    "required_themes",
    "forbidden_themes",
    "author_notes",
)

FORBIDDEN_MODEL_ACTIONS = (
    "Do not explore the repository or choose additional files.",
    "Do not assign adventure_id, internal IDs, file paths, or manifest names.",
    "Do not write directly into the repository.",
    "Do not modify protected values supplied by Python.",
    "Do not include chat history.",
    "Do not output markdown fences or commentary outside JSON.",
)


def build_prompt(task: LocalAITask, context: ContextBuildResult) -> str:
    """Build a deterministic model-ready prompt from task and context."""
    semantic_fields = ", ".join(SEMANTIC_RESPONSE_FIELDS)
    protected = "\n".join(f"- {key}: {value}" for key, value in sorted(task.protected_values.items()))
    forbidden = "\n".join(f"- {line}" for line in FORBIDDEN_MODEL_ACTIONS)
    approved_facts = task.approved_prior_stage_facts or {}
    sections = [
        "# IDNE Local AI Task",
        f"Task ID: {task.task_id}",
        f"Task type: {task.task_type}",
        f"Stage: {task.stage_name or '(none)'}",
        "",
        "## Instruction",
        task.task_instruction.strip(),
        "",
        "## Authoritative context",
        context.context_text,
        "",
        "## Approved prior-stage facts",
        str(approved_facts),
        "",
        "## Protected values (Python-owned — do not change)",
        protected or "- (none)",
        "",
        "## Expected output",
        f"Return one JSON object only, conforming to {task.expected_output_schema_ref}.",
        f"Provide semantic values for these response fields: {semantic_fields}.",
        "Python will map your response into the canonical Adventure Generator v2 brief.",
        "",
        "## Explicitly forbidden",
        forbidden,
        "",
        "## Response format",
        "Respond with valid JSON only. No markdown. No prose before or after the JSON object.",
    ]
    return "\n".join(sections).strip() + "\n"
