"""Tests for Story Validator (Milestone 8)."""

import unittest
from pathlib import Path

from idne.story_validate import validate_story

FIXTURES = Path(__file__).resolve().parent / "fixtures"
HARBORVIEW = Path(__file__).resolve().parents[1] / "adventures" / "CASE_BENCHMARK_v0.4"


class TestStoryValidatorFixtures(unittest.TestCase):
    def test_valid_clear_passes(self):
        res = validate_story(FIXTURES / "sv_valid_clear")
        self.assertEqual(res.status, "PASS")

    def test_valid_solo_passes(self):
        res = validate_story(FIXTURES / "sv_valid_solo")
        self.assertEqual(res.status, "PASS")

    def test_valid_two_player_passes(self):
        res = validate_story(FIXTURES / "sv_valid_two_player")
        self.assertEqual(res.status, "PASS")

    def test_ambiguous_incident_day_fails(self):
        res = validate_story(FIXTURES / "sv_ambiguous_incident_day")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "SV-AMBIGUOUS-DAY" for f in res.findings))

    def test_start_confused_with_incident_fails(self):
        res = validate_story(FIXTURES / "sv_start_confused_with_incident")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "SV-START-INCIDENT-CONFUSED" for f in res.findings))

    def test_contradictory_timeline_fails(self):
        res = validate_story(FIXTURES / "sv_contradictory_timeline")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "SV-CONTRADICTORY-TIMELINE" for f in res.findings))

    def test_unexplained_relative_date_fails(self):
        res = validate_story(FIXTURES / "sv_unexplained_relative_date")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "SV-RELATIVE-NO-ANCHOR" for f in res.findings))

    def test_fact_before_introduction_fails(self):
        res = validate_story(FIXTURES / "sv_fact_before_introduction")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "SV-FACT-BEFORE-INTRO" for f in res.findings))

    def test_undefined_entity_fails(self):
        res = validate_story(FIXTURES / "sv_undefined_entity")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "SV-UNDEFINED-ENTITY" for f in res.findings))

    def test_half_information_fails(self):
        res = validate_story(FIXTURES / "sv_half_information")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "SV-HALF-INFORMATION" for f in res.findings))

    def test_npc_testimony_beyond_knowledge_fails(self):
        res = validate_story(FIXTURES / "sv_npc_testimony_beyond_knowledge")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "SV-NPC-BEYOND-KNOWLEDGE" for f in res.findings))

    def test_npc_contradicts_motivation_fails(self):
        res = validate_story(FIXTURES / "sv_npc_contradicts_motivation")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "SV-NPC-MOTIVATION" for f in res.findings))

    def test_suspicious_innocent_unexplained_fails(self):
        res = validate_story(FIXTURES / "sv_suspicious_innocent_unexplained")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "SV-SUSPICIOUS-INNOCENT" for f in res.findings))

    def test_object_moves_no_event_fails(self):
        res = validate_story(FIXTURES / "sv_object_moves_no_event")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "SV-OBJECT-MOVES" for f in res.findings))

    def test_revisit_ignores_state_fails(self):
        res = validate_story(FIXTURES / "sv_revisit_ignores_state")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "SV-REVISIT-IGNORES-STATE" for f in res.findings))

    def test_inference_undefined_term_fails(self):
        res = validate_story(FIXTURES / "sv_inference_undefined_term")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "SV-INFERENCE-UNDEFINED-TERM" for f in res.findings))

    def test_inference_unclear_grammar_fails(self):
        res = validate_story(FIXTURES / "sv_inference_unclear_grammar")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "SV-INFERENCE-UNCLEAR" for f in res.findings))

    def test_opening_lacks_context_fails(self):
        res = validate_story(FIXTURES / "sv_opening_lacks_context")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "SV-OPENING-LACKS-CONTEXT" for f in res.findings))

    def test_transition_no_cause_fails(self):
        res = validate_story(FIXTURES / "sv_transition_no_cause")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "SV-TRANSITION-NO-CAUSE" for f in res.findings))

    def test_ending_contradicts_truth_fails(self):
        res = validate_story(FIXTURES / "sv_ending_contradicts_truth")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "SV-ENDING-CONTRADICTS-TRUTH" for f in res.findings))

    def test_imperfect_ending_leak_fails(self):
        res = validate_story(FIXTURES / "sv_imperfect_ending_leak")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "SV-IMPERFECT-LEAK" for f in res.findings))

    def test_loaded_suspect_description_conditional(self):
        res = validate_story(FIXTURES / "sv_loaded_suspect_description")
        self.assertEqual(res.status, "CONDITIONAL_PASS")
        self.assertTrue(any(f.finding_id == "SV-LOADED-DESCRIPTION" for f in res.findings))

    def test_quotation_mark_emphasis_conditional(self):
        res = validate_story(FIXTURES / "sv_quotation_mark_emphasis")
        self.assertEqual(res.status, "CONDITIONAL_PASS")
        self.assertTrue(any(f.finding_id == "SV-QUOTATION-EMPHASIS" for f in res.findings))

    def test_undefined_acronym_fails(self):
        res = validate_story(FIXTURES / "sv_undefined_acronym")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "SV-UNDEFINED-ACRONYM" for f in res.findings))

    def test_excessive_jargon_fails(self):
        res = validate_story(FIXTURES / "sv_excessive_jargon")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "SV-EXCESSIVE-JARGON" for f in res.findings))

    def test_inconsistent_naming_fails(self):
        res = validate_story(FIXTURES / "sv_inconsistent_naming")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "SV-INCONSISTENT-NAMING" for f in res.findings))

    def test_player_absent_blocked(self):
        res = validate_story(FIXTURES / "sv_player_absent")
        self.assertEqual(res.status, "BLOCKED")
        self.assertTrue(any(f.finding_id == "SV-PLAYER-ABSENT" for f in res.findings))

    def test_assumes_unavailable_knowledge_fails(self):
        res = validate_story(FIXTURES / "sv_assumes_unavailable_knowledge")
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "SV-ASSUMES-UNAVAILABLE-KNOWLEDGE" for f in res.findings))

    def test_perfect_ending_coherent_passes(self):
        res = validate_story(FIXTURES / "sv_perfect_ending_coherent")
        self.assertEqual(res.status, "PASS")

    def test_imperfect_ending_uncertain_passes(self):
        res = validate_story(FIXTURES / "sv_imperfect_ending_uncertain")
        self.assertEqual(res.status, "PASS")

    def test_harborview_skips(self):
        if not HARBORVIEW.exists():
            self.skipTest("no harborview")
        res = validate_story(HARBORVIEW)
        self.assertEqual(res.status, "SKIP")


if __name__ == "__main__":
    unittest.main()
