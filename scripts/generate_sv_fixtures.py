"""Generate story validator test fixtures (Milestone 8)."""

import json
from pathlib import Path

FIXTURES = Path(__file__).resolve().parents[1] / "tests" / "fixtures"

OPENING_VALID = (
    "You arrive at the manager's office on Monday morning at nine o'clock. "
    "The police called you to investigate a theft that occurred yesterday evening "
    "at nineteen fifty-five. Your client needs answers before the deadline tonight."
)

INVESTIGATION_VALID = "Search the desk in the manager's office.\nQuestion the caretaker about yesterday evening."


def base_sv(adventure_id: str, play_modes: list[str]) -> dict:
    two_valid = "two_player" in play_modes
    return {
        "schema_version": "1.0",
        "adventure_id": adventure_id,
        "play_modes": play_modes,
        "story_frame": {
            "investigation_starts_where": "manager's office",
            "investigation_starts_when": "Monday morning nine o'clock",
            "incident_description": "theft from the office",
            "incident_when": "yesterday evening nineteen fifty-five",
            "investigator_involvement": "police called you to investigate",
            "deadline_or_constraint": "deadline tonight",
            "reveals_culprit": False,
            "reveals_motive": False,
            "reveals_hidden_relationships": False,
            "reveals_correct_priority": False,
        },
        "timeline": {
            "investigation_start": {"label": "Monday 9am", "anchor_id": "T-INV-START"},
            "incident_date": {"label": "Sunday", "anchor_id": "T-INCIDENT-DATE"},
            "incident_time": {"label": "19:55", "anchor_id": "T-INCIDENT-TIME"},
            "current_in_world_time": {"label": "Monday 9am", "anchor_id": "T-CURRENT"},
            "investigation_confused_with_incident": False,
            "impossible_ordering": False,
            "events": [
                {
                    "event_id": "EVT-THEFT",
                    "label": "Office theft",
                    "anchor_id": "T-INCIDENT-DATE",
                    "ordering_index": 1,
                    "ambiguous_day": False,
                    "relative_without_anchor": False,
                    "silent_time_switch": False,
                    "contradicts": [],
                }
            ],
            "temporal_references": [
                {
                    "ref_id": "REF-INCIDENT-TIME",
                    "text_fragment": "at nineteen fifty-five",
                    "maps_to_anchor": "T-INCIDENT-TIME",
                    "day_clear": True,
                    "contradictory": False,
                },
                {
                    "ref_id": "REF-YESTERDAY",
                    "text_fragment": "yesterday evening",
                    "maps_to_anchor": "T-INCIDENT-DATE",
                    "day_clear": True,
                    "contradictory": False,
                },
            ],
        },
        "causal_events": [
            {
                "event_id": "EVT-THEFT",
                "cause_event_ids": ["EVT-OFFICE-ENTRY"],
                "consequences": ["key hidden in desk"],
                "actors": ["NPC-A"],
                "physical_traces": ["OBS-KEY"],
                "dependent_events": ["EVT-SEARCH"],
                "motive_connected": True,
                "method_compatible_with_world": True,
                "action_consistent_with_knowledge": True,
                "ending_supported": True,
                "missing_cause": False,
                "orphan_consequence": False,
            }
        ],
        "information_facts": [
            {
                "fact_id": "FACT-KEY",
                "term": "hidden key",
                "first_mention_scene": "SCENE-OFFICE",
                "explanation_scene": "SCENE-OFFICE",
                "player_understandable_at_first_use": True,
                "half_information": False,
                "undefined_term": False,
                "undefined_entity": False,
                "used_before_introduction": False,
                "explained_after_required_use": False,
                "unexplained_pronoun": False,
                "conflicting_duplicates": False,
                "appears_from_nowhere": False,
            }
        ],
        "knowledge_order": [
            {
                "scene_id": "SCENE-OFFICE",
                "unit_id": "UNIT-OFFICE",
                "required_knowledge_ids": ["KNOW-KEY"],
                "possible_prior_knowledge_ids": ["KNOW-KEY"],
                "assumes_undiscovered_event": False,
                "inference_terms_not_introduced": False,
                "npc_assumes_unformulated_question": False,
                "object_uses_hidden_background": False,
                "ending_relies_on_unavailable_info": False,
            }
        ],
        "npc_consistency": [
            {
                "npc_id": "NPC-B",
                "motivation_consistent": True,
                "testimony_within_knowledge": True,
                "actions_match_motivation": True,
                "deception_has_motive": True,
                "confession_has_pressure_or_evidence": True,
                "suspicious_innocent_believable": True,
                "guilty_not_highlighted_by_wording": True,
                "trust_reaction_consistent": True,
                "dialogue_within_knowledge": True,
                "drama_only_behavior": False,
                "sudden_cooperation_unexplained": False,
            }
        ],
        "location_object_continuity": [
            {
                "entity_id": "OBJ-DESK",
                "entity_type": "object",
                "introduced": True,
                "moved_without_event": False,
                "layout_changes_without_cause": False,
                "removed_item_reappears": False,
                "locked_described_open": False,
                "references_inaccessible_area": False,
                "revisit_ignores_changes": False,
                "time_variant_not_reflected": False,
            }
        ],
        "narrative_neutrality": [
            {
                "entity_id": "SUSPECT-A",
                "suspicious_quotation_marks": False,
                "loaded_adjectives": False,
                "loaded_description": False,
                "asymmetric_detail": False,
                "emphasis_spotlight": False,
                "tier_b_review_required": False,
            }
        ],
        "inference_questions": [
            {
                "question_id": "INF-001",
                "player_facing_text": "Where was the key hidden?",
                "terms_defined": True,
                "grammatically_clear": True,
                "subject_explicit": True,
                "facts_communicated_not_just_canonical": True,
                "presupposes_answer": False,
                "options_reveal_solution": False,
                "understandable": True,
                "undefined_terms": [],
                "grammatically_unclear": False,
            }
        ],
        "opening_transitions": [
            {
                "transition_id": "OPEN-001",
                "scene_id": "SCENE-OPEN",
                "clear_purpose": True,
                "player_knows_actions": True,
                "causal_transition": True,
                "unexplained_exposition": False,
                "unexplained_jump": False,
                "return_makes_sense": True,
                "opening_lacks_incident_context": False,
                "no_causal_explanation": False,
            }
        ],
        "ending_story": [
            {
                "ending_id": "END-PERFECT",
                "ending_type": "perfect",
                "causal_sequence": True,
                "outcome_follows_actions": True,
                "contradicts_fixed_truth": False,
                "contradicts_timeline": False,
                "imperfect_leaks_full_truth": False,
                "claims_unsupported_certainty": False,
                "coherently_explains_truth": True,
                "intentionally_uncertain": False,
            },
            {
                "ending_id": "END-PARTIAL",
                "ending_type": "imperfect",
                "causal_sequence": True,
                "outcome_follows_actions": True,
                "contradicts_fixed_truth": False,
                "contradicts_timeline": False,
                "imperfect_leaks_full_truth": False,
                "claims_unsupported_certainty": False,
                "coherently_explains_truth": False,
                "intentionally_uncertain": True,
            },
        ],
        "plain_language": {
            "known_acronyms": ["ID"],
            "jargon_terms": ["cryptanalysis", "forensic", "spectrometry"],
            "entity_name_aliases": {"Manager": ["the manager", "Mr. Hale"]},
            "entries": [
                {
                    "source_ref": "PLAYER/OPENING.md",
                    "very_long_sentences": False,
                    "undefined_acronyms": [],
                    "excessive_jargon": False,
                    "ambiguous_pronouns": False,
                    "stacked_unrelated_facts": False,
                    "inconsistent_entity_names": False,
                }
            ],
        },
        "player_audit": {
            "files": ["PLAYER/OPENING.md", "PLAYER/INVESTIGATION.md"],
            "opening_file": "PLAYER/OPENING.md",
            "story_frame_communicated": True,
            "player_text_absent": False,
        },
        "play_mode_constraints": {
            "single_investigator_valid": True,
            "two_player_valid": two_valid,
        },
        "tier_b_mandatory": [],
    }


def write_fixture(name: str, mutate=None, play_modes=None, opening=None, investigation=None, skip_player=False):
    dest = FIXTURES / name
    if dest.exists():
        import shutil

        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    modes = play_modes or ["single_investigator"]
    pkg = base_sv(name, modes)
    if mutate:
        mutate(pkg)
    if skip_player:
        pkg["player_audit"]["player_text_absent"] = True
        pkg["player_audit"]["files"] = ["PLAYER/OPENING.md"]
    (dest / "DO_NOT_READ").mkdir(parents=True, exist_ok=True)
    (dest / "DO_NOT_READ" / "story_validator_package.json").write_text(json.dumps(pkg, indent=2) + "\n")
    (dest / "story_validator_manifest.json").write_text(
        json.dumps(
            {
                "schema_version": "1.0",
                "story_validator_method": "canonical",
                "package_path": "DO_NOT_READ/story_validator_package.json",
            },
            indent=2,
        )
        + "\n"
    )
    if not skip_player:
        player = dest / "PLAYER"
        player.mkdir(parents=True, exist_ok=True)
        (player / "OPENING.md").write_text(opening or OPENING_VALID + "\n")
        (player / "INVESTIGATION.md").write_text(investigation or INVESTIGATION_VALID + "\n")


MUTATIONS = {
    "sv_valid_clear": None,
    "sv_ambiguous_incident_day": lambda p: p["timeline"]["events"][0].update({"ambiguous_day": True}),
    "sv_start_confused_with_incident": lambda p: p["timeline"].update({"investigation_confused_with_incident": True}),
    "sv_contradictory_timeline": lambda p: p["timeline"]["events"][0]["contradicts"].append("EVT-OTHER"),
    "sv_unexplained_relative_date": lambda p: p["timeline"]["events"].append(
        {
            "event_id": "EVT-REL",
            "relative_without_anchor": True,
            "ambiguous_day": False,
            "silent_time_switch": False,
            "contradicts": [],
        }
    ),
    "sv_fact_before_introduction": lambda p: p["information_facts"][0].update({"used_before_introduction": True}),
    "sv_undefined_entity": lambda p: p["information_facts"][0].update({"undefined_entity": True}),
    "sv_half_information": lambda p: p["information_facts"][0].update({"half_information": True}),
    "sv_npc_testimony_beyond_knowledge": lambda p: p["npc_consistency"][0].update({"testimony_within_knowledge": False}),
    "sv_npc_contradicts_motivation": lambda p: p["npc_consistency"][0].update({"actions_match_motivation": False}),
    "sv_suspicious_innocent_unexplained": lambda p: p["npc_consistency"][0].update({"suspicious_innocent_believable": False}),
    "sv_object_moves_no_event": lambda p: p["location_object_continuity"][0].update({"moved_without_event": True}),
    "sv_revisit_ignores_state": lambda p: p["location_object_continuity"][0].update({"revisit_ignores_changes": True}),
    "sv_inference_undefined_term": lambda p: p["inference_questions"][0].update(
        {"terms_defined": False, "undefined_terms": ["cryptic_term"]}
    ),
    "sv_inference_unclear_grammar": lambda p: p["inference_questions"][0].update(
        {"grammatically_clear": False, "grammatically_unclear": True}
    ),
    "sv_opening_lacks_context": lambda p: p["opening_transitions"][0].update({"opening_lacks_incident_context": True}),
    "sv_transition_no_cause": lambda p: p["opening_transitions"][0].update(
        {"no_causal_explanation": True, "causal_transition": False}
    ),
    "sv_ending_contradicts_truth": lambda p: next(e for e in p["ending_story"] if e["ending_id"] == "END-PERFECT").update(
        {"contradicts_fixed_truth": True}
    ),
    "sv_imperfect_ending_leak": lambda p: next(
        e for e in p["ending_story"] if e["ending_id"] == "END-PARTIAL"
    ).update({"imperfect_leaks_full_truth": True}),
    "sv_loaded_suspect_description": lambda p: p["narrative_neutrality"][0].update({"loaded_description": True}),
    "sv_quotation_mark_emphasis": lambda p: p["narrative_neutrality"][0].update({"suspicious_quotation_marks": True}),
    "sv_undefined_acronym": lambda p: p["plain_language"]["entries"][0].update({"undefined_acronyms": ["XYZ"]}),
    "sv_excessive_jargon": lambda p: p["plain_language"]["entries"][0].update({"excessive_jargon": True}),
    "sv_inconsistent_naming": lambda p: p["plain_language"]["entries"][0].update(
        {"inconsistent_entity_names": ["Manager"]}
    ),
    "sv_player_absent": None,
    "sv_valid_solo": None,
    "sv_valid_two_player": None,
    "sv_assumes_unavailable_knowledge": lambda p: p["knowledge_order"][0].update(
        {
            "assumes_undiscovered_event": True,
            "possible_prior_knowledge_ids": [],
        }
    ),
    "sv_perfect_ending_coherent": None,
    "sv_imperfect_ending_uncertain": None,
}


if __name__ == "__main__":
    for name, mut in MUTATIONS.items():
        modes = (
            ["single_investigator", "two_player"]
            if name == "sv_valid_two_player"
            else ["single_investigator"]
        )
        if name == "sv_player_absent":
            write_fixture(name, mut, modes, skip_player=True)
        elif name == "sv_loaded_suspect_description":
            write_fixture(
                name,
                mut,
                modes,
                opening=OPENING_VALID + "\nThe caretaker seemed strangely cooperative today.\n",
            )
        elif name == "sv_quotation_mark_emphasis":
            write_fixture(
                name,
                mut,
                modes,
                opening=OPENING_VALID + "\nYou meet the \"suspicious\" caretaker.\n",
            )
        elif name == "sv_excessive_jargon":
            write_fixture(
                name,
                mut,
                modes,
                opening=OPENING_VALID
                + "\nCryptanalysis forensic spectrometry analysis required.\n",
            )
        elif name == "sv_undefined_acronym":
            write_fixture(
                name,
                mut,
                modes,
                opening=OPENING_VALID + "\nThe XYZ report arrived.\n",
            )
        elif name == "sv_inconsistent_naming":
            write_fixture(
                name,
                mut,
                modes,
                opening=OPENING_VALID + "\nMr. Hale waits in the office.\n",
            )
        else:
            write_fixture(name, mut, modes)
    print("done", len(MUTATIONS))
