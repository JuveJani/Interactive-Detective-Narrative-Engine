#!/usr/bin/env python3
"""Structural validation for CASE_BENCHMARK_v0.4 PLAYER package."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent
REQUIRED = [
    "README.md", "SETUP.md", "HOW_TO_PLAY.md", "NAVIGATION_INDEX.md",
    "JOINT_SCENES.md", "BOOKLET_PEOPLE.md", "BOOKLET_RECORDS.md", "ENDINGS.md",
    "SHARED/CASE_FILE.md",
    "CHARACTERS/CHARACTER_SHEET_PEOPLE.md",
    "CHARACTERS/CHARACTER_SHEET_RECORDS.md",
    "COMPILATION_REPORT.md",
]

JOINT_CODES = ["J-100", "J-110", "J-120", "J-130", "J-200", "J-210", "J-300", "J-330", "J-400", "J-410", "J-500", "J-510", "J-600"]
ENDING_CODES = ["E-901", "E-902", "E-903", "E-904", "E-905"]
CLUE_RE = re.compile(r"C-\d{2}")

def main():
    errors = []
    for rel in REQUIRED:
        if not (ROOT / rel).exists():
            errors.append(f"Missing required file: {rel}")

    joint = (ROOT / "JOINT_SCENES.md").read_text()
    for code in JOINT_CODES:
        if code not in joint:
            errors.append(f"Missing joint scene: {code}")

    endings = (ROOT / "ENDINGS.md").read_text()
    for code in ENDING_CODES:
        if code not in endings:
            errors.append(f"Missing ending: {code}")

    case = (ROOT / "SHARED/CASE_FILE.md").read_text()
    clues = CLUE_RE.findall(case)
    if len(set(clues)) < 14:
        errors.append(f"Expected 14 clue slots, found {len(set(clues))}")

    for path in ["JOINT_SCENES.md", "BOOKLET_PEOPLE.md", "BOOKLET_RECORDS.md"]:
        text = (ROOT / path).read_text().lower()
        if "recommended" in text or "you should" in text:
            errors.append(f"Steering language in {path}")

    if errors:
        print("FAIL")
        for e in errors:
            print(" -", e)
        sys.exit(1)
    print("PASS")
    print(f"Files: {len(REQUIRED)}")
    print(f"Joint scenes: {len(JOINT_CODES)}")
    print(f"Endings: {len(ENDING_CODES)}")
    print(f"Clues: {len(set(clues))}")

if __name__ == "__main__":
    main()
