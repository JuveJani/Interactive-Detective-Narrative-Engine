"""Tests for Local AI support-bundle command."""

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

from idne.local_ai.output_paths import DEFAULT_BRIEF_OUTPUT
from idne.local_ai.platform_runtime import local_ai_runs_root
from idne.local_ai.support_bundle import (
    SUPPORT_ROOT,
    _bundle_id,
    generate_support_bundle,
    redact_mapping,
)
from idne.local_ai.task_builder import prepare_task

REPO_ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_INPUT = "OFFLINE_AI/examples/adventure_brief_input.md"


def _prepare_run_dir() -> Path:
    from idne.local_ai.paths import normalize_allowlist, resolve_allowed_file, safe_task_directory_name
    from idne.local_ai.task_model import make_task_id, sha256_bytes

    input_bytes = resolve_allowed_file(EXAMPLE_INPUT, REPO_ROOT).read_bytes()
    allowed = normalize_allowlist([EXAMPLE_INPUT], REPO_ROOT)
    task_id = make_task_id(
        "adventure_brief",
        allowed,
        [sha256_bytes(input_bytes)],
        [DEFAULT_BRIEF_OUTPUT],
    )
    run_dir = local_ai_runs_root(REPO_ROOT) / safe_task_directory_name(task_id)
    if run_dir.exists():
        shutil.rmtree(run_dir)
    _task, _ctx, _prompt, _metrics, run_dir = prepare_task(
        "adventure_brief",
        EXAMPLE_INPUT,
        repo_root=REPO_ROOT,
        output_path=DEFAULT_BRIEF_OUTPUT,
    )
    return run_dir


class TestRedaction(unittest.TestCase):
    def test_secret_keys_redacted(self):
        data = {
            "api_token_env": "LM_STUDIO_API_TOKEN",
            "authorization": "Bearer secret-token-value",
            "nested": {"api_key": "abc123", "model": "test"},
        }
        redacted = redact_mapping(data)
        self.assertEqual(redacted["authorization"], "[REDACTED]")
        self.assertEqual(redacted["nested"]["api_key"], "[REDACTED]")
        self.assertEqual(redacted["nested"]["model"], "test")

    def test_sorted_keys(self):
        data = {"z": 1, "a": 2, "m": 3}
        self.assertEqual(list(redact_mapping(data).keys()), ["a", "m", "z"])


class TestBundleId(unittest.TestCase):
    def test_deterministic_bundle_id(self):
        self.assertEqual(_bundle_id("adventure_brief-abc", "fcdb8de1"), "adventure_brief-abc_fcdb8de1")
        self.assertEqual(_bundle_id(None, "fcdb8de1"), "environment_fcdb8de1")


class TestSupportBundle(unittest.TestCase):
    def setUp(self) -> None:
        self._support_dirs: list[Path] = []

    def tearDown(self) -> None:
        for path in self._support_dirs:
            if path.exists():
                shutil.rmtree(path, ignore_errors=True)

    def _generate(self, run_dir: Path | None = None, *, mock: bool = True) -> Path:
        bundle_dir = generate_support_bundle(run_dir, repo_root=REPO_ROOT, mock=mock)
        self._support_dirs.append(bundle_dir)
        return bundle_dir

    def test_environment_only_bundle(self):
        bundle_dir = self._generate(None)
        self.assertTrue(bundle_dir.is_dir())
        self.assertTrue((bundle_dir / "REPORT.md").is_file())
        self.assertTrue((bundle_dir / "environment.json").is_file())
        manifest = json.loads((bundle_dir / "bundle_manifest.json").read_text(encoding="utf-8"))
        self.assertIsNone(manifest["task_id"])

    def test_task_bundle_creates_expected_files(self):
        run_dir = _prepare_run_dir()
        before_task_mtime = (run_dir / "task.json").stat().st_mtime_ns
        before_task_hash = (run_dir / "task.json").read_bytes()

        bundle_dir = self._generate(run_dir)
        self.assertTrue((bundle_dir / "artifacts" / "task.json").is_file())
        self.assertTrue((bundle_dir / "artifact_summary.json").is_file())

        after_task_mtime = (run_dir / "task.json").stat().st_mtime_ns
        after_task_hash = (run_dir / "task.json").read_bytes()
        self.assertEqual(before_task_hash, after_task_hash)
        self.assertEqual(before_task_mtime, after_task_mtime)

    def test_missing_optional_artifacts_tolerated(self):
        run_dir = _prepare_run_dir()
        bundle_dir = self._generate(run_dir)
        summary = json.loads((bundle_dir / "artifact_summary.json").read_text(encoding="utf-8"))
        self.assertFalse(summary["artifacts"]["response.txt"])
        self.assertFalse(summary["artifacts"]["transport_report.json"])

    def test_secret_redaction_in_environment(self):
        run_dir = _prepare_run_dir()
        with tempfile.NamedTemporaryFile("w", suffix=".toml", delete=False) as tmp:
            tmp.write(
                '[adapter]\ntype = "mock"\nbase_url = "http://127.0.0.1:1234/v1"\n'
                'api_token_env = "LM_STUDIO_API_TOKEN"\n'
            )
            config_path = Path(tmp.name)
        os.environ["LM_STUDIO_API_TOKEN"] = "super-secret-token-should-not-appear"
        try:
            bundle_dir = generate_support_bundle(
                run_dir,
                config_path=config_path,
                repo_root=REPO_ROOT,
                mock=True,
            )
            self._support_dirs.append(bundle_dir)
            env = json.loads((bundle_dir / "environment.json").read_text(encoding="utf-8"))
            serialized = json.dumps(env)
            self.assertNotIn("super-secret-token-should-not-appear", serialized)
            self.assertTrue(env["config_effective"].get("api_token_present"))
        finally:
            os.environ.pop("LM_STUDIO_API_TOKEN", None)
            config_path.unlink(missing_ok=True)

    def test_deterministic_ordering_in_manifest(self):
        run_dir = _prepare_run_dir()
        bundle_dir = self._generate(run_dir)
        manifest = json.loads((bundle_dir / "bundle_manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(list(manifest.keys()), sorted(manifest.keys()))
        summary = json.loads((bundle_dir / "artifact_summary.json").read_text(encoding="utf-8"))
        self.assertEqual(list(summary["artifacts"].keys()), sorted(summary["artifacts"].keys()))

    def test_repo_relative_paths_use_posix(self):
        run_dir = _prepare_run_dir()
        bundle_dir = self._generate(run_dir)
        manifest = json.loads((bundle_dir / "bundle_manifest.json").read_text(encoding="utf-8"))
        self.assertIn(SUPPORT_ROOT, manifest["bundle_path"])
        self.assertNotIn("\\", manifest["bundle_path"])
        summary = json.loads((bundle_dir / "artifact_summary.json").read_text(encoding="utf-8"))
        self.assertNotIn("\\", summary["task_directory"])

    def test_bundle_id_stable_for_same_git_head(self):
        run_dir = _prepare_run_dir()
        head = subprocess.run(
            ["git", "-C", str(REPO_ROOT), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()[:8]
        expected_id = _bundle_id(json.loads((run_dir / "task.json").read_text())["task_id"], head)
        bundle_dir = self._generate(run_dir)
        self.assertEqual(bundle_dir.name, expected_id)

    def test_reasoning_metadata_in_manifest_when_present(self):
        run_dir = _prepare_run_dir()
        transport = {
            "reasoning_present": True,
            "reasoning_character_count": 42,
            "finish_reason": "stop",
            "success": True,
        }
        (run_dir / "transport_report.json").write_text(
            json.dumps(transport, indent=2) + "\n",
            encoding="utf-8",
        )
        bundle_dir = self._generate(run_dir)
        manifest = json.loads((bundle_dir / "bundle_manifest.json").read_text(encoding="utf-8"))
        self.assertTrue(manifest["reasoning_metadata"]["reasoning_present"])
        self.assertEqual(manifest["reasoning_metadata"]["reasoning_character_count"], 42)
        report = (bundle_dir / "REPORT.md").read_text(encoding="utf-8")
        self.assertIn("diagnostic metadata only", report)

    @mock.patch("idne.local_ai.paths.to_posix_relpath")
    def test_pathlib_safe_serialization(self, mock_relpath):
        mock_relpath.side_effect = lambda path, root: path.as_posix().replace(str(root.as_posix()) + "/", "")
        run_dir = _prepare_run_dir()
        bundle_dir = self._generate(run_dir)
        summary = json.loads((bundle_dir / "artifact_summary.json").read_text(encoding="utf-8"))
        self.assertIn(".local_ai_runs/", summary["task_directory"])


class TestSupportBundleCLI(unittest.TestCase):
    def test_cli_support_bundle_mock(self):
        run_dir = _prepare_run_dir()
        proc = subprocess.run(
            [
                sys.executable,
                "-m",
                "idne.local_ai",
                "support-bundle",
                str(run_dir),
                "--mock",
            ],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn(".local_ai_support/", proc.stdout)


if __name__ == "__main__":
    unittest.main()
