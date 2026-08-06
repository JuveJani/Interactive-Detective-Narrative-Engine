#!/usr/bin/env python3
"""Restore English unit markers in Hungarian PLAYER markdown from source."""

from __future__ import annotations

import re
from pathlib import Path

EN = Path("adventures/The_Cold_Storage_Alarm/adventure/PLAYER")
HU = Path("adventures/A_Hutoriasztas/adventure/PLAYER")

MARKER_ANY = re.compile(r"<!--\s*unit:[^>]+-->", re.I)
MARKER_SLUG = re.compile(r"<!--\s*unit:([a-z0-9_-]+)\s*-->", re.I)
SKIP = {"HOW_TO_PLAY.md", "README.md", "OPENING.md", "NAVIGATION_INDEX.md", "GAMEBOOK.md"}


def english_slugs(path: Path) -> list[str]:
    return MARKER_SLUG.findall(path.read_text(encoding="utf-8"))


def main() -> None:
    total = 0
    for en_path in sorted(EN.rglob("*.md")):
        if en_path.name in SKIP:
            continue
        rel = en_path.relative_to(EN)
        hu_path = HU / rel
        if not hu_path.exists():
            continue
        en_m = english_slugs(en_path)
        text = hu_path.read_text(encoding="utf-8")
        idx = 0

        def repl(_: re.Match[str]) -> str:
            nonlocal idx
            if idx >= len(en_m):
                return _.group(0)
            out = f"<!-- unit:{en_m[idx]} -->"
            idx += 1
            return out

        new = MARKER_ANY.sub(repl, text)
        if new != text:
            hu_path.write_text(new, encoding="utf-8")
            print(f"restored {rel}: {idx} markers")
            total += idx
    print(f"total markers restored: {total}")


if __name__ == "__main__":
    main()
