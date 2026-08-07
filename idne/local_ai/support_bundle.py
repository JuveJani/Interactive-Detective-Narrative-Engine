"""Generate offline Local AI diagnostic support bundles."""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from idne.local_ai.attempts import active_attempt, list_attempts
from idne.local_ai.config import endpoint_for_display, load_config, resolve_api_token
from idne.local_ai.doctor import run_doctor
from idne.local_ai.paths import find_repo_root, to_posix_relpath
from idne.local_ai.platform_runtime import detect_platform_runtime, local_ai_runs_root
from idne.local_ai.run_state import load_status, load_task
from idne.local_ai.task_model import compute_run_definition_identity

SUPPORT_ROOT = ".local_ai_support"
ARTIFACT_NAMES = (
    "apply_report.json",
    "context_manifest.json",
    "diagnostics.json",
    "parsed_response.json",
    "prompt.txt",
    "request.json",
    "response.txt",
    "response_parse_report.json",
    "response_validation_report.json",
    "status.json",
    "task.json",
    "transport_report.json",
)
PROPOSAL_ARTIFACTS = (
    "proposal/adventure_brief.json",
    "proposal/human_review.md",
    "proposal/proposal_manifest.json",
    "proposal/provenance.json",
    "proposal/validation_report.json",
)
SECRET_KEY_PATTERN = re.compile(r"(token|secret|password|api[_-]?key|authorization)", re.I)
TOKEN_LIKE = re.compile(r"^[A-Za-z0-9_\-]{20,}$")


def redact_value(key: str, value: Any) -> Any:
    if isinstance(value, dict):
        return redact_mapping(value)
    if isinstance(value, list):
        return [redact_value(key, item) for item in value]
    if isinstance(value, str):
        lower = key.lower()
        if SECRET_KEY_PATTERN.search(lower):
            return "[REDACTED]"
        if lower in {"authorization", "api_key", "apikey"}:
            return "[REDACTED]"
        if "bearer " in value.lower():
            return "[REDACTED]"
    return value


def redact_mapping(data: dict[str, Any]) -> dict[str, Any]:
    redacted: dict[str, Any] = {}
    for key in sorted(data.keys()):
        redacted[key] = redact_value(key, data[key])
    return redacted


def redact_config_dict(cfg_dict: dict[str, Any]) -> dict[str, Any]:
    out = redact_mapping(dict(cfg_dict))
    token_env = str(out.get("api_token_env", "LM_STUDIO_API_TOKEN"))
    if os.environ.get(token_env):
        out["api_token_env_set"] = True
        out["api_token_present"] = True
    else:
        out["api_token_env_set"] = bool(os.environ.get(token_env))
        out["api_token_present"] = False
    return out


def _git_info(repo_root: Path) -> dict[str, Any]:
    try:
        head = subprocess.run(
            ["git", "-C", str(repo_root), "rev-parse", "HEAD"],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=10,
        )
        status = subprocess.run(
            ["git", "-C", str(repo_root), "status", "--porcelain"],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return {"available": False, "error": str(exc)}
    if head.returncode != 0:
        return {"available": False, "error": (head.stderr or head.stdout).strip()}
    lines = [line for line in status.stdout.splitlines() if line.strip()]
    return {
        "available": True,
        "commit": head.stdout.strip(),
        "commit_short": head.stdout.strip()[:8],
        "dirty": bool(lines),
        "changed_files": len(lines),
    }


def _repo_rel(path: Path, repo_root: Path) -> str:
    try:
        return to_posix_relpath(path.resolve(), repo_root.resolve())
    except ValueError:
        return path.as_posix()


def _read_json(path: Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    return data if isinstance(data, dict) else {"value": data}


def _artifact_summary(run_dir: Path | None) -> dict[str, bool]:
    summary: dict[str, bool] = {}
    names = list(ARTIFACT_NAMES) + list(PROPOSAL_ARTIFACTS)
    if run_dir is None:
        return {name: False for name in names}
    for name in sorted(names):
        summary[name] = (run_dir / name).is_file()
    summary["raw_response.json"] = (run_dir / "raw_response.json").is_file()
    summary["attempts/"] = (run_dir / "attempts").is_dir()
    summary["proposal/"] = (run_dir / "proposal").is_dir()
    return summary


def _last_error(run_dir: Path | None, status: dict[str, Any] | None) -> dict[str, Any] | None:
    if run_dir is None:
        return None
    diagnostics = _read_json(run_dir / "diagnostics.json") or {}
    failure = diagnostics.get("last_transport_failure")
    if isinstance(failure, dict):
        return {
            "source": "diagnostics.last_transport_failure",
            "classification": failure.get("classification"),
            "message": failure.get("message"),
        }
    transport = _read_json(run_dir / "transport_report.json") or {}
    if transport.get("success") is False:
        return {
            "source": "transport_report.json",
            "classification": transport.get("classification"),
            "message": transport.get("message"),
        }
    if status:
        for report_name in ("response_validation_report.json", "proposal/validation_report.json"):
            report = _read_json(run_dir / report_name)
            if report and report.get("passed") is False:
                return {
                    "source": report_name,
                    "classification": "validation_failed",
                    "message": str(report.get("findings", report.get("findings", [])))[:500],
                }
    return None


def _bundle_id(task_id: str | None, git_short: str | None) -> str:
    safe_task = (task_id or "environment").replace("/", "_")
    safe_git = git_short or "nogit"
    return f"{safe_task}_{safe_git}"


def _copy_artifact(src: Path, dest: Path, *, redact_json: bool = False) -> None:
    if not src.is_file():
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    if redact_json and src.suffix.lower() == ".json":
        data = _read_json(src)
        if data is not None:
            dest.write_text(
                json.dumps(redact_mapping(data), indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            return
    shutil.copy2(src, dest)


def generate_support_bundle(
    task_directory: Path | None = None,
    *,
    config_path: Path | None = None,
    repo_root: Path | None = None,
    mock: bool = False,
) -> Path:
    root = repo_root or find_repo_root(task_directory)
    runtime = detect_platform_runtime(root)
    git = _git_info(root)
    cfg = load_config(config_path=config_path, repo_root=root)
    cfg_dict = redact_config_dict(cfg.to_dict())
    token_env = cfg.api_token_env
    if resolve_api_token(cfg):
        cfg_dict["api_token_present"] = True
    cfg_dict["api_token_env"] = token_env

    run_dir = task_directory.resolve() if task_directory else None
    task = None
    status: dict[str, Any] | None = None
    if run_dir is not None:
        if not run_dir.is_dir():
            raise FileNotFoundError(f"not a task directory: {run_dir}")
        task = load_task(run_dir)
        status = load_status(run_dir)

    bundle_id = _bundle_id(task.task_id if task else None, git.get("commit_short"))
    bundle_dir = root / SUPPORT_ROOT / bundle_id
    artifacts_dir = bundle_dir / "artifacts"
    if bundle_dir.exists():
        shutil.rmtree(bundle_dir)
    bundle_dir.mkdir(parents=True)
    artifacts_dir.mkdir()

    doctor = run_doctor(
        start=root,
        config_path=config_path,
        mock=mock,
        test_completion=False,
    )
    summary = _artifact_summary(run_dir)
    attempts = list_attempts(run_dir) if run_dir else []
    active = active_attempt(run_dir) if run_dir else "none"
    transport = _read_json(run_dir / "transport_report.json") if run_dir else None
    last_error = _last_error(run_dir, status)

    environment = {
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "platform": runtime.to_dict(),
        "python_version": sys.version.split()[0],
        "git": git,
        "config_effective": cfg_dict,
        "adapter": cfg.adapter_type,
        "endpoint": endpoint_for_display(cfg.base_url),
        "configured_model": cfg.model,
        "doctor_status": doctor.status,
        "doctor_messages": doctor.messages,
    }
    (bundle_dir / "environment.json").write_text(
        json.dumps(environment, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    if run_dir:
        for name in sorted(set(ARTIFACT_NAMES) | {"raw_response.json"}):
            _copy_artifact(
                run_dir / name,
                artifacts_dir / name,
                redact_json=name in {"request.json", "transport_report.json"},
            )
        for name in PROPOSAL_ARTIFACTS:
            _copy_artifact(run_dir / name, artifacts_dir / name, redact_json=name.endswith(".json"))

    artifact_summary = {
        "task_directory": _repo_rel(run_dir, root) if run_dir else None,
        "artifacts": summary,
    }
    (bundle_dir / "artifact_summary.json").write_text(
        json.dumps(artifact_summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    reasoning_meta = {
        "reasoning_present": transport.get("reasoning_present") if transport else None,
        "reasoning_character_count": transport.get("reasoning_character_count") if transport else None,
        "finish_reason": transport.get("finish_reason") if transport else None,
    }

    task_identity: dict[str, Any] | None = None
    if task:
        task_identity = {
            "source_content_identity": task.source_content_identity.to_dict(),
            "run_definition_identity": compute_run_definition_identity(task),
        }

    manifest = {
        "bundle_id": bundle_id,
        "task_id": task.task_id if task else None,
        "task_status": task.status.value if task else None,
        "processing_stage": status.get("processing_stage") if status else None,
        "task_identity": task_identity,
        "active_attempt": active,
        "attempt_count_archived": len(attempts),
        "reasoning_metadata": reasoning_meta,
        "last_error": last_error,
        "support_root": SUPPORT_ROOT,
        "bundle_path": _repo_rel(bundle_dir, root),
    }
    (bundle_dir / "bundle_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    report_lines = [
        "# Local AI Support Bundle",
        "",
        f"Generated: {environment['generated_at']}",
        f"Bundle: `{manifest['bundle_path']}`",
        "",
        "## Summary",
        f"- Task ID: {manifest['task_id'] or '(none)'}",
        f"- Task status: {manifest['task_status'] or '(none)'}",
        f"- Processing stage: {manifest['processing_stage'] or 'NONE'}",
        f"- Active attempt: {active}",
        f"- Git commit: {git.get('commit', '(unknown)')}",
        f"- Git dirty: {git.get('dirty', '(unknown)')}",
        "",
        "## Environment",
        f"- Platform: {runtime.platform_name}",
        f"- Python: {sys.version.split()[0]}",
        f"- Adapter: {cfg.adapter_type}",
        f"- Endpoint: {endpoint_for_display(cfg.base_url)}",
        f"- Configured model: {cfg.model or '(auto-select)'}",
        f"- Doctor status: {doctor.status}",
        "",
        "## Reasoning metadata",
        f"- reasoning_present: {reasoning_meta['reasoning_present']}",
        f"- reasoning_character_count: {reasoning_meta['reasoning_character_count']}",
        f"- finish_reason: {reasoning_meta['finish_reason']}",
        "",
        "Note: `reasoning_content` is diagnostic metadata only and is never written to `response.txt` or proposals.",
        "",
        "## Last error",
    ]
    if last_error:
        report_lines.extend(
            [
                f"- Source: {last_error.get('source')}",
                f"- Classification: {last_error.get('classification')}",
                f"- Message: {last_error.get('message')}",
            ]
        )
    else:
        report_lines.append("- (none recorded)")

    report_lines.extend(["", "## Artifact presence", ""])
    for name in sorted(summary.keys()):
        mark = "yes" if summary[name] else "no"
        report_lines.append(f"- {name}: {mark}")

    report_lines.extend(
        [
            "",
            "## Useful paths",
            f"- Runs root: `{_repo_rel(local_ai_runs_root(root), root)}`",
            f"- Example config: `OFFLINE_AI/local_ai.example.toml`",
            f"- User config: `local_ai.toml` (gitignored, never overwritten)",
            f"- User guide: `OFFLINE_AI/USER_GUIDE.md`",
            f"- Support guide: `OFFLINE_AI/LOCAL_AI_SUPPORT.md`",
        ]
    )
    if run_dir:
        report_lines.append(f"- Task directory: `{_repo_rel(run_dir, root)}`")

    (bundle_dir / "REPORT.md").write_text("\n".join(report_lines) + "\n", encoding="utf-8")
    return bundle_dir
