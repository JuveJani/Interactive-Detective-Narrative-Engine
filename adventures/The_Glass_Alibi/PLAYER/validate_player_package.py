#!/usr/bin/env python3
"""Validate compiled PLAYER package structure for The Glass Alibi."""

from __future__ import annotations

import re
import sys
from pathlib import Path

PLAYER = Path(__file__).resolve().parent
REQUIRED = [
    "README.md",
    "SETUP.md",
    "HOW_TO_PLAY.md",
    "NAVIGATION_INDEX.md",
    "JOINT_SCENES.md",
    "BOOKLET_SYSTEMS.md",
    "BOOKLET_FIELD.md",
    "ENDINGS.md",
    "SHARED/CASE_FILE.md",
    "CHARACTERS/CHARACTER_SHEET_SYSTEMS.md",
    "CHARACTERS/CHARACTER_SHEET_FIELD.md",
    "COMPILATION_REPORT.md",
]

# Scene codes that must exist in compiled booklets
JOINT_CODES = {"J-100", "J-130", "J-150", "J-300", "J-410", "J-420", "J-430", "J-900"}
SYSTEMS_CODES = {"S-110", "S-111", "S-112", "S-113", "S-115", "S-123", "S-210", "S-230", "S-260", "S-240", "S-220"}
FIELD_CODES = {"F-120", "F-121", "F-140", "F-141", "F-250", "F-270", "F-271", "F-122", "F-312", "F-330"}
ENDING_CODES = {"E-901", "E-902", "E-903", "E-904", "E-905"}
CLUE_CODES = {f"C-{i:02d}" for i in range(1, 17)}

CHECK_RE = re.compile(r"DC\s+(10|15)")
CLUE_IN_SYSTEMS = {"C-01", "C-02", "C-03", "C-04", "C-14", "C-05", "C-16", "C-07"}
CLUE_IN_FIELD = {"C-11", "C-10", "C-13", "C-06", "C-08", "C-12", "C-09"}


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def codes_in(text: str, prefix: str) -> set[str]:
    return set(re.findall(rf"\b{prefix}-\d+\b", text))


def main() -> int:
    failures: list[str] = []

    for rel in REQUIRED:
        if not (PLAYER / rel).is_file():
            failures.append(f"missing file: {rel}")

    joint = read(PLAYER / "JOINT_SCENES.md")
    systems = read(PLAYER / "BOOKLET_SYSTEMS.md")
    field = read(PLAYER / "BOOKLET_FIELD.md")
    endings = read(PLAYER / "ENDINGS.md")
    case_file = read(PLAYER / "SHARED/CASE_FILE.md")

    for code in JOINT_CODES:
        if code not in joint:
            failures.append(f"missing joint scene: {code}")
    for code in SYSTEMS_CODES:
        if code not in systems:
            failures.append(f"missing systems scene: {code}")
    for code in FIELD_CODES:
        if code not in field:
            failures.append(f"missing field scene: {code}")
    for code in ENDING_CODES:
        if code not in endings:
            failures.append(f"missing ending: {code}")

    for code in CLUE_CODES:
        if code not in case_file:
            failures.append(f"missing clue slot: {code}")

    # checks present
    check_count = len(CHECK_RE.findall(systems + field))
    if check_count < 5:
        failures.append(f"expected 5 skill checks, found {check_count}")

    # spoiler leak guard: DO_NOT_READ path in player docs
    for rel in REQUIRED:
        text = read(PLAYER / rel)
        if "DO_NOT_READ" in text and rel != "COMPILATION_REPORT.md":
            if "do not open" not in text.lower() and "do not consult" not in text.lower():
                failures.append(f"DO_NOT_READ reference without warning in {rel}")

    # navigation cross-refs
    if "J-150" not in systems or "J-150" not in field:
        failures.append("regroup J-150 not referenced from both booklets")

    print("PLAYER package validation\n")
    if failures:
        for f in failures:
            print(f"FAIL  {f}")
        print(f"\nTotal failures: {len(failures)}")
        return 1

    print("PASS  all required files present")
    print(f"PASS  scene codes: joint={len(JOINT_CODES)} systems={len(SYSTEMS_CODES)} field={len(FIELD_CODES)} endings={len(ENDING_CODES)}")
    print(f"PASS  clue slots: {len(CLUE_CODES)}")
    print(f"PASS  skill checks referenced: {check_count}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
