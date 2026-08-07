#!/usr/bin/env python3
"""Generate adventures/The_Gallery_Verdict/pack_spec.json from Harbor Light template."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "adventures/The_Harbor_Light_Signal/pack_spec.json"
OUTPUT = ROOT / "adventures/The_Gallery_Verdict/pack_spec.json"


def main() -> None:
    spec = json.loads(TEMPLATE.read_text(encoding="utf-8"))
    spec = _transform(spec)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT} ({len(spec['player_units']['units'])} player units)")


def _transform(spec: dict) -> dict:
    s = deepcopy(spec)
    s["pack_id"] = "The_Gallery_Verdict"
    s["brief"] = _brief()
    s["fixed_truth"] = _fixed_truth()
    s["locations"] = _locations()
    s["location_states"] = _location_states()
    s["features"] = _features()
    s["navigation"] = _navigation()
    s["npcs"] = _npcs()
    s["objects"] = _objects()
    s["knowledge"] = _knowledge()
    s["conversations"] = _conversations()
    s["object_actions"] = _object_actions()
    s["checks"] = _checks()
    s["flow"] = _flow()
    s["player_units"] = _player_units()
    s["epistemic"] = _epistemic()
    s["gamebook"] = {"enabled": True, "start_template_unit_id": "UNIT-LOBBY-BASE"}
    s["validator_seeds"] = _validator_seeds()
    s["modifier_sources"] = s["modifier_sources"]  # unchanged
    return s


def _brief() -> dict:
    return {
        "working_title": "The Gallery Verdict",
        "premise": "An independent insurance adjuster investigates the disappearance of a featured painting during a private gallery opening, reconstructing the evening from conflicting witness accounts, security logs, and sightline evidence.",
        "setting": "Contemporary urban art gallery during a private exhibition opening — main hall, secure vault, director's office, lobby, and rooftop terrace",
        "universe": "real world",
        "genre": "detective mystery",
        "realism_level": "grounded contemporary",
        "player_mode": "single_investigator",
        "investigator_character": "Independent insurance adjuster retained to determine whether the loss was theft or a staged claim",
        "opening_situation": "You arrive at the Meridian Contemporary after the opening-night alarm. Gallery director Vera Okonkwo reports a theft; curator Lina Morales and security chief James Holt give accounts that do not align.",
        "initial_observable_facts": [
            "The featured painting Midnight Verdict is missing from its wall mount in the main hall.",
            "Head of security James Holt claims the piece was secured in the vault until the 2100 alarm.",
            "Curator Lina Morales says she noticed the empty wall during her podium remarks around 2055.",
            "Collector Otto Weiss photographed activity near the painting shortly before the alarm.",
        ],
        "target_playtime_minutes": 120,
        "in_world_duration": "one opening night (approximately three in-world hours)",
        "tone": "urban, polished, quietly tense",
        "difficulty": "standard",
        "location_scale": "single urban gallery with five primary locations",
        "content_boundaries": "no graphic violence; no supernatural elements; insurance fraud and witness contradiction themes; no sexual content",
        "required_themes": [
            "fair-play mystery",
            "witness and NPC contradiction",
            "alibis and sightlines",
            "meaningful time pressure",
            "one perfect ending and several imperfect endings",
        ],
        "forbidden_themes": [
            "supernatural explanations",
            "theft-primary plots",
            "magic or occult resolution",
            "direct narrator solution delivery",
        ],
        "deadline_or_constraint": "Carrier claim filing deadline at 2300; witnesses dispersing after midnight",
        "author_notes": "Codename: The Gallery Verdict. Culprit NPC-VERA staged removal for insurance fraud after private sale. Emphasis on contradictory testimony, alibis, and sightlines — not burglary mechanics.",
    }


def _fixed_truth() -> dict:
    facts = [
        ("FACT-001", "Featured painting Midnight Verdict hung in the main hall until opening night"),
        ("FACT-002", "Gallery director Vera Okonkwo completed a private sale of the painting one week before opening"),
        ("FACT-003", "Vera Okonkwo staged crate removal disguised as loan return during the opening at 2042"),
        ("FACT-004", "James Holt authorized crate movement believing it was a scheduled loan return"),
        ("FACT-005", "The painting was not in the vault after 2030, contradicting James Holt's vault claim"),
        ("FACT-006", "Lina Morales was on the podium from 2035 to 2100, contradicting James Holt's claim she was in the vault"),
        ("FACT-007", "Otto Weiss's phone photo metadata places Vera Okonkwo at the crate at 2043"),
        ("FACT-008", "The insurance rider lists an inflated appraisal above the private sale price"),
        ("FACT-009", "The crate shipping label bears Vera Okonkwo's signature timestamped 2042"),
        ("FACT-010", "A security camera gap was manually disabled from the office terminal at 2038"),
        ("FACT-011", "A private sale contract for Midnight Verdict is dated one week before opening"),
        ("FACT-012", "The 2100 alarm triggered when the empty frame was detected, timing the staged discovery"),
        ("FACT-013", "Vera Okonkwo's office badge log shows she left her office at 2040, contradicting her alibi"),
        ("FACT-014", "The crate departed via service elevator to off-site storage registered to the gallery"),
    ]
    immutable = [{"fact_id": fid, "statement": stmt} for fid, stmt in facts]

    events = [
        ("EVT-001", "2026-03-14T20:00:00", "Night 1", "LOC-MAIN-HALL", "Opening reception begins; painting on display", ["NPC-LINA", "NPC-OTTO"], [], ["FACT-001"]),
        ("EVT-002", "2026-03-14T20:30:00", "Night 1", "LOC-OFFICE", "Vera Okonkwo reviews insurance rider and private sale file", ["NPC-VERA"], [], ["FACT-002", "FACT-008", "FACT-011"]),
        ("EVT-003", "2026-03-14T20:35:00", "Night 1", "LOC-MAIN-HALL", "Lina Morales takes the podium for artist remarks", ["NPC-LINA"], ["EVT-001"], ["FACT-006"]),
        ("EVT-004", "2026-03-14T20:38:00", "Night 1", "LOC-OFFICE", "Vera disables hall camera segment from office terminal", ["NPC-VERA"], ["EVT-002"], ["FACT-010"]),
        ("EVT-005", "2026-03-14T20:40:00", "Night 1", "LOC-OFFICE", "Vera leaves office toward service corridor", ["NPC-VERA"], ["EVT-004"], ["FACT-013"]),
        ("EVT-006", "2026-03-14T20:42:00", "Night 1", "LOC-MAIN-HALL", "Vera signs crate label; painting crated as loan return", ["NPC-VERA", "NPC-JAMES"], ["EVT-005"], ["FACT-003", "FACT-009"]),
        ("EVT-007", "2026-03-14T20:43:00", "Night 1", "LOC-MAIN-HALL", "Otto Weiss photographs Vera at the crate", ["NPC-OTTO", "NPC-VERA"], ["EVT-006"], ["FACT-007"]),
        ("EVT-008", "2026-03-14T20:45:00", "Night 1", "LOC-VAULT", "James logs false vault transfer in security tablet", ["NPC-JAMES"], ["EVT-006"], ["FACT-004", "FACT-005"]),
        ("EVT-009", "2026-03-14T21:00:00", "Night 1", "LOC-MAIN-HALL", "Empty frame triggers gallery alarm", [], ["EVT-006"], ["FACT-012"]),
        ("EVT-010", "2026-03-14T21:15:00", "Night 1", "LOC-LOBBY", "Insurance adjuster arrives on scene", ["PC-ADJUSTER"], ["EVT-009"], []),
        ("EVT-011", "2026-03-14T21:30:00", "Night 1", "LOC-OFFICE", "Security footage sync completes on adjuster tablet", [], ["EVT-010"], []),
        ("EVT-012", "2026-03-14T22:00:00", "Night 1", "LOC-TERRACE", "Otto shares phone photo with adjuster", ["NPC-OTTO"], ["EVT-010"], ["FACT-007"]),
        ("EVT-013", "2026-03-14T23:00:00", "Night 1", "LOC-OFFICE", "Carrier claim filing deadline", [], ["EVT-010"], []),
    ]

    return {
        "culprit_id": "NPC-VERA",
        "motive": "Collect insurance payout after already completing a private sale of Midnight Verdict",
        "method": "Crate removal disguised as loan return during opening chaos, with coached contradictory witness accounts",
        "opportunity": "Gallery director authority, vault codes, and ability to disable camera segments",
        "immutable_facts": immutable,
        "causal_timeline": {
            "clock_start": "2026-03-14T20:00:00",
            "events": [
                {
                    "event_id": eid,
                    "timestamp": ts,
                    "day_label": day,
                    "location_id": loc,
                    "description": desc,
                    "participants": parts,
                    "causes": causes,
                    "reveals_facts": reveals,
                    "effects": [],
                }
                for eid, ts, day, loc, desc, parts, causes, reveals in events
            ],
        },
        "world_state_timeline": {
            "snapshots": [
                {
                    "at_event_id": "EVT-006",
                    "people_locations": {"NPC-VERA": "LOC-MAIN-HALL", "NPC-JAMES": "LOC-MAIN-HALL"},
                    "object_states": {"OBJ-PAINTING": "crated"},
                    "access_states": {"LOC-MAIN-HALL": "crowded"},
                    "evidence_conditions": {},
                },
                {
                    "at_event_id": "EVT-010",
                    "people_locations": {"PC-ADJUSTER": "LOC-LOBBY"},
                    "object_states": {"OBJ-CRATE-LABEL": "archived"},
                    "access_states": {"LOC-OFFICE": "open"},
                    "evidence_conditions": {},
                },
                {
                    "at_event_id": "EVT-011",
                    "people_locations": {},
                    "object_states": {"OBJ-CAMERA-LOG": "sync_complete"},
                    "access_states": {"LOC-OFFICE": "records_available"},
                    "evidence_conditions": {},
                },
            ]
        },
        "npc_knowledge": {
            "npcs": [
                {
                    "npc_id": "NPC-VERA",
                    "knows": ["FACT-002", "FACT-003", "FACT-008", "FACT-010", "FACT-011", "FACT-013"],
                    "believes_incorrectly": [],
                    "witnessed_events": ["EVT-002", "EVT-004", "EVT-005", "EVT-006"],
                    "hides": ["FACT-002", "FACT-003", "FACT-010", "FACT-011", "FACT-013"],
                    "behavior_rationale": "Conceals private sale and staged removal to preserve insurance claim",
                },
                {
                    "npc_id": "NPC-JAMES",
                    "knows": ["FACT-004", "FACT-005"],
                    "believes_incorrectly": [
                        {
                            "belief_fact_id": "FACT-005",
                            "actual_fact_id": "FACT-003",
                            "cause": "Logged vault transfer per director's instruction without verifying contents",
                        }
                    ],
                    "witnessed_events": ["EVT-006", "EVT-008"],
                    "hides": [],
                    "behavior_rationale": "Truthful about authorization but wrong about vault timeline",
                },
                {
                    "npc_id": "NPC-LINA",
                    "knows": ["FACT-006", "FACT-012"],
                    "believes_incorrectly": [],
                    "witnessed_events": ["EVT-001", "EVT-003", "EVT-009"],
                    "hides": [],
                    "behavior_rationale": "Truthful curator whose podium alibi contradicts James",
                },
                {
                    "npc_id": "NPC-OTTO",
                    "knows": ["FACT-007"],
                    "believes_incorrectly": [],
                    "witnessed_events": ["EVT-007", "EVT-012"],
                    "hides": [],
                    "behavior_rationale": "Cooperative insured collector with timestamped photo evidence",
                },
            ]
        },
        "evidence_provenance": {
            "evidence": [
                {
                    "evidence_id": "EVD-SECURITY-TABLET",
                    "source_event_id": "EVT-008",
                    "type": "document",
                    "description": "Security tablet vault transfer log",
                    "establishes_fact_ids": ["FACT-004", "FACT-005"],
                    "misleading": True,
                    "misleading_cause": "Records vault transfer that did not match physical movement",
                },
                {
                    "evidence_id": "EVD-CRATE-LABEL",
                    "source_event_id": "EVT-006",
                    "type": "physical",
                    "description": "Crate shipping label with director signature",
                    "establishes_fact_ids": ["FACT-003", "FACT-009"],
                    "misleading": False,
                    "misleading_cause": None,
                },
                {
                    "evidence_id": "EVD-CAMERA-LOG",
                    "source_event_id": "EVT-004",
                    "type": "document",
                    "description": "Security camera disable audit log",
                    "establishes_fact_ids": ["FACT-010", "FACT-013"],
                    "misleading": False,
                    "misleading_cause": None,
                },
                {
                    "evidence_id": "EVD-INSURANCE-RIDER",
                    "source_event_id": "EVT-002",
                    "type": "document",
                    "description": "Inflated insurance appraisal rider",
                    "establishes_fact_ids": ["FACT-008"],
                    "misleading": False,
                    "misleading_cause": None,
                },
                {
                    "evidence_id": "EVD-PRIVATE-SALE",
                    "source_event_id": "EVT-002",
                    "type": "document",
                    "description": "Private sale contract dated before opening",
                    "establishes_fact_ids": ["FACT-002", "FACT-011"],
                    "misleading": False,
                    "misleading_cause": None,
                },
                {
                    "evidence_id": "EVD-OTTO-PHOTO",
                    "source_event_id": "EVT-007",
                    "type": "document",
                    "description": "Phone photo with embedded metadata",
                    "establishes_fact_ids": ["FACT-007"],
                    "misleading": False,
                    "misleading_cause": None,
                },
            ]
        },
        "observable_information": {
            "observations": [
                {
                    "observation_id": "OBS-VAULT-LOG",
                    "learnable_fact_id": "FACT-005",
                    "source_evidence_id": "EVD-SECURITY-TABLET",
                    "requires": {"action": "review", "location_id": "LOC-VAULT"},
                    "hidden_if_not_met": True,
                },
                {
                    "observation_id": "OBS-CRATE",
                    "learnable_fact_id": "FACT-009",
                    "source_evidence_id": "EVD-CRATE-LABEL",
                    "requires": {"action": "inspect", "location_id": "LOC-MAIN-HALL", "check_id": "CHK-SIGHTLINE"},
                    "hidden_if_not_met": True,
                },
                {
                    "observation_id": "OBS-CAMERA",
                    "learnable_fact_id": "FACT-010",
                    "source_evidence_id": "EVD-CAMERA-LOG",
                    "requires": {"action": "review", "location_id": "LOC-OFFICE", "check_id": "CHK-CAMERA"},
                    "hidden_if_not_met": True,
                },
            ]
        },
        "conclusion_requirements": {
            "questions": [
                {
                    "question_id": "Q-CULPRIT",
                    "answer_entity_id": "NPC-VERA",
                    "required_fact_ids": ["FACT-002", "FACT-003", "FACT-009", "FACT-010", "FACT-013"],
                },
                {
                    "question_id": "Q-METHOD",
                    "answer_entity_id": "METHOD-STAGED-REMOVAL",
                    "required_fact_ids": ["FACT-003", "FACT-009", "FACT-012"],
                },
            ]
        },
        "ending_claims": [
            {"ending_id": "END-PERFECT", "asserted_fact_ids": ["FACT-002", "FACT-003", "FACT-009", "FACT-010"]},
            {"ending_id": "END-TIMEOUT", "asserted_fact_ids": []},
        ],
    }


def _locations() -> list:
    return [
        {
            "location_id": "LOC-LOBBY",
            "public_name": "Gallery lobby",
            "start_location": True,
            "hub_unit_id": "UNIT-LOBBY-BASE",
            "parent_location_id": None,
            "location_type": "gallery_lobby",
            "description_source": "DESC-LOBBY",
            "default_attributes": {"access": "open"},
        },
        {
            "location_id": "LOC-MAIN-HALL",
            "public_name": "Main exhibition hall",
            "hub_unit_id": "UNIT-MAIN-HALL-BASE",
            "parent_location_id": "LOC-LOBBY",
            "location_type": "exhibition_hall",
            "description_source": "DESC-MAIN-HALL",
            "default_attributes": {"access": "open"},
        },
        {
            "location_id": "LOC-VAULT",
            "public_name": "Secure vault",
            "hub_unit_id": "UNIT-VAULT-BASE",
            "parent_location_id": "LOC-LOBBY",
            "location_type": "secure_storage",
            "description_source": "DESC-VAULT",
            "default_attributes": {"access": "restricted"},
        },
        {
            "location_id": "LOC-OFFICE",
            "public_name": "Director's office",
            "hub_unit_id": "UNIT-OFFICE-BASE",
            "parent_location_id": "LOC-LOBBY",
            "location_type": "office",
            "description_source": "DESC-OFFICE",
            "default_attributes": {"access": "open"},
        },
        {
            "location_id": "LOC-TERRACE",
            "public_name": "Rooftop terrace",
            "hub_unit_id": "UNIT-TERRACE-BASE",
            "parent_location_id": "LOC-LOBBY",
            "location_type": "terrace",
            "description_source": "DESC-TERRACE",
            "default_attributes": {"access": "open"},
        },
    ]


def _location_states() -> list:
    return [
        {
            "state_id": "LOC-LOBBY:default",
            "location_id": "LOC-LOBBY",
            "variant_label": "investigation_start",
            "attributes": {"access": "open", "crowd_level": "dispersing"},
            "cause": {"type": "timeline_event", "ref": "EVT-010"},
        },
        {
            "state_id": "LOC-OFFICE:camera_sync",
            "location_id": "LOC-OFFICE",
            "variant_label": "camera_synced",
            "attributes": {"camera_sync": "complete"},
            "cause": {"type": "timeline_event", "ref": "EVT-011"},
        },
    ]


def _features() -> list:
    return [
        {
            "feature_id": "FEAT-EMPTY-FRAME",
            "location_id": "LOC-MAIN-HALL",
            "label": "Empty wall mount for Midnight Verdict",
            "object_ref": "OBJ-PAINTING-FRAME",
        },
        {
            "feature_id": "FEAT-CRATE-LABEL",
            "location_id": "LOC-MAIN-HALL",
            "label": "Archived crate shipping label",
            "object_ref": "OBJ-CRATE-LABEL",
        },
    ]


def _navigation() -> list:
    pairs = [
        ("NAV-LOBBY-MAIN", "LOC-LOBBY", "LOC-MAIN-HALL", "Enter the main exhibition hall", 2),
        ("NAV-LOBBY-VAULT", "LOC-LOBBY", "LOC-VAULT", "Descend to the secure vault", 3),
        ("NAV-LOBBY-OFFICE", "LOC-LOBBY", "LOC-OFFICE", "Take the corridor to the director's office", 2),
        ("NAV-LOBBY-TERRACE", "LOC-LOBBY", "LOC-TERRACE", "Ride the elevator to the rooftop terrace", 3),
        ("NAV-MAIN-LOBBY", "LOC-MAIN-HALL", "LOC-LOBBY", "Return to the lobby", 2),
        ("NAV-VAULT-LOBBY", "LOC-VAULT", "LOC-LOBBY", "Return to the lobby", 3),
        ("NAV-OFFICE-LOBBY", "LOC-OFFICE", "LOC-LOBBY", "Return to the lobby", 2),
        ("NAV-TERRACE-LOBBY", "LOC-TERRACE", "LOC-LOBBY", "Return to the lobby", 3),
    ]
    return [
        {
            "edge_id": eid,
            "from_location_id": fr,
            "to_location_id": to,
            "direction_label": label,
            "time_cost_minutes": cost,
        }
        for eid, fr, to, label, cost in pairs
    ]


def _npcs() -> list:
    return [
        {
            "npc_id": "NPC-VERA",
            "public_name": "Vera Okonkwo",
            "role": "Gallery director",
            "relationships": [{"target_npc_id": "NPC-LINA", "relationship_type": "professional"}],
        },
        {
            "npc_id": "NPC-JAMES",
            "public_name": "James Holt",
            "role": "Head of security",
            "relationships": [{"target_npc_id": "NPC-VERA", "relationship_type": "professional"}],
        },
        {
            "npc_id": "NPC-LINA",
            "public_name": "Lina Morales",
            "role": "Lead curator",
            "relationships": [{"target_npc_id": "NPC-VERA", "relationship_type": "professional"}],
        },
        {
            "npc_id": "NPC-OTTO",
            "public_name": "Otto Weiss",
            "role": "Insured collector",
            "relationships": [{"target_npc_id": "NPC-VERA", "relationship_type": "patron"}],
        },
    ]


def _objects() -> list:
    return [
        {
            "object_id": "OBJ-SECURITY-TABLET",
            "public_name": "Security tablet log",
            "location_id": "LOC-VAULT",
            "interaction_type": "terminal",
        },
        {
            "object_id": "OBJ-CAMERA-LOG",
            "public_name": "Camera audit terminal",
            "location_id": "LOC-OFFICE",
            "interaction_type": "terminal",
        },
        {
            "object_id": "OBJ-INSURANCE-RIDER",
            "public_name": "Insurance rider binder",
            "location_id": "LOC-OFFICE",
            "interaction_type": "document",
        },
        {
            "object_id": "OBJ-CRATE-LABEL",
            "public_name": "Crate shipping label",
            "location_id": "LOC-MAIN-HALL",
            "interaction_type": "physical",
        },
        {
            "object_id": "OBJ-PAINTING-FRAME",
            "public_name": "Empty wall mount",
            "location_id": "LOC-MAIN-HALL",
            "interaction_type": "physical",
        },
        {
            "object_id": "OBJ-PRIVATE-SALE",
            "public_name": "Private sale contract file",
            "location_id": "LOC-OFFICE",
            "interaction_type": "document",
        },
    ]


def _knowledge() -> dict:
    facts = _fixed_truth()["immutable_facts"]
    knowledge_items = [
        ("KNOW-OPEN-01", "Featured painting Midnight Verdict is missing after opening alarm", "briefing", "A", []),
        ("KNOW-OPEN-02", "Witness accounts disagree about who was where when the piece vanished", "briefing", "A", []),
        ("KNOW-OPEN-03", "Security chief James Holt claims the painting was vault-secured until 2100", "briefing", "A", []),
        ("KNOW-OPEN-04", "Carrier claim filing deadline is 2300 tonight", "briefing", "A", []),
        ("KNOW-VAULT-LOG", "Security tablet shows vault transfer logged at 2045", "document", "B", ["FACT-004", "FACT-005"]),
        ("KNOW-CRATE-LABEL", "Crate label signed by Vera Okonkwo at 2042 as loan return", "physical", "B", ["FACT-003", "FACT-009"]),
        ("KNOW-CAMERA-GAP", "Hall camera segment disabled from office terminal at 2038", "document", "B", ["FACT-010", "FACT-013"]),
        ("KNOW-INSURANCE-RIDER", "Insurance rider lists appraisal above recent market comps", "document", "B", ["FACT-008"]),
        ("KNOW-PRIVATE-SALE", "Private sale contract for Midnight Verdict predates opening", "document", "B", ["FACT-002", "FACT-011"]),
        ("KNOW-LINA-PODIUM", "Lina Morales was on podium from 2035 to 2100", "testimony", "B", ["FACT-006"]),
        ("KNOW-JAMES-VAULT", "James Holt insists painting was in vault until alarm", "testimony", "B", ["FACT-005"]),
        ("KNOW-OTTO-PHOTO", "Otto Weiss photo metadata places Vera at crate at 2043", "testimony", "B", ["FACT-007"]),
        ("KNOW-VERA-OFFICE", "Vera Okonkwo claims she never left her office after 2030", "testimony", "B", []),
        ("KNOW-JAMES-AUTH", "James Holt admits authorizing crate movement on director's order", "testimony", "B", ["FACT-004"]),
        ("KNOW-SIGHTLINE", "Podium sightline to wall mount was unobstructed during remarks", "physical", "B", ["FACT-006", "FACT-012"]),
        ("KNOW-CONTRADICTION-JAMES-LINA", "James and Lina cannot both be correct about vault versus podium", "inference", "C", []),
        ("KNOW-VERA-STAGING", "Evidence supports staged removal by gallery director", "inference", "C", []),
        ("KNOW-PERFECT-VERDICT", "Full reconstruction: private sale, staged crate removal, false vault log", "inference", "C", []),
    ]
    return {
        "facts": [{"fact_id": f["fact_id"], "statement": f["statement"], "immutable": True} for f in facts],
        "observations": [
            {
                "observation_id": "OBS-VAULT-DISCREPANCY",
                "description": "Vault log inconsistent with hall movement",
                "establishes_knowledge_id": "KNOW-VAULT-LOG",
            },
            {
                "observation_id": "OBS-SIGHTLINE-GAP",
                "description": "Podium view shows when wall went empty",
                "establishes_knowledge_id": "KNOW-SIGHTLINE",
            },
            {
                "observation_id": "OBS-CAMERA-DISABLE",
                "description": "Camera gap timed before crate movement",
                "establishes_knowledge_id": "KNOW-CAMERA-GAP",
            },
        ],
        "evidence": [
            {"evidence_id": "EVD-SECURITY-TABLET", "name": "Security tablet log", "location_id": "LOC-VAULT"},
            {"evidence_id": "EVD-CRATE-LABEL", "name": "Crate shipping label", "location_id": "LOC-MAIN-HALL"},
            {"evidence_id": "EVD-CAMERA-LOG", "name": "Camera audit log", "location_id": "LOC-OFFICE"},
            {"evidence_id": "EVD-INSURANCE-RIDER", "name": "Insurance rider", "location_id": "LOC-OFFICE"},
            {"evidence_id": "EVD-PRIVATE-SALE", "name": "Private sale contract", "location_id": "LOC-OFFICE"},
            {"evidence_id": "EVD-OTTO-PHOTO", "name": "Otto Weiss phone photo", "location_id": "LOC-TERRACE"},
        ],
        "testimony": [
            {"testimony_id": "TEST-LINA-PODIUM", "npc_id": "NPC-LINA", "summary": "On podium during disappearance window", "grants_knowledge_id": "KNOW-LINA-PODIUM"},
            {"testimony_id": "TEST-JAMES-VAULT", "npc_id": "NPC-JAMES", "summary": "Painting vault-secured until alarm", "grants_knowledge_id": "KNOW-JAMES-VAULT"},
            {"testimony_id": "TEST-OTTO-PHOTO", "npc_id": "NPC-OTTO", "summary": "Photo of Vera at crate", "grants_knowledge_id": "KNOW-OTTO-PHOTO"},
            {"testimony_id": "TEST-VERA-OFFICE", "npc_id": "NPC-VERA", "summary": "Office alibi after 2030", "grants_knowledge_id": "KNOW-VERA-OFFICE"},
        ],
        "knowledge_items": [
            {
                "knowledge_id": kid,
                "summary": summary,
                "source_type": stype,
                "tier": tier,
                **({"establishes_fact_ids": fids} if fids else {}),
            }
            for kid, summary, stype, tier, fids in knowledge_items
        ],
        "hypotheses": [
            {
                "hypothesis_id": "HYP-WITNESS-CONFLICT",
                "statement": "Witness accounts contradict on locations during the disappearance window",
                "related_knowledge_ids": ["KNOW-LINA-PODIUM", "KNOW-JAMES-VAULT", "KNOW-VERA-OFFICE", "KNOW-VAULT-LOG", "KNOW-SIGHTLINE"],
                "yields_knowledge_id": "KNOW-CONTRADICTION-JAMES-LINA",
            },
            {
                "hypothesis_id": "HYP-STAGING",
                "statement": "Removal was staged rather than opportunistic theft",
                "related_knowledge_ids": ["KNOW-CRATE-LABEL", "KNOW-CAMERA-GAP", "KNOW-PRIVATE-SALE", "KNOW-SIGHTLINE"],
                "yields_knowledge_id": "KNOW-VERA-STAGING",
            },
            {
                "hypothesis_id": "HYP-VERA-FRAUD",
                "statement": "Gallery director orchestrated removal for insurance fraud",
                "related_knowledge_ids": ["KNOW-INSURANCE-RIDER", "KNOW-PRIVATE-SALE", "KNOW-OTTO-PHOTO", "KNOW-VAULT-LOG"],
                "yields_knowledge_id": "KNOW-VERA-STAGING",
            },
            {
                "hypothesis_id": "HYP-PERFECT-VERDICT",
                "statement": "Full reconstruction resolves all contradictions",
                "related_knowledge_ids": ["KNOW-CONTRADICTION-JAMES-LINA", "KNOW-VERA-STAGING", "KNOW-PERFECT-VERDICT"],
                "yields_knowledge_id": "KNOW-PERFECT-VERDICT",
            },
        ],
        "conclusions": [
            {"conclusion_id": "CONC-WHO", "question": "Who staged the disappearance?", "correct_answer": "NPC-VERA"},
            {"conclusion_id": "CONC-WHAT", "question": "What happened to Midnight Verdict?", "correct_answer": "Crate removal disguised as loan return after prior private sale"},
            {"conclusion_id": "CONC-HOW", "question": "How were witnesses misled?", "correct_answer": "False vault log and coached contradictory alibis"},
            {"conclusion_id": "CONC-WHEN", "question": "When was the painting removed?", "correct_answer": "Approximately 2042 during opening remarks"},
        ],
        "proofs": [
            {
                "proof_id": "PROOF-WHO",
                "conclusion_id": "CONC-WHO",
                "required_knowledge_ids": [
                    "KNOW-PERFECT-VERDICT",
                    "KNOW-VERA-STAGING",
                    "KNOW-CONTRADICTION-JAMES-LINA",
                ],
            },
            {
                "proof_id": "PROOF-WHAT",
                "conclusion_id": "CONC-WHAT",
                "required_knowledge_ids": [
                    "KNOW-PRIVATE-SALE",
                    "KNOW-CRATE-LABEL",
                    "KNOW-VERA-STAGING",
                ],
            },
            {
                "proof_id": "PROOF-HOW",
                "conclusion_id": "CONC-HOW",
                "required_knowledge_ids": [
                    "KNOW-JAMES-VAULT",
                    "KNOW-JAMES-AUTH",
                    "KNOW-VERA-OFFICE",
                ],
            },
            {
                "proof_id": "PROOF-WHEN",
                "conclusion_id": "CONC-WHEN",
                "required_knowledge_ids": [
                    "KNOW-SIGHTLINE",
                    "KNOW-OTTO-PHOTO",
                    "KNOW-CAMERA-GAP",
                ],
            },
        ],
        "relationships": [
            {
                "relationship_id": "REL-VERA-JAMES",
                "from_entity": "NPC-VERA",
                "to_entity": "NPC-JAMES",
                "relationship_type": "director_to_security",
            }
        ],
    }


def _conversations() -> list:
    def conv(cid, npc, hub, topics):
        return {
            "conversation_id": cid,
            "npc_id": npc,
            "hub_unit_id": hub,
            "topics": topics,
        }

    def topic(tid, label, unit, know, minutes=2):
        return {
            "topic_id": tid,
            "player_label": label,
            "response_unit_id": unit,
            "grants_knowledge_id": know,
            "time_cost_minutes": minutes,
        }

    return [
        conv(
            "CONV-VERA",
            "NPC-VERA",
            "UNIT-NPC-VERA-HUB",
            [
                topic("TOPIC-VERA-ALIBI", "Ask about her whereabouts after 2030.", "UNIT-TOPIC-VERA-ALIBI", "KNOW-VERA-OFFICE"),
                topic("TOPIC-VERA-CLAIM", "Ask why she reported a theft.", "UNIT-TOPIC-VERA-CLAIM", "KNOW-OPEN-01"),
                topic("TOPIC-VERA-INSURANCE", "Ask about the insurance appraisal.", "UNIT-TOPIC-VERA-INSURANCE", "KNOW-INSURANCE-RIDER"),
            ],
        ),
        conv(
            "CONV-JAMES",
            "NPC-JAMES",
            "UNIT-NPC-JAMES-HUB",
            [
                topic("TOPIC-JAMES-VAULT", "Ask whether the painting was in the vault.", "UNIT-TOPIC-JAMES-VAULT", "KNOW-JAMES-VAULT"),
                topic("TOPIC-JAMES-CRATE", "Ask about crate movement during the opening.", "UNIT-TOPIC-JAMES-CRATE", "KNOW-JAMES-AUTH"),
                topic("TOPIC-JAMES-LINA", "Ask where Lina Morales was at 2045.", "UNIT-TOPIC-JAMES-LINA", "KNOW-JAMES-VAULT"),
            ],
        ),
        conv(
            "CONV-LINA",
            "NPC-LINA",
            "UNIT-NPC-LINA-HUB",
            [
                topic("TOPIC-LINA-PODIUM", "Ask where she was during the disappearance window.", "UNIT-TOPIC-LINA-PODIUM", "KNOW-LINA-PODIUM"),
                topic("TOPIC-LINA-WALL", "Ask when she first noticed the empty wall.", "UNIT-TOPIC-LINA-WALL", "KNOW-LINA-PODIUM"),
                topic("TOPIC-LINA-JAMES", "Ask whether James could see the vault from the hall.", "UNIT-TOPIC-LINA-JAMES", "KNOW-LINA-PODIUM"),
            ],
        ),
        conv(
            "CONV-OTTO",
            "NPC-OTTO",
            "UNIT-NPC-OTTO-HUB",
            [
                topic("TOPIC-OTTO-PHOTO", "Ask about photos taken near the painting.", "UNIT-TOPIC-OTTO-PHOTO", "KNOW-OTTO-PHOTO"),
                topic("TOPIC-OTTO-SIGHTLINE", "Ask what he saw from the patron rail.", "UNIT-TOPIC-OTTO-SIGHTLINE", "KNOW-OTTO-PHOTO"),
                topic("TOPIC-OTTO-INSURED", "Ask about his insurance interest in the piece.", "UNIT-TOPIC-OTTO-INSURED", "KNOW-INSURANCE-RIDER"),
            ],
        ),
    ]


def _object_actions() -> list:
    return [
        {
            "action_id": "ACT-SECURITY-TABLET",
            "object_id": "OBJ-SECURITY-TABLET",
            "menu_unit_id": "UNIT-OBJ-TABLET-MENU",
            "result_unit_id": "UNIT-OBJ-TABLET-RESULT",
            "grants_knowledge_ids": ["KNOW-VAULT-LOG"],
        },
        {
            "action_id": "ACT-CAMERA-LOG",
            "object_id": "OBJ-CAMERA-LOG",
            "menu_unit_id": "UNIT-OBJ-CAMERA-MENU",
            "result_unit_id": "UNIT-OBJ-CAMERA-RESULT",
            "grants_knowledge_ids": ["KNOW-CAMERA-GAP"],
        },
        {
            "action_id": "ACT-INSURANCE-RIDER",
            "object_id": "OBJ-INSURANCE-RIDER",
            "menu_unit_id": "UNIT-OBJ-RIDER-MENU",
            "result_unit_id": "UNIT-OBJ-RIDER-RESULT",
            "grants_knowledge_ids": ["KNOW-INSURANCE-RIDER"],
        },
        {
            "action_id": "ACT-CRATE-LABEL",
            "object_id": "OBJ-CRATE-LABEL",
            "menu_unit_id": "UNIT-CHK-SIGHTLINE-DECL",
            "check_id": "CHK-SIGHTLINE",
        },
        {
            "action_id": "ACT-PRIVATE-SALE",
            "object_id": "OBJ-PRIVATE-SALE",
            "menu_unit_id": "UNIT-OBJ-SALE-MENU",
            "result_unit_id": "UNIT-OBJ-SALE-RESULT",
            "grants_knowledge_ids": ["KNOW-PRIVATE-SALE"],
        },
    ]


def _checks() -> list:
    return [
        {
            "check_id": "CHK-SIGHTLINE",
            "declaration_unit_id": "UNIT-CHK-SIGHTLINE-DECL",
            "success_unit_id": "UNIT-SIGHTLINE-SUCCESS",
            "failure_unit_id": "UNIT-SIGHTLINE-FAIL",
            "capability": "perception",
            "capability_category": "perception_observation",
            "modifier_source_id": "MOD-PERCEPTION",
            "dc": 12,
            "parent_action_id": "ACT-CRATE-LABEL",
            "success_grants_knowledge_ids": ["KNOW-SIGHTLINE", "KNOW-CRATE-LABEL"],
            "player_action_label": "Reconstruct podium sightlines to the wall mount.",
        },
        {
            "check_id": "CHK-CRATE",
            "declaration_unit_id": "UNIT-CHK-CRATE-DECL",
            "success_unit_id": "UNIT-CRATE-SUCCESS",
            "failure_unit_id": "UNIT-CRATE-FAIL",
            "capability": "reasoning",
            "capability_category": "reasoning_analysis",
            "modifier_source_id": "MOD-REASONING",
            "dc": 11,
            "parent_action_id": "ACT-SECURITY-TABLET",
            "success_grants_knowledge_ids": ["KNOW-VAULT-LOG"],
            "player_action_label": "Compare vault log timestamps with witness accounts.",
        },
        {
            "check_id": "CHK-CAMERA",
            "declaration_unit_id": "UNIT-CHK-CAMERA-DECL",
            "success_unit_id": "UNIT-CAMERA-SUCCESS",
            "failure_unit_id": "UNIT-CAMERA-FAIL",
            "capability": "technical",
            "capability_category": "technical_systems",
            "modifier_source_id": "MOD-TECHNICAL",
            "dc": 12,
            "parent_action_id": "ACT-CAMERA-LOG",
            "success_grants_knowledge_ids": ["KNOW-CAMERA-GAP"],
            "player_action_label": "Correlate camera disable log with badge records.",
        },
    ]


def _flow() -> dict:
    return {
        "placeholder_resolution": {},
        "state_model": {
            "flags": [
                "camera_sync_complete",
                "rider_reviewed",
                "tablet_reviewed",
                "camera_reviewed",
                "sightline_examined",
                "sale_reviewed",
                "ready_to_accuse",
                "accusation_complete",
                "inference_witness_resolved",
                "inference_staging_resolved",
                "inference_vera_resolved",
                "inference_perfect_resolved",
                "check_sightline_failed",
                "check_crate_failed",
                "check_camera_failed",
            ],
            "counters": ["investigation_phase"],
            "initial_state": {
                "camera_sync_complete": False,
                "rider_reviewed": False,
                "tablet_reviewed": False,
                "camera_reviewed": False,
                "sightline_examined": False,
                "sale_reviewed": False,
                "ready_to_accuse": False,
                "accusation_complete": False,
                "inference_witness_resolved": False,
                "inference_staging_resolved": False,
                "inference_vera_resolved": False,
                "inference_perfect_resolved": False,
                "check_sightline_failed": False,
                "check_crate_failed": False,
                "check_camera_failed": False,
                "investigation_phase": 0,
            },
        },
        "time_model": {
            "clocks": ["T_ARRIVAL", "T_CAMERA_SYNC", "T_OTTO_PHOTO", "T_DEADLINE"],
            "clock_event_map": {
                "T_ARRIVAL": "EVT-010",
                "T_CAMERA_SYNC": "EVT-011",
                "T_OTTO_PHOTO": "EVT-012",
                "T_DEADLINE": "EVT-013",
            },
            "deadline_clock": "T_DEADLINE",
            "scene_time_cost_default_minutes": 5,
            "no_earlier_time_travel": True,
        },
        "scene_chains": [
            {
                "chain_id": "CHAIN-OPENING",
                "active_from_clock": "T_ARRIVAL",
                "active_until_clock": "T_OTTO_PHOTO",
                "steps": [
                    {
                        "step_id": "SC-LOBBY-ARRIVAL",
                        "scene_unit_id": "SC-LOBBY-ARRIVAL",
                        "player_label": "Receive arrival briefing.",
                        "location_id": "LOC-LOBBY",
                    },
                    {
                        "step_id": "SC-HALL-ALARM",
                        "scene_unit_id": "SC-HALL-ALARM",
                        "player_label": "Survey the empty wall mount.",
                        "location_id": "LOC-MAIN-HALL",
                    },
                ],
            },
            {
                "chain_id": "CHAIN-RECORDS",
                "active_from_clock": "T_OTTO_PHOTO",
                "active_until_clock": "T_CAMERA_SYNC",
                "steps": [
                    {
                        "step_id": "SC-TERRACE-PHOTO",
                        "scene_unit_id": "SC-TERRACE-PHOTO",
                        "player_label": "Review Otto's timestamped photo.",
                        "location_id": "LOC-TERRACE",
                    },
                    {
                        "step_id": "SC-OFFICE-CAMERA",
                        "scene_unit_id": "SC-OFFICE-CAMERA",
                        "player_label": "Pull camera audit records.",
                        "location_id": "LOC-OFFICE",
                        "state_updates": {"camera_sync_complete": True},
                    },
                ],
            },
            {
                "chain_id": "CHAIN-FINAL",
                "active_from_clock": "T_CAMERA_SYNC",
                "active_until_clock": "T_DEADLINE",
                "steps": [
                    {
                        "step_id": "SC-VAULT-LOG",
                        "scene_unit_id": "SC-VAULT-LOG",
                        "player_label": "Compare vault logs with testimony.",
                        "location_id": "LOC-VAULT",
                    },
                    {
                        "step_id": "SC-HALL-SIGHTLINE",
                        "scene_unit_id": "SC-HALL-SIGHTLINE",
                        "player_label": "Walk the podium sightline.",
                        "location_id": "LOC-MAIN-HALL",
                        "state_updates": {"sightline_examined": True},
                    },
                    {
                        "step_id": "SC-ACCUSATION-PREP",
                        "scene_unit_id": "SC-ACCUSATION-PREP",
                        "player_label": "Prepare final claim determination.",
                        "location_id": "LOC-OFFICE",
                        "requires_state": {"ready_to_accuse": True},
                    },
                    {
                        "step_id": "SC-DEADLINE-WARN",
                        "scene_unit_id": "SC-DEADLINE-WARN",
                        "player_label": "Hear deadline warning.",
                        "location_id": "LOC-LOBBY",
                    },
                ],
            },
        ],
        "world_state_variants": [
            {
                "variant_id": "VAR-OFFICE-CAMERA",
                "base_scene_unit_id": "SC-OFFICE-CAMERA",
                "variants": [
                    {"when_state": {"flag": "camera_sync_complete", "value": True}, "scene_unit_id": "SC-OFFICE-CAMERA"},
                    {"when_state": {"flag": "camera_sync_complete", "value": False}, "scene_unit_id": "SC-OFFICE-CAMERA"},
                ],
            }
        ],
        "location_revisits": [
            {
                "location_id": "LOC-OFFICE",
                "revisit_rules": [
                    {
                        "rule_id": "REV-SALE",
                        "when_clock_at_least": "T_CAMERA_SYNC",
                        "unlocks_scene_unit_id": "SC-OFFICE-CAMERA",
                        "state_updates": {"sale_reviewed": True},
                    }
                ],
            },
            {
                "location_id": "LOC-MAIN-HALL",
                "revisit_rules": [
                    {
                        "rule_id": "REV-SIGHTLINE",
                        "when_knowledge_held": ["KNOW-LINA-PODIUM"],
                        "unlocks_scene_unit_id": "SC-HALL-SIGHTLINE",
                        "state_updates": {"sightline_examined": True},
                    }
                ],
            },
        ],
        "inference_flow_gates": [
            {
                "inference_id": "INF-WITNESS-CONFLICT",
                "hypothesis_id": "HYP-WITNESS-CONFLICT",
                "required_knowledge_ids": ["KNOW-LINA-PODIUM", "KNOW-JAMES-VAULT", "KNOW-VERA-OFFICE"],
                "success_state_updates": {"inference_witness_resolved": True},
                "failure_preserves_investigation": True,
                "recovery_routes": ["REC-VAULT-TABLET", "REC-LINA-PODIUM"],
            },
            {
                "inference_id": "INF-STAGING",
                "hypothesis_id": "HYP-STAGING",
                "required_knowledge_ids": ["KNOW-CRATE-LABEL", "KNOW-CAMERA-GAP", "KNOW-PRIVATE-SALE"],
                "success_state_updates": {"inference_staging_resolved": True},
                "failure_preserves_investigation": True,
                "recovery_routes": ["REC-OFFICE-CAMERA", "REC-HALL-CRATE"],
            },
            {
                "inference_id": "INF-VERA-FRAUD",
                "hypothesis_id": "HYP-VERA-FRAUD",
                "required_knowledge_ids": ["KNOW-INSURANCE-RIDER", "KNOW-PRIVATE-SALE", "KNOW-OTTO-PHOTO"],
                "success_state_updates": {"inference_vera_resolved": True, "ready_to_accuse": True},
                "failure_preserves_investigation": True,
                "recovery_routes": ["REC-OFFICE-RIDER", "REC-TERRACE-PHOTO"],
            },
            {
                "inference_id": "INF-PERFECT-VERDICT",
                "hypothesis_id": "HYP-PERFECT-VERDICT",
                "required_knowledge_ids": ["KNOW-CONTRADICTION-JAMES-LINA", "KNOW-VERA-STAGING", "KNOW-PERFECT-VERDICT"],
                "success_state_updates": {"inference_perfect_resolved": True},
                "failure_preserves_investigation": True,
                "recovery_routes": ["REC-OFFICE-CAMERA", "REC-HALL-CRATE"],
            },
        ],
        "recovery_routes": [
            {
                "route_id": "REC-OFFICE-CAMERA",
                "player_action_label": "Return to the camera audit terminal.",
                "destination_ref": "LOC-OFFICE",
                "action_ref": "ACT-CAMERA-LOG",
            },
            {
                "route_id": "REC-HALL-CRATE",
                "player_action_label": "Re-examine the crate shipping label.",
                "destination_ref": "LOC-MAIN-HALL",
                "action_ref": "ACT-CRATE-LABEL",
            },
            {
                "route_id": "REC-VAULT-TABLET",
                "player_action_label": "Re-read the security tablet log.",
                "destination_ref": "LOC-VAULT",
                "action_ref": "ACT-SECURITY-TABLET",
            },
            {
                "route_id": "REC-OFFICE-RIDER",
                "player_action_label": "Review the insurance rider again.",
                "destination_ref": "LOC-OFFICE",
                "action_ref": "ACT-INSURANCE-RIDER",
            },
            {
                "route_id": "REC-LINA-PODIUM",
                "player_action_label": "Return to Lina Morales for podium timing.",
                "destination_ref": "LOC-MAIN-HALL",
                "action_ref": "CONV-LINA",
            },
            {
                "route_id": "REC-TERRACE-PHOTO",
                "player_action_label": "Ask Otto Weiss about the photo again.",
                "destination_ref": "LOC-TERRACE",
                "action_ref": "CONV-OTTO",
            },
        ],
        "accusation_questionnaire": {
            "questionnaire_id": "ACC-GALLERY-VERDICT",
            "required_before_ending_eval": True,
            "multi_component": True,
            "questions": [
                {"question_id": "Q-WHO", "conclusion_id": "CONC-WHO", "answer_type": "npc_id", "player_label": "Who staged the disappearance?"},
                {"question_id": "Q-WHAT", "conclusion_id": "CONC-WHAT", "answer_type": "text", "player_label": "What happened to Midnight Verdict?"},
                {"question_id": "Q-HOW", "conclusion_id": "CONC-HOW", "answer_type": "text", "player_label": "How were witnesses misled?"},
                {"question_id": "Q-WHEN", "conclusion_id": "CONC-WHEN", "answer_type": "text", "player_label": "When was the painting removed?"},
            ],
            "accusation_complete_state_flag": "accusation_complete",
        },
        "deadline": {
            "enabled": True,
            "deadline_clock": "T_DEADLINE",
            "deadline_ending_id": "END-TIMEOUT",
            "blocks_accusation_after": True,
        },
        "endings": [
            {
                "ending_id": "END-PERFECT",
                "ending_type": "perfect",
                "priority": 100,
                "unit_id": "END-PERFECT",
                "trigger": {
                    "type": "state_driven",
                    "required_state": {"accusation_complete": True, "inference_perfect_resolved": True},
                    "required_accusation": {"Q-WHO": "NPC-VERA"},
                },
            },
            {
                "ending_id": "END-PARTIAL-CULPRIT",
                "ending_type": "partial",
                "priority": 50,
                "unit_id": "END-PARTIAL-CULPRIT",
                "trigger": {
                    "type": "state_driven",
                    "required_state": {"accusation_complete": True, "inference_vera_resolved": True},
                },
            },
            {
                "ending_id": "END-PARTIAL-WITNESS",
                "ending_type": "partial",
                "priority": 40,
                "unit_id": "END-PARTIAL-WITNESS",
                "trigger": {
                    "type": "state_driven",
                    "required_state": {"accusation_complete": True, "inference_witness_resolved": True},
                },
            },
            {
                "ending_id": "END-PARTIAL-WRONG",
                "ending_type": "partial",
                "priority": 30,
                "unit_id": "END-PARTIAL-WRONG",
                "trigger": {"type": "state_driven", "required_state": {"accusation_complete": True}, "wrong_accusation_allowed": True},
            },
            {
                "ending_id": "END-TIMEOUT",
                "ending_type": "timeout",
                "priority": 10,
                "unit_id": "END-TIMEOUT",
                "trigger": {"type": "deadline", "deadline_clock": "T_DEADLINE"},
            },
        ],
    }


def _player_units() -> dict:
    atmosphere = "Polished concrete, track lighting, and murmured patron conversations fill the space."
    units: list[dict] = []

    def hub(uid, title, loc, loc_id, choices, body=None):
        units.append(
            {
                "unit_id": uid,
                "title": title,
                "player_file": "LOCATIONS",
                "unit_kind": "location_hub",
                "linked_location_id": loc_id,
                "prose": {"body": body or f"You are at the {title.lower()}. {atmosphere}"},
                "choices": choices,
                "meta": {"location_id": loc_id, "time_cost_minutes": 0},
            }
        )

    hub(
        "UNIT-LOBBY-BASE",
        "Gallery lobby",
        "lobby",
        "LOC-LOBBY",
        [
            {"label": "Enter the main exhibition hall.", "destination_unit_id": "UNIT-MAIN-HALL-BASE"},
            {"label": "Descend to the secure vault.", "destination_unit_id": "UNIT-VAULT-BASE"},
            {"label": "Take the corridor to the director's office.", "destination_unit_id": "UNIT-OFFICE-BASE"},
            {"label": "Ride the elevator to the rooftop terrace.", "destination_unit_id": "UNIT-TERRACE-BASE"},
            {"label": "Speak with gallery director Vera Okonkwo.", "destination_unit_id": "UNIT-NPC-VERA-HUB"},
            {"label": "Speak with head of security James Holt.", "destination_unit_id": "UNIT-NPC-JAMES-HUB"},
        ],
    )
    hub(
        "UNIT-MAIN-HALL-BASE",
        "Main exhibition hall",
        "hall",
        "LOC-MAIN-HALL",
        [
            {"label": "Inspect the empty wall mount and archived crate label.", "destination_unit_id": "UNIT-CHK-SIGHTLINE-DECL"},
            {"label": "Speak with curator Lina Morales.", "destination_unit_id": "UNIT-NPC-LINA-HUB"},
            {"label": "Return to the lobby.", "destination_unit_id": "UNIT-LOBBY-BASE"},
            {"label": "Go to the director's office.", "destination_unit_id": "UNIT-OFFICE-BASE"},
        ],
    )
    hub(
        "UNIT-VAULT-BASE",
        "Secure vault",
        "vault",
        "LOC-VAULT",
        [
            {"label": "Review the security tablet vault log.", "destination_unit_id": "UNIT-OBJ-TABLET-MENU"},
            {"label": "Return to the lobby.", "destination_unit_id": "UNIT-LOBBY-BASE"},
            {"label": "Go to the main exhibition hall.", "destination_unit_id": "UNIT-MAIN-HALL-BASE"},
        ],
    )
    hub(
        "UNIT-OFFICE-BASE",
        "Director's office",
        "office",
        "LOC-OFFICE",
        [
            {"label": "Use the camera audit terminal.", "destination_unit_id": "UNIT-OBJ-CAMERA-MENU"},
            {"label": "Review the insurance rider binder.", "destination_unit_id": "UNIT-OBJ-RIDER-MENU"},
            {"label": "Search the private sale contract file.", "destination_unit_id": "UNIT-OBJ-SALE-MENU"},
            {"label": "Return to the lobby.", "destination_unit_id": "UNIT-LOBBY-BASE"},
            {"label": "Go to the main exhibition hall.", "destination_unit_id": "UNIT-MAIN-HALL-BASE"},
        ],
    )
    hub(
        "UNIT-TERRACE-BASE",
        "Rooftop terrace",
        "terrace",
        "LOC-TERRACE",
        [
            {"label": "Speak with collector Otto Weiss.", "destination_unit_id": "UNIT-NPC-OTTO-HUB"},
            {"label": "Return to the lobby.", "destination_unit_id": "UNIT-LOBBY-BASE"},
        ],
    )

    def npc_hub(uid, title, loc_id, topics, return_to):
        units.append(
            {
                "unit_id": uid,
                "title": title,
                "player_file": "NPCS",
                "unit_kind": "npc_interaction",
                "linked_location_id": loc_id,
                "prose": {"body": f"{title} meets you here. Their account may contradict other witnesses."},
                "choices": topics + [{"label": "End this conversation.", "destination_unit_id": return_to}],
                "meta": {"location_id": loc_id, "time_cost_minutes": 0},
            }
        )

    npc_hub(
        "UNIT-NPC-VERA-HUB",
        "Gallery director Vera Okonkwo",
        "LOC-LOBBY",
        [
            {"label": "Ask about her whereabouts after 2030.", "destination_unit_id": "UNIT-TOPIC-VERA-ALIBI"},
            {"label": "Ask why she reported a theft.", "destination_unit_id": "UNIT-TOPIC-VERA-CLAIM"},
            {"label": "Ask about the insurance appraisal.", "destination_unit_id": "UNIT-TOPIC-VERA-INSURANCE"},
        ],
        "UNIT-LOBBY-BASE",
    )
    npc_hub(
        "UNIT-NPC-JAMES-HUB",
        "Head of security James Holt",
        "LOC-LOBBY",
        [
            {"label": "Ask whether the painting was in the vault.", "destination_unit_id": "UNIT-TOPIC-JAMES-VAULT"},
            {"label": "Ask about crate movement during the opening.", "destination_unit_id": "UNIT-TOPIC-JAMES-CRATE"},
            {"label": "Ask where Lina Morales was at 2045.", "destination_unit_id": "UNIT-TOPIC-JAMES-LINA"},
        ],
        "UNIT-LOBBY-BASE",
    )
    npc_hub(
        "UNIT-NPC-LINA-HUB",
        "Lead curator Lina Morales",
        "LOC-MAIN-HALL",
        [
            {"label": "Ask where she was during the disappearance window.", "destination_unit_id": "UNIT-TOPIC-LINA-PODIUM"},
            {"label": "Ask when she first noticed the empty wall.", "destination_unit_id": "UNIT-TOPIC-LINA-WALL"},
            {"label": "Ask whether James could see the vault from the hall.", "destination_unit_id": "UNIT-TOPIC-LINA-JAMES"},
        ],
        "UNIT-MAIN-HALL-BASE",
    )
    npc_hub(
        "UNIT-NPC-OTTO-HUB",
        "Collector Otto Weiss",
        "LOC-TERRACE",
        [
            {"label": "Ask about photos taken near the painting.", "destination_unit_id": "UNIT-TOPIC-OTTO-PHOTO"},
            {"label": "Ask what he saw from the patron rail.", "destination_unit_id": "UNIT-TOPIC-OTTO-SIGHTLINE"},
            {"label": "Ask about his insurance interest in the piece.", "destination_unit_id": "UNIT-TOPIC-OTTO-INSURED"},
        ],
        "UNIT-TERRACE-BASE",
    )

    topics = [
        ("UNIT-TOPIC-VERA-ALIBI", "Vera Okonkwo", "Vera adjusts her gallery badge without meeting your eyes.", "I was on a carrier call in my office from 2030 onward. I did not go near the main hall until the alarm.", "UNIT-NPC-VERA-HUB", "UNIT-LOBBY-BASE"),
        ("UNIT-TOPIC-VERA-CLAIM", "Vera Okonkwo", "Vera gestures toward the alarm panel printout.", "We secured the piece according to protocol. Someone exploited the crowd — that is why I filed the theft report immediately.", "UNIT-NPC-VERA-HUB", "UNIT-LOBBY-BASE"),
        ("UNIT-TOPIC-VERA-INSURANCE", "Vera Okonkwo", "Vera slides the rider across the desk.", "The appraisal reflects independent valuation. Otto insisted on full replacement coverage for the opening.", "UNIT-NPC-VERA-HUB", "UNIT-LOBBY-BASE"),
        ("UNIT-TOPIC-JAMES-VAULT", "James Holt", "James pulls up the vault screen on his tablet.", "The painting was logged into vault storage at 2045. It stayed there until the frame alarm at 2100.", "UNIT-NPC-JAMES-HUB", "UNIT-LOBBY-BASE"),
        ("UNIT-TOPIC-JAMES-CRATE", "James Holt", "James exhales slowly.", "The director ordered a loan-return crate moved during the speech. I signed off because the paperwork looked routine.", "UNIT-NPC-JAMES-HUB", "UNIT-LOBBY-BASE"),
        ("UNIT-TOPIC-JAMES-LINA", "James Holt", "James frowns at his notes.", "Lina was handling vault intake with me around 2045. She would have seen the piece go downstairs.", "UNIT-NPC-JAMES-HUB", "UNIT-LOBBY-BASE"),
        ("UNIT-TOPIC-LINA-PODIUM", "Lina Morales", "Lina points to the fixed podium mic.", "I was on the podium from 2035 until the alarm. I never entered the vault tonight.", "UNIT-NPC-LINA-HUB", "UNIT-MAIN-HALL-BASE"),
        ("UNIT-TOPIC-LINA-WALL", "Lina Morales", "Lina's voice drops.", "I saw the wall mount empty around 2055 while thanking the artist. James insists it was already in the vault — that cannot be right.", "UNIT-NPC-LINA-HUB", "UNIT-MAIN-HALL-BASE"),
        ("UNIT-TOPIC-LINA-JAMES", "Lina Morales", "Lina shakes her head.", "From the podium I had a clear sightline to the wall. James could not see the vault door from there.", "UNIT-NPC-LINA-HUB", "UNIT-MAIN-HALL-BASE"),
        ("UNIT-TOPIC-OTTO-PHOTO", "Otto Weiss", "Otto opens his phone gallery.", "I photographed Vera signing a crate label at 2043. The metadata is intact if your carrier needs it.", "UNIT-NPC-OTTO-HUB", "UNIT-TERRACE-BASE"),
        ("UNIT-TOPIC-OTTO-SIGHTLINE", "Otto Weiss", "Otto indicates the patron rail.", "From here I could see the crate and the wall mount. Vera was at the crate; Lina was at the podium.", "UNIT-NPC-OTTO-HUB", "UNIT-TERRACE-BASE"),
        ("UNIT-TOPIC-OTTO-INSURED", "Otto Weiss", "Otto taps the policy number on his card.", "I insured Midnight Verdict for the opening. The rider value is higher than what I paid at private preview — Vera arranged that.", "UNIT-NPC-OTTO-HUB", "UNIT-TERRACE-BASE"),
    ]
    for uid, speaker, scene, quote, hub_id, exit_id in topics:
        units.append(
            {
                "unit_id": uid,
                "title": uid.replace("UNIT-TOPIC-", "Topic ").replace("-", " ").title(),
                "player_file": "NPCS",
                "unit_kind": "dialogue_topic",
                "prose": {"dialogue": {"scene": scene, "speaker": speaker, "prompt": "says", "quote": quote, "coda": "You note the answer in your case file."}},
                "choices": [
                    {"label": f"Return to speaking with {speaker.split()[-1]}.", "destination_unit_id": hub_id},
                    {"label": "Leave this conversation.", "destination_unit_id": exit_id},
                ],
                "meta": {"time_cost_minutes": 2},
            }
        )

    obj_units = [
        ("UNIT-OBJ-TABLET-MENU", "Security tablet log", "The vault tablet shows overnight transfer entries.", "UNIT-VAULT-BASE", [
            ("Compare vault timestamps with witness accounts.", "UNIT-CHK-CRATE-DECL"),
            ("Read the raw vault transfer log.", "UNIT-OBJ-TABLET-RESULT"),
        ]),
        ("UNIT-OBJ-TABLET-RESULT", "Vault transfer log", "A 2045 entry claims Midnight Verdict moved to vault bay three. No scan confirms physical placement.", "UNIT-VAULT-BASE", []),
        ("UNIT-OBJ-CAMERA-MENU", "Camera audit terminal", "The terminal lists camera segment status for opening night.", "UNIT-OFFICE-BASE", [
            ("Correlate disable log with badge records.", "UNIT-CHK-CAMERA-DECL"),
            ("Print the raw camera audit log.", "UNIT-OBJ-CAMERA-RESULT"),
        ]),
        ("UNIT-OBJ-CAMERA-RESULT", "Camera audit log", "Hall camera segment disabled at 2038 from office terminal user VOKONKWO. Badge log shows Vera left office at 2040.", "UNIT-OFFICE-BASE", []),
        ("UNIT-OBJ-RIDER-MENU", "Insurance rider binder", "The binder holds appraisal and coverage terms for Midnight Verdict.", "UNIT-OFFICE-BASE", [
            ("Review appraisal versus market comps.", "UNIT-OBJ-RIDER-RESULT"),
        ]),
        ("UNIT-OBJ-RIDER-RESULT", "Insurance rider", "Replacement value exceeds recent private sale comps by forty percent.", "UNIT-OFFICE-BASE", []),
        ("UNIT-OBJ-SALE-MENU", "Private sale contract file", "A locked file drawer holds pre-opening contracts.", "UNIT-OFFICE-BASE", [
            ("Read the Midnight Verdict private sale contract.", "UNIT-OBJ-SALE-RESULT"),
        ]),
        ("UNIT-OBJ-SALE-RESULT", "Private sale contract", "Contract dated one week before opening shows Midnight Verdict sold privately to an offshore buyer.", "UNIT-OFFICE-BASE", []),
    ]
    for uid, title, body, ret, extra in obj_units:
        choices = [{"label": lab, "destination_unit_id": dest} for lab, dest in extra]
        choices.append({"label": "Return to the location.", "destination_unit_id": ret})
        units.append(
            {
                "unit_id": uid,
                "title": title,
                "player_file": "OBJECTS",
                "unit_kind": "object_interaction",
                "prose": {"body": body},
                "choices": choices,
                "meta": {"time_cost_minutes": 2},
            }
        )

    checks = [
        ("UNIT-CHK-SIGHTLINE-DECL", "Podium sightline", "perception", "You walk the podium sightline toward the empty wall mount.", "UNIT-SIGHTLINE-SUCCESS", "UNIT-SIGHTLINE-FAIL", "UNIT-MAIN-HALL-BASE"),
        ("UNIT-CHK-CRATE-DECL", "Vault log comparison", "reasoning", "You align James's vault claim, Lina's podium timing, and the tablet entries.", "UNIT-CRATE-SUCCESS", "UNIT-CRATE-FAIL", "UNIT-VAULT-BASE"),
        ("UNIT-CHK-CAMERA-DECL", "Camera correlation", "technical", "You reconcile camera disable timestamps with Vera's office alibi.", "UNIT-CAMERA-SUCCESS", "UNIT-CAMERA-FAIL", "UNIT-OFFICE-BASE"),
    ]
    for decl, title, cap, setup, succ, fail, ret in checks:
        units.append(
            {
                "unit_id": decl,
                "title": title,
                "player_file": "OBJECTS",
                "unit_kind": "check_declaration",
                "prose": {"setup": setup, "fact": "Roll d20 plus your modifier.", "coda": "Compare your result to the difficulty."},
                "choices": [
                    {"label": "If your roll succeeds, read the success section.", "destination_unit_id": succ},
                    {"label": "If your roll fails, read the failure section.", "destination_unit_id": fail},
                ],
                "meta": {"check": cap, "time_cost_minutes": 2},
            }
        )
    check_results = [
        ("UNIT-SIGHTLINE-SUCCESS", "Podium sightline — success", "From the podium, the wall mount was visible until approximately 2055; crate movement at 2042 would have been in direct sight.", "UNIT-MAIN-HALL-BASE", "check_success"),
        ("UNIT-SIGHTLINE-FAIL", "Podium sightline — failure", "The sightlines seem plausible, but you cannot fix the exact minute the wall went empty.", "UNIT-MAIN-HALL-BASE", "check_failure"),
        ("UNIT-CRATE-SUCCESS", "Vault log comparison — success", "James's 2045 vault entry cannot be true if Lina was on the podium and Otto photographed Vera at the crate at 2043.", "UNIT-VAULT-BASE", "check_success"),
        ("UNIT-CRATE-FAIL", "Vault log comparison — failure", "The timestamps blur together without a clear contradiction.", "UNIT-VAULT-BASE", "check_failure"),
        ("UNIT-CAMERA-SUCCESS", "Camera correlation — success", "Vera's office alibi fails: badge and camera logs place her away from the office before crate signing.", "UNIT-OFFICE-BASE", "check_success"),
        ("UNIT-CAMERA-FAIL", "Camera correlation — failure", "The terminal codes remain ambiguous without cross-reference.", "UNIT-OFFICE-BASE", "check_failure"),
    ]
    for uid, title, body, ret, kind in check_results:
        units.append(
            {
                "unit_id": uid,
                "title": title,
                "player_file": "OBJECTS",
                "unit_kind": kind,
                "prose": {"body": body},
                "choices": [{"label": "Continue investigating." if "success" in kind else "Try another route.", "destination_unit_id": ret}],
            }
        )

    scenes = [
        ("SC-LOBBY-ARRIVAL", "Arrival briefing", "Carrier dispatch meets you in the lobby as patrons filter toward the exits.", "UNIT-LOBBY-BASE"),
        ("SC-HALL-ALARM", "Empty wall mount", "Staff have roped off the empty mount where Midnight Verdict hung.", "UNIT-MAIN-HALL-BASE"),
        ("SC-TERRACE-PHOTO", "Timestamped photo", "Otto walks you through the photo metadata on the terrace rail.", "UNIT-TERRACE-BASE"),
        ("SC-OFFICE-CAMERA", "Camera records pull", "The audit terminal finishes syncing opening-night logs.", "UNIT-OFFICE-BASE"),
        ("SC-VAULT-LOG", "Vault comparison", "You compare the vault tablet with witness statements.", "UNIT-VAULT-BASE"),
        ("SC-HALL-SIGHTLINE", "Sightline walk", "You trace the curator's podium view to the wall mount.", "UNIT-MAIN-HALL-BASE"),
        ("SC-ACCUSATION-PREP", "Final determination prep", "You assemble the claim file for the carrier questionnaire.", "UNIT-OFFICE-BASE"),
        ("SC-DEADLINE-WARN", "Deadline warning", "Carrier counsel warns that the 2300 filing window is closing.", "UNIT-LOBBY-BASE"),
    ]
    for uid, title, body, ret in scenes:
        units.append(
            {
                "unit_id": uid,
                "title": title,
                "player_file": "SCENES",
                "unit_kind": "scene",
                "prose": {"body": body},
                "choices": [
                    {"label": "Continue.", "destination_unit_id": ret},
                    {"label": "Return to the location base.", "destination_unit_id": ret},
                ],
                "meta": {"time_cost_minutes": 5},
            }
        )

    inferences = [
        ("INF-WITNESS-CONFLICT", "Witness contradiction", "Which accounts cannot all be true about locations during the disappearance window?", "UNIT-MAIN-HALL-BASE"),
        ("INF-STAGING", "Staged removal", "What evidence suggests removal was planned rather than opportunistic theft?", "UNIT-OFFICE-BASE"),
        ("INF-VERA-FRAUD", "Director accountability", "Who had motive and opportunity to stage the loss for insurance?", "UNIT-LOBBY-BASE"),
        ("INF-PERFECT-VERDICT", "Full reconstruction", "Reconstruct the evening: private sale, crate removal, false vault log.", "UNIT-OFFICE-BASE"),
    ]
    for uid, title, setup, ret in inferences:
        units.append(
            {
                "unit_id": uid,
                "title": title,
                "player_file": "INFERENCE",
                "unit_kind": "inference",
                "prose": {"setup": setup, "fact": "Record your conclusion in the case file before proceeding."},
                "choices": [
                    {"label": "My conclusion matches the evidence.", "destination_unit_id": ret},
                    {"label": "I need more information.", "destination_unit_id": "UNIT-LOBBY-BASE"},
                ],
                "meta": {"time_cost_minutes": 3},
            }
        )

    recoveries = [
        ("REC-OFFICE-CAMERA", "Office Camera", "Return to the camera audit terminal.", "UNIT-OBJ-CAMERA-MENU"),
        ("REC-HALL-CRATE", "Hall Crate", "Re-examine the crate shipping label.", "UNIT-CHK-SIGHTLINE-DECL"),
        ("REC-VAULT-TABLET", "Vault Tablet", "Re-read the security tablet log.", "UNIT-OBJ-TABLET-MENU"),
        ("REC-OFFICE-RIDER", "Office Rider", "Review the insurance rider again.", "UNIT-OBJ-RIDER-MENU"),
        ("REC-LINA-PODIUM", "Lina Podium", "Return to Lina Morales for podium timing.", "UNIT-NPC-LINA-HUB"),
        ("REC-TERRACE-PHOTO", "Terrace Photo", "Ask Otto Weiss about the photo again.", "UNIT-NPC-OTTO-HUB"),
    ]
    for uid, title, body, dest in recoveries:
        units.append(
            {
                "unit_id": uid,
                "title": title,
                "player_file": "RECOVERY",
                "unit_kind": "recovery",
                "prose": {"body": body},
                "choices": [{"label": "Follow this recovery route.", "destination_unit_id": dest}],
            }
        )

    endings = [
        ("END-PERFECT", "Perfect verdict", "You document private sale, staged crate removal, and Vera Okonkwo's false alibi before the carrier deadline."),
        ("END-PARTIAL-CULPRIT", "Partial — culprit named", "You name Vera Okonkwo but miss part of the contradiction reconstruction."),
        ("END-PARTIAL-WITNESS", "Partial — witnesses only", "You resolve testimony conflicts but stop short of naming staged fraud."),
        ("END-PARTIAL-WRONG", "Partial — wrong accusation", "Your report reaches the carrier on time but misassigns accountability."),
        ("END-TIMEOUT", "Deadline timeout", "The carrier closes the filing window before you can support a determination."),
    ]
    for uid, title, body in endings:
        units.append(
            {"unit_id": uid, "title": title, "player_file": "ENDINGS", "unit_kind": "ending", "prose": {"body": body}, "choices": []}
        )

    return {
        "shell": {
            "opening": {
                "prose": "Track lighting dims over polished concrete as Vera Okonkwo meets you in the lobby. James Holt and Lina Morales wait nearby with stories that already diverge."
            },
            "how_to_play": {
                "sections": [
                    {"heading": "Your role", "body": "You are an independent insurance adjuster determining whether the loss was theft or a staged claim."},
                    {"heading": "Time", "body": "Track in-world time. Carrier filing is due at 2300."},
                    {"heading": "Checks", "body": "Roll d20 plus the modifier on your character sheet when prompted."},
                ]
            },
            "readme": {"body": "Fair-play mystery at a contemporary gallery opening. Resolve contradictory witness accounts, alibis, and sightlines."},
            "character_sheet": {
                "role": "Independent insurance adjuster",
                "intro": "You evaluate contested art losses for carrier liability.",
                "modifiers": [
                    {"capability": "perception", "modifier": 2, "when_applies": "Sightline and observation checks"},
                    {"capability": "reasoning", "modifier": 2, "when_applies": "Timeline and testimony contradiction checks"},
                    {"capability": "technical", "modifier": 1, "when_applies": "Security log and metadata checks"},
                ],
                "equipment": "Carrier tablet, badge scanner, pocket scale loupe.",
                "stakes": "File a supported claim determination before the 2300 deadline.",
            },
            "case_file": "# Case file — The Gallery Verdict\n\n## Witness notes\n\n## Timeline cross-reference\n\n## Final determination\n",
            "navigation_index": {
                "entries": [
                    {"label": "Locations", "file_ref": "PLAYER/LOCATIONS.md"},
                    {"label": "NPCs", "file_ref": "PLAYER/NPCS.md"},
                    {"label": "Objects", "file_ref": "PLAYER/OBJECTS.md"},
                    {"label": "Scenes", "file_ref": "PLAYER/SCENES.md"},
                    {"label": "Inference", "file_ref": "PLAYER/INFERENCE.md"},
                    {"label": "Recovery", "file_ref": "PLAYER/RECOVERY.md"},
                    {"label": "Endings", "file_ref": "PLAYER/ENDINGS.md"},
                ]
            },
        },
        "units": units,
    }


def _epistemic() -> dict:
    return {
        "start_template_unit_id": "UNIT-LOBBY-BASE",
        "initial_player_knowledge": ["KNOW-OPEN-01", "KNOW-OPEN-02", "KNOW-OPEN-03", "KNOW-OPEN-04"],
        "initial_observable_entities": ["NPC-VERA", "NPC-JAMES", "NPC-LINA"],
        "initial_observable_objects": ["OBJ-PAINTING-FRAME"],
        "hub_definitions": [
            {
                "hub_unit_id": "UNIT-LOBBY-BASE",
                "event_kind": "location_hub",
                "physical_location_id": "LOC-LOBBY",
                "observable_entities": ["NPC-VERA", "NPC-JAMES"],
                "actions": [
                    {"label": "Enter the main exhibition hall.", "destination_unit_id": "UNIT-MAIN-HALL-BASE", "action_type": "nav"},
                    {"label": "Descend to the secure vault.", "destination_unit_id": "UNIT-VAULT-BASE", "action_type": "nav"},
                    {"label": "Take the corridor to the director's office.", "destination_unit_id": "UNIT-OFFICE-BASE", "action_type": "nav"},
                    {"label": "Ride the elevator to the rooftop terrace.", "destination_unit_id": "UNIT-TERRACE-BASE", "action_type": "nav"},
                    {"label": "Speak with gallery director Vera Okonkwo.", "destination_unit_id": "UNIT-NPC-VERA-HUB", "action_type": "conversation"},
                    {"label": "Speak with head of security James Holt.", "destination_unit_id": "UNIT-NPC-JAMES-HUB", "action_type": "conversation"},
                ],
            },
            {
                "hub_unit_id": "UNIT-NPC-VERA-HUB",
                "event_kind": "npc_interaction",
                "physical_location_id": "LOC-LOBBY",
                "actions": [
                    {"label": "Ask about her whereabouts after 2030.", "destination_unit_id": "UNIT-TOPIC-VERA-ALIBI", "action_type": "conversation", "investigative": True},
                    {"label": "Ask why she reported a theft.", "destination_unit_id": "UNIT-TOPIC-VERA-CLAIM", "action_type": "conversation", "investigative": True},
                    {"label": "Ask about the insurance appraisal.", "destination_unit_id": "UNIT-TOPIC-VERA-INSURANCE", "action_type": "conversation", "investigative": True},
                ],
            },
            {
                "hub_unit_id": "UNIT-NPC-JAMES-HUB",
                "event_kind": "npc_interaction",
                "physical_location_id": "LOC-LOBBY",
                "actions": [
                    {"label": "Ask whether the painting was in the vault.", "destination_unit_id": "UNIT-TOPIC-JAMES-VAULT", "action_type": "conversation", "investigative": True},
                    {"label": "Ask about crate movement during the opening.", "destination_unit_id": "UNIT-TOPIC-JAMES-CRATE", "action_type": "conversation", "investigative": True},
                    {"label": "Ask where Lina Morales was at 2045.", "destination_unit_id": "UNIT-TOPIC-JAMES-LINA", "action_type": "conversation", "investigative": True},
                ],
            },
            {
                "hub_unit_id": "UNIT-NPC-LINA-HUB",
                "event_kind": "npc_interaction",
                "physical_location_id": "LOC-MAIN-HALL",
                "actions": [
                    {"label": "Ask where she was during the disappearance window.", "destination_unit_id": "UNIT-TOPIC-LINA-PODIUM", "action_type": "conversation", "investigative": True},
                    {"label": "Ask when she first noticed the empty wall.", "destination_unit_id": "UNIT-TOPIC-LINA-WALL", "action_type": "conversation", "investigative": True},
                    {"label": "Ask whether James could see the vault from the hall.", "destination_unit_id": "UNIT-TOPIC-LINA-JAMES", "action_type": "conversation", "investigative": True},
                ],
            },
            {
                "hub_unit_id": "UNIT-NPC-OTTO-HUB",
                "event_kind": "npc_interaction",
                "physical_location_id": "LOC-TERRACE",
                "actions": [
                    {"label": "Ask about photos taken near the painting.", "destination_unit_id": "UNIT-TOPIC-OTTO-PHOTO", "action_type": "conversation", "investigative": True},
                    {"label": "Ask what he saw from the patron rail.", "destination_unit_id": "UNIT-TOPIC-OTTO-SIGHTLINE", "action_type": "conversation", "investigative": True},
                    {"label": "Ask about his insurance interest in the piece.", "destination_unit_id": "UNIT-TOPIC-OTTO-INSURED", "action_type": "conversation", "investigative": True},
                ],
            },
        ],
        "topic_return_profiles": [
            {"unit_prefix": "UNIT-TOPIC-VERA", "hub_unit_id": "UNIT-NPC-VERA-HUB", "hub_label": "Return to Vera.", "exit_unit_id": "UNIT-LOBBY-BASE", "exit_label": "Leave the conversation."},
            {"unit_prefix": "UNIT-TOPIC-JAMES", "hub_unit_id": "UNIT-NPC-JAMES-HUB", "hub_label": "Return to James.", "exit_unit_id": "UNIT-LOBBY-BASE", "exit_label": "Leave the conversation."},
            {"unit_prefix": "UNIT-TOPIC-LINA", "hub_unit_id": "UNIT-NPC-LINA-HUB", "hub_label": "Return to Lina.", "exit_unit_id": "UNIT-MAIN-HALL-BASE", "exit_label": "Leave the conversation."},
            {"unit_prefix": "UNIT-TOPIC-OTTO", "hub_unit_id": "UNIT-NPC-OTTO-HUB", "hub_label": "Return to Otto.", "exit_unit_id": "UNIT-TERRACE-BASE", "exit_label": "Leave the conversation."},
        ],
        "topic_knowledge_grants": {
            "UNIT-TOPIC-LINA-PODIUM": ["KNOW-LINA-PODIUM"],
            "UNIT-TOPIC-JAMES-VAULT": ["KNOW-JAMES-VAULT"],
            "UNIT-TOPIC-OTTO-PHOTO": ["KNOW-OTTO-PHOTO"],
            "UNIT-TOPIC-VERA-ALIBI": ["KNOW-VERA-OFFICE"],
            "UNIT-TOPIC-JAMES-CRATE": ["KNOW-JAMES-AUTH"],
            "UNIT-TOPIC-VERA-INSURANCE": ["KNOW-INSURANCE-RIDER"],
        },
        "inference_choice_gates": [
            {"label_contains": "My conclusion matches the evidence", "requires_knowledge_ids": ["KNOW-CONTRADICTION-JAMES-LINA"]}
        ],
        "materialization": {"max_states": 500000},
    }


def _validator_seeds() -> dict:
    return {
        "story": {
            "story_frame": {
                "investigation_starts_where": "urban gallery lobby after opening-night alarm",
                "investigation_starts_when": "approximately 2115 same evening",
                "incident_description": "featured painting missing with contradictory witness accounts",
                "incident_when": "opening night between 2035 and 2100",
                "investigator_involvement": "independent insurance adjuster retained for claim determination",
                "deadline_or_constraint": "carrier claim filing deadline at 2300",
            },
            "timeline": {"investigation_confused_with_incident": False, "impossible_ordering": False, "events": []},
        },
        "dm_feeling": {
            "tier_c_playtest": {"required": True, "completed": False, "notes": "Pack spec seed — playtest pending"},
            "time_pressure": {"deadline_relevant": True, "forced_tradeoffs": True, "waiting_dominates": False},
        },
    }


if __name__ == "__main__":
    main()
