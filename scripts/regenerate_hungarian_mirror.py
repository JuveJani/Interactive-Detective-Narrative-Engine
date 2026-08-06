#!/usr/bin/env python3
"""Regenerate A hűtőriasztás Hungarian mirror from The Cold Storage Alarm."""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "adventures" / "The_Cold_Storage_Alarm"
TARGET = ROOT / "adventures" / "A_Hutoriasztas"

# Import glossary from sibling script
sys.path.insert(0, str(ROOT / "scripts"))
from translate_cold_storage_hu import (  # noqa: E402
    GLOSSARY,
    PROSE_KEYS,
    _apply_glossary,
    _protect_tokens,
    _restore_tokens,
    _should_skip_value,
    translate_json_value,
    translate_text,
)

PROTECTED_FILENAMES = {
    "GAMEBOOK.md", "HOW_TO_PLAY.md", "OPENING.md", "README.md", "NAVIGATION_INDEX.md",
    "LOCATIONS.md", "SCENES.md", "OBJECTS.md", "NPCS.md", "INFERENCE.md", "RECOVERY.md",
    "ENDINGS.md", "CASE_FILE.md", "CHARACTER_SHEET.md", "PLAY.md",
}

FORMAL_TO_INFORMAL = [
    (r"\bÖn\b", "te"),
    (r"\bÖnnek\b", "neked"),
    (r"\bÖnt\b", "téged"),
    (r"\bnyissa meg\b", "nyisd meg"),
    (r"\bválassza\b", "válassz"),
    (r"\bmenjen\b", "menj"),
    (r"\bvizsgálja meg\b", "vizsgáld meg"),
    (r"\bdobjon\b", "dobj"),
    (r"\blapozzon\b", "lapozz"),
    (r"\bjegyezze fel\b", "jegyezd fel"),
    (r"\bkezdje\b", "kezdd"),
    (r"\bolvassa\b", "olvasd"),
    (r"\bkövesse\b", "kövesd"),
]

SECTION_HEADING = re.compile(r"^## Section (\d+)\s*$", re.M)
TURN_TO_SUFFIX = re.compile(r"(?i)(\.?\s*Turn to section \*\*\d+\*\*\.?\s*)$")
CHECK_LINE = re.compile(
    r"(?i)^- If your roll \*\*(succeeds|fails)\*\*, turn to section \*\*\d+\*\*\.\s*$"
)
WHAT_DO_YOU_DO = "**What do you do?**"
STARTING_SECTION = re.compile(
    r"(\*\*Starting section: (\d+)\*\* — )turn to section \*\*(\d+)\*\*(.*)$",
    re.M,
)

PATH_PATTERN = re.compile(
    r"(?<![A-Za-z0-9_/])(PLAYER/[\w./-]+\.(?:md|json)|DO_NOT_READ/[\w./-]+|adventures/[\w./-]+|[\w-]+\.md)(?![A-Za-z0-9_])"
)


def protect_paths_and_files(text: str) -> tuple[str, dict[str, str]]:
    mapping: dict[str, str] = {}
    counter = 0

    def repl(m: re.Match[str]) -> str:
        nonlocal counter
        token = f"⟦PATH{counter}⟧"
        mapping[token] = m.group(0)
        counter += 1
        return token

    protected = PATH_PATTERN.sub(repl, text)
    for fn in sorted(PROTECTED_FILENAMES, key=len, reverse=True):
        if fn in protected:
            token = f"⟦FN{counter}⟧"
            mapping[token] = fn
            protected = protected.replace(fn, token)
            counter += 1
    return protected, mapping


def restore_paths(text: str, mapping: dict[str, str]) -> str:
    for token, original in mapping.items():
        text = text.replace(token, original)
    return text


def enforce_informal(text: str) -> str:
    for pattern, repl in FORMAL_TO_INFORMAL:
        text = re.sub(pattern, repl, text)
    return text


def translate_gamebook(content: str) -> str:
    """Translate GAMEBOOK prose while preserving machine-readable navigation markers."""
    lines_out: list[str] = []
    for line in content.splitlines():
        if SECTION_HEADING.match(line):
            lines_out.append(line)
            continue
        if line.strip() == WHAT_DO_YOU_DO:
            lines_out.append(WHAT_DO_YOU_DO)
            continue
        if CHECK_LINE.match(line):
            lines_out.append(line)
            continue
        m_start = STARTING_SECTION.match(line)
        if m_start:
            prefix, sec, _, tail = m_start.group(1), m_start.group(2), m_start.group(3), m_start.group(4)
            hu_tail = translate_text(tail.strip()) if tail.strip() else ""
            lines_out.append(
                f"**Kezdő szakasz: {sec}** — turn to section **{sec}**{(' ' + hu_tail) if hu_tail else ''}"
            )
            continue
        if line.strip().startswith("- ") and TURN_TO_SUFFIX.search(line):
            body = TURN_TO_SUFFIX.sub("", line).strip()
            suffix = TURN_TO_SUFFIX.search(line)
            nav = suffix.group(1).strip() if suffix else ""
            if body.startswith("- "):
                body = body[2:]
            protected, pmap = protect_paths_and_files(body)
            hu_body = translate_text(protected)
            hu_body = restore_paths(hu_body, pmap)
            lines_out.append(f"- {hu_body.strip()} {nav}".rstrip())
            continue
        if line.startswith("```"):
            lines_out.append(line)
            continue
        protected, pmap = protect_paths_and_files(line)
        hu = translate_text(protected) if line.strip() else line
        hu = restore_paths(hu, pmap)
        lines_out.append(hu)
    return "\n".join(lines_out) + ("\n" if content.endswith("\n") else "")


def translate_markdown_file(content: str, *, is_gamebook: bool = False) -> str:
    if is_gamebook:
        return translate_gamebook(content)
    parts = re.split(r"(```[\s\S]*?```)", content)
    out: list[str] = []
    for part in parts:
        if part.startswith("```"):
            out.append(part)
            continue
        protected, pmap = protect_paths_and_files(part)
        hu = translate_text(protected)
        hu = restore_paths(hu, pmap)
        out.append(hu)
    return enforce_informal("".join(out))


MANIFEST_TRANSLATABLE = {"label", "anchor"}


def translate_manifest(data: dict) -> dict:
    """Mirror English manifest structure; translate labels/anchors only."""
    out = json.loads(json.dumps(data))
    for uid, entry in out.get("units", {}).items():
        if "anchor" in entry and isinstance(entry["anchor"], str):
            entry["anchor"] = translate_text(entry["anchor"])
        for choice in entry.get("choices") or []:
            if "label" in choice and isinstance(choice["label"], str):
                choice["label"] = translate_text(choice["label"])
    return out


@dataclass
class Stats:
    translated_files: list[str] = field(default_factory=list)
    copied_unchanged: list[str] = field(default_factory=list)
    skipped_binary: list[str] = field(default_factory=list)
    translated_json: int = 0
    translated_md: int = 0
    source_words: int = 0
    target_words: int = 0
    errors: list[str] = field(default_factory=list)


def count_words(root: Path) -> int:
    total = 0
    for p in root.rglob("*"):
        if p.is_file() and p.suffix in {".md", ".json"} and not p.name.endswith(".idne"):
            if p.name.startswith("TRANSLATION_"):
                continue
            try:
                total += len(p.read_text(encoding="utf-8").split())
            except Exception:
                pass
    return total


def copy_translate_file(src: Path, dst: Path, stats: Stats) -> None:
    rel = src.relative_to(SOURCE)
    dst.parent.mkdir(parents=True, exist_ok=True)

    if src.suffix == ".idne":
        stats.skipped_binary.append(str(rel))
        return

    if rel.name == "player_mapping_manifest.json":
        data = json.loads(src.read_text(encoding="utf-8"))
        translated = translate_manifest(data)
        dst.write_text(json.dumps(translated, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        stats.translated_json += 1
        stats.translated_files.append(str(rel))
        return

    if src.suffix == ".json":
        data = json.loads(src.read_text(encoding="utf-8"))
        if rel.name == "generation_state.json":
            data["workspace_root"] = str(TARGET)
        translated = translate_json_value(None, data)
        dst.write_text(json.dumps(translated, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        json.loads(dst.read_text(encoding="utf-8"))
        stats.translated_json += 1
        stats.translated_files.append(str(rel))
        return

    if src.suffix == ".md":
        content = src.read_text(encoding="utf-8")
        is_gamebook = rel.name == "GAMEBOOK.md"
        hu = translate_markdown_file(content, is_gamebook=is_gamebook)
        hu = enforce_informal(hu)
        dst.write_text(hu, encoding="utf-8")
        stats.translated_md += 1
        stats.translated_files.append(str(rel))
        return

    shutil.copy2(src, dst)
    stats.copied_unchanged.append(str(rel))


def write_glossary() -> None:
    lines = [
        "# Glosszárium — A hűtőriasztás",
        "",
        "Következetes terminológia az angol forrás magyar tükörfordításához.",
        "",
        "| Angol | Magyar |",
        "|-------|--------|",
    ]
    for en, hu in GLOSSARY:
        lines.append(f"| {en} | {hu} |")
    lines.extend([
        "",
        "## Védett fájlnevek",
        "",
        "A játékosnak szóló utasításokban soha ne fordítsd le:",
        "",
    ])
    for fn in sorted(PROTECTED_FILENAMES):
        lines.append(f"- `{fn}`")
    lines.extend([
        "",
        "## Megszólítás",
        "",
        "Minden játékosnak szóló szövegben tegezés: nyisd meg, kezdd, válassz, menj.",
        "",
    ])
    (TARGET / "TRANSLATION_GLOSSARY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    t0 = time.time()
    stats = Stats()
    stats.source_words = count_words(SOURCE)

    if TARGET.exists():
        shutil.rmtree(TARGET)
    TARGET.mkdir(parents=True)

    files = sorted(p for p in SOURCE.rglob("*") if p.is_file())
    for i, src in enumerate(files):
        dst = TARGET / src.relative_to(SOURCE)
        try:
            copy_translate_file(src, dst, stats)
            if (i + 1) % 10 == 0:
                print(f"  [{i+1}/{len(files)}] {src.relative_to(SOURCE)}", flush=True)
        except Exception as exc:
            stats.errors.append(f"{src.relative_to(SOURCE)}: {exc}")

    # Title overrides for Hungarian adventure name in human titles only
    for md_path in TARGET.rglob("README.md"):
        t = md_path.read_text(encoding="utf-8")
        t = t.replace("The Cold Storage Alarm", "A hűtőriasztás")
        t = t.replace("Cold Storage Alarm", "A hűtőriasztás")
        md_path.write_text(t, encoding="utf-8")

    write_glossary()
    stats.target_words = count_words(TARGET)

    print(json.dumps({
        "translated_files": len(stats.translated_files),
        "translated_json": stats.translated_json,
        "translated_md": stats.translated_md,
        "source_words": stats.source_words,
        "target_words": stats.target_words,
        "errors": stats.errors,
        "elapsed_s": round(time.time() - t0, 1),
    }, indent=2))
    return 1 if stats.errors else 0


if __name__ == "__main__":
    sys.exit(main())
