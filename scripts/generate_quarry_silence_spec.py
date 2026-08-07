#!/usr/bin/env python3
"""Generate adventures/The_Quarry_Silence/pack_spec.json from Harbor Light template."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "adventures/The_Harbor_Light_Signal/pack_spec.json"
OUTPUT = ROOT / "adventures/The_Quarry_Silence/pack_spec.json"


def main() -> None:
    spec = json.loads(TEMPLATE.read_text(encoding="utf-8"))
    spec = _transform(spec)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT} ({len(spec['player_units']['units'])} player units)")


def _transform(spec: dict) -> dict:
    s = deepcopy(spec)
    s["pack_id"] = "The_Quarry_Silence"
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
    s["gamebook"] = {"enabled": True, "start_template_unit_id": "UNIT-YARD-BASE"}
    s["validator_seeds"] = _validator_seeds()
    return s


def _brief() -> dict:
    return {
        "working_title": "The Quarry Silence",
        "premise": "A county occupational safety investigator examines a night-shift fatality at a limestone quarry, reconstructing events from physical traces, equipment condition, and conflicting incident reports.",
        "setting": "Active limestone quarry and processing plant — yard gate, quarry floor, primary crusher platform, shift control shack, and maintenance bay",
        "universe": "real world",
        "genre": "detective mystery",
        "realism_level": "grounded contemporary",
        "player_mode": "single_investigator",
        "investigator_character": "County occupational safety investigator dispatched to verify the official equipment-failure report",
        "opening_situation": "You arrive at dawn to find shift supervisor Marcus Reed waiting at the yard gate. The coroner liaison Diana Okoro has already tagged the scene at the quarry base, but Marcus insists hydraulic conveyor failure caused the death.",
        "initial_observable_facts": [
            "Night-shift worker Carl Mendez was found dead at the quarry base beneath the primary crusher feed.",
            "Shift supervisor Marcus Reed filed an equipment-failure incident report at 0315.",
            "Coroner liaison Diana Okoro notes impact injuries inconsistent with a pure crush narrative.",
            "Maintenance technician Elena Vasquez says the hydraulic line shows cut marks, not burst failure.",
        ],
        "target_playtime_minutes": 120,
        "in_world_duration": "one morning investigation (approximately four in-world hours)",
        "tone": "industrial, methodical, quietly tense",
        "difficulty": "standard",
        "location_scale": "single quarry site with five primary locations",
        "content_boundaries": "no graphic violence; no supernatural elements; workplace safety cover-up themes; death by fall and blunt impact; no sexual content",
        "required_themes": [
            "fair-play mystery",
            "physical and environmental evidence",
            "equipment condition versus official report",
            "meaningful time pressure",
            "one perfect ending and several imperfect endings",
        ],
        "forbidden_themes": [
            "supernatural explanations",
            "theft-primary plots",
            "magic or occult resolution",
            "direct narrator solution delivery",
        ],
        "deadline_or_constraint": "OSHA preliminary report due at 1200; crusher restart scheduled at 1300",
        "author_notes": "Codename: The Quarry Silence. Culprit NPC-MARCUS covered up safety interlock bypass after confrontation. Emphasis on physical/environmental evidence — scrape marks, fluid patterns, boot prints, dust — not testimony alone.",
    }


def _fixed_truth() -> dict:
    facts = [
        ("FACT-001", "Victim Carl Mendez was assigned solo crusher feed inspection at 0230"),
        ("FACT-002", "Hydraulic conveyor line did not fail catastrophically per maintenance baseline"),
        ("FACT-003", "Shift supervisor Marcus Reed filed equipment-failure incident report at 0315"),
        ("FACT-004", "Marcus Reed bypassed crusher feed safety interlock earlier in the shift"),
        ("FACT-005", "Limestone scrape marks at quarry base contradict pure conveyor crush narrative"),
        ("FACT-006", "Mud boot prints on crusher platform show two persons present at 0245"),
        ("FACT-007", "Hydraulic fluid splatter pattern indicates line was cut, not burst"),
        ("FACT-008", "Maintenance log shows safety interlock inspection was falsified by Marcus"),
        ("FACT-009", "Weather station records show dry conditions; claimed wet-slip cause invalid"),
        ("FACT-010", "Victim hard hat found on crusher platform, not at quarry base"),
        ("FACT-011", "Equipment operator Rick Torres witnessed Marcus on platform at 0245"),
        ("FACT-012", "Coroner preliminary notes suggest blunt impact before fall, not crush alone"),
        ("FACT-013", "Marcus Reed had prior OSHA citation for bypassing safety interlocks"),
        ("FACT-014", "Dust deposition on platform railing shows struggle or forced movement"),
    ]
    immutable = [{"fact_id": fid, "statement": stmt} for fid, stmt in facts]

    events = [
        ("EVT-001", "2026-06-12T02:15:00", "Night 1", "LOC-CRUSHER", "Marcus Reed bypasses crusher feed safety interlock", ["NPC-MARCUS"], [], ["FACT-004"]),
        ("EVT-002", "2026-06-12T02:30:00", "Night 1", "LOC-CRUSHER", "Carl Mendez begins solo feed inspection on platform", ["NPC-CARL"], ["EVT-001"], ["FACT-001"]),
        ("EVT-003", "2026-06-12T02:42:00", "Night 1", "LOC-CRUSHER", "Marcus cuts hydraulic line to simulate failure after confrontation", ["NPC-MARCUS"], ["EVT-002"], ["FACT-007"]),
        ("EVT-004", "2026-06-12T02:45:00", "Night 1", "LOC-CRUSHER", "Carl falls from platform after struggle at railing", ["NPC-CARL", "NPC-MARCUS"], ["EVT-003"], ["FACT-005", "FACT-010", "FACT-014"]),
        ("EVT-005", "2026-06-12T02:48:00", "Night 1", "LOC-QUARRY-FLOOR", "Carl's body comes to rest at quarry base", ["NPC-CARL"], ["EVT-004"], ["FACT-012"]),
        ("EVT-006", "2026-06-12T03:15:00", "Night 1", "LOC-CONTROL", "Marcus files equipment-failure incident report", ["NPC-MARCUS"], ["EVT-004"], ["FACT-003"]),
        ("EVT-007", "2026-06-12T03:30:00", "Night 1", "LOC-MAINT", "Marcus falsifies interlock inspection in maintenance log", ["NPC-MARCUS"], ["EVT-006"], ["FACT-008"]),
        ("EVT-008", "2026-06-12T04:00:00", "Night 1", "LOC-QUARRY-FLOOR", "Rick Torres told to stay quiet about platform presence", ["NPC-RICK", "NPC-MARCUS"], ["EVT-006"], ["FACT-006", "FACT-011"]),
        ("EVT-009", "2026-06-12T06:30:00", "Day 1", "LOC-YARD", "Coroner liaison Diana Okoro arrives on scene", ["NPC-DIANA"], [], ["FACT-012"]),
        ("EVT-010", "2026-06-12T07:00:00", "Day 1", "LOC-YARD", "Occupational safety investigator arrives", ["PC-INVESTIGATOR"], ["EVT-009"], []),
        ("EVT-011", "2026-06-12T08:30:00", "Day 1", "LOC-MAINT", "Maintenance records sync to investigator tablet", [], ["EVT-010"], []),
        ("EVT-012", "2026-06-12T09:30:00", "Day 1", "LOC-CRUSHER", "Elena Vasquez shares hydraulic cut findings with investigator", ["NPC-ELENA"], ["EVT-010"], ["FACT-002", "FACT-007"]),
        ("EVT-013", "2026-06-12T12:00:00", "Day 1", "LOC-CONTROL", "OSHA preliminary report deadline", [], ["EVT-010"], []),
    ]

    return {
        "culprit_id": "NPC-MARCUS",
        "motive": "Avoid OSHA shutdown and discipline after bypassing safety interlock and confrontation with Carl Mendez",
        "method": "Bypassed interlock, confrontation on platform, cut hydraulic line to simulate failure, falsified incident and maintenance records",
        "opportunity": "Shift supervisor authority, access to control shack logs and maintenance entries",
        "immutable_facts": immutable,
        "causal_timeline": {
            "clock_start": "2026-06-12T02:00:00",
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
                    "at_event_id": "EVT-004",
                    "people_locations": {"NPC-MARCUS": "LOC-CRUSHER", "NPC-CARL": "LOC-QUARRY-FLOOR"},
                    "object_states": {"OBJ-HARD-HAT": "on_platform"},
                    "access_states": {"LOC-CRUSHER": "restricted"},
                    "evidence_conditions": {},
                },
                {
                    "at_event_id": "EVT-010",
                    "people_locations": {"PC-INVESTIGATOR": "LOC-YARD"},
                    "object_states": {"OBJ-INCIDENT-REPORT": "filed"},
                    "access_states": {"LOC-YARD": "open"},
                    "evidence_conditions": {},
                },
                {
                    "at_event_id": "EVT-011",
                    "people_locations": {},
                    "object_states": {"OBJ-MAINT-RECORD": "sync_complete"},
                    "access_states": {"LOC-MAINT": "records_available"},
                    "evidence_conditions": {},
                },
            ]
        },
        "npc_knowledge": {
            "npcs": [
                {
                    "npc_id": "NPC-MARCUS",
                    "knows": ["FACT-003", "FACT-004", "FACT-007", "FACT-008"],
                    "believes_incorrectly": [],
                    "witnessed_events": ["EVT-001", "EVT-003", "EVT-004", "EVT-006", "EVT-007"],
                    "hides": ["FACT-004", "FACT-007", "FACT-008", "FACT-014"],
                    "behavior_rationale": "Conceals interlock bypass and staged hydraulic failure after platform confrontation",
                },
                {
                    "npc_id": "NPC-DIANA",
                    "knows": ["FACT-012", "FACT-005"],
                    "believes_incorrectly": [],
                    "witnessed_events": ["EVT-004", "EVT-005", "EVT-009"],
                    "hides": [],
                    "behavior_rationale": "Cooperative coroner liaison focused on physical injury patterns",
                },
                {
                    "npc_id": "NPC-ELENA",
                    "knows": ["FACT-002", "FACT-007", "FACT-008"],
                    "believes_incorrectly": [],
                    "witnessed_events": ["EVT-007", "EVT-012"],
                    "hides": [],
                    "behavior_rationale": "Truthful maintenance tech who trusts equipment condition over supervisor narrative",
                },
                {
                    "npc_id": "NPC-RICK",
                    "knows": ["FACT-006", "FACT-011"],
                    "believes_incorrectly": [],
                    "witnessed_events": ["EVT-004", "EVT-008"],
                    "hides": ["FACT-011"],
                    "behavior_rationale": "Frightened operator coached to stay quiet about Marcus on platform",
                },
            ]
        },
        "evidence_provenance": {
            "evidence": [
                {
                    "evidence_id": "EVD-INCIDENT-REPORT",
                    "source_event_id": "EVT-006",
                    "type": "document",
                    "description": "Shift supervisor equipment-failure incident report",
                    "establishes_fact_ids": ["FACT-003"],
                    "misleading": True,
                    "misleading_cause": "Attributes death to hydraulic failure rather than platform fall",
                },
                {
                    "evidence_id": "EVD-LIMESTONE-SCRAPE",
                    "source_event_id": "EVT-004",
                    "type": "physical",
                    "description": "Fresh scrape marks on quarry base limestone",
                    "establishes_fact_ids": ["FACT-005"],
                    "misleading": False,
                    "misleading_cause": None,
                },
                {
                    "evidence_id": "EVD-HYDRAULIC-STAIN",
                    "source_event_id": "EVT-003",
                    "type": "physical",
                    "description": "Hydraulic fluid splatter on crusher deck",
                    "establishes_fact_ids": ["FACT-007"],
                    "misleading": False,
                    "misleading_cause": None,
                },
                {
                    "evidence_id": "EVD-BOOT-PRINTS",
                    "source_event_id": "EVT-004",
                    "type": "physical",
                    "description": "Mud boot print pairs on crusher platform",
                    "establishes_fact_ids": ["FACT-006"],
                    "misleading": False,
                    "misleading_cause": None,
                },
                {
                    "evidence_id": "EVD-MAINT-LOG",
                    "source_event_id": "EVT-007",
                    "type": "document",
                    "description": "Falsified interlock inspection maintenance log",
                    "establishes_fact_ids": ["FACT-008", "FACT-013"],
                    "misleading": True,
                    "misleading_cause": "Shows passed inspection that did not occur",
                },
                {
                    "evidence_id": "EVD-WEATHER-LOG",
                    "source_event_id": "EVT-010",
                    "type": "document",
                    "description": "Site weather station overnight log",
                    "establishes_fact_ids": ["FACT-009"],
                    "misleading": False,
                    "misleading_cause": None,
                },
            ]
        },
        "observable_information": {
            "observations": [
                {
                    "observation_id": "OBS-SCRAPE",
                    "learnable_fact_id": "FACT-005",
                    "source_evidence_id": "EVD-LIMESTONE-SCRAPE",
                    "requires": {"action": "inspect", "location_id": "LOC-QUARRY-FLOOR", "check_id": "CHK-IMPACT"},
                    "hidden_if_not_met": True,
                },
                {
                    "observation_id": "OBS-HYDRAULIC",
                    "learnable_fact_id": "FACT-007",
                    "source_evidence_id": "EVD-HYDRAULIC-STAIN",
                    "requires": {"action": "inspect", "location_id": "LOC-CRUSHER", "check_id": "CHK-HYDRAULIC"},
                    "hidden_if_not_met": True,
                },
                {
                    "observation_id": "OBS-BOOTS",
                    "learnable_fact_id": "FACT-006",
                    "source_evidence_id": "EVD-BOOT-PRINTS",
                    "requires": {"action": "inspect", "location_id": "LOC-CRUSHER", "check_id": "CHK-TRACKS"},
                    "hidden_if_not_met": True,
                },
            ]
        },
        "conclusion_requirements": {
            "questions": [
                {
                    "question_id": "Q-CULPRIT",
                    "answer_entity_id": "NPC-MARCUS",
                    "required_fact_ids": ["FACT-004", "FACT-007", "FACT-008", "FACT-014"],
                },
                {
                    "question_id": "Q-METHOD",
                    "answer_entity_id": "METHOD-COVERUP",
                    "required_fact_ids": ["FACT-003", "FACT-007", "FACT-008"],
                },
            ]
        },
        "ending_claims": [
            {"ending_id": "END-PERFECT", "asserted_fact_ids": ["FACT-004", "FACT-007", "FACT-008", "FACT-014"]},
            {"ending_id": "END-TIMEOUT", "asserted_fact_ids": []},
        ],
    }


def _locations() -> list:
    return [
        {
            "location_id": "LOC-YARD",
            "public_name": "Quarry yard gate",
            "start_location": True,
            "hub_unit_id": "UNIT-YARD-BASE",
            "parent_location_id": None,
            "location_type": "industrial_yard",
            "description_source": "DESC-YARD",
            "default_attributes": {"access": "open"},
        },
        {
            "location_id": "LOC-QUARRY-FLOOR",
            "public_name": "Quarry floor",
            "hub_unit_id": "UNIT-QUARRY-FLOOR-BASE",
            "parent_location_id": "LOC-YARD",
            "location_type": "quarry_base",
            "description_source": "DESC-QUARRY-FLOOR",
            "default_attributes": {"access": "restricted"},
        },
        {
            "location_id": "LOC-CRUSHER",
            "public_name": "Primary crusher platform",
            "hub_unit_id": "UNIT-CRUSHER-BASE",
            "parent_location_id": "LOC-YARD",
            "location_type": "processing_plant",
            "description_source": "DESC-CRUSHER",
            "default_attributes": {"access": "restricted"},
        },
        {
            "location_id": "LOC-CONTROL",
            "public_name": "Shift control shack",
            "hub_unit_id": "UNIT-CONTROL-BASE",
            "parent_location_id": "LOC-YARD",
            "location_type": "control_office",
            "description_source": "DESC-CONTROL",
            "default_attributes": {"access": "open"},
        },
        {
            "location_id": "LOC-MAINT",
            "public_name": "Maintenance bay",
            "hub_unit_id": "UNIT-MAINT-BASE",
            "parent_location_id": "LOC-YARD",
            "location_type": "maintenance_bay",
            "description_source": "DESC-MAINT",
            "default_attributes": {"access": "open"},
        },
    ]


def _location_states() -> list:
    return [
        {
            "state_id": "LOC-YARD:default",
            "location_id": "LOC-YARD",
            "variant_label": "investigation_start",
            "attributes": {"access": "open", "scene_taped": "partial"},
            "cause": {"type": "timeline_event", "ref": "EVT-010"},
        },
        {
            "state_id": "LOC-MAINT:records_sync",
            "location_id": "LOC-MAINT",
            "variant_label": "records_synced",
            "attributes": {"records_sync": "complete"},
            "cause": {"type": "timeline_event", "ref": "EVT-011"},
        },
    ]


def _features() -> list:
    return [
        {
            "feature_id": "FEAT-LIMESTONE-SCRAPE",
            "location_id": "LOC-QUARRY-FLOOR",
            "label": "Limestone scrape marks at impact zone",
            "object_ref": "OBJ-LIMESTONE-SCRAPE",
        },
        {
            "feature_id": "FEAT-HYDRAULIC-STAIN",
            "location_id": "LOC-CRUSHER",
            "label": "Hydraulic fluid stain on crusher deck",
            "object_ref": "OBJ-HYDRAULIC-STAIN",
        },
    ]


def _navigation() -> list:
    pairs = [
        ("NAV-YARD-FLOOR", "LOC-YARD", "LOC-QUARRY-FLOOR", "Descend to the quarry floor", 4),
        ("NAV-YARD-CRUSHER", "LOC-YARD", "LOC-CRUSHER", "Climb to the primary crusher platform", 5),
        ("NAV-YARD-CONTROL", "LOC-YARD", "LOC-CONTROL", "Walk to the shift control shack", 2),
        ("NAV-YARD-MAINT", "LOC-YARD", "LOC-MAINT", "Cross to the maintenance bay", 3),
        ("NAV-FLOOR-YARD", "LOC-QUARRY-FLOOR", "LOC-YARD", "Return to the yard gate", 4),
        ("NAV-CRUSHER-YARD", "LOC-CRUSHER", "LOC-YARD", "Return to the yard gate", 5),
        ("NAV-CONTROL-YARD", "LOC-CONTROL", "LOC-YARD", "Return to the yard gate", 2),
        ("NAV-MAINT-YARD", "LOC-MAINT", "LOC-YARD", "Return to the yard gate", 3),
    ]
    return [
        {"edge_id": eid, "from_location_id": fr, "to_location_id": to, "direction_label": label, "time_cost_minutes": cost}
        for eid, fr, to, label, cost in pairs
    ]


def _npcs() -> list:
    return [
        {"npc_id": "NPC-MARCUS", "public_name": "Marcus Reed", "role": "Shift supervisor", "relationships": [{"target_npc_id": "NPC-RICK", "relationship_type": "supervisor"}]},
        {"npc_id": "NPC-DIANA", "public_name": "Diana Okoro", "role": "County coroner liaison", "relationships": [{"target_npc_id": "NPC-MARCUS", "relationship_type": "professional"}]},
        {"npc_id": "NPC-ELENA", "public_name": "Elena Vasquez", "role": "Maintenance technician", "relationships": [{"target_npc_id": "NPC-MARCUS", "relationship_type": "professional"}]},
        {"npc_id": "NPC-RICK", "public_name": "Rick Torres", "role": "Equipment operator", "relationships": [{"target_npc_id": "NPC-MARCUS", "relationship_type": "supervisor"}]},
    ]


def _objects() -> list:
    return [
        {"object_id": "OBJ-LIMESTONE-SCRAPE", "public_name": "Limestone scrape marks", "location_id": "LOC-QUARRY-FLOOR", "interaction_type": "physical"},
        {"object_id": "OBJ-HARD-HAT", "public_name": "Victim hard hat", "location_id": "LOC-CRUSHER", "interaction_type": "physical"},
        {"object_id": "OBJ-HYDRAULIC-STAIN", "public_name": "Hydraulic fluid stain", "location_id": "LOC-CRUSHER", "interaction_type": "physical"},
        {"object_id": "OBJ-BOOT-PRINTS", "public_name": "Mud boot print trail", "location_id": "LOC-CRUSHER", "interaction_type": "physical"},
        {"object_id": "OBJ-INCIDENT-REPORT", "public_name": "Incident report terminal", "location_id": "LOC-CONTROL", "interaction_type": "terminal"},
        {"object_id": "OBJ-WEATHER-LOG", "public_name": "Weather station log", "location_id": "LOC-CONTROL", "interaction_type": "document"},
        {"object_id": "OBJ-MAINT-RECORD", "public_name": "Maintenance inspection log", "location_id": "LOC-MAINT", "interaction_type": "document"},
    ]


def _knowledge() -> dict:
    facts = _fixed_truth()["immutable_facts"]
    knowledge_items = [
        ("KNOW-OPEN-01", "Carl Mendez found dead at quarry base; official report cites equipment failure", "briefing", "A", []),
        ("KNOW-OPEN-02", "Coroner liaison notes impact injuries inconsistent with pure crush", "briefing", "A", []),
        ("KNOW-OPEN-03", "Shift supervisor Marcus Reed filed incident report at 0315", "briefing", "A", []),
        ("KNOW-OPEN-04", "OSHA preliminary report due at 1200 before crusher restart", "briefing", "A", []),
        ("KNOW-SCRAPE-MARKS", "Fresh limestone scrape marks at quarry base suggest lateral impact before rest; dust scuff on railing confirms struggle", "physical", "B", ["FACT-005", "FACT-014"]),
        ("KNOW-HYDRAULIC-CUT", "Hydraulic fluid splatter shows cut line, not burst failure", "physical", "B", ["FACT-002", "FACT-007"]),
        ("KNOW-BOOT-PRINTS", "Two distinct boot print sets on crusher platform at 0245", "physical", "B", ["FACT-006"]),
        ("KNOW-HARD-HAT", "Victim hard hat on platform contradicts crush-at-base narrative", "physical", "B", ["FACT-010"]),
        ("KNOW-INCIDENT-REPORT", "Marcus Reed logged hydraulic conveyor failure as cause of death", "document", "B", ["FACT-003"]),
        ("KNOW-WEATHER-DRY", "Weather log shows dry overnight conditions; wet-slip claim invalid", "document", "B", ["FACT-009"]),
        ("KNOW-MAINT-FALSIFIED", "Interlock inspection entry signed by Marcus does not match equipment state", "document", "B", ["FACT-008", "FACT-013"]),
        ("KNOW-DIANA-IMPACT", "Coroner notes blunt impact injuries before fall", "testimony", "B", ["FACT-012"]),
        ("KNOW-ELENA-HYDRAULIC", "Maintenance tech says hydraulic line was cut, not failed", "testimony", "B", ["FACT-002", "FACT-007"]),
        ("KNOW-RICK-WITNESS", "Rick Torres saw Marcus on platform but was told to stay quiet", "testimony", "B", ["FACT-011"]),
        ("KNOW-MARCUS-SLIP", "Marcus claims wet deck caused slip into equipment", "testimony", "B", []),
        ("KNOW-PHYSICAL-CONTRADICTS", "Physical traces contradict official equipment-failure narrative", "inference", "C", []),
        ("KNOW-MARCUS-COVERUP", "Evidence supports staged failure and falsified records by shift supervisor", "inference", "C", []),
        ("KNOW-PERFECT-RECON", "Full reconstruction: interlock bypass, platform fall, cut hydraulic line, falsified logs", "inference", "C", []),
    ]
    return {
        "facts": [{"fact_id": f["fact_id"], "statement": f["statement"], "immutable": True} for f in facts],
        "observations": [
            {"observation_id": "OBS-SCRAPE-PHYS", "description": "Limestone scrape inconsistent with crush", "establishes_knowledge_id": "KNOW-SCRAPE-MARKS"},
            {"observation_id": "OBS-FLUID-PATTERN", "description": "Hydraulic splatter indicates cut", "establishes_knowledge_id": "KNOW-HYDRAULIC-CUT"},
            {"observation_id": "OBS-BOOT-PAIR", "description": "Two boot print sets on platform", "establishes_knowledge_id": "KNOW-BOOT-PRINTS"},
        ],
        "evidence": [
            {"evidence_id": "EVD-LIMESTONE-SCRAPE", "name": "Limestone scrape marks", "location_id": "LOC-QUARRY-FLOOR"},
            {"evidence_id": "EVD-HYDRAULIC-STAIN", "name": "Hydraulic fluid stain", "location_id": "LOC-CRUSHER"},
            {"evidence_id": "EVD-BOOT-PRINTS", "name": "Mud boot prints", "location_id": "LOC-CRUSHER"},
            {"evidence_id": "EVD-INCIDENT-REPORT", "name": "Incident report", "location_id": "LOC-CONTROL"},
            {"evidence_id": "EVD-WEATHER-LOG", "name": "Weather station log", "location_id": "LOC-CONTROL"},
            {"evidence_id": "EVD-MAINT-LOG", "name": "Maintenance inspection log", "location_id": "LOC-MAINT"},
        ],
        "testimony": [
            {"testimony_id": "TEST-DIANA-IMPACT", "npc_id": "NPC-DIANA", "summary": "Impact before fall", "grants_knowledge_id": "KNOW-DIANA-IMPACT"},
            {"testimony_id": "TEST-ELENA-HYDRAULIC", "npc_id": "NPC-ELENA", "summary": "Cut hydraulic line", "grants_knowledge_id": "KNOW-ELENA-HYDRAULIC"},
            {"testimony_id": "TEST-RICK-WITNESS", "npc_id": "NPC-RICK", "summary": "Marcus on platform", "grants_knowledge_id": "KNOW-RICK-WITNESS"},
            {"testimony_id": "TEST-MARCUS-SLIP", "npc_id": "NPC-MARCUS", "summary": "Wet slip claim", "grants_knowledge_id": "KNOW-MARCUS-SLIP"},
        ],
        "knowledge_items": [
            {"knowledge_id": kid, "summary": summary, "source_type": stype, "tier": tier, **({"establishes_fact_ids": fids} if fids else {})}
            for kid, summary, stype, tier, fids in knowledge_items
        ],
        "hypotheses": [
            {"hypothesis_id": "HYP-PHYSICAL-CONFLICT", "statement": "Physical evidence contradicts official equipment-failure report", "related_knowledge_ids": ["KNOW-SCRAPE-MARKS", "KNOW-HYDRAULIC-CUT", "KNOW-HARD-HAT", "KNOW-WEATHER-DRY"], "yields_knowledge_id": "KNOW-PHYSICAL-CONTRADICTS"},
            {"hypothesis_id": "HYP-STAGING", "statement": "Hydraulic failure was staged after platform incident", "related_knowledge_ids": ["KNOW-HYDRAULIC-CUT", "KNOW-BOOT-PRINTS", "KNOW-SCRAPE-MARKS"], "yields_knowledge_id": "KNOW-MARCUS-COVERUP"},
            {"hypothesis_id": "HYP-MARCUS-ACCOUNTABLE", "statement": "Shift supervisor orchestrated cover-up", "related_knowledge_ids": ["KNOW-MAINT-FALSIFIED", "KNOW-RICK-WITNESS", "KNOW-INCIDENT-REPORT"], "yields_knowledge_id": "KNOW-MARCUS-COVERUP"},
            {"hypothesis_id": "HYP-PERFECT-RECON", "statement": "Full physical reconstruction resolves the case", "related_knowledge_ids": ["KNOW-PHYSICAL-CONTRADICTS", "KNOW-MARCUS-COVERUP", "KNOW-PERFECT-RECON"], "yields_knowledge_id": "KNOW-PERFECT-RECON"},
        ],
        "conclusions": [
            {"conclusion_id": "CONC-WHO", "question": "Who falsified the equipment-failure narrative?", "correct_answer": "NPC-MARCUS"},
            {"conclusion_id": "CONC-WHAT", "question": "What happened to Carl Mendez?", "correct_answer": "Fall from crusher platform after confrontation, not hydraulic crush alone"},
            {"conclusion_id": "CONC-HOW", "question": "How was the cover-up executed?", "correct_answer": "Cut hydraulic line and falsified incident and maintenance logs"},
            {"conclusion_id": "CONC-WHEN", "question": "When did the fall occur?", "correct_answer": "Approximately 0245 during night shift"},
        ],
        "proofs": [
            {"proof_id": "PROOF-WHO", "conclusion_id": "CONC-WHO", "required_knowledge_ids": ["KNOW-PERFECT-RECON", "KNOW-MARCUS-COVERUP", "KNOW-PHYSICAL-CONTRADICTS"]},
            {"proof_id": "PROOF-WHAT", "conclusion_id": "CONC-WHAT", "required_knowledge_ids": ["KNOW-SCRAPE-MARKS", "KNOW-DIANA-IMPACT", "KNOW-HARD-HAT"]},
            {"proof_id": "PROOF-HOW", "conclusion_id": "CONC-HOW", "required_knowledge_ids": ["KNOW-HYDRAULIC-CUT", "KNOW-MAINT-FALSIFIED", "KNOW-INCIDENT-REPORT"]},
            {"proof_id": "PROOF-WHEN", "conclusion_id": "CONC-WHEN", "required_knowledge_ids": ["KNOW-BOOT-PRINTS", "KNOW-RICK-WITNESS"]},
        ],
        "relationships": [
            {"relationship_id": "REL-MARCUS-RICK", "from_entity": "NPC-MARCUS", "to_entity": "NPC-RICK", "relationship_type": "supervisor_to_operator"},
        ],
    }


def _conversations() -> list:
    def conv(cid, npc, hub, topics):
        return {"conversation_id": cid, "npc_id": npc, "hub_unit_id": hub, "topics": topics}

    def topic(tid, label, unit, know, minutes=2):
        return {"topic_id": tid, "player_label": label, "response_unit_id": unit, "grants_knowledge_id": know, "time_cost_minutes": minutes}

    return [
        conv("CONV-MARCUS", "NPC-MARCUS", "UNIT-NPC-MARCUS-HUB", [
            topic("TOPIC-MARCUS-REPORT", "Ask about the equipment-failure report.", "UNIT-TOPIC-MARCUS-REPORT", "KNOW-INCIDENT-REPORT"),
            topic("TOPIC-MARCUS-SLIP", "Ask about wet deck conditions.", "UNIT-TOPIC-MARCUS-SLIP", "KNOW-MARCUS-SLIP"),
            topic("TOPIC-MARCUS-INTERLOCK", "Ask about crusher safety interlock status.", "UNIT-TOPIC-MARCUS-INTERLOCK", "KNOW-MAINT-FALSIFIED"),
        ]),
        conv("CONV-DIANA", "NPC-DIANA", "UNIT-NPC-DIANA-HUB", [
            topic("TOPIC-DIANA-IMPACT", "Ask about preliminary injury findings.", "UNIT-TOPIC-DIANA-IMPACT", "KNOW-DIANA-IMPACT"),
            topic("TOPIC-DIANA-SCENE", "Ask what the quarry base scene suggests.", "UNIT-TOPIC-DIANA-SCENE", "KNOW-DIANA-IMPACT"),
            topic("TOPIC-DIANA-HAT", "Ask about hard hat placement.", "UNIT-TOPIC-DIANA-HAT", "KNOW-DIANA-IMPACT"),
        ]),
        conv("CONV-ELENA", "NPC-ELENA", "UNIT-NPC-ELENA-HUB", [
            topic("TOPIC-ELENA-HYDRAULIC", "Ask about hydraulic line condition.", "UNIT-TOPIC-ELENA-HYDRAULIC", "KNOW-ELENA-HYDRAULIC"),
            topic("TOPIC-ELENA-INTERLOCK", "Ask about interlock inspection records.", "UNIT-TOPIC-ELENA-INTERLOCK", "KNOW-MAINT-FALSIFIED"),
            topic("TOPIC-ELENA-BASELINE", "Ask about normal failure patterns.", "UNIT-TOPIC-ELENA-BASELINE", "KNOW-ELENA-HYDRAULIC"),
        ]),
        conv("CONV-RICK", "NPC-RICK", "UNIT-NPC-RICK-HUB", [
            topic("TOPIC-RICK-PLATFORM", "Ask who was on the crusher platform.", "UNIT-TOPIC-RICK-PLATFORM", "KNOW-RICK-WITNESS"),
            topic("TOPIC-RICK-BOOTS", "Ask about boot prints in the mud.", "UNIT-TOPIC-RICK-BOOTS", "KNOW-RICK-WITNESS"),
            topic("TOPIC-RICK-TIMING", "Ask about timing before the alarm.", "UNIT-TOPIC-RICK-TIMING", "KNOW-RICK-WITNESS"),
        ]),
    ]


def _object_actions() -> list:
    return [
        {"action_id": "ACT-LIMESTONE-SCRAPE", "object_id": "OBJ-LIMESTONE-SCRAPE", "menu_unit_id": "UNIT-CHK-IMPACT-DECL", "check_id": "CHK-IMPACT"},
        {"action_id": "ACT-HYDRAULIC-STAIN", "object_id": "OBJ-HYDRAULIC-STAIN", "menu_unit_id": "UNIT-CHK-HYDRAULIC-DECL", "check_id": "CHK-HYDRAULIC"},
        {"action_id": "ACT-BOOT-PRINTS", "object_id": "OBJ-BOOT-PRINTS", "menu_unit_id": "UNIT-CHK-TRACKS-DECL", "check_id": "CHK-TRACKS"},
        {"action_id": "ACT-INCIDENT-REPORT", "object_id": "OBJ-INCIDENT-REPORT", "menu_unit_id": "UNIT-OBJ-REPORT-MENU", "result_unit_id": "UNIT-OBJ-REPORT-RESULT", "grants_knowledge_ids": ["KNOW-INCIDENT-REPORT"]},
        {"action_id": "ACT-WEATHER-LOG", "object_id": "OBJ-WEATHER-LOG", "menu_unit_id": "UNIT-OBJ-WEATHER-MENU", "result_unit_id": "UNIT-OBJ-WEATHER-RESULT", "grants_knowledge_ids": ["KNOW-WEATHER-DRY"]},
        {"action_id": "ACT-MAINT-RECORD", "object_id": "OBJ-MAINT-RECORD", "menu_unit_id": "UNIT-OBJ-MAINT-MENU", "result_unit_id": "UNIT-OBJ-MAINT-RESULT", "grants_knowledge_ids": ["KNOW-MAINT-FALSIFIED"]},
    ]


def _checks() -> list:
    return [
        {
            "check_id": "CHK-IMPACT",
            "declaration_unit_id": "UNIT-CHK-IMPACT-DECL",
            "success_unit_id": "UNIT-IMPACT-SUCCESS",
            "failure_unit_id": "UNIT-IMPACT-FAIL",
            "capability": "perception",
            "capability_category": "perception_observation",
            "modifier_source_id": "MOD-PERCEPTION",
            "dc": 12,
            "parent_action_id": "ACT-LIMESTONE-SCRAPE",
            "success_grants_knowledge_ids": ["KNOW-SCRAPE-MARKS"],
            "player_action_label": "Examine limestone scrape marks at the quarry base.",
        },
        {
            "check_id": "CHK-HYDRAULIC",
            "declaration_unit_id": "UNIT-CHK-HYDRAULIC-DECL",
            "success_unit_id": "UNIT-HYDRAULIC-SUCCESS",
            "failure_unit_id": "UNIT-HYDRAULIC-FAIL",
            "capability": "technical",
            "capability_category": "technical_systems",
            "modifier_source_id": "MOD-TECHNICAL",
            "dc": 12,
            "parent_action_id": "ACT-HYDRAULIC-STAIN",
            "success_grants_knowledge_ids": ["KNOW-HYDRAULIC-CUT"],
            "player_action_label": "Analyze hydraulic fluid splatter pattern on the crusher deck.",
        },
        {
            "check_id": "CHK-TRACKS",
            "declaration_unit_id": "UNIT-CHK-TRACKS-DECL",
            "success_unit_id": "UNIT-TRACKS-SUCCESS",
            "failure_unit_id": "UNIT-TRACKS-FAIL",
            "capability": "reasoning",
            "capability_category": "reasoning_analysis",
            "modifier_source_id": "MOD-REASONING",
            "dc": 11,
            "parent_action_id": "ACT-BOOT-PRINTS",
            "success_grants_knowledge_ids": ["KNOW-BOOT-PRINTS", "KNOW-HARD-HAT"],
            "player_action_label": "Reconstruct boot print patterns on the crusher platform.",
        },
    ]


def _flow() -> dict:
    return {
        "placeholder_resolution": {},
        "state_model": {
            "flags": [
                "records_sync_complete", "report_reviewed", "weather_reviewed", "maint_reviewed",
                "impact_examined", "hydraulic_examined", "tracks_examined", "ready_to_accuse", "accusation_complete",
                "inference_physical_resolved", "inference_staging_resolved", "inference_marcus_resolved", "inference_perfect_resolved",
                "check_impact_failed", "check_hydraulic_failed", "check_tracks_failed",
            ],
            "counters": ["investigation_phase"],
            "initial_state": {
                "records_sync_complete": False, "report_reviewed": False, "weather_reviewed": False, "maint_reviewed": False,
                "impact_examined": False, "hydraulic_examined": False, "tracks_examined": False,
                "ready_to_accuse": False, "accusation_complete": False,
                "inference_physical_resolved": False, "inference_staging_resolved": False,
                "inference_marcus_resolved": False, "inference_perfect_resolved": False,
                "check_impact_failed": False, "check_hydraulic_failed": False, "check_tracks_failed": False,
                "investigation_phase": 0,
            },
        },
        "time_model": {
            "clocks": ["T_ARRIVAL", "T_RECORDS_SYNC", "T_ELENA_FINDINGS", "T_DEADLINE"],
            "clock_event_map": {"T_ARRIVAL": "EVT-010", "T_RECORDS_SYNC": "EVT-011", "T_ELENA_FINDINGS": "EVT-012", "T_DEADLINE": "EVT-013"},
            "deadline_clock": "T_DEADLINE",
            "scene_time_cost_default_minutes": 5,
            "no_earlier_time_travel": True,
        },
        "scene_chains": [
            {
                "chain_id": "CHAIN-OPENING",
                "active_from_clock": "T_ARRIVAL",
                "active_until_clock": "T_ELENA_FINDINGS",
                "steps": [
                    {"step_id": "SC-YARD-ARRIVAL", "scene_unit_id": "SC-YARD-ARRIVAL", "player_label": "Receive arrival briefing.", "location_id": "LOC-YARD"},
                    {"step_id": "SC-FLOOR-SCENE", "scene_unit_id": "SC-FLOOR-SCENE", "player_label": "Survey the quarry floor scene.", "location_id": "LOC-QUARRY-FLOOR"},
                ],
            },
            {
                "chain_id": "CHAIN-RECORDS",
                "active_from_clock": "T_ELENA_FINDINGS",
                "active_until_clock": "T_RECORDS_SYNC",
                "steps": [
                    {"step_id": "SC-CRUSHER-HYDRAULIC", "scene_unit_id": "SC-CRUSHER-HYDRAULIC", "player_label": "Review hydraulic findings with Elena.", "location_id": "LOC-CRUSHER"},
                    {"step_id": "SC-MAINT-RECORDS", "scene_unit_id": "SC-MAINT-RECORDS", "player_label": "Pull maintenance records.", "location_id": "LOC-MAINT", "state_updates": {"records_sync_complete": True}},
                ],
            },
            {
                "chain_id": "CHAIN-FINAL",
                "active_from_clock": "T_RECORDS_SYNC",
                "active_until_clock": "T_DEADLINE",
                "steps": [
                    {"step_id": "SC-CRUSHER-TRACKS", "scene_unit_id": "SC-CRUSHER-TRACKS", "player_label": "Document platform boot prints.", "location_id": "LOC-CRUSHER", "state_updates": {"tracks_examined": True}},
                    {"step_id": "SC-FLOOR-IMPACT", "scene_unit_id": "SC-FLOOR-IMPACT", "player_label": "Measure limestone impact marks.", "location_id": "LOC-QUARRY-FLOOR", "state_updates": {"impact_examined": True}},
                    {"step_id": "SC-ACCUSATION-PREP", "scene_unit_id": "SC-ACCUSATION-PREP", "player_label": "Prepare final OSHA report.", "location_id": "LOC-CONTROL", "requires_state": {"ready_to_accuse": True}},
                    {"step_id": "SC-DEADLINE-WARN", "scene_unit_id": "SC-DEADLINE-WARN", "player_label": "Hear deadline warning.", "location_id": "LOC-YARD"},
                ],
            },
        ],
        "world_state_variants": [
            {
                "variant_id": "VAR-MAINT-RECORDS",
                "base_scene_unit_id": "SC-MAINT-RECORDS",
                "variants": [
                    {"when_state": {"flag": "records_sync_complete", "value": True}, "scene_unit_id": "SC-MAINT-RECORDS"},
                    {"when_state": {"flag": "records_sync_complete", "value": False}, "scene_unit_id": "SC-MAINT-RECORDS"},
                ],
            }
        ],
        "location_revisits": [
            {
                "location_id": "LOC-MAINT",
                "revisit_rules": [{"rule_id": "REV-MAINT", "when_clock_at_least": "T_RECORDS_SYNC", "unlocks_scene_unit_id": "SC-MAINT-RECORDS", "state_updates": {"maint_reviewed": True}}],
            },
            {
                "location_id": "LOC-CRUSHER",
                "revisit_rules": [{"rule_id": "REV-HYDRAULIC", "when_knowledge_held": ["KNOW-DIANA-IMPACT"], "unlocks_scene_unit_id": "SC-CRUSHER-HYDRAULIC", "state_updates": {"hydraulic_examined": True}}],
            },
        ],
        "inference_flow_gates": [
            {"inference_id": "INF-PHYSICAL-CONFLICT", "hypothesis_id": "HYP-PHYSICAL-CONFLICT", "required_knowledge_ids": ["KNOW-SCRAPE-MARKS", "KNOW-HYDRAULIC-CUT", "KNOW-WEATHER-DRY"], "success_state_updates": {"inference_physical_resolved": True}, "failure_preserves_investigation": True, "recovery_routes": ["REC-FLOOR-SCRAPE", "REC-CRUSHER-HYDRAULIC"]},
            {"inference_id": "INF-STAGING", "hypothesis_id": "HYP-STAGING", "required_knowledge_ids": ["KNOW-HYDRAULIC-CUT", "KNOW-BOOT-PRINTS", "KNOW-SCRAPE-MARKS"], "success_state_updates": {"inference_staging_resolved": True}, "failure_preserves_investigation": True, "recovery_routes": ["REC-CRUSHER-TRACKS", "REC-CRUSHER-HYDRAULIC"]},
            {"inference_id": "INF-MARCUS-COVERUP", "hypothesis_id": "HYP-MARCUS-ACCOUNTABLE", "required_knowledge_ids": ["KNOW-MAINT-FALSIFIED", "KNOW-RICK-WITNESS", "KNOW-INCIDENT-REPORT"], "success_state_updates": {"inference_marcus_resolved": True, "ready_to_accuse": True}, "failure_preserves_investigation": True, "recovery_routes": ["REC-MAINT-LOG", "REC-RICK-WITNESS"]},
            {"inference_id": "INF-PERFECT-RECON", "hypothesis_id": "HYP-PERFECT-RECON", "required_knowledge_ids": ["KNOW-PHYSICAL-CONTRADICTS", "KNOW-MARCUS-COVERUP", "KNOW-PERFECT-RECON"], "success_state_updates": {"inference_perfect_resolved": True}, "failure_preserves_investigation": True, "recovery_routes": ["REC-FLOOR-SCRAPE", "REC-CONTROL-REPORT"]},
        ],
        "recovery_routes": [
            {"route_id": "REC-FLOOR-SCRAPE", "player_action_label": "Return to the limestone scrape marks.", "destination_ref": "LOC-QUARRY-FLOOR", "action_ref": "ACT-LIMESTONE-SCRAPE"},
            {"route_id": "REC-CRUSHER-HYDRAULIC", "player_action_label": "Re-examine the hydraulic fluid stain.", "destination_ref": "LOC-CRUSHER", "action_ref": "ACT-HYDRAULIC-STAIN"},
            {"route_id": "REC-CRUSHER-TRACKS", "player_action_label": "Re-document the boot print trail.", "destination_ref": "LOC-CRUSHER", "action_ref": "ACT-BOOT-PRINTS"},
            {"route_id": "REC-MAINT-LOG", "player_action_label": "Review the maintenance inspection log again.", "destination_ref": "LOC-MAINT", "action_ref": "ACT-MAINT-RECORD"},
            {"route_id": "REC-CONTROL-REPORT", "player_action_label": "Re-read the incident report terminal.", "destination_ref": "LOC-CONTROL", "action_ref": "ACT-INCIDENT-REPORT"},
            {"route_id": "REC-RICK-WITNESS", "player_action_label": "Return to Rick Torres about platform timing.", "destination_ref": "LOC-YARD", "action_ref": "CONV-RICK"},
        ],
        "accusation_questionnaire": {
            "questionnaire_id": "ACC-QUARRY-SILENCE",
            "required_before_ending_eval": True,
            "multi_component": True,
            "questions": [
                {"question_id": "Q-WHO", "conclusion_id": "CONC-WHO", "answer_type": "npc_id", "player_label": "Who falsified the equipment-failure narrative?"},
                {"question_id": "Q-WHAT", "conclusion_id": "CONC-WHAT", "answer_type": "text", "player_label": "What happened to Carl Mendez?"},
                {"question_id": "Q-HOW", "conclusion_id": "CONC-HOW", "answer_type": "text", "player_label": "How was the cover-up executed?"},
                {"question_id": "Q-WHEN", "conclusion_id": "CONC-WHEN", "answer_type": "text", "player_label": "When did the fall occur?"},
            ],
            "accusation_complete_state_flag": "accusation_complete",
        },
        "deadline": {"enabled": True, "deadline_clock": "T_DEADLINE", "deadline_ending_id": "END-TIMEOUT", "blocks_accusation_after": True},
        "endings": [
            {"ending_id": "END-PERFECT", "ending_type": "perfect", "priority": 100, "unit_id": "END-PERFECT", "trigger": {"type": "state_driven", "required_state": {"accusation_complete": True, "inference_perfect_resolved": True}, "required_accusation": {"Q-WHO": "NPC-MARCUS"}}},
            {"ending_id": "END-PARTIAL-CULPRIT", "ending_type": "partial", "priority": 50, "unit_id": "END-PARTIAL-CULPRIT", "trigger": {"type": "state_driven", "required_state": {"accusation_complete": True, "inference_marcus_resolved": True}}},
            {"ending_id": "END-PARTIAL-PHYSICAL", "ending_type": "partial", "priority": 40, "unit_id": "END-PARTIAL-PHYSICAL", "trigger": {"type": "state_driven", "required_state": {"accusation_complete": True, "inference_physical_resolved": True}}},
            {"ending_id": "END-PARTIAL-WRONG", "ending_type": "partial", "priority": 30, "unit_id": "END-PARTIAL-WRONG", "trigger": {"type": "state_driven", "required_state": {"accusation_complete": True}, "wrong_accusation_allowed": True}},
            {"ending_id": "END-TIMEOUT", "ending_type": "timeout", "priority": 10, "unit_id": "END-TIMEOUT", "trigger": {"type": "deadline", "deadline_clock": "T_DEADLINE"}},
        ],
    }




def _player_units() -> dict:
    atmosphere = "Limestone dust, diesel exhaust, and morning fog hang over the active quarry."
    units: list[dict] = []

    def hub(uid, title, loc_id, choices, body=None):
        units.append({
            "unit_id": uid, "title": title, "player_file": "LOCATIONS", "unit_kind": "location_hub",
            "linked_location_id": loc_id,
            "prose": {"body": body or f"You are at the {title.lower()}. {atmosphere}"},
            "choices": choices, "meta": {"location_id": loc_id, "time_cost_minutes": 0},
        })

    hub("UNIT-YARD-BASE", "Quarry yard gate", "LOC-YARD", [
        {"label": "Descend to the quarry floor.", "destination_unit_id": "UNIT-QUARRY-FLOOR-BASE"},
        {"label": "Climb to the primary crusher platform.", "destination_unit_id": "UNIT-CRUSHER-BASE"},
        {"label": "Walk to the shift control shack.", "destination_unit_id": "UNIT-CONTROL-BASE"},
        {"label": "Cross to the maintenance bay.", "destination_unit_id": "UNIT-MAINT-BASE"},
        {"label": "Speak with shift supervisor Marcus Reed.", "destination_unit_id": "UNIT-NPC-MARCUS-HUB"},
        {"label": "Speak with coroner liaison Diana Okoro.", "destination_unit_id": "UNIT-NPC-DIANA-HUB"},
        {"label": "Speak with equipment operator Rick Torres.", "destination_unit_id": "UNIT-NPC-RICK-HUB"},
    ])
    hub("UNIT-QUARRY-FLOOR-BASE", "Quarry floor", "LOC-QUARRY-FLOOR", [
        {"label": "Examine limestone scrape marks at the impact zone.", "destination_unit_id": "UNIT-CHK-IMPACT-DECL"},
        {"label": "Return to the yard gate.", "destination_unit_id": "UNIT-YARD-BASE"},
        {"label": "Climb to the crusher platform.", "destination_unit_id": "UNIT-CRUSHER-BASE"},
    ])
    hub("UNIT-CRUSHER-BASE", "Primary crusher platform", "LOC-CRUSHER", [
        {"label": "Analyze hydraulic fluid stain on the deck.", "destination_unit_id": "UNIT-CHK-HYDRAULIC-DECL"},
        {"label": "Document mud boot print patterns.", "destination_unit_id": "UNIT-CHK-TRACKS-DECL"},
        {"label": "Speak with maintenance technician Elena Vasquez.", "destination_unit_id": "UNIT-NPC-ELENA-HUB"},
        {"label": "Return to the yard gate.", "destination_unit_id": "UNIT-YARD-BASE"},
    ])
    hub("UNIT-CONTROL-BASE", "Shift control shack", "LOC-CONTROL", [
        {"label": "Review the incident report terminal.", "destination_unit_id": "UNIT-OBJ-REPORT-MENU"},
        {"label": "Check the weather station log.", "destination_unit_id": "UNIT-OBJ-WEATHER-MENU"},
        {"label": "Return to the yard gate.", "destination_unit_id": "UNIT-YARD-BASE"},
    ])
    hub("UNIT-MAINT-BASE", "Maintenance bay", "LOC-MAINT", [
        {"label": "Review the maintenance inspection log.", "destination_unit_id": "UNIT-OBJ-MAINT-MENU"},
        {"label": "Return to the yard gate.", "destination_unit_id": "UNIT-YARD-BASE"},
        {"label": "Go to the crusher platform.", "destination_unit_id": "UNIT-CRUSHER-BASE"},
    ])

    def npc_hub(uid, title, loc_id, topics, return_to):
        units.append({
            "unit_id": uid, "title": title, "player_file": "NPCS", "unit_kind": "npc_interaction",
            "linked_location_id": loc_id,
            "prose": {"body": f"{title} meets you here. Their account may not match the physical evidence."},
            "choices": topics + [{"label": "End this conversation.", "destination_unit_id": return_to}],
            "meta": {"location_id": loc_id, "time_cost_minutes": 0},
        })

    npc_hub("UNIT-NPC-MARCUS-HUB", "Shift supervisor Marcus Reed", "LOC-YARD", [
        {"label": "Ask about the equipment-failure report.", "destination_unit_id": "UNIT-TOPIC-MARCUS-REPORT"},
        {"label": "Ask about wet deck conditions.", "destination_unit_id": "UNIT-TOPIC-MARCUS-SLIP"},
        {"label": "Ask about crusher safety interlock status.", "destination_unit_id": "UNIT-TOPIC-MARCUS-INTERLOCK"},
    ], "UNIT-YARD-BASE")
    npc_hub("UNIT-NPC-DIANA-HUB", "Coroner liaison Diana Okoro", "LOC-YARD", [
        {"label": "Ask about preliminary injury findings.", "destination_unit_id": "UNIT-TOPIC-DIANA-IMPACT"},
        {"label": "Ask what the quarry base scene suggests.", "destination_unit_id": "UNIT-TOPIC-DIANA-SCENE"},
        {"label": "Ask about hard hat placement.", "destination_unit_id": "UNIT-TOPIC-DIANA-HAT"},
    ], "UNIT-YARD-BASE")
    npc_hub("UNIT-NPC-ELENA-HUB", "Maintenance technician Elena Vasquez", "LOC-CRUSHER", [
        {"label": "Ask about hydraulic line condition.", "destination_unit_id": "UNIT-TOPIC-ELENA-HYDRAULIC"},
        {"label": "Ask about interlock inspection records.", "destination_unit_id": "UNIT-TOPIC-ELENA-INTERLOCK"},
        {"label": "Ask about normal failure patterns.", "destination_unit_id": "UNIT-TOPIC-ELENA-BASELINE"},
    ], "UNIT-CRUSHER-BASE")
    npc_hub("UNIT-NPC-RICK-HUB", "Equipment operator Rick Torres", "LOC-YARD", [
        {"label": "Ask who was on the crusher platform.", "destination_unit_id": "UNIT-TOPIC-RICK-PLATFORM"},
        {"label": "Ask about boot prints in the mud.", "destination_unit_id": "UNIT-TOPIC-RICK-BOOTS"},
        {"label": "Ask about timing before the alarm.", "destination_unit_id": "UNIT-TOPIC-RICK-TIMING"},
    ], "UNIT-YARD-BASE")

    topics = [
        ("UNIT-TOPIC-MARCUS-REPORT", "Marcus Reed", "Marcus taps the incident tablet with a grease-stained glove.", "Hydraulic line let go during Carl's inspection. Standard equipment failure — I filed at 0315 like protocol requires.", "UNIT-NPC-MARCUS-HUB", "UNIT-YARD-BASE"),
        ("UNIT-TOPIC-MARCUS-SLIP", "Marcus Reed", "Marcus gestures toward the crusher deck.", "Deck was slick from overnight mist. Carl lost footing near the feed gate.", "UNIT-NPC-MARCUS-HUB", "UNIT-YARD-BASE"),
        ("UNIT-TOPIC-MARCUS-INTERLOCK", "Marcus Reed", "Marcus avoids the interlock panel.", "Interlock passed inspection at shift start. Elena signed off on the log.", "UNIT-NPC-MARCUS-HUB", "UNIT-YARD-BASE"),
        ("UNIT-TOPIC-DIANA-IMPACT", "Diana Okoro", "Diana opens her field notes at the tape line.", "Preliminary findings show blunt impact consistent with a fall, not crush injury alone.", "UNIT-NPC-DIANA-HUB", "UNIT-YARD-BASE"),
        ("UNIT-TOPIC-DIANA-SCENE", "Diana Okoro", "Diana points toward the quarry base.", "Fresh scrape marks on the limestone suggest lateral contact before the body came to rest.", "UNIT-NPC-DIANA-HUB", "UNIT-YARD-BASE"),
        ("UNIT-TOPIC-DIANA-HAT", "Diana Okoro", "Diana photographs the platform railing.", "Carl's hard hat is on the platform railing, not at the base where you'd expect after a crush.", "UNIT-NPC-DIANA-HUB", "UNIT-YARD-BASE"),
        ("UNIT-TOPIC-ELENA-HYDRAULIC", "Elena Vasquez", "Elena holds up a cut hose sample.", "This line was cut with a blade, not burst by pressure. Splatter pattern confirms it.", "UNIT-NPC-ELENA-HUB", "UNIT-CRUSHER-BASE"),
        ("UNIT-TOPIC-ELENA-INTERLOCK", "Elena Vasquez", "Elena pulls the maintenance tablet.", "Marcus signed the interlock check, but the gate sensor shows it was bypassed hours earlier.", "UNIT-NPC-ELENA-HUB", "UNIT-CRUSHER-BASE"),
        ("UNIT-TOPIC-ELENA-BASELINE", "Elena Vasquez", "Elena spreads a reference chart on the bench.", "Catastrophic hydraulic failure leaves radial burst patterns. This stain is directional — a cut.", "UNIT-NPC-ELENA-HUB", "UNIT-CRUSHER-BASE"),
        ("UNIT-TOPIC-RICK-PLATFORM", "Rick Torres", "Rick keeps his eyes on the ground.", "Marcus was up on the platform around 0245. He told me to keep quiet about it.", "UNIT-NPC-RICK-HUB", "UNIT-YARD-BASE"),
        ("UNIT-TOPIC-RICK-BOOTS", "Rick Torres", "Rick scuffs the mud with his boot.", "Two sets of prints went to the railing that night. Carl's and a larger tread — supervisor issue.", "UNIT-NPC-RICK-HUB", "UNIT-YARD-BASE"),
        ("UNIT-TOPIC-RICK-TIMING", "Rick Torres", "Rick speaks barely above a whisper.", "Alarm came after Marcus came down alone. Carl never walked off that platform.", "UNIT-NPC-RICK-HUB", "UNIT-YARD-BASE"),
    ]
    for uid, speaker, scene, quote, hub_id, exit_id in topics:
        units.append({
            "unit_id": uid, "title": uid.replace("UNIT-TOPIC-", "Topic ").replace("-", " ").title(),
            "player_file": "NPCS", "unit_kind": "dialogue_topic",
            "prose": {"dialogue": {"scene": scene, "speaker": speaker, "prompt": "says", "quote": quote, "coda": "You note the answer in your case file."}},
            "choices": [
                {"label": f"Return to speaking with {speaker.split()[-1]}.", "destination_unit_id": hub_id},
                {"label": "Leave this conversation.", "destination_unit_id": exit_id},
            ],
            "meta": {"time_cost_minutes": 2},
        })

    obj_units = [
        ("UNIT-OBJ-REPORT-MENU", "Incident report terminal", "The terminal shows Marcus Reed's 0315 equipment-failure filing.", "UNIT-CONTROL-BASE", [("Read the filed incident narrative.", "UNIT-OBJ-REPORT-RESULT")]),
        ("UNIT-OBJ-REPORT-RESULT", "Incident report", "Report attributes death to hydraulic conveyor failure during solo inspection. No mention of platform fall.", "UNIT-CONTROL-BASE", []),
        ("UNIT-OBJ-WEATHER-MENU", "Weather station log", "Overnight precipitation and humidity readings are posted.", "UNIT-CONTROL-BASE", [("Review overnight weather data.", "UNIT-OBJ-WEATHER-RESULT")]),
        ("UNIT-OBJ-WEATHER-RESULT", "Weather log", "Station recorded dry conditions from 0200 onward. Deck wet-slip claim is unsupported.", "UNIT-CONTROL-BASE", []),
        ("UNIT-OBJ-MAINT-MENU", "Maintenance inspection log", "Shift interlock and hydraulic inspection entries are indexed here.", "UNIT-MAINT-BASE", [("Compare interlock log to equipment state.", "UNIT-OBJ-MAINT-RESULT")]),
        ("UNIT-OBJ-MAINT-RESULT", "Maintenance log", "Marcus signed interlock pass at shift start, but sensor logs show bypass at 0215.", "UNIT-MAINT-BASE", []),
    ]
    for uid, title, body, ret, extra in obj_units:
        choices = [{"label": lab, "destination_unit_id": dest} for lab, dest in extra]
        choices.append({"label": "Return to the location.", "destination_unit_id": ret})
        units.append({"unit_id": uid, "title": title, "player_file": "OBJECTS", "unit_kind": "object_interaction", "prose": {"body": body}, "choices": choices, "meta": {"time_cost_minutes": 2}})

    checks = [
        ("UNIT-CHK-IMPACT-DECL", "Limestone impact marks", "perception", "You measure fresh scrape marks on the quarry base limestone.", "UNIT-IMPACT-SUCCESS", "UNIT-IMPACT-FAIL", "UNIT-QUARRY-FLOOR-BASE"),
        ("UNIT-CHK-HYDRAULIC-DECL", "Hydraulic splatter", "technical", "You trace hydraulic fluid direction across the crusher deck.", "UNIT-HYDRAULIC-SUCCESS", "UNIT-HYDRAULIC-FAIL", "UNIT-CRUSHER-BASE"),
        ("UNIT-CHK-TRACKS-DECL", "Boot print reconstruction", "reasoning", "You map paired boot prints in the platform mud.", "UNIT-TRACKS-SUCCESS", "UNIT-TRACKS-FAIL", "UNIT-CRUSHER-BASE"),
    ]
    for decl, title, cap, setup, succ, fail, ret in checks:
        units.append({
            "unit_id": decl, "title": title, "player_file": "OBJECTS", "unit_kind": "check_declaration",
            "prose": {"setup": setup, "fact": "Roll d20 plus your modifier.", "coda": "Compare your result to the difficulty."},
            "choices": [
                {"label": "If your roll succeeds, read the success section.", "destination_unit_id": succ},
                {"label": "If your roll fails, read the failure section.", "destination_unit_id": fail},
            ],
            "meta": {"check": cap, "time_cost_minutes": 2},
        })

    check_results = [
        ("UNIT-IMPACT-SUCCESS", "Impact marks — success", "Scrape angle shows lateral impact before rest; dust scuff on railing confirms struggle at platform edge.", "UNIT-QUARRY-FLOOR-BASE", "check_success"),
        ("UNIT-IMPACT-FAIL", "Impact marks — failure", "The marks are visible but you cannot fix the impact sequence.", "UNIT-QUARRY-FLOOR-BASE", "check_failure"),
        ("UNIT-HYDRAULIC-SUCCESS", "Hydraulic splatter — success", "Fluid arcs from a cut line, not a burst fitting. Staging after platform incident is likely.", "UNIT-CRUSHER-BASE", "check_success"),
        ("UNIT-HYDRAULIC-FAIL", "Hydraulic splatter — failure", "The stain could be failure or cut without clearer measurement.", "UNIT-CRUSHER-BASE", "check_failure"),
        ("UNIT-TRACKS-SUCCESS", "Boot prints — success", "Two print sets converge at the railing at 0245 — Carl's and a supervisor tread. Hard hat on railing confirms fall, not crush at base.", "UNIT-CRUSHER-BASE", "check_success"),
        ("UNIT-TRACKS-FAIL", "Boot prints — failure", "Mud disturbance obscures the second print set.", "UNIT-CRUSHER-BASE", "check_failure"),
    ]
    for uid, title, body, ret, kind in check_results:
        units.append({"unit_id": uid, "title": title, "player_file": "OBJECTS", "unit_kind": kind, "prose": {"body": body}, "choices": [{"label": "Continue investigating." if "success" in kind else "Try another route.", "destination_unit_id": ret}]})

    scenes = [
        ("SC-YARD-ARRIVAL", "Arrival briefing", "County dispatch meets you at the yard gate as Marcus Reed waits with a printed incident summary.", "UNIT-YARD-BASE"),
        ("SC-FLOOR-SCENE", "Quarry floor survey", "Diana Okoro walks you along the taped impact zone at the quarry base.", "UNIT-QUARRY-FLOOR-BASE"),
        ("SC-CRUSHER-HYDRAULIC", "Hydraulic findings", "Elena Vasquez demonstrates the cut line sample on the crusher deck.", "UNIT-CRUSHER-BASE"),
        ("SC-MAINT-RECORDS", "Maintenance records pull", "The maintenance bay terminal finishes syncing overnight logs.", "UNIT-MAINT-BASE"),
        ("SC-CRUSHER-TRACKS", "Boot print documentation", "You photograph paired prints in the platform mud before wind dries them.", "UNIT-CRUSHER-BASE"),
        ("SC-FLOOR-IMPACT", "Impact measurement", "You triangulate scrape marks against coroner measurements.", "UNIT-QUARRY-FLOOR-BASE"),
        ("SC-ACCUSATION-PREP", "Final report prep", "You assemble the OSHA preliminary file for the questionnaire.", "UNIT-CONTROL-BASE"),
        ("SC-DEADLINE-WARN", "Deadline warning", "Dispatch warns the 1200 preliminary report window is closing.", "UNIT-YARD-BASE"),
    ]
    for uid, title, body, ret in scenes:
        units.append({"unit_id": uid, "title": title, "player_file": "SCENES", "unit_kind": "scene", "prose": {"body": body}, "choices": [{"label": "Continue.", "destination_unit_id": ret}, {"label": "Return to the location base.", "destination_unit_id": ret}], "meta": {"time_cost_minutes": 5}})

    inferences = [
        ("INF-PHYSICAL-CONFLICT", "Physical contradiction", "Which physical traces contradict the official equipment-failure report?", "UNIT-QUARRY-FLOOR-BASE"),
        ("INF-STAGING", "Staged failure", "What evidence suggests hydraulic failure was staged after a platform incident?", "UNIT-CRUSHER-BASE"),
        ("INF-MARCUS-COVERUP", "Supervisor accountability", "Who had opportunity to falsify incident and maintenance records?", "UNIT-CONTROL-BASE"),
        ("INF-PERFECT-RECON", "Full reconstruction", "Reconstruct the night: interlock bypass, platform fall, cut line, falsified logs.", "UNIT-CONTROL-BASE"),
    ]
    for uid, title, setup, ret in inferences:
        units.append({"unit_id": uid, "title": title, "player_file": "INFERENCE", "unit_kind": "inference", "prose": {"setup": setup, "fact": "Record your conclusion in the case file before proceeding."}, "choices": [{"label": "My conclusion matches the evidence.", "destination_unit_id": ret}, {"label": "I need more information.", "destination_unit_id": "UNIT-YARD-BASE"}], "meta": {"time_cost_minutes": 3}})

    recoveries = [
        ("REC-FLOOR-SCRAPE", "Floor Scrape", "Return to the limestone scrape marks.", "UNIT-CHK-IMPACT-DECL"),
        ("REC-CRUSHER-HYDRAULIC", "Crusher Hydraulic", "Re-examine the hydraulic fluid stain.", "UNIT-CHK-HYDRAULIC-DECL"),
        ("REC-CRUSHER-TRACKS", "Crusher Tracks", "Re-document the boot print trail.", "UNIT-CHK-TRACKS-DECL"),
        ("REC-MAINT-LOG", "Maint Log", "Review the maintenance inspection log again.", "UNIT-OBJ-MAINT-MENU"),
        ("REC-CONTROL-REPORT", "Control Report", "Re-read the incident report terminal.", "UNIT-OBJ-REPORT-MENU"),
        ("REC-RICK-WITNESS", "Rick Witness", "Return to Rick Torres about platform timing.", "UNIT-NPC-RICK-HUB"),
    ]
    for uid, title, body, dest in recoveries:
        units.append({"unit_id": uid, "title": title, "player_file": "RECOVERY", "unit_kind": "recovery", "prose": {"body": body}, "choices": [{"label": "Follow this recovery route.", "destination_unit_id": dest}]})

    endings = [
        ("END-PERFECT", "Perfect reconstruction", "You document interlock bypass, platform fall, cut hydraulic line, and Marcus Reed's falsified records before the OSHA deadline."),
        ("END-PARTIAL-CULPRIT", "Partial — culprit named", "You name Marcus Reed but miss part of the physical reconstruction."),
        ("END-PARTIAL-PHYSICAL", "Partial — physical only", "You disprove the equipment-failure narrative but stop short of naming the cover-up."),
        ("END-PARTIAL-WRONG", "Partial — wrong accusation", "Your report reaches OSHA on time but misassigns accountability."),
        ("END-TIMEOUT", "Deadline timeout", "The preliminary report window closes before you can support a determination."),
    ]
    for uid, title, body in endings:
        units.append({"unit_id": uid, "title": title, "player_file": "ENDINGS", "unit_kind": "ending", "prose": {"body": body}, "choices": []})

    return {
        "shell": {
            "opening": {"prose": "Limestone dust and diesel exhaust hang in the morning air as Marcus Reed meets you at the yard gate. Diana Okoro waits by the quarry floor tape with findings that already diverge from his report."},
            "how_to_play": {"sections": [
                {"heading": "Your role", "body": "You are a county occupational safety investigator verifying the official equipment-failure report."},
                {"heading": "Time", "body": "Track in-world time. OSHA preliminary report is due at 1200."},
                {"heading": "Checks", "body": "Roll d20 plus the modifier on your character sheet when prompted."},
            ]},
            "readme": {"body": "Fair-play mystery at an active limestone quarry. Reconstruct events from physical traces, equipment condition, and incident records."},
            "character_sheet": {
                "role": "County occupational safety investigator",
                "intro": "You investigate workplace fatalities and verify employer incident reports.",
                "modifiers": [
                    {"capability": "perception", "modifier": 2, "when_applies": "Physical inspection and environmental observation checks"},
                    {"capability": "reasoning", "modifier": 2, "when_applies": "Timeline and physical evidence reconstruction checks"},
                    {"capability": "technical", "modifier": 1, "when_applies": "Equipment and hydraulic system checks"},
                ],
                "equipment": "County tablet, measuring tape, evidence camera, pocket field guide.",
                "stakes": "File a supported preliminary report before the 1200 deadline.",
            },
            "case_file": "# Case file — The Quarry Silence\n\n## Physical evidence notes\n\n## Equipment cross-reference\n\n## Final determination\n",
            "navigation_index": {"entries": [
                {"label": "Locations", "file_ref": "PLAYER/LOCATIONS.md"},
                {"label": "NPCs", "file_ref": "PLAYER/NPCS.md"},
                {"label": "Objects", "file_ref": "PLAYER/OBJECTS.md"},
                {"label": "Scenes", "file_ref": "PLAYER/SCENES.md"},
                {"label": "Inference", "file_ref": "PLAYER/INFERENCE.md"},
                {"label": "Recovery", "file_ref": "PLAYER/RECOVERY.md"},
                {"label": "Endings", "file_ref": "PLAYER/ENDINGS.md"},
            ]},
        },
        "units": units,
    }


def _epistemic() -> dict:
    return {
        "start_template_unit_id": "UNIT-YARD-BASE",
        "initial_player_knowledge": ["KNOW-OPEN-01", "KNOW-OPEN-02", "KNOW-OPEN-03", "KNOW-OPEN-04"],
        "initial_observable_entities": ["NPC-MARCUS", "NPC-DIANA", "NPC-RICK"],
        "initial_observable_objects": ["OBJ-LIMESTONE-SCRAPE"],
        "hub_definitions": [
            {
                "hub_unit_id": "UNIT-YARD-BASE", "event_kind": "location_hub", "physical_location_id": "LOC-YARD",
                "observable_entities": ["NPC-MARCUS", "NPC-DIANA", "NPC-RICK"],
                "actions": [
                    {"label": "Descend to the quarry floor.", "destination_unit_id": "UNIT-QUARRY-FLOOR-BASE", "action_type": "nav"},
                    {"label": "Climb to the primary crusher platform.", "destination_unit_id": "UNIT-CRUSHER-BASE", "action_type": "nav"},
                    {"label": "Walk to the shift control shack.", "destination_unit_id": "UNIT-CONTROL-BASE", "action_type": "nav"},
                    {"label": "Cross to the maintenance bay.", "destination_unit_id": "UNIT-MAINT-BASE", "action_type": "nav"},
                    {"label": "Speak with shift supervisor Marcus Reed.", "destination_unit_id": "UNIT-NPC-MARCUS-HUB", "action_type": "conversation"},
                    {"label": "Speak with coroner liaison Diana Okoro.", "destination_unit_id": "UNIT-NPC-DIANA-HUB", "action_type": "conversation"},
                    {"label": "Speak with equipment operator Rick Torres.", "destination_unit_id": "UNIT-NPC-RICK-HUB", "action_type": "conversation"},
                ],
            },
            {
                "hub_unit_id": "UNIT-NPC-MARCUS-HUB", "event_kind": "npc_interaction", "physical_location_id": "LOC-YARD",
                "actions": [
                    {"label": "Ask about the equipment-failure report.", "destination_unit_id": "UNIT-TOPIC-MARCUS-REPORT", "action_type": "conversation", "investigative": True},
                    {"label": "Ask about wet deck conditions.", "destination_unit_id": "UNIT-TOPIC-MARCUS-SLIP", "action_type": "conversation", "investigative": True},
                    {"label": "Ask about crusher safety interlock status.", "destination_unit_id": "UNIT-TOPIC-MARCUS-INTERLOCK", "action_type": "conversation", "investigative": True},
                ],
            },
            {
                "hub_unit_id": "UNIT-NPC-DIANA-HUB", "event_kind": "npc_interaction", "physical_location_id": "LOC-YARD",
                "actions": [
                    {"label": "Ask about preliminary injury findings.", "destination_unit_id": "UNIT-TOPIC-DIANA-IMPACT", "action_type": "conversation", "investigative": True},
                    {"label": "Ask what the quarry base scene suggests.", "destination_unit_id": "UNIT-TOPIC-DIANA-SCENE", "action_type": "conversation", "investigative": True},
                    {"label": "Ask about hard hat placement.", "destination_unit_id": "UNIT-TOPIC-DIANA-HAT", "action_type": "conversation", "investigative": True},
                ],
            },
            {
                "hub_unit_id": "UNIT-NPC-ELENA-HUB", "event_kind": "npc_interaction", "physical_location_id": "LOC-CRUSHER",
                "actions": [
                    {"label": "Ask about hydraulic line condition.", "destination_unit_id": "UNIT-TOPIC-ELENA-HYDRAULIC", "action_type": "conversation", "investigative": True},
                    {"label": "Ask about interlock inspection records.", "destination_unit_id": "UNIT-TOPIC-ELENA-INTERLOCK", "action_type": "conversation", "investigative": True},
                    {"label": "Ask about normal failure patterns.", "destination_unit_id": "UNIT-TOPIC-ELENA-BASELINE", "action_type": "conversation", "investigative": True},
                ],
            },
            {
                "hub_unit_id": "UNIT-NPC-RICK-HUB", "event_kind": "npc_interaction", "physical_location_id": "LOC-YARD",
                "actions": [
                    {"label": "Ask who was on the crusher platform.", "destination_unit_id": "UNIT-TOPIC-RICK-PLATFORM", "action_type": "conversation", "investigative": True},
                    {"label": "Ask about boot prints in the mud.", "destination_unit_id": "UNIT-TOPIC-RICK-BOOTS", "action_type": "conversation", "investigative": True},
                    {"label": "Ask about timing before the alarm.", "destination_unit_id": "UNIT-TOPIC-RICK-TIMING", "action_type": "conversation", "investigative": True},
                ],
            },
        ],
        "topic_return_profiles": [
            {"unit_prefix": "UNIT-TOPIC-MARCUS", "hub_unit_id": "UNIT-NPC-MARCUS-HUB", "hub_label": "Return to Marcus.", "exit_unit_id": "UNIT-YARD-BASE", "exit_label": "Leave the conversation."},
            {"unit_prefix": "UNIT-TOPIC-DIANA", "hub_unit_id": "UNIT-NPC-DIANA-HUB", "hub_label": "Return to Diana.", "exit_unit_id": "UNIT-YARD-BASE", "exit_label": "Leave the conversation."},
            {"unit_prefix": "UNIT-TOPIC-ELENA", "hub_unit_id": "UNIT-NPC-ELENA-HUB", "hub_label": "Return to Elena.", "exit_unit_id": "UNIT-CRUSHER-BASE", "exit_label": "Leave the conversation."},
            {"unit_prefix": "UNIT-TOPIC-RICK", "hub_unit_id": "UNIT-NPC-RICK-HUB", "hub_label": "Return to Rick.", "exit_unit_id": "UNIT-YARD-BASE", "exit_label": "Leave the conversation."},
        ],
        "topic_knowledge_grants": {
            "UNIT-TOPIC-DIANA-IMPACT": ["KNOW-DIANA-IMPACT"],
            "UNIT-TOPIC-ELENA-HYDRAULIC": ["KNOW-ELENA-HYDRAULIC"],
            "UNIT-TOPIC-ELENA-INTERLOCK": ["KNOW-MAINT-FALSIFIED"],
            "UNIT-TOPIC-RICK-PLATFORM": ["KNOW-RICK-WITNESS"],
            "UNIT-TOPIC-MARCUS-REPORT": ["KNOW-INCIDENT-REPORT"],
        },
        "inference_choice_gates": [{"label_contains": "My conclusion matches the evidence", "requires_knowledge_ids": ["KNOW-PHYSICAL-CONTRADICTS"]}],
        "materialization": {"max_states": 500000},
    }


def _validator_seeds() -> dict:
    return {
        "story": {
            "story_frame": {
                "investigation_starts_where": "limestone quarry yard gate after night-shift fatality",
                "investigation_starts_when": "morning after incident discovery",
                "incident_description": "worker death at quarry base with official equipment-failure report",
                "incident_when": "night shift ending approximately 0315",
                "investigator_involvement": "county occupational safety investigator dispatched to verify incident report",
                "deadline_or_constraint": "OSHA preliminary report due at 1200",
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
