"""Extract playable units from PLAYER markdown."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

UNIT_MARKER = re.compile(r"<!--\s*unit:([a-z0-9_-]+)\s*-->", re.I)
HEADING = re.compile(r"^###\s+(.+)$", re.M)
CHOICES_HEADER = re.compile(r"\*\*What do you do\?\*\*", re.I)
META_TIME = re.compile(r"\*\*Time cost:\*\*|\*\*Location:\*\*|\*\*Check:\*\*|\*\*Scene transition\*\*")


@dataclass
class PlayerUnit:
    unit_id: str
    file: str
    title: str
    body: str
    meta_lines: list[str] = field(default_factory=list)
    choices: list[str] = field(default_factory=list)


def _slug_to_unit_id(slug: str, known: set[str]) -> str:
    candidate = slug.upper().replace("_", "-")
    if candidate in known:
        return candidate
    # try with common prefixes
    for prefix in ("UNIT-", "SC-", "INF-", "REC-", "END-"):
        if f"{prefix}{candidate.replace(prefix, '')}" in known:
            return f"{prefix}{candidate.replace(prefix, '')}"
    return candidate


def resolve_manifest_aliases(
    units: dict[str, PlayerUnit],
    manifest_units: dict[str, dict],
) -> dict[str, PlayerUnit]:
    """Fill manifest units that share prose with another mapped unit (same file + anchor)."""
    if not manifest_units:
        return units
    out = dict(units)
    for uid, entry in manifest_units.items():
        if uid in out:
            continue
        anchor = entry.get("anchor", "")
        file_ref = entry.get("file", "")
        for source_uid, source in out.items():
            src_entry = manifest_units.get(source_uid, {})
            if src_entry.get("anchor") == anchor and src_entry.get("file") == file_ref:
                out[uid] = PlayerUnit(
                    unit_id=uid,
                    file=entry.get("file", source.file),
                    title=source.title,
                    body=source.body,
                    meta_lines=list(source.meta_lines),
                    choices=[],
                )
                break
    return out


def parse_player_units(player_root: Path, known_unit_ids: set[str] | None = None) -> dict[str, PlayerUnit]:
    known = known_unit_ids or set()
    units: dict[str, PlayerUnit] = {}
    for path in sorted(player_root.rglob("*.md")):
        if path.name in {"HOW_TO_PLAY.md", "README.md", "NAVIGATION_INDEX.md", "OPENING.md", "GAMEBOOK.md"}:
            continue
        if "CHARACTERS" in path.parts or "SHARED" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        rel = str(path.relative_to(player_root.parent)).replace("\\", "/")
        parts = UNIT_MARKER.split(text)
        # parts: [preamble, slug, block, slug, block, ...]
        i = 1
        while i < len(parts) - 1:
            slug = parts[i].strip()
            block = parts[i + 1]
            uid = _slug_to_unit_id(slug, known) if known else slug.upper()
            if known and uid not in known:
                i += 2
                continue
            title_match = HEADING.search(block)
            title = title_match.group(1).strip() if title_match else uid
            if CHOICES_HEADER.search(block):
                pre, _, post = block.partition("**What do you do?**")
                body = pre.strip()
                choice_lines = [
                    ln.strip()[2:].strip()
                    for ln in post.splitlines()
                    if ln.strip().startswith("- ")
                ]
            else:
                body = block.strip()
                choice_lines = []
            meta = [ln.strip() for ln in body.splitlines() if META_TIME.search(ln)]
            units[uid] = PlayerUnit(
                unit_id=uid,
                file=rel,
                title=title,
                body=body,
                meta_lines=meta,
                choices=choice_lines,
            )
            i += 2
    return units


def load_opening(player_root: Path) -> str:
    opening = player_root / "OPENING.md"
    if opening.exists():
        return opening.read_text(encoding="utf-8").strip()
    return ""
