"""Deterministic GAMEBOOK.md section parsing."""

from __future__ import annotations

import re
from pathlib import Path

from simulator_v2.human_delivery.types import ParsedSection, VisibleChoice

SECTION_HEADING = re.compile(r"^## Section (\d+)\s*$", re.M)
CHECK_SUCCESS = re.compile(
    r"if your roll \*\*succeeds\*\*, turn to section (?:\[\*\*(\d+)\*\*\]\(#section-\d+\)|\*\*(\d+)\*\*)",
    re.I,
)
CHECK_FAILURE = re.compile(
    r"if your roll \*\*fails\*\*, turn to section (?:\[\*\*(\d+)\*\*\]\(#section-\d+\)|\*\*(\d+)\*\*)",
    re.I,
)
TURN_TO = re.compile(
    r"turn to section (?:\[\*\*(\d+)\*\*\]\(#section-\d+\)|\*\*(\d+)\*\*)",
    re.I,
)
TURN_TO_PLAIN = re.compile(r"turn to section (\d+)", re.I)
CHOICE_LINE = re.compile(r"^- (.+)$", re.M)


def _section_from_match(match: re.Match[str]) -> int:
    for group in match.groups():
        if group:
            return int(group)
    raise ValueError("no section number in match")


def _parse_choices(block: str) -> list[VisibleChoice]:
    choices: list[VisibleChoice] = []
    for line in block.splitlines():
        line = line.strip()
        if not line.startswith("- "):
            continue
        text = line[2:].strip()
        succ = CHECK_SUCCESS.search(text)
        if succ:
            choices.append(VisibleChoice(text, _section_from_match(succ), "check_success"))
            continue
        fail = CHECK_FAILURE.search(text)
        if fail:
            choices.append(VisibleChoice(text, _section_from_match(fail), "check_failure"))
            continue
        dest = TURN_TO.search(text) or TURN_TO_PLAIN.search(text)
        if dest:
            choices.append(VisibleChoice(text, _section_from_match(dest), "navigate"))
        else:
            choices.append(VisibleChoice(text, None, "navigate"))
    return choices


def parse_gamebook(
    gamebook_path: Path,
    section_to_unit: dict[int, str],
) -> dict[int, ParsedSection]:
    text = gamebook_path.read_text(encoding="utf-8")
    sections: dict[int, ParsedSection] = {}
    matches = list(SECTION_HEADING.finditer(text))
    for i, match in enumerate(matches):
        sec_num = int(match.group(1))
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        block = text[start:end].strip()
        body = block
        choice_block = ""
        if "**What do you do?**" in block:
            body, _, choice_block = block.partition("**What do you do?**")
        unit_id = section_to_unit.get(sec_num, "")
        sections[sec_num] = ParsedSection(
            section_number=sec_num,
            unit_id=unit_id,
            body_excerpt=body.strip()[:240],
            choices=_parse_choices(choice_block),
        )
    return sections


def extract_start_section(manifest: dict) -> tuple[str, int, str]:
    static = manifest.get("static_book") or {}
    start_file = static.get("gamebook_path", "PLAYER/GAMEBOOK.md")
    start_section = static.get("start_section")
    start_unit = static.get("start_unit_id", "")
    if start_section is None:
        pub = manifest.get("public_sections") or {}
        start_section = pub.get(start_unit)
    return start_file, int(start_section or 0), start_unit
