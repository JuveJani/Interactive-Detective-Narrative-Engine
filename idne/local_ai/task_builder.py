"""Task definitions and deterministic task preparation."""

from __future__ import annotations

import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from idne.local_ai.context_builder import (
    AuthoritativeFileSpec,
    ContextBuildResult,
    build_context_package,
)
from idne.local_ai.output_paths import DEFAULT_BRIEF_OUTPUT, validate_output_path
from idne.local_ai.paths import normalize_allowlist, normalize_repo_relative, resolve_allowed_file, to_posix_relpath
from idne.local_ai.platform_runtime import detect_platform_runtime
from idne.local_ai.prompt_builder import build_prompt
from idne.local_ai.run_state import (
    PreparationMetrics,
    has_active_model_artifacts,
    load_status,
    load_task,
    reload_prepared_task,
    run_directory_for_task,
    write_run_artifacts,
)
from idne.local_ai.task_model import (
    LocalAITask,
    SourceIdentity,
    TaskStatus,
    make_task_id,
    sha256_bytes,
    stable_run_identity,
    utc_now_iso,
)


@dataclass(frozen=True)
class TaskDefinition:
    task_type: str
    stage_name: str
    authoritative_files: tuple[AuthoritativeFileSpec, ...]
    allowed_output_files: tuple[str, ...]
    expected_output_schema_ref: str
    context_budget: int
    validator_commands: tuple[str, ...]
    task_instruction: str


ADVENTURE_BRIEF_TASK = TaskDefinition(
    task_type="adventure_brief",
    stage_name="adventure_brief",
    authoritative_files=(
        AuthoritativeFileSpec(
            path="ADVENTURE_GENERATOR_V2_SPEC.md",
            authority_rank=1,
            kind="specification",
            excerpt_start="## 4. Human approval gates",
            excerpt_end="## 5. Model adapter",
        ),
        AuthoritativeFileSpec(
            path="ADVENTURE_GENERATOR_V2_SCHEMA.md",
            authority_rank=1,
            kind="specification",
            excerpt_start="## 1. Adventure brief",
            excerpt_end="## 2. Generation state",
        ),
        AuthoritativeFileSpec(
            path="ADVENTURE_GENERATOR_V2_WORKFLOW.md",
            authority_rank=2,
            kind="workflow",
            excerpt_start="## 2. Author brief",
            excerpt_end="## 3. Run generation",
        ),
        AuthoritativeFileSpec(
            path="AGENTS.md",
            authority_rank=1,
            kind="specification",
            excerpt_start="## Generator v2 workflow",
            excerpt_end="## Validation and Simulator v2",
        ),
    ),
    allowed_output_files=(DEFAULT_BRIEF_OUTPUT,),
    expected_output_schema_ref="idne/schemas/local_ai_adventure_brief_response.schema.json",
    context_budget=12000,
    validator_commands=(
        f"python -m idne.generate.brief <{DEFAULT_BRIEF_OUTPUT}>",
    ),
    task_instruction=(
        "Transform the author input into a semantic adventure brief response JSON object. "
        "Provide premise, opening situation, and brief parameters only. "
        "Do not write story prose, spoilers, culprit details, or deterministic metadata. "
        "Python will assign IDs, paths, and manifests later."
    ),
)


TASK_DEFINITIONS: dict[str, TaskDefinition] = {
    "adventure_brief": ADVENTURE_BRIEF_TASK,
}


class TaskPreparationError(RuntimeError):
    pass


def _resolve_input_path(input_arg: str, repo_root: Path) -> str:
    rel = normalize_repo_relative(input_arg, repo_root)
    resolve_allowed_file(rel, repo_root)
    return rel


def _assert_existing_run_compatible(
    run_dir: Path,
    *,
    output_rel: str,
    run_definition_identity: str,
) -> LocalAITask | None:
    """Return existing task when prepare is idempotent; raise on incompatible reuse."""
    task_path = run_dir / "task.json"
    if not task_path.is_file():
        return None
    existing = load_task(run_dir)
    if existing.allowed_output_files != [output_rel]:
        raise TaskPreparationError(
            "run directory already exists for a different output destination: "
            f"expected {output_rel}, found {existing.allowed_output_files[0]}"
        )
    if has_active_model_artifacts(run_dir) and existing.status == TaskStatus.READY_FOR_MODEL:
        raise TaskPreparationError(
            "inconsistent run state: response artifacts present while task status is READY_FOR_MODEL"
        )
    status_path = run_dir / "status.json"
    if status_path.is_file():
        status = load_status(run_dir)
        stored_identity = status.get("run_definition_identity")
        if stored_identity and stored_identity != run_definition_identity:
            raise TaskPreparationError("run directory run_definition_identity mismatch")
        stored_outputs = status.get("allowed_output_files")
        if stored_outputs and stored_outputs != [output_rel]:
            raise TaskPreparationError("run directory allowed_output_files mismatch")
    return existing


def prepare_task(
    task_type: str,
    input_path: str,
    *,
    repo_root: Path | None = None,
    context_budget: int | None = None,
    output_path: str | None = None,
) -> tuple[LocalAITask, ContextBuildResult, str, PreparationMetrics, Path]:
    runtime = detect_platform_runtime(repo_root)
    root = runtime.repo_root
    definition = TASK_DEFINITIONS.get(task_type)
    if definition is None:
        raise TaskPreparationError(f"unsupported task type: {task_type}")

    input_rel = _resolve_input_path(input_path, root)
    input_abs = resolve_allowed_file(input_rel, root)
    input_bytes = input_abs.read_bytes()
    input_hash = sha256_bytes(input_bytes)

    allowed_inputs = normalize_allowlist([input_rel], root)
    output_rel = validate_output_path(output_path or DEFAULT_BRIEF_OUTPUT, root)
    allowed_outputs = [output_rel]
    run_definition_identity = stable_run_identity(
        task_type, allowed_inputs, [input_hash], allowed_outputs
    )
    task_id = make_task_id(task_type, allowed_inputs, [input_hash], allowed_outputs)
    run_dir = run_directory_for_task(root, task_id)
    run_rel = to_posix_relpath(run_dir, root)

    existing = _assert_existing_run_compatible(
        run_dir,
        output_rel=output_rel,
        run_definition_identity=run_definition_identity,
    )
    if existing is not None:
        return reload_prepared_task(run_dir)

    task = LocalAITask(
        schema_version="1.0",
        task_id=task_id,
        task_type=task_type,
        stage_name=definition.stage_name,
        adventure_id=None,
        created_at=utc_now_iso(),
        source_content_identity=SourceIdentity(sha256=input_hash, path=input_rel),
        allowed_input_files=allowed_inputs,
        allowed_output_files=allowed_outputs,
        authoritative_sources=[],
        approved_prior_stage_facts={},
        protected_values={
            "task_id": task_id,
            "stage_name": definition.stage_name,
            "python_assigns": [
                "adventure_id",
                "brief_version",
                "file_paths",
                "manifest_names",
                "internal_ids",
            ],
        },
        expected_output_schema_ref=definition.expected_output_schema_ref,
        context_budget=context_budget or definition.context_budget,
        generation_settings={
            "backend": None,
            "model_name": None,
            "temperature": 0.1,
            "max_output_tokens": 2048,
            "local_mode": True,
        },
        validator_commands=[f"python -m idne.generate.brief <{output_rel}>"],
        status=TaskStatus.CREATED,
        attempt_count=0,
        run_directory=run_rel,
        task_instruction=definition.task_instruction,
    )

    start = time.perf_counter()
    context = build_context_package(
        root,
        allowed_inputs,
        list(definition.authoritative_files),
        context_budget=task.context_budget,
    )
    elapsed = time.perf_counter() - start

    if context.blocked:
        task.status = TaskStatus.BLOCKED
        prompt = ""
        metrics = PreparationMetrics(
            files_read=context.files_read,
            bytes_read=context.bytes_read,
            character_count=context.character_count,
            approximate_tokens=context.approximate_tokens,
            context_budget=task.context_budget,
            preparation_seconds=elapsed,
            status=task.status.value,
        )
        diagnostics = {
            "blocked": True,
            "reason": context.block_reason,
            "overflow_source": context.overflow_source,
            "authoritative_files": [spec.path for spec in definition.authoritative_files],
        }
        write_run_artifacts(
            run_dir,
            task,
            context,
            prompt,
            metrics,
            diagnostics,
            run_definition_identity=run_definition_identity,
        )
        raise TaskPreparationError(context.block_reason)

    task.authoritative_sources = list(context.authoritative_sources)
    task.status = TaskStatus.PREPARED
    prompt = build_prompt(task, context)
    task.status = TaskStatus.READY_FOR_MODEL

    metrics = PreparationMetrics(
        files_read=context.files_read,
        bytes_read=context.bytes_read,
        character_count=context.character_count,
        approximate_tokens=context.approximate_tokens,
        context_budget=task.context_budget,
        preparation_seconds=elapsed,
        status=task.status.value,
    )
    diagnostics = {
        "blocked": False,
        "files_included": [input_rel] + [spec.path for spec in definition.authoritative_files],
        "authoritative_files": [src.path for src in task.authoritative_sources],
        "preparation_seconds": elapsed,
    }
    write_run_artifacts(
        run_dir,
        task,
        context,
        prompt,
        metrics,
        diagnostics,
        run_definition_identity=run_definition_identity,
    )
    return task, context, prompt, metrics, run_dir
