"""Adventure Generator v2 staged pipeline."""

from __future__ import annotations

import json
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from idne.generate.brief import brief_play_mode, load_brief, validate_brief
from idne.generate.context import build_context
from idne.generate.repair import attempt_schema_repair, can_auto_repair, repair_request_payload
from idne.generate.reports import write_all_reports
from idne.generate.stage_validate import has_critical_or_major, run_stage_validator
from idne.generate.stages import LOGIC_STAGES, STAGE_DEFINITIONS, STAGE_ORDER
from idne.generate.state import GenerationStateManager
from idne.idne_package import build_idne_package
from idne.model_adapter.base import ModelRequest, ModelResultStatus
from idne.model_adapter.mock import MockModelAdapter
from idne.model_adapter.registry import create_adapter


@dataclass
class PipelineResult:
    status: str
    last_stage: str = ""
    message: str = ""
    state_path: str = ""
    errors: list[str] = field(default_factory=list)


class GenerationPipeline:
    def __init__(
        self,
        workspace_root: Path,
        brief_path: Path,
        model_config: dict[str, Any] | None = None,
        auto_approve: bool = False,
        max_repair_attempts: int = 2,
    ) -> None:
        self.workspace_root = workspace_root.resolve()
        self.brief_path = brief_path.resolve()
        self.brief = load_brief(self.brief_path)
        self.play_mode = brief_play_mode(self.brief)
        self.manager = GenerationStateManager(self.workspace_root)
        self.adapter = create_adapter(model_config or {"backend": "mock", "local_mode": True})
        self.auto_approve = auto_approve
        self.max_repair_attempts = max_repair_attempts
        self.adventure_root = self.manager.adventure_root
        self.adventure_root.mkdir(parents=True, exist_ok=True)

        self.manager.state.model_metadata = self.adapter.config.to_dict()
        self.manager.save()

    def run(
        self,
        resume: bool = False,
        target_stage: str | None = None,
    ) -> PipelineResult:
        brief_errors = validate_brief(self.brief)
        if brief_errors:
            return PipelineResult(status="FAIL", errors=brief_errors)

        start_idx = 0
        if resume and self.manager.state.checkpoint_stage:
            try:
                start_idx = STAGE_ORDER.index(self.manager.state.checkpoint_stage)
            except ValueError:
                start_idx = 0

        end_idx = len(STAGE_ORDER) - 1
        if target_stage:
            end_idx = STAGE_ORDER.index(target_stage)

        for stage_id in STAGE_ORDER[start_idx:end_idx + 1]:
            result = self._run_stage(stage_id)
            if result.status != "COMPLETE":
                write_all_reports(self.workspace_root, self.manager.state)
                return result

        write_all_reports(self.workspace_root, self.manager.state)
        return PipelineResult(
            status="COMPLETE",
            last_stage=STAGE_ORDER[end_idx],
            state_path=str(self.manager.state_path),
        )

    def _run_stage(self, stage_id: str) -> PipelineResult:
        defn = STAGE_DEFINITIONS[stage_id]
        current = self.manager.state.stage_status.get(stage_id, "PENDING")

        if current == "COMPLETE" and not self.manager.state.invalidated_stages:
            return PipelineResult(status="COMPLETE", last_stage=stage_id)

        if defn.requires_logic_complete and not self.manager.state.logic_validation_complete:
            self.manager.set_stage_status(stage_id, "BLOCKED")
            return PipelineResult(
                status="BLOCKED",
                last_stage=stage_id,
                message="PLAYER generation blocked until logic validation passes",
            )

        if self.manager.needs_approval(stage_id) and not self.auto_approve:
            self.manager.set_stage_status(stage_id, "AWAITING_APPROVAL")
            return PipelineResult(
                status="AWAITING_APPROVAL",
                last_stage=stage_id,
                message=f"human approval required for {stage_id}",
            )

        if self.auto_approve and defn.requires_human_approval:
            self.manager.approve(stage_id, approver="auto_test")

        self.manager.set_stage_status(stage_id, "RUNNING")

        if stage_id == "adventure_brief":
            return self._complete_brief_stage(stage_id)

        stage_output_dir = self.workspace_root / ".generation" / "stages" / stage_id
        stage_output_dir.mkdir(parents=True, exist_ok=True)

        context_budget = int(self.adapter.config.context_size)
        ctx = build_context(stage_id, self.brief, context_budget)
        self.manager.state.token_estimates[stage_id] = ctx.to_dict()
        self.manager.save()

        if ctx.blocked:
            self.manager.set_stage_status(stage_id, "BLOCKED")
            return PipelineResult(
                status="BLOCKED",
                last_stage=stage_id,
                message=ctx.block_reason,
            )

        model_resp = self.adapter.complete(
            ModelRequest(
                stage_id=stage_id,
                system_prompt=ctx.system_prompt,
                user_prompt=ctx.user_prompt,
                metadata={"play_mode": self.play_mode, "brief": self.brief},
            )
        )

        if model_resp.status == ModelResultStatus.BLOCKED:
            self.manager.set_stage_status(stage_id, "BLOCKED")
            return PipelineResult(status="BLOCKED", last_stage=stage_id, message=model_resp.error)

        if model_resp.status != ModelResultStatus.SUCCESS:
            self.manager.set_stage_status(stage_id, "FAILED")
            return PipelineResult(
                status="FAIL",
                last_stage=stage_id,
                message=model_resp.error or "model error",
            )

        output_path = stage_output_dir / "model_response.json"
        output_path.write_text(model_resp.text, encoding="utf-8")
        self.manager.record_output_hash(stage_id, output_path)

        if isinstance(self.adapter, MockModelAdapter):
            applied = self.adapter.apply_overlay(stage_id, self.play_mode, self.adventure_root)
            overlay_record = stage_output_dir / "applied_files.json"
            overlay_record.write_text(json.dumps(applied, indent=2), encoding="utf-8")

        if stage_id == "package_export":
            return self._export_package(stage_id)

        val_result = run_stage_validator(defn.validator_name, self.adventure_root)
        self.manager.record_validator(stage_id, val_result)

        if val_result.get("skipped"):
            self._mark_logic_if_needed(stage_id)
            self.manager.set_stage_status(stage_id, "COMPLETE")
            return PipelineResult(status="COMPLETE", last_stage=stage_id)

        status = val_result.get("status", "FAIL")
        findings = val_result.get("findings", [])
        errors = val_result.get("errors", [])

        if status in ("FAIL", "BLOCKED") or has_critical_or_major(findings, errors):
            repaired = self._attempt_repair(stage_id, val_result)
            if repaired:
                val_result = run_stage_validator(defn.validator_name, self.adventure_root)
                self.manager.record_validator(stage_id, val_result)
                status = val_result.get("status", "FAIL")
                findings = val_result.get("findings", [])
                errors = val_result.get("errors", [])

            if status in ("FAIL", "BLOCKED") or has_critical_or_major(findings, errors):
                self.manager.set_stage_status(stage_id, "FAILED")
                return PipelineResult(
                    status="FAIL",
                    last_stage=stage_id,
                    message=f"validator {defn.validator_name} failed",
                    errors=errors,
                )

        self._evaluate_readiness(stage_id, val_result)
        self.manager.set_stage_status(stage_id, "COMPLETE")
        self._mark_logic_if_needed(stage_id)
        return PipelineResult(status="COMPLETE", last_stage=stage_id)

    def _complete_brief_stage(self, stage_id: str) -> PipelineResult:
        brief_dir = self.workspace_root / "brief"
        brief_dir.mkdir(parents=True, exist_ok=True)
        dest = brief_dir / "adventure_brief.json"
        dest.write_text(json.dumps(self.brief, indent=2), encoding="utf-8")
        self.manager.record_output_hash(stage_id, dest)
        self.manager.set_stage_status(stage_id, "COMPLETE")
        return PipelineResult(status="COMPLETE", last_stage=stage_id)

    def _attempt_repair(self, stage_id: str, val_result: dict[str, Any]) -> bool:
        findings = val_result.get("findings", [])
        repair_payload = repair_request_payload(stage_id, findings, {"brief": self.brief})
        self.manager.record_repair(repair_payload)

        attempts = 0
        changed = False
        for finding in findings:
            if not can_auto_repair(finding):
                continue
            if attempts >= self.max_repair_attempts:
                break
            for pkg in self.adventure_root.rglob("*.json"):
                if attempt_schema_repair(pkg, finding):
                    changed = True
                    attempts += 1
        return changed

    def _mark_logic_if_needed(self, stage_id: str) -> None:
        if stage_id in LOGIC_STAGES:
            logic_stages = [s for s in STAGE_ORDER if s in LOGIC_STAGES]
            if all(
                self.manager.state.stage_status.get(s) == "COMPLETE"
                for s in logic_stages
            ):
                self.manager.state.logic_validation_complete = True
                self.manager.save()

    def _evaluate_readiness(self, stage_id: str, val_result: dict[str, Any]) -> None:
        if stage_id == "playtime" and val_result.get("status") == "FAIL":
            self.manager.state.readiness_status = "PLAYTIME_MISMATCH"
            self.manager.save()
        if stage_id == "dm_feeling":
            tier_b = val_result.get("tier_b_pending", [])
            tier_c = val_result.get("tier_c_complete", False)
            if tier_b or not tier_c:
                self.manager.state.readiness_status = "TIER_BC_INCOMPLETE"
                self.manager.save()
        if stage_id == "final_validation":
            integrated_status = val_result.get("status", "FAIL")
            if integrated_status == "PASS":
                if self.manager.state.readiness_status == "IN_PROGRESS":
                    self.manager.state.readiness_status = "PRE_PLAYTEST"
            else:
                self.manager.state.readiness_status = "VALIDATION_FAILED"
            self.manager.save()

    def _export_package(self, stage_id: str) -> PipelineResult:
        package_path = self.workspace_root / f"{self.manager.state.adventure_id}.idne"
        build_idne_package(
            self.adventure_root,
            package_path,
            self.manager.state.adventure_id,
            extra_roots={
                "generation": self.workspace_root / ".generation",
                "brief": self.workspace_root / "brief",
            },
        )
        self.manager.set_stage_status(stage_id, "COMPLETE")
        return PipelineResult(status="COMPLETE", last_stage=stage_id)


def invalidate_and_regenerate(
    workspace_root: Path,
    from_stage: str,
    reason: str,
    pipeline: GenerationPipeline,
) -> PipelineResult:
    manager = pipeline.manager
    affected = manager.invalidate_downstream(from_stage, reason)
    for s in affected:
        manager.state.stage_status[s] = "PENDING"
    manager.save()
    return pipeline.run(resume=True)
