"""Regression tests for adventure pack canonical normalization."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from idne.adventure_pack.normalize import (
    build_result_units,
    normalize_flow,
    normalize_navigation,
)
from idne.adventure_pack.spec import AdventurePackSpec


def _minimal_spec(**overrides) -> AdventurePackSpec:
    raw = {
        "pack_id": "Test_Pack",
        "locations": [{"location_id": "LOC-A", "public_name": "A"}],
        "navigation": [
            {
                "edge_id": "NAV-A-B",
                "from_location_id": "LOC-A",
                "to_location_id": "LOC-B",
                "direction_label": "Go to B.",
            }
        ],
        "objects": [],
        "object_actions": [],
        "checks": [
            {
                "check_id": "CHK-1",
                "declaration_unit_id": "UNIT-CHK-TEST-DECL",
                "success_unit_id": "UNIT-TEST-SUCCESS",
                "failure_unit_id": "UNIT-TEST-FAIL",
            }
        ],
        "player_units": {
            "units": [
                {
                    "unit_id": "UNIT-TEST-SUCCESS",
                    "choices": [{"label": "Back", "destination_unit_id": "UNIT-A-BASE"}],
                },
                {
                    "unit_id": "UNIT-TEST-FAIL",
                    "choices": [{"label": "Back", "destination_unit_id": "UNIT-A-BASE"}],
                },
            ]
        },
        "flow": {
            "endings": [
                {
                    "ending_id": "END-TIMEOUT",
                    "ending_type": "timeout",
                    "trigger": {"type": "deadline"},
                }
            ]
        },
        "knowledge": {},
        "npcs": [],
        "conversations": [],
        "epistemic": {},
        "gamebook": {},
        "brief": {},
        "fixed_truth": {},
    }
    raw.update(overrides)
    return AdventurePackSpec(
        raw=raw,
        pack_id=str(raw.get("pack_id")),
        brief=dict(raw.get("brief") or {}),
        fixed_truth=dict(raw.get("fixed_truth") or {}),
        locations=list(raw.get("locations") or []),
        npcs=list(raw.get("npcs") or []),
        objects=list(raw.get("objects") or []),
        knowledge=dict(raw.get("knowledge") or {}),
        player_units=dict(raw.get("player_units") or {}),
        navigation=list(raw.get("navigation") or []),
        flow=dict(raw.get("flow") or {}),
        conversations=list(raw.get("conversations") or []),
        object_actions=list(raw.get("object_actions") or []),
        checks=list(raw.get("checks") or []),
        epistemic=dict(raw.get("epistemic") or {}),
        gamebook=dict(raw.get("gamebook") or {}),
        validator_seeds=dict(raw.get("validator_seeds") or {}),
    )


class AdventurePackNormalizeTests(unittest.TestCase):
    def test_navigation_remaps_authoring_fields(self) -> None:
        spec = _minimal_spec()
        nav = normalize_navigation(spec)
        self.assertEqual(nav[0]["source_location_id"], "LOC-A")
        self.assertEqual(nav[0]["destination_location_id"], "LOC-B")
        self.assertEqual(nav[0]["player_label"], "Go to B.")
        self.assertEqual(nav[0]["access_condition"], {"type": "always"})

    def test_flow_timeout_becomes_deadline_ending(self) -> None:
        spec = _minimal_spec()
        flow = normalize_flow(spec)
        timeout = next(e for e in flow["endings"] if e["ending_id"] == "END-TIMEOUT")
        self.assertEqual(timeout["ending_type"], "deadline")
        self.assertEqual(timeout["trigger"]["type"], "deadline_expired")

    def test_result_units_include_check_destinations(self) -> None:
        spec = _minimal_spec()
        units = {u["unit_id"] for u in build_result_units(spec)}
        self.assertIn("UNIT-TEST-SUCCESS", units)
        self.assertIn("UNIT-TEST-FAIL", units)
        self.assertNotIn("UNIT-CHK-TEST-SUCCESS", units)

    def test_harbor_light_gamebook_check_split_passes(self) -> None:
        root = Path("adventures/The_Harbor_Light_Signal/adventure")
        if not root.exists():
            self.skipTest("Harbor Light not present")
        from idne.gamebook_validate import validate_gamebook

        result = validate_gamebook(root)
        self.assertEqual(result.checks.get("GB-CHECK-SPLIT"), "PASS")


if __name__ == "__main__":
    unittest.main()
