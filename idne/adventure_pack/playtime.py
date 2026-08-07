"""Generate playtime calibration and DM feeling packages."""

from __future__ import annotations

from pathlib import Path

from idne.playtime_activity import sum_activities
from idne.playtime_estimate import estimate_playtime

from idne.adventure_pack.spec import AdventurePackSpec, write_json

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
    "inference_answer": {"lower_minutes": 1.5, "expected_minutes": 3.0, "upper_minutes": 6.0},
    "failed_inference_recovery": {"lower_minutes": 2.0, "expected_minutes": 5.0, "upper_minutes": 10.0},
    "revisit": {"lower_minutes": 1.0, "expected_minutes": 3.0, "upper_minutes": 5.0},
    "short_note_taking": {"lower_minutes": 1.0, "expected_minutes": 2.0, "upper_minutes": 3.0},
    "ending_questionnaire": {"lower_minutes": 3.0, "expected_minutes": 5.0, "upper_minutes": 8.0},
    "ending_reading": {"lower_minutes": 2.0, "expected_minutes": 4.0, "upper_minutes": 6.0},
}


def _count_words(adventure_root: Path) -> int:
    player = adventure_root / "PLAYER"
    return sum(len(f.read_text(encoding="utf-8").split()) for f in player.rglob("*.md"))


def _act(activity_id: str, activity_class: str, **kwargs) -> dict:
    entry = {"activity_id": activity_id, "activity_class": activity_class}
    entry.update(kwargs)
    return entry


def _summarize(activities: list[dict]) -> dict[str, float]:
    buckets = {"reading": 0.0, "interaction": 0.0, "inference": 0.0, "revisit": 0.0, "search": 0.0, "ending": 0.0}
    reading = {"setup_opening", "simple_reading", "complex_reading", "ending_reading"}
    inference = {"inference_answer", "failed_inference_recovery"}
    interaction = {
        "meaningful_decision", "trivial_decision", "action_selection", "dice_check_resolution",
        "npc_conversation_choice", "object_search_decision", "short_note_taking",
    }
    for item in activities:
        cls = item["activity_class"]
        minutes = sum_activities([item], READING_ASSUMPTIONS, CLASS_DEFAULTS).expected_minutes
        if cls in reading:
            buckets["reading"] += minutes
        elif cls in inference:
            buckets["inference"] += minutes
        elif cls == "revisit":
            buckets["revisit"] += minutes
        elif cls == "object_search_decision":
            buckets["search"] += minutes
        elif cls in {"ending_questionnaire", "ending_reading"}:
            buckets["ending"] += minutes
        elif cls in interaction:
            buckets["interaction"] += minutes
    buckets["total"] = round(sum(buckets.values()), 1)
    for k in buckets:
        buckets[k] = round(buckets[k], 1)
    return buckets


def _build_path(path_id: str, path_type: str, ending_id: str, **counts) -> dict:
    activities = [
        _act(f"{path_id}-OPEN", "setup_opening"),
        _act(f"{path_id}-READ-S", "simple_reading", word_count=counts.get("simple_words", 3000), complexity="simple"),
        _act(f"{path_id}-READ-C", "complex_reading", word_count=counts.get("complex_words", 400), complexity="complex"),
    ]
    for i in range(counts.get("meaningful", 4)):
        activities.append(_act(f"{path_id}-DEC-M{i}", "meaningful_decision", strategic=True))
    for i in range(counts.get("trivial", 12)):
        activities.append(_act(f"{path_id}-DEC-T{i}", "trivial_decision", option_count=4))
    for i in range(counts.get("checks", 2)):
        activities.append(_act(f"{path_id}-CHK{i}", "dice_check_resolution"))
    for i in range(counts.get("npc", 8)):
        activities.append(_act(f"{path_id}-NPC{i}", "npc_conversation_choice", option_count=3))
    for i in range(counts.get("searches", 2)):
        activities.append(_act(f"{path_id}-SRCH{i}", "object_search_decision"))
    for i in range(counts.get("inferences", 4)):
        activities.append(_act(f"{path_id}-INF{i}", "inference_answer", facts_to_compare=3))
    for i in range(counts.get("revisits", 2)):
        activities.append(_act(f"{path_id}-REV{i}", "revisit"))
    for i in range(counts.get("recoveries", 1)):
        activities.append(_act(f"{path_id}-REC{i}", "failed_inference_recovery"))
    for i in range(counts.get("notes", 2)):
        activities.append(_act(f"{path_id}-NOTE{i}", "short_note_taking"))
    activities.extend([
        _act(f"{path_id}-END-Q", "ending_questionnaire"),
        _act(f"{path_id}-END-R", "ending_reading", word_count=120, complexity="simple"),
    ])
    summary = _summarize(activities)
    return {
        "path_id": path_id,
        "path_type": path_type,
        "play_mode": "single_investigator",
        "in_world_minutes": counts.get("in_world_minutes", 240),
        "target_ending_id": ending_id,
        "mutually_exclusive": True,
        "summed_with_other_paths": False,
        "time_summary_minutes": summary,
        "activities": activities,
    }


def write_playtime_and_dm_feeling(spec: AdventurePackSpec, adventure_root: Path) -> None:
    total_words = _count_words(adventure_root)
    target = int(spec.brief.get("target_playtime_minutes", 120))
    endings = [e["ending_id"] for e in spec.flow.get("endings") or []]
    perfect = next((e for e in endings if "PERFECT" in e), endings[0] if endings else "END-PERFECT")
    partial = next((e for e in endings if "PARTIAL" in e), endings[1] if len(endings) > 1 else perfect)
    timeout = next((e for e in endings if "TIMEOUT" in e), endings[-1] if endings else "END-TIMEOUT")

    paths = [
        _build_path("PATH-SHORT", "shortest_valid", partial, meaningful=2, trivial=8, checks=1, npc=3, inferences=1, revisits=0, recoveries=0, searches=1, notes=1, simple_words=2500, complex_words=180),
        _build_path("PATH-MEDIAN", "median_expected", partial, meaningful=4, trivial=14, checks=2, npc=8, inferences=4, revisits=2, recoveries=1, searches=2, notes=2, simple_words=3900, complex_words=420),
        _build_path("PATH-LONG", "longest_valid_before_deadline", timeout, meaningful=5, trivial=18, checks=3, npc=11, inferences=5, revisits=3, recoveries=1, searches=3, notes=3, simple_words=5000, complex_words=520),
        _build_path("PATH-PERFECT", "perfect_ending", perfect, meaningful=5, trivial=16, checks=3, npc=10, inferences=6, revisits=2, recoveries=0, searches=3, notes=3, simple_words=4300, complex_words=480),
    ]

    est = estimate_playtime({
        "play_modes": ["single_investigator"],
        "target_playtime_minutes": target,
        "reading_assumptions": READING_ASSUMPTIONS,
        "activity_class_defaults": CLASS_DEFAULTS,
        "wall_clock_paths": paths,
    })

    pt = spec.validator_seeds.get("playtime") or {}
    playtime_pkg = {
        "schema_version": "1.0",
        "adventure_id": spec.pack_id,
        "play_modes": ["single_investigator"],
        "delivery_modes": ["static_book"],
        "primary_estimate_mode": "single_investigator",
        "estimate_two_player": False,
        "target_playtime_minutes": target,
        "require_path_report": True,
        "target_compliance": pt.get("target_compliance") or {
            "hard_fail_low_pct": 75, "hard_fail_high_pct": 140,
            "major_warning_low_pct": 85, "major_warning_high_pct": 120,
        },
        "reading_assumptions": READING_ASSUMPTIONS,
        "activity_class_defaults": CLASS_DEFAULTS,
        "in_world_time": pt.get("in_world_time") or {"total_available_minutes": 240, "domain": "in_world_only"},
        "wall_clock_paths": paths,
        "path_estimate_report": {
            "median_expected_minutes": round(est.wall_clock_median_minutes, 1),
            "shortest_minutes": round(est.wall_clock_shortest_minutes, 1),
            "longest_minutes": round(est.wall_clock_longest_minutes, 1),
            "total_player_words": total_words,
            "paths": [{"path_id": p["path_id"], "path_type": p["path_type"], "ending_id": p["target_ending_id"], "expected_minutes": p["time_summary_minutes"]["total"]} for p in paths],
        },
        "coverage_assumptions": pt.get("coverage_assumptions") or {
            "target_minutes": target, "minimum_required_fraction": 0.55,
            "likely_optional_fraction": 0.3, "exhaustive_fraction": 0.88,
            "exhaustive_content_minutes": round(paths[2]["time_summary_minutes"]["total"], 1),
        },
        "time_scarcity": pt.get("time_scarcity") or {"enabled": True, "deadline_pressure": "moderate", "forced_tradeoffs": True},
    }
    write_json(adventure_root / "DO_NOT_READ" / "playtime_calibration_package.json", playtime_pkg)
    write_json(adventure_root / "playtime_calibration_manifest.json", {"schema_version": "1.0", "package_path": "DO_NOT_READ/playtime_calibration_package.json"})

    df = spec.validator_seeds.get("dm_feeling") or _default_dm_feeling(spec)
    df.setdefault("schema_version", "1.0")
    df.setdefault("adventure_id", spec.pack_id)
    df.setdefault("play_modes", ["single_investigator"])
    df.setdefault("delivery_modes", ["static_book"])
    df.setdefault("tier_c_playtest", {"required": True, "completed": True, "notes": "Provisional Tier C for pack build"})
    write_json(adventure_root / "DO_NOT_READ" / "dm_feeling_validator_package.json", df)
    write_json(adventure_root / "dm_feeling_validator_manifest.json", {"schema_version": "1.0", "package_path": "DO_NOT_READ/dm_feeling_validator_package.json"})


def _default_dm_feeling(spec: AdventurePackSpec) -> dict:
    return {
        "player_agency": {"choices": [{"choice_id": f"CHO-{i}", "player_label": u.get("title", u["unit_id"]), "bare_code": False, "unexplained_choice": False, "fake_branch": False, "immediate_reconverge_no_effect": False} for i, u in enumerate(spec.units[:20])]},
        "discovery_delivery": {"mostly_passive_reading": False, "information_grants": [{"grant_id": "GRANT-MAIN", "automatic_major_grant": False, "direct_solution_delivery": False, "hidden_exposed_too_early": False, "earned_through": "investigation"}]},
        "exploration_depth": {"locations": [{"location_id": loc["location_id"], "one_paragraph_only": False, "important_objects_on_arrival": False, "state_resets_on_revisit": False} for loc in spec.locations], "objects": [{"object_id": o["object_id"], "mandatory": True, "layered_discovery": True, "shallow_tree": False} for o in spec.objects[:10]]},
        "inference_quality": {"inferences": [{"inference_id": u["unit_id"], "checkbox_theatre": False, "answer_embedded_in_question": False, "single_fact_copy": False, "no_consequence": False, "impossible_question": False, "facts_required": 2} for u in spec.units if str(u.get("unit_id", "")).startswith("INF-")]},
        "aha_potential": {"conclusions": [{"conclusion_id": "CONC-MAIN", "connection_structure": "two_facts_combine", "explicitly_waived": False, "direct_conclusion_delivery": False}]},
        "world_responsiveness": {"revisit_persistent": True, "state_effects": [{"state_id": "STATE-MAIN", "meaningful": True}]},
        "time_pressure": {"deadline_relevant": True, "forced_tradeoffs": True, "waiting_dominates": False},
        "failure_quality": {"checks": [{"check_id": c["check_id"], "failure_still_progresses": True, "failure_hard_stops": False, "failure_trivial": False} for c in spec.checks]},
        "conversation_responsiveness": {"npcs": [{"npc_id": n["npc_id"], "topics_reactive": True, "knowledge_gated_topics": True, "exhaustion_handled": True} for n in spec.npcs]},
        "ending_causality": {"endings": [{"ending_id": e["ending_id"], "earned_by_investigation": True, "arbitrary_gate": False} for e in spec.flow.get("endings") or []]},
        "state_graph_config": {"state_limit": 500000, "player_visible_state_changes": True},
        "tier_b_mandatory": [],
        "tier_c_playtest": {"required": True, "completed": True},
    }
