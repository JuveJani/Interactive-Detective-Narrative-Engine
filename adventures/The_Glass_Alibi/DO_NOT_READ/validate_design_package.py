#!/usr/bin/env python3
"""Manual design-package validation for The Glass Alibi (Milestone B gates)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOGIC = ROOT / "DO_NOT_READ" / "LOGIC"
DESIGN = ROOT / "DO_NOT_READ"

PREFIXES = (
    "NPC_", "LOC_", "ITEM_", "CLUE_", "CON_", "FACT_", "ARC_", "EVT_", "END_",
    "CLK_", "TR_", "EVAL_", "CHK_",
)
LEGACY = re.compile(r"\b[CD]_\d+\b")
EVT_HEADER = re.compile(r"^### `?(EVT_\d+)`?", re.M)
EVT_SECTION = re.compile(r"^## \d+\. .*`(EVT_\d+)`", re.M)
OUTGOING = re.compile(r"^\*\*Outgoing\*\*\s*$", re.M)
SCENE_REGISTRY = re.compile(
    r"^\| `(EVT_\d+)` \| `(Joint|Split)` \|", re.M
)

PLAYABLE_EVT = {
    f"EVT_{n}"
    for n in (
        100, 110, 111, 112, 113, 115, 123, 120, 121, 140, 141, 130, 150,
        210, 230, 260, 250, 270, 271, 122, 240, 300, 220, 312, 330,
        410, 420, 430, 900, 901, 902, 903, 904, 905,
    )
}


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def extract_registry_keys(text: str) -> set[str]:
    keys: set[str] = set()
    for line in text.splitlines():
        m = re.search(r"`((?:NPC|LOC|ITEM|CLUE|CON|CHK|END|ARC|EVT|CLK|TR|EVAL)_[A-Z0-9_]+)`", line)
        if m:
            keys.add(m.group(1))
    return keys


def main() -> int:
    results: list[tuple[str, str, str]] = []
    entity = read(LOGIC / "00_ENTITY_KEY_TABLE.md")
    node_graph = read(LOGIC / "10_INVESTIGATION_NODE_GRAPH.md")
    check_reg = read(LOGIC / "17_CHECK_REGISTER.md")
    clue_graph = read(LOGIC / "12_CLUE_DEPENDENCY_GRAPH.md")
    ending = read(LOGIC / "14_ENDING_TRIGGER_MATRIX.md")
    loc_db = read(DESIGN / "04_LOCATION_DATABASE.md")

    registry_keys = extract_registry_keys(entity)

    # V1 identifier resolution in LOGIC
    logic_text = "\n".join(p.read_text(encoding="utf-8") for p in LOGIC.glob("*.md"))
    legacy_hits = LEGACY.findall(logic_text)
    unknown: list[str] = []
    for m in re.finditer(r"`((?:NPC|LOC|ITEM|CLUE|CON|CHK|END|ARC|EVT|CLK|TR|EVAL)_[A-Z0-9_]+)`", logic_text):
        key = m.group(1)
        if key.startswith("EVT_8"):
            continue
        if key not in registry_keys and not key.startswith("ARC_"):
            # EVT playable nodes may not all be in 00 table
            if key.startswith("EVT_") and key in PLAYABLE_EVT:
                continue
            if key.startswith("TR_") or key.startswith("CLK_") or key.startswith("EVAL_"):
                continue
            unknown.append(key)
    unknown_unique = sorted(set(unknown))
    results.append((
        "V1",
        "PASS" if not legacy_hits and len(unknown_unique) <= 5 else "FAIL",
        f"legacy={len(legacy_hits)} unknown_sample={unknown_unique[:8]}",
    ))

    # V-SM scene modes
    modes = {m.group(1): m.group(2) for m in SCENE_REGISTRY.finditer(node_graph)}
    missing_modes = sorted(PLAYABLE_EVT - set(modes))
    unclassified = [k for k, v in modes.items() if v not in {"Joint", "Split"}]
    joint = sum(1 for v in modes.values() if v == "Joint")
    split = sum(1 for v in modes.values() if v == "Split")
    results.append((
        "V-SM",
        "PASS" if not missing_modes and not unclassified else "FAIL",
        f"joint={joint} split={split} missing={missing_modes}",
    ))

    # V-CHK
    chk_active = len(re.findall(r"`CHK_[A-Z0-9_]+`", check_reg))
    chk_records = len(re.findall(r"^### `CHK_", check_reg, re.M))
    results.append((
        "V-CHK",
        "PASS" if chk_records == 5 else "FAIL",
        f"records={chk_records}",
    ))

    # Clue count
    clue_active = len(re.findall(r"`CLUE_[A-Z0-9_]+`.*`ACTIVE`", entity))
    results.append((
        "CLUE_COUNT",
        "PASS" if clue_active == 16 else "FAIL",
        f"active_clues={clue_active}",
    ))

    # Ending count
    end_count = len(re.findall(r"`END_[A-Z_]+`", ending))
    results.append((
        "ENDING_COUNT",
        "PASS" if end_count >= 5 else "FAIL",
        f"end_refs={end_count}",
    ))

    # Location keys in design 04
    loc_sections = re.findall(r"^## (LOC_[A-Z_]+):", loc_db, re.M)
    bad_locs = [x for x in loc_sections if x not in registry_keys]
    results.append((
        "LOC_ALIGN",
        "PASS" if not bad_locs and len(loc_sections) == 8 else "FAIL",
        f"sections={len(loc_sections)} bad={bad_locs}",
    ))

    # Outgoing edge targets (basic)
    outgoing_blocks = re.split(r"(?=^## |\n### `EVT_)", node_graph, flags=re.M)
    nodes_with_out: set[str] = set()
    targets: set[str] = set()
    for block in outgoing_blocks:
        hm = re.search(r"`(EVT_\d+)`", block[:80])
        if not hm:
            continue
        nid = hm.group(1)
        if "**Outgoing**" in block:
            nodes_with_out.add(nid)
            for t in re.findall(r"`(EVT_\d+)`", block.split("**Outgoing**", 1)[1].split("\n\n", 1)[0]):
                if t != nid:
                    targets.add(t)
    missing_out = sorted(PLAYABLE_EVT - {n for n in PLAYABLE_EVT if n.startswith("EVT_90")} - nodes_with_out)
    # terminals 901-905 have Outgoing: None
    for t in sorted(targets):
        if t not in PLAYABLE_EVT:
            results.append(("GRAPH_EDGE", "FAIL", f"unknown_target={t}"))
            break
    else:
        results.append(("GRAPH_EDGE", "PASS", f"nodes_with_outgoing={len(nodes_with_out)}"))

    # Participation audit present
    split_flow = read(LOGIC / "13_SPLIT_AND_REGROUP_FLOW.md")
    results.append((
        "PARTICIPATION",
        "PASS" if "## 9. Participation audit" in split_flow else "FAIL",
        "audit_section_present",
    ))

    # C6 two_player
    results.append((
        "C6",
        "PASS" if "`two_player`" in node_graph and "**ACTIVE**" in node_graph.split("## 18. Play modes", 1)[-1] else "FAIL",
        "two_player_only",
    ))

    print("The Glass Alibi — validation summary\n")
    failed = 0
    for gate, status, detail in results:
        print(f"{gate:16} {status:4}  {detail}")
        if status == "FAIL":
            failed += 1
    print(f"\nTotal failures: {failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
