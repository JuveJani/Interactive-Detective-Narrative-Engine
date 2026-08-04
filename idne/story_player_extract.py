"""PLAYER text extraction for Story Validator (Milestone 8)."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

ACRONYM_RE = re.compile(r"\b[A-Z]{2,}\b")
SENTENCE_SPLIT_RE = re.compile(r"[.!?]+")
WORD_RE = re.compile(r"\b\w+\b")


def collect_player_files(root: Path, rel_paths: list[str]) -> dict[str, str]:
    """Return mapping of relative path → text for existing PLAYER files."""
    out: dict[str, str] = {}
    for rel in rel_paths:
        path = root / rel
        if path.exists() and path.is_file():
            out[rel] = path.read_text(encoding="utf-8")
    return out


def scan_plain_language(
    text: str,
    known_acronyms: set[str],
    entity_aliases: dict[str, list[str]],
    long_sentence_threshold: int = 45,
) -> dict[str, Any]:
    """Measurable plain-language signals on prose."""
    sentences = [s.strip() for s in SENTENCE_SPLIT_RE.split(text) if s.strip()]
    long_sentences = []
    for s in sentences:
        words = WORD_RE.findall(s)
        if len(words) > long_sentence_threshold:
            long_sentences.append(s[:120])

    acronyms_found = sorted({m for m in ACRONYM_RE.findall(text) if m not in known_acronyms})

    inconsistent_names: list[str] = []
    for canonical, aliases in entity_aliases.items():
        present = [a for a in aliases if a.lower() in text.lower()]
        if len(present) >= 2:
            # all aliases should appear if any appear — flag partial usage in same doc
            if len(present) < len(aliases) and canonical.lower() not in text.lower():
                inconsistent_names.append(canonical)

    ambiguous_pronouns = bool(re.search(r"\b(he|she|they|it)\b", text, re.I)) and len(sentences) > 3

    return {
        "very_long_sentences": bool(long_sentences),
        "long_sentence_samples": long_sentences[:3],
        "undefined_acronyms": acronyms_found,
        "inconsistent_entity_names": inconsistent_names,
        "ambiguous_pronouns": ambiguous_pronouns,
        "word_count": len(WORD_RE.findall(text)),
    }


def opening_communicates_frame(opening_text: str, frame: dict[str, Any]) -> bool:
    """Heuristic: opening mentions incident, timing, and investigator role."""
    text = opening_text.lower()
    checks = 0
    for key in (
        "investigation_starts_where",
        "investigation_starts_when",
        "incident_description",
        "incident_when",
        "investigator_involvement",
    ):
        val = str(frame.get(key, "")).lower()
        if val and any(token in text for token in val.split()[:3] if len(token) > 3):
            checks += 1
    return checks >= 3
