"""Deterministic context package builder for Local AI tasks."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from idne.local_ai.paths import resolve_allowed_file
from idne.local_ai.task_model import AuthoritativeSource, sha256_text


APPROX_CHARS_PER_TOKEN = 4


@dataclass(frozen=True)
class AuthoritativeFileSpec:
    path: str
    authority_rank: int
    kind: str
    excerpt_start: str | None = None
    excerpt_end: str | None = None


@dataclass
class ContextSection:
    label: str
    path: str
    authority_rank: int
    kind: str
    heading: str
    content: str

    @property
    def char_count(self) -> int:
        return len(self.content)


@dataclass
class ContextBuildResult:
    sections: list[ContextSection] = field(default_factory=list)
    context_text: str = ""
    character_count: int = 0
    approximate_tokens: int = 0
    files_read: int = 0
    bytes_read: int = 0
    blocked: bool = False
    block_reason: str = ""
    overflow_source: str = ""
    authoritative_sources: list[AuthoritativeSource] = field(default_factory=list)

    def to_manifest(self) -> dict[str, Any]:
        return {
            "files_read": self.files_read,
            "bytes_read": self.bytes_read,
            "character_count": self.character_count,
            "approximate_tokens": self.approximate_tokens,
            "approximation_rule": f"characters / {APPROX_CHARS_PER_TOKEN}",
            "blocked": self.blocked,
            "block_reason": self.block_reason,
            "overflow_source": self.overflow_source,
            "sections": [
                {
                    "label": s.label,
                    "path": s.path,
                    "authority_rank": s.authority_rank,
                    "kind": s.kind,
                    "heading": s.heading,
                    "char_count": s.char_count,
                }
                for s in self.sections
            ],
            "authoritative_sources": [s.to_dict() for s in self.authoritative_sources],
        }


def estimate_tokens(char_count: int) -> int:
    return max(1, char_count // APPROX_CHARS_PER_TOKEN)


def extract_heading_excerpt(text: str, start_heading: str, end_heading: str | None) -> tuple[str, str]:
    lines = text.splitlines()
    start_idx = None
    for idx, line in enumerate(lines):
        if line.strip().startswith(start_heading):
            start_idx = idx
            break
    if start_idx is None:
        return start_heading, text
    end_idx = len(lines)
    if end_heading:
        for idx in range(start_idx + 1, len(lines)):
            if lines[idx].strip().startswith(end_heading):
                end_idx = idx
                break
    excerpt = "\n".join(lines[start_idx:end_idx]).strip()
    return start_heading, excerpt


def build_context_package(
    repo_root: Path,
    input_files: list[str],
    authoritative_specs: list[AuthoritativeFileSpec],
    *,
    context_budget: int,
) -> ContextBuildResult:
    """Build deterministic context from explicit allowlisted files only."""
    result = ContextBuildResult()
    sections: list[ContextSection] = []

    for rel in input_files:
        path = resolve_allowed_file(rel, repo_root)
        raw = path.read_text(encoding="utf-8")
        result.files_read += 1
        result.bytes_read += len(raw.encode("utf-8"))
        sections.append(
            ContextSection(
                label=f"INPUT: {rel}",
                path=rel,
                authority_rank=0,
                kind="author_input",
                heading="(complete file)",
                content=raw.strip(),
            )
        )

    for spec in sorted(authoritative_specs, key=lambda s: (s.authority_rank, s.path)):
        path = resolve_allowed_file(spec.path, repo_root)
        raw = path.read_text(encoding="utf-8")
        result.files_read += 1
        result.bytes_read += len(raw.encode("utf-8"))
        if spec.excerpt_start:
            heading, content = extract_heading_excerpt(raw, spec.excerpt_start, spec.excerpt_end)
        else:
            heading, content = "(complete file)", raw.strip()
        sections.append(
            ContextSection(
                label=f"AUTHORITY[{spec.authority_rank}] {spec.path}",
                path=spec.path,
                authority_rank=spec.authority_rank,
                kind=spec.kind,
                heading=heading,
                content=content,
            )
        )

    parts: list[str] = []
    running_chars = 0
    for section in sections:
        block = f"=== {section.label} ===\nSource: {section.path}\nHeading: {section.heading}\n\n{section.content}\n"
        next_total = running_chars + len(block)
        if next_total > context_budget:
            result.blocked = True
            result.block_reason = "context budget exceeded"
            result.overflow_source = section.path
            break
        parts.append(block)
        running_chars = next_total
        if section.authority_rank > 0:
            result.authoritative_sources.append(
                AuthoritativeSource(
                    path=section.path,
                    authority_rank=section.authority_rank,
                    kind=section.kind,
                    heading=section.heading,
                    char_count=len(section.content),
                    excerpt_chars=len(section.content),
                )
            )

    result.sections = sections[: len(parts)]
    result.context_text = "\n".join(parts).strip()
    result.character_count = len(result.context_text)
    result.approximate_tokens = estimate_tokens(result.character_count)
    return result
