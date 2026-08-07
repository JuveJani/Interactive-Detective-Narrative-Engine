"""Regression tests for Local AI semantic → canonical brief structured mapping."""

from __future__ import annotations

import json
import shutil
import unittest
from pathlib import Path

from idne.generate.brief import load_brief, validate_brief
from idne.local_ai.mock_adapter import _semantic_payload
from idne.local_ai.proposal_builder import map_semantic_to_canonical
from idne.local_ai.process import process_task
from idne.local_ai.task_builder import prepare_task
from idne.local_ai.transport import run_task

REPO_ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_INPUT = "OFFLINE_AI/examples/adventure_brief_input.md"
LEGACY_BRIEF = REPO_ROOT / "tests/fixtures/gen_v2_brief_solo.json"
DRAFT_OUTPUT = "adventures/_local_ai_drafts/mapping_test/adventure_brief.json"


def _valid_semantic() -> dict:
    return _semantic_payload("mappingtest1234")


def _fresh_prepare():
    from idne.local_ai.paths import normalize_allowlist, resolve_allowed_file, safe_task_directory_name
    from idne.local_ai.platform_runtime import local_ai_runs_root
    from idne.local_ai.task_model import make_task_id, sha256_bytes

    input_bytes = resolve_allowed_file(EXAMPLE_INPUT, REPO_ROOT).read_bytes()
    allowed = normalize_allowlist([EXAMPLE_INPUT], REPO_ROOT)
    task_id = make_task_id("adventure_brief", allowed, [sha256_bytes(input_bytes)], [DRAFT_OUTPUT])
    run_dir = local_ai_runs_root(REPO_ROOT) / safe_task_directory_name(task_id)
    if run_dir.exists():
        shutil.rmtree(run_dir)
    return prepare_task(
        "adventure_brief",
        EXAMPLE_INPUT,
        repo_root=REPO_ROOT,
        output_path=DRAFT_OUTPUT,
    )


class TestStructuredBriefMapping(unittest.TestCase):
    def test_premise_remains_machine_readable(self):
        semantic = _valid_semantic()
        canonical = map_semantic_to_canonical(semantic)
        self.assertEqual(canonical["premise"], semantic["premise"])

    def test_setting_remains_machine_readable(self):
        semantic = _valid_semantic()
        canonical = map_semantic_to_canonical(semantic)
        self.assertEqual(canonical["setting"], semantic["setting"])

    def test_opening_situation_remains_machine_readable(self):
        semantic = _valid_semantic()
        canonical = map_semantic_to_canonical(semantic)
        self.assertEqual(canonical["opening_situation"], semantic["opening_situation"])

    def test_initial_observable_facts_remain_structured_list(self):
        semantic = _valid_semantic()
        canonical = map_semantic_to_canonical(semantic)
        self.assertIsInstance(canonical["initial_observable_facts"], list)
        self.assertEqual(canonical["initial_observable_facts"], semantic["initial_observable_facts"])

    def test_author_notes_contains_only_actual_author_notes(self):
        semantic = _valid_semantic()
        canonical = map_semantic_to_canonical(semantic)
        self.assertEqual(canonical["author_notes"], semantic["author_notes"])
        notes = canonical["author_notes"]
        self.assertNotIn("Premise:", notes)
        self.assertNotIn("Setting:", notes)
        self.assertNotIn("Opening situation:", notes)
        self.assertNotIn("Initial observable facts:", notes)
        self.assertNotIn(semantic["premise"], notes)

    def test_author_notes_omitted_when_semantic_author_notes_missing(self):
        semantic = _valid_semantic()
        del semantic["author_notes"]
        canonical = map_semantic_to_canonical(semantic)
        self.assertNotIn("author_notes", canonical)

    def test_no_semantic_information_silently_dropped(self):
        semantic = _valid_semantic()
        canonical = map_semantic_to_canonical(semantic)
        for key in (
            "working_title",
            "premise",
            "setting",
            "opening_situation",
            "initial_observable_facts",
            "universe",
            "required_themes",
            "forbidden_themes",
        ):
            self.assertEqual(canonical[key], semantic[key], key)
        self.assertEqual(canonical["author_notes"], semantic["author_notes"])

    def test_proposal_validation_accepts_structured_representation(self):
        _task, _, _, _, run_dir = _fresh_prepare()
        run_task(run_dir, mock=True)
        process_result = process_task(run_dir)
        self.assertTrue(process_result.success, process_result.details)
        proposal_report = json.loads(
            (run_dir / "proposal/validation_report.json").read_text(encoding="utf-8")
        )
        self.assertTrue(proposal_report["passed"], proposal_report.get("findings"))
        brief = json.loads((run_dir / "proposal/adventure_brief.json").read_text(encoding="utf-8"))
        self.assertIn("premise", brief)
        self.assertNotIn("Premise:", brief.get("author_notes", ""))

    def test_existing_valid_briefs_remain_compatible(self):
        legacy = load_brief(LEGACY_BRIEF)
        self.assertEqual(validate_brief(legacy), [])

    def test_mock_uses_same_deterministic_mapping_as_direct_call(self):
        _task, _, _, _, run_dir = _fresh_prepare()
        run_task(run_dir, mock=True)
        process_task(run_dir)
        parsed = json.loads((run_dir / "parsed_response.json").read_text(encoding="utf-8"))
        direct = map_semantic_to_canonical(parsed)
        built = json.loads((run_dir / "proposal/adventure_brief.json").read_text(encoding="utf-8"))
        self.assertEqual(built, direct)


if __name__ == "__main__":
    unittest.main()
