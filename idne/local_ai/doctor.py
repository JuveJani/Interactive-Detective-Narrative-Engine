"""Environment diagnostics for Local AI orchestrator."""

from __future__ import annotations

import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from idne.local_ai.config import LocalAIConfig, endpoint_for_display, load_config
from idne.local_ai.errors import ModelSelectionError, ReasoningWithoutContentTransportError, TransportError
from idne.local_ai.mock_adapter import doctor_completion
from idne.local_ai.model_adapter import create_adapter, select_model
from idne.local_ai.paths import find_repo_root, normalize_allowlist
from idne.local_ai.platform_runtime import detect_platform_runtime, local_ai_runs_root
from idne.local_ai.task_builder import TASK_DEFINITIONS


@dataclass
class DoctorReport:
    status: str
    checks: dict[str, Any]
    messages: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {"status": self.status, "checks": self.checks, "messages": self.messages}


def _utf8_roundtrip_check(base: Path) -> bool:
    probe = base / ".idne_utf8_probe.txt"
    sample = "IDNE UTF-8 probe: árvíztűrő tükörfúrógép — 日本語 — emoji ✓"
    try:
        probe.write_text(sample, encoding="utf-8")
        return probe.read_text(encoding="utf-8") == sample
    except OSError:
        return False
    finally:
        probe.unlink(missing_ok=True)


def _deterministic_ordering_check(base: Path) -> bool:
    root = base / ".idne_order_probe"
    try:
        root.mkdir(parents=True, exist_ok=True)
        names = ["b.txt", "a.txt", "c.txt"]
        for name in names:
            (root / name).write_text(name, encoding="utf-8")
        ordered = sorted(p.name for p in root.iterdir() if p.is_file())
        return ordered == sorted(names)
    except OSError:
        return False
    finally:
        import shutil

        shutil.rmtree(root, ignore_errors=True)


def _git_status(repo_root: Path) -> dict[str, Any]:
    try:
        proc = subprocess.run(
            ["git", "-C", str(repo_root), "status", "--porcelain"],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return {"available": False, "error": str(exc)}
    if proc.returncode != 0:
        return {"available": False, "error": (proc.stderr or proc.stdout).strip()}
    lines = [line for line in proc.stdout.splitlines() if line.strip()]
    return {"available": True, "dirty": bool(lines), "changed_files": len(lines)}


def _adapter_checks(
    cfg: LocalAIConfig,
    *,
    mock: bool,
) -> dict[str, Any]:
    adapter = create_adapter(cfg, mock=mock)
    result: dict[str, Any] = {
        "adapter": adapter.name,
        "endpoint": endpoint_for_display(cfg.base_url),
        "endpoint_policy": "allowed",
        "configured_model": cfg.model,
        "connect_timeout_seconds": cfg.connect_timeout_seconds,
        "response_timeout_seconds": cfg.response_timeout_seconds,
        "max_output_tokens": cfg.max_output_tokens,
        "reachable": False,
        "available_models": [],
        "selected_model": None,
        "model_selection_status": "unknown",
    }
    try:
        models = adapter.list_models(cfg)
        result["reachable"] = True
        result["available_models"] = [m.model_id for m in models]
        selection = select_model(cfg, models)
        result["selected_model"] = selection.model_id
        result["model_selection_status"] = selection.reason
    except ModelSelectionError as exc:
        result["reachable"] = True
        result["model_selection_status"] = "blocked"
        result["model_selection_message"] = str(exc)
        result["available_models"] = exc.available_models
    except TransportError as exc:
        result["model_selection_status"] = "blocked"
        result["transport_error"] = {"classification": exc.classification, "message": str(exc)}
    return result


def run_doctor(
    start: Path | None = None,
    *,
    config_path: Path | None = None,
    mock: bool = False,
    test_completion: bool = False,
) -> DoctorReport:
    messages: list[str] = []
    checks: dict[str, Any] = {}
    blocked_reasons: list[str] = []
    degraded_reasons: list[str] = []

    runtime = detect_platform_runtime(start)
    checks["platform"] = runtime.to_dict()

    temp_writable = False
    try:
        probe = runtime.temp_directory / ".idne_local_ai_probe"
        probe.write_text("ok", encoding="utf-8")
        temp_writable = probe.read_text(encoding="utf-8") == "ok"
        probe.unlink(missing_ok=True)
    except OSError as exc:
        blocked_reasons.append(f"temp not writable: {exc}")
    checks["temp_writable"] = temp_writable
    if not temp_writable:
        blocked_reasons.append("temporary directory is not writable")

    runs_root = local_ai_runs_root(runtime.repo_root)
    runs_writable = False
    try:
        runs_root.mkdir(parents=True, exist_ok=True)
        probe = runs_root / ".doctor_probe"
        probe.write_text("ok", encoding="utf-8")
        runs_writable = probe.read_text(encoding="utf-8") == "ok"
        probe.unlink(missing_ok=True)
    except OSError as exc:
        blocked_reasons.append(f"run directory not writable: {exc}")
    checks["run_directory"] = {"path": runs_root.as_posix(), "writable": runs_writable}
    if not runs_writable:
        blocked_reasons.append("local AI run directory is not writable")

    checks["utf8_roundtrip"] = _utf8_roundtrip_check(
        runs_root if runs_writable else runtime.temp_directory
    )
    if not checks["utf8_roundtrip"]:
        blocked_reasons.append("UTF-8 read/write check failed")

    checks["deterministic_ordering"] = _deterministic_ordering_check(runtime.temp_directory)
    if not checks["deterministic_ordering"]:
        blocked_reasons.append("deterministic path ordering check failed")

    required_files: dict[str, bool] = {}
    for definition in TASK_DEFINITIONS.values():
        for spec in definition.authoritative_files:
            path = runtime.repo_root / spec.path
            required_files[spec.path] = path.is_file()
    checks["required_authoritative_files"] = required_files
    missing = [path for path, ok in required_files.items() if not ok]
    if missing:
        blocked_reasons.append(f"missing authoritative files: {', '.join(missing)}")

    git = _git_status(runtime.repo_root)
    checks["git"] = git
    if not git.get("available"):
        degraded_reasons.append("git unavailable — working tree status not reported")

    try:
        checks["path_normalization_sample"] = normalize_allowlist(["AGENTS.md"], runtime.repo_root)
    except Exception as exc:  # noqa: BLE001
        blocked_reasons.append(f"path normalization failed: {exc}")

    try:
        cfg = load_config(config_path=config_path, repo_root=runtime.repo_root)
        if mock:
            cfg.adapter_type = "mock"
        checks["config"] = cfg.to_dict()
        checks["adapter"] = _adapter_checks(cfg, mock=mock)
        adapter_info = checks["adapter"]
        if not adapter_info.get("reachable"):
            blocked_reasons.append("model server not reachable")
        elif adapter_info.get("model_selection_status") == "blocked":
            blocked_reasons.append(adapter_info.get("model_selection_message") or adapter_info.get("transport_error", {}).get("message", "model selection blocked"))
    except TransportError as exc:
        checks["adapter"] = {"transport_error": {"classification": exc.classification, "message": str(exc)}}
        blocked_reasons.append(str(exc))

    if test_completion:
        completion_check: dict[str, Any] = {"requested": True}
        try:
            cfg = load_config(config_path=config_path, repo_root=runtime.repo_root)
            if mock:
                cfg.adapter_type = "mock"
            start_time = time.perf_counter()
            result = doctor_completion(cfg, mock=mock)
            completion_check.update(
                {
                    "server_reachable": True,
                    "model_available": True,
                    "completion_successful": True,
                    "duration_seconds": time.perf_counter() - start_time,
                    "response_character_count": len(result.content),
                    "reasoning_present": result.reasoning_present,
                    "reasoning_character_count": result.reasoning_character_count,
                    "finish_reason": result.finish_reason,
                    "doctor_probe_max_tokens": cfg.doctor_probe_max_tokens,
                }
            )
        except TransportError as exc:
            failure: dict[str, Any] = {
                "server_reachable": exc.classification
                not in {"endpoint_rejected", "configuration_error"},
                "model_available": exc.classification != "model_selection_blocked",
                "completion_successful": False,
                "error": str(exc),
                "classification": exc.classification,
            }
            if isinstance(exc, ReasoningWithoutContentTransportError):
                failure["reasoning_present"] = True
                failure["reasoning_character_count"] = exc.reasoning_character_count
                failure["finish_reason"] = exc.finish_reason
            completion_check.update(failure)
            blocked_reasons.append(f"doctor completion failed: {exc}")
        checks["completion_test"] = completion_check

    if blocked_reasons:
        status = "BLOCKED"
        messages.extend(blocked_reasons)
    elif degraded_reasons:
        status = "DEGRADED"
        messages.extend(degraded_reasons)
    else:
        status = "READY"
        adapter_name = checks.get("adapter", {}).get("adapter", "unknown")
        messages.append(f"Local AI adapter ready ({adapter_name}).")

    return DoctorReport(status=status, checks=checks, messages=messages)


def format_doctor_report(report: DoctorReport) -> str:
    lines = [f"Status: {report.status}"]
    runtime = report.checks.get("platform", {})
    lines.append(f"Platform: {runtime.get('platform_name', '?')}")
    lines.append(f"Python: {runtime.get('python_version', '?')}")
    lines.append(f"Repo: {runtime.get('repo_root', '?')}")
    lines.append(f"Runs: {report.checks.get('run_directory', {}).get('path', '?')}")
    adapter = report.checks.get("adapter", {})
    if adapter:
        lines.append(f"Adapter: {adapter.get('adapter', '?')}")
        lines.append(f"Endpoint: {adapter.get('endpoint', '?')}")
        lines.append(f"Reachable: {adapter.get('reachable', False)}")
        if adapter.get("selected_model"):
            lines.append(f"Model: {adapter.get('selected_model')}")
        if adapter.get("available_models"):
            lines.append(f"Models: {', '.join(adapter['available_models'])}")
    completion = report.checks.get("completion_test")
    if completion:
        lines.append(
            f"Completion: {'OK' if completion.get('completion_successful') else 'FAIL'} "
            f"({completion.get('duration_seconds', '?')}s)"
        )
    for message in report.messages:
        lines.append(f"- {message}")
    return "\n".join(lines)
