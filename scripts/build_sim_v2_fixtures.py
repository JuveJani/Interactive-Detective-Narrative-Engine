"""Build Simulator v2 test fixtures and .idne packages."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

from idne.idne_package import build_idne_package

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures"
GEN_SOLO = FIXTURES / "gen_v2_canonical_solo"
GEN_TWO = FIXTURES / "gen_v2_canonical_two_player"
BRIEF_SOLO = FIXTURES / "gen_v2_brief_solo.json"
BRIEF_TWO = FIXTURES / "gen_v2_brief_two_player.json"
IFLOW = FIXTURES / "iflow_valid_minimal" / "DO_NOT_READ" / "investigation_flow_package.json"

TWO_PLAYER_EXTRA_FILES = [
    "environment_manifest.json",
    "object_interaction_manifest.json",
    "investigation_manifest.json",
    "npc_investigation_manifest.json",
    "DO_NOT_READ/environment_package.json",
    "DO_NOT_READ/object_interaction_package.json",
    "DO_NOT_READ/investigation_core_package.json",
    "DO_NOT_READ/npc_investigation_package.json",
    "DO_NOT_READ/world_truth_package.json",
    "generation_manifest.json",
]


def _patched_flow(adventure_id: str) -> dict:
    flow = json.loads(IFLOW.read_text(encoding="utf-8"))
    flow["adventure_id"] = adventure_id
    flow["accusation_questionnaire"]["questions"] = [
        flow["accusation_questionnaire"]["questions"][0]
    ]
    for ending in flow["endings"]:
        if ending.get("ending_id") == "END-PERFECT":
            ending["trigger"]["required_accusation"] = {"Q-CULPRIT": "NPC-A"}
    return flow


def _minimal_cap(adventure_id: str, play_modes: list[str]) -> dict:
    return {
        "schema_version": "1.0",
        "adventure_id": adventure_id,
        "play_modes": play_modes,
        "investigation_core_links": {"package_path": "DO_NOT_READ/investigation_core_package.json"},
        "object_interaction_links": {"package_path": "DO_NOT_READ/object_interaction_package.json"},
        "npc_investigation_links": {"package_path": "DO_NOT_READ/npc_investigation_package.json"},
        "modifier_sources": [
            {
                "modifier_id": "MOD-PERCEPTION",
                "capability_category": "perception_observation",
                "source": "character_sheet.perception",
            }
        ],
        "resolution_model": {"formula": "d20 + character_modifier", "success_when": "result >= dc"},
        "difficulty_bands": {"easy": 5, "medium": 10, "hard": 15},
        "destination_units": [
            {
                "unit_id": "UNIT-CHK-DECL",
                "player_text": "Search carefully.",
                "exposes_success_content": False,
                "exposes_failure_content": False,
            },
            {"unit_id": "UNIT-SUCCESS", "player_text": "You notice fresh scuff marks."},
            {"unit_id": "UNIT-FAIL", "player_text": "You find nothing useful."},
        ],
        "checks": [
            {
                "check_id": "CHK-OBS-SCUff",
                "parent_action_id": "ACT-SEARCH-DESK",
                "parent_action_layer": "object_interaction",
                "parent_action_type": "search",
                "player_action_label": "Search the desk carefully.",
                "capability": "perception",
                "capability_category": "perception_observation",
                "modifier_source_id": "MOD-PERCEPTION",
                "dc": 10,
                "dc_justification": "Hidden scuff requires careful observation",
                "why_check_exists": "Reveal observation knowledge",
                "success_enables": "Scuff mark knowledge",
                "failure_consequence": "Miss observation; alternate route via testimony",
                "alternate_route_exists": True,
                "attempt_policy": {"default": "one_attempt"},
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
                    "success_destination": "UNIT-SUCCESS",
                    "failure_destination": "UNIT-FAIL",
                },
                "success_effects": {"grants_knowledge_ids": ["KNOW-001"], "npc_social_effects": []},
                "failure_effects": {"npc_social_effects": []},
                "information_trace": {
                    "fixed_truth_ref": "WF-001",
                    "source_layer": "observation",
                    "source_id": "OBS-001",
                    "observation_id": "OBS-001",
                },
            }
        ],
    }


def _write_flow_cap(dest: Path, adventure_id: str, play_modes: list[str]) -> None:
    (dest / "DO_NOT_READ" / "investigation_flow_package.json").write_text(
        json.dumps(_patched_flow(adventure_id), indent=2),
        encoding="utf-8",
    )
    (dest / "investigation_flow_manifest.json").write_text(
        json.dumps(
            {
                "schema_version": "1.0",
                "investigation_flow_method": "canonical",
                "package_path": "DO_NOT_READ/investigation_flow_package.json",
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    (dest / "DO_NOT_READ" / "capability_check_package.json").write_text(
        json.dumps(_minimal_cap(adventure_id, play_modes), indent=2),
        encoding="utf-8",
    )
    (dest / "capability_check_manifest.json").write_text(
        json.dumps(
            {
                "schema_version": "1.0",
                "capability_check_method": "canonical",
                "package_path": "DO_NOT_READ/capability_check_package.json",
            },
            indent=2,
        ),
        encoding="utf-8",
    )


def build_adventure_fixture(name: str, source: Path, brief: Path, play_modes: list[str]) -> Path:
    dest = FIXTURES / name
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(source, dest)
    if name == "sim_v2_two_player":
        for rel in TWO_PLAYER_EXTRA_FILES:
            src = GEN_SOLO / rel
            if src.exists():
                target = dest / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, target)
    _write_flow_cap(dest, name, play_modes)
    brief_data = json.loads(brief.read_text(encoding="utf-8"))
    (dest / "play_manifest.json").write_text(
        json.dumps(
            {
                "schema_version": "1.0",
                "play_modes": play_modes,
                "single_investigator": {"enabled": "single_investigator" in play_modes},
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    (dest / "brief").mkdir(exist_ok=True)
    (dest / "brief/adventure_brief.json").write_text(json.dumps(brief_data, indent=2), encoding="utf-8")
    return dest


def build_idne_fixture(adventure_dir: Path, brief: Path, out_name: str) -> Path:
    workspace = FIXTURES / f"{out_name}_workspace"
    if workspace.exists():
        shutil.rmtree(workspace)
    workspace.mkdir(parents=True)
    brief_dir = workspace / "brief"
    brief_dir.mkdir()
    shutil.copy2(brief, brief_dir / "adventure_brief.json")
    gen_dir = workspace / "generation"
    gen_dir.mkdir()
    (gen_dir / "generation_state.json").write_text(
        json.dumps(
            {
                "schema_version": "1.0",
                "adventure_id": out_name,
                "readiness_status": "PRE_PLAYTEST",
                "logic_validation_complete": True,
                "stage_status": {"package_export": "COMPLETE", "final_validation": "COMPLETE"},
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    out = FIXTURES / f"{out_name}.idne"
    build_idne_package(
        adventure_dir,
        out,
        out_name,
        extra_roots={"brief": brief_dir, "generation": gen_dir},
    )
    return out


def main() -> None:
    solo = build_adventure_fixture("sim_v2_solo", GEN_SOLO, BRIEF_SOLO, ["single_investigator"])
    two = build_adventure_fixture(
        "sim_v2_two_player", GEN_TWO, BRIEF_TWO, ["two_player"]
    )
    build_idne_fixture(solo, BRIEF_SOLO, "sim_v2_solo")
    build_idne_fixture(two, BRIEF_TWO, "sim_v2_two_player")

    missing = FIXTURES / "sim_v2_missing_layer"
    if missing.exists():
        shutil.rmtree(missing)
    shutil.copytree(GEN_SOLO, missing)

    validation_fail = FIXTURES / "sim_v2_validation_fail"
    if validation_fail.exists():
        shutil.rmtree(validation_fail)
    shutil.copytree(solo, validation_fail)
    wt = json.loads((validation_fail / "DO_NOT_READ/world_truth_package.json").read_text())
    wt["world_state_timeline"]["snapshots"] = []
    (validation_fail / "DO_NOT_READ/world_truth_package.json").write_text(
        json.dumps(wt, indent=2),
        encoding="utf-8",
    )

    print("sim_v2 fixtures built")


if __name__ == "__main__":
    main()
