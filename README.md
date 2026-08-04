# Interactive Detective Narrative Engine (IDNE)

A reusable specification for creating fair-play interactive detective gamebooks.

## Current status

**Engine Specification 2.0:** In Development  
**Repository release:** 0.1

## Main modules

- Engine Specification
- Data Dictionary
- Templates
- Adventures
- Reviews
- Changelog

## Current milestone

**Milestone 1 — Single Investigator Mode** (complete).

Normative spec: `SINGLE_INVESTIGATOR_MODE_SPEC.md`. Engine §6.8 and §0.5. Validation: `python3 -m idne.single_investigator_validate`.

**Milestone 2 — World-First Generation** (complete).

Normative spec: `WORLD_FIRST_GENERATION_SPEC.md`. Validation: `python3 -m idne.world_first_validate`.

**Milestone 3 — Environment System** (complete).

Normative spec: `ENVIRONMENT_SYSTEM_SPEC.md`. Validation: `python3 -m idne.environment_validate`.

**Milestone 4 — Object Interaction System** (complete).

Normative spec: `OBJECT_INTERACTION_SYSTEM_SPEC.md`. Validation: `python3 -m idne.object_interaction_validate`.

**Milestone 5A — Investigation Core** (complete).

Normative spec: `INVESTIGATION_CORE_SPEC.md`. Validation: `python3 -m idne.investigation_core_validate`.

**Milestone 5B — NPC Investigation System** (complete).

Normative spec: `NPC_INVESTIGATION_SYSTEM_SPEC.md`. Validation: `python3 -m idne.npc_investigation_validate`.

**Milestone 5C — Investigation Flow & Ending System** (complete).

Normative specs: `INVESTIGATION_FLOW_SPEC.md`, `ENDING_SYSTEM_SPEC.md`. Validation: `python3 -m idne.investigation_flow_validate`.

**Milestone 6 — Capability Check System** (complete).

Normative spec: `CAPABILITY_CHECK_SYSTEM_SPEC.md`. Validation: `python3 -m idne.capability_check_validate`.

**Milestone 7 — Investigation Validator** (complete).

Normative spec: `INVESTIGATION_VALIDATOR_SPEC.md`. Validation: `python3 -m idne.investigation_validate`.

**Milestone 8 — Story Validator** (complete).

Normative spec: `STORY_VALIDATOR_SPEC.md`. Validation: `python3 -m idne.story_validate`.

**Milestone 9 — Playtime Calibration** (complete).

Normative spec: `PLAYTIME_CALIBRATION_SPEC.md`. Validation: `python3 -m idne.playtime_validate`.

**Milestone 10 — DM Feeling Validator** (complete).

Normative spec: `DM_FEELING_VALIDATOR_SPEC.md`. Validation: `python3 -m idne.dm_feeling_validate`.

**Milestone 11 — Adventure Generator v2** (complete).

Normative spec: `ADVENTURE_GENERATOR_V2_SPEC.md`. Generation: `python3 -m idne.generate <brief>`. Integrated validation: `python3 -m idne.validate_adventure <adventure_root>`. Offline setup: `OFFLINE_SETUP_WINDOWS.md`.

## First reference adventure

**The Last Witness**

The adventure is kept separate from the reusable engine specification.
