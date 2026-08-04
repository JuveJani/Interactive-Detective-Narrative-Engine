"""Generate DM Feeling validator fixtures (Milestone 10)."""

import json
from pathlib import Path

FIXTURES = Path(__file__).resolve().parents[1] / "tests" / "fixtures"

PLAYER_GOOD = "Search the desk in the manager's office.\nQuestion the caretaker about the theft.\n"
PLAYER_BARE = "Go to J-223.\nContinue to page 345.\n"


def base_df(adventure_id: str, play_modes: list[str]) -> dict:
    two = "two_player" in play_modes
    return {
        "schema_version": "1.0",
        "adventure_id": adventure_id,
        "play_modes": play_modes,
        "delivery_modes": ["static_book", "ai_dm"],
        "player_agency": {
            "choices": [
                {
                    "choice_id": "CHO-SEARCH",
                    "player_label": "Search the desk.",
                    "bare_code": False,
                    "unexplained_choice": False,
                    "fake_branch": False,
                    "immediate_reconverge_no_effect": False,
                }
            ]
        },
        "discovery_delivery": {
            "mostly_passive_reading": False,
            "information_grants": [
                {
                    "grant_id": "GRANT-KEY",
                    "automatic_major_grant": False,
                    "direct_solution_delivery": False,
                    "hidden_exposed_too_early": False,
                    "earned_through": "object_search",
                }
            ],
        },
        "exploration_depth": {
            "locations": [
                {
                    "location_id": "LOC-OFFICE",
                    "one_paragraph_only": False,
                    "important_objects_on_arrival": False,
                    "state_resets_on_revisit": False,
                }
            ],
            "objects": [
                {
                    "object_id": "OBJ-DESK",
                    "mandatory": True,
                    "layered_discovery": True,
                    "shallow_tree": False,
                }
            ],
        },
        "inference_quality": {
            "inferences": [
                {
                    "inference_id": "INF-001",
                    "checkbox_theatre": False,
                    "answer_embedded_in_question": False,
                    "single_fact_copy": False,
                    "no_consequence": False,
                    "impossible_question": False,
                    "facts_required": 2,
                }
            ],
        },
        "aha_potential": {
            "conclusions": [
                {
                    "conclusion_id": "CONC-001",
                    "connection_structure": "two_facts_combine",
                    "explicitly_waived": False,
                    "direct_conclusion_delivery": False,
                }
            ],
        },
        "world_responsiveness": {
            "revisit_persistent": True,
            "state_effects": [
                {
                    "state_id": "STATE-DESK-SEARCHED",
                    "affects_player_content": True,
                    "declared_but_inert": False,
                    "time_threshold_inert": False,
                }
            ],
        },
        "time_pressure": {
            "deadline_irrelevant": False,
            "exhaustive_always_fits": False,
            "time_gated_unreachable": False,
        },
        "failure_quality": {
            "failures": [
                {
                    "failure_id": "FAIL-PERCEPTION",
                    "meaningless_failure": False,
                    "no_persistent_effect": False,
                    "unfair_dead_end": False,
                    "changes_fixed_truth": False,
                    "leaks_success_content": False,
                    "free_retry": False,
                    "meaningful_effect": True,
                }
            ],
        },
        "conversation_agency": {
            "npc_routes": [
                {
                    "npc_id": "NPC-B",
                    "mandatory_route": True,
                    "responds_to_relationship": True,
                    "exposition_menu_only": False,
                    "trust_declared_unused": False,
                    "identical_outcomes": False,
                    "dispenser_only": False,
                }
            ],
        },
        "ending_causality": {
            "endings": [
                {
                    "ending_id": "END-PERFECT",
                    "causal_trace": True,
                    "final_choice_only": False,
                    "unreachable": False,
                    "decorative": False,
                    "truth_leak": False,
                    "auto_perfect_unlock": False,
                },
                {
                    "ending_id": "END-PARTIAL",
                    "causal_trace": True,
                    "final_choice_only": False,
                    "truth_leak": False,
                    "decorative": False,
                },
            ],
        },
        "mode_specific": {
            "single_investigator": {
                "partner_dependency": False,
                "artificial_split_remnants": False,
            },
            "two_player": {
                "little_joint_investigation": False,
                "high_idle_time": False,
                "joint_reasoning_required": True if two else False,
            },
        },
        "player_audit": {"files": ["PLAYER/INVESTIGATION.md"]},
        "state_graph_config": {"max_states": 5000, "explored_states": 10, "forced_explosion": False},
        "tier_b_mandatory": [],
        "tier_c_playtest": {"required": True, "completed": True},
        "local_ai_export": {"required": True, "ready": True, "offline_runnable": True, "write_reports": False},
    }


def write_fixture(name: str, pkg: dict, player: str = PLAYER_GOOD):
    dest = FIXTURES / name
    if dest.exists():
        import shutil

        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    (dest / "DO_NOT_READ").mkdir(parents=True, exist_ok=True)
    (dest / "DO_NOT_READ" / "dm_feeling_validator_package.json").write_text(json.dumps(pkg, indent=2) + "\n")
    (dest / "dm_feeling_validator_manifest.json").write_text(
        json.dumps(
            {
                "schema_version": "1.0",
                "dm_feeling_validator_method": "canonical",
                "package_path": "DO_NOT_READ/dm_feeling_validator_package.json",
            },
            indent=2,
        )
        + "\n"
    )
    player_dir = dest / "PLAYER"
    player_dir.mkdir(parents=True, exist_ok=True)
    (player_dir / "INVESTIGATION.md").write_text(player + "\n")


def build(adventure_id: str, modes: list[str], mut=None) -> dict:
    p = base_df(adventure_id, modes)
    if mut:
        mut(p)
    return p


def mut_bare_code(p):
    p["player_agency"]["choices"][0].update({"bare_code": True, "player_label": "Go to J-223."})


def mut_unexplained(p):
    p["player_agency"]["choices"].append(
        {"choice_id": "CHO-RAND", "unexplained_choice": True, "player_label": "Pick option R-212b."}
    )


def mut_fake_branch(p):
    p["player_agency"]["choices"][0]["fake_branch"] = True


def mut_passive(p):
    p["discovery_delivery"]["mostly_passive_reading"] = True


def mut_auto_grant(p):
    p["discovery_delivery"]["information_grants"][0]["automatic_major_grant"] = True


def mut_hidden_early(p):
    p["discovery_delivery"]["information_grants"][0]["hidden_exposed_too_early"] = True


def mut_layered_object(p):
    p["exploration_depth"]["objects"][0]["layered_discovery"] = True
    p["exploration_depth"]["objects"][0]["interaction_layers"] = 3


def mut_check_leak(p):
    p["failure_quality"]["failures"][0]["leaks_success_content"] = True


def mut_multi_fact(p):
    p["inference_quality"]["inferences"][0]["facts_required"] = 3


def mut_inference_theatre(p):
    p["inference_quality"]["inferences"][0]["checkbox_theatre"] = True


def mut_answer_in_q(p):
    p["inference_quality"]["inferences"][0]["answer_embedded_in_question"] = True


def mut_aha(p):
    p["aha_potential"]["conclusions"][0]["connection_structure"] = "delayed_significance"


def mut_direct_conclusion(p):
    p["aha_potential"]["conclusions"][0]["direct_conclusion_delivery"] = True


def mut_persistent_revisit(p):
    p["world_responsiveness"]["revisit_persistent"] = True


def mut_reset_loc(p):
    p["exploration_depth"]["locations"][0]["state_resets_on_revisit"] = True


def mut_inert_time(p):
    p["world_responsiveness"]["state_effects"][0]["time_threshold_inert"] = True


def mut_irrelevant_deadline(p):
    p["time_pressure"]["deadline_irrelevant"] = True


def mut_meaningful_fail(p):
    p["failure_quality"]["failures"][0]["meaningful_effect"] = True


def mut_fail_no_effect(p):
    p["failure_quality"]["failures"][0]["no_persistent_effect"] = True


def mut_responsive_npc(p):
    p["conversation_agency"]["npc_routes"][0]["responds_to_relationship"] = True


def mut_exposition_menu(p):
    p["conversation_agency"]["npc_routes"][0]["exposition_menu_only"] = True


def mut_trust_unused(p):
    p["conversation_agency"]["npc_routes"][0]["trust_declared_unused"] = True


def mut_final_only(p):
    p["ending_causality"]["endings"][0]["final_choice_only"] = True
    p["ending_causality"]["endings"][0]["causal_trace"] = False


def mut_causal_ending(p):
    p["ending_causality"]["endings"][0]["causal_trace"] = True


def mut_ending_leak(p):
    p["ending_causality"]["endings"][1]["truth_leak"] = True


def mut_solo_clean(p):
    p["mode_specific"]["single_investigator"]["partner_dependency"] = False


def mut_little_joint(p):
    p["mode_specific"]["two_player"]["little_joint_investigation"] = True


def mut_state_blocked(p):
    p["state_graph_config"]["forced_explosion"] = True


def mut_missing_tier_b(p):
    p["tier_b_mandatory"] = [{"review_id": "DF-B-AGENCY", "category": "player_agency", "expected": "agency review", "resolved": False}]
    p["tier_c_playtest"]["completed"] = True


def mut_missing_playtest(p):
    p["tier_c_playtest"] = {"required": True, "completed": False}


def mut_offline_export(p):
    p["local_ai_export"] = {"required": True, "ready": True, "offline_runnable": True, "write_reports": False}


FIXTURES_MAP = {
    "df_valid_solo_agency": ("single_investigator", None, PLAYER_GOOD),
    "df_valid_two_player": (["single_investigator", "two_player"], None, PLAYER_GOOD),
    "df_bare_code_choice": ("single_investigator", mut_bare_code, PLAYER_BARE),
    "df_unexplained_choice": ("single_investigator", mut_unexplained, PLAYER_GOOD),
    "df_fake_branch": ("single_investigator", mut_fake_branch, PLAYER_GOOD),
    "df_passive_reading": ("single_investigator", mut_passive, PLAYER_GOOD),
    "df_auto_major_grant": ("single_investigator", mut_auto_grant, PLAYER_GOOD),
    "df_valid_layered_object": ("single_investigator", mut_layered_object, PLAYER_GOOD),
    "df_hidden_exposed_early": ("single_investigator", mut_hidden_early, PLAYER_GOOD),
    "df_check_leak_failure": ("single_investigator", mut_check_leak, PLAYER_GOOD),
    "df_valid_multi_fact_inference": ("single_investigator", mut_multi_fact, PLAYER_GOOD),
    "df_inference_theatre": ("single_investigator", mut_inference_theatre, PLAYER_GOOD),
    "df_answer_in_question": ("single_investigator", mut_answer_in_q, PLAYER_GOOD),
    "df_valid_aha_structure": ("single_investigator", mut_aha, PLAYER_GOOD),
    "df_direct_conclusion_delivery": ("single_investigator", mut_direct_conclusion, PLAYER_GOOD),
    "df_persistent_revisit": ("single_investigator", mut_persistent_revisit, PLAYER_GOOD),
    "df_reset_location": ("single_investigator", mut_reset_loc, PLAYER_GOOD),
    "df_inert_time_threshold": ("single_investigator", mut_inert_time, PLAYER_GOOD),
    "df_irrelevant_deadline": ("single_investigator", mut_irrelevant_deadline, PLAYER_GOOD),
    "df_meaningful_failure": ("single_investigator", mut_meaningful_fail, PLAYER_GOOD),
    "df_failure_no_effect": ("single_investigator", mut_fail_no_effect, PLAYER_GOOD),
    "df_responsive_npc": ("single_investigator", mut_responsive_npc, PLAYER_GOOD),
    "df_exposition_npc_menu": ("single_investigator", mut_exposition_menu, PLAYER_GOOD),
    "df_trust_unused": ("single_investigator", mut_trust_unused, PLAYER_GOOD),
    "df_final_choice_only_ending": ("single_investigator", mut_final_only, PLAYER_GOOD),
    "df_valid_causal_ending": ("single_investigator", mut_causal_ending, PLAYER_GOOD),
    "df_imperfect_ending_leak": ("single_investigator", mut_ending_leak, PLAYER_GOOD),
    "df_absent_partner_dependency": ("single_investigator", mut_solo_clean, PLAYER_GOOD),
    "df_two_player_little_joint": (["two_player"], mut_little_joint, PLAYER_GOOD),
    "df_state_limit_blocked": ("single_investigator", mut_state_blocked, PLAYER_GOOD),
    "df_missing_tier_b": ("single_investigator", mut_missing_tier_b, PLAYER_GOOD),
    "df_missing_playtest": ("single_investigator", mut_missing_playtest, PLAYER_GOOD),
    "df_valid_offline_ai_export": ("single_investigator", mut_offline_export, PLAYER_GOOD),
}


if __name__ == "__main__":
    for name, (modes, mut, player) in FIXTURES_MAP.items():
        m = modes if isinstance(modes, list) else [modes]
        write_fixture(name, build(name, m, mut), player)
    print("done", len(FIXTURES_MAP))
