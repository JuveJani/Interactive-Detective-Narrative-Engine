#!/usr/bin/env python3
"""Retranslate PLAYER files preserving unit-marker structure."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from regenerate_hungarian_mirror import enforce_informal, protect_paths_and_files, restore_paths, translate_text

EN_PLAYER = ROOT / "adventures" / "The_Cold_Storage_Alarm" / "adventure" / "PLAYER"
HU_PLAYER = ROOT / "adventures" / "A_Hutoriasztas" / "adventure" / "PLAYER"

MARKER = re.compile(r"(<!--\s*unit:[a-z0-9_-]+\s*-->)", re.I)


def translate_block(block: str) -> str:
    lines_out = []
    for line in block.splitlines():
        stripped = line.strip()
        if not stripped:
            lines_out.append("")
            continue
        if stripped == "**What do you do?**" or stripped == "**Scene transition**":
            lines_out.append(stripped)
            continue
        if line.startswith("### "):
            protected, pmap = protect_paths_and_files(line[4:])
            hu = translate_text(protected)
            lines_out.append(f"### {restore_paths(hu, pmap).strip()}")
            continue
        if line.startswith("- "):
            protected, pmap = protect_paths_and_files(line[2:])
            hu = translate_text(protected)
            lines_out.append(f"- {restore_paths(hu, pmap).strip()}")
            continue
        if line.startswith("**Time cost:**") or line.startswith("**Location:**") or line.startswith("**Check:**"):
            if "|" in line:
                left, right = line.split("|", 1)
                protected, pmap = protect_paths_and_files(right.strip())
                hu = translate_text(protected)
                lines_out.append(f"{left.strip()} | {restore_paths(hu, pmap).strip()}")
            else:
                protected, pmap = protect_paths_and_files(line)
                lines_out.append(restore_paths(translate_text(protected), pmap))
            continue
        protected, pmap = protect_paths_and_files(line)
        lines_out.append(restore_paths(translate_text(protected), pmap))
    return "\n".join(lines_out)


def retranslate_file(name: str) -> None:
    en = (EN_PLAYER / name).read_text(encoding="utf-8")
    tokens = MARKER.split(en)
    result: list[str] = []
    for i, tok in enumerate(tokens):
        if MARKER.fullmatch(tok):
            result.append(tok)
        elif i == 0:
            protected, pmap = protect_paths_and_files(tok)
            result.append(restore_paths(translate_text(protected), pmap))
        else:
            result.append(translate_block(tok))
    text = enforce_informal("".join(result))
    if not text.endswith("\n"):
        text += "\n"
    (HU_PLAYER / name).write_text(text, encoding="utf-8")
    print(f"retranslated {name}")


def main() -> None:
    for name in ["SCENES.md", "NPCS.md"]:
        retranslate_file(name)


if __name__ == "__main__":
    main()
