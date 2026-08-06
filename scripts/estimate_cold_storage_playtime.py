#!/usr/bin/env python3
"""Provisional path-sensitive playtime estimate for The Cold Storage Alarm."""

from __future__ import annotations

import json
import re
from pathlib import Path

from idne.playtime_activity import sum_activities

ROOT = Path(__file__).resolve().parents[1]
ADV = ROOT / "adventures" / "The_Cold_Storage_Alarm"
ADVENTURE = ADV / "adventure"
PLAYER = ADVENTURE / "PLAYER"

READING_ASSUMPTIONS = {
    "simple_seconds_per_word": 1,
    "complex_seconds_per_word": 2,
    "reread_add_full_reading_plus_seconds": 10,
    "callback_recent_minutes": 2,
    "callback_old_minutes": 5,
    "callback_old_threshold_minutes": 60,
}

CLASS_DEFAULTS = {
    "setup_opening": {"lower_minutes": 3.0, "expected_minutes": 4.0, "upper_minutes": 5.0},
    "simple_reading": {"lower_minutes": 0.5, "expected_minutes": 1.0, "upper_minutes": 1.5},
    "complex_reading": {"lower_minutes": 1.0, "expected_minutes": 2.0, "upper_minutes": 3.0},
    "meaningful_decision": {"lower_minutes": 2.0, "expected_minutes": 4.0, "upper_minutes": 8.0},
    "trivial_decision": {"lower_minutes": 0.3, "expected_minutes": 0.5, "upper_minutes": 1.0},
    "dice_check_resolution": {"lower_minutes": 1.5, "expected_minutes": 2.5, "upper_minutes": 4.0},
    "npc_conversation_choice": {"lower_minutes": 1.0, "expected_minutes": 1.5, "upper_minutes": 2.5},
    "inference_answer": {"lower_minutes": 1.5, "expected_minutes": 3.0, "upper_minutes": 6.0},
    "failed_inference_recovery": {"lower_minutes": 2.0, "expected_minutes": 5.0, "upper_minutes": 10.0},
    "revisit": {"lower_minutes": 1.0, "expected_minutes": 3.0, "upper_minutes": 5.0},
    "short_note_taking": {"lower_minutes": 1.0, "expected_minutes": 2.0, "upper_minutes": 3.0},
    "ending_questionnaire": {"lower_minutes": 3.0, "expected_minutes": 5.0, "upper_minutes": 8.0},
    "ending_reading": {"lower_minutes": 2.0, "expected_minutes": 4.0, "upper_minutes": 6.0},
}

UNIT_HEADER = re.compile(r"^<!-- unit:([a-z0-9-]+) -->", re.M)


def word_count(path: Path) -> int:
    return len(path.read_text(encoding="utf-8").split())


def words_for_units(unit_ids: set[str]) -> int:
    total = 0
    for md in PLAYER.rglob("*.md"):
        text = md.read_text(encoding="utf-8")
        parts = UNIT_HEADER.split(text)
        # parts alternate: preamble, id, body, id, body...
        for i in range(1, len(parts), 2):
            uid_slug = parts[i]
            body = parts[i + 1] if i + 1 < len(parts) else ""
            uid = uid_slug.upper().replace("unit-", "UNIT-").replace("sc-", "SC-").replace("inf-", "INF-").replace("end-", "END-").replace("rec-", "REC-")
            # normalize known prefixes
            for prefix in ("UNIT-", "SC-", "INF-", "END-", "REC-"):
                if uid_slug.upper().startswith(prefix.lower().replace("-", "")):
                    break
            candidates = {uid_slug.upper(), uid_slug.upper().replace("-", "_")}
            key_variants = {uid_slug.upper()}
            if uid_slug.startswith("unit-"):
                key_variants.add("UNIT-" + uid_slug[5:].upper())
            if uid_slug.startswith("sc-"):
                key_variants.add("SC-" + uid_slug[3:].upper())
            if uid_slug.startswith("inf-"):
                key_variants.add("INF-" + uid_slug[4:].upper().replace("-", "-"))
            if uid_slug.startswith("end-"):
                key_variants.add("END-" + uid_slug[4:].upper())
            if uid_slug.startswith("rec-"):
                key_variants.add("REC-" + uid_slug[4:].upper())
            mapped = False
            for key in unit_ids:
                if key.lower().replace("_", "-") == uid_slug or key.lower() == uid_slug:
                    mapped = True
                    break
                if key.lower().endswith(uid_slug.split("-", 1)[-1]) and uid_slug.split("-")[0] in key.lower():
                    mapped = True
                    break
            if not mapped:
                continue
            total += len(body.split())
    return total


def count_player_words() -> int:
    return sum(word_count(p) for p in PLAYER.rglob("*.md"))


def build_path(path_id: str, path_type: str, reading_words: int, activities: list[dict]) -> dict:
    acts = [
        {"activity_id": "ACT-OPEN", "activity_class": "setup_opening"},
        {
            "activity_id": "ACT-READ",
            "activity_class": "simple_reading",
            "word_count": reading_words,
            "complexity": "simple",
        },
        *activities,
        {"activity_id": "ACT-END-Q", "activity_class": "ending_questionnaire"},
        {"activity_id": "ACT-END-R", "activity_class": "ending_reading", "word_count": 80, "complexity": "simple"},
    ]
    est = sum_activities(acts, READING_ASSUMPTIONS, CLASS_DEFAULTS)
    return {
        "path_id": path_id,
        "path_type": path_type,
        "expected_minutes": round(est.expected_minutes, 1),
        "reading_words": reading_words,
        "activities": len(acts),
    }


def estimate() -> dict:
    total_words = count_player_words()

    # Path-sensitive unit coverage (provisional; playtime package not yet authored)
    shortest = build_path(
        "PATH-SHORT",
        "shortest_valid",
        reading_words=int(total_words * 0.42),
        activities=[
            {"activity_id": "ACT-DEC-M", "activity_class": "meaningful_decision", "strategic": True},
            {"activity_id": "ACT-DEC-M2", "activity_class": "meaningful_decision", "strategic": True},
            {"activity_id": "ACT-DEC-T", "activity_class": "trivial_decision", "option_count": 10},
            {"activity_id": "ACT-CHK", "activity_class": "dice_check_resolution"},
            {"activity_id": "ACT-NPC", "activity_class": "npc_conversation_choice", "option_count": 4},
            {"activity_id": "ACT-INF", "activity_class": "inference_answer", "facts_to_compare": 2},
        ],
    )
    expected = build_path(
        "PATH-MEDIAN",
        "median_expected",
        reading_words=int(total_words * 0.68),
        activities=[
            {"activity_id": "ACT-DEC-M", "activity_class": "meaningful_decision", "strategic": True},
            {"activity_id": "ACT-DEC-M2", "activity_class": "meaningful_decision", "strategic": True},
            {"activity_id": "ACT-DEC-M3", "activity_class": "meaningful_decision", "strategic": True},
            {"activity_id": "ACT-DEC-T", "activity_class": "trivial_decision", "option_count": 18},
            {"activity_id": "ACT-CHK1", "activity_class": "dice_check_resolution"},
            {"activity_id": "ACT-CHK2", "activity_class": "dice_check_resolution"},
            {"activity_id": "ACT-NPC", "activity_class": "npc_conversation_choice", "option_count": 10},
            {"activity_id": "ACT-INF1", "activity_class": "inference_answer", "facts_to_compare": 3},
            {"activity_id": "ACT-INF2", "activity_class": "inference_answer", "facts_to_compare": 3},
            {"activity_id": "ACT-INF3", "activity_class": "inference_answer", "facts_to_compare": 4},
            {"activity_id": "ACT-REV", "activity_class": "revisit"},
            {"activity_id": "ACT-REV2", "activity_class": "revisit"},
            {"activity_id": "ACT-NOTE", "activity_class": "short_note_taking"},
            {"activity_id": "ACT-NOTE2", "activity_class": "short_note_taking"},
        ],
    )
    broad = build_path(
        "PATH-BROAD",
        "broad_exploration",
        reading_words=int(total_words * 0.88),
        activities=[
            {"activity_id": "ACT-DEC-M", "activity_class": "meaningful_decision", "strategic": True},
            {"activity_id": "ACT-DEC-M2", "activity_class": "meaningful_decision", "strategic": True},
            {"activity_id": "ACT-DEC-M3", "activity_class": "meaningful_decision", "strategic": True},
            {"activity_id": "ACT-DEC-M4", "activity_class": "meaningful_decision", "strategic": True},
            {"activity_id": "ACT-DEC-T", "activity_class": "trivial_decision", "option_count": 24},
            {"activity_id": "ACT-CHK1", "activity_class": "dice_check_resolution"},
            {"activity_id": "ACT-CHK2", "activity_class": "dice_check_resolution"},
            {"activity_id": "ACT-CHK3", "activity_class": "dice_check_resolution"},
            {"activity_id": "ACT-CHK4", "activity_class": "dice_check_resolution"},
            {"activity_id": "ACT-NPC", "activity_class": "npc_conversation_choice", "option_count": 14},
            {"activity_id": "ACT-INF1", "activity_class": "inference_answer", "facts_to_compare": 3},
            {"activity_id": "ACT-INF2", "activity_class": "inference_answer", "facts_to_compare": 3},
            {"activity_id": "ACT-INF3", "activity_class": "inference_answer", "facts_to_compare": 4},
            {"activity_id": "ACT-INF4", "activity_class": "inference_answer", "facts_to_compare": 4},
            {"activity_id": "ACT-INF5", "activity_class": "inference_answer", "facts_to_compare": 5},
            {"activity_id": "ACT-INF6", "activity_class": "inference_answer", "facts_to_compare": 5},
            {"activity_id": "ACT-REV", "activity_class": "revisit"},
            {"activity_id": "ACT-REV2", "activity_class": "revisit"},
            {"activity_id": "ACT-REV3", "activity_class": "revisit"},
            {"activity_id": "ACT-REC", "activity_class": "failed_inference_recovery"},
            {"activity_id": "ACT-NOTE", "activity_class": "short_note_taking"},
            {"activity_id": "ACT-NOTE2", "activity_class": "short_note_taking"},
            {"activity_id": "ACT-NOTE3", "activity_class": "short_note_taking"},
        ],
    )

    target = 120
    median = expected["expected_minutes"]
    achievable = median >= target * 0.85

    reading_min = expected["reading_words"] / 60.0  # 1 sec/word simple
    interaction_min = expected["expected_minutes"] - reading_min - 9  # minus opening+ending bucket

    shortfall_categories = []
    if median < target * 0.85:
        if total_words < 6500:
            shortfall_categories.append("total_player_prose_volume")
        if interaction_min < 35:
            shortfall_categories.append("interaction_and_inference_overhead")
        if broad["expected_minutes"] < target:
            shortfall_categories.append("optional_branch_coverage")

    return {
        "target_minutes": target,
        "total_player_words": total_words,
        "paths": [shortest, expected, broad],
        "reading_time_expected_path_minutes": round(reading_min, 1),
        "interaction_inference_revisit_expected_path_minutes": round(max(interaction_min, 0), 1),
        "approximately_120_minutes_achievable": achievable,
        "shortfall_categories": shortfall_categories,
        "method": "provisional_playtime_calibration_rules_pre_package",
    }


def main() -> None:
    report = estimate()
    out = ADV / "PROVISIONAL_PLAYTIME_ESTIMATE.json"
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
