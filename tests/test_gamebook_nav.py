"""Tests for static gamebook navigation."""

from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from idne.gamebook_nav.build import build_gamebook_package
from idne.gamebook_nav.numbering import assign_public_sections
from idne.gamebook_nav.validate import validate_gamebook_navigation
from idne.gamebook_validate import requires_static_gamebook, validate_gamebook
from idne.validate_adventure.runner import validate_adventure

FIXTURES = Path(__file__).resolve().parent / "fixtures"
MINIMAL = FIXTURES / "gamebook_minimal"
COLD = Path(__file__).resolve().parents[1] / "adventures" / "The_Cold_Storage_Alarm"


class TestGamebookNav(unittest.TestCase):
    def test_numbering_is_deterministic_and_scrambled(self):
        units = ["UNIT-A", "UNIT-B", "UNIT-C", "UNIT-D"]
        first = assign_public_sections(units, "demo-adventure")
        second = assign_public_sections(units, "demo-adventure")
        self.assertEqual(first, second)
        self.assertEqual(len(set(first.values())), len(units))
        self.assertTrue(all(101 <= n <= 999 for n in first.values()))
        self.assertNotEqual(sorted(first.values()), sorted(units))

    def test_numbering_retains_existing_assignments(self):
        existing = {"UNIT-A": 111, "UNIT-B": 222}
        out = assign_public_sections(["UNIT-A", "UNIT-B", "UNIT-C"], "demo", existing_map=existing)
        self.assertEqual(out["UNIT-A"], 111)
        self.assertEqual(out["UNIT-B"], 222)
        self.assertNotIn(out["UNIT-C"], (111, 222))

    def test_validate_detects_duplicate_sections(self):
        manifest = {
            "units": {"UNIT-A": {}, "UNIT-B": {}},
            "public_sections": {"UNIT-A": 101, "UNIT-B": 101},
            "static_book": {"start_unit_id": "UNIT-A", "delivery_mode": "static_book"},
        }
        res = validate_gamebook_navigation(MINIMAL / "adventure", manifest=manifest, section_map=manifest["public_sections"])
        self.assertEqual(res.checks.get("GB-DUPLICATE"), "FAIL")

    def test_build_minimal_gamebook(self):
        ws = Path(tempfile.mkdtemp(prefix="gb_min_"))
        shutil.copytree(MINIMAL, ws / "gamebook_minimal")
        root = ws / "gamebook_minimal" / "adventure"
        result = build_gamebook_package(root, start_unit_id="UNIT-DOCK-BASE")
        self.assertEqual(result["validation"]["status"], "PASS")
        gamebook = (root / "PLAYER" / "GAMEBOOK.md").read_text(encoding="utf-8")
        self.assertIn("Starting section:", gamebook)
        self.assertIn("Turn to section", gamebook)
        manifest = json.loads((ws / "gamebook_minimal" / "player_mapping_manifest.json").read_text())
        self.assertEqual(manifest["schema_version"], "1.1")
        self.assertIn("static_book", manifest)

    def test_integrated_validator_skips_without_static_book_declaration(self):
        if not (FIXTURES / "gen_v2_canonical_solo").exists():
            self.skipTest("fixture missing")
        res = validate_adventure(FIXTURES / "gen_v2_canonical_solo")
        self.assertNotIn("gamebook", res.validators)

    def test_gamebook_validator_requires_declaration(self):
        res = validate_gamebook(MINIMAL / "adventure")
        self.assertEqual(res.status, "SKIP")

    @unittest.skipUnless(COLD.exists(), "Cold Storage adventure not present")
    def test_cold_storage_epistemic_conversation_flow_passes(self):
        from idne.epistemic_progression_validate import validate_epistemic_progression

        root = COLD / "adventure"
        res = validate_epistemic_progression(root)
        self.assertEqual(res.status, "PASS")
        self.assertEqual(res.checks.get("EP-CONVERSATION-FLOW"), "PASS")
        self.assertEqual(res.checks.get("EP-VARIANT-DEST"), "PASS")

    @unittest.skipUnless(COLD.exists(), "Cold Storage adventure not present")
    def test_cold_storage_map_exit_targets_post_knowledge_dock(self):
        from idne.epistemic_progression.loader import load_epistemic_package, initial_epistemic_state
        from idne.epistemic_progression.eligibility import filter_eligible_actions
        from idne.epistemic_progression.resolve import resolve_playable_unit
        from idne.epistemic_progression.fingerprint import STATE_SUFFIX

        root = COLD / "adventure"
        pkg = load_epistemic_package(root)
        state = initial_epistemic_state(pkg)
        for unit, label in (
            ("UNIT-DOCK-BASE", "Talk to Elena Morales."),
            ("UNIT-DOCK-ELENA-HUB", "Ask whether a map or site overview is available."),
            ("UNIT-ELENA-MAP", "Return to the loading dock."),
        ):
            cur = resolve_playable_unit(pkg, state, unit)
            event = pkg.events_by_unit[cur]
            action = next(a for a, ok, _ in filter_eligible_actions(event, state) if ok and a.label == label)
            state = state.apply_action_deltas(action)
            state.current_unit_id = resolve_playable_unit(pkg, state, action.destination_unit_id)

        self.assertIn("KNOW-OPEN-ORIENT", state.player_knowledge)
        self.assertIn(STATE_SUFFIX, state.current_unit_id)
        dock = pkg.events_by_unit[state.current_unit_id]
        labels = {a.label for a, ok, _ in filter_eligible_actions(dock, state) if ok}
        self.assertIn("Request escort clearance to the automation control room.", labels)

    @unittest.skipUnless(COLD.exists(), "Cold Storage adventure not present")
    def test_cold_storage_gamebook_build_passes(self):
        ws = Path(tempfile.mkdtemp(prefix="gb_cold_"))
        shutil.copytree(COLD, ws / "The_Cold_Storage_Alarm")
        root = ws / "The_Cold_Storage_Alarm" / "adventure"
        result = build_gamebook_package(root, adventure_id="The_Cold_Storage_Alarm")
        self.assertGreater(result["section_count"], 1000)
        self.assertEqual(result["delivery_mode"], "materialized_static_book")
        self.assertEqual(result["validation"]["status"], "PASS")
        self.assertTrue(requires_static_gamebook(root))
        gb = validate_gamebook(root)
        self.assertEqual(gb.status, "PASS")


class TestColdStorageEpisodicDelivery(unittest.TestCase):
    """Regression tests for materialized static delivery (EPISODIC_STATIC_DELIVERY_SPEC)."""

    @unittest.skipUnless(COLD.exists(), "Cold Storage adventure not present")
    def setUp(self) -> None:
        self.root = COLD / "adventure"
        self.manifest = json.loads((COLD / "player_mapping_manifest.json").read_text(encoding="utf-8"))

    @unittest.skipUnless(COLD.exists(), "Cold Storage adventure not present")
    def test_opening_section_has_exactly_three_choices(self):
        from idne.gamebook_nav.delivery import load_materialized_delivery
        from idne.gamebook_nav.extract import parse_player_units

        _, _, graph, _ = load_materialized_delivery(
            self.root, parse_player_units(self.root / "PLAYER", None)
        )
        nav = graph["UNIT-DOCK-BASE"]
        labels = [e.label for e in nav.choices]
        self.assertEqual(len(labels), 3)
        self.assertIn("Talk to Elena Morales.", labels)
        self.assertIn("Walk through the dock corridor to the cold storage hall.", labels)
        self.assertIn("Talk to a dock worker.", labels)

    @unittest.skipUnless(COLD.exists(), "Cold Storage adventure not present")
    def test_opening_has_no_inference_or_flattened_dialogue(self):
        from idne.gamebook_nav.delivery import load_materialized_delivery
        from idne.gamebook_nav.extract import parse_player_units

        _, _, graph, _ = load_materialized_delivery(
            self.root, parse_player_units(self.root / "PLAYER", None)
        )
        nav = graph["UNIT-DOCK-BASE"]
        for edge in nav.choices:
            self.assertNotIn("inference worksheet", edge.label.lower())
            self.assertFalse(edge.label.lower().startswith("ask "))
            self.assertNotIn("dialogue_topic", edge.edge_kind)

    @unittest.skipUnless(COLD.exists(), "Cold Storage adventure not present")
    def test_map_acquisition_yields_distinct_post_orient_dock(self):
        from idne.epistemic_progression.loader import load_epistemic_package, initial_epistemic_state
        from idne.epistemic_progression.resolve import resolve_playable_unit
        from idne.epistemic_progression.eligibility import filter_eligible_actions
        from idne.epistemic_progression.fingerprint import STATE_SUFFIX
        from idne.gamebook_nav.delivery import load_materialized_delivery
        from idne.gamebook_nav.extract import parse_player_units

        pkg = load_epistemic_package(self.root)
        state = initial_epistemic_state(pkg)
        _, _, graph, _ = load_materialized_delivery(
            self.root, parse_player_units(self.root / "PLAYER", None)
        )
        opening_sec = self.manifest["public_sections"]["UNIT-DOCK-BASE"]

        for unit, label in (
            ("UNIT-DOCK-BASE", "Talk to Elena Morales."),
            ("UNIT-DOCK-ELENA-HUB", "Ask whether a map or site overview is available."),
            ("UNIT-ELENA-MAP", "Return to the loading dock."),
        ):
            cur = resolve_playable_unit(pkg, state, unit)
            event = pkg.events_by_unit[cur]
            action = next(a for a, ok, _ in filter_eligible_actions(event, state) if ok and a.label == label)
            state = state.apply_action_deltas(action)
            state.current_unit_id = resolve_playable_unit(pkg, state, action.destination_unit_id)

        self.assertIn("KNOW-OPEN-ORIENT", state.player_knowledge)
        post_dock = state.current_unit_id
        self.assertIn(STATE_SUFFIX, post_dock)
        post_sec = self.manifest["public_sections"][post_dock]
        self.assertNotEqual(post_sec, opening_sec)

        post_labels = {e.label for e in graph[post_dock].choices}
        self.assertIn("Request escort clearance to the automation control room.", post_labels)

    @unittest.skipUnless(COLD.exists(), "Cold Storage adventure not present")
    def test_post_map_choices_use_materialized_destinations(self):
        from idne.epistemic_progression.loader import load_epistemic_package, initial_epistemic_state
        from idne.epistemic_progression.resolve import resolve_playable_unit
        from idne.epistemic_progression.eligibility import filter_eligible_actions

        pkg = load_epistemic_package(self.root)
        state = initial_epistemic_state(pkg)
        for unit, label in (
            ("UNIT-DOCK-BASE", "Talk to Elena Morales."),
            ("UNIT-DOCK-ELENA-HUB", "Ask whether a map or site overview is available."),
            ("UNIT-ELENA-MAP", "Return to the loading dock."),
        ):
            cur = resolve_playable_unit(pkg, state, unit)
            event = pkg.events_by_unit[cur]
            action = next(a for a, ok, _ in filter_eligible_actions(event, state) if ok and a.label == label)
            state = state.apply_action_deltas(action)
            state.current_unit_id = resolve_playable_unit(pkg, state, action.destination_unit_id)

        dock_event = pkg.events_by_unit[state.current_unit_id]
        escort = next(
            a for a in dock_event.structured_actions if "escort clearance" in a.label.lower()
        )
        manifest_entry = self.manifest["units"][state.current_unit_id]
        manifest_escort = next(
            c for c in manifest_entry["choices"] if "escort clearance" in c["label"].lower()
        )
        self.assertEqual(manifest_escort["destination_unit_id"], escort.destination_unit_id)

    @unittest.skipUnless(COLD.exists(), "Cold Storage adventure not present")
    def test_completed_topic_changes_conversation_hub(self):
        from idne.epistemic_progression.loader import load_epistemic_package, initial_epistemic_state
        from idne.epistemic_progression.resolve import resolve_playable_unit
        from idne.epistemic_progression.eligibility import filter_eligible_actions

        pkg = load_epistemic_package(self.root)
        state = initial_epistemic_state(pkg)
        hub_before = resolve_playable_unit(pkg, state, "UNIT-DOCK-ELENA-HUB")
        labels_before = {
            a.label
            for a, ok, _ in filter_eligible_actions(pkg.events_by_unit[hub_before], state)
            if ok
        }
        self.assertIn("Ask whether a map or site overview is available.", labels_before)

        cur = resolve_playable_unit(pkg, state, "UNIT-DOCK-BASE")
        talk = next(
            a
            for a, ok, _ in filter_eligible_actions(pkg.events_by_unit[cur], state)
            if ok and a.label == "Talk to Elena Morales."
        )
        state = state.apply_action_deltas(talk)
        hub = resolve_playable_unit(pkg, state, "UNIT-DOCK-ELENA-HUB")
        map_action = next(
            a
            for a, ok, _ in filter_eligible_actions(pkg.events_by_unit[hub], state)
            if ok and a.label == "Ask whether a map or site overview is available."
        )
        state = state.apply_action_deltas(map_action)
        map_unit = resolve_playable_unit(pkg, state, map_action.destination_unit_id)
        ret = next(
            a
            for a, ok, _ in filter_eligible_actions(pkg.events_by_unit[map_unit], state)
            if ok and "conversation menu" in a.label.lower()
        )
        state = state.apply_action_deltas(ret)
        state.current_unit_id = resolve_playable_unit(pkg, state, ret.destination_unit_id)

        hub_after = resolve_playable_unit(pkg, state, "UNIT-DOCK-ELENA-HUB")
        labels_after = {
            a.label
            for a, ok, _ in filter_eligible_actions(pkg.events_by_unit[hub_after], state)
            if ok
        }
        self.assertNotIn("Ask whether a map or site overview is available.", labels_after)

    @unittest.skipUnless(COLD.exists(), "Cold Storage adventure not present")
    def test_snapshot_delivery_has_no_cross_state_extras(self):
        from idne.epistemic_progression_validate import validate_epistemic_progression

        res = validate_epistemic_progression(self.root)
        self.assertEqual(res.checks.get("EP-DELIVERY-ALIGN"), "PASS")
        extra = [f for f in res.findings if f.finding_id == "EP-DELIVERY-EXTRA-CHOICE"]
        self.assertEqual(extra, [])

    @unittest.skipUnless(COLD.exists(), "Cold Storage adventure not present")
    def test_every_materialized_snapshot_has_public_section(self):
        from idne.epistemic_progression.loader import load_epistemic_package
        from idne.epistemic_progression_validate import validate_epistemic_progression

        pkg = load_epistemic_package(self.root)
        sections = self.manifest.get("public_sections") or {}
        materialized = [uid for uid, ev in pkg.events_by_unit.items() if ev.state_snapshot]
        missing = [uid for uid in materialized if uid not in sections]
        self.assertEqual(missing, [])
        res = validate_epistemic_progression(self.root)
        self.assertEqual(res.checks.get("EP-DELIVERY-ALIGN"), "PASS")

    @unittest.skipUnless(COLD.exists(), "Cold Storage adventure not present")
    def test_opening_prose_does_not_claim_map_or_orientation(self):
        from idne.gamebook_nav.delivery import load_materialized_delivery
        from idne.gamebook_nav.extract import parse_player_units

        _, units, _, _ = load_materialized_delivery(
            self.root, parse_player_units(self.root / "PLAYER", None)
        )
        body = units["UNIT-DOCK-BASE"].body.lower()
        self.assertIn("not yet marked in your notes", body)
        self.assertNotIn("site map is in your notes", body)
        self.assertNotIn("corridors to the break room", body)

    @unittest.skipUnless(COLD.exists(), "Cold Storage adventure not present")
    def test_post_map_prose_reflects_known_layout(self):
        from idne.epistemic_progression.loader import load_epistemic_package, initial_epistemic_state
        from idne.epistemic_progression.resolve import resolve_playable_unit
        from idne.epistemic_progression.eligibility import filter_eligible_actions
        from idne.gamebook_nav.delivery import load_materialized_delivery
        from idne.gamebook_nav.extract import parse_player_units

        pkg = load_epistemic_package(self.root)
        state = initial_epistemic_state(pkg)
        _, units, _, _ = load_materialized_delivery(
            self.root, parse_player_units(self.root / "PLAYER", None)
        )
        for unit, label in (
            ("UNIT-DOCK-BASE", "Talk to Elena Morales."),
            ("UNIT-DOCK-ELENA-HUB", "Ask whether a map or site overview is available."),
            ("UNIT-ELENA-MAP", "Return to the loading dock."),
        ):
            cur = resolve_playable_unit(pkg, state, unit)
            event = pkg.events_by_unit[cur]
            action = next(a for a, ok, _ in filter_eligible_actions(event, state) if ok and a.label == label)
            state = state.apply_action_deltas(action)
            state.current_unit_id = resolve_playable_unit(pkg, state, action.destination_unit_id)

        post_body = units[state.current_unit_id].body.lower()
        self.assertIn("site map is in your notes", post_body)
        self.assertIn("security office", post_body)
        self.assertNotIn("not yet marked in your notes", post_body)

    @unittest.skipUnless(COLD.exists(), "Cold Storage adventure not present")
    def test_narrative_rendering_is_deterministic(self):
        from idne.gamebook_nav.delivery import load_materialized_delivery
        from idne.gamebook_nav.extract import parse_player_units

        tpl = parse_player_units(self.root / "PLAYER", None)
        _, first, _, _ = load_materialized_delivery(self.root, tpl)
        _, second, _, _ = load_materialized_delivery(self.root, tpl)
        self.assertEqual(
            {uid: u.body for uid, u in first.items()},
            {uid: u.body for uid, u in second.items()},
        )

    @unittest.skipUnless(COLD.exists(), "Cold Storage adventure not present")
    def test_worker_hub_reuses_base_prose_without_state_blocks(self):
        from idne.gamebook_nav.delivery import load_materialized_delivery
        from idne.gamebook_nav.extract import parse_player_units

        _, units, _, _ = load_materialized_delivery(
            self.root, parse_player_units(self.root / "PLAYER", None)
        )
        worker_ids = [uid for uid in units if uid.startswith("UNIT-DOCK-WORKER-HUB")]
        self.assertGreater(len(worker_ids), 1)
        bodies = {units[uid].body for uid in worker_ids}
        self.assertEqual(len(bodies), 1)

    @unittest.skipUnless(COLD.exists(), "Cold Storage adventure not present")
    def test_gamebook_has_clickable_section_links_and_anchors(self):
        from idne.gamebook_nav.sections import ANCHOR_TAG, SECTION_LINK

        book = (self.root / "PLAYER" / "GAMEBOOK.md").read_text(encoding="utf-8")
        sections = self.manifest.get("public_sections") or {}
        self.assertGreater(len(SECTION_LINK.findall(book)), 10)
        anchor_ids = [int(m.group(1)) for m in ANCHOR_TAG.finditer(book)]
        self.assertEqual(sorted(anchor_ids), sorted(sections.values()))
        for label, target in SECTION_LINK.findall(book):
            self.assertEqual(label, target)
            self.assertIn(f'<a id="section-{target}"></a>', book)
        val = self.manifest.get("gamebook_validation") or {}
        self.assertEqual(val.get("checks", {}).get("GB-ANCHORS"), "PASS")
        self.assertEqual(val.get("checks", {}).get("GB-LINKS"), "PASS")

    @unittest.skipUnless(COLD.exists(), "Cold Storage adventure not present")
    def test_static_navigation_and_route_equivalence(self):
        from simulator_v2.human_delivery.runner import cmd_delivery_validate, cmd_human_trace

        out = cmd_delivery_validate(COLD)
        self.assertEqual(out["status"], "PASS")
        engine_out = cmd_human_trace(COLD, seed=42, strategy="human_random_legal")
        self.assertEqual(engine_out["result"]["canonical_equivalence"], "PASS")


if __name__ == "__main__":
    unittest.main()
