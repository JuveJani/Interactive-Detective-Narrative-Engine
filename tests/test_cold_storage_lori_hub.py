"""Regression tests for Lori conversation hub and player-visible self-loops."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

COLD = Path(__file__).resolve().parents[1] / "adventures" / "The_Cold_Storage_Alarm"
ADV = COLD / "adventure"


@unittest.skipUnless(COLD.exists(), "Cold Storage adventure not present")
class TestColdStorageLoriConversationHub(unittest.TestCase):
    def setUp(self) -> None:
        self.root = ADV
        self.manifest = json.loads((COLD / "player_mapping_manifest.json").read_text(encoding="utf-8"))
        from idne.epistemic_progression.loader import load_epistemic_package

        self.pkg = load_epistemic_package(self.root)

    def _sections(self) -> dict[str, int]:
        out = {}
        for uid, entry in (self.manifest.get("units") or {}).items():
            if entry.get("public_section") is not None:
                out[uid] = int(entry["public_section"])
        out.update({uid: int(sec) for uid, sec in (self.manifest.get("public_sections") or {}).items()})
        return out

    def test_speak_with_lori_goes_to_distinct_hub_section(self):
        sections = self._sections()
        manager_ids = [uid for uid in self.manifest["units"] if uid.startswith("UNIT-MANAGER-BASE--S-")]
        self.assertTrue(manager_ids)
        mgr = manager_ids[0]
        lori = next(
            c
            for c in self.manifest["units"][mgr]["choices"]
            if "Speak with Lori Okonkwo" in c["label"]
        )
        dest = lori["destination_unit_id"]
        self.assertTrue(dest.startswith("UNIT-MANAGER-LORI-HUB--S-"))
        self.assertNotEqual(sections[mgr], sections[dest])

    def test_lori_hub_shows_gated_topics_only_when_prerequisites_met(self):
        import sys

        sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
        from scripts.build_cold_storage_epistemic import LORI_HUB_ACTIONS
        from idne.epistemic_progression.loader import initial_epistemic_state
        from idne.epistemic_progression.eligibility import action_eligible
        from idne.epistemic_progression.model import EpistemicState, StructuredAction

        actions = {
            a["label"]: StructuredAction.from_dict(
                {
                    **a,
                    "requires_knowledge_ids": a.get("requires_knowledge_ids") or [],
                    "forbidden_knowledge_ids": [],
                    "requires_world_state": a.get("requires_world_state") or {},
                    "forbidden_world_state": {},
                    "requires_observable": a.get("requires_observable") or [],
                    "referenced_fact_ids": a.get("referenced_fact_ids") or [],
                    "referenced_entity_ids": [],
                    "knowledge_delta": a.get("knowledge_delta") or [],
                    "world_state_delta": a.get("world_state_delta") or {},
                    "interaction_delta": a.get("interaction_delta") or {},
                    "investigative": a.get("investigative", False),
                    "purpose": a.get("purpose", ""),
                }
            )
            for a in LORI_HUB_ACTIONS
        }
        base = initial_epistemic_state(self.pkg)
        low = EpistemicState(
            player_knowledge=frozenset(list(base.player_knowledge) + ["KNOW-OPEN-ORIENT"]),
            world_state=dict(base.world_state),
            interaction_state={"exhausted_actions": [], "completed_topics": []},
            observable_entities=base.observable_entities,
            observable_objects=base.observable_objects,
        )
        self.assertTrue(action_eligible(actions["Ask whether you entered cold storage after hours."], low)[0])
        self.assertFalse(
            action_eligible(actions["Ask about your control room visit around 23:20."], low)[0]
        )

        high = EpistemicState(
            player_knowledge=frozenset(
                list(low.player_knowledge)
                + ["KNOW-CONTROL-ENTRY", "KNOW-MANIFEST-GAP", "KNOW-LABEL-RESIDUE"]
            ),
            world_state=dict(base.world_state),
            interaction_state={"exhausted_actions": [], "completed_topics": []},
            observable_entities=base.observable_entities,
            observable_objects=base.observable_objects,
        )
        for label in (
            "Ask about your control room visit around 23:20.",
            "Confront with manifest exception evidence from MNF-IN-4471.",
            "Press about label residue found in aisle C.",
        ):
            self.assertTrue(action_eligible(actions[label], high)[0], label)

    def test_lori_topic_returns_to_updated_hub(self):
        from idne.epistemic_progression.loader import initial_epistemic_state
        from idne.epistemic_progression.resolve import resolve_playable_unit
        from idne.epistemic_progression.eligibility import filter_eligible_actions

        state = initial_epistemic_state(self.pkg)
        mgr = resolve_playable_unit(self.pkg, state, "UNIT-MANAGER-BASE")
        talk = next(
            a
            for a, ok, _ in filter_eligible_actions(self.pkg.events_by_unit[mgr], state)
            if ok and "Speak with Lori" in a.label
        )
        state = state.apply_action_deltas(talk)
        hub_before = resolve_playable_unit(self.pkg, state, talk.destination_unit_id)
        topic = next(
            a
            for a, ok, _ in filter_eligible_actions(self.pkg.events_by_unit[hub_before], state)
            if ok and a.label.startswith("Ask whether you entered cold storage")
        )
        state = state.apply_action_deltas(topic)
        topic_unit = resolve_playable_unit(self.pkg, state, topic.destination_unit_id)
        ret = next(
            a
            for a, ok, _ in filter_eligible_actions(self.pkg.events_by_unit[topic_unit], state)
            if ok and "Lori conversation menu" in a.label
        )
        state = state.apply_action_deltas(ret)
        hub_after = resolve_playable_unit(self.pkg, state, ret.destination_unit_id)
        self.assertNotEqual(hub_before, hub_after)
        labels_after = {
            a.label
            for a, ok, _ in filter_eligible_actions(self.pkg.events_by_unit[hub_after], state)
            if ok
        }
        self.assertNotIn("Ask whether you entered cold storage after hours.", labels_after)

    def test_lori_hub_exit_returns_to_manager_office_snapshot(self):
        from idne.epistemic_progression.loader import initial_epistemic_state
        from idne.epistemic_progression.resolve import resolve_playable_unit
        from idne.epistemic_progression.eligibility import filter_eligible_actions

        state = initial_epistemic_state(self.pkg)
        mgr_before = resolve_playable_unit(self.pkg, state, "UNIT-MANAGER-BASE")
        talk = next(
            a
            for a, ok, _ in filter_eligible_actions(self.pkg.events_by_unit[mgr_before], state)
            if ok and "Speak with Lori" in a.label
        )
        state = state.apply_action_deltas(talk)
        hub = resolve_playable_unit(self.pkg, state, talk.destination_unit_id)
        ret = next(
            a
            for a, ok, _ in filter_eligible_actions(self.pkg.events_by_unit[hub], state)
            if ok and a.label == "Return to the warehouse manager office."
        )
        state = state.apply_action_deltas(ret)
        mgr_after = resolve_playable_unit(self.pkg, state, ret.destination_unit_id)
        from idne.epistemic_progression.fingerprint import template_unit_id

        self.assertEqual(template_unit_id(mgr_after), "UNIT-MANAGER-BASE")

    def test_manager_location_hub_has_no_lori_dialogue_topics(self):
        template = next(e for e in self.pkg.events_by_unit.values() if e.unit_id == "UNIT-MANAGER-BASE")
        labels = [a.label for a in template.structured_actions]
        self.assertNotIn("Ask whether you entered cold storage after hours.", labels)
        self.assertNotIn("Confront with manifest exception evidence from MNF-IN-4471.", labels)
        self.assertIn("Speak with Lori Okonkwo about receiving and access topics you have unlocked.", labels)

    def test_no_player_visible_exact_self_loops(self):
        from idne.epistemic_progression.template_navigation import find_player_visible_self_loops

        loops = find_player_visible_self_loops(self.manifest)
        self.assertEqual(loops, [], f"player-visible self-loops: {loops[:5]}")

    def test_opening_still_has_exactly_three_choices(self):
        from idne.gamebook_nav.delivery import load_materialized_delivery
        from idne.gamebook_nav.extract import parse_player_units

        _, _, graph, _ = load_materialized_delivery(self.root, parse_player_units(self.root / "PLAYER"))
        nav = graph["UNIT-DOCK-BASE"]
        labels = [e.label for e in nav.choices]
        self.assertEqual(len(labels), 3)


if __name__ == "__main__":
    unittest.main()
