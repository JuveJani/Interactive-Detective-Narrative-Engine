"""Deterministic structural repairs for model responses."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any


@dataclass
class RepairRecord:
    code: str
    detail: str


@dataclass
class RepairResult:
    text: str
    repairs: list[RepairRecord] = field(default_factory=list)


def strip_bom(text: str) -> RepairResult:
    if text.startswith("\ufeff"):
        return RepairResult(text[1:], [RepairRecord("strip_bom", "removed UTF-8 BOM")])
    return RepairResult(text, [])


def trim_whitespace(text: str) -> RepairResult:
    stripped = text.strip()
    if stripped != text:
        return RepairResult(stripped, [RepairRecord("trim_whitespace", "trimmed leading/trailing whitespace")])
    return RepairResult(text, [])


def normalize_newlines(text: str) -> RepairResult:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    if normalized != text:
        return RepairResult(normalized, [RepairRecord("normalize_newlines", "normalized line endings to LF")])
    return RepairResult(text, [])


def remove_json_fence(text: str) -> RepairResult:
    match = re.fullmatch(r"\s*```(?:json)?\s*\n?(.*?)\n?```\s*", text, flags=re.DOTALL | re.IGNORECASE)
    if match:
        return RepairResult(
            match.group(1).strip(),
            [RepairRecord("remove_json_fence", "removed single Markdown JSON code fence")],
        )
    return RepairResult(text, [])


def apply_safe_repairs(raw: str) -> RepairResult:
    repairs: list[RepairRecord] = []
    current = raw
    for step in (strip_bom, normalize_newlines, trim_whitespace, remove_json_fence, trim_whitespace):
        result = step(current)
        current = result.text
        repairs.extend(result.repairs)
    return RepairResult(current, repairs)
