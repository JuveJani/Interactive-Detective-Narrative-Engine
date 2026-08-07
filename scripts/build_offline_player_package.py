#!/usr/bin/env python3
"""Build an offline IDNE player distribution package with bundled adventures."""

from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLAYER_SRC = REPO_ROOT / "idne_player"
DEFAULT_OUT = REPO_ROOT / "dist" / "idne-player"


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _safe_title(adventure_id: str, brief: dict) -> str:
    if brief.get("working_title"):
        return str(brief["working_title"])
    notes = str(brief.get("author_notes") or "")
    match = re.search(r"Codename:\s*([^.\n]+)", notes, re.I)
    if match:
        return match.group(1).strip()
    return adventure_id.replace("_", " ")


def _library_entry(workspace: Path) -> dict | None:
    adventure_root = workspace / "adventure"
    gamebook_path = adventure_root / "PLAYER" / "gamebook.json"
    if not gamebook_path.exists():
        return None

    brief: dict = {}
    pack_spec = workspace / "pack_spec.json"
    if pack_spec.exists():
        brief = (_read_json(pack_spec).get("brief") or {})
    else:
        for candidate in (workspace / "brief" / "adventure_brief.json", workspace / "adventure_brief.json"):
            if candidate.exists():
                brief = _read_json(candidate)
                break

    gamebook = _read_json(gamebook_path)
    bundle_id = workspace.name
    playtime = brief.get("target_playtime_minutes")
    return {
        "id": bundle_id,
        "adventure_id": gamebook.get("adventure_id") or bundle_id,
        "title": gamebook.get("title") or _safe_title(bundle_id, brief),
        "premise": brief.get("premise") or brief.get("location_scale") or brief.get("genre") or "",
        "player_role": brief.get("investigator_character") or "Investigator",
        "playtime": f"About {playtime} minutes" if playtime else "About two hours",
        "start_section": gamebook.get("start_section"),
        "section_count": gamebook.get("section_count"),
    }


def _write_js_object(path: Path, var_name: str, key: str, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = (
        f"window.{var_name} = window.{var_name} || {{}};\n"
        f"window.{var_name}[{json.dumps(key)}] = {json.dumps(payload, ensure_ascii=False)};\n"
    )
    path.write_text(text, encoding="utf-8")


def build_package(
  *,
  output_dir: Path,
  adventure_workspaces: list[Path],
) -> dict:
    if output_dir.exists():
        shutil.rmtree(output_dir)
    shutil.copytree(PLAYER_SRC, output_dir)

    library: list[dict] = []
    for workspace in adventure_workspaces:
        workspace = workspace.resolve()
        entry = _library_entry(workspace)
        if not entry:
            print(f"skip (no gamebook.json): {workspace}")
            continue
        gamebook = _read_json(workspace / "adventure" / "PLAYER" / "gamebook.json")
        _write_js_object(
            output_dir / "library" / "adventures" / f"{entry['id']}.js",
            "IDNE_GAMEBOOKS",
            entry["id"],
            gamebook,
        )
        library.append(entry)
        print(f"bundled: {entry['title']} ({entry['section_count']} sections)")

    library = sorted(library, key=lambda item: item["title"].lower())
    index_js = (
        "window.IDNE_LIBRARY = "
        + json.dumps(library, indent=2, ensure_ascii=False)
        + ";\n"
    )
    (output_dir / "library" / "index.js").write_text(index_js, encoding="utf-8")

    readme = f"""# IDNE Offline Player

Copy this folder to a laptop and open `index.html` in a modern browser.

## Quick start

1. Open `index.html`.
2. Choose an adventure from the library.
3. Press **Start** for a new game or **Continue** to resume autosaved progress.

## Bundled adventures

{chr(10).join(f"- {item['title']} ({item['section_count']} sections)" for item in library) or "- None"}

## Load your own adventure

Use **Load adventure file…** and select an adventure's `PLAYER/gamebook.json`.

## Offline notes

Bundled adventures are loaded as local JavaScript files so the player works from `file://` without a web server.

## Save slots

Each adventure supports autosave plus three manual save slots in browser local storage.
"""
    (output_dir / "README.md").write_text(readme, encoding="utf-8")
    return {"output_dir": str(output_dir), "adventure_count": len(library), "library": library}


def main() -> None:
    parser = argparse.ArgumentParser(description="Build offline IDNE player package")
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUT,
        help="Output directory for the player package",
    )
    parser.add_argument(
        "adventures",
        nargs="*",
        type=Path,
        help="Adventure workspace roots (default: auto-discover under adventures/)",
    )
    args = parser.parse_args()

    workspaces = [Path(p) for p in args.adventures]
    if not workspaces:
        adventures_root = REPO_ROOT / "adventures"
        workspaces = sorted(
            p for p in adventures_root.iterdir()
            if p.is_dir() and (p / "adventure" / "PLAYER" / "gamebook.json").exists()
        )

    summary = build_package(output_dir=args.output.resolve(), adventure_workspaces=workspaces)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
