#!/usr/bin/env python3
"""Structural validation for CASE_BENCHMARK_v0.4 PLAYER package (v0.4.1)."""
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
    if len(set(clues)) < 15:
        errors.append(f"Expected 15 clue slots, found {len(set(clues))}")

    dispatch = joint[joint.find("## J-600"):joint.find("## J-600") + 1200]
    if re.search(r"Tomás Reyes", dispatch, re.I):
        errors.append("Culprit name in J-600 dispatch")

    if "(Accident" in joint or "accident without" in joint.lower():
        errors.append("Answered infer parenthetical in joint scenes")

    for path in ["JOINT_SCENES.md", "BOOKLET_PEOPLE.md", "BOOKLET_RECORDS.md"]:
        text = (ROOT / path).read_text().lower()
        if "recommended" in text or "you should" in text:
            errors.append(f"Steering language in {path}")

    records = (ROOT / "BOOKLET_RECORDS.md").read_text()
    if "verbal claim" in records.lower():
        errors.append("Phantom verbal claim in Records booklet")

    if "gain it now" in joint.lower() or "faxed copy" in joint.lower():
        errors.append("Soft bailout language in joint scenes")

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
