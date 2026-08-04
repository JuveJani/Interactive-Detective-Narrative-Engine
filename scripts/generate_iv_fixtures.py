"""Generate investigation validator test fixtures (Milestone 7)."""

import copy
import json
import shutil
from pathlib import Path

FIXTURES = Path(__file__).resolve().parents[1] / "tests" / "fixtures"
SRC_IFLOW = FIXTURES / "iflow_valid_minimal"
SRC_CAP = FIXTURES / "cap_valid_perception_key"
SRC_NPC = FIXTURES / "npc_valid_minimal"


def base_iv(adventure_id: str, play_modes: list[str]) -> dict:
    two_valid = "two_player" in play_modes
    return {
        "schema_version": "1.0",
        "adventure_id": adventure_id,
        "play_modes": play_modes,
        "layer_links": {
            "investigation_core": "DO_NOT_READ/investigation_core_package.json",
            "investigation_flow": "DO_NOT_READ/investigation_flow_package.json",
            "environment": "DO_NOT_READ/environment_package.json",
            "object_interaction": "DO_NOT_READ/object_interaction_package.json",
            "capability_check": "DO_NOT_READ/capability_check_package.json",
            "npc_investigation": "DO_NOT_READ/npc_investigation_package.json",
        },
        "conclusion_traces": [
            {
                "conclusion_id": "CONC-CULPRIT",
                "proof_id": "PROOF-A",
                "chain": [
                    {"layer": "fixed_truth", "ref": "WF-KEY"},
                    {"layer": "location", "ref": "LOC-OFFICE"},
                    {"layer": "object", "ref": "OBJ-DESK"},
                    {"layer": "player_action", "ref": "ACT-SEARCH-DESK"},
                    {"layer": "capability_check", "ref": "CHK-PERCEPTION-DESK"},
                    {"layer": "observation", "ref": "OBS-KEY"},
                    {"layer": "knowledge", "ref": "KNOW-KEY"},
                    {"layer": "knowledge", "ref": "KNOW-SECRET"},
                    {"layer": "conclusion", "ref": "CONC-CULPRIT"},
                    {"layer": "proof", "ref": "PROOF-A"},
                    {"layer": "ending", "ref": "END-PERFECT"},
                ],
            }
        ],
        "inference_questions": [
            {
                "question_id": "INF-001",
                "hypothesis_id": "HYP-001",
                "player_facing_text": "Where was the key hidden?",
                "defined_terms": ["key", "hidden"],
                "undefined_terms": [],
                "required_knowledge_ids": ["KNOW-KEY"],
                "available_before_question": True,
                "accepted_hypothesis_id": "HYP-001",
                "equally_supported_alternatives": [],
                "question_reveals_answer": False,
                "requires_internal_ids": False,
            }
        ],
        "information_sufficiency": [
            {
                "inference_id": "INF-001",
                "required_knowledge_ids": ["KNOW-KEY"],
                "minimum_independent_sources": 1,
                "sources": [
                    {"knowledge_id": "KNOW-KEY", "accessible": True, "before_inference": True, "independent": True},
                    {"knowledge_id": "KNOW-SECRET", "accessible": True, "before_inference": True, "independent": True},
                ],
            }
        ],
        "recovery_routes": [
            {
                "route_id": "REC-OFFICE",
                "trigger": "inference_incomplete",
                "inference_id": "INF-001",
                "player_action_label": "Return to the manager's office.",
                "destination_ref": "LOC-OFFICE",
                "destination_legal": True,
                "changes_knowledge_or_access": True,
                "changes_state": True,
                "zero_cost_loop": False,
                "vague_instruction": False,
                "bare_page_code": False,
            }
        ],
        "access_requirements": [
            {
                "requirement_id": "ACC-KEY",
                "type": "key",
                "object_id": "OBJ-KEY-HIDDEN",
                "discovery_route_exists": True,
                "requires_own_key": False,
                "mandatory": True,
                "fair_paths": ["ROUTE-PERCEPTION", "ROUTE-WITNESS"],
            },
            {
                "requirement_id": "ACC-PASSWORD",
                "type": "password",
                "mandatory": False,
                "derivation_route_exists": True,
            },
        ],
        "mandatory_check_fairness": [
            {
                "check_id": "CHK-PERCEPTION-DESK",
                "mandatory_path": True,
                "failure_destroys_all_routes": False,
                "alternate_route_on_failure": "ROUTE-WITNESS",
                "uses_capability_validator": True,
            }
        ],
        "npc_disclosure_routes": [
            {
                "route_id": "NPC-B-SECRET",
                "npc_id": "NPC-B",
                "knowledge_id": "KNOW-SECRET",
                "npc_holds_information": True,
                "disclosure_route_exists": True,
                "trust_achievable": True,
                "topic_unlock_achievable": True,
                "available_before_deadline": True,
                "impossible_social_check": False,
            }
        ],
        "time_validation": {
            "deadline_clock": "T_DEADLINE",
            "mandatory_paths_fit_deadline": True,
            "revisit_uses_current_variant": True,
            "zero_cost_investigation_loop": False,
            "mutually_impossible_clocks": False,
        },
        "ending_reachability": [
            {"ending_id": "END-PERFECT", "reachable": True, "decorative": False, "ending_type": "perfect", "reveals_full_truth": True},
            {"ending_id": "END-TIMEOUT", "reachable": True, "decorative": False, "deadline_trigger": True, "ending_type": "deadline"},
        ],
        "accusation_fairness": {"options_neutral": True, "reveal_correct_answer": False, "requires_unknown_info": False},
        "play_mode_constraints": {
            "single_investigator_valid": True,
            "two_player_valid": two_valid,
            "solo_requires_player_2": False,
            "two_player_private_unshared": False,
        },
        "player_audit": {
            "files": ["PLAYER/INVESTIGATION.md"],
            "canonical_actions": [{"action_label": "Search the desk.", "canonical_ref": "ACT-SEARCH-DESK", "present_in_player": True}],
            "information_entries": [{"info_id": "INFO-KEY-LOC", "canonical_source": "OBS-001", "orphan_in_player": False}],
            "check_units": [{"unit_id": "UNIT-CHK-DECL", "exposes_pass_fail_together": False}],
            "destination_refs": [{"destination_id": "UNIT-KEY-SUCCESS", "exists": True}],
            "location_reset_on_return": False,
            "ending_contradicts_truth": False,
        },
        "state_graph_config": {"max_states": 5000, "max_depth": 40, "forced_explosion": False},
        "tier_b_mandatory": [],
    }


def copy_layers(dest: Path):
    dnr = dest / "DO_NOT_READ"
    dnr.mkdir(parents=True, exist_ok=True)
    for name in (
        "investigation_core_package.json",
        "object_interaction_package.json",
        "capability_check_package.json",
    ):
        shutil.copy(SRC_CAP / "DO_NOT_READ" / name, dnr / name)
    for name in ("investigation_flow_package.json", "environment_package.json"):
        shutil.copy(SRC_IFLOW / "DO_NOT_READ" / name, dnr / name)
    shutil.copy(SRC_NPC / "DO_NOT_READ" / "npc_investigation_package.json", dnr / "npc_investigation_package.json")
    # Align npc package investigation core link knowledge with cap core
    inv = json.loads((dnr / "investigation_core_package.json").read_text())
    inv["adventure_id"] = dest.name
    (dnr / "investigation_core_package.json").write_text(json.dumps(inv, indent=2) + "\n")
    for m in (
        "investigation_flow_manifest.json",
        "environment_manifest.json",
        "object_interaction_manifest.json",
        "capability_check_manifest.json",
        "npc_investigation_manifest.json",
    ):
        src = SRC_IFLOW / m
        if not src.exists():
            src = SRC_CAP / m
        if not src.exists():
            src = SRC_NPC / m
        if src.exists():
            shutil.copy(src, dest / m)
    # investigation core manifest for delegate validators
    inv_manifest = {
        "schema_version": "1.0",
        "investigation_method": "canonical",
        "package_path": "DO_NOT_READ/investigation_core_package.json",
    }
    (dest / "investigation_manifest.json").write_text(json.dumps(inv_manifest, indent=2) + "\n")


def write_player(dest: Path, content: str = "Search the desk.\nReturn to the manager's office.\n"):
    p = dest / "PLAYER" / "INVESTIGATION.md"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content)


def write_fixture(name: str, mutate=None, play_modes=None):
    dest = FIXTURES / name
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    modes = play_modes or ["single_investigator"]
    pkg = base_iv(name, modes)
    if mutate:
        mutate(pkg)
    copy_layers(dest)
    write_player(dest)
    (dest / "investigation_validator_manifest.json").write_text(
        json.dumps(
            {
                "schema_version": "1.0",
                "investigation_validator_method": "canonical",
                "package_path": "DO_NOT_READ/investigation_validator_package.json",
            },
            indent=2,
        ) + "\n"
    )
    (dest / "DO_NOT_READ" / "investigation_validator_package.json").write_text(json.dumps(pkg, indent=2) + "\n")


def mut_inference_missing(p):
    p["inference_questions"][0]["required_knowledge_ids"].append("KNOW-MISSING")


def mut_info_after(p):
    p["inference_questions"][0]["available_before_question"] = False


def mut_undefined_term(p):
    p["inference_questions"][0]["undefined_terms"] = ["cryptic_term"]


def mut_equally_supported(p):
    p["inference_questions"][0]["equally_supported_alternatives"] = ["ALT-1", "ALT-2"]


def mut_vague_recovery(p):
    p["recovery_routes"][0].update({"vague_instruction": True, "player_action_label": "Investigate again."})


def mut_recovery_bare(p):
    p["recovery_routes"][0].update({"bare_page_code": True, "player_action_label": "Go to J-223."})


def mut_zero_loop(p):
    p["recovery_routes"][0]["zero_cost_loop"] = True


def mut_key_own_lock(p):
    next(a for a in p["access_requirements"] if a["requirement_id"] == "ACC-KEY")["requires_own_key"] = True


def mut_password_no_route(p):
    p["access_requirements"].append({"requirement_id": "ACC-PWD2", "type": "password", "mandatory": True, "derivation_route_exists": False})


def mut_item_consumed(p):
    next(a for a in p["access_requirements"] if a["requirement_id"] == "ACC-KEY")["consumed_before_use"] = True


def mut_check_destroys(p):
    p["mandatory_check_fairness"][0].update({"failure_destroys_all_routes": True, "alternate_route_on_failure": None})


def mut_npc_unreachable(p):
    p["npc_disclosure_routes"][0]["disclosure_route_exists"] = False


def mut_undefined_trust(p):
    p["npc_disclosure_routes"][0]["undefined_trust_condition"] = True


def mut_npc_leaves(p):
    p["npc_disclosure_routes"][0]["npc_leaves_before_mandatory"] = True


def mut_time_variant(p):
    p["time_validation"]["revisit_uses_current_variant"] = False


def mut_deadline_exceeded(p):
    p["time_validation"]["mandatory_paths_fit_deadline"] = False


def mut_unreachable_ending(p):
    p["ending_reachability"][0]["reachable"] = False


def mut_decorative_impossible(p):
    p["ending_reachability"].append({"ending_id": "END-DECOR", "decorative": True, "impossible_trigger": True, "reachable": False})


def mut_ending_leak(p):
    p["ending_reachability"].append({"ending_id": "END-PARTIAL", "ending_type": "partial", "reveals_full_truth": True, "reachable": True})


def mut_accusation_reveals(p):
    p["accusation_fairness"]["reveal_correct_answer"] = True


def mut_player_no_source(p):
    p["player_audit"]["information_entries"][0]["orphan_in_player"] = True


def mut_player_missing_action(p):
    p["player_audit"]["canonical_actions"][0]["present_in_player"] = False


def mut_destination_missing(p):
    p["player_audit"]["destination_refs"][0]["exists"] = False


def mut_location_reset(p):
    p["player_audit"]["location_reset_on_return"] = True


def mut_solo_p2(p):
    p["play_mode_constraints"]["solo_requires_player_2"] = True


def mut_two_player_private(p):
    p["play_mode_constraints"]["two_player_private_unshared"] = True


def mut_state_explosion(p):
    p["state_graph_config"]["forced_explosion"] = True


MUTATIONS = {
    "iv_complete_solo": None,
    "iv_complete_two_player": None,
    "iv_inference_missing_info": mut_inference_missing,
    "iv_info_after_inference": mut_info_after,
    "iv_undefined_term": mut_undefined_term,
    "iv_equally_supported": mut_equally_supported,
    "iv_vague_recovery": mut_vague_recovery,
    "iv_recovery_bare_code": mut_recovery_bare,
    "iv_zero_cost_loop": mut_zero_loop,
    "iv_key_behind_own_lock": mut_key_own_lock,
    "iv_password_no_route": mut_password_no_route,
    "iv_item_consumed_early": mut_item_consumed,
    "iv_check_destroys_routes": mut_check_destroys,
    "iv_npc_disclosure_unreachable": mut_npc_unreachable,
    "iv_undefined_trust": mut_undefined_trust,
    "iv_npc_leaves_early": mut_npc_leaves,
    "iv_time_variant_not_used": mut_time_variant,
    "iv_deadline_exceeded": mut_deadline_exceeded,
    "iv_unreachable_ending": mut_unreachable_ending,
    "iv_decorative_impossible_ending": mut_decorative_impossible,
    "iv_ending_truth_leak": mut_ending_leak,
    "iv_accusation_reveals_answer": mut_accusation_reveals,
    "iv_player_no_source": mut_player_no_source,
    "iv_player_missing_action": mut_player_missing_action,
    "iv_pass_fail_leak": None,
    "iv_destination_missing": mut_destination_missing,
    "iv_location_reset": mut_location_reset,
    "iv_solo_requires_p2": mut_solo_p2,
    "iv_two_player_private_unshared": mut_two_player_private,
    "iv_state_explosion": mut_state_explosion,
}


if __name__ == "__main__":
    for name, mut in MUTATIONS.items():
        modes = (
            ["single_investigator", "two_player"]
            if name in ("iv_complete_two_player", "iv_two_player_private_unshared")
            else ["single_investigator"]
        )
        if name == "iv_pass_fail_leak":
            write_fixture(name, None, modes)
            write_player(FIXTURES / name, "Success: you find the key. Failure: you find nothing.\n")
        else:
            write_fixture(name, mut, modes)
    print("done", len(MUTATIONS))
