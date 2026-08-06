#!/usr/bin/env python3
"""Validate Hungarian mirror against English source."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "adventures" / "The_Cold_Storage_Alarm"
TARGET = ROOT / "adventures" / "A_Hutoriasztas"

FORMAL_PATTERNS = [
    r"\bÖn\b", r"\bÖnnek\b", r"\bÖnt\b", r"\bnyissa\b", r"\bválassza\b",
    r"\bmenjen\b", r"\bvizsgálja\b", r"\bdobjon\b", r"\blapozzon\b", r"\bjegyezze\b",
]

TRANSLATED_FILENAMES = [
    "JÁTÉKKÖNYV", "HELYSZÍNEK", "JÁTSSZ", "NYITÁS", "VÉGEK", "TÁRGYAK", "NPC",
    "KÖVETKEZTETÉS", "HELYREÁLLÍTÁS", "JÁTÉKKÖNYV.md", "HELYSZÍNEK.md",
]

SECTION_HEADING = re.compile(r"^## Section (\d+)\s*$", re.M)
TURN_TO = re.compile(r"turn to section \*\*(\d+)\*\*", re.I)


def source_files() -> set[Path]:
    return {
        p.relative_to(SOURCE)
        for p in SOURCE.rglob("*")
        if p.is_file() and p.suffix != ".idne"
    }


def target_files() -> set[Path]:
    return {
        p.relative_to(TARGET)
        for p in TARGET.rglob("*")
        if p.is_file() and not p.name.startswith("TRANSLATION_")
    }


def extract_route_graph(gamebook: Path) -> dict[int, list[int]]:
    text = gamebook.read_text(encoding="utf-8")
    graph: dict[int, list[int]] = {}
    matches = list(SECTION_HEADING.finditer(text))
    for i, match in enumerate(matches):
        sec = int(match.group(1))
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        block = text[start:end]
        dests = [int(m.group(1)) for m in TURN_TO.finditer(block)]
        graph[sec] = sorted(set(dests))
    return graph


def check_json_preserve(src: Path, dst: Path, errors: list[str]) -> None:
    s = json.loads(src.read_text(encoding="utf-8"))
    t = json.loads(dst.read_text(encoding="utf-8"))

    def ids(obj, found=None):
        found = found or set()
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k in {"unit_id", "destination_unit_id", "ending_id", "adventure_id", "schema_version"}:
                    if isinstance(v, str):
                        found.add(v)
                if k == "public_section" and isinstance(v, int):
                    found.add(str(v))
                ids(v, found)
        elif isinstance(obj, list):
            for item in obj:
                ids(item, found)
        return found

    # Spot-check public_sections match
    if "public_sections" in s and "public_sections" in t:
        if s["public_sections"] != t["public_sections"]:
            errors.append(f"public_sections mismatch in {dst.name}")


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    src_set = source_files()
    tgt_set = target_files()
    extra = tgt_set - src_set
    missing = src_set - tgt_set
    if missing:
        errors.append(f"missing Hungarian files: {sorted(str(x) for x in missing)[:20]}")
    if extra:
        errors.append(f"stale extra files: {sorted(str(x) for x in extra)[:20]}")

    en_gb = SOURCE / "adventure" / "PLAYER" / "GAMEBOOK.md"
    hu_gb = TARGET / "adventure" / "PLAYER" / "GAMEBOOK.md"
    if not hu_gb.exists():
        errors.append("missing Hungarian GAMEBOOK.md")
    else:
        en_secs = set(SECTION_HEADING.findall(en_gb.read_text(encoding="utf-8")))
        hu_secs = set(SECTION_HEADING.findall(hu_gb.read_text(encoding="utf-8")))
        if en_secs != hu_secs:
            errors.append(f"section count mismatch EN={len(en_secs)} HU={len(hu_secs)}")
        if "636" not in hu_secs:
            errors.append("starting section 636 missing from Hungarian GAMEBOOK")
        en_graph = extract_route_graph(en_gb)
        hu_graph = extract_route_graph(hu_gb)
        for sec, dests in en_graph.items():
            if hu_graph.get(sec) != dests:
                errors.append(f"route mismatch section {sec}: EN={dests} HU={hu_graph.get(sec)}")
                if len(errors) > 15:
                    break

    for p in TARGET.rglob("*.json"):
        try:
            json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            errors.append(f"JSON parse fail {p.relative_to(TARGET)}: {e}")

    player_md = list((TARGET / "adventure" / "PLAYER").rglob("*.md"))
    for p in player_md:
        text = p.read_text(encoding="utf-8")
        for pat in FORMAL_PATTERNS:
            if re.search(pat, text):
                warnings.append(f"formal address pattern {pat} in {p.relative_to(TARGET)}")
        for bad in TRANSLATED_FILENAMES:
            if bad.endswith(".md"):
                if bad in text.replace("NPCS.md", "").replace("OBJECTS.md", ""):
                    errors.append(f"translated filename '{bad}' in {p.relative_to(TARGET)}")
            elif bad not in ("NPC",) and bad in text:
                errors.append(f"translated filename '{bad}' in {p.relative_to(TARGET)}")

    manifest = TARGET / "player_mapping_manifest.json"
    if manifest.exists():
        m = json.loads(manifest.read_text(encoding="utf-8"))
        if m.get("static_book", {}).get("start_section") != 636:
            errors.append("manifest start_section != 636")
        if m.get("schema_version") != "1.1":
            warnings.append(f"manifest schema {m.get('schema_version')}")

    result = {
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "warnings": warnings[:30],
        "source_file_count": len(src_set),
        "target_file_count": len(tgt_set),
        "section_count": len(hu_secs) if hu_gb.exists() else 0,
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
