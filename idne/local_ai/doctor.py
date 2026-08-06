"""Environment diagnostics for Local AI orchestrator Step 1."""

from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

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


def run_doctor(start: Path | None = None) -> DoctorReport:
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
    checks["run_directory"] = {
        "path": runs_root.as_posix(),
        "writable": runs_writable,
    }
    if not runs_writable:
        blocked_reasons.append("local AI run directory is not writable")

    utf8_ok = _utf8_roundtrip_check(runs_root if runs_writable else runtime.temp_directory)
    checks["utf8_roundtrip"] = utf8_ok
    if not utf8_ok:
        blocked_reasons.append("UTF-8 read/write check failed")

    ordering_ok = _deterministic_ordering_check(runtime.temp_directory)
    checks["deterministic_ordering"] = ordering_ok
    if not ordering_ok:
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
        sample = normalize_allowlist(["AGENTS.md"], runtime.repo_root)
        checks["path_normalization_sample"] = sample
    except Exception as exc:  # noqa: BLE001 — doctor must report, not crash
        blocked_reasons.append(f"path normalization failed: {exc}")

    if blocked_reasons:
        status = "BLOCKED"
        messages.extend(blocked_reasons)
    elif degraded_reasons:
        status = "DEGRADED"
        messages.extend(degraded_reasons)
    else:
        status = "READY"
        messages.append("Local AI deterministic core is ready (no model adapter configured).")

    return DoctorReport(status=status, checks=checks, messages=messages)


def format_doctor_report(report: DoctorReport) -> str:
    lines = [f"Status: {report.status}"]
    runtime = report.checks.get("platform", {})
    lines.append(f"Platform: {runtime.get('platform_name', '?')}")
    lines.append(f"Python: {runtime.get('python_version', '?')}")
    lines.append(f"Repo: {runtime.get('repo_root', '?')}")
    lines.append(f"Runs: {report.checks.get('run_directory', {}).get('path', '?')}")
    for message in report.messages:
        lines.append(f"- {message}")
    return "\n".join(lines)
