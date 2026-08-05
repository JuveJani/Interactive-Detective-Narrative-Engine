# Architecture Map

High-level flow for IDNE canonical adventures. **Authoritative details live in linked specs** — this map orients agents only.

```text
Approved Brief
     │
     ▼
┌─────────────┐     ┌──────────────────┐
│ World First │────▶│ Fixed Truth +    │
│ (M1)        │     │ causal timeline  │
└─────────────┘     └────────┬─────────┘
                             │
     ┌───────────────────────┼───────────────────────┐
     ▼                       ▼                       ▼
┌──────────┐          ┌─────────────┐          ┌─────────────┐
│Environment│         │ Object      │          │ Investigation│
│ (M2)     │          │ Interaction │          │ Core (M4)   │
└──────────┘          │ (M3)        │          └─────────────┘
     │                  └─────────────┘                 │
     └──────────────────────┬────────────────────────────┘
                            ▼
              ┌─────────────────────────┐
              │ NPC Investigation (M5B) │
              │ Investigation Flow (M5C)│
              │ Capability Check (M6)   │
              └────────────┬────────────┘
                           ▼
              ┌─────────────────────────┐
              │ Adventure Generator v2  │  ← staged layer pipeline
              │ (M11) idne/generate/    │
              └────────────┬────────────┘
                           ▼
              ┌─────────────────────────┐
              │ .idne canonical package │
              └────────────┬────────────┘
                           ▼
              ┌─────────────────────────┐
              │ Integrated Validators   │  ← idne.validate_adventure
              │ M7–M10 + layer validators│
              └────────────┬────────────┘
                           ▼
              ┌─────────────────────────┐
              │ Simulator v2            │  ← idne.sim_v2
              │ trace / simulate / diag │
              └────────────┬────────────┘
                           ▼
              ┌─────────────────────────┐
              │ Findings + repair advise│  ← reports, OFFLINE_AI export
              │ (human approval required)│
              └─────────────────────────┘
```

## Key repository locations

| Layer | Spec | Code | Validate |
|-------|------|------|----------|
| Engine | `IDNE_ENGINE_v0.4.md` | — | — |
| Workflow | `IDNE_DEVELOPMENT_WORKFLOW.md` | — | — |
| World First | `WORLD_FIRST_GENERATION_SPEC.md` | `idne/world_first_validate.py` | `python -m idne.world_first_validate` |
| Environment | `ENVIRONMENT_SYSTEM_SPEC.md` | `idne/environment_validate.py` | integrated |
| Objects | `OBJECT_INTERACTION_SYSTEM_SPEC.md` | `idne/object_interaction_validate.py` | integrated |
| Investigation core | `INVESTIGATION_CORE_SPEC.md` | `idne/investigation_core_validate.py` | integrated |
| NPC | `NPC_INVESTIGATION_SYSTEM_SPEC.md` | `idne/npc_investigation_validate.py` | integrated |
| Flow | `INVESTIGATION_FLOW_SPEC.md` | `idne/investigation_flow_validate.py` | integrated |
| Capability | `CAPABILITY_CHECK_SYSTEM_SPEC.md` | `idne/capability_check_validate.py` | integrated |
| Generator v2 | `ADVENTURE_GENERATOR_V2_SPEC.md` | `idne/generate/` | stage + integrated |
| Simulator v2 | `SIMULATOR_V2_SPEC.md` | `simulator_v2/`, `idne/sim_v2/` | `python -m idne.sim_v2` |
| Legacy sim | `SIMULATOR_README.md` | `simulator/`, `idne_sim.py` | deprecated for `.idne` |
| Schemas | `idne/schemas/` | JSON schemas per layer | — |
| Fixtures | `tests/fixtures/` | canonical test packages | — |

## Integrated validation entry point

```bash
python -m idne.validate_adventure <adventure_root>
```

## Simulator v2 entry point

```bash
python -m idne.sim_v2 validate tests/fixtures/sim_v2_solo.idne
python -m idne.sim_v2 diagnose tests/fixtures/sim_v2_solo.idne
```

## Repair boundary

- **Generator repair:** `idne/generate/repair.py` — schema-level auto-repair during generation.
- **Simulator repair advisor:** suggestions only in reports; no automatic adventure edits.
- Human approval required for adventure logic changes.
