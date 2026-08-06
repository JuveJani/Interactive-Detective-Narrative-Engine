"""Build public-section manifest and GAMEBOOK.md."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from idne.gamebook_nav.extract import load_opening, parse_player_units, resolve_manifest_aliases
from idne.gamebook_nav.graph import build_navigation_graph
from idne.gamebook_nav.numbering import assign_public_sections
from idne.gamebook_nav.constants import DEFAULT_START_UNIT
from idne.gamebook_nav.validate import validate_gamebook_navigation


def _choice_lines(edges, section_map: dict[str, int]) -> list[str]:
    lines: list[str] = []
    for edge in edges:
        dest = edge.destination_unit_id
        sec = section_map.get(dest)
        if not sec:
            lines.append(f"- {edge.label}")
            continue
        if edge.edge_kind == "check_success":
            lines.append(f"- If your roll **succeeds**, turn to section **{sec}**.")
        elif edge.edge_kind == "check_failure":
            lines.append(f"- If your roll **fails**, turn to section **{sec}**.")
        else:
            lines.append(f"- {edge.label} Turn to section **{sec}**.")
    return lines


def render_gamebook(
    player_units,
    graph,
    section_map: dict[str, int],
    *,
    opening: str,
    start_unit_id: str,
    adventure_title: str,
) -> str:
    start_sec = section_map[start_unit_id]
    lines = [
        f"# {adventure_title} — Static Gamebook",
        "",
        "Read the opening below, then **begin at the starting section**. "
        "Follow only the section numbers given in each choice. "
        "Do not look up internal codes or browse ahead.",
        "",
        "## Opening",
        "",
        opening,
        "",
        f"**Starting section: {start_sec}** — turn to section **{start_sec}** to begin your investigation.",
        "",
        "---",
        "",
    ]

    for uid in sorted(player_units.keys(), key=lambda u: section_map.get(u, 9999)):
        unit = player_units[uid]
        sec = section_map[uid]
        nav = graph.get(uid)
        lines.append(f"## Section {sec}")
        lines.append("")
        if unit.meta_lines:
            for m in unit.meta_lines:
                lines.append(m)
            lines.append("")
        # body without duplicate heading
        body = unit.body
        for m in unit.meta_lines:
            body = body.replace(m, "").strip()
        if body:
            lines.append(body.strip())
            lines.append("")
        if nav and nav.choices:
            lines.append("**What do you do?**")
            lines.append("")
            lines.extend(_choice_lines(nav.choices, section_map))
            lines.append("")
        lines.append("---")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def build_gamebook_package(
    adventure_root: Path,
    *,
    adventure_id: str | None = None,
    mapping_path: Path | None = None,
    start_unit_id: str = DEFAULT_START_UNIT,
    numbering_seed: str | None = None,
) -> dict[str, Any]:
    """Generate/extend player mapping manifest and GAMEBOOK.md."""
    adventure_root = Path(adventure_root).resolve()
    workspace = adventure_root.parent
    player_root = adventure_root / "PLAYER"

    if mapping_path is None:
        candidate = workspace / "player_mapping_manifest.json"
        mapping_path = candidate if candidate.exists() else adventure_root / "player_mapping_manifest.json"

    manifest: dict[str, Any] = {}
    if mapping_path.exists():
        manifest = json.loads(mapping_path.read_text(encoding="utf-8"))

    adventure_id = adventure_id or manifest.get("adventure_id") or adventure_root.name
    manifest_units = manifest.get("units") or {}
    known = set(manifest_units.keys())
    player_units = parse_player_units(player_root, known or None)
    player_units = resolve_manifest_aliases(player_units, manifest_units)
    if not player_units:
        raise ValueError("no playable units found")

    persisted_seed = numbering_seed
    if persisted_seed is None and manifest.get("static_book"):
        persisted_seed = manifest["static_book"].get("numbering_seed")
    existing_sections = manifest.get("public_sections") or {}

    graph = build_navigation_graph(adventure_root, player_units, manifest_units=manifest_units)
    section_map = assign_public_sections(
        player_units.keys(),
        adventure_id,
        seed_override=persisted_seed,
        existing_map=existing_sections if persisted_seed else None,
    )

    # enrich manifest units
    units = dict(manifest.get("units") or {})
    for uid, unit in player_units.items():
        entry = dict(units.get(uid) or {"unit_id": uid, "file": unit.file, "anchor": unit.title})
        entry["public_section"] = section_map[uid]
        nav = graph.get(uid)
        if nav:
            entry["choices"] = [
                {
                    "label": e.label,
                    "destination_unit_id": e.destination_unit_id,
                    "kind": e.edge_kind,
                }
                for e in nav.choices
            ]
        units[uid] = entry

    manifest["schema_version"] = "1.1"
    manifest["adventure_id"] = adventure_id
    manifest["unit_count"] = len(units)
    manifest["units"] = units
    manifest["public_sections"] = section_map
    manifest["static_book"] = {
        "gamebook_path": "PLAYER/GAMEBOOK.md",
        "start_unit_id": start_unit_id,
        "start_section": section_map[start_unit_id],
        "numbering_seed": persisted_seed or adventure_id,
        "delivery_mode": "static_book",
    }

    opening = load_opening(player_root)
    title = adventure_id.replace("_", " ")
    gamebook = render_gamebook(
        player_units,
        graph,
        section_map,
        opening=opening,
        start_unit_id=start_unit_id,
        adventure_title=title,
    )

    gamebook_path = player_root / "GAMEBOOK.md"
    gamebook_path.write_text(gamebook, encoding="utf-8")

    val = validate_gamebook_navigation(
        adventure_root,
        manifest=manifest,
        player_units=player_units,
        graph=graph,
        section_map=section_map,
        start_unit_id=start_unit_id,
        gamebook_text=gamebook,
    )

    manifest["gamebook_validation"] = val.to_dict()
    mapping_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    return {
        "manifest_path": str(mapping_path),
        "gamebook_path": str(gamebook_path),
        "section_count": len(section_map),
        "start_section": section_map[start_unit_id],
        "start_unit_id": start_unit_id,
        "validation": val.to_dict(),
    }
