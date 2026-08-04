# Adventure Generator v2 — Normative Specification

**Milestone:** 11  
**Status:** Normative for staged offline adventure generation  
**Aligned with:** `IDNE_ENGINE_v0.4.md`, `IDNE_DEVELOPMENT_WORKFLOW.md`, Milestones 1–10 validators

---

## 1. Purpose

Adventure Generator v2 creates a complete IDNE adventure from a **human-approved brief** using a **staged pipeline**. One model call MUST NOT generate the entire adventure in a single pass.

The generator MUST:

- generate, validate, repair, save, and resume **one canonical layer at a time**;
- support `single_investigator` and `two_player`;
- support static-book and future AI-DM delivery;
- support cloud or local LLM backends via a provider-independent adapter;
- run fully offline when a local backend is configured.

---

## 2. Canonical generation pipeline

Generate in this order:

1. Approved adventure brief  
2. Fixed Truth  
3. Causal Timeline  
4. World-State Timeline  
5. NPCs, motivations, relationships, knowledge  
6. Environment  
7. Object hierarchy and interactions  
8. Investigation Core  
9. NPC conversation graph  
10. Investigation flow and endings  
11. Capability checks  
12. Story and PLAYER content  
13. Playtime metadata  
14. DM-feeling evidence  
15. Final integrated validation  
16. Package export  

**MUST NOT** generate PLAYER content before canonical logic layers pass validation.

---

## 3. Stage behavior

Every stage MUST:

- receive only stage-specific context;
- produce machine-readable output;
- save output before validation;
- run the relevant validator;
- classify findings;
- build a repair request with relevant errors and source context only;
- retry up to a configurable maximum;
- stop on unresolved Critical or Major findings;
- preserve earlier approved truth;
- never silently rewrite earlier layers.

If a later stage requires an earlier layer change:

- return to the owning stage;
- record the reason;
- invalidate dependent stages;
- regenerate affected layers only;
- rerun dependent validators.

---

## 4. Human approval gates

Explicit human approval REQUIRED for:

- adventure brief;
- Fixed Truth;
- culprit, motive, method, and major timeline;
- major NPC relationships and motivations;
- major conclusions and ending structure;
- any change to an already approved earlier layer;
- final Pre-Playtest package.

The generator MAY propose options but MUST NOT choose irreversible story changes without approval.

---

## 5. Model adapter

Provider-independent interface with backends:

- external/cloud HTTP adapter;
- local OpenAI-compatible endpoint;
- command-line local runner;
- deterministic mock backend (tests).

Core generation logic MUST NOT hardcode a specific vendor. Configuration covers model name, context size, temperature, max output, timeout, retries, and local vs remote mode.

---

## 6. Local-model constraints

Prompts and context packages MUST be suitable for a local 30–32B quantized model:

- small stage-specific prompts;
- relevant spec excerpts only;
- machine-readable JSON responses;
- resumable jobs;
- low-temperature deterministic mode;
- context budget reporting;
- graceful `BLOCKED` when context is too large.

---

## 7. Integrated validation

`python3 -m idne.validate_adventure <adventure_root>` runs all applicable validators from Milestones 1–10.

Overall PASS is forbidden when any mandatory validator is FAIL or BLOCKED. Tier B and Tier C requirements remain visible. Legacy adventures without canonical manifests report SKIP (not PASS).

---

## 8. Package format

Export unified `<adventure>.idne` ZIP packages for Simulator v2, Android import, local repair, and static-book export (consumers not implemented in Milestone 11).

---

## 9. CLI

```bash
python3 -m idne.generate <brief.json>
python3 -m idne.generate <brief.json> --resume
python3 -m idne.generate <brief.json> --stage world_truth
python3 -m idne.validate_adventure <adventure_root>
```

---

## 10. Scope limits (Milestone 11)

- No reference adventure generation.
- No Simulator v2, Android UI, inventory expansion, paid retries, false checks, or puzzle mechanics.
- Local 32B quality is not claimed proven without later testing.

**Schema:** `ADVENTURE_GENERATOR_V2_SCHEMA.md`  
**Workflow:** `ADVENTURE_GENERATOR_V2_WORKFLOW.md`  
**Reports:** `ADVENTURE_GENERATOR_V2_REPORT_FORMAT.md`
