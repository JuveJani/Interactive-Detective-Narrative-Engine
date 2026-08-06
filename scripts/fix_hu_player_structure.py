#!/usr/bin/env python3
"""Restore machine-readable structural markers in Hungarian PLAYER files."""

from __future__ import annotations

import re
from pathlib import Path

TARGET = Path(__file__).resolve().parents[1] / "adventures" / "A_Hutoriasztas" / "adventure" / "PLAYER"

STRUCTURAL_REPLACEMENTS = [
    (r"\*\*Mit csinálsz\?\*\*", "**What do you do?**"),
    (r"\*\*Mit teszel\?\*\*", "**What do you do?**"),
    (r"\*\*Helyszín:\*\*", "**Location:**"),
    (r"\*\*Időköltség:\*\*", "**Time cost:**"),
    (r"\*\*Ellenőrzés:\*\*", "**Check:**"),
    (r"\*\*Jelenet átmenet\*\*", "**Scene transition**"),
    (r"\*\*Scene transition\*\*", "**Scene transition**"),
]

INFORMAL_CHOICE_FIXES = [
    (r"^- Menjen ", "- Menj "),
    (r"^- Vágjon ", "- Vágj "),
    (r"^- Kérjen ", "- Kérj "),
    (r"^- Tekintse ", "- Tekintsd "),
    (r"^- Nyomja ", "- Nyomd "),
    (r"^- Szembesüljön ", "- Szembesülj "),
    (r"^- Térjen ", "- Térj "),
    (r"^- Folytassa ", "- Folytasd "),
    (r"^- Használja ", "- Használd "),
    (r"^- Olvassa ", "- Olvasd "),
    (r"^- Lapozzon ", "- Lapozz "),
]


def main() -> None:
    skip = {"GAMEBOOK.md", "HOW_TO_PLAY.md", "README.md", "OPENING.md", "NAVIGATION_INDEX.md"}
    count = 0
    for md in sorted(TARGET.rglob("*.md")):
        if md.name in skip:
            continue
        text = md.read_text(encoding="utf-8")
        original = text
        for pat, repl in STRUCTURAL_REPLACEMENTS:
            text = re.sub(pat, repl, text)
        for pat, repl in INFORMAL_CHOICE_FIXES:
            text = re.sub(pat, repl, text, flags=re.M)
        if text != original:
            md.write_text(text, encoding="utf-8")
            count += 1
            print(f"fixed {md.name}")
    print(f"done {count} files")


if __name__ == "__main__":
    main()
