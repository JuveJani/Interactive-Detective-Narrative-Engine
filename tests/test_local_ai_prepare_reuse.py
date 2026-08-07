"""Regression tests for Local AI prepare reuse and run identity."""

from __future__ import annotations

import json
import shutil
import unittest
from pathlib import Path

from idne.local_ai.apply import apply_proposal
from idne.local_ai.attempts import list_attempts
from idne.local_ai.output_paths import DEFAULT_BRIEF_OUTPUT
from idne.local_ai.process import process_task
from idne.local_ai.run_state import load_status, load_task, write_json
from idne.local_ai.task_builder import prepare_task
from idne.local_ai.task_model import TaskStatus, make_task_id, stable_run_identity
from idne.local_ai.transport import run_task

REPO_ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_INPUT = "OFFLINE_AI/examples/adventure_brief_input.md"
OUTPUT_A = "adventures/_local_ai_drafts/reuse_test_a/adventure_brief.json"
OUTPUT_B = "adventures/_local_ai_drafts/reuse_test_b/adventure_brief.json"


def _cleanup_run_dirs(outputs: tuple[str, ...]) -> None:
    from idne.local_ai.paths import normalize_allowlist, resolve_allowed_file, safe_task_directory_name
    from idne.local_ai.platform_runtime import local_ai_runs_root
    from idne.local_ai.task_model import make_task_id, sha256_bytes

    input_bytes = resolve_allowed_file(EXAMPLE_INPUT, REPO_ROOT).read_bytes()
    allowed = normalize_allowlist([EXAMPLE_INPUT], REPO_ROOT)
    input_hash = sha256_bytes(input_bytes)
    for output in outputs:
        task_id = make_task_id("adventure_brief", allowed, [input_hash], [output])
        run_dir = local_ai_runs_root(REPO_ROOT) / safe_task_directory_name(task_id)
        if run_dir.exists():
            shutil.rmtree(run_dir)


def _cleanup_outputs() -> None:
    for rel in (OUTPUT_A, OUTPUT_B, DEFAULT_BRIEF_OUTPUT):
        path = REPO_ROOT / rel
        sidecar = path.with_suffix(".json.local_ai_applied")
        for candidate in (path, sidecar):
            if candidate.is_file():
                candidate.unlink()
        parent = path.parent
        if parent.is_dir() and not any(parent.iterdir()):
            parent.rmdir()


class TestPrepareReuseIdentity(unittest.TestCase):
    def setUp(self):
        _cleanup_run_dirs((OUTPUT_A, OUTPUT_B))

    def tearDown(self):
        _cleanup_run_dirs((OUTPUT_A, OUTPUT_B))
        _cleanup_outputs()

    def test_same_input_and_output_prepare_twice_does_not_reset_response_received(self):
        _task, _, _, _, run_dir = prepare_task(
            "adventure_brief",
            EXAMPLE_INPUT,
            repo_root=REPO_ROOT,
            output_path=OUTPUT_A,
        )
        run_task(run_dir, mock=True)
        task_after_run = load_task(run_dir)
        self.assertEqual(task_after_run.status, TaskStatus.RESPONSE_RECEIVED)

        task2, _, _, _, run_dir2 = prepare_task(
            "adventure_brief",
            EXAMPLE_INPUT,
            repo_root=REPO_ROOT,
            output_path=OUTPUT_A,
        )
        self.assertEqual(run_dir2, run_dir)
        self.assertEqual(task2.status, TaskStatus.RESPONSE_RECEIVED)
        self.assertTrue((run_dir / "response.txt").is_file())

    def test_same_input_and_output_prepare_twice_does_not_reset_validated(self):
        _task, _, _, _, run_dir = prepare_task(
            "adventure_brief",
            EXAMPLE_INPUT,
            repo_root=REPO_ROOT,
            output_path=OUTPUT_A,
        )
        run_task(run_dir, mock=True)
        process_task(run_dir)
        self.assertEqual(load_task(run_dir).status, TaskStatus.VALIDATED)

        task2, _, _, _, run_dir2 = prepare_task(
            "adventure_brief",
            EXAMPLE_INPUT,
            repo_root=REPO_ROOT,
            output_path=OUTPUT_A,
        )
        self.assertEqual(run_dir2, run_dir)
        self.assertEqual(task2.status, TaskStatus.VALIDATED)
        self.assertEqual(load_status(run_dir).get("processing_stage"), "VALIDATED")

    def test_different_output_creates_distinct_task_and_run_directory(self):
        _task_a, _, _, _, run_dir_a = prepare_task(
            "adventure_brief",
            EXAMPLE_INPUT,
            repo_root=REPO_ROOT,
            output_path=OUTPUT_A,
        )
        _task_b, _, _, _, run_dir_b = prepare_task(
            "adventure_brief",
            EXAMPLE_INPUT,
            repo_root=REPO_ROOT,
            output_path=OUTPUT_B,
        )
        self.assertNotEqual(run_dir_a, run_dir_b)
        self.assertNotEqual(_task_a.task_id, _task_b.task_id)
        self.assertEqual(_task_a.allowed_output_files, [OUTPUT_A])
        self.assertEqual(_task_b.allowed_output_files, [OUTPUT_B])

    def test_output_path_participates_in_execution_identity(self):
        from idne.local_ai.paths import normalize_allowlist, resolve_allowed_file
        from idne.local_ai.task_model import sha256_bytes

        input_bytes = resolve_allowed_file(EXAMPLE_INPUT, REPO_ROOT).read_bytes()
        allowed = normalize_allowlist([EXAMPLE_INPUT], REPO_ROOT)
        input_hash = sha256_bytes(input_bytes)
        id_a = make_task_id("adventure_brief", allowed, [input_hash], [OUTPUT_A])
        id_b = make_task_id("adventure_brief", allowed, [input_hash], [OUTPUT_B])
        self.assertNotEqual(id_a, id_b)
        run_a = stable_run_identity("adventure_brief", allowed, [input_hash], [OUTPUT_A])
        run_b = stable_run_identity("adventure_brief", allowed, [input_hash], [OUTPUT_B])
        self.assertNotEqual(run_a, run_b)

    def test_response_artifacts_cannot_coexist_with_ready_for_model_after_prepare(self):
        _task, _, _, _, run_dir = prepare_task(
            "adventure_brief",
            EXAMPLE_INPUT,
            repo_root=REPO_ROOT,
            output_path=OUTPUT_A,
        )
        run_task(run_dir, mock=True)
        task = load_task(run_dir)
        task.status = TaskStatus.READY_FOR_MODEL
        write_json(run_dir / "task.json", task.to_dict())
        status = load_status(run_dir)
        status["status"] = TaskStatus.READY_FOR_MODEL.value
        write_json(run_dir / "status.json", status)

        from idne.local_ai.task_builder import TaskPreparationError

        with self.assertRaises(TaskPreparationError):
            prepare_task(
                "adventure_brief",
                EXAMPLE_INPUT,
                repo_root=REPO_ROOT,
                output_path=OUTPUT_A,
            )

    def test_old_attempts_remain_preserved_on_force_rerun(self):
        _task, _, _, _, run_dir = prepare_task(
            "adventure_brief",
            EXAMPLE_INPUT,
            repo_root=REPO_ROOT,
            output_path=OUTPUT_A,
        )
        run_task(run_dir, mock=True)
        run_task(run_dir, mock=True, force=True)
        attempts = list_attempts(run_dir)
        self.assertEqual(len(attempts), 1)
        self.assertTrue((run_dir / "attempts" / "001" / "response.txt").is_file())

    def test_process_rejects_response_for_different_task_definition(self):
        _task, _, _, _, run_dir = prepare_task(
            "adventure_brief",
            EXAMPLE_INPUT,
            repo_root=REPO_ROOT,
            output_path=OUTPUT_A,
        )
        run_task(run_dir, mock=True)
        task = load_task(run_dir)
        task.allowed_output_files = [OUTPUT_B]
        write_json(run_dir / "task.json", task.to_dict())

        result = process_task(run_dir)
        self.assertFalse(result.success)
        self.assertEqual(result.stopped_at, "parse")
        self.assertEqual(result.details.get("code"), "definition_mismatch")

    def test_mock_end_to_end_two_timestamped_outputs(self):
        drafts: list[Path] = []
        for output in (OUTPUT_A, OUTPUT_B):
            _task, _, _, _, run_dir = prepare_task(
                "adventure_brief",
                EXAMPLE_INPUT,
                repo_root=REPO_ROOT,
                output_path=output,
            )
            run_task(run_dir, mock=True)
            result = process_task(run_dir)
            self.assertTrue(result.success, result.details)
            apply_proposal(run_dir)
            draft = REPO_ROOT / output
            drafts.append(draft)
            self.assertTrue(draft.is_file())
            self.assertEqual(load_task(run_dir).status, TaskStatus.APPLIED)
        self.assertNotEqual(drafts[0], drafts[1])


if __name__ == "__main__":
    unittest.main()
