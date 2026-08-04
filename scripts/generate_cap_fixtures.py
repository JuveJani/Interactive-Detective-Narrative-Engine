"""Generate capability check test fixtures (Milestone 6)."""

import copy
import json
from pathlib import Path

FIXTURES = Path(__file__).resolve().parents[1] / "tests" / "fixtures"

MODIFIERS = [
    {"modifier_id": "MOD-PERCEPTION", "capability_category": "perception_observation", "source": "character_sheet.perception"},
    {"modifier_id": "MOD-REASONING", "capability_category": "reasoning_interpretation", "source": "character_sheet.reasoning"},
    {"modifier_id": "MOD-TECHNICAL", "capability_category": "technical_operation", "source": "character_sheet.technical"},
    {"modifier_id": "MOD-STRENGTH", "capability_category": "physical_strength", "source": "character_sheet.strength"},
    {"modifier_id": "MOD-PERSUADE", "capability_category": "social_persuasion", "source": "character_sheet.persuasion"},
    {"modifier_id": "MOD-INTIMIDATE", "capability_category": "social_intimidation", "source": "character_sheet.intimidation"},
]

INV_STUB = {
    "schema_version": "1.0",
    "adventure_id": "cap_stub",
    "world_facts": [{"fact_id": "WF-KEY", "statement": "Key under keyboard", "immutable": True}],
    "knowledge": [
        {"knowledge_id": "KNOW-KEY", "statement": "Key location", "acquisition": {"source_type": "observation", "source_id": "OBS-KEY"}},
        {"knowledge_id": "KNOW-LOGIN", "statement": "Login succeeded", "acquisition": {"source_type": "observation", "source_id": "OBS-LOGIN"}},
        {"knowledge_id": "KNOW-SECRET", "statement": "NPC secret", "acquisition": {"source_type": "testimony", "source_id": "TEST-001"}},
    ],
    "observations": [
        {"observation_id": "OBS-KEY", "description": "Key under keyboard"},
        {"observation_id": "OBS-LOGIN", "description": "System access"},
    ],
    "testimony": [{"testimony_id": "TEST-001", "source_npc_id": "NPC-B", "content_knowledge_id": "KNOW-SECRET"}],
    "conclusions": [
        {"conclusion_id": "CONC-CULPRIT", "category": "culprit", "answer_entity_id": "NPC-A"},
        {"conclusion_id": "CONC-METHOD", "category": "method", "answer_entity_id": "METHOD-PUSH"},
    ],
    "proofs": [{"proof_id": "PROOF-A", "conclusion_id": "CONC-CULPRIT", "required_knowledge_ids": ["KNOW-KEY", "KNOW-SECRET"]}],
    "hypotheses": [],
    "relationships": [],
    "physical_evidence": [],
    "compatibility_clue_map": [],
}

NPC_STUB = {
    "schema_version": "1.0",
    "adventure_id": "cap_stub",
    "investigation_core_links": {"package_path": "DO_NOT_READ/investigation_core_package.json"},
    "npcs": [
        {
            "npc_id": "NPC-A",
            "public_name": "Custodian",
            "static_properties": {"motivation": "job", "honesty": 0.5, "deception": 0.3, "manipulation": 0.2, "loyalty": "employer", "fear": "arrest"},
            "relationships": [],
            "initial_dynamic_state": {"trust": 40, "information_known": ["INFO-NPC-B-1"], "revealed_topics": [], "suspicion": 10, "pressure": 0},
        },
        {
            "npc_id": "NPC-B",
            "public_name": "Witness",
            "static_properties": {"motivation": "safety", "honesty": 0.8, "deception": 0.1, "manipulation": 0.1, "loyalty": "family", "fear": "retaliation"},
            "relationships": [],
            "initial_dynamic_state": {"trust": 50, "information_known": ["INFO-NPC-B-1"], "revealed_topics": [], "suspicion": 5, "pressure": 0},
        },
    ],
    "npc_graph": {"nodes": ["NPC-A", "NPC-B"], "edges": []},
    "information_known_model": [{"info_id": "INFO-NPC-B-1", "npc_id": "NPC-B", "knowledge_id": "KNOW-SECRET", "topic_id": "TOPIC-1"}],
    "topics": [{"topic_id": "TOPIC-1", "unlock_conditions": [{"type": "trust_threshold", "npc_id": "NPC-B", "min": 20}]}],
    "conversation_graph": [],
    "trust_model": {"default_range": {"min": 0, "max": 100}, "not_globally_positive": True, "modifiers": []},
    "relationship_reactions": [],
    "testimony_links": [],
}

OBJ_STUB = {
    "schema_version": "1.0",
    "adventure_id": "cap_stub",
    "objects": [
        {"object_id": "OBJ-DESK", "parent_id": "LOC-OFFICE", "parent_type": "location", "initial_state": "unsearched", "current_state": "unsearched"},
        {"object_id": "OBJ-KEY-HIDDEN", "parent_id": "OBJ-DESK", "parent_type": "object", "initial_state": "concealed", "current_state": "concealed"},
        {"object_id": "OBJ-CABINET", "parent_id": "LOC-OFFICE", "parent_type": "location", "initial_state": "locked", "current_state": "locked"},
    ],
    "actions": [],
    "result_units": [],
}


def base_pkg(adventure_id: str) -> dict:
    return {
        "schema_version": "1.0",
        "adventure_id": adventure_id,
        "play_modes": ["single_investigator", "two_player"],
        "investigation_core_links": {"package_path": "DO_NOT_READ/investigation_core_package.json"},
        "object_interaction_links": {"package_path": "DO_NOT_READ/object_interaction_package.json"},
        "npc_investigation_links": {"package_path": "DO_NOT_READ/npc_investigation_package.json"},
        "modifier_sources": copy.deepcopy(MODIFIERS),
        "resolution_model": {"formula": "d20 + character_modifier", "success_when": "result >= dc"},
        "difficulty_bands": {"easy": 5, "medium": 10, "hard": 15},
        "destination_units": [
            {"unit_id": "UNIT-CHK-DECL", "player_text": "Search the desk carefully.", "exposes_success_content": False, "exposes_failure_content": False},
            {"unit_id": "UNIT-KEY-SUCCESS", "player_text": "You notice something tucked beneath the papers.", "reveals_hidden_object": False},
            {"unit_id": "UNIT-KEY-FAIL", "player_text": "You search the desk but find nothing useful.", "hints_missed_content": False, "reveals_hidden_object": False},
            {"unit_id": "UNIT-LOGIN-SUCCESS", "player_text": "The login succeeds."},
            {"unit_id": "UNIT-LOGIN-FAIL", "player_text": "The system rejects the attempt.", "hints_missed_content": False},
            {"unit_id": "UNIT-SOCIAL-SUCCESS", "player_text": "She reluctantly answers."},
            {"unit_id": "UNIT-SOCIAL-FAIL", "player_text": "She refuses to discuss it.", "hints_missed_content": False},
            {"unit_id": "UNIT-COOP-SUCCESS", "player_text": "Together you spot the detail."},
            {"unit_id": "UNIT-COOP-FAIL", "player_text": "Neither of you spots anything useful.", "hints_missed_content": False},
        ],
        "checks": [
            {
                "check_id": "CHK-PERCEPTION-DESK",
                "parent_action_id": "ACT-SEARCH-DESK",
                "parent_action_layer": "object_interaction",
                "parent_action_type": "search",
                "player_action_label": "Search the desk carefully.",
                "capability": "perception",
                "capability_category": "perception_observation",
                "modifier_source_id": "MOD-PERCEPTION",
                "dc": 15,
                "dc_justification": "Key concealed under loose papers; medium-hard perception",
                "why_check_exists": "Concealed item may be missed",
                "success_enables": "Notice key location",
                "failure_consequence": "Key not found via this search",
                "alternate_route_exists": True,
                "alternate_route_id": "ALT-WITNESS-KEY",
                "mandatory_for_fair_path": False,
                "attempt_policy": {"default": "one_attempt", "retry_extension_point": "future_retry_policy"},
                "time_cost_minutes": 2,
                "cost_applied_once": True,
                "cost_applied_count": 1,
                "eligibility": {"single_investigator": "active_investigator", "two_player": "role_or_scene"},
                "fixed_truth_invariants": {
                    "changes_evidence_existence": False,
                    "changes_document_contents": False,
                    "changes_fixed_truth": False,
                    "changes_npc_fixed_knowledge": False,
                },
                "destinations": {
                    "action_unit_id": "UNIT-CHK-DECL",
                    "success_destination": "UNIT-KEY-SUCCESS",
                    "failure_destination": "UNIT-KEY-FAIL",
                },
                "success_effects": {
                    "reveals_information_ids": ["INFO-KEY-LOC"],
                    "grants_knowledge_ids": ["KNOW-KEY"],
                    "npc_social_effects": [],
                },
                "failure_effects": {"reveals_information_ids": [], "npc_social_effects": []},
                "information_trace": {
                    "fixed_truth_ref": "WF-KEY",
                    "source_layer": "object",
                    "source_id": "OBJ-KEY-HIDDEN",
                    "observation_id": "OBS-KEY",
                },
            },
            {
                "check_id": "CHK-TECH-LOGIN",
                "parent_action_id": "ACT-LOGIN",
                "parent_action_layer": "object_interaction",
                "parent_action_type": "login",
                "player_action_label": "Attempt to bypass the login screen.",
                "capability": "technical",
                "capability_category": "technical_operation",
                "modifier_source_id": "MOD-TECHNICAL",
                "dc": 10,
                "dc_justification": "Standard office login; medium difficulty",
                "why_check_exists": "Access may fail without technical skill",
                "success_enables": "System access",
                "failure_consequence": "Access denied; alternate witness route remains",
                "alternate_route_exists": True,
                "attempt_policy": {"default": "one_attempt", "retry_extension_point": "future_retry_policy"},
                "time_cost_minutes": 3,
                "cost_applied_once": True,
                "cost_applied_count": 1,
                "eligibility": {"single_investigator": "active_investigator"},
                "fixed_truth_invariants": {
                    "changes_evidence_existence": False,
                    "changes_document_contents": False,
                    "changes_fixed_truth": False,
                    "changes_npc_fixed_knowledge": False,
                },
                "destinations": {
                    "action_unit_id": "UNIT-CHK-DECL",
                    "success_destination": "UNIT-LOGIN-SUCCESS",
                    "failure_destination": "UNIT-LOGIN-FAIL",
                },
                "success_effects": {"grants_knowledge_ids": ["KNOW-LOGIN"], "npc_social_effects": []},
                "failure_effects": {"npc_social_effects": []},
                "information_trace": {
                    "fixed_truth_ref": "WF-KEY",
                    "source_layer": "object",
                    "source_id": "OBJ-CABINET",
                    "observation_id": "OBS-LOGIN",
                },
            },
            {
                "check_id": "CHK-PERSUADE-WITNESS",
                "parent_action_id": "ACT-TALK-B",
                "parent_action_layer": "npc_interaction",
                "parent_action_type": "persuade",
                "player_action_label": "Press the witness gently for details.",
                "capability": "persuasion",
                "capability_category": "social_persuasion",
                "modifier_source_id": "MOD-PERSUADE",
                "dc": 10,
                "dc_justification": "Witness is nervous but not hostile",
                "why_check_exists": "Social leverage may open testimony",
                "success_enables": "Witness shares held information",
                "failure_consequence": "Witness stays guarded",
                "alternate_route_exists": True,
                "attempt_policy": {"default": "one_attempt", "retry_extension_point": "future_retry_policy"},
                "eligibility": {"single_investigator": "active_investigator"},
                "fixed_truth_invariants": {
                    "changes_evidence_existence": False,
                    "changes_document_contents": False,
                    "changes_fixed_truth": False,
                    "changes_npc_fixed_knowledge": False,
                },
                "destinations": {"success_destination": "UNIT-SOCIAL-SUCCESS", "failure_destination": "UNIT-SOCIAL-FAIL"},
                "success_effects": {
                    "grants_knowledge_ids": ["KNOW-SECRET"],
                    "npc_social_effects": [{"npc_id": "NPC-B", "trust_delta": 5}],
                },
                "failure_effects": {"npc_social_effects": [{"npc_id": "NPC-B", "trust_delta": -2}]},
                "information_trace": {
                    "fixed_truth_ref": "WF-KEY",
                    "source_layer": "npc",
                    "source_id": "NPC-B",
                    "knowledge_id": "KNOW-SECRET",
                },
            },
            {
                "check_id": "CHK-COOP-PERCEPTION",
                "parent_action_id": "ACT-JOINT-SEARCH",
                "parent_action_layer": "object_interaction",
                "parent_action_type": "search",
                "player_action_label": "Both investigators search the alcove together.",
                "capability": "perception",
                "capability_category": "perception_observation",
                "modifier_source_id": "MOD-PERCEPTION",
                "dc": 12,
                "dc_justification": "Cooperative search; either may spot detail",
                "why_check_exists": "Two investigators may cooperate",
                "alternate_route_exists": True,
                "attempt_policy": {"default": "one_attempt", "retry_extension_point": "future_retry_policy"},
                "eligibility": {
                    "two_player": "both_at_scene",
                    "cooperative_policy": {
                        "explicit_joint_attempt_allowed": True,
                        "higher_result_counts": True,
                        "free_second_player_retry": False,
                    },
                },
                "fixed_truth_invariants": {
                    "changes_evidence_existence": False,
                    "changes_document_contents": False,
                    "changes_fixed_truth": False,
                    "changes_npc_fixed_knowledge": False,
                },
                "destinations": {"success_destination": "UNIT-COOP-SUCCESS", "failure_destination": "UNIT-COOP-FAIL"},
                "success_effects": {"grants_knowledge_ids": ["KNOW-KEY"]},
                "failure_effects": {},
                "information_trace": {"fixed_truth_ref": "WF-KEY", "source_id": "OBJ-KEY-HIDDEN", "observation_id": "OBS-KEY"},
            },
        ],
        "player_content_refs": {"files": [], "action_units": []},
    }


def mut_evidence(p):
    p["checks"][0]["fixed_truth_invariants"]["changes_evidence_existence"] = True


def mut_document(p):
    p["checks"][0]["fixed_truth_invariants"]["changes_document_contents"] = True


def mut_meaningless(p):
    c = copy.deepcopy(p["checks"][0])
    c.update({"check_id": "CHK-GUARANTEED", "guaranteed_action": True, "requires_roll": True, "parent_action_type": "open_unlocked_door"})
    p["checks"].append(c)


def mut_mismatch(p):
    p["checks"][0]["parent_action_type"] = "persuade"
    p["checks"][0]["capability_category"] = "perception_observation"


def mut_same_unit(p):
    p["player_content_refs"]["action_units"].append(
        {"unit_id": "UNIT-BAD", "body": "Success: you find the key. Failure: you find nothing.", "exposes_success_content": True, "exposes_failure_content": True}
    )


def mut_fail_leak(p):
    p["destination_units"][2]["hints_missed_content"] = True
    p["destination_units"][2]["player_text"] = "You fail to notice the hidden key under the keyboard."
    p["checks"][0]["failure_effects"]["reveals_information_ids"] = ["INFO-KEY-LOC"]


def mut_repeat(p):
    p["checks"].append(copy.deepcopy(p["checks"][0]))


def mut_free_retry(p):
    p["checks"][0]["eligibility"]["cooperative_policy"] = {"free_second_player_retry": True}


def mut_only_route(p):
    p["checks"][0]["alternate_route_exists"] = False
    p["checks"][0]["mandatory_for_fair_path"] = True


def mut_full_conclusion(p):
    p["checks"][0]["success_effects"]["grants_complete_solution"] = True


def mut_dup_cost(p):
    p["checks"][0]["failure_time_cost_minutes"] = 5
    p["checks"][0]["failure_cost_applied_count"] = 2
    p["checks"][0]["cost_applied_count"] = 2


def mut_npc_unknown(p):
    p["checks"][2]["success_effects"]["npc_social_effects"] = [{"npc_id": "NPC-B", "reveals_information_npc_did_not_know": True}]


def mut_intimidation_trust(p):
    c = copy.deepcopy(p["checks"][2])
    c.update({
        "check_id": "CHK-INTIMIDATE",
        "capability_category": "social_intimidation",
        "parent_action_type": "intimidate",
        "modifier_source_id": "MOD-INTIMIDATE",
        "success_effects": {"npc_social_effects": [{"npc_id": "NPC-B", "trust_delta": 10}]},
    })
    p["checks"].append(c)


def mut_no_provenance(p):
    p["checks"][0]["information_trace"] = {}


def mut_no_dc(p):
    p["checks"][0]["dc_justification"] = ""


def mut_bare_code(p):
    pass  # handled in write_fixture


def mut_solo_p2(p):
    p["checks"][0]["eligibility"]["requires_player_2"] = True


def mut_social_valid(p):
    c = copy.deepcopy(p["checks"][2])
    c.update({
        "check_id": "CHK-INTIMIDATE-VALID",
        "capability_category": "social_intimidation",
        "parent_action_type": "intimidate",
        "modifier_source_id": "MOD-INTIMIDATE",
        "success_effects": {
            "npc_social_effects": [{"npc_id": "NPC-B", "trust_delta": -5, "pressure_delta": 10, "intimidation_not_trust_justified": True}],
        },
    })
    p["checks"].append(c)


FIXTURES_MAP = {
    "cap_valid_perception_key": None,
    "cap_valid_fail_no_leak": None,
    "cap_evidence_existence_changed": mut_evidence,
    "cap_document_contents_changed": mut_document,
    "cap_meaningless_guaranteed": mut_meaningless,
    "cap_capability_mismatch": mut_mismatch,
    "cap_pass_fail_same_unit": mut_same_unit,
    "cap_fail_reveals_hidden": mut_fail_leak,
    "cap_repeated_check": mut_repeat,
    "cap_free_second_player_retry": mut_free_retry,
    "cap_only_proof_route": mut_only_route,
    "cap_success_full_conclusion": mut_full_conclusion,
    "cap_duplicated_failure_cost": mut_dup_cost,
    "cap_npc_unknown_info": mut_npc_unknown,
    "cap_intimidation_as_trust": mut_intimidation_trust,
    "cap_missing_provenance": mut_no_provenance,
    "cap_unjustified_dc": mut_no_dc,
    "cap_bare_code_choice": mut_bare_code,
    "cap_solo_requires_player2": mut_solo_p2,
    "cap_valid_cooperative_two": None,
    "cap_valid_technical_access": None,
    "cap_valid_social_trust_pressure": mut_social_valid,
}


def write_fixture(name: str, mutate=None):
    root = FIXTURES / name
    dnr = root / "DO_NOT_READ"
    dnr.mkdir(parents=True, exist_ok=True)
    pkg = base_pkg(name)
    if mutate:
        mutate(pkg)
    if name == "cap_bare_code_choice":
        player = root / "PLAYER" / "CHECKS.md"
        player.parent.mkdir(parents=True, exist_ok=True)
        player.write_text("Choose J-223 or J-224.\n")
        pkg["player_content_refs"]["files"] = ["PLAYER/CHECKS.md"]
    (root / "capability_check_manifest.json").write_text(
        json.dumps(
            {
                "schema_version": "1.0",
                "capability_check_method": "canonical",
                "package_path": "DO_NOT_READ/capability_check_package.json",
            },
            indent=2,
        ) + "\n"
    )
    (dnr / "capability_check_package.json").write_text(json.dumps(pkg, indent=2) + "\n")
    inv = copy.deepcopy(INV_STUB)
    inv["adventure_id"] = name
    (dnr / "investigation_core_package.json").write_text(json.dumps(inv, indent=2) + "\n")
    npc = copy.deepcopy(NPC_STUB)
    npc["adventure_id"] = name
    (dnr / "npc_investigation_package.json").write_text(json.dumps(npc, indent=2) + "\n")
    obj = copy.deepcopy(OBJ_STUB)
    obj["adventure_id"] = name
    (dnr / "object_interaction_package.json").write_text(json.dumps(obj, indent=2) + "\n")


if __name__ == "__main__":
    for name, mut in FIXTURES_MAP.items():
        write_fixture(name, mut)
    print("done", len(FIXTURES_MAP))
