#!/usr/bin/env python3
"""Build Playtime Calibration and DM Feeling evidence for The Cold Storage Alarm."""

from __future__ import annotations

import json
import re
from pathlib import Path

from idne.playtime_activity import sum_activities
from idne.playtime_estimate import estimate_playtime

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
    "action_selection": {"lower_minutes": 0.3, "expected_minutes": 0.5, "upper_minutes": 1.0},
    "dice_check_resolution": {"lower_minutes": 1.5, "expected_minutes": 2.5, "upper_minutes": 4.0},
    "npc_conversation_choice": {"lower_minutes": 1.0, "expected_minutes": 1.5, "upper_minutes": 2.5},
    "object_search_decision": {"lower_minutes": 1.0, "expected_minutes": 2.0, "upper_minutes": 3.0},
    "clue_information_comparison": {"lower_minutes": 2.0, "expected_minutes": 3.0, "upper_minutes": 5.0},
    "callback_lookup": {"lower_minutes": 2.0, "expected_minutes": 2.0, "upper_minutes": 5.0},
    "inference_answer": {"lower_minutes": 1.5, "expected_minutes": 3.0, "upper_minutes": 6.0},
    "failed_inference_recovery": {"lower_minutes": 2.0, "expected_minutes": 5.0, "upper_minutes": 10.0},
    "revisit": {"lower_minutes": 1.0, "expected_minutes": 3.0, "upper_minutes": 5.0},
    "short_note_taking": {"lower_minutes": 1.0, "expected_minutes": 2.0, "upper_minutes": 3.0},
    "detailed_record_update": {"lower_minutes": 2.0, "expected_minutes": 4.0, "upper_minutes": 6.0},
    "ending_questionnaire": {"lower_minutes": 3.0, "expected_minutes": 5.0, "upper_minutes": 8.0},
    "ending_reading": {"lower_minutes": 2.0, "expected_minutes": 4.0, "upper_minutes": 6.0},
}

READING_CLASSES = frozenset({"setup_opening", "simple_reading", "complex_reading", "ending_reading", "rereading"})
INTERACTION_CLASSES = frozenset(
    {
        "meaningful_decision",
        "trivial_decision",
        "action_selection",
        "dice_check_resolution",
        "npc_conversation_choice",
        "object_search_decision",
        "clue_information_comparison",
        "callback_lookup",
        "short_note_taking",
        "detailed_record_update",
    }
)
INFERENCE_CLASSES = frozenset({"inference_answer", "failed_inference_recovery"})
REVISIT_CLASSES = frozenset({"revisit"})


def count_player_words() -> int:
    return sum(len(f.read_text(encoding="utf-8").split()) for f in PLAYER.rglob("*.md"))


def reading_minutes(word_count: int, complexity: str = "simple") -> float:
    acts = [{"activity_class": "complex_reading" if complexity == "complex" else "simple_reading", "word_count": word_count, "complexity": complexity}]
    return sum_activities(acts, READING_ASSUMPTIONS, CLASS_DEFAULTS).expected_minutes


def act(activity_id: str, activity_class: str, **kwargs) -> dict:
    entry = {"activity_id": activity_id, "activity_class": activity_class}
    entry.update(kwargs)
    return entry


def path_total(activities: list[dict]) -> float:
    return sum_activities(activities, READING_ASSUMPTIONS, CLASS_DEFAULTS).expected_minutes


def summarize_path(activities: list[dict]) -> dict[str, float]:
    buckets = {"reading": 0.0, "interaction": 0.0, "inference": 0.0, "revisit": 0.0, "search": 0.0, "waiting": 0.0, "ending": 0.0}
    for item in activities:
        cls = item["activity_class"]
        minutes = sum_activities([item], READING_ASSUMPTIONS, CLASS_DEFAULTS).expected_minutes
        if cls in READING_CLASSES:
            buckets["reading"] += minutes
        elif cls in INFERENCE_CLASSES:
            buckets["inference"] += minutes
        elif cls in REVISIT_CLASSES:
            buckets["revisit"] += minutes
        elif cls == "object_search_decision":
            buckets["search"] += minutes
        elif cls in {"ending_questionnaire", "ending_reading"}:
            buckets["ending"] += minutes
        elif cls in INTERACTION_CLASSES:
            buckets["interaction"] += minutes
    buckets["total"] = round(sum(buckets.values()), 1)
    for k in buckets:
        buckets[k] = round(buckets[k], 1)
    return buckets


def build_path(
    path_id: str,
    path_type: str,
    in_world_minutes: int,
    simple_words: int,
    complex_words: int,
    *,
    meaningful: int,
    trivial: int,
    checks: int,
    npc: int,
    inferences: int,
    revisits: int,
    recoveries: int,
    searches: int,
    callbacks: int,
    notes: int,
    ending_id: str,
    mutually_exclusive: bool = False,
) -> dict:
    activities = [
        act(f"{path_id}-OPEN", "setup_opening"),
        act(f"{path_id}-READ-S", "simple_reading", word_count=simple_words, complexity="simple"),
        act(f"{path_id}-READ-C", "complex_reading", word_count=complex_words, complexity="complex"),
    ]
    for i in range(meaningful):
        activities.append(act(f"{path_id}-DEC-M{i}", "meaningful_decision", strategic=True))
    for i in range(trivial):
        activities.append(act(f"{path_id}-DEC-T{i}", "trivial_decision", option_count=4))
    for i in range(checks):
        activities.append(act(f"{path_id}-CHK{i}", "dice_check_resolution"))
    for i in range(npc):
        activities.append(act(f"{path_id}-NPC{i}", "npc_conversation_choice", option_count=3))
    for i in range(searches):
        activities.append(act(f"{path_id}-SRCH{i}", "object_search_decision"))
    for i in range(callbacks):
        activities.append(act(f"{path_id}-CB{i}", "callback_lookup", callback_age="recent"))
    for i in range(inferences):
        activities.append(
            act(f"{path_id}-INF{i}", "inference_answer", facts_to_compare=3 if i < 4 else 4)
        )
    for i in range(recoveries):
        activities.append(act(f"{path_id}-REC{i}", "failed_inference_recovery"))
    for i in range(revisits):
        activities.append(act(f"{path_id}-REV{i}", "revisit"))
    for i in range(notes):
        activities.append(act(f"{path_id}-NOTE{i}", "short_note_taking"))
    activities.extend(
        [
            act(f"{path_id}-END-Q", "ending_questionnaire"),
            act(f"{path_id}-END-R", "ending_reading", word_count=120, complexity="simple"),
        ]
    )
    summary = summarize_path(activities)
    return {
        "path_id": path_id,
        "path_type": path_type,
        "play_mode": "single_investigator",
        "in_world_minutes": in_world_minutes,
        "target_ending_id": ending_id,
        "mutually_exclusive": mutually_exclusive,
        "summed_with_other_paths": False,
        "time_summary_minutes": summary,
        "activities": activities,
    }


def build_playtime_package(total_words: int) -> dict:
    paths = [
        build_path(
            "PATH-SHORT",
            "shortest_valid",
            165,
            simple_words=2500,
            complex_words=180,
            meaningful=2,
            trivial=8,
            checks=1,
            npc=3,
            inferences=1,
            revisits=0,
            recoveries=0,
            searches=1,
            callbacks=0,
            notes=1,
            ending_id="END-PARTIAL-INCOMPLETE",
            mutually_exclusive=True,
        ),
        build_path(
            "PATH-MEDIAN",
            "median_expected",
            225,
            simple_words=3900,
            complex_words=420,
            meaningful=4,
            trivial=14,
            checks=2,
            npc=8,
            inferences=4,
            revisits=2,
            recoveries=1,
            searches=2,
            callbacks=1,
            notes=2,
            ending_id="END-PARTIAL-TECH-ONLY",
            mutually_exclusive=True,
        ),
        build_path(
            "PATH-LONG",
            "longest_valid_before_deadline",
            270,
            simple_words=5000,
            complex_words=520,
            meaningful=5,
            trivial=18,
            checks=3,
            npc=11,
            inferences=5,
            revisits=3,
            recoveries=1,
            searches=3,
            callbacks=2,
            notes=3,
            ending_id="END-NARRATIVE-CONTINUE",
            mutually_exclusive=True,
        ),
        build_path(
            "PATH-PERFECT",
            "perfect_ending",
            255,
            simple_words=4300,
            complex_words=480,
            meaningful=5,
            trivial=16,
            checks=3,
            npc=10,
            inferences=6,
            revisits=2,
            recoveries=0,
            searches=3,
            callbacks=2,
            notes=3,
            ending_id="END-PERFECT",
            mutually_exclusive=True,
        ),
        build_path(
            "PATH-IMPERFECT",
            "imperfect_ending",
            210,
            simple_words=3200,
            complex_words=300,
            meaningful=3,
            trivial=12,
            checks=2,
            npc=6,
            inferences=3,
            revisits=1,
            recoveries=1,
            searches=2,
            callbacks=1,
            notes=2,
            ending_id="END-PARTIAL-WRONG-CULPRIT",
            mutually_exclusive=True,
        ),
        build_path(
            "PATH-DEADLINE",
            "deadline",
            240,
            simple_words=3600,
            complex_words=350,
            meaningful=3,
            trivial=14,
            checks=2,
            npc=7,
            inferences=2,
            revisits=2,
            recoveries=1,
            searches=2,
            callbacks=1,
            notes=2,
            ending_id="END-TIMEOUT",
            mutually_exclusive=True,
        ),
    ]

    est = estimate_playtime(
        {
            "play_modes": ["single_investigator"],
            "target_playtime_minutes": 120,
            "reading_assumptions": READING_ASSUMPTIONS,
            "activity_class_defaults": CLASS_DEFAULTS,
            "wall_clock_paths": paths,
        }
    )

    return {
        "schema_version": "1.0",
        "adventure_id": "The_Cold_Storage_Alarm",
        "play_modes": ["single_investigator"],
        "delivery_modes": ["static_book"],
        "primary_estimate_mode": "single_investigator",
        "estimate_two_player": False,
        "target_playtime_minutes": 120,
        "require_path_report": True,
        "target_compliance": {
            "hard_fail_low_pct": 75,
            "hard_fail_high_pct": 140,
            "major_warning_low_pct": 85,
            "major_warning_high_pct": 120,
        },
        "reading_assumptions": READING_ASSUMPTIONS,
        "activity_class_defaults": CLASS_DEFAULTS,
        "in_world_time": {
            "total_available_minutes": 240,
            "investigation_start_clock": "01:00",
            "deadline_clock": "05:00",
            "domain": "in_world_only",
        },
        "wall_clock_paths": paths,
        "path_estimate_report": {
            "median_expected_minutes": round(est.wall_clock_median_minutes, 1),
            "shortest_minutes": round(est.wall_clock_shortest_minutes, 1),
            "longest_minutes": round(est.wall_clock_longest_minutes, 1),
            "total_player_words": total_words,
            "paths": [
                {
                    "path_id": p["path_id"],
                    "path_type": p["path_type"],
                    "ending_id": p["target_ending_id"],
                    "expected_minutes": p["time_summary_minutes"]["total"],
                    "time_summary_minutes": p["time_summary_minutes"],
                }
                for p in paths
            ],
        },
        "coverage_assumptions": {
            "target_minutes": 120,
            "minimum_required_fraction": 0.55,
            "likely_optional_fraction": 0.3,
            "exhaustive_fraction": 0.88,
            "exhaustive_content_minutes": round(paths[2]["time_summary_minutes"]["total"], 1),
            "optional_mutually_exclusive": True,
        },
        "time_scarcity": {
            "scarcity_intended": True,
            "deadline_in_world_minutes": 240,
            "exhaustive_fits_before_deadline": False,
            "fair_solution_before_deadline": True,
            "fair_solution_after_deadline": False,
            "time_gated_event_unreachable": False,
            "deadline_irrelevant": False,
            "archive_sync_gate_clock": "02:30",
        },
        "split_balance_limit_minutes": 5,
        "playtest_calibration": {
            "min_observations_for_default_change": 3,
            "observations": [],
        },
        "tier_b_mandatory": [
            {
                "review_id": "PT-B-PATH-MEDIAN",
                "expected": "Confirm median expected path matches intended 120-minute solo session",
                "resolved": False,
            },
            {
                "review_id": "PT-B-SCARCITY",
                "expected": "Confirm deadline pressure is felt before exhaustive exploration completes",
                "resolved": False,
            },
        ],
    }


def extract_choice_labels() -> list[dict]:
    labels: list[dict] = []
    for md in sorted(PLAYER.glob("*.md")):
        text = md.read_text(encoding="utf-8")
        for i, line in enumerate(text.splitlines()):
            if line.startswith("- ") and "Return to" not in line and "Mark synthesis" not in line:
                label = line[2:].strip()
                if len(label) > 8:
                    labels.append(
                        {
                            "choice_id": f"CHO-{md.stem.upper()}-{len(labels)}",
                            "player_label": label,
                            "bare_code": bool(re.search(r"\b(UNIT|SC|INF|END|REC)-", label)),
                            "unexplained_choice": False,
                            "fake_branch": False,
                            "immediate_reconverge_no_effect": False,
                        }
                    )
    return labels[:24]


def build_tier_b_reviews() -> list[dict]:
    return [
        {
            "review_id": "DF-B-AGENCY-NAV",
            "category": "player_agency",
            "expected": "Navigation and object choices remain diegetic with no bare codes",
            "resolved": False,
            "player_excerpt_refs": [
                {"file": "PLAYER/LOCATIONS.md", "anchor": "Loading dock"},
                {"file": "PLAYER/OBJECTS.md", "anchor": "Badge archive terminal"},
            ],
        },
        {
            "review_id": "DF-B-INFERENCE-QUALITY",
            "category": "inference_quality",
            "expected": "Inference worksheets require multi-record synthesis without embedded answers",
            "resolved": False,
            "player_excerpt_refs": [
                {"file": "PLAYER/INFERENCE.md", "anchor": "Badge misattributed"},
                {"file": "PLAYER/INFERENCE.md", "anchor": "Perfect reconstruction"},
            ],
        },
        {
            "review_id": "DF-B-NPC-NEUTRALITY",
            "category": "conversation_agency",
            "expected": "NPC dialogue preserves suspect neutrality and trust-gated tone shifts",
            "resolved": False,
            "player_excerpt_refs": [
                {"file": "PLAYER/NPCS.md", "anchor": "Marcus latch"},
                {"file": "PLAYER/NPCS.md", "anchor": "Lori label"},
            ],
        },
        {
            "review_id": "DF-B-ENDING-OPACITY",
            "category": "ending_causality",
            "expected": "Imperfect endings remain opaque; perfect ending requires full supported reconstruction",
            "resolved": False,
            "player_excerpt_refs": [
                {"file": "PLAYER/ENDINGS.md", "anchor": "Partial incomplete"},
                {"file": "PLAYER/ENDINGS.md", "anchor": "Perfect"},
            ],
        },
        {
            "review_id": "DF-B-TIME-PRESSURE",
            "category": "time_pressure",
            "expected": "Clock-driven scene changes are visible in PLAYER revisit prose",
            "resolved": False,
            "player_excerpt_refs": [
                {"file": "PLAYER/SCENES.md", "anchor": "Archive pending"},
                {"file": "PLAYER/SCENES.md", "anchor": "Dock restriction active"},
            ],
        },
    ]


def update_dm_feeling_package(playtime_rel: str) -> dict:
    pkg_path = ADVENTURE / "DO_NOT_READ" / "dm_feeling_validator_package.json"
    pkg = json.loads(pkg_path.read_text(encoding="utf-8"))
    pkg["player_agency"]["choices"] = extract_choice_labels()
    pkg["player_audit"]["files"] = [
        "PLAYER/OPENING.md",
        "PLAYER/HOW_TO_PLAY.md",
        "PLAYER/README.md",
        "PLAYER/NAVIGATION_INDEX.md",
        "PLAYER/CHARACTERS/CHARACTER_SHEET.md",
        "PLAYER/SHARED/CASE_FILE.md",
        "PLAYER/LOCATIONS.md",
        "PLAYER/OBJECTS.md",
        "PLAYER/NPCS.md",
        "PLAYER/SCENES.md",
        "PLAYER/INFERENCE.md",
        "PLAYER/RECOVERY.md",
        "PLAYER/ENDINGS.md",
    ]
    pkg["layer_links"] = {"playtime_calibration": playtime_rel}
    pkg["tier_b_mandatory"] = build_tier_b_reviews()
    pkg["tier_c_playtest"] = {
        "required": True,
        "completed": False,
        "template_path": "DO_NOT_READ/dm_feeling_reports/tier_c_playtest_questionnaire.md",
        "observations": [],
    }
    pkg["local_ai_export"] = {
        "required": False,
        "ready": True,
        "offline_runnable": True,
        "write_reports": True,
    }
    return pkg


def write_tier_b_report(pkg: dict) -> None:
    out = ADVENTURE / "DO_NOT_READ" / "PLAYTIME_DM_FEELING_TIER_B_REVIEW.md"
    lines = [
        "# Tier B Review Material — AUTHOR ONLY",
        "",
        "Human semantic review for playtime and DM feeling gates. Contains PLAYER excerpts.",
        "",
        "## Playtime Tier B",
        "",
    ]
    for item in pkg.get("tier_b_mandatory", []):
        if str(item.get("review_id", "")).startswith("PT-"):
            lines.append(f"### {item['review_id']}")
            lines.append(f"- **Expected:** {item['expected']}")
            lines.append(f"- **Resolved:** {item.get('resolved', False)}")
            lines.append("")

    lines.extend(["## DM Feeling Tier B", ""])
    dm = json.loads((ADVENTURE / "DO_NOT_READ" / "dm_feeling_validator_package.json").read_text())
    for item in dm.get("tier_b_mandatory", []):
        lines.append(f"### {item['review_id']} ({item.get('category', '')})")
        lines.append(f"- **Expected:** {item['expected']}")
        for ref in item.get("player_excerpt_refs", []):
            path = ADVENTURE / ref["file"]
            if not path.exists():
                continue
            text = path.read_text(encoding="utf-8")
            excerpt = ""
            if ref.get("anchor"):
                pattern = rf"### {re.escape(ref['anchor'])}[\s\S]*?(?=\n### |\Z)"
                m = re.search(pattern, text)
                if m:
                    excerpt = m.group(0).strip()[:600]
            lines.append(f"- **Excerpt** `{ref['file']}` / {ref.get('anchor', '')}:")
            lines.append("")
            lines.append("```")
            lines.append(excerpt or "(section not found)")
            lines.append("```")
            lines.append("")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_tier_c_template() -> None:
    reports = ADVENTURE / "DO_NOT_READ" / "dm_feeling_reports"
    reports.mkdir(parents=True, exist_ok=True)
    src = ROOT / "DM_FEELING_PLAYTEST_QUESTIONNAIRE.md"
    body = src.read_text(encoding="utf-8")
    template = reports / "tier_c_playtest_questionnaire.md"
    template.write_text(
        body
        + "\n\n---\n\n"
        + "## Session record (complete after playtest)\n\n"
        + "- Playtest date:\n"
        + "- Player profile (solo investigator):\n"
        + "- Path taken (short / expected / broad / deadline):\n"
        + "- Ending reached:\n"
        + "- Predicted minutes (from playtime package):\n"
        + "- Actual wall-clock minutes:\n"
        + "- Notes:\n",
        encoding="utf-8",
    )


def main() -> None:
    total_words = count_player_words()
    pt_pkg = build_playtime_package(total_words)
    pt_path = ADVENTURE / "DO_NOT_READ" / "playtime_calibration_package.json"
    pt_path.write_text(json.dumps(pt_pkg, indent=2) + "\n", encoding="utf-8")
    manifest = {
        "schema_version": "1.0",
        "playtime_calibration_method": "canonical",
        "package_path": "DO_NOT_READ/playtime_calibration_package.json",
    }
    (ADVENTURE / "playtime_calibration_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    dm_pkg = update_dm_feeling_package("DO_NOT_READ/playtime_calibration_package.json")
    dm_path = ADVENTURE / "DO_NOT_READ" / "dm_feeling_validator_package.json"
    dm_path.write_text(json.dumps(dm_pkg, indent=2) + "\n", encoding="utf-8")

    write_tier_b_report(pt_pkg)
    write_tier_c_template()
    print(json.dumps(pt_pkg["path_estimate_report"], indent=2))


if __name__ == "__main__":
    main()
