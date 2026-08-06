"""Tests for Adventure Generator v2 (Milestone 11)."""

from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from idne.generate.brief import load_brief
from idne.generate.context import build_context
from idne.generate.pipeline import GenerationPipeline, invalidate_and_regenerate
from idne.generate.repair import can_auto_repair, would_change_fixed_truth
from idne.generate.stages import STAGE_ORDER
from idne.generate.state import GenerationStateManager
from idne.idne_package import (
    CHECKSUM_NAME,
    build_idne_package,
    read_idne_package,
    verify_extracted_package,
)
from idne.model_adapter.base import ModelConfig, ModelRequest
from idne.model_adapter.mock import build_mock_adapter
from idne.model_adapter.registry import create_adapter
from idne.validate_adventure.runner import validate_adventure

FIXTURES = Path(__file__).resolve().parent / "fixtures"
HARBORVIEW = Path(__file__).resolve().parents[1] / "adventures" / "CASE_BENCHMARK_v0.4"
BRIEF_SOLO = FIXTURES / "gen_v2_brief_solo.json"
BRIEF_TWO = FIXTURES / "gen_v2_brief_two_player.json"


def _first_checksum_covered_adventure_file(extract_dir: Path) -> Path:
    """Return the lexicographically first checksum-covered regular file under adventure/."""
    checksum_path = extract_dir / CHECKSUM_NAME
    if not checksum_path.is_file():
        raise AssertionError(f"missing {CHECKSUM_NAME}")
    covered_adventure_files: list[Path] = []
    for line in checksum_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        _digest, rel_path = line.split("  ", 1)
        if not rel_path.startswith("adventure/"):
            continue
        candidate = extract_dir / rel_path
        if candidate.is_file():
            covered_adventure_files.append(candidate)
    if not covered_adventure_files:
        raise AssertionError("no checksum-covered regular file exists under adventure/")
    return sorted(covered_adventure_files)[0]


class TestAdventureGeneratorV2(unittest.TestCase):
    def _workspace(self) -> Path:
        return Path(tempfile.mkdtemp(prefix="gen_v2_"))

    def test_valid_staged_solo_generation_mock(self):
        ws = self._workspace()
        pipeline = GenerationPipeline(
            ws,
            BRIEF_SOLO,
            model_config={"backend": "mock", "local_mode": True},
            auto_approve=True,
        )
        result = pipeline.run()
        self.assertEqual(result.status, "COMPLETE")
        self.assertEqual(pipeline.manager.state.stage_status["package_export"], "COMPLETE")
        pkg = ws / f"{pipeline.manager.state.adventure_id}.idne"
        self.assertTrue(pkg.exists())

    def test_valid_staged_two_player_generation(self):
        ws = self._workspace()
        pipeline = GenerationPipeline(
            ws,
            BRIEF_TWO,
            model_config={"backend": "mock", "local_mode": True},
            auto_approve=True,
        )
        result = pipeline.run()
        self.assertEqual(result.status, "COMPLETE")

    def test_stage_order_enforcement(self):
        self.assertEqual(STAGE_ORDER[0], "adventure_brief")
        self.assertEqual(STAGE_ORDER[-1], "package_export")
        self.assertIn("story_player", STAGE_ORDER)
        logic_before = STAGE_ORDER.index("capability_checks")
        player_idx = STAGE_ORDER.index("story_player")
        self.assertLess(logic_before, player_idx)

    def test_resume_after_interruption(self):
        ws = self._workspace()
        pipeline = GenerationPipeline(
            ws,
            BRIEF_SOLO,
            model_config={"backend": "mock", "local_mode": True},
            auto_approve=True,
        )
        first = pipeline.run(target_stage="environment")
        self.assertEqual(first.status, "COMPLETE")
        self.assertEqual(pipeline.manager.state.stage_status["objects"], "PENDING")
        second = pipeline.run(resume=True)
        self.assertEqual(second.status, "COMPLETE")
        self.assertEqual(pipeline.manager.state.stage_status["package_export"], "COMPLETE")

    def test_failed_validator_stops_progress(self):
        ws = self._workspace()
        bad_root = ws / "bad_overlays" / "single_investigator" / "fixed_truth"
        shutil.copytree(FIXTURES / "wf_contradictory_timeline", bad_root)
        pipeline = GenerationPipeline(
            ws,
            BRIEF_SOLO,
            model_config={
                "backend": "mock",
                "local_mode": True,
                "extra": {"overlay_root": str(ws / "bad_overlays")},
            },
            auto_approve=True,
        )
        result = pipeline.run(target_stage="fixed_truth")
        self.assertEqual(result.status, "FAIL")
        self.assertEqual(pipeline.manager.state.stage_status["fixed_truth"], "FAILED")

    def test_repair_schema_error(self):
        ws = self._workspace()
        adv = ws / "adventure"
        adv.mkdir(parents=True)
        pkg = adv / "DO_NOT_READ" / "broken.json"
        pkg.parent.mkdir(parents=True)
        pkg.write_text('{"missing_schema": true}', encoding="utf-8")
        from idne.generate.repair import attempt_schema_repair

        finding = {"finding_id": "SCHEMA-MISSING", "severity": "MINOR"}
        self.assertTrue(attempt_schema_repair(pkg, finding))
        data = json.loads(pkg.read_text())
        self.assertEqual(data.get("schema_version"), "1.0")

    def test_repair_cannot_change_fixed_truth(self):
        self.assertTrue(would_change_fixed_truth("culprit_id"))
        self.assertTrue(would_change_fixed_truth("motive"))
        self.assertFalse(can_auto_repair({"finding_id": "CULPRIT-WRONG", "human_approval_needed": True}))

    def test_downstream_invalidation(self):
        ws = self._workspace()
        pipeline = GenerationPipeline(
            ws,
            BRIEF_SOLO,
            model_config={"backend": "mock", "local_mode": True},
            auto_approve=True,
        )
        pipeline.run(target_stage="environment")
        affected = pipeline.manager.invalidate_downstream("fixed_truth", "truth revision")
        self.assertIn("environment", affected)
        self.assertEqual(pipeline.manager.state.stage_status["environment"], "INVALIDATED")

    def test_context_budget_blocked(self):
        brief = load_brief(BRIEF_SOLO)
        ctx = build_context("fixed_truth", brief, context_budget=50)
        self.assertTrue(ctx.blocked)
        adapter = build_mock_adapter(ModelConfig(context_size=50))
        resp = adapter.complete(
            ModelRequest(
                stage_id="fixed_truth",
                system_prompt="x" * 400,
                user_prompt="y" * 400,
            )
        )
        self.assertEqual(resp.status.value, "BLOCKED")

    def test_local_backend_configuration(self):
        adapter = create_adapter(
            {
                "backend": "openai_compatible",
                "local_mode": True,
                "endpoint_url": "http://127.0.0.1:1234",
            }
        )
        self.assertFalse(adapter.config.local_mode is False)
        self.assertEqual(adapter.config.backend, "openai_compatible")

    def test_deterministic_mock_output(self):
        adapter = build_mock_adapter()
        req = ModelRequest(stage_id="environment", system_prompt="s", user_prompt="u")
        a = adapter.complete(req).text
        b = adapter.complete(req).text
        self.assertEqual(a, b)

    def test_player_blocked_before_logic_validation(self):
        ws = self._workspace()
        pipeline = GenerationPipeline(
            ws,
            BRIEF_SOLO,
            model_config={"backend": "mock", "local_mode": True},
            auto_approve=True,
        )
        pipeline.manager.state.logic_validation_complete = False
        pipeline.manager.state.stage_status["story_player"] = "PENDING"
        for s in STAGE_ORDER:
            if s != "story_player":
                pipeline.manager.state.stage_status[s] = "COMPLETE"
        pipeline.manager.save()
        result = pipeline._run_stage("story_player")
        self.assertEqual(result.status, "BLOCKED")

    def test_severe_playtime_mismatch_blocks_readiness(self):
        ws = self._workspace()
        shutil.copytree(FIXTURES / "gen_v2_canonical_solo", ws / "adventure")
        shutil.copy2(
            FIXTURES / "pt_solo_30_min_content" / "playtime_calibration_manifest.json",
            ws / "adventure" / "playtime_calibration_manifest.json",
        )
        shutil.copy2(
            FIXTURES / "pt_solo_30_min_content" / "DO_NOT_READ" / "playtime_calibration_package.json",
            ws / "adventure" / "DO_NOT_READ" / "playtime_calibration_package.json",
        )
        from idne.generate.stage_validate import run_stage_validator

        val = run_stage_validator("playtime", ws / "adventure")
        self.assertEqual(val.get("status"), "FAIL")

    def test_missing_tier_bc_prevents_adventure_ready(self):
        ws = self._workspace()
        pipeline = GenerationPipeline(
            ws,
            BRIEF_SOLO,
            model_config={"backend": "mock", "local_mode": True},
            auto_approve=True,
        )
        pipeline._evaluate_readiness(
            "dm_feeling",
            {"status": "PASS", "tier_b_pending": ["agency"], "tier_c_complete": False},
        )
        self.assertEqual(pipeline.manager.state.readiness_status, "TIER_BC_INCOMPLETE")

    def test_package_export_and_import(self):
        ws = self._workspace()
        adv = FIXTURES / "gen_v2_canonical_solo"
        out = ws / "test.idne"
        build_idne_package(adv, out, "GEN-V2-TEST")
        extract = ws / "extracted"
        result = read_idne_package(out, extract)
        self.assertEqual(result.status, "PASS")
        self.assertTrue(result.checksum_valid)
        self.assertTrue((extract / "adventure").exists())

    def test_broken_package_checksum(self):
        ws = self._workspace()
        adv = FIXTURES / "gen_v2_canonical_solo"
        out = ws / "broken.idne"
        build_idne_package(adv, out, "GEN-V2-BROKEN")
        extract = ws / "extracted"
        result = read_idne_package(out, extract)
        self.assertTrue(result.checksum_valid)
        target = _first_checksum_covered_adventure_file(extract)
        target.write_bytes(b"corrupted-content")
        self.assertFalse(verify_extracted_package(extract))

    def test_integrated_validation_command(self):
        res = validate_adventure(FIXTURES / "gen_v2_canonical_solo")
        self.assertEqual(res.status, "PASS")

    def test_legacy_adventure_skipped_not_passed(self):
        if not HARBORVIEW.exists():
            self.skipTest("Harborview not in workspace")
        res = validate_adventure(HARBORVIEW)
        self.assertEqual(res.status, "SKIP")

    def test_no_internet_dependency_local_mode(self):
        adapter = build_mock_adapter(ModelConfig(local_mode=True))
        self.assertFalse(adapter.requires_network())
        cloud = create_adapter({"backend": "cloud", "local_mode": False, "endpoint_url": "http://example.com"})
        self.assertTrue(cloud.requires_network())

    def test_human_approval_gate_without_auto(self):
        ws = self._workspace()
        pipeline = GenerationPipeline(
            ws,
            BRIEF_SOLO,
            model_config={"backend": "mock", "local_mode": True},
            auto_approve=False,
        )
        result = pipeline.run(target_stage="adventure_brief")
        self.assertEqual(result.status, "AWAITING_APPROVAL")


if __name__ == "__main__":
    unittest.main()
