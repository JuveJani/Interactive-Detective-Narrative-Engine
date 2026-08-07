"""Generate PLAYER markdown from adventure pack spec."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from idne.adventure_pack.spec import AdventurePackSpec


FILE_MAP = {
    "LOCATIONS": "LOCATIONS.md",
    "NPCS": "NPCS.md",
    "OBJECTS": "OBJECTS.md",
    "SCENES": "SCENES.md",
    "INFERENCE": "INFERENCE.md",
    "RECOVERY": "RECOVERY.md",
    "ENDINGS": "ENDINGS.md",
}


def human_title(uid: str) -> str:
    s = uid
    for prefix in ("UNIT-CHK-", "UNIT-", "SC-", "INF-", "END-", "REC-"):
        if s.startswith(prefix):
            s = s[len(prefix) :]
            break
    return re.sub(r"\s+", " ", s.replace("-", " ")).strip().capitalize()


def _meta_lines(meta: dict[str, Any]) -> str:
    parts = []
    if meta.get("location_id"):
        loc = meta["location_id"].replace("LOC-", "").replace("-", " ").title()
        parts.append(f"**Location:** {loc}")
    if meta.get("time_cost_minutes") is not None:
        parts.append(f"**Time cost:** {meta['time_cost_minutes']} min")
    if meta.get("check"):
        parts.append(f"**Check:** {meta['check']}")
    return " | ".join(parts)


def _render_body(unit: dict[str, Any]) -> str:
    prose = unit.get("prose") or {}
    if isinstance(prose, str):
        return prose.strip()
    if unit.get("unit_kind") == "dialogue_topic" and prose.get("dialogue"):
        d = prose["dialogue"]
        lines = []
        if d.get("scene"):
            lines.append(d["scene"].strip())
            lines.append("")
        if d.get("speaker") and d.get("quote"):
            lines.append(f'{d["speaker"]} {d.get("prompt", "says")}:')
            lines.append(f'"{d["quote"].strip()}"')
        elif prose.get("body"):
            lines.append(prose["body"].strip())
        if d.get("coda"):
            lines.append("")
            lines.append(d["coda"].strip())
        return "\n".join(lines).strip()
    if prose.get("setup") or prose.get("fact"):
        lines = []
        if prose.get("setup"):
            lines.append(prose["setup"].strip())
            lines.append("")
        if prose.get("fact"):
            lines.append(prose["fact"].strip())
            lines.append("")
        if prose.get("coda"):
            lines.append(prose["coda"].strip())
        return "\n".join(lines).strip()
    return str(prose.get("body") or "").strip()


def unit_block(unit: dict[str, Any]) -> str:
    uid = unit["unit_id"]
    title = unit.get("title") or human_title(uid)
    slug = uid.lower()
    meta = unit.get("meta") or {}
    meta_str = _meta_lines(meta)
    body = _render_body(unit)
    choices = unit.get("choices") or []
    lines = [f"<!-- unit:{slug} -->", f"### {title}", ""]
    if meta_str:
        lines.extend([meta_str, ""])
    if body:
        lines.extend([body, ""])
    if choices:
        lines.extend(["**What do you do?**", ""])
        for c in choices:
            lines.append(f"- {c['label']}")
        lines.append("")
    return "\n".join(lines)


def write_player_files(spec: AdventurePackSpec, adventure_root: Path) -> dict[str, Any]:
    player = adventure_root / "PLAYER"
    player.mkdir(parents=True, exist_ok=True)
    shell = spec.player_units.get("shell") or {}

    if shell.get("opening"):
        (player / "OPENING.md").write_text(str(shell["opening"].get("prose") or shell["opening"]) + "\n", encoding="utf-8")
    if shell.get("how_to_play"):
        ht = shell["how_to_play"]
        if isinstance(ht, dict):
            text = "\n\n".join(f"## {s['heading']}\n\n{s['body']}" for s in ht.get("sections") or [])
        else:
            text = str(ht)
        (player / "HOW_TO_PLAY.md").write_text(text + "\n", encoding="utf-8")
    if shell.get("readme"):
        rd = shell["readme"]
        if isinstance(rd, dict):
            text = f"# {spec.pack_id.replace('_', ' ')} — Player Package\n\n**Mode:** Single investigator\n**Estimated playtime:** About two hours\n\n{rd.get('body', '')}"
        else:
            text = str(rd)
        (player / "README.md").write_text(text + "\n", encoding="utf-8")
    if shell.get("navigation_index"):
        ni = shell["navigation_index"]
        lines = ["# Navigation index", "", "Do not read ahead in these files.", ""]
        for e in ni.get("entries") or []:
            lines.append(f"- {e['label']}: `{e.get('file_ref', e.get('file', ''))}`")
        (player / "NAVIGATION_INDEX.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    (player / "CHARACTERS").mkdir(parents=True, exist_ok=True)
    cs = shell.get("character_sheet") or {}
    if isinstance(cs, dict):
        mods = cs.get("modifiers") or []
        mod_table = "\n".join(f"| **{m['capability'].title()}** | **{m['modifier']:+d}** | {m.get('when_applies', '')} |" for m in mods)
        cs_text = f"# Character sheet — {cs.get('role', 'investigator')}\n\n{cs.get('intro', '')}\n\n## Check modifiers\n\n| Capability | Modifier | When it applies |\n|---|---|---|\n{mod_table}\n\n{cs.get('equipment', '')}\n\n{cs.get('stakes', '')}\n"
        (player / "CHARACTERS" / "CHARACTER_SHEET.md").write_text(cs_text, encoding="utf-8")
    elif isinstance(cs, str):
        (player / "CHARACTERS" / "CHARACTER_SHEET.md").write_text(cs + "\n", encoding="utf-8")

    (player / "SHARED").mkdir(parents=True, exist_ok=True)
    cf = shell.get("case_file_template") or shell.get("case_file")
    if cf:
        (player / "SHARED" / "CASE_FILE.md").write_text(str(cf) + "\n" if not str(cf).startswith("#") else str(cf) + "\n", encoding="utf-8")

    buckets: dict[str, list[str]] = {}
    mapping: dict[str, dict[str, str]] = {}
    for unit in spec.units:
        fname = FILE_MAP.get(str(unit.get("player_file", "LOCATIONS")).upper(), "LOCATIONS.md")
        block = unit_block(unit)
        buckets.setdefault(fname, []).append(block)
        title = unit.get("title") or human_title(unit["unit_id"])
        mapping[unit["unit_id"]] = {"file": f"PLAYER/{fname}", "anchor": title, "unit_id": unit["unit_id"]}

    for fname, blocks in buckets.items():
        (player / fname).write_text("\n".join(blocks), encoding="utf-8")

    workspace = adventure_root.parent
    manifest = {
        "schema_version": "1.0",
        "adventure_id": spec.pack_id,
        "unit_count": len(mapping),
        "units": mapping,
    }
    (workspace / "player_mapping_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest
