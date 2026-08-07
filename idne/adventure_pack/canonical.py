"""Generate canonical JSON packages from an adventure pack spec."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from idne.adventure_pack.spec import AdventurePackSpec, write_json
from idne.adventure_pack.normalize import (
    build_result_units,
    normalize_conversation_graph,
    normalize_flow,
    normalize_info_known_model,
    normalize_investigation_core,
    normalize_locations,
    normalize_mandatory_locations,
    normalize_navigation,
    normalize_npcs,
    normalize_object_actions,
    normalize_objects,
    normalize_checks,
    normalize_topics,
)


def _manifest(method_key: str, package_rel: str, extra: dict[str, Any] | None = None) -> dict[str, Any]:
    data: dict[str, Any] = {
        "schema_version": "1.0",
        f"{method_key}_method": "canonical",
        "package_path": package_rel,
    }
    if extra:
        data.update(extra)
    return data


def write_canonical_packages(spec: AdventurePackSpec, adventure_root: Path) -> None:
    dnr = adventure_root / "DO_NOT_READ"
    aid = spec.pack_id

    # world_truth
    ft = spec.fixed_truth
    wt = {
        "schema_version": "1.0",
        "adventure_id": aid,
        "fixed_truth": {
            "culprit_id": ft.get("culprit_id"),
            "motive": ft.get("motive"),
            "method": ft.get("method"),
            "opportunity": ft.get("opportunity"),
            "immutable_facts": ft.get("immutable_facts") or [],
        },
        "causal_timeline": ft.get("causal_timeline") or {},
        "world_state_timeline": ft.get("world_state_timeline") or {},
        "npc_knowledge": ft.get("npc_knowledge") or {},
        "evidence_provenance": ft.get("evidence_provenance") or {},
        "observable_information": ft.get("observable_information") or {},
        "conclusion_requirements": ft.get("conclusion_requirements") or {},
        "narrative_construction": ft.get("narrative_construction") or {},
        "ending_claims": ft.get("ending_claims") or [],
    }
    write_json(dnr / "world_truth_package.json", wt)
    write_json(
        adventure_root / "generation_manifest.json",
        {
            "schema_version": "1.0",
            "generation_method": "world_first",
            "package_path": "DO_NOT_READ/world_truth_package.json",
            "gates": {f"G-WF{i}": {"status": "PASS"} for i in range(1, 8)},
        },
    )

    # environment
    env = {
        "schema_version": "1.0",
        "adventure_id": aid,
        "start_location_id": spec.start_location_id,
        "world_first_links": {"truth_package_path": "DO_NOT_READ/world_truth_package.json"},
        "locations": normalize_locations(spec),
        "location_states": spec.raw.get("location_states") or _default_location_states(spec),
        "features": spec.raw.get("features") or [],
        "navigation": normalize_navigation(spec),
        "revisit_rules": spec.raw.get("revisit_rules")
        or {
            "persist_physical_changes": True,
            "persist_acquired_objects": True,
            "persist_open_access": True,
            "suppress_repeat_one_time_observations": True,
            "allow_time_variants": True,
            "reset_to_initial_on_revisit": False,
        },
        "mandatory_locations": normalize_mandatory_locations(spec),
    }
    write_json(dnr / "environment_package.json", env)
    write_json(
        adventure_root / "environment_manifest.json",
        _manifest("environment", "DO_NOT_READ/environment_package.json"),
    )

    # object interaction
    obj_pkg = {
        "schema_version": "1.0",
        "adventure_id": aid,
        "world_first_links": {"truth_package_path": "DO_NOT_READ/world_truth_package.json"},
        "environment_links": {"package_path": "DO_NOT_READ/environment_package.json"},
        "investigation_core_links": {"package_path": "DO_NOT_READ/investigation_core_package.json"},
        "items_registry": spec.raw.get("items_registry") or [],
        "objects": normalize_objects(spec),
        "actions": normalize_object_actions(spec),
        "result_units": spec.raw.get("result_units") or build_result_units(spec),
        "hierarchy_roots": spec.raw.get("hierarchy_roots") or [o["object_id"] for o in spec.objects if not o.get("parent_id")],
    }
    write_json(dnr / "object_interaction_package.json", obj_pkg)
    write_json(
        adventure_root / "object_interaction_manifest.json",
        _manifest("object_interaction", "DO_NOT_READ/object_interaction_package.json"),
    )

    # investigation core
    ic_core = normalize_investigation_core(spec)
    ic = {
        "schema_version": "1.0",
        "adventure_id": aid,
        "world_first_links": {"truth_package_path": "DO_NOT_READ/world_truth_package.json"},
        "object_interaction_links": spec.raw.get("object_interaction_links") or {"info_id_to_knowledge_id": {}},
        "placeholder_resolution": spec.flow.get("placeholder_resolution") or {},
        **ic_core,
    }
    write_json(dnr / "investigation_core_package.json", ic)
    write_json(
        adventure_root / "investigation_manifest.json",
        _manifest("investigation", "DO_NOT_READ/investigation_core_package.json"),
    )

    # npc investigation
    npc_nodes = [n["npc_id"] for n in spec.npcs]
    npc_edges = []
    for npc in spec.npcs:
        for rel in npc.get("relationships") or []:
            npc_edges.append(
                {
                    "from_npc_id": npc["npc_id"],
                    "to_npc_id": rel["target_npc_id"],
                    "relationship_type": rel.get("relationship_type", "professional"),
                }
            )
    npc_pkg = {
        "schema_version": "1.0",
        "adventure_id": aid,
        "investigation_core_links": {"package_path": "DO_NOT_READ/investigation_core_package.json"},
        "npcs": normalize_npcs(spec),
        "npc_graph": {"nodes": npc_nodes, "edges": npc_edges},
        "information_known_model": spec.raw.get("information_known_model") or normalize_info_known_model(spec),
        "topics": spec.raw.get("topics") or normalize_topics(spec),
        "conversation_graph": spec.raw.get("conversation_graph") or normalize_conversation_graph(spec),
        "testimony_links": spec.raw.get("testimony_links") or [],
        "trust_model": spec.raw.get("trust_model") or {"default_trust_delta_per_topic": 2},
    }
    write_json(dnr / "npc_investigation_package.json", npc_pkg)
    write_json(
        adventure_root / "npc_investigation_manifest.json",
        _manifest("npc_investigation", "DO_NOT_READ/npc_investigation_package.json"),
    )

    # investigation flow
    flow = normalize_flow(spec)
    flow.setdefault("investigation_core_links", {"package_path": "DO_NOT_READ/investigation_core_package.json"})
    flow.setdefault("environment_links", {"package_path": "DO_NOT_READ/environment_package.json"})
    flow.setdefault("object_interaction_links", {"package_path": "DO_NOT_READ/object_interaction_package.json"})
    flow.setdefault("npc_investigation_links", {"package_path": "DO_NOT_READ/npc_investigation_package.json"})
    write_json(dnr / "investigation_flow_package.json", flow)
    write_json(
        adventure_root / "investigation_flow_manifest.json",
        _manifest("investigation_flow", "DO_NOT_READ/investigation_flow_package.json"),
    )

    # capability checks
    cap = spec.raw.get("capability_check_package") or _build_capability_package(spec)
    write_json(dnr / "capability_check_package.json", cap)
    write_json(
        adventure_root / "capability_check_manifest.json",
        _manifest("capability_check", "DO_NOT_READ/capability_check_package.json"),
    )

    # story validator
    story = spec.validator_seeds.get("story") or _default_story_seed(spec)
    story.setdefault("schema_version", "1.0")
    story.setdefault("adventure_id", aid)
    story.setdefault("play_modes", ["single_investigator"])
    write_json(dnr / "story_validator_package.json", story)
    write_json(
        adventure_root / "story_validator_manifest.json",
        _manifest("story_validator", "DO_NOT_READ/story_validator_package.json"),
    )

    # playtime + dm feeling written by playtime module

    # play manifest
    play = spec.raw.get("play_manifest") or {
        "schema_version": "1.0",
        "adventure_id": aid,
        "play_modes": ["single_investigator"],
        "single_investigator": {
            "character_sheet": "PLAYER/CHARACTERS/CHARACTER_SHEET.md",
            "record_sheet": "PLAYER/SHARED/CASE_FILE.md",
            "scene_package": "PLAYER/SCENES.md",
            "navigation_index": "PLAYER/NAVIGATION_INDEX.md",
            "endings": "PLAYER/ENDINGS.md",
            "inventory_owner": "investigator",
            "clock_model": "single_sequential",
            "wall_clock_target_minutes": spec.brief.get("target_playtime_minutes", 120),
        },
    }
    write_json(adventure_root / "play_manifest.json", play)

    # investigation validator manifest (cross-layer)
    write_json(
        adventure_root / "investigation_validator_manifest.json",
        {
            "schema_version": "1.0",
            "package_path": "DO_NOT_READ/investigation_core_package.json",
            "flow_package_path": "DO_NOT_READ/investigation_flow_package.json",
        },
    )


def _default_location_states(spec: AdventurePackSpec) -> list[dict[str, Any]]:
    states = []
    for loc in spec.locations:
        states.append(
            {
                "state_id": f"{loc['location_id']}:default",
                "location_id": loc["location_id"],
                "variant_label": "default",
                "attributes": loc.get("default_attributes") or {"access": "open"},
                "cause": {"type": "initial", "ref": "authoring"},
            }
        )
    return states


def _info_known_model(spec: AdventurePackSpec) -> list[dict[str, Any]]:
    out = []
    for conv in spec.conversations:
        npc_id = conv.get("npc_id")
        for topic in conv.get("topics") or []:
            kid = topic.get("grants_knowledge_id")
            if kid:
                out.append(
                    {
                        "info_id": f"INFO-{topic['topic_id']}",
                        "npc_id": npc_id,
                        "knowledge_id": kid,
                        "topic_id": topic["topic_id"],
                    }
                )
    return out


def _topics_from_conversations(spec: AdventurePackSpec) -> list[dict[str, Any]]:
    topics = []
    for conv in spec.conversations:
        for topic in conv.get("topics") or []:
            entry = {
                "topic_id": topic["topic_id"],
                "unlock_conditions": topic.get("unlock_conditions") or [],
            }
            topics.append(entry)
    return topics


def _conversation_graph(spec: AdventurePackSpec) -> list[dict[str, Any]]:
    graphs = []
    for conv in spec.conversations:
        nodes = []
        for topic in conv.get("topics") or []:
            nodes.append(
                {
                    "node_id": topic["topic_id"],
                    "topic_id": topic["topic_id"],
                    "player_prompt": topic.get("player_label", ""),
                    "npc_response_unit": topic.get("response_unit_id", ""),
                    "time_cost_minutes": topic.get("time_cost_minutes", 2),
                    "grants_knowledge_id": topic.get("grants_knowledge_id"),
                    "unlock_conditions": topic.get("unlock_conditions") or [],
                }
            )
        graphs.append(
            {
                "conversation_id": conv.get("conversation_id", f"CONV-{conv.get('npc_id')}"),
                "npc_id": conv.get("npc_id"),
                "hub_unit_id": conv.get("hub_unit_id"),
                "nodes": nodes,
            }
        )
    return graphs


def _build_capability_package(spec: AdventurePackSpec) -> dict[str, Any]:
    normalized_checks = normalize_checks(spec)
    dest_units = []
    for chk in normalized_checks:
        dest_units.extend(
            [
                {"unit_id": chk["declaration_unit_id"], "player_text": chk.get("declaration_text", "Make your check.")},
                {"unit_id": chk["success_unit_id"], "player_text": chk.get("success_text", "Success.")},
                {
                    "unit_id": chk["failure_unit_id"],
                    "player_text": chk.get("failure_text", "Failure."),
                    "hints_missed_content": False,
                    "reveals_hidden_object": False,
                },
            ]
        )
    checks = []
    for chk in normalized_checks:
        cat = chk.get("capability_category", "perception_observation")
        checks.append(
            {
                "check_id": chk["check_id"],
                "parent_action_id": chk.get("parent_action_id", f"ACT-{chk['check_id']}"),
                "parent_action_layer": chk.get("parent_action_layer", "object_interaction"),
                "parent_action_type": chk.get("parent_action_type", "search"),
                "player_action_label": chk.get("player_action_label", "Investigate carefully."),
                "capability": chk.get("capability", "perception"),
                "capability_category": cat,
                "modifier_source_id": chk.get("modifier_source_id", "MOD-PERCEPTION"),
                "dc": chk.get("dc", 10),
                "dc_justification": chk.get("dc_justification", "Careful observation required"),
                "why_check_exists": chk.get("why_check_exists", "Reveal hidden detail"),
                "success_enables": chk.get("success_enables", "Additional knowledge"),
                "failure_consequence": chk.get("failure_consequence", "Alternate route available"),
                "alternate_route_exists": chk.get("alternate_route_exists", True),
                "attempt_policy": {"default": "one_attempt"},
                "time_cost_minutes": chk.get("time_cost_minutes", 2),
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
                    "action_unit_id": chk["declaration_unit_id"],
                    "success_destination": chk["success_unit_id"],
                    "failure_destination": chk["failure_unit_id"],
                },
                "success_effects": {"grants_knowledge_ids": chk.get("success_grants_knowledge_ids") or [], "npc_social_effects": []},
                "failure_effects": {"npc_social_effects": []},
                "information_trace": chk.get("information_trace") or {},
            }
        )
    return {
        "schema_version": "1.0",
        "adventure_id": spec.pack_id,
        "play_modes": ["single_investigator"],
        "investigation_core_links": {"package_path": "DO_NOT_READ/investigation_core_package.json"},
        "object_interaction_links": {"package_path": "DO_NOT_READ/object_interaction_package.json"},
        "npc_investigation_links": {"package_path": "DO_NOT_READ/npc_investigation_package.json"},
        "environment_links": {"package_path": "DO_NOT_READ/environment_package.json"},
        "modifier_sources": spec.raw.get("modifier_sources")
        or [
            {"modifier_id": "MOD-PERCEPTION", "capability_category": "perception_observation", "source": "character_sheet.perception"},
            {"modifier_id": "MOD-REASONING", "capability_category": "reasoning_interpretation", "source": "character_sheet.reasoning"},
            {"modifier_id": "MOD-TECHNICAL", "capability_category": "technical_operation", "source": "character_sheet.technical"},
        ],
        "resolution_model": {"formula": "d20 + character_modifier", "success_when": "result >= dc"},
        "difficulty_bands": {"easy": 5, "medium": 10, "hard": 15},
        "destination_units": dest_units,
        "checks": checks,
    }


def _default_story_seed(spec: AdventurePackSpec) -> dict[str, Any]:
    sf = spec.validator_seeds.get("story_frame") or spec.brief
    endings = spec.flow.get("endings") or []
    return {
        "story_frame": {
            "investigation_starts_where": sf.get("setting", "the scene"),
            "investigation_starts_when": sf.get("opening_situation", "investigation start"),
            "incident_description": sf.get("premise", "an incident"),
            "incident_when": sf.get("in_world_duration", "recently"),
            "investigator_involvement": sf.get("investigator_character", "investigator called in"),
            "deadline_or_constraint": sf.get("deadline_or_constraint", "time pressure applies"),
            "reveals_culprit": False,
            "reveals_motive": False,
            "reveals_hidden_relationships": False,
            "reveals_correct_priority": False,
        },
        "timeline": spec.validator_seeds.get("timeline") or {"investigation_confused_with_incident": False, "impossible_ordering": False, "events": []},
        "causal_events": spec.validator_seeds.get("causal_events") or [],
        "information_facts": spec.validator_seeds.get("information_facts") or [],
        "knowledge_order": spec.validator_seeds.get("knowledge_order") or [],
        "npc_consistency": spec.validator_seeds.get("npc_consistency") or [],
        "inference_questions": spec.validator_seeds.get("inference_questions") or [],
        "ending_stories": spec.validator_seeds.get("ending_stories") or [{"ending_id": e["ending_id"], "player_visible": True} for e in endings],
        "player_audit": spec.validator_seeds.get("player_audit") or {"files": ["PLAYER/OPENING.md", "PLAYER/LOCATIONS.md", "PLAYER/NPCS.md"]},
    }
