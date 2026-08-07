"""Regression tests for reasoning-capable LM Studio model compatibility."""

from __future__ import annotations

import json
import shutil
import unittest
from pathlib import Path
from unittest import mock

import idne.local_ai.mock_adapter as mock_adapter_module
from idne.local_ai.config import LocalAIConfig
from idne.local_ai.doctor import run_doctor
from idne.local_ai.errors import EmptyCompletionTransportError, ReasoningWithoutContentTransportError
from idne.local_ai.lm_studio_client import chat_completion, parse_completion_response
from idne.local_ai.mock_adapter import MockAdapter, MockAdapterState, doctor_completion
from idne.local_ai.output_paths import DEFAULT_BRIEF_OUTPUT
from idne.local_ai.response_parser import parse_response
from idne.local_ai.task_builder import prepare_task
from idne.local_ai.transport import run_task

REPO_ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_INPUT = "OFFLINE_AI/examples/adventure_brief_input.md"
REASONING_TEXT = "Internal chain-of-thought that must not become task output."


class TestReasoningCompletionParsing(unittest.TestCase):
    def test_normal_non_reasoning_completion(self):
        data = {
            "choices": [{"message": {"content": '{"ok": true}'}, "finish_reason": "stop"}],
            "usage": {"prompt_tokens": 1, "completion_tokens": 2, "total_tokens": 3},
        }
        parsed = parse_completion_response(data)
        self.assertEqual(parsed.content, '{"ok": true}')
        self.assertFalse(parsed.reasoning_present)

    def test_reasoning_with_valid_final_content(self):
        data = {
            "choices": [
                {
                    "message": {
                        "content": '{"status":"ok","probe":"doctor"}',
                        "reasoning_content": REASONING_TEXT,
                    },
                    "finish_reason": "stop",
                }
            ],
            "usage": {"prompt_tokens": 10, "completion_tokens": 40, "total_tokens": 50},
        }
        parsed = parse_completion_response(data)
        self.assertTrue(parsed.reasoning_present)
        self.assertEqual(parsed.reasoning_character_count, len(REASONING_TEXT))
        self.assertIn("probe", parsed.content)
        self.assertNotIn("chain-of-thought", parsed.content)

    def test_reasoning_with_blank_final_content(self):
        data = {
            "choices": [
                {
                    "message": {"content": "   ", "reasoning_content": REASONING_TEXT},
                    "finish_reason": "length",
                }
            ],
            "usage": {},
        }
        with self.assertRaises(ReasoningWithoutContentTransportError) as ctx:
            parse_completion_response(data)
        self.assertIn("reasoning produced but no final content", str(ctx.exception))
        self.assertEqual(ctx.exception.reasoning_character_count, len(REASONING_TEXT))
        self.assertEqual(ctx.exception.finish_reason, "length")

    def test_blank_content_without_reasoning(self):
        data = {
            "choices": [{"message": {"content": "   "}, "finish_reason": "stop"}],
            "usage": {},
        }
        with self.assertRaises(EmptyCompletionTransportError) as ctx:
            parse_completion_response(data)
        self.assertEqual(str(ctx.exception), "completion content is blank")


class TestDoctorReasoningProbe(unittest.TestCase):
    def test_doctor_probe_uses_configured_token_budget(self):
        cfg = LocalAIConfig(doctor_probe_max_tokens=256)
        seen: dict[str, int | None] = {}
        original_complete = MockAdapter.complete

        def capturing_complete(
            self,
            cfg,
            *,
            model,
            user_prompt,
            max_output_tokens=None,
            temperature=None,
        ):
            seen["max_output_tokens"] = max_output_tokens
            return original_complete(
                self,
                cfg,
                model=model,
                user_prompt=user_prompt,
                max_output_tokens=max_output_tokens,
                temperature=temperature,
            )

        with mock.patch.object(MockAdapter, "complete", capturing_complete):
            doctor_completion(cfg, mock=True)
        self.assertEqual(seen["max_output_tokens"], 256)

    def test_doctor_probe_reasoning_model_mock(self):
        cfg = LocalAIConfig()
        adapter = MockAdapter(MockAdapterState(scenario="reasoning_with_content"))
        with mock.patch.object(mock_adapter_module, "MockAdapter", return_value=adapter):
            result = doctor_completion(cfg, mock=True)
        self.assertTrue(result.reasoning_present)
        self.assertGreater(result.reasoning_character_count, 0)
        self.assertTrue(result.content.strip().startswith("{"))

    def test_doctor_reports_reasoning_without_content(self):
        cfg = LocalAIConfig()
        adapter = MockAdapter(MockAdapterState(scenario="reasoning_blank_content"))
        with mock.patch.object(mock_adapter_module, "MockAdapter", return_value=adapter):
            report = run_doctor(start=REPO_ROOT, mock=True, test_completion=True)
        completion = report.checks["completion_test"]
        self.assertFalse(completion["completion_successful"])
        self.assertEqual(completion["classification"], "reasoning_without_content")
        self.assertTrue(completion["reasoning_present"])
        self.assertIn("reasoning produced but no final content", completion["error"])


class TestReasoningTransportIntegration(unittest.TestCase):
    def setUp(self):
        from idne.local_ai.paths import normalize_allowlist, resolve_allowed_file, safe_task_directory_name
        from idne.local_ai.platform_runtime import local_ai_runs_root
        from idne.local_ai.task_model import make_task_id, sha256_bytes

        self._draft = REPO_ROOT / DEFAULT_BRIEF_OUTPUT
        if self._draft.is_file():
            self._draft.unlink()
        input_bytes = resolve_allowed_file(EXAMPLE_INPUT, REPO_ROOT).read_bytes()
        allowed = normalize_allowlist([EXAMPLE_INPUT], REPO_ROOT)
        task_id = make_task_id(
            "adventure_brief",
            allowed,
            [sha256_bytes(input_bytes)],
            [DEFAULT_BRIEF_OUTPUT],
        )
        self._run_dir = local_ai_runs_root(REPO_ROOT) / safe_task_directory_name(task_id)
        if self._run_dir.exists():
            shutil.rmtree(self._run_dir)

    def tearDown(self):
        if self._run_dir.exists():
            shutil.rmtree(self._run_dir)
        if self._draft.is_file():
            self._draft.unlink()

    def test_reasoning_not_written_to_response_txt(self):
        _task, _, _, _, run_dir = prepare_task(
            "adventure_brief",
            EXAMPLE_INPUT,
            repo_root=REPO_ROOT,
            output_path=DEFAULT_BRIEF_OUTPUT,
        )
        adapter = MockAdapter(MockAdapterState(scenario="reasoning_with_content"))
        with mock.patch("idne.local_ai.transport.create_adapter", return_value=adapter):
            run_task(run_dir, mock=True)

        response_text = (run_dir / "response.txt").read_text(encoding="utf-8")
        self.assertNotIn("chain-of-thought", response_text)
        self.assertNotIn("Thinking step by step", response_text)
        self.assertIn("premise", response_text)

        raw = json.loads((run_dir / "raw_response.json").read_text(encoding="utf-8"))
        self.assertIn("reasoning_content", raw["choices"][0]["message"])

        report = json.loads((run_dir / "transport_report.json").read_text(encoding="utf-8"))
        self.assertTrue(report["reasoning_present"])
        self.assertGreater(report["reasoning_character_count"], 0)
        self.assertEqual(report["finish_reason"], "stop")

    def test_response_parser_ignores_reasoning(self):
        _task, _, _, _, run_dir = prepare_task(
            "adventure_brief",
            EXAMPLE_INPUT,
            repo_root=REPO_ROOT,
            output_path=DEFAULT_BRIEF_OUTPUT,
        )
        adapter = MockAdapter(MockAdapterState(scenario="reasoning_with_content"))
        with mock.patch("idne.local_ai.transport.create_adapter", return_value=adapter):
            run_task(run_dir, mock=True)
        parse_response(run_dir)
        parsed = json.loads((run_dir / "parsed_response.json").read_text(encoding="utf-8"))
        self.assertIn("premise", parsed)
        self.assertNotIn("reasoning_content", parsed)

    def test_existing_non_reasoning_mock_behavior_unchanged(self):
        _task, _, _, _, run_dir = prepare_task(
            "adventure_brief",
            EXAMPLE_INPUT,
            repo_root=REPO_ROOT,
            output_path=DEFAULT_BRIEF_OUTPUT,
        )
        run_task(run_dir, mock=True)
        report = json.loads((run_dir / "transport_report.json").read_text(encoding="utf-8"))
        self.assertFalse(report["reasoning_present"])
        self.assertEqual(report["reasoning_character_count"], 0)


if __name__ == "__main__":
    unittest.main()
