"""Parse model responses into structured JSON."""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from idne.local_ai.run_state import load_status, load_task, write_json
from idne.local_ai.structural_repair import RepairRecord, apply_safe_repairs
from idne.local_ai.task_model import ProcessingStage, TaskStatus, transition_processing_stage

MAX_RESPONSE_CHARS = 256_000


class ParseError(RuntimeError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


@dataclass
class ParseResult:
    parsed: dict[str, Any]
    repairs: list[RepairRecord]
    original_sha256: str
    parsed_sha256: str
    duration_seconds: float
    extraction_method: str


def _duplicate_key_hook(duplicates: list[str]):
    def hook(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        seen: set[str] = set()
        for key, _value in pairs:
            if key in seen:
                duplicates.append(key)
            seen.add(key)
        return dict(pairs)

    return hook


def _find_json_objects(text: str) -> list[tuple[int, int, str]]:
    objects: list[tuple[int, int, str]] = []
    i = 0
    n = len(text)
    while i < n:
        if text[i] != "{":
            i += 1
            continue
        depth = 0
        in_string = False
        escape = False
        start = i
        for j in range(i, n):
            ch = text[j]
            if in_string:
                if escape:
                    escape = False
                elif ch == "\\":
                    escape = True
                elif ch == '"':
                    in_string = False
                continue
            if ch == '"':
                in_string = True
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    objects.append((start, j + 1, text[start : j + 1]))
                    break
        i += 1
    return objects


def extract_json_candidate(text: str) -> tuple[str, str]:
    stripped = text.strip()
    objects = _find_json_objects(stripped)
    if len(objects) > 1:
        raise ParseError("multiple_json_objects", f"found {len(objects)} JSON objects; refusing to choose")
    if stripped.startswith("{") and stripped.endswith("}") and len(objects) == 1:
        start, end, _candidate = objects[0]
        if start == 0 and end == len(stripped):
            return stripped, "plain_json"
    if not objects:
        raise ParseError("no_json_object", "no JSON object found in response")
    start, end, candidate = objects[0]
    prefix = text[:start].strip()
    suffix = text[end:].strip()
    if prefix or suffix:
        if len(prefix) > 500 or len(suffix) > 500:
            raise ParseError("commentary_too_long", "surrounding commentary exceeds allowed bounds")
        return candidate, "commentary_extract"
    return candidate, "plain_json"


def parse_json_object(text: str) -> dict[str, Any]:
    duplicates: list[str] = []
    try:
        value = json.loads(text, object_pairs_hook=_duplicate_key_hook(duplicates))
    except json.JSONDecodeError as exc:
        raise ParseError("malformed_json", f"malformed JSON: {exc}") from exc
    if duplicates:
        raise ParseError("duplicate_keys", f"duplicate keys: {', '.join(sorted(set(duplicates)))}")
    if isinstance(value, list):
        raise ParseError("top_level_array", "top-level JSON array is not supported")
    if not isinstance(value, dict):
        raise ParseError("unsupported_top_level", "top-level JSON must be an object")
    return value


def parse_response(run_dir: Path) -> ParseResult:
    from idne.local_ai.task_model import sha256_text

    start = time.perf_counter()
    task = load_task(run_dir)
    status = load_status(run_dir)
    stage = status.get("processing_stage", ProcessingStage.NONE.value)
    if task.status != TaskStatus.RESPONSE_RECEIVED:
        raise ParseError("invalid_status", f"task status {task.status.value} cannot be parsed")
    if stage not in {ProcessingStage.NONE.value, ProcessingStage.PARSED.value}:
        raise ParseError(
            "invalid_stage",
            f"processing stage {stage} cannot be re-parsed without a new model response",
        )

    response_path = run_dir / "response.txt"
    if not response_path.is_file():
        raise ParseError("missing_response", "response.txt missing")
    raw = response_path.read_text(encoding="utf-8")
    if not raw.strip():
        raise ParseError("empty_response", "response is empty")
    if len(raw) > MAX_RESPONSE_CHARS:
        raise ParseError("response_too_large", f"response exceeds {MAX_RESPONSE_CHARS} characters")

    original_sha256 = sha256_text(raw)
    repair_result = apply_safe_repairs(raw)
    candidate, extraction_method = extract_json_candidate(repair_result.text)
    parsed = parse_json_object(candidate)
    normalized = json.dumps(parsed, indent=2, sort_keys=True) + "\n"
    parsed_sha256 = sha256_text(normalized)
    duration = time.perf_counter() - start

    write_json(
        run_dir / "response_parse_report.json",
        {
            "success": True,
            "original_sha256": original_sha256,
            "parsed_sha256": parsed_sha256,
            "extraction_method": extraction_method,
            "repairs": [{"code": r.code, "detail": r.detail} for r in repair_result.repairs],
            "duration_seconds": duration,
        },
    )
    (run_dir / "parsed_response.json").write_text(normalized, encoding="utf-8")
    transition_processing_stage(run_dir, ProcessingStage.PARSED)
    return ParseResult(
        parsed=parsed,
        repairs=repair_result.repairs,
        original_sha256=original_sha256,
        parsed_sha256=parsed_sha256,
        duration_seconds=duration,
        extraction_method=extraction_method,
    )
