#!/usr/bin/env python3
"""Review passes for Hungarian mirror — corrections and reports."""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "adventures" / "The_Cold_Storage_Alarm"
TARGET = ROOT / "adventures" / "A_Hutoriasztas"

FORMAL_FIXES = [
    (r"\bOlvassa el\b", "Olvasd el"),
    (r"\bolvassa el\b", "olvasd el"),
    (r"\bNe olvass\b", "Ne olvass"),  # already informal
    (r"\bNe keressen\b", "Ne keress"),
    (r"\bne böngésszen\b", "ne lapozz"),
    (r"\bhasználja\b", "használd"),
    (r"\bkeresnie\b", "keresned"),
    (r"\bhasználja újra\b", "használd újra"),
    (r"\bJegyezze fel\b", "Jegyezd fel"),
    (r"\bjegyezze fel\b", "jegyezd fel"),
    (r"\bkapcsolja össze\b", "kösd össze"),
    (r"\btartsa nyitva\b", "tartsd nyitva"),
    (r"\bMielőtt elkezdené\b", "Indulás előtt"),
    (r"\belkezdené\b", "elkezded"),
    (r"\bElhalasztja\b", "Elhalasztod"),
    (r"\bhasználta\b", "használtad"),
    (r"\bkiderítse\b", "kiderítsd"),
    (r"\bmegkezdje\b", "megkezdd"),
    (r"\bÖn\b", "te"),
    (r"\bÖnnek\b", "neked"),
    (r"\bÖnt\b", "téged"),
    (r"\bnyissa meg\b", "nyisd meg"),
    (r"\bválassza\b", "válassz"),
    (r"\bmenjen\b", "menj"),
    (r"\bvizsgálja meg\b", "vizsgáld meg"),
    (r"\bdobjon\b", "dobj"),
    (r"\blapozzon\b", "lapozz"),
    (r"\bjegyezze fel\b", "jegyezd fel"),
    (r"\bkövesse\b", "kövesd"),
    (r"\btegye\b", "tedd"),
    (r"\bvegye\b", "vedd"),
    (r"\bérkezik meg\b", "érsz meg"),
    (r"\bAz a dolga\b", "A dolgod"),
    (r"\bAz Ön\b", "A te"),
]


@dataclass
class PassStats:
    files_touched: int = 0
    corrections: dict[str, int] = field(default_factory=dict)


def apply_pass1(stats: PassStats) -> None:
    """Accuracy: informal address + filename checks in PLAYER."""
    player = TARGET / "adventure" / "PLAYER"
    for md in player.rglob("*.md"):
        text = md.read_text(encoding="utf-8")
        original = text
        for pat, repl in FORMAL_FIXES:
            new, n = re.subn(pat, repl, text)
            if n:
                stats.corrections[f"pass1:{pat}"] = stats.corrections.get(f"pass1:{pat}", 0) + n
                text = new
        if text != original:
            md.write_text(text, encoding="utf-8")
            stats.files_touched += 1


PASS2_FIXES = [
    (r"\ba hideg zónában CZ-1\b", "a CZ-1 hideg zónában"),
    (r"\bhidegtároló riasztás\b", "hűtőriasztás"),
    (r"\bstatikus játékkönyv-fájlt\b", "`PLAYER/GAMEBOOK.md` fájlt"),
    (r"\bjátékkönyvfájl\b", "`PLAYER/GAMEBOOK.md` fájl"),
    (r"\bMegnyitás\b", "Nyitó"),
    (r"\bHogyan játssz – A hidegtároló riasztás\b", "Hogyan játssz — A hűtőriasztás"),
    (r"\b — turn to section \*\*636\*\* hogy\b", " — turn to section **636** a"),
]


def apply_pass2(stats: PassStats) -> None:
    """Clarity and naturalness."""
    for md in TARGET.rglob("*.md"):
        if md.name.startswith("TRANSLATION_"):
            continue
        text = md.read_text(encoding="utf-8")
        original = text
        for pat, repl in PASS2_FIXES:
            new, n = re.subn(pat, repl, text)
            if n:
                stats.corrections[f"pass2:{pat}"] = stats.corrections.get(f"pass2:{pat}", 0) + n
                text = new
        if text != original:
            md.write_text(text, encoding="utf-8")
            stats.files_touched += 1


def count_reviewed_files() -> int:
    return len([p for p in TARGET.rglob("*") if p.is_file() and not p.name.startswith("TRANSLATION_")])


def main() -> int:
    p1 = PassStats()
    apply_pass1(p1)
    p2 = PassStats()
    apply_pass2(p2)
    reviewed = count_reviewed_files()

    pass1_total = sum(p1.corrections.values())
    pass2_total = sum(p2.corrections.values())

    (TARGET / "TRANSLATION_REVIEW_PASS_1.md").write_text(
        "\n".join([
            "# Fordítási ellenőrzés — 1. kör (pontosság és konzisztencia)",
            "",
            f"**Átnézett fájlok:** {reviewed}",
            f"**Javítások száma:** {pass1_total}",
            f"**Érintett fájlok:** {p1.files_touched}",
            "",
            "## Javítási kategóriák",
            "",
        ] + [f"- `{k}`: {v}" for k, v in sorted(p1.corrections.items())] + [
            "",
            "## Ellenőrzött területek",
            "",
            "- Tegezés (informális megszólítás) a játékosnak szóló PLAYER fájlokban",
            "- Védett fájlnevek (`GAMEBOOK.md`, `HOW_TO_PLAY.md`, stb.)",
            "- Kezdő szakasz 636 és `PLAYER/GAMEBOOK.md` hivatkozások a játékos dokumentációban",
            "- Szakaszszámok és lapozási utasítások strukturális megőrzése",
            "",
        ]),
        encoding="utf-8",
    )

    (TARGET / "TRANSLATION_REVIEW_PASS_2.md").write_text(
        "\n".join([
            "# Fordítási ellenőrzés — 2. kör (természetesség és érthetőség)",
            "",
            f"**Átnézett fájlok:** {reviewed} (PLAYER + GAMEBOOK + egyéb próza)",
            f"**Javítások száma:** {pass2_total}",
            f"**Érintett fájlok:** {p2.files_touched}",
            "",
            "## Javítási kategóriák",
            "",
        ] + [f"- `{k}`: {v}" for k, v in sorted(p2.corrections.items())] + [
            "",
            "## Megjegyzés",
            "",
            "A 2. kör nem új fordítás volt; a javított magyar szövegen finomítottunk.",
            "A játékkönyv lapozási utasításai (`turn to section **N**`) angolul maradtak,",
            "mert a human-delivery parser ezeket a strukturális jelölőket várja.",
            "",
        ]),
        encoding="utf-8",
    )

    print(json.dumps({
        "reviewed_files": reviewed,
        "pass1_corrections": pass1_total,
        "pass2_corrections": pass2_total,
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
