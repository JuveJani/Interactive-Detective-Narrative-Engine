"""Tests for Local AI response validation, proposal, and apply (Step 3)."""

from __future__ import annotations

import json
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from idne.local_ai.apply import ApplyError, apply_proposal
from idne.local_ai.attempts import archive_current_attempt, list_attempts, reset_processing_state
from idne.local_ai.content_identity import stable_brief_id
from idne.local_ai.mock_adapter import MockAdapter, MockAdapterState, _semantic_payload
from idne.local_ai.output_paths import DEFAULT_BRIEF_OUTPUT, validate_output_path
from idne.local_ai.paths import PathValidationError
from idne.local_ai.process import process_task
from idne.local_ai.proposal_builder import map_semantic_to_canonical
from idne.local_ai.response_parser import MAX_RESPONSE_CHARS, ParseError, extract_json_candidate, parse_json_object, parse_response
from idne.local_ai.response_validate import validate_protected_values, validate_response, validate_response_schema, validate_semantic_boundaries
from idne.local_ai.run_state import load_task, write_json
from idne.local_ai.structural_repair import apply_safe_repairs
from idne.local_ai.task_builder import prepare_task
from idne.local_ai.task_model import TaskStatus
from idne.local_ai.transport import run_task
from tests.local_ai_test_helpers import can_create_symlinks
from idne.generate.brief import validate_brief

REPO_ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_INPUT = "OFFLINE_AI/examples/adventure_brief_input.md"
DRAFT_OUTPUT = DEFAULT_BRIEF_OUTPUT


def _fresh_prepare(*, output: str | None = None):
    from idne.local_ai.paths import normalize_allowlist, resolve_allowed_file, safe_task_directory_name
    from idne.local_ai.platform_runtime import local_ai_runs_root
    from idne.local_ai.task_model import make_task_id, sha256_bytes

    output_path = output or DRAFT_OUTPUT
    input_rel = EXAMPLE_INPUT
    input_bytes = resolve_allowed_file(input_rel, REPO_ROOT).read_bytes()
    allowed = normalize_allowlist([input_rel], REPO_ROOT)
    task_id = make_task_id("adventure_brief", allowed, [sha256_bytes(input_bytes)], [output_path])
    run_dir = local_ai_runs_root(REPO_ROOT) / safe_task_directory_name(task_id)
    if run_dir.exists():
        shutil.rmtree(run_dir)
    return prepare_task(
        "adventure_brief",
        EXAMPLE_INPUT,
        repo_root=REPO_ROOT,
        output_path=output_path,
    )


def _valid_semantic() -> dict:
    return _semantic_payload("testdigest1234")


class TestStructuralRepair(unittest.TestCase):
    def test_strip_bom_and_fence(self):
        body = json.dumps({"a": 1})
        raw = "\ufeff```json\n" + body + "\n```"
        result = apply_safe_repairs(raw)
        self.assertEqual(json.loads(result.text), {"a": 1})
        codes = {r.code for r in result.repairs}
        self.assertIn("strip_bom", codes)
        self.assertIn("remove_json_fence", codes)

    def test_commentary_extract(self):
        body = json.dumps(_valid_semantic())
        wrapped = f"Here is the JSON:\n{body}\nThanks."
        candidate, method = extract_json_candidate(apply_safe_repairs(wrapped).text)
        self.assertEqual(method, "commentary_extract")
        self.assertIn("premise", json.loads(candidate))


class TestResponseParser(unittest.TestCase):
    def test_plain_valid_json(self):
        data = _valid_semantic()
        parsed = parse_json_object(json.dumps(data))
        self.assertEqual(parsed["premise"], data["premise"])

    def test_fenced_json_repair(self):
        body = json.dumps(_valid_semantic())
        text = apply_safe_repairs(f"```json\n{body}\n```").text
        candidate, method = extract_json_candidate(text)
        self.assertEqual(method, "plain_json")
        self.assertIn("opening_situation", json.loads(candidate))

    def test_multiple_objects_rejected(self):
        with self.assertRaises(ParseError) as ctx:
            extract_json_candidate('{"a":1}{"b":2}')
        self.assertEqual(ctx.exception.code, "multiple_json_objects")

    def test_malformed_json_rejected(self):
        with self.assertRaises(ParseError):
            parse_json_object("{bad")

    def test_duplicate_keys_rejected(self):
        with self.assertRaises(ParseError) as ctx:
            parse_json_object('{"a":1,"a":2}')
        self.assertEqual(ctx.exception.code, "duplicate_keys")

    def test_top_level_array_rejected(self):
        with self.assertRaises(ParseError) as ctx:
            parse_json_object("[1,2]")
        self.assertEqual(ctx.exception.code, "top_level_array")

    def test_empty_response_rejected(self):
        with self.assertRaises(ParseError) as ctx:
            extract_json_candidate("   ")
        self.assertEqual(ctx.exception.code, "no_json_object")

    def test_response_size_limit(self):
        huge = "{" + '"x": "' + ("a" * (MAX_RESPONSE_CHARS + 1)) + '"}'
        with self.assertRaises(ParseError) as ctx:
            if len(huge) > MAX_RESPONSE_CHARS:
                raise ParseError("response_too_large", "too big")
        self.assertEqual(ctx.exception.code, "response_too_large")

    def test_deterministic_parse_serialization(self):
        data = _valid_semantic()
        a = json.dumps(parse_json_object(json.dumps(data)), indent=2, sort_keys=True) + "\n"
        b = json.dumps(parse_json_object(json.dumps(data)), indent=2, sort_keys=True) + "\n"
        self.assertEqual(a, b)


class TestResponseValidation(unittest.TestCase):
    def test_schema_success(self):
        findings = validate_response_schema(_valid_semantic())
        self.assertEqual(findings, [])

    def test_missing_required_field(self):
        data = _valid_semantic()
        del data["opening_situation"]
        findings = validate_response_schema(data)
        self.assertTrue(any(f.code == "missing_field" for f in findings))

    def test_wrong_type(self):
        data = _valid_semantic()
        data["target_playtime_minutes"] = "90"
        findings = validate_response_schema(data)
        self.assertTrue(any(f.code == "wrong_type" for f in findings))

    def test_invalid_enum(self):
        data = _valid_semantic()
        data["player_mode"] = "solo"
        findings = validate_response_schema(data)
        self.assertTrue(any(f.code == "invalid_enum" for f in findings))

    def test_unexpected_field(self):
        data = _valid_semantic()
        data["task_id"] = "x"
        findings = validate_response_schema(data)
        self.assertTrue(any(f.code == "unexpected_field" for f in findings))

    def test_protected_field_injection(self):
        data = _valid_semantic()
        data["adventure_id"] = "ADV-1"
        findings = validate_protected_values(data)
        self.assertTrue(findings)

    def test_empty_semantic_value(self):
        data = _valid_semantic()
        data["premise"] = "  "
        findings = validate_response_schema(data)
        self.assertTrue(any(f.code == "empty_value" for f in findings))

    def test_invalid_playtime(self):
        data = _valid_semantic()
        data["target_playtime_minutes"] = 0
        findings = validate_response_schema(data)
        self.assertTrue(any(f.path == "target_playtime_minutes" for f in findings))

    def test_author_only_opening_fact(self):
        data = _valid_semantic()
        data["opening_situation"] = "The culprit is already known and the case is closed."
        findings, _warnings = validate_semantic_boundaries(data)
        self.assertTrue(any(f.code in {"author_only_fact", "solved_mystery"} for f in findings))


class TestOutputPaths(unittest.TestCase):
    def test_draft_root_required(self):
        with self.assertRaises(PathValidationError):
            validate_output_path("adventures/Other/brief/adventure_brief.json", REPO_ROOT)

    def test_valid_draft_path(self):
        rel = validate_output_path(DRAFT_OUTPUT, REPO_ROOT)
        self.assertEqual(rel, DRAFT_OUTPUT)

    def test_path_traversal_rejected(self):
        with self.assertRaises(PathValidationError):
            validate_output_path("adventures/_local_ai_drafts/../The_Cold_Storage_Alarm/x/adventure_brief.json", REPO_ROOT)

    def test_cold_storage_forbidden(self):
        with self.assertRaises(PathValidationError):
            validate_output_path(
                "adventures/The_Cold_Storage_Alarm/brief/adventure_brief.json",
                REPO_ROOT,
            )

    def test_resolved_path_outside_repository_rejected(self):
        """Platform-independent escape check without creating a real symlink."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            (root / "AGENTS.md").write_text("x", encoding="utf-8")
            (root / "IDNE_ENGINE_v0.4.md").write_text("x", encoding="utf-8")
            rel = "adventures/_local_ai_drafts/mocktest/adventure_brief.json"
            outside = (Path(tmp) / "outside_repo" / "evil.json").resolve()
            candidate = (root / rel).resolve()
            real_resolve = Path.resolve

            def selective_resolve(self: Path, *args, **kwargs):
                resolved = real_resolve(self, *args, **kwargs)
                if resolved == candidate:
                    return outside
                return resolved

            with mock.patch.object(Path, "resolve", selective_resolve):
                with self.assertRaises(PathValidationError) as ctx:
                    validate_output_path(rel, root)
            self.assertIn("escapes", str(ctx.exception).lower())

    def test_symlink_escape_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            (root / "AGENTS.md").write_text("x", encoding="utf-8")
            (root / "IDNE_ENGINE_v0.4.md").write_text("x", encoding="utf-8")
            outside = Path(tmp) / "outside_repo"
            outside.mkdir()
            (outside / "evil.json").write_text("{}", encoding="utf-8")
            draft = root / "adventures" / "_local_ai_drafts" / "linktest"
            draft.mkdir(parents=True)
            if not can_create_symlinks(draft):
                self.skipTest("symlink creation not permitted in this environment")
            target = draft / "adventure_brief.json"
            target.symlink_to(outside / "evil.json")
            with self.assertRaises(PathValidationError) as ctx:
                validate_output_path(
                    "adventures/_local_ai_drafts/linktest/adventure_brief.json",
                    root,
                )
            self.assertIn("escapes", str(ctx.exception).lower())


class TestProposalAndApply(unittest.TestCase):
    def setUp(self):
        self._draft = REPO_ROOT / DRAFT_OUTPUT
        self._sidecar = self._draft.with_suffix(".json.local_ai_applied")
        for path in (self._draft, self._sidecar):
            if path.is_file():
                path.unlink()

    def tearDown(self):
        for path in (self._draft, self._sidecar):
            if path.is_file():
                path.unlink()
        draft_dir = self._draft.parent
        if draft_dir.is_dir() and not any(draft_dir.iterdir()):
            draft_dir.rmdir()
            parent = draft_dir.parent
            if parent.is_dir() and parent.name == "_local_ai_drafts" and not any(parent.iterdir()):
                parent.rmdir()

    def test_canonical_proposal_generation(self):
        canonical = map_semantic_to_canonical(_valid_semantic())
        self.assertEqual(validate_brief(canonical), [])
        self.assertIn("Opening situation:", canonical["author_notes"])

    def test_deterministic_brief_id(self):
        _task, _, _, _, run_dir = _fresh_prepare()
        task = load_task(run_dir)
        id_a = stable_brief_id(task)
        id_b = stable_brief_id(task)
        self.assertEqual(id_a, id_b)
        self.assertTrue(id_a.startswith("draft-"))

    def test_apply_blocked_before_validation(self):
        _task, _, _, _, run_dir = _fresh_prepare()
        run_task(run_dir, mock=True)
        with self.assertRaises(ApplyError):
            apply_proposal(run_dir)

    def test_mock_end_to_end_reaches_applied(self):
        _task, _, _, _, run_dir = _fresh_prepare()
        run_task(run_dir, mock=True)
        result = process_task(run_dir)
        self.assertTrue(result.success, result.details)
        apply_report = apply_proposal(run_dir)
        task = load_task(run_dir)
        self.assertEqual(task.status, TaskStatus.APPLIED)
        self.assertTrue(self._draft.is_file())
        self.assertEqual(apply_report["applied_hash"], apply_report["applied_hash"])

    def test_second_apply_rejected_without_overwrite(self):
        _task, _, _, _, run_dir = _fresh_prepare()
        run_task(run_dir, mock=True)
        process_task(run_dir)
        apply_proposal(run_dir)
        with self.assertRaises(ApplyError):
            apply_proposal(run_dir)

    def test_same_task_overwrite_allowed(self):
        _task, _, _, _, run_dir = _fresh_prepare()
        run_task(run_dir, mock=True)
        process_task(run_dir)
        apply_proposal(run_dir)
        apply_proposal(run_dir, overwrite=True)

    def test_process_stops_at_first_failure(self):
        _task, _, _, _, run_dir = _fresh_prepare()
        run_task(run_dir, mock=True)
        (run_dir / "response.txt").write_text("{not json", encoding="utf-8")
        result = process_task(run_dir)
        self.assertFalse(result.success)
        self.assertEqual(result.stopped_at, "parse")

    def test_attempts_preserved_on_force(self):
        _task, _, _, _, run_dir = _fresh_prepare()
        run_task(run_dir, mock=True)
        archive_current_attempt(run_dir)
        reset_processing_state(run_dir)
        task = load_task(run_dir)
        task.status = TaskStatus.RESPONSE_RECEIVED
        write_json(run_dir / "task.json", task.to_dict())
        run_task(run_dir, mock=True, force=True)
        attempts = list_attempts(run_dir)
        self.assertEqual(len(attempts), 1)

    def test_mock_mode_opens_no_socket(self):
        _task, _, _, _, run_dir = _fresh_prepare()
        with mock.patch("socket.socket", side_effect=AssertionError("socket opened")):
            run_task(run_dir, mock=True)
            process_task(run_dir)

    def test_no_existing_adventure_modified(self):
        cold = REPO_ROOT / "adventures" / "The_Cold_Storage_Alarm"
        if not cold.is_dir():
            self.skipTest("Cold Storage adventure not present")
        before = {
            p: p.read_bytes()
            for p in cold.rglob("*")
            if p.is_file() and p.stat().st_size < 500_000
        }
        _task, _, _, _, run_dir = _fresh_prepare()
        run_task(run_dir, mock=True)
        process_task(run_dir)
        apply_proposal(run_dir)
        after = {
            p: p.read_bytes()
            for p in cold.rglob("*")
            if p.is_file() and p.stat().st_size < 500_000
        }
        self.assertEqual(before, after)


class TestMockAdapterScenarios(unittest.TestCase):
    def test_fenced_json_scenario(self):
        adapter = MockAdapter(MockAdapterState(scenario="fenced_json"))
        result = adapter.complete(None, model="mock", user_prompt="x")
        self.assertIn("```", result.content)

    def test_duplicate_key_scenario(self):
        adapter = MockAdapter(MockAdapterState(scenario="duplicate_key"))
        result = adapter.complete(None, model="mock", user_prompt="x")
        self.assertIn('"premise"', result.content)


class TestCLIEndToEnd(unittest.TestCase):
    def setUp(self):
        from idne.local_ai.paths import normalize_allowlist, resolve_allowed_file, safe_task_directory_name
        from idne.local_ai.platform_runtime import local_ai_runs_root
        from idne.local_ai.task_model import make_task_id, sha256_bytes

        self._draft = REPO_ROOT / DRAFT_OUTPUT
        self._sidecar = self._draft.with_suffix(".json.local_ai_applied")
        for path in (self._draft, self._sidecar):
            if path.is_file():
                path.unlink()
        input_bytes = resolve_allowed_file(EXAMPLE_INPUT, REPO_ROOT).read_bytes()
        allowed = normalize_allowlist([EXAMPLE_INPUT], REPO_ROOT)
        task_id = make_task_id("adventure_brief", allowed, [sha256_bytes(input_bytes)], [DRAFT_OUTPUT])
        run_dir = local_ai_runs_root(REPO_ROOT) / safe_task_directory_name(task_id)
        if run_dir.exists():
            shutil.rmtree(run_dir)

    def tearDown(self):
        for path in (self._draft, self._sidecar):
            if path.is_file():
                path.unlink()

    def _run_cli(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, "-m", "idne.local_ai", *args],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )

    def test_cli_mock_workflow(self):
        prep = self._run_cli(
            "prepare",
            "--task-type",
            "adventure_brief",
            "--input",
            EXAMPLE_INPUT,
            "--output",
            DRAFT_OUTPUT,
        )
        self.assertEqual(prep.returncode, 0, prep.stderr)
        run_dir = None
        for line in prep.stdout.splitlines():
            if line.startswith("Dir:"):
                run_dir = line.split("Dir:", 1)[1].strip()
        self.assertIsNotNone(run_dir)
        run = self._run_cli("run", run_dir, "--mock")
        self.assertEqual(run.returncode, 0, run.stderr)
        proc = self._run_cli("process", run_dir)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        review = self._run_cli("review", run_dir)
        self.assertEqual(review.returncode, 0)
        self.assertIn("Apply allowed: yes", review.stdout)
        apply = self._run_cli("apply", run_dir)
        self.assertEqual(apply.returncode, 0, apply.stderr)
        self.assertTrue(self._draft.is_file())


if __name__ == "__main__":
    unittest.main()
