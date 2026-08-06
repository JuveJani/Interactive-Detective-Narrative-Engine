#!/usr/bin/env python3
"""Restore English choice lines in Hungarian PLAYER files for graph validation."""

from __future__ import annotations

import re
from pathlib import Path

EN = Path("adventures/The_Cold_Storage_Alarm/adventure/PLAYER")
HU = Path("adventures/A_Hutoriasztas/adventure/PLAYER")
SKIP = {"HOW_TO_PLAY.md", "README.md", "OPENING.md", "NAVIGATION_INDEX.md", "GAMEBOOK.md"}


def restore_choices(en_text: str, hu_text: str) -> str:
    en_lines = en_text.splitlines()
    hu_lines = hu_text.splitlines()
    if len(en_lines) != len(hu_lines):
        # block-wise restore within What do you do sections
        out = []
        en_i = 0
        hu_i = 0
        while hu_i < len(hu_lines):
            if hu_i < len(hu_lines) and en_i < len(en_lines) and en_lines[en_i].strip().startswith("- ") and hu_lines[hu_i].strip().startswith("- "):
                out.append(en_lines[en_i])
                en_i += 1
                hu_i += 1
            else:
                out.append(hu_lines[hu_i])
                if en_i < len(en_lines) and en_lines[en_i] == hu_lines[hu_i]:
                    en_i += 1
                hu_i += 1
        return "\n".join(out)

    out = []
    for el, hl in zip(en_lines, hu_lines):
        if el.strip().startswith("- ") and hl.strip().startswith("- "):
            out.append(el)
        else:
            out.append(hl)
    return "\n".join(out)


def main() -> None:
    count = 0
    for en_path in sorted(EN.rglob("*.md")):
        if en_path.name in SKIP:
            continue
        hu_path = HU / en_path.relative_to(EN)
        if not hu_path.exists():
            continue
        en_text = en_path.read_text(encoding="utf-8")
        hu_text = hu_path.read_text(encoding="utf-8")
        # Restore choice blocks after What do you do
        parts_en = en_text.split("**What do you do?**")
        parts_hu = hu_text.split("**What do you do?**")
        if len(parts_en) != len(parts_hu):
            continue
        merged = []
        for i, (pe, ph) in enumerate(zip(parts_en, parts_hu)):
            if i == 0:
                merged.append(ph)
            else:
                en_lines = pe.splitlines()
                hu_lines = ph.splitlines()
                block = []
                for el, hl in zip(en_lines, hu_lines):
                    if el.strip().startswith("- "):
                        block.append(el)
                    else:
                        block.append(hl)
                if len(en_lines) > len(hu_lines):
                    block.extend(en_lines[len(hu_lines):])
                merged.append("\n".join(block))
        new = "**What do you do?**".join(merged)
        if new != hu_text:
            hu_path.write_text(new, encoding="utf-8")
            count += 1
            print(f"restored choices in {en_path.name}")
    print(f"done {count} files")


if __name__ == "__main__":
    main()
