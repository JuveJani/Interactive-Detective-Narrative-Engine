"""Generate playtime calibration test fixtures (Milestone 9)."""

import json
from pathlib import Path

FIXTURES = Path(__file__).resolve().parents[1] / "tests" / "fixtures"

DEFAULTS = {
    "simple_reading": {"lower_minutes": 0.5, "expected_minutes": 1.0, "upper_minutes": 1.5},
    "complex_reading": {"lower_minutes": 1.0, "expected_minutes": 2.0, "upper_minutes": 3.0},
    "meaningful_decision": {"lower_minutes": 2.0, "expected_minutes": 4.0, "upper_minutes": 8.0},
    "trivial_decision": {"lower_minutes": 0.3, "expected_minutes": 0.5, "upper_minutes": 1.0},
    "medium_puzzle": {"lower_minutes": 5.0, "expected_minutes": 10.0, "upper_minutes": 20.0},
    "simple_puzzle": {"lower_minutes": 1.0, "expected_minutes": 2.0, "upper_minutes": 4.0},
    "inference_answer": {"lower_minutes": 1.5, "expected_minutes": 3.0, "upper_minutes": 6.0},
    "failed_inference_recovery": {"lower_minutes": 2.0, "expected_minutes": 5.0, "upper_minutes": 10.0},
    "revisit": {"lower_minutes": 1.0, "expected_minutes": 3.0, "upper_minutes": 5.0},
    "ending_questionnaire": {"lower_minutes": 3.0, "expected_minutes": 5.0, "upper_minutes": 8.0},
    "ending_reading": {"lower_minutes": 2.0, "expected_minutes": 4.0, "upper_minutes": 6.0},
    "callback_lookup": {"lower_minutes": 2.0, "expected_minutes": 2.0, "upper_minutes": 5.0},
    "player_discussion": {"lower_minutes": 3.0, "expected_minutes": 5.0, "upper_minutes": 10.0},
    "regroup_discussion": {"lower_minutes": 3.0, "expected_minutes": 5.0, "upper_minutes": 8.0},
    "joint_scene": {"lower_minutes": 5.0, "expected_minutes": 10.0, "upper_minutes": 15.0},
}


def solo_activities(total_minutes: float) -> list[dict]:
    """Build activities summing to approximately total_minutes."""
    chunks = [
        ("setup_opening", 5),
        ("simple_reading", 25),
        ("complex_reading", 15),
        ("meaningful_decision", 12),
        ("inference_answer", 10),
        ("medium_puzzle", 15),
        ("revisit", 8),
        ("failed_inference_recovery", 5),
        ("ending_questionnaire", 5),
        ("ending_reading", 5),
    ]
    scale = total_minutes / sum(c for _, c in chunks)
    acts = []
    for i, (cls, mins) in enumerate(chunks):
        m = mins * scale
        act = {
            "activity_id": f"ACT-{i:03d}",
            "activity_class": cls,
            "authored_lower_minutes": m * 0.9,
            "authored_expected_minutes": m,
            "authored_upper_minutes": m * 1.1,
        }
        if cls == "simple_reading":
            act["word_count"] = int(m * 60)
            act["complexity"] = "simple"
        if cls == "complex_reading":
            act["word_count"] = int(m * 30)
            act["complexity"] = "complex"
        if cls == "meaningful_decision":
            act["strategic"] = True
        if cls == "medium_puzzle":
            act["puzzle_lower_minutes"] = m * 0.8
            act["puzzle_expected_minutes"] = m
            act["puzzle_upper_minutes"] = m * 1.2
        acts.append(act)
    return acts


def base_pt(adventure_id: str, play_modes: list[str], target: int = 120, median_minutes: float = 120) -> dict:
    paths = [
        {
            "path_id": "PATH-SHORT",
            "path_type": "shortest_valid",
            "play_mode": "single_investigator",
            "in_world_minutes": 180,
            "activities": solo_activities(median_minutes * 0.75),
        },
        {
            "path_id": "PATH-MEDIAN",
            "path_type": "median_expected",
            "play_mode": "single_investigator",
            "in_world_minutes": 240,
            "activities": solo_activities(median_minutes),
        },
        {
            "path_id": "PATH-LONG",
            "path_type": "longest_valid_before_deadline",
            "play_mode": "single_investigator",
            "in_world_minutes": 300,
            "activities": solo_activities(median_minutes * 1.15),
        },
        {
            "path_id": "PATH-PERFECT",
            "path_type": "perfect_ending",
            "play_mode": "single_investigator",
            "in_world_minutes": 260,
            "activities": solo_activities(median_minutes * 1.05),
        },
    ]
    return {
        "schema_version": "1.0",
        "adventure_id": adventure_id,
        "play_modes": play_modes,
        "delivery_modes": ["static_book", "ai_dm"],
        "primary_estimate_mode": "single_investigator",
        "estimate_two_player": "two_player" in play_modes,
        "target_playtime_minutes": target,
        "require_path_report": True,
        "target_compliance": {
            "hard_fail_low_pct": 75,
            "hard_fail_high_pct": 140,
            "major_warning_low_pct": 85,
            "major_warning_high_pct": 120,
        },
        "reading_assumptions": {
            "simple_seconds_per_word": 1,
            "complex_seconds_per_word": 2,
            "reread_add_full_reading_plus_seconds": 10,
            "callback_recent_minutes": 2,
            "callback_old_minutes": 5,
            "callback_old_threshold_minutes": 60,
        },
        "activity_class_defaults": DEFAULTS,
        "in_world_time": {"total_available_minutes": 480, "domain": "in_world_only"},
        "wall_clock_paths": paths,
        "coverage_assumptions": {
            "target_minutes": target,
            "minimum_required_fraction": 0.6,
            "likely_optional_fraction": 0.25,
            "exhaustive_fraction": 1.0,
            "exhaustive_content_minutes": median_minutes * 1.8,
        },
        "time_scarcity": {
            "scarcity_intended": True,
            "deadline_in_world_minutes": 480,
            "exhaustive_fits_before_deadline": False,
            "fair_solution_after_deadline": False,
            "time_gated_event_unreachable": False,
            "deadline_irrelevant": False,
        },
        "split_balance_limit_minutes": 5,
        "playtest_calibration": {
            "min_observations_for_default_change": 3,
            "observations": [],
        },
        "tier_b_mandatory": [],
    }


def two_player_model(joint: float = 20, split_a: float = 25, split_b: float = 30, regroup: float = 5) -> dict:
    return {
        "joint_activities": [
            {"activity_id": "J-001", "activity_class": "joint_scene", "authored_expected_minutes": joint}
        ],
        "split_windows": [
            {
                "window_id": "SPLIT-1",
                "branches": [
                    {
                        "player_id": "player_1",
                        "activities": [
                            {
                                "activity_id": "P1-001",
                                "activity_class": "simple_reading",
                                "authored_expected_minutes": split_a,
                                "word_count": int(split_a * 60),
                            }
                        ],
                    },
                    {
                        "player_id": "player_2",
                        "activities": [
                            {
                                "activity_id": "P2-001",
                                "activity_class": "simple_reading",
                                "authored_expected_minutes": split_b,
                                "word_count": int(split_b * 60),
                            }
                        ],
                    },
                ],
            }
        ],
        "regroup_activities": [
            {"activity_id": "R-001", "activity_class": "regroup_discussion", "authored_expected_minutes": regroup}
        ],
        "ending_activities": [
            {"activity_id": "E-001", "activity_class": "ending_questionnaire", "authored_expected_minutes": 8},
            {"activity_id": "E-002", "activity_class": "ending_reading", "authored_expected_minutes": 5},
        ],
        "incorrectly_summed_parallel": False,
    }


def write_fixture(name: str, pkg: dict):
    dest = FIXTURES / name
    if dest.exists():
        import shutil

        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    (dest / "DO_NOT_READ").mkdir(parents=True, exist_ok=True)
    (dest / "DO_NOT_READ" / "playtime_calibration_package.json").write_text(json.dumps(pkg, indent=2) + "\n")
    (dest / "playtime_calibration_manifest.json").write_text(
        json.dumps(
            {
                "schema_version": "1.0",
                "playtime_calibration_method": "canonical",
                "package_path": "DO_NOT_READ/playtime_calibration_package.json",
            },
            indent=2,
        )
        + "\n"
    )


MUTATIONS: dict[str, callable] = {}


def mut_solo_30(p):
    p["wall_clock_paths"] = [
        {
            "path_id": "PATH-MEDIAN",
            "path_type": "median_expected",
            "play_mode": "single_investigator",
            "activities": solo_activities(30),
        }
    ]
    p["require_path_report"] = False
    return p


def mut_parallel_summed(p):
    p["play_modes"] = ["two_player"]
    p["estimate_two_player"] = True
    p["primary_estimate_mode"] = "two_player"
    tp = two_player_model(20, 40, 50, 5)
    tp["incorrectly_summed_parallel"] = True
    tp["incorrect_parallel_sum_minutes"] = 20 + 40 + 50 + 5 + 13  # sum both branches
    p["two_player_model"] = tp


def mut_valid_two_player(p):
    p["play_modes"] = ["single_investigator", "two_player"]
    p["estimate_two_player"] = True
    p["primary_estimate_mode"] = "two_player"
    p["two_player_model"] = two_player_model(45, 44, 48, 15)


def mut_mutex_summed(p):
    p["wall_clock_paths"].append(
        {
            "path_id": "PATH-ALT",
            "path_type": "mutually_exclusive_branch",
            "play_mode": "single_investigator",
            "mutually_exclusive": True,
            "summed_with_other_paths": True,
            "activities": solo_activities(60),
        }
    )


def mut_simple_complex(p):
    act = p["wall_clock_paths"][1]["activities"][1]
    act.update({"complexity": "simple", "complexity_misclassified_as_complex": True, "word_count": 600})


def mut_reread(p):
    p["wall_clock_paths"][1]["activities"].append(
        {
            "activity_id": "ACT-REREAD",
            "activity_class": "rereading",
            "word_count": 200,
            "reread_expected": True,
        }
    )


def mut_callback_recent(p):
    p["wall_clock_paths"][1]["activities"].append(
        {"activity_id": "ACT-CB-REC", "activity_class": "callback_lookup", "callback_age": "recent"}
    )


def mut_callback_old(p):
    p["wall_clock_paths"][1]["activities"].append(
        {
            "activity_id": "ACT-CB-OLD",
            "activity_class": "callback_lookup",
            "callback_age": "old",
            "minutes_since_introduction": 90,
        }
    )


def mut_fake_decision(p):
    p["wall_clock_paths"][1]["activities"].append(
        {
            "activity_id": "ACT-BARE",
            "activity_class": "meaningful_decision",
            "bare_destination_code": True,
            "meaningful_decision_credit": True,
            "decision_expected_minutes": 5,
        }
    )


def mut_meaningful_decision(p):
    p["wall_clock_paths"][1]["activities"].append(
        {
            "activity_id": "ACT-STRAT",
            "activity_class": "meaningful_decision",
            "strategic": True,
            "option_count": 4,
            "decision_expected_minutes": 6,
        }
    )


def mut_simple_inference(p):
    p["wall_clock_paths"][1]["activities"].append(
        {"activity_id": "ACT-INF-S", "activity_class": "inference_answer", "facts_to_compare": 1}
    )


def mut_inference_many_facts(p):
    p["wall_clock_paths"][1]["activities"].append(
        {"activity_id": "ACT-INF-M", "activity_class": "inference_answer", "facts_to_compare": 6}
    )


def mut_checkbox_puzzle(p):
    p["wall_clock_paths"][1]["activities"].append(
        {
            "activity_id": "ACT-CHK",
            "activity_class": "medium_puzzle",
            "checkbox_masquerade": True,
            "puzzle_expected_minutes": 15,
        }
    )


def mut_medium_puzzle(p):
    p["wall_clock_paths"][1]["activities"].append(
        {
            "activity_id": "ACT-PUZ",
            "activity_class": "medium_puzzle",
            "puzzle_lower_minutes": 8,
            "puzzle_expected_minutes": 12,
            "puzzle_upper_minutes": 18,
        }
    )


def mut_recovery(p):
    p["wall_clock_paths"][1]["activities"].append(
        {"activity_id": "ACT-REC", "activity_class": "failed_inference_recovery", "authored_expected_minutes": 8}
    )


def mut_revisit_heavy(p):
    for i in range(5):
        p["wall_clock_paths"][1]["activities"].append(
            {"activity_id": f"ACT-REV-{i}", "activity_class": "revisit", "authored_expected_minutes": 6}
        )


def mut_scarcity_fail(p):
    p["time_scarcity"]["exhaustive_fits_before_deadline"] = True
    p["coverage_assumptions"]["exhaustive_content_minutes"] = 200


def mut_deadline_impossible(p):
    p["time_scarcity"]["fair_solution_after_deadline"] = True


def mut_time_gated_unreachable(p):
    p["time_scarcity"]["time_gated_event_unreachable"] = True


def mut_missing_metadata(p):
    p["metadata_incomplete"] = True
    del p["activity_class_defaults"]


def mut_split_imbalance(p):
    p["play_modes"] = ["two_player"]
    p["estimate_two_player"] = True
    p["two_player_model"] = two_player_model(15, 10, 45, 5)


def mut_playtest_30(p):
    p["playtest_calibration"]["observations"] = [
        {"predicted_minutes": 120, "actual_minutes": 30, "mode": "single_investigator", "player_count": 1}
    ]


def mut_playtest_70(p):
    p["playtest_calibration"]["observations"] = [
        {"predicted_minutes": 120, "actual_minutes": 70, "mode": "single_investigator", "player_count": 1}
    ]


def mut_single_playtest_change(p):
    p["playtest_calibration"]["observations"] = [
        {"predicted_minutes": 120, "actual_minutes": 90, "mode": "single_investigator"}
    ]
    p["playtest_calibration"]["attempted_default_change"] = True


def mut_multi_playtest_recommend(p):
    p["playtest_calibration"]["observations"] = [
        {"predicted_minutes": 120, "actual_minutes": 95, "mode": "single_investigator"},
        {"predicted_minutes": 120, "actual_minutes": 100, "mode": "single_investigator"},
        {"predicted_minutes": 120, "actual_minutes": 98, "mode": "single_investigator"},
    ]
    p["playtest_calibration"]["recommendation"] = "reduce reading_seconds_per_word by 5%"


def mut_ending_questionnaire(p):
    p["wall_clock_paths"][1]["activities"].append(
        {"activity_id": "ACT-EQ", "activity_class": "ending_questionnaire", "authored_expected_minutes": 10}
    )


def build(adventure_id: str, modes: list[str], target: int = 120, median: float = 118, mut=None) -> dict:
    p = base_pt(adventure_id, modes, target, median)
    if mut:
        mut(p)
    return p


FIXTURES_MAP = {
    "pt_valid_solo_120": lambda: build("pt_valid_solo_120", ["single_investigator"], 120, 118),
    "pt_solo_30_min_content": lambda: build("pt_solo_30_min_content", ["single_investigator"], 120, 30, mut_solo_30),
    "pt_two_player_parallel_summed": lambda: build("pt_two_player_parallel_summed", ["two_player"], 120, 118, mut_parallel_summed),
    "pt_valid_two_player_max_branch": lambda: build("pt_valid_two_player_max_branch", ["single_investigator", "two_player"], 120, 118, mut_valid_two_player),
    "pt_mutually_exclusive_summed": lambda: build("pt_mutually_exclusive_summed", ["single_investigator"], 120, 118, mut_mutex_summed),
    "pt_simple_as_complex": lambda: build("pt_simple_as_complex", ["single_investigator"], 120, 118, mut_simple_complex),
    "pt_rereading_overhead": lambda: build("pt_rereading_overhead", ["single_investigator"], 120, 118, mut_reread),
    "pt_callback_recent": lambda: build("pt_callback_recent", ["single_investigator"], 120, 118, mut_callback_recent),
    "pt_callback_old": lambda: build("pt_callback_old", ["single_investigator"], 120, 118, mut_callback_old),
    "pt_fake_decision_no_credit": lambda: build("pt_fake_decision_no_credit", ["single_investigator"], 120, 118, mut_fake_decision),
    "pt_meaningful_decision": lambda: build("pt_meaningful_decision", ["single_investigator"], 120, 118, mut_meaningful_decision),
    "pt_simple_inference": lambda: build("pt_simple_inference", ["single_investigator"], 120, 118, mut_simple_inference),
    "pt_inference_many_facts": lambda: build("pt_inference_many_facts", ["single_investigator"], 120, 118, mut_inference_many_facts),
    "pt_checkbox_masquerade_puzzle": lambda: build("pt_checkbox_masquerade_puzzle", ["single_investigator"], 120, 118, mut_checkbox_puzzle),
    "pt_medium_puzzle_authored": lambda: build("pt_medium_puzzle_authored", ["single_investigator"], 120, 118, mut_medium_puzzle),
    "pt_failed_inference_recovery": lambda: build("pt_failed_inference_recovery", ["single_investigator"], 120, 118, mut_recovery),
    "pt_revisit_heavy": lambda: build("pt_revisit_heavy", ["single_investigator"], 120, 118, mut_revisit_heavy),
    "pt_exhaustive_fits_scarcity": lambda: build("pt_exhaustive_fits_scarcity", ["single_investigator"], 120, 118, mut_scarcity_fail),
    "pt_deadline_impossible_fair": lambda: build("pt_deadline_impossible_fair", ["single_investigator"], 120, 118, mut_deadline_impossible),
    "pt_time_gated_unreachable": lambda: build("pt_time_gated_unreachable", ["single_investigator"], 120, 118, mut_time_gated_unreachable),
    "pt_missing_metadata_blocked": lambda: build("pt_missing_metadata_blocked", ["single_investigator"], 120, 118, mut_missing_metadata),
    "pt_valid_solo_path_report": lambda: build("pt_valid_solo_path_report", ["single_investigator"], 120, 115),
    "pt_valid_two_player_split_wait": lambda: build("pt_valid_two_player_split_wait", ["two_player"], 120, 118, mut_valid_two_player),
    "pt_severe_split_imbalance": lambda: build("pt_severe_split_imbalance", ["two_player"], 75, 118, mut_split_imbalance),
    "pt_playtest_predicted_120_measured_30": lambda: build("pt_playtest_predicted_120_measured_30", ["single_investigator"], 120, 118, mut_playtest_30),
    "pt_playtest_predicted_120_measured_70": lambda: build("pt_playtest_predicted_120_measured_70", ["single_investigator"], 120, 118, mut_playtest_70),
    "pt_one_playtest_insufficient": lambda: build("pt_one_playtest_insufficient", ["single_investigator"], 120, 118, mut_single_playtest_change),
    "pt_multiple_playtests_recommendation": lambda: build("pt_multiple_playtests_recommendation", ["single_investigator"], 120, 118, mut_multi_playtest_recommend),
    "pt_ending_questionnaire_time": lambda: build("pt_ending_questionnaire_time", ["single_investigator"], 120, 118, mut_ending_questionnaire),
    "pt_perfect_ending_path": lambda: build("pt_perfect_ending_path", ["single_investigator"], 120, 120),
}


if __name__ == "__main__":
    for name, builder in FIXTURES_MAP.items():
        write_fixture(name, builder())
    print("done", len(FIXTURES_MAP))
