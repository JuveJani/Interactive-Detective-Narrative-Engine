"""Public section anchors and same-document navigation links."""

from __future__ import annotations

import re

ANCHOR_TAG = re.compile(r'<a\s+id="section-(\d+)"\s*></a>', re.I)
SECTION_HEADING = re.compile(r"^## Section (\d+)\s*$", re.M)
SECTION_LINK = re.compile(r"\[\*\*(\d+)\*\*\]\(#section-(\d+)\)", re.I)
LEGACY_BOLD_TURN = re.compile(r"turn to section \*\*(\d+)\*\*(?!\]\(#section-\1\))", re.I)
LEGACY_TURN = re.compile(r"turn to section \*\*(\d+)\*\*", re.I)


def section_anchor(section_number: int) -> str:
    return f'<a id="section-{section_number}"></a>'


def section_link(section_number: int) -> str:
    sec = int(section_number)
    return f"[**{sec}**](#section-{sec})"


def section_heading(section_number: int) -> str:
    return f"{section_anchor(section_number)}\n## Section {section_number}"
