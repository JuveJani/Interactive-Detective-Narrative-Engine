"""Tests for IDNE Offline Local AI Orchestrator deterministic core."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from idne.local_ai.context_builder import build_context_package, estimate_tokens
from idne.local_ai.doctor import run_doctor
from idne.local_ai.paths import (
    PathValidationError,
    normalize_allowlist,
    normalize_repo_relative,
    resolve_allowed_file,
)
from idne.local_ai.prompt_builder import build_prompt
from idne.local_ai.run_state import load_task, set_task_status
from idne.local_ai.task_builder import TASK_DEFINITIONS, prepare_task
from idne.local_ai.task_model import (
    LocalAITask,
    SourceIdentity,
    TaskStatus,
    assert_valid_transition,
    make_task_id,
    stable_task_identity,
    validate_task_schema,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_INPUT = "OFFLINE_AI/examples/adventure_brief_input.md"


class TestPathNormalization(unittest.TestCase):
    def test_windows_style_path_normalized_to_posix(self):
        rel = normalize_repo_relative(r"OFFLINE_AI\examples\adventure_brief_input.md", REPO_ROOT)
        self.assertEqual(rel, "OFFLINE_AI/examples/adventure_brief_input.md")

    def test_posix_path_unchanged(self):
        rel = normalize_repo_relative("AGENTS.md", REPO_ROOT)
        self.assertEqual(rel, "AGENTS.md")

    def test_repository_relative_serialization(self):
        rel = normalize_repo_relative("./OFFLINE_AI/examples/adventure_brief_input.md", REPO_ROOT)
        self.assertFalse(rel.startswith("./"))
        self.assertNotIn("\\", rel)

    def test_absolute_path_rejected(self):
        with self.assertRaises(PathValidationError):
            normalize_repo_relative("/etc/passwd", REPO_ROOT)
        with self.assertRaises(PathValidationError):
            normalize_repo_relative("C:/Windows/notepad.exe", REPO_ROOT)

    def test_traversal_rejected(self):
        with self.assertRaises(PathValidationError):
            normalize_repo_relative("../AGENTS.md", REPO_ROOT)

    def test_directory_rejected_as_input_file(self):
        with self.assertRaises(PathValidationError):
            resolve_allowed_file("adventures/The_Cold_Storage_Alarm/adventure/DO_NOT_READ", REPO_ROOT)

    def test_duplicate_normalized_path_rejected(self):
        with self.assertRaises(PathValidationError):
            normalize_allowlist(["AGENTS.md", "./AGENTS.md"], REPO_ROOT)

    def test_file_outside_repository_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            outside = Path(tmp) / "outside.txt"
            outside.write_text("x", encoding="utf-8")
            with self.assertRaises(PathValidationError):
                resolve_allowed_file(outside.as_posix(), REPO_ROOT)

    def test_deterministic_file_ordering(self):
        ordered = normalize_allowlist(
            ["OFFLINE_AI/README.md", "AGENTS.md", "OFFLINE_AI/CURRENT_STATE.md"],
            REPO_ROOT,
        )
        self.assertEqual(ordered, sorted(ordered))

    def test_do_not_read_directory_never_opened_as_first_rglob_file(self):
        """Regression: directory-first iteration must not be used for task input."""
        adventure_root = REPO_ROOT / "adventures" / "The_Cold_Storage_Alarm" / "adventure"
        if not adventure_root.is_dir():
            self.skipTest("Cold Storage adventure not present")
        unsorted_first = next(adventure_root.rglob("*"))
        self.assertTrue(unsorted_first.exists())
        if unsorted_first.is_dir():
            with self.assertRaises(PathValidationError):
                resolve_allowed_file(
                    unsorted_first.relative_to(REPO_ROOT).as_posix(),
                    REPO_ROOT,
                )


class TestContextBuilder(unittest.TestCase):
    def test_utf8_read(self):
        path = REPO_ROOT / EXAMPLE_INPUT
        text = path.read_text(encoding="utf-8")
        self.assertIn("museum", text.lower())

    def test_exact_allowlist_only(self):
        spec = TASK_DEFINITIONS["adventure_brief"].authoritative_files[0]
        with mock.patch("idne.local_ai.context_builder.resolve_allowed_file", wraps=resolve_allowed_file) as resolver:
            build_context_package(
                REPO_ROOT,
                [EXAMPLE_INPUT],
                [spec],
                context_budget=50000,
            )
            touched = {call.args[0] for call in resolver.call_args_list}
        self.assertIn(EXAMPLE_INPUT, touched)
        self.assertIn(spec.path, touched)
        self.assertEqual(len(touched), 2)

    def test_context_budget_success(self):
        result = build_context_package(
            REPO_ROOT,
            [EXAMPLE_INPUT],
            list(TASK_DEFINITIONS["adventure_brief"].authoritative_files),
            context_budget=50000,
        )
        self.assertFalse(result.blocked)
        self.assertGreater(result.character_count, 0)

    def test_context_budget_failure(self):
        result = build_context_package(
            REPO_ROOT,
            [EXAMPLE_INPUT],
            list(TASK_DEFINITIONS["adventure_brief"].authoritative_files),
            context_budget=200,
        )
        self.assertTrue(result.blocked)
        self.assertIn("budget", result.block_reason.lower())
        self.assertTrue(result.overflow_source)


class TestTaskModel(unittest.TestCase):
    def _sample_task(self) -> LocalAITask:
        return LocalAITask(
            schema_version="1.0",
            task_id="adventure_brief-deadbeef0123",
            task_type="adventure_brief",
            stage_name="adventure_brief",
            created_at="2026-08-06T10:00:00+00:00",
            source_content_identity=SourceIdentity(sha256="a" * 64, path=EXAMPLE_INPUT),
            allowed_input_files=[EXAMPLE_INPUT],
            allowed_output_files=["brief/adventure_brief.json"],
            authoritative_sources=[],
            approved_prior_stage_facts={},
            protected_values={"task_id": "adventure_brief-deadbeef0123"},
            expected_output_schema_ref="ADVENTURE_GENERATOR_V2_SCHEMA.md#1",
            context_budget=12000,
            generation_settings={"backend": None},
            validator_commands=[],
            status=TaskStatus.CREATED,
            attempt_count=0,
            run_directory=".local_ai_runs/adventure_brief-deadbeef0123",
            task_instruction="test",
        )

    def test_task_schema_validation(self):
        data = self._sample_task().to_dict()
        self.assertEqual(validate_task_schema(data), [])

    def test_stable_task_serialization(self):
        data1 = self._sample_task().to_dict()
        data2 = LocalAITask.from_dict(data1).to_dict()
        self.assertEqual(data1, data2)

    def test_deterministic_task_identity(self):
        paths = [EXAMPLE_INPUT]
        hashes = ["abc", "abc"]
        id1 = stable_task_identity("adventure_brief", paths, hashes)
        id2 = stable_task_identity("adventure_brief", paths, hashes)
        self.assertEqual(id1, id2)
        self.assertNotEqual(
            stable_task_identity("adventure_brief", paths, ["different"]),
            id1,
        )

    def test_make_task_id_format(self):
        task_id = make_task_id("adventure_brief", [EXAMPLE_INPUT], ["deadbeef"])
        self.assertTrue(task_id.startswith("adventure_brief-"))

    def test_invalid_status_transition_rejected(self):
        with self.assertRaises(ValueError):
            assert_valid_transition(TaskStatus.APPLIED, TaskStatus.CREATED)
        task = self._sample_task()
        task.status = TaskStatus.READY_FOR_MODEL
        with self.assertRaises(ValueError):
            set_task_status(task, TaskStatus.CREATED)


class TestPromptBuilder(unittest.TestCase):
    def test_deterministic_prompt_generation(self):
        task, context, _, _, run_dir = prepare_task(
            "adventure_brief",
            EXAMPLE_INPUT,
            repo_root=REPO_ROOT,
        )
        prompt_a = build_prompt(task, context)
        prompt_b = (run_dir / "prompt.txt").read_text(encoding="utf-8")
        self.assertEqual(prompt_a, prompt_b)
        self.assertIn("JSON only", prompt_a)
        self.assertIn("protected", prompt_a.lower())
        self.assertIn("Do not assign adventure_id", prompt_a)

    def test_protected_values_included(self):
        task, context, _, _, _ = prepare_task(
            "adventure_brief",
            EXAMPLE_INPUT,
            repo_root=REPO_ROOT,
        )
        prompt = build_prompt(task, context)
        self.assertIn(task.task_id, prompt)
        self.assertIn("python_assigns", prompt)


class TestPrepareEndToEnd(unittest.TestCase):
    def setUp(self):
        self._runs = REPO_ROOT / ".local_ai_runs"
        self._prior = list(self._runs.glob("*")) if self._runs.exists() else []

    def test_adventure_brief_preparation_without_model(self):
        task, context, prompt, metrics, run_dir = prepare_task(
            "adventure_brief",
            EXAMPLE_INPUT,
            repo_root=REPO_ROOT,
        )
        self.assertEqual(task.status, TaskStatus.READY_FOR_MODEL)
        self.assertTrue(run_dir.is_dir())
        self.assertTrue((run_dir / "task.json").is_file())
        self.assertTrue((run_dir / "context_manifest.json").is_file())
        self.assertTrue((run_dir / "context.txt").is_file())
        self.assertTrue((run_dir / "prompt.txt").is_file())
        self.assertTrue((run_dir / "status.json").is_file())
        self.assertTrue((run_dir / "diagnostics.json").is_file())
        self.assertGreater(metrics.character_count, 0)
        self.assertGreater(metrics.approximate_tokens, 0)
        self.assertLess(metrics.preparation_seconds, 10.0)
        self.assertFalse(context.blocked)
        self.assertIn("universe", prompt.lower())
        loaded = load_task(run_dir)
        self.assertEqual(loaded.task_id, task.task_id)
        schema_errors = validate_task_schema(json.loads((run_dir / "task.json").read_text(encoding="utf-8")))
        self.assertEqual(schema_errors, [])


class TestDoctor(unittest.TestCase):
    def test_doctor_ready_in_valid_repository(self):
        report = run_doctor(start=REPO_ROOT, mock=True)
        self.assertIn(report.status, ("READY", "DEGRADED"))
        self.assertTrue(report.checks["utf8_roundtrip"])
        self.assertTrue(report.checks["deterministic_ordering"])
        self.assertTrue(report.checks["run_directory"]["writable"])

    def test_doctor_degraded_without_git(self):
        with mock.patch("idne.local_ai.doctor.subprocess.run", side_effect=FileNotFoundError("git")):
            report = run_doctor(start=REPO_ROOT, mock=True)
        self.assertEqual(report.status, "DEGRADED")
        self.assertFalse(report.checks["git"]["available"])

    def test_doctor_ready_in_temporary_valid_repository(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "AGENTS.md").write_text("# agents", encoding="utf-8")
            (root / "IDNE_ENGINE_v0.4.md").write_text("# engine", encoding="utf-8")
            for spec in TASK_DEFINITIONS["adventure_brief"].authoritative_files:
                target = root / spec.path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(f"# {spec.path}\n\n{spec.excerpt_start or 'content'}\n", encoding="utf-8")
            report = run_doctor(start=root, mock=True)
            self.assertIn(report.status, ("READY", "DEGRADED"))


class TestCLI(unittest.TestCase):
    def test_cli_doctor(self):
        proc = subprocess.run(
            [sys.executable, "-m", "idne.local_ai", "doctor", "--mock"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )
        self.assertIn("Status:", proc.stdout)
        self.assertIn(proc.returncode, (0, 3))

    def test_cli_prepare(self):
        proc = subprocess.run(
            [
                sys.executable,
                "-m",
                "idne.local_ai",
                "prepare",
                "--task-type",
                "adventure_brief",
                "--input",
                EXAMPLE_INPUT,
            ],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )
        self.assertEqual(proc.returncode, 0, msg=proc.stderr)
        self.assertIn("READY_FOR_MODEL", proc.stdout + proc.stderr)


class TestTokenEstimate(unittest.TestCase):
    def test_approximate_tokens(self):
        self.assertEqual(estimate_tokens(400), 100)


if __name__ == "__main__":
    unittest.main()
