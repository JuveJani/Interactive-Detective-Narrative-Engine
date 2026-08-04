"""Mandatory Single Investigator validation (Milestone 1)."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from idne.play_modes import PLAY_MODE_SINGLE, PLAY_MODE_TWO_PLAYER, normalize_play_modes

SPLIT_MARKERS = re.compile(
    r"\b(split|regroup|rejoin|private booklet|do not read|people investigator|records investigator)\b",
    re.I,
)
ROLE_BOOKLET_NAMES = ("BOOKLET_PEOPLE.md", "BOOKLET_RECORDS.md")
ROLE_SHEET_NAMES = ("CHARACTER_SHEET_PEOPLE.md", "CHARACTER_SHEET_RECORDS.md")
SPLIT_SCENE_PREFIXES = ("P-", "R-")  # Harborview-style role-private codes
SCENE_CODE_RE = re.compile(r"\b([JPR]-\d{3}[a-z]?)\b")
PARTNER_MARKERS = re.compile(
    r"\b(your partner|partner's|people investigator|records investigator|wait for (?:your )?partner)\b",
    re.I,
)


@dataclass
class ValidationResult:
    adventure_root: Path
    status: str  # PASS | FAIL | SKIP
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    checks: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "adventure_root": str(self.adventure_root),
            "status": self.status,
            "errors": self.errors,
            "warnings": self.warnings,
            "checks": self.checks,
        }


def load_play_manifest(root: Path) -> dict[str, Any] | None:
    for name in ("play_manifest.json", "PLAY_MANIFEST.json"):
        path = root / name
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    return None


def validate_single_investigator(adventure_root: str | Path) -> ValidationResult:
    """Run mandatory Single Investigator checks when mode is declared."""
    root = Path(adventure_root).resolve()
    result = ValidationResult(adventure_root=root, status="PASS")

    manifest = load_play_manifest(root)
    if not manifest:
        result.status = "SKIP"
        result.warnings.append("no play_manifest.json — single investigator not declared")
        return result

    try:
        modes = normalize_play_modes(manifest.get("play_modes"))
    except ValueError as e:
        result.status = "FAIL"
        result.errors.append(str(e))
        return result

    if PLAY_MODE_SINGLE not in modes:
        result.status = "SKIP"
        result.warnings.append(
            f"play_modes={modes} — single_investigator not declared; solo validation not applicable"
        )
        return result

    solo = manifest.get("single_investigator", {})
    if not isinstance(solo, dict):
        result.status = "FAIL"
        result.errors.append("single_investigator block missing or invalid in play_manifest.json")
        return result

    player = root / "PLAYER"
    if not player.is_dir():
        result.status = "FAIL"
        result.errors.append("Missing PLAYER directory")
        return result

    # --- Required artifact paths ---
    required_paths = {
        "character_sheet": solo.get("character_sheet"),
        "record_sheet": solo.get("record_sheet"),
        "scene_package": solo.get("scene_package"),
        "navigation_index": solo.get("navigation_index"),
        "endings": solo.get("endings"),
    }
    for key, rel in required_paths.items():
        check_id = f"QA-SI-ART-{key}"
        if not rel:
            result.errors.append(f"single_investigator.{key} not declared in manifest")
            result.checks[check_id] = "FAIL"
            continue
        path = root / rel if not str(rel).startswith("PLAYER") else root / rel
        if not path.exists():
            result.errors.append(f"Required solo artifact missing: {rel}")
            result.checks[check_id] = "FAIL"
        else:
            result.checks[check_id] = "PASS"

    # --- No split-only private booklets ---
    for name in ROLE_BOOKLET_NAMES:
        check_id = f"QA-SI-NO-{name}"
        path = player / name
        if path.exists():
            result.errors.append(
                f"Two-player private booklet present ({name}) — not allowed in single_investigator mode"
            )
            result.checks[check_id] = "FAIL"
        else:
            result.checks[check_id] = "PASS"

    for name in ROLE_SHEET_NAMES:
        path = player / "CHARACTERS" / name
        if path.exists():
            result.errors.append(
                f"Role-specific character sheet present ({name}) — use one investigator sheet"
            )
            result.checks[f"QA-SI-NO-{name}"] = "FAIL"

    # --- Scene graph: no split/regroup-only dependency in solo scene package ---
    scene_rel = solo.get("scene_package")
    if scene_rel:
        scene_path = root / scene_rel
        if scene_path.exists():
            scene_text = scene_path.read_text(encoding="utf-8")
            if SPLIT_MARKERS.search(scene_text):
                result.errors.append(
                    f"Split/regroup/private-booklet language in solo scene package: {scene_rel}"
                )
                result.checks["QA-SI-NO-SPLIT-MECHANICS"] = "FAIL"
            else:
                result.checks["QA-SI-NO-SPLIT-MECHANICS"] = "PASS"

            # Role-private scene codes in solo package
            role_only_codes = [
                line
                for line in scene_text.splitlines()
                if re.search(r"##\s+[PR]-\d{3}", line)
            ]
            if role_only_codes:
                result.errors.append(
                    f"Role-private scene codes in solo package ({len(role_only_codes)} headings)"
                )
                result.checks["QA-SI-NO-ROLE-PRIVATE-CODES"] = "FAIL"
            else:
                result.checks["QA-SI-NO-ROLE-PRIVATE-CODES"] = "PASS"

    # --- Navigation index must not require second player ---
    nav_rel = solo.get("navigation_index")
    if nav_rel and (root / nav_rel).exists():
        nav_text = (root / nav_rel).read_text(encoding="utf-8")
        if "BOOKLET_PEOPLE" in nav_text or "BOOKLET_RECORDS" in nav_text:
            result.errors.append("Navigation index references two-player private booklets")
            result.checks["QA-SI-NAV-ONE-PLAYER"] = "FAIL"
        else:
            result.checks["QA-SI-NAV-ONE-PLAYER"] = "PASS"

    # --- Inventory ownership ---
    inv_owner = solo.get("inventory_owner", "investigator")
    if inv_owner != "investigator":
        result.errors.append(f"inventory_owner must be 'investigator' for solo mode, got {inv_owner}")
        result.checks["QA-SI-INVENTORY"] = "FAIL"
    else:
        result.checks["QA-SI-INVENTORY"] = "PASS"

    # --- Clock model ---
    clock_model = solo.get("clock_model", "single_sequential")
    if clock_model not in ("single_sequential", "single_world_clock"):
        result.errors.append(f"invalid clock_model for solo: {clock_model}")
        result.checks["QA-SI-CLOCK"] = "FAIL"
    else:
        result.checks["QA-SI-CLOCK"] = "PASS"

    # --- Wall-clock estimate declared ---
    if solo.get("wall_clock_target_minutes") is None:
        result.errors.append("single_investigator.wall_clock_target_minutes not declared")
        result.checks["QA-SI-PLAYTIME"] = "FAIL"
    else:
        result.checks["QA-SI-PLAYTIME"] = "PASS"

    # --- Dual-mode adventures must also declare two_player routing ---
    if PLAY_MODE_TWO_PLAYER in modes:
        two = manifest.get("two_player", {})
        if not two.get("people_booklet") or not two.get("records_booklet"):
            result.errors.append(
                "play_modes includes two_player but two_player routing incomplete in manifest"
            )
            result.checks["QA-SI-DUAL-MODE"] = "FAIL"
        else:
            result.checks["QA-SI-DUAL-MODE"] = "PASS"

    # --- False PASS guard: if only two_player files exist without solo package ---
    if scene_rel and not (root / scene_rel).exists() and any(
        (player / n).exists() for n in ROLE_BOOKLET_NAMES
    ):
        result.errors.append(
            "Declared single_investigator but only two-player booklets found — false PASS guard"
        )
        result.checks["QA-SI-NO-FALSE-PASS"] = "FAIL"
    else:
        result.checks["QA-SI-NO-FALSE-PASS"] = "PASS"

    # --- Endings: no two-player-only dependencies ---
    endings_rel = solo.get("endings")
    if endings_rel and (root / endings_rel).exists():
        endings_text = (root / endings_rel).read_text(encoding="utf-8")
        if SPLIT_MARKERS.search(endings_text) or "BOOKLET_PEOPLE" in endings_text:
            result.errors.append("Endings reference split/regroup or two-player booklets")
            result.checks["QA-SI-ENDING"] = "FAIL"
        else:
            result.checks["QA-SI-ENDING"] = "PASS"

    # --- Knowledge: record sheet must not require partner ---
    record_rel = solo.get("record_sheet")
    if record_rel and (root / record_rel).exists():
        record_text = (root / record_rel).read_text(encoding="utf-8")
        if PARTNER_MARKERS.search(record_text):
            result.errors.append("Record sheet references partner / second-player knowledge")
            result.checks["QA-SI-KNOWLEDGE"] = "FAIL"
        else:
            result.checks["QA-SI-KNOWLEDGE"] = "PASS"

    # --- Wall-clock target sanity ---
    wct = solo.get("wall_clock_target_minutes")
    if wct is not None:
        try:
            minutes = int(wct)
            if minutes <= 0:
                result.errors.append("wall_clock_target_minutes must be positive")
                result.checks["QA-SI-PLAYTIME-VALUE"] = "FAIL"
            else:
                result.checks["QA-SI-PLAYTIME-VALUE"] = "PASS"
        except (TypeError, ValueError):
            result.errors.append("wall_clock_target_minutes must be an integer")
            result.checks["QA-SI-PLAYTIME-VALUE"] = "FAIL"

    # --- Scene reachability from declared or inferred start ---
    if scene_rel and (root / scene_rel).exists():
        scene_text = (root / scene_rel).read_text(encoding="utf-8")
        codes = {
            m.group(1)
            for line in scene_text.splitlines()
            if line.strip().startswith("##")
            for m in SCENE_CODE_RE.finditer(line)
        }
        refs = set(SCENE_CODE_RE.findall(scene_text))
        start = solo.get("start_scene")
        if not start and codes:
            # First ## heading scene code
            for line in scene_text.splitlines():
                if line.strip().startswith("##"):
                    m = SCENE_CODE_RE.search(line)
                    if m:
                        start = m.group(1)
                        break
        unreachable = codes - refs
        if start:
            unreachable.discard(start)
        if unreachable:
            result.errors.append(
                f"Unreachable solo scenes (no inbound reference): {sorted(unreachable)}"
            )
            result.checks["QA-SI-REACH"] = "FAIL"
        else:
            result.checks["QA-SI-REACH"] = "PASS"

    if result.errors:
        result.status = "FAIL"
    return result


def main(argv: list[str] | None = None) -> int:
    import sys

    args = argv or sys.argv[1:]
    if not args:
        print("Usage: python3 -m idne.single_investigator_validate <adventure_root>")
        return 2
    res = validate_single_investigator(args[0])
    print(json.dumps(res.to_dict(), indent=2))
    if res.status == "SKIP":
        return 0
    return 0 if res.status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
