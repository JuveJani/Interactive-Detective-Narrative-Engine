"""Tests for Epistemic Progression Validator."""

from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from idne.epistemic_progression_validate import validate_epistemic_progression
from idne.validate_adventure.runner import validate_adventure

FIXTURES = Path(__file__).resolve().parent / "fixtures"


def _write(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def _minimal_workspace(tmp: Path, ep_pkg: dict, *, player_units: dict | None = None) -> Path:
    adv = tmp / "adventure"
    player = adv / "PLAYER"
    dnr = adv / "DO_NOT_READ"
    player.mkdir(parents=True)
    dnr.mkdir(parents=True)
    _write(
        adv / "generation_manifest.json",
        {
            "schema_version": "1.0",
            "generation_method": "world_first",
            "epistemic_progression": {"enabled": True},
        },
    )
    _write(
        adv / "epistemic_progression_manifest.json",
        {
            "schema_version": "1.0",
            "epistemic_progression_method": "canonical",
            "package_path": "DO_NOT_READ/epistemic_progression_package.json",
        },
    )
    _write(dnr / "epistemic_progression_package.json", ep_pkg)
    _write(
        dnr / "investigation_core_package.json",
        {
            "schema_version": "1.0",
            "adventure_id": "ep_test",
            "knowledge": [{"knowledge_id": kid} for kid in ep_pkg.get("all_knowledge", [])],
        },
    )
    _write(
        dnr / "investigation_flow_package.json",
        {
            "schema_version": "1.0",
            "adventure_id": "ep_test",
            "state_model": {"flags": [], "counters": [], "initial_state": ep_pkg.get("initial_world_state", {})},
            "time_model": {"clocks": ["T0"], "deadline_clock": "T0"},
            "endings": [],
            "ending_graph": {},
        },
    )
    manifest_units = {}
    blocks: list[str] = []
    for event in ep_pkg.get("playable_events", []):
        uid = event["unit_id"]
        body = event.get("_player_body", "Scene body.")
        choices = [a["label"] for a in event.get("structured_actions", [])]
        block = f"<!-- unit:{uid.lower()} -->\n### {uid}\n\n{body}\n\n"
        if choices:
            block += "**What do you do?**\n\n" + "\n".join(f"- {c}" for c in choices) + "\n"
        blocks.append(block)
        manifest_units[uid] = {
            "unit_id": uid,
            "file": "PLAYER/PLAY.md",
            "anchor": uid,
            "choices": [
                {
                    "label": a["label"],
                    "destination_unit_id": a["destination_unit_id"],
                    "kind": a.get("action_type", "action"),
                }
                for a in event.get("structured_actions", [])
            ],
        }
        for action in event.get("structured_actions", []):
            dest = action["destination_unit_id"]
            if dest not in manifest_units and dest not in {e["unit_id"] for e in ep_pkg.get("playable_events", [])}:
                manifest_units[dest] = {"unit_id": dest, "file": "PLAYER/PLAY.md", "anchor": dest, "choices": []}
    (player / "PLAY.md").write_text("\n".join(blocks), encoding="utf-8")
    if player_units:
        manifest_units.update(player_units)
    _write(
        tmp / "player_mapping_manifest.json",
        {
            "schema_version": "1.1",
            "adventure_id": "ep_test",
            "unit_count": len(manifest_units),
            "units": manifest_units,
            "static_book": {"start_unit_id": "UNIT-DOCK-BASE", "delivery_mode": "static_book"},
        },
    )
    return adv


class TestEpistemicProgression(unittest.TestCase):
    def test_opening_with_later_clue_fails(self):
        ws = Path(tempfile.mkdtemp(prefix="ep_"))
        ep = {
            "schema_version": "1.0",
            "adventure_id": "ep_test",
            "initial_player_knowledge": [],
            "initial_world_state": {},
            "all_knowledge": ["KNOW-LATER"],
            "playable_events": [
                {
                    "event_id": "EVT-OPEN",
                    "unit_id": "UNIT-DOCK-BASE",
                    "location_id": "LOC-DOCK",
                    "event_kind": "location_hub",
                    "structured_actions": [
                        {
                            "action_id": "ACT-LATE",
                            "action_type": "dialogue_topic",
                            "label": "Ask about the deleted alarm entry from 22:14.",
                            "destination_unit_id": "UNIT-TOPIC",
                            "requires_knowledge_ids": [],
                            "referenced_fact_ids": ["KNOW-LATER"],
                        }
                    ],
                },
                {"event_id": "EVT-TOPIC", "unit_id": "UNIT-TOPIC", "location_id": "LOC-DOCK", "event_kind": "dialogue_topic", "structured_actions": []},
            ],
        }
        root = _minimal_workspace(ws, ep)
        res = validate_epistemic_progression(root)
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "EP-CHOICE-UNKNOWN-FACT" for f in res.findings))

    def test_choice_names_unknown_fact_fails(self):
        ws = Path(tempfile.mkdtemp(prefix="ep_"))
        ep = {
            "schema_version": "1.0",
            "adventure_id": "ep_test",
            "initial_player_knowledge": [],
            "initial_world_state": {},
            "all_knowledge": ["KNOW-SECRET"],
            "playable_events": [
                {
                    "event_id": "EVT-OPEN",
                    "unit_id": "UNIT-DOCK-BASE",
                    "location_id": "LOC-DOCK",
                    "event_kind": "location_hub",
                    "structured_actions": [
                        {
                            "action_id": "ACT-BAD",
                            "action_type": "action",
                            "label": "Inspect the secret badge log entry.",
                            "destination_unit_id": "UNIT-X",
                            "referenced_fact_ids": ["KNOW-SECRET"],
                        }
                    ],
                },
                {"event_id": "EVT-X", "unit_id": "UNIT-X", "location_id": "LOC-DOCK", "event_kind": "observation_result", "structured_actions": []},
            ],
        }
        res = validate_epistemic_progression(_minimal_workspace(ws, ep))
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "EP-CHOICE-UNKNOWN-FACT" for f in res.findings))

    def test_unknown_npc_fails(self):
        ws = Path(tempfile.mkdtemp(prefix="ep_"))
        ep = {
            "schema_version": "1.0",
            "adventure_id": "ep_test",
            "initial_player_knowledge": [],
            "initial_world_state": {},
            "initial_observable_entities": ["NPC-ELENA"],
            "playable_events": [
                {
                    "event_id": "EVT-OPEN",
                    "unit_id": "UNIT-DOCK-BASE",
                    "location_id": "LOC-DOCK",
                    "event_kind": "location_hub",
                    "structured_actions": [
                        {
                            "action_id": "ACT-MARCUS",
                            "action_type": "approach_npc",
                            "label": "Talk to Marcus Hale.",
                            "destination_unit_id": "UNIT-MARCUS",
                            "requires_observable": ["NPC-MARCUS"],
                        }
                    ],
                },
                {"event_id": "EVT-M", "unit_id": "UNIT-MARCUS", "location_id": "LOC-DOCK", "event_kind": "npc_interaction", "structured_actions": []},
            ],
        }
        res = validate_epistemic_progression(_minimal_workspace(ws, ep))
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "EP-CHOICE-UNKNOWN-ENTITY" for f in res.findings))

    def test_hub_flattened_dialogue_fails(self):
        ws = Path(tempfile.mkdtemp(prefix="ep_"))
        ep = {
            "schema_version": "1.0",
            "adventure_id": "ep_test",
            "initial_player_knowledge": [],
            "initial_world_state": {},
            "playable_events": [
                {
                    "event_id": "EVT-HUB",
                    "unit_id": "UNIT-DOCK-BASE",
                    "location_id": "LOC-DOCK",
                    "event_kind": "location_hub",
                    "structured_actions": [
                        {
                            "action_id": "ACT-TOPIC",
                            "action_type": "dialogue_topic",
                            "label": "Ask Elena where to begin.",
                            "destination_unit_id": "UNIT-TOPIC",
                        }
                    ],
                },
                {"event_id": "EVT-T", "unit_id": "UNIT-TOPIC", "location_id": "LOC-DOCK", "event_kind": "dialogue_topic", "structured_actions": []},
            ],
        }
        res = validate_epistemic_progression(_minimal_workspace(ws, ep))
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "EP-HUB-FLATTENED-DIALOGUE" for f in res.findings))

    def test_npc_approach_then_topic_menu_passes(self):
        ws = Path(tempfile.mkdtemp(prefix="ep_"))
        ep = {
            "schema_version": "1.0",
            "adventure_id": "ep_test",
            "initial_player_knowledge": [],
            "initial_world_state": {},
            "initial_observable_entities": ["NPC-ELENA"],
            "playable_events": [
                {
                    "event_id": "EVT-HUB",
                    "unit_id": "UNIT-DOCK-BASE",
                    "location_id": "LOC-DOCK",
                    "event_kind": "location_hub",
                    "structured_actions": [
                        {
                            "action_id": "ACT-APPROACH",
                            "action_type": "approach_npc",
                            "label": "Talk to Elena.",
                            "destination_unit_id": "UNIT-ELENA-HUB",
                            "requires_observable": ["NPC-ELENA"],
                        }
                    ],
                },
                {
                    "event_id": "EVT-ELENA",
                    "unit_id": "UNIT-ELENA-HUB",
                    "location_id": "LOC-DOCK",
                    "event_kind": "npc_interaction",
                    "structured_actions": [
                        {
                            "action_id": "ACT-BEGIN",
                            "action_type": "dialogue_topic",
                            "label": "Ask where the investigation should begin.",
                            "destination_unit_id": "UNIT-ELENA-BEGIN",
                        }
                    ],
                },
                {"event_id": "EVT-B", "unit_id": "UNIT-ELENA-BEGIN", "location_id": "LOC-DOCK", "event_kind": "dialogue_topic", "structured_actions": [
                    {
                        "action_id": "ACT-HUB",
                        "action_type": "return",
                        "label": "Return to the Elena conversation menu.",
                        "destination_unit_id": "UNIT-ELENA-HUB",
                    },
                    {
                        "action_id": "ACT-EXIT",
                        "action_type": "return",
                        "label": "Return to the loading dock.",
                        "destination_unit_id": "UNIT-DOCK-BASE",
                    },
                ]},
            ],
        }
        res = validate_epistemic_progression(_minimal_workspace(ws, ep))
        self.assertEqual(res.status, "PASS")

    def test_return_to_old_unit_after_knowledge_fails(self):
        ws = Path(tempfile.mkdtemp(prefix="ep_"))
        ep = {
            "schema_version": "1.0",
            "adventure_id": "ep_test",
            "initial_player_knowledge": [],
            "initial_world_state": {},
            "playable_events": [
                {
                    "event_id": "EVT-HUB",
                    "unit_id": "UNIT-DOCK-BASE",
                    "location_id": "LOC-DOCK",
                    "physical_location_id": "LOC-DOCK",
                    "event_kind": "location_hub",
                    "relevant_knowledge_dependencies": ["KNOW-A"],
                    "structured_actions": [
                        {
                            "action_id": "ACT-LEARN",
                            "action_type": "observation",
                            "label": "Look around.",
                            "destination_unit_id": "UNIT-DOCK-BASE",
                            "knowledge_delta": ["KNOW-A"],
                            "investigative": True,
                            "purpose": "orient",
                        }
                    ],
                }
            ],
        }
        res = validate_epistemic_progression(_minimal_workspace(ws, ep))
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(
            any(
                f.finding_id in ("EP-DEST-PREREQ-MISMATCH", "EP-SCENE-REUSE-KNOWLEDGE")
                for f in res.findings
            )
        )

    def test_return_with_new_variant_passes(self):
        ws = Path(tempfile.mkdtemp(prefix="ep_"))
        ep = {
            "schema_version": "1.0",
            "adventure_id": "ep_test",
            "initial_player_knowledge": [],
            "initial_world_state": {},
            "playable_events": [
                {
                    "event_id": "EVT-OPEN",
                    "unit_id": "UNIT-DOCK-BASE",
                    "location_id": "LOC-DOCK",
                    "physical_location_id": "LOC-DOCK",
                    "event_kind": "location_hub",
                    "relevant_knowledge_dependencies": [],
                    "structured_actions": [
                        {
                            "action_id": "ACT-LEARN",
                            "action_type": "observation",
                            "label": "Look around.",
                            "destination_unit_id": "UNIT-DOCK-AFTER",
                            "knowledge_delta": ["KNOW-A"],
                            "investigative": True,
                            "purpose": "orient",
                        }
                    ],
                },
                {
                    "event_id": "EVT-AFTER",
                    "unit_id": "UNIT-DOCK-AFTER",
                    "location_id": "LOC-DOCK",
                    "physical_location_id": "LOC-DOCK",
                    "event_kind": "location_hub",
                    "variant_of": "UNIT-DOCK-BASE",
                    "required_knowledge_ids": ["KNOW-A"],
                    "relevant_knowledge_dependencies": ["KNOW-A"],
                    "structured_actions": [],
                },
            ],
        }
        res = validate_epistemic_progression(_minimal_workspace(ws, ep))
        self.assertEqual(res.status, "PASS")

    def test_unrelated_knowledge_does_not_invalidate_scene_passes(self):
        ws = Path(tempfile.mkdtemp(prefix="ep_"))
        ep = {
            "schema_version": "1.0",
            "adventure_id": "ep_test",
            "initial_player_knowledge": ["KNOW-UNRELATED"],
            "initial_world_state": {},
            "playable_events": [
                {
                    "event_id": "EVT-HUB",
                    "unit_id": "UNIT-DOCK-BASE",
                    "location_id": "LOC-DOCK",
                    "event_kind": "location_hub",
                    "relevant_knowledge_dependencies": ["KNOW-A"],
                    "structured_actions": [
                        {
                            "action_id": "ACT-NAV",
                            "action_type": "nav",
                            "label": "Go to cold storage.",
                            "destination_unit_id": "UNIT-COLD",
                        }
                    ],
                },
                {"event_id": "EVT-C", "unit_id": "UNIT-COLD", "location_id": "LOC-COLD", "event_kind": "location_hub", "structured_actions": []},
            ],
        }
        res = validate_epistemic_progression(_minimal_workspace(ws, ep))
        self.assertEqual(res.status, "PASS")

    def test_one_time_question_still_available_fails(self):
        ws = Path(tempfile.mkdtemp(prefix="ep_"))
        ep = {
            "schema_version": "1.0",
            "adventure_id": "ep_test",
            "initial_player_knowledge": [],
            "initial_world_state": {},
            "playable_events": [
                {
                    "event_id": "EVT-HUB",
                    "unit_id": "UNIT-DOCK-BASE",
                    "location_id": "LOC-DOCK",
                    "event_kind": "npc_interaction",
                    "structured_actions": [
                        {
                            "action_id": "ACT-ONCE",
                            "action_type": "dialogue_topic",
                            "label": "Ask their name.",
                            "destination_unit_id": "UNIT-NAME",
                            "exhaustion": "one_time",
                        },
                        {
                            "action_id": "ACT-ONCE",
                            "action_type": "dialogue_topic",
                            "label": "Ask their name again.",
                            "destination_unit_id": "UNIT-NAME",
                            "exhaustion": "repeatable",
                        },
                    ],
                },
                {"event_id": "EVT-N", "unit_id": "UNIT-NAME", "location_id": "LOC-DOCK", "event_kind": "dialogue_topic", "structured_actions": []},
            ],
        }
        res = validate_epistemic_progression(_minimal_workspace(ws, ep))
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "EP-ONETIME-STILL-VISIBLE" for f in res.findings))

    def test_investigative_no_progress_fails(self):
        ws = Path(tempfile.mkdtemp(prefix="ep_"))
        ep = {
            "schema_version": "1.0",
            "adventure_id": "ep_test",
            "initial_player_knowledge": [],
            "initial_world_state": {},
            "playable_events": [
                {
                    "event_id": "EVT-HUB",
                    "unit_id": "UNIT-DOCK-BASE",
                    "location_id": "LOC-DOCK",
                    "event_kind": "location_hub",
                    "structured_actions": [
                        {
                            "action_id": "ACT-EMPTY",
                            "action_type": "observation",
                            "label": "Stare at the wall.",
                            "destination_unit_id": "UNIT-DOCK-BASE",
                            "investigative": True,
                        }
                    ],
                }
            ],
        }
        res = validate_epistemic_progression(_minimal_workspace(ws, ep))
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "EP-NO-PROGRESS" for f in res.findings))

    def test_prose_extra_choice_fails(self):
        ws = Path(tempfile.mkdtemp(prefix="ep_"))
        ep = {
            "schema_version": "1.0",
            "adventure_id": "ep_test",
            "initial_player_knowledge": [],
            "initial_world_state": {},
            "playable_events": [
                {
                    "event_id": "EVT-HUB",
                    "unit_id": "UNIT-DOCK-BASE",
                    "location_id": "LOC-DOCK",
                    "event_kind": "location_hub",
                    "_player_body": "Dock.",
                    "structured_actions": [
                        {
                            "action_id": "ACT-A",
                            "action_type": "nav",
                            "label": "Go to cold storage.",
                            "destination_unit_id": "UNIT-COLD",
                        }
                    ],
                },
                {"event_id": "EVT-C", "unit_id": "UNIT-COLD", "location_id": "LOC-COLD", "event_kind": "location_hub", "structured_actions": []},
            ],
        }
        adv = _minimal_workspace(ws, ep)
        play = adv / "PLAYER" / "PLAY.md"
        text = play.read_text(encoding="utf-8")
        text = text.replace(
            "- Go to cold storage.",
            "- Go to cold storage.\n- Sneak into the hidden vault.",
        )
        play.write_text(text, encoding="utf-8")
        res = validate_epistemic_progression(adv)
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "EP-PROSE-EXTRA-CHOICE" for f in res.findings))

    def test_integrated_validation_fails_when_ep_fails(self):
        ws = Path(tempfile.mkdtemp(prefix="ep_"))
        ep = {
            "schema_version": "1.0",
            "adventure_id": "ep_test",
            "initial_player_knowledge": [],
            "initial_world_state": {},
            "playable_events": [
                {
                    "event_id": "EVT-HUB",
                    "unit_id": "UNIT-DOCK-BASE",
                    "location_id": "LOC-DOCK",
                    "event_kind": "location_hub",
                    "structured_actions": [
                        {
                            "action_id": "ACT-BAD",
                            "action_type": "dialogue_topic",
                            "label": "Ask about secret logs.",
                            "destination_unit_id": "UNIT-X",
                            "referenced_fact_ids": ["KNOW-SECRET"],
                        }
                    ],
                },
                {"event_id": "EVT-X", "unit_id": "UNIT-X", "location_id": "LOC-DOCK", "event_kind": "dialogue_topic", "structured_actions": []},
            ],
        }
        adv = _minimal_workspace(ws, ep)
        _write(adv / "investigation_validator_manifest.json", {"schema_version": "1.0", "investigation_validator_method": "canonical", "package_path": "DO_NOT_READ/investigation_validator_package.json"})
        _write(adv / "story_validator_manifest.json", {"schema_version": "1.0", "story_validator_method": "canonical", "package_path": "DO_NOT_READ/story_validator_package.json"})
        _write(adv / "DO_NOT_READ/investigation_validator_package.json", {"schema_version": "1.0", "adventure_id": "ep_test", "inference_questions": [], "information_sufficiency": [], "conclusion_traces": [], "recovery_routes": [], "access_requirements": [], "ending_reachability": [], "state_graph_config": {"max_states": 10, "max_depth": 5}})
        _write(adv / "DO_NOT_READ/story_validator_package.json", {"schema_version": "1.0", "adventure_id": "ep_test", "play_modes": ["single_investigator"], "story_frame": {}, "timeline": {}, "knowledge_order": [], "npc_consistency": [], "object_consistency": [], "ending_consistency": [], "opening_transitions": [], "player_files": {"opening_file": "PLAYER/OPENING.md"}})
        res = validate_adventure(adv)
        self.assertIn("epistemic_progression", res.validators)
        self.assertEqual(res.validators["epistemic_progression"]["status"], "FAIL")
        self.assertEqual(res.status, "FAIL")

    def test_single_target_pseudo_choice_fails(self):
        ws = Path(tempfile.mkdtemp(prefix="ep_"))
        ep = {
            "schema_version": "1.0",
            "adventure_id": "ep_test",
            "initial_player_knowledge": [],
            "initial_world_state": {},
            "initial_observable_entities": ["NPC-ELENA"],
            "playable_events": [
                {
                    "event_id": "EVT-HUB",
                    "unit_id": "UNIT-DOCK-ELENA-HUB",
                    "location_id": "LOC-DOCK",
                    "event_kind": "npc_interaction",
                    "structured_actions": [
                        {
                            "action_id": "ACT-TOPIC",
                            "action_type": "dialogue_topic",
                            "label": "Ask a question.",
                            "destination_unit_id": "UNIT-TOPIC",
                        }
                    ],
                },
                {
                    "event_id": "EVT-TOPIC",
                    "unit_id": "UNIT-TOPIC",
                    "location_id": "LOC-DOCK",
                    "event_kind": "dialogue_topic",
                    "structured_actions": [
                        {
                            "action_id": "ACT-RET",
                            "action_type": "return",
                            "label": "Return to your current location menu or continue the conversation.",
                            "destination_unit_id": "UNIT-DOCK-BASE",
                        }
                    ],
                },
                {"event_id": "EVT-BASE", "unit_id": "UNIT-DOCK-BASE", "location_id": "LOC-DOCK", "event_kind": "location_hub", "structured_actions": []},
            ],
        }
        adv = _minimal_workspace(ws, ep)
        res = validate_epistemic_progression(adv)
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "EP-PSEUDO-CHOICE" for f in res.findings))

    def test_dialogue_topic_requires_hub_return(self):
        ws = Path(tempfile.mkdtemp(prefix="ep_"))
        ep = {
            "schema_version": "1.0",
            "adventure_id": "ep_test",
            "initial_player_knowledge": [],
            "initial_world_state": {},
            "playable_events": [
                {
                    "event_id": "EVT-TOPIC",
                    "unit_id": "UNIT-TOPIC",
                    "location_id": "LOC-DOCK",
                    "event_kind": "dialogue_topic",
                    "structured_actions": [
                        {
                            "action_id": "ACT-EXIT",
                            "action_type": "return",
                            "label": "Return to the loading dock.",
                            "destination_unit_id": "UNIT-DOCK-BASE",
                        },
                        {
                            "action_id": "ACT-OTHER",
                            "action_type": "return",
                            "label": "Leave entirely.",
                            "destination_unit_id": "UNIT-BREAK-BASE",
                        },
                    ],
                },
                {"event_id": "EVT-BASE", "unit_id": "UNIT-DOCK-BASE", "location_id": "LOC-DOCK", "event_kind": "location_hub", "structured_actions": []},
                {"event_id": "EVT-BREAK", "unit_id": "UNIT-BREAK-BASE", "location_id": "LOC-BREAK", "event_kind": "location_hub", "structured_actions": []},
            ],
        }
        res = validate_epistemic_progression(_minimal_workspace(ws, ep))
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "EP-CONVERSATION-NO-HUB-RETURN" for f in res.findings))

    def test_unresolved_topic_time_cost_fails(self):
        ws = Path(tempfile.mkdtemp(prefix="ep_"))
        ep = {
            "schema_version": "1.0",
            "adventure_id": "ep_test",
            "initial_player_knowledge": [],
            "initial_world_state": {},
            "initial_observable_entities": ["NPC-ELENA"],
            "playable_events": [
                {
                    "event_id": "EVT-HUB",
                    "unit_id": "UNIT-DOCK-ELENA-HUB",
                    "location_id": "LOC-DOCK",
                    "event_kind": "npc_interaction",
                    "structured_actions": [
                        {
                            "action_id": "ACT-TOPIC",
                            "action_type": "dialogue_topic",
                            "label": "Ask a question.",
                            "destination_unit_id": "UNIT-TOPIC",
                        },
                        {
                            "action_id": "ACT-RET",
                            "action_type": "return",
                            "label": "Return to the loading dock.",
                            "destination_unit_id": "UNIT-DOCK-BASE",
                        },
                    ],
                },
                {
                    "event_id": "EVT-TOPIC",
                    "unit_id": "UNIT-TOPIC",
                    "location_id": "LOC-DOCK",
                    "event_kind": "dialogue_topic",
                    "_player_body": "Answer text.",
                    "structured_actions": [
                        {
                            "action_id": "ACT-HUB",
                            "action_type": "return",
                            "label": "Return to the Elena conversation menu.",
                            "destination_unit_id": "UNIT-DOCK-ELENA-HUB",
                        },
                        {
                            "action_id": "ACT-EXIT",
                            "action_type": "return",
                            "label": "Return to the loading dock.",
                            "destination_unit_id": "UNIT-DOCK-BASE",
                        },
                    ],
                },
                {"event_id": "EVT-BASE", "unit_id": "UNIT-DOCK-BASE", "location_id": "LOC-DOCK", "event_kind": "location_hub", "structured_actions": []},
            ],
        }
        adv = _minimal_workspace(ws, ep)
        play = adv / "PLAYER" / "PLAY.md"
        text = play.read_text(encoding="utf-8")
        text = text.replace("Answer text.", "Answer text.\n\n**Time cost:** varies by topic")
        play.write_text(text, encoding="utf-8")
        res = validate_epistemic_progression(adv)
        self.assertEqual(res.status, "FAIL")
        self.assertTrue(any(f.finding_id == "EP-TIME-COST-UNRESOLVED" for f in res.findings))

    def test_knowledge_map_returns_oriented_variant(self):
        ws = Path(tempfile.mkdtemp(prefix="ep_"))
        ep = {
            "schema_version": "1.0",
            "adventure_id": "ep_test",
            "initial_player_knowledge": [],
            "initial_world_state": {},
            "initial_observable_entities": ["NPC-ELENA"],
            "playable_events": [
                {
                    "event_id": "EVT-OPEN",
                    "unit_id": "UNIT-DOCK-BASE",
                    "location_id": "LOC-DOCK",
                    "event_kind": "location_hub",
                    "structured_actions": [
                        {
                            "action_id": "ACT-HUB",
                            "action_type": "approach_npc",
                            "label": "Talk to Elena.",
                            "destination_unit_id": "UNIT-DOCK-ELENA-HUB",
                        }
                    ],
                },
                {
                    "event_id": "EVT-HUB",
                    "unit_id": "UNIT-DOCK-ELENA-HUB",
                    "location_id": "LOC-DOCK",
                    "event_kind": "npc_interaction",
                    "structured_actions": [
                        {
                            "action_id": "ACT-MAP",
                            "action_type": "dialogue_topic",
                            "label": "Ask for a map.",
                            "destination_unit_id": "UNIT-ELENA-MAP",
                        }
                    ],
                },
                {
                    "event_id": "EVT-MAP",
                    "unit_id": "UNIT-ELENA-MAP",
                    "location_id": "LOC-DOCK",
                    "event_kind": "dialogue_topic",
                    "structured_actions": [
                        {
                            "action_id": "ACT-HUB",
                            "action_type": "return",
                            "label": "Return to the Elena conversation menu.",
                            "destination_unit_id": "UNIT-DOCK-ELENA-HUB",
                            "knowledge_delta": ["KNOW-OPEN-ORIENT"],
                        },
                        {
                            "action_id": "ACT-EXIT",
                            "action_type": "return",
                            "label": "Return to the loading dock.",
                            "destination_unit_id": "UNIT-DOCK-BASE-SURVEYED",
                            "knowledge_delta": ["KNOW-OPEN-ORIENT"],
                        },
                    ],
                },
                {
                    "event_id": "EVT-SURVEYED",
                    "unit_id": "UNIT-DOCK-BASE-SURVEYED",
                    "location_id": "LOC-DOCK",
                    "event_kind": "location_hub",
                    "variant_of": "UNIT-DOCK-BASE",
                    "required_knowledge_ids": ["KNOW-OPEN-ORIENT"],
                    "structured_actions": [
                        {
                            "action_id": "ACT-NAV",
                            "action_type": "nav",
                            "label": "Go to security.",
                            "destination_unit_id": "UNIT-SECURITY-BASE",
                        }
                    ],
                },
                {"event_id": "EVT-SEC", "unit_id": "UNIT-SECURITY-BASE", "location_id": "LOC-SECURITY", "event_kind": "location_hub", "structured_actions": []},
            ],
        }
        res = validate_epistemic_progression(_minimal_workspace(ws, ep))
        self.assertEqual(res.status, "PASS")

    def test_resolve_playable_unit_picks_surveyed_variant(self):
        from idne.epistemic_progression.loader import load_epistemic_package, initial_epistemic_state
        from idne.epistemic_progression.resolve import resolve_playable_unit

        ws = Path(tempfile.mkdtemp(prefix="ep_"))
        ep = {
            "schema_version": "1.0",
            "adventure_id": "ep_test",
            "initial_player_knowledge": ["KNOW-OPEN-ORIENT"],
            "initial_world_state": {},
            "playable_events": [
                {
                    "event_id": "EVT-OPEN",
                    "unit_id": "UNIT-DOCK-BASE",
                    "location_id": "LOC-DOCK",
                    "event_kind": "location_hub",
                    "structured_actions": [],
                },
                {
                    "event_id": "EVT-SURVEYED",
                    "unit_id": "UNIT-DOCK-BASE-SURVEYED",
                    "location_id": "LOC-DOCK",
                    "event_kind": "location_hub",
                    "variant_of": "UNIT-DOCK-BASE",
                    "supersedes_unit_id": "UNIT-DOCK-BASE",
                    "required_knowledge_ids": ["KNOW-OPEN-ORIENT"],
                    "structured_actions": [],
                },
            ],
        }
        adv = _minimal_workspace(ws, ep)
        pkg = load_epistemic_package(adv)
        state = initial_epistemic_state(pkg)
        self.assertEqual(resolve_playable_unit(pkg, state, "UNIT-DOCK-BASE"), "UNIT-DOCK-BASE-SURVEYED")


if __name__ == "__main__":
    unittest.main()
