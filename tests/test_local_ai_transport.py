"""Tests for Local AI LM Studio adapter and transport (Step 2)."""

from __future__ import annotations

import json
import os
import socket
import subprocess
import sys
import tempfile
import unittest
import urllib.error
import urllib.request
from pathlib import Path
from unittest import mock

from idne.local_ai.config import (
    ConfigurationError,
    EndpointRejectedError,
    load_config,
    normalize_base_url,
    resolve_api_token,
    validate_endpoint_policy,
)
from idne.local_ai.errors import (
    ConnectionRefusedTransportError,
    EmptyCompletionTransportError,
    HttpTransportError,
    MalformedJsonTransportError,
    ModelNotFoundTransportError,
    ModelSelectionError,
    UnsupportedResponseTransportError,
)
from idne.local_ai.lm_studio_client import (
    chat_completion,
    extract_completion_content,
    list_models,
    parse_models_response,
)
from idne.local_ai.mock_adapter import MockAdapter, MockAdapterState
from idne.local_ai.model_adapter import create_adapter, execute_with_retries, select_model
from idne.local_ai.task_builder import prepare_task
from idne.local_ai.task_model import TaskStatus
from idne.local_ai.transport import TaskRunError, run_task
from tests.local_ai_test_helpers import assert_resolved_under

REPO_ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_INPUT = "OFFLINE_AI/examples/adventure_brief_input.md"


def _fresh_prepare():
    import shutil

    from idne.local_ai.paths import normalize_allowlist, resolve_allowed_file, safe_task_directory_name
    from idne.local_ai.platform_runtime import local_ai_runs_root
    from idne.local_ai.task_model import make_task_id, sha256_bytes

    input_rel = EXAMPLE_INPUT
    input_bytes = resolve_allowed_file(input_rel, REPO_ROOT).read_bytes()
    allowed = normalize_allowlist([input_rel], REPO_ROOT)
    task_id = make_task_id("adventure_brief", allowed, [sha256_bytes(input_bytes)])
    run_dir = local_ai_runs_root(REPO_ROOT) / safe_task_directory_name(task_id)
    if run_dir.exists():
        shutil.rmtree(run_dir)
    return prepare_task("adventure_brief", EXAMPLE_INPUT, repo_root=REPO_ROOT)


def _write_toml(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


class TestConfiguration(unittest.TestCase):
    def setUp(self):
        self._env = os.environ.copy()

    def tearDown(self):
        os.environ.clear()
        os.environ.update(self._env)

    def test_default_loopback_endpoint(self):
        cfg = load_config(repo_root=REPO_ROOT)
        self.assertEqual(cfg.base_url, "http://127.0.0.1:1234/v1")

    def test_base_url_normalization_without_v1(self):
        self.assertEqual(normalize_base_url("http://127.0.0.1:1234"), "http://127.0.0.1:1234/v1")

    def test_base_url_normalization_with_v1(self):
        self.assertEqual(normalize_base_url("http://127.0.0.1:1234/v1"), "http://127.0.0.1:1234/v1")

    def test_no_duplicate_v1_in_paths(self):
        base = normalize_base_url("http://127.0.0.1:1234/v1")
        self.assertFalse(base.endswith("/v1/v1"))

    def test_https_allowed(self):
        self.assertEqual(normalize_base_url("https://127.0.0.1:1234"), "https://127.0.0.1:1234/v1")

    def test_unsupported_scheme_rejected(self):
        with self.assertRaises(ConfigurationError):
            normalize_base_url("ftp://127.0.0.1:1234")

    def test_non_loopback_rejected_by_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            cfg_path = Path(tmp) / "local_ai.toml"
            _write_toml(
                cfg_path,
                '[adapter]\ntype = "lm_studio"\nbase_url = "http://192.168.1.10:1234/v1"\n',
            )
            with self.assertRaises(EndpointRejectedError):
                load_config(config_path=cfg_path, repo_root=REPO_ROOT)

    def test_remote_allowed_when_configured(self):
        with tempfile.TemporaryDirectory() as tmp:
            cfg_path = Path(tmp) / "local_ai.toml"
            _write_toml(
                cfg_path,
                '[adapter]\ntype = "lm_studio"\nbase_url = "http://192.168.1.10:1234/v1"\nallow_remote_endpoint = true\n',
            )
            cfg = load_config(config_path=cfg_path, repo_root=REPO_ROOT)
            self.assertTrue(cfg.allow_remote_endpoint)

    def test_config_precedence_explicit_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            cfg_path = Path(tmp) / "local_ai.toml"
            _write_toml(cfg_path, '[adapter]\nmodel = "from-file"\n')
            cfg = load_config(config_path=cfg_path, repo_root=REPO_ROOT)
            self.assertEqual(cfg.model, "from-file")

    def test_environment_override(self):
        os.environ["IDNE_LOCAL_AI_MODEL"] = "env-model"
        cfg = load_config(repo_root=REPO_ROOT)
        self.assertEqual(cfg.model, "env-model")

    def test_toml_parsing(self):
        with tempfile.TemporaryDirectory() as tmp:
            cfg_path = Path(tmp) / "local_ai.toml"
            _write_toml(
                cfg_path,
                """
[adapter]
type = "lm_studio"
model = "test-model"

[transport]
temperature = 0.2
max_output_tokens = 512
retry_count = 1
""",
            )
            cfg = load_config(config_path=cfg_path, repo_root=REPO_ROOT)
            self.assertEqual(cfg.model, "test-model")
            self.assertEqual(cfg.temperature, 0.2)
            self.assertEqual(cfg.max_output_tokens, 512)
            self.assertEqual(cfg.retry_count, 1)

    def test_api_token_header_without_logging(self):
        with tempfile.TemporaryDirectory() as tmp:
            cfg_path = Path(tmp) / "local_ai.toml"
            _write_toml(cfg_path, '[adapter]\napi_token_env = "TEST_LOCAL_AI_TOKEN"\n')
            os.environ["TEST_LOCAL_AI_TOKEN"] = "secret-token"
            cfg = load_config(config_path=cfg_path, repo_root=REPO_ROOT)
            token = resolve_api_token(cfg)
            self.assertEqual(token, "secret-token")
            self.assertNotIn("secret-token", cfg.to_dict().__str__())


class TestModelSelection(unittest.TestCase):
    def test_exact_configured_model(self):
        from idne.local_ai.config import LocalAIConfig
        from idne.local_ai.lm_studio_client import ModelDescriptor

        cfg = LocalAIConfig(model="model-b")
        models = [ModelDescriptor(model_id="model-a"), ModelDescriptor(model_id="model-b")]
        sel = select_model(cfg, models)
        self.assertEqual(sel.model_id, "model-b")

    def test_single_model_auto_select(self):
        from idne.local_ai.config import LocalAIConfig
        from idne.local_ai.lm_studio_client import ModelDescriptor

        cfg = LocalAIConfig(model=None)
        models = [ModelDescriptor(model_id="only-model")]
        sel = select_model(cfg, models)
        self.assertEqual(sel.model_id, "only-model")

    def test_multiple_models_blocked(self):
        from idne.local_ai.config import LocalAIConfig
        from idne.local_ai.lm_studio_client import ModelDescriptor

        cfg = LocalAIConfig(model=None)
        models = [ModelDescriptor(model_id="a"), ModelDescriptor(model_id="b")]
        with self.assertRaises(ModelSelectionError) as ctx:
            select_model(cfg, models)
        self.assertEqual(ctx.exception.available_models, ["a", "b"])

    def test_empty_model_list(self):
        from idne.local_ai.config import LocalAIConfig

        cfg = LocalAIConfig(model=None)
        with self.assertRaises(ModelSelectionError):
            select_model(cfg, [])

    def test_missing_configured_model(self):
        from idne.local_ai.config import LocalAIConfig
        from idne.local_ai.lm_studio_client import ModelDescriptor

        cfg = LocalAIConfig(model="missing")
        with self.assertRaises(ModelNotFoundTransportError):
            select_model(cfg, [ModelDescriptor(model_id="other")])


class TestResponseParsing(unittest.TestCase):
    def test_successful_completion_parse(self):
        data = {
            "choices": [{"message": {"content": '{"ok": true}'}, "finish_reason": "stop"}],
            "usage": {"prompt_tokens": 1, "completion_tokens": 2, "total_tokens": 3},
        }
        content, finish, usage = extract_completion_content(data)
        self.assertEqual(content, '{"ok": true}')
        self.assertEqual(finish, "stop")
        self.assertEqual(usage["total_tokens"], 3)

    def test_missing_choices(self):
        with self.assertRaises(UnsupportedResponseTransportError):
            extract_completion_content({"choices": []})

    def test_null_content(self):
        with self.assertRaises(EmptyCompletionTransportError):
            extract_completion_content({"choices": [{"message": {"content": None}}]})

    def test_blank_content(self):
        with self.assertRaises(EmptyCompletionTransportError):
            extract_completion_content({"choices": [{"message": {"content": "   "}}]})

    def test_model_list_parsing(self):
        models = parse_models_response({"data": [{"id": "m1", "owned_by": "local"}]})
        self.assertEqual(models[0].model_id, "m1")


class TestHttpClient(unittest.TestCase):
    def test_chat_completion_success(self):
        from idne.local_ai.config import LocalAIConfig

        cfg = LocalAIConfig()
        payload = {
            "choices": [
                {
                    "message": {"content": '{"probe":"ok"}'},
                    "finish_reason": "stop",
                }
            ],
            "usage": {"prompt_tokens": 5, "completion_tokens": 6, "total_tokens": 11},
        }

        def fake_urlopen(req, timeout=0):
            self.assertIn("Bearer", req.headers.get("Authorization", "") or req.headers.get("authorization", "") or "")
            return _FakeHTTPResponse(json.dumps(payload).encode("utf-8"))

        with mock.patch("urllib.request.urlopen", fake_urlopen):
            os.environ.pop("LM_STUDIO_API_TOKEN", None)
            os.environ["LM_STUDIO_API_TOKEN"] = "tok"
            result = chat_completion(cfg, model="m1", user_prompt="hello")
            self.assertIn("probe", result.content)
            self.assertEqual(result.usage["total_tokens"], 11)

    def test_malformed_json(self):
        from idne.local_ai.config import LocalAIConfig

        cfg = LocalAIConfig()

        def fake_urlopen(req, timeout=0):
            return _FakeHTTPResponse(b"not-json")

        with mock.patch("urllib.request.urlopen", fake_urlopen):
            with self.assertRaises(MalformedJsonTransportError):
                chat_completion(cfg, model="m1", user_prompt="hello")

    def test_http_error(self):
        from idne.local_ai.config import LocalAIConfig

        cfg = LocalAIConfig()

        def fake_urlopen(req, timeout=0):
            raise urllib.error.HTTPError(req.full_url, 500, "error", hdrs=None, fp=None)

        with mock.patch("urllib.request.urlopen", fake_urlopen):
            with self.assertRaises(HttpTransportError) as ctx:
                chat_completion(cfg, model="m1", user_prompt="hello")
            self.assertTrue(ctx.exception.retryable)

    def test_connection_refused(self):
        from idne.local_ai.config import LocalAIConfig

        cfg = LocalAIConfig()

        def fake_urlopen(req, timeout=0):
            raise urllib.error.URLError(ConnectionRefusedError("refused"))

        with mock.patch("urllib.request.urlopen", fake_urlopen):
            with self.assertRaises(ConnectionRefusedTransportError):
                list_models(cfg)

    def test_external_endpoint_blocked_before_request(self):
        with self.assertRaises(EndpointRejectedError):
            validate_endpoint_policy("http://example.com/v1", allow_remote_endpoint=False)


class _FakeHTTPResponse:
    def __init__(self, body: bytes, status: int = 200) -> None:
        self._body = body
        self.status = status

    def read(self, n=-1):
        return self._body

    def getcode(self):
        return self.status

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


class TestMockAdapter(unittest.TestCase):
    def test_mock_success(self):
        adapter = MockAdapter()
        from idne.local_ai.config import LocalAIConfig

        cfg = LocalAIConfig(model="mock-model")
        result = adapter.complete(cfg, model="mock-model", user_prompt="task prompt")
        self.assertIn("genre", result.content)

    def test_deterministic_mock_output(self):
        adapter = MockAdapter()
        from idne.local_ai.config import LocalAIConfig

        cfg = LocalAIConfig(model="mock-model")
        a = adapter.complete(cfg, model="mock-model", user_prompt="same").content
        b = adapter.complete(cfg, model="mock-model", user_prompt="same").content
        self.assertEqual(a, b)

    def test_mock_no_socket(self):
        adapter = MockAdapter(MockAdapterState(scenario="connection_refused"))
        from idne.local_ai.config import LocalAIConfig

        cfg = LocalAIConfig()
        with mock.patch("urllib.request.urlopen", side_effect=AssertionError("socket opened")):
            with self.assertRaises(ConnectionRefusedTransportError):
                adapter.list_models(cfg)

    def test_retry_only_transient(self):
        from idne.local_ai.config import LocalAIConfig

        cfg = LocalAIConfig(retry_count=1)
        calls = {"n": 0}

        def flaky():
            calls["n"] += 1
            if calls["n"] == 1:
                raise ConnectionRefusedTransportError("temporary")
            return "ok"

        result = execute_with_retries(cfg, "probe", flaky)
        self.assertEqual(result, "ok")
        self.assertEqual(calls["n"], 2)


class TestTransportRun(unittest.TestCase):
    def test_end_to_end_mock_run(self):
        _task, _ctx, _prompt, _metrics, run_dir = _fresh_prepare()
        result = run_task(run_dir, mock=True)
        self.assertEqual(result.task.status, TaskStatus.RESPONSE_RECEIVED)
        self.assertTrue((run_dir / "raw_response.json").is_file())
        self.assertTrue((run_dir / "response.txt").is_file())
        self.assertTrue((run_dir / "transport_report.json").is_file())
        report = json.loads((run_dir / "transport_report.json").read_text(encoding="utf-8"))
        self.assertTrue(report["success"])
        self.assertNotIn("secret", json.dumps(report))

    def test_status_requirement(self):
        _task, _ctx, _prompt, _metrics, run_dir = _fresh_prepare()
        task_path = run_dir / "task.json"
        data = json.loads(task_path.read_text(encoding="utf-8"))
        data["status"] = "CREATED"
        task_path.write_text(json.dumps(data), encoding="utf-8")
        with self.assertRaises(TaskRunError):
            run_task(run_dir, mock=True)

    def test_no_overwrite_without_force(self):
        _task, _ctx, _prompt, _metrics, run_dir = _fresh_prepare()
        run_task(run_dir, mock=True)
        with self.assertRaises(TaskRunError):
            run_task(run_dir, mock=True)

    def test_force_allows_rerun(self):
        _task, _ctx, _prompt, _metrics, run_dir = _fresh_prepare()
        run_task(run_dir, mock=True)
        result = run_task(run_dir, mock=True, force=True)
        self.assertEqual(result.task.status, TaskStatus.RESPONSE_RECEIVED)

    def test_writes_only_inside_task_directory(self):
        _task, _ctx, _prompt, _metrics, run_dir = _fresh_prepare()
        task_dir = run_dir.resolve()
        runs_root = task_dir.parent.resolve()
        repo_root = REPO_ROOT.resolve()

        # String prefix checks are insufficient on Windows (backslashes) and for
        # decoy names such as ".local_ai_runs_evil/".
        decoy = (repo_root / ".local_ai_runs_evil" / "escape.txt").resolve()
        with self.assertRaises(ValueError):
            decoy.relative_to(runs_root)

        before = {p.resolve() for p in REPO_ROOT.rglob("*") if p.is_file()}
        run_task(run_dir, mock=True)
        after = {p.resolve() for p in REPO_ROOT.rglob("*") if p.is_file()}
        new_files = after - before
        self.assertTrue(new_files, "run should create transport artifacts")
        for path in new_files:
            assert_resolved_under(path, repo_root)
            assert_resolved_under(path, runs_root)
            assert_resolved_under(path, task_dir)


class TestDoctorTransport(unittest.TestCase):
    def test_doctor_ready_mock(self):
        from idne.local_ai.doctor import run_doctor

        report = run_doctor(start=REPO_ROOT, mock=True)
        self.assertIn(report.status, ("READY", "DEGRADED"))
        self.assertTrue(report.checks["adapter"]["reachable"])

    def test_doctor_completion_mock(self):
        from idne.local_ai.doctor import run_doctor

        report = run_doctor(start=REPO_ROOT, mock=True, test_completion=True)
        completion = report.checks.get("completion_test", {})
        self.assertTrue(completion.get("completion_successful"))


class TestCLI(unittest.TestCase):
    def test_models_mock(self):
        proc = subprocess.run(
            [sys.executable, "-m", "idne.local_ai", "models", "--mock"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(proc.returncode, 0, msg=proc.stderr)
        data = json.loads(proc.stdout)
        self.assertEqual(data["adapter"], "mock")

    def test_run_mock_cli(self):
        prep = subprocess.run(
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
        )
        self.assertEqual(prep.returncode, 0, msg=prep.stderr)
        run_dir = None
        for line in prep.stdout.splitlines():
            if line.startswith("Dir:"):
                run_dir = line.split(":", 1)[1].strip()
        self.assertIsNotNone(run_dir)
        proc = subprocess.run(
            [sys.executable, "-m", "idne.local_ai", "run", run_dir, "--mock", "--force"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(proc.returncode, 0, msg=proc.stderr)
        self.assertIn("RESPONSE_RECEIVED", proc.stdout)


if __name__ == "__main__":
    unittest.main()
