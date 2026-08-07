"""Build public-section manifest and GAMEBOOK.md."""

from __future__ import annotations

import json
import re
import time
from pathlib import Path
from typing import Any

from idne.gamebook_nav.delivery import load_materialized_delivery
from idne.gamebook_nav.extract import load_opening, parse_player_units
from idne.gamebook_nav.graph import build_navigation_graph
from idne.gamebook_nav.numbering import assign_public_sections
from idne.gamebook_nav.constants import DEFAULT_START_UNIT
from idne.gamebook_nav.player_json import (
    PLAYER_GAMEBOOK_PATH,
    build_player_gamebook,
    write_player_gamebook,
)
from idne.gamebook_nav.sections import section_heading, section_link
from idne.gamebook_nav.validate import validate_gamebook_navigation


def _choice_lines(edges, section_map: dict[str, int]) -> list[str]:
    lines: list[str] = []
    for edge in edges:
        dest = edge.destination_unit_id
        sec = section_map.get(dest)
        if not sec:
            lines.append(f"- {edge.label}")
            continue
        link = section_link(sec)
        if edge.edge_kind == "check_success":
            lines.append(f"- If your roll **succeeds**, turn to section {link}.")
        elif edge.edge_kind == "check_failure":
            lines.append(f"- If your roll **fails**, turn to section {link}.")
        else:
            lines.append(f"- {edge.label} Turn to section {link}.")
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
        f"**Starting section: {start_sec}** — turn to section {section_link(start_sec)} to begin your investigation.",
        "",
        "---",
        "",
    ]

    for uid in sorted(player_units.keys(), key=lambda u: section_map.get(u, 999999)):
        unit = player_units[uid]
        sec = section_map[uid]
        nav = graph.get(uid)
        lines.append(section_heading(sec))
        lines.append("")
        if unit.meta_lines:
            for m in unit.meta_lines:
                lines.append(m)
            lines.append("")
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


def _resolve_adventure_title(adventure_id: str, adventure_root: Path) -> str:
    workspace = adventure_root.parent
    brief: dict[str, Any] = {}
    for candidate in (
        workspace / "pack_spec.json",
        workspace / "brief" / "adventure_brief.json",
        workspace / "adventure_brief.json",
    ):
        if not candidate.exists():
            continue
        raw = json.loads(candidate.read_text(encoding="utf-8"))
        brief = raw.get("brief", raw) if candidate.name == "pack_spec.json" else raw
        break
    if brief.get("working_title"):
        return str(brief["working_title"])
    notes = str(brief.get("author_notes") or "")
    match = re.search(r"(?:Codename|Kódnév):\s*([^.\n]+)", notes, re.I)
    if match:
        return match.group(1).strip()
    if workspace.name != adventure_id:
        return workspace.name.replace("_", " ")
    return adventure_id.replace("_", " ")


def build_gamebook_package(
    adventure_root: Path,
    *,
    adventure_id: str | None = None,
    mapping_path: Path | None = None,
    start_unit_id: str = DEFAULT_START_UNIT,
    numbering_seed: str | None = None,
) -> dict[str, Any]:
    """Generate/extend player mapping manifest and GAMEBOOK.md."""
    t0 = time.perf_counter()
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
    if manifest.get("static_book", {}).get("start_unit_id"):
        start_unit_id = manifest["static_book"]["start_unit_id"]
    template_units = parse_player_units(player_root, None)
    if not template_units:
        raise ValueError("no playable template units found")

    persisted_seed = numbering_seed
    if persisted_seed is None and manifest.get("static_book"):
        persisted_seed = manifest["static_book"].get("numbering_seed")
    existing_sections = manifest.get("public_sections") or {}

    delivery_stats = None
    package, delivery_units, graph, delivery_stats = load_materialized_delivery(
        adventure_root,
        template_units,
        manifest_units=manifest.get("units") or {},
    )
    if delivery_units and graph:
        player_units = delivery_units
        delivery_mode = "materialized_static_book"
    else:
        from idne.gamebook_nav.extract import resolve_manifest_aliases

        manifest_units = manifest.get("units") or {}
        known = set(manifest_units.keys())
        player_units = parse_player_units(player_root, known or None)
        player_units = resolve_manifest_aliases(player_units, manifest_units)
        graph = build_navigation_graph(adventure_root, player_units, manifest_units=manifest_units)
        delivery_mode = "static_book"

    section_map = assign_public_sections(
        player_units.keys(),
        adventure_id,
        seed_override=persisted_seed,
        existing_map=existing_sections if persisted_seed else None,
    )
    if delivery_stats:
        delivery_stats.public_sections = len(section_map)

    units: dict[str, dict] = {}
    template_prose_index = {
        uid: {"file": u.file, "anchor": u.title, "template_unit_id": uid}
        for uid, u in template_units.items()
    }
    for uid, unit in player_units.items():
        tpl = uid.split("--S-", 1)[0]
        prose_ref = template_prose_index.get(tpl, {})
        entry: dict[str, Any] = {
            "unit_id": uid,
            "file": prose_ref.get("file", unit.file),
            "anchor": prose_ref.get("anchor", unit.title),
            "public_section": section_map[uid],
        }
        if tpl != uid:
            entry["template_unit_id"] = tpl
            entry["prose_template_unit_id"] = tpl
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
        "delivery_mode": delivery_mode,
    }
    if delivery_stats:
        manifest["delivery_projection"] = delivery_stats.to_dict()
        if package:
            mat = {}
            pkg_path = adventure_root / "DO_NOT_READ" / "epistemic_progression_package.json"
            if pkg_path.exists():
                raw = json.loads(pkg_path.read_text(encoding="utf-8"))
                mat = raw.get("materialization") or {}
            manifest["delivery_projection"]["epistemic_materialization"] = mat

    opening = load_opening(player_root)
    title = _resolve_adventure_title(adventure_id, adventure_root)
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

    player_payload = build_player_gamebook(
        adventure_id=adventure_id,
        adventure_title=title,
        opening=opening,
        start_section=section_map[start_unit_id],
        delivery_mode=delivery_mode,
        player_units=player_units,
        graph=graph,
        section_map=section_map,
    )
    player_json_path = player_root / "gamebook.json"
    player_json_bytes = write_player_gamebook(player_json_path, player_payload)
    from idne.player_delivery_validate import validate_player_gamebook_payload

    player_validation = validate_player_gamebook_payload(
        player_payload,
        manifest=manifest,
        gamebook_text=gamebook,
    )

    t_val = time.perf_counter()
    val = validate_gamebook_navigation(
        adventure_root,
        manifest=manifest,
        player_units=player_units,
        graph=graph,
        section_map=section_map,
        start_unit_id=start_unit_id,
        gamebook_text=gamebook,
    )
    validate_ms = int((time.perf_counter() - t_val) * 1000)

    manifest["gamebook_validation"] = val.to_dict()
    manifest["static_book"]["player_gamebook_path"] = PLAYER_GAMEBOOK_PATH
    manifest["player_delivery_validation"] = player_validation.to_dict()
    mapping_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    build_ms = int((time.perf_counter() - t0) * 1000)
    gamebook_bytes = gamebook_path.stat().st_size

    return {
        "manifest_path": str(mapping_path),
        "gamebook_path": str(gamebook_path),
        "player_gamebook_path": str(player_json_path),
        "section_count": len(section_map),
        "start_section": section_map[start_unit_id],
        "start_unit_id": start_unit_id,
        "validation": val.to_dict(),
        "player_delivery_validation": player_validation.to_dict(),
        "delivery_mode": delivery_mode,
        "delivery_projection": delivery_stats.to_dict() if delivery_stats else None,
        "gamebook_bytes": gamebook_bytes,
        "player_gamebook_bytes": player_json_bytes,
        "build_ms": build_ms,
        "validate_ms": validate_ms,
    }
