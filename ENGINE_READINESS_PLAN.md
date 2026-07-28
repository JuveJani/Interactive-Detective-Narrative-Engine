---
title: Engine Readiness Gap Resolution Plan
version: 1.0
status: Draft
depends_on:
  - BOOK_COMPILER_SPEC.md
  - CONTENT_GENERATION_SPEC.md
  - adventures/The_Last_Witness/README.md
used_by:
  - adventures/The_Last_Witness/DO_NOT_READ/07_PROTOTYPE_BUILD_PLAN.md
last_review:
reviewer:
---

# Engine Readiness Gap Resolution Plan

## 0. Purpose

This document merges every blocker from:

- `BOOK_COMPILER_SPEC.md` § 10 (MS-01 through MS-16)
- `CONTENT_GENERATION_SPEC.md` § 12 (AR-01 through AR-15)

into one unified implementation roadmap. It identifies, classifies, prioritizes, and sequences the minimum remaining work required before the IDNE engine can support **deterministic AI generation of a complete playable gamebook**.

This plan does not redesign the engine, invent gameplay, or prescribe solutions. It defines what must be specified, where, and in what order.

### 0.1 Source mapping

| Unified ID | Merged from |
|---|---|
| ER-01 | MS-14, AR-01 |
| ER-02 | MS-04, AR-02 |
| ER-03 | MS-08, AR-04 |
| ER-04 | MS-09, AR-03 |
| ER-05 | MS-11, AR-06 |
| ER-06 | AR-07 |
| ER-07 | MS-16, AR-13 |
| ER-08 | AR-15 |
| ER-09 | MS-13, AR-12 |
| ER-10 | MS-10, AR-05 |
| ER-11 | MS-05, AR-09 |
| ER-12 | AR-08 |
| ER-13 | MS-15 |
| ER-14 | MS-07, AR-10 |
| ER-15 | MS-06, AR-11 |
| ER-16 | MS-01, MS-02, MS-03 |
| ER-17 | MS-12 |
| ER-18 | AR-14 |

MS-01, MS-02, and MS-03 describe distinct compiled artifacts but share one root cause: the Alpha 0.3 narrative layer has not been authored. They are merged into ER-16.

---

## 1. Unified blocker list

| ID | Title | Merged sources |
|---|---|---|
| **ER-01** | Per-node `Outgoing` completeness on eleven `INTERMEDIATE` nodes | MS-14, AR-01 |
| **ER-02** | Check (`CHK_*`) record definitions | MS-04, AR-02 |
| **ER-03** | Scene mode (`Joint` / `Split` / `Solo`) per playable node | MS-08, AR-04 |
| **ER-04** | Split-branch terminator per split branch | MS-09, AR-03 |
| **ER-05** | Synchronization window maximum durations and leftover-time rule | MS-11, AR-06 |
| **ER-06** | Multi-outcome variant enumeration for conditional clue grants | AR-07 |
| **ER-07** | Correct `END_*` identifier status metadata | MS-16, AR-13 |
| **ER-08** | Wrong-accusation accusation menu wiring at `EVT_440` | AR-15 |
| **ER-09** | Participation audit field population | MS-13, AR-12 |
| **ER-10** | Solo play mode graph and artifact rules | MS-10, AR-05 |
| **ER-11** | Public condition tag and public name instance registry | MS-05, AR-09 |
| **ER-12** | Formal narrative record (`NAR_*`) schema | AR-08 |
| **ER-13** | Formal Public Static Node (compiler output) schema | MS-15 |
| **ER-14** | Two-player delivery model declaration | MS-07, AR-10 |
| **ER-15** | Record sheet and time tracker layouts | MS-06, AR-11 |
| **ER-16** | Alpha 0.3 Narrative Record Package (scenes, choice labels, clue cards) | MS-01, MS-02, MS-03 |
| **ER-17** | Wrong-accusation rebuttal player passages | MS-12 |
| **ER-18** | `DEFINITION_ONLY` clue grant completeness audit | AR-14 |

**Total:** 18 unified blockers (28 source items → 18 after deduplication).

---

## 2. Classification

### ER-01 — Per-node `Outgoing` completeness

| Field | Value |
|---|---|
| **Affected files** | `adventures/The_Last_Witness/DO_NOT_READ/LOGIC/10_INVESTIGATION_NODE_GRAPH.md` |
| **Engine layer** | Structural graph contract (`engine/03` § 3.18) |
| **Authoring layer** | Blocks `NAR_CHOICE_*` and complete `NAR_EVT_*` for eleven nodes |
| **Compiler layer** | Blocks Stage 1 ingestion and Stage 2 reachability |
| **Gameplay impact** | Undefined forward routes from `EVT_115`, `EVT_123`, `EVT_150`, `EVT_212`, `EVT_223`, `EVT_232`, `EVT_243`, `EVT_300`, `EVT_314`, `EVT_331`, `EVT_440` |
| **Implementation impact** | Graph integrity assertion in `10` § 16 is false; V3 strict per-node check fails |

### ER-02 — Check (`CHK_*`) record definitions

| Field | Value |
|---|---|
| **Affected files** | `LOGIC/10_INVESTIGATION_NODE_GRAPH.md` (failure transformations); new `CHK_*` declarations (location TBD per `00_ENTITY_KEY_TABLE.md`); `templates/EVENT_TEMPLATE.md` (reference) |
| **Engine layer** | D20 resolution expectation (`engine/01` § 1.2) |
| **Authoring layer** | Blocks `NAR_CHK_*` and failure variants of `NAR_EVT_*` |
| **Compiler layer** | Blocks Stage 3–4 variant expansion for check-gated branches |
| **Gameplay impact** | Referenced checks (e.g. perception on `EVT_115`) have no skill, DC, pass/fail route, or player instruction |
| **Implementation impact** | No `CHK_*` namespace populated; fair-play failure paths undefined |

### ER-03 — Scene mode per playable node

| Field | Value |
|---|---|
| **Affected files** | `LOGIC/10_INVESTIGATION_NODE_GRAPH.md` |
| **Engine layer** | `engine/05` § 3 scene mode requirement |
| **Authoring layer** | `scene_mode` metadata cannot be logic-authoritative; derivation is temporary |
| **Compiler layer** | Stage 6 multiplayer partition and communication callouts |
| **Gameplay impact** | Joint vs split vs solo eligibility undefined at logic level |
| **Implementation impact** | Booklet routing and knowledge isolation rules cannot be validated against logic |

### ER-04 — Split-branch terminator per split branch

| Field | Value |
|---|---|
| **Affected files** | `LOGIC/10_INVESTIGATION_NODE_GRAPH.md`; `LOGIC/13_SPLIT_AND_REGROUP_FLOW.md` |
| **Engine layer** | `engine/05` § 5 anti-drift terminators |
| **Authoring layer** | `split_terminator` metadata incomplete beyond regroup defaults |
| **Compiler layer** | Stage 6 split flow validation; deferred V8-related checks |
| **Gameplay impact** | Split branches lack declared end condition (`REJOIN`, `REMOTE_CONTACT`, etc.) |
| **Implementation impact** | Temporal drift prevention cannot be validated |

### ER-05 — Synchronization window durations and leftover-time rule

| Field | Value |
|---|---|
| **Affected files** | `LOGIC/04_TIME_COST_MATRIX.md` § 3; `LOGIC/13_SPLIT_AND_REGROUP_FLOW.md`; possibly `engine/05` § 4 alignment note |
| **Engine layer** | `engine/05` § 4 synchronization windows |
| **Authoring layer** | Split-scene timing instructions cannot state window limits |
| **Compiler layer** | Stage 2 V8 (deferred); Stage 6 timing instructions |
| **Gameplay impact** | Maximum split-window duration undeclared; leftover-time handling conflicts between adventure and engine docs |
| **Implementation impact** | V8 cannot pass; prose cannot cite authoritative window caps |

### ER-06 — Multi-outcome variant enumeration

| Field | Value |
|---|---|
| **Affected files** | `LOGIC/10_INVESTIGATION_NODE_GRAPH.md` (e.g. `EVT_113` careful/rushed; "two of" clue grants) |
| **Engine layer** | Variant materiality (`engine/04` § 5) |
| **Authoring layer** | `NAR_EVT_*` variant keys undefined |
| **Compiler layer** | Stage 4 variant expansion |
| **Gameplay impact** | Which clues appear in which outcome branch is unspecified |
| **Implementation impact** | Generator or compiler must choose clue subsets — a gameplay decision |

### ER-07 — Correct `END_*` identifier status

| Field | Value |
|---|---|
| **Affected files** | `LOGIC/14_ENDING_TRIGGER_MATRIX.md` § 9 |
| **Engine layer** | Identifier status convention (`00_ENTITY_KEY_TABLE.md`) |
| **Authoring layer** | `NAR_END_*` family binding validation |
| **Compiler layer** | Stage 2 V2 identifier status |
| **Gameplay impact** | None directly — metadata only |
| **Implementation impact** | Seven `END_*` families listed `DEFINITION_ONLY` while terminal nodes reference them as active |

### ER-08 — Wrong-accusation accusation menu wiring

| Field | Value |
|---|---|
| **Affected files** | `LOGIC/10_INVESTIGATION_NODE_GRAPH.md` (`EVT_440`); `LOGIC/14_ENDING_TRIGGER_MATRIX.md` § 7; `LOGIC/07_EVIDENCE_VALIDATION.md` § 3 |
| **Engine layer** | Terminal routing (`EVT_907`) |
| **Authoring layer** | `NAR_CHOICE_*` at `EVT_440`; `NAR_END_*` rebuttal variant selection |
| **Compiler layer** | Stage 6 terminal `EVT_907` dispatch |
| **Gameplay impact** | Accusation targets not wired to rebuttal categories in logic |
| **Implementation impact** | Depends on ER-01 for `EVT_440` edges; rebuttal category selection undefined at logic layer |

### ER-09 — Participation audit population

| Field | Value |
|---|---|
| **Affected files** | `LOGIC/08_TWO_PLAYER_CORE_RULES.md` § 9; `LOGIC/13_SPLIT_AND_REGROUP_FLOW.md` |
| **Engine layer** | Two-player equality (`engine/02` § 2.13) |
| **Authoring layer** | Pre-generation parity gate |
| **Compiler layer** | Stage 2 pre-compilation gate |
| **Gameplay impact** | Cannot verify equal meaningful participation before compile/generate |
| **Implementation impact** | Audit table empty; `08` § 9 requirement unmet |

### ER-10 — Solo play mode graph

| Field | Value |
|---|---|
| **Affected files** | `LOGIC/10_INVESTIGATION_NODE_GRAPH.md`; `LOGIC/13_SPLIT_AND_REGROUP_FLOW.md`; `adventures/The_Last_Witness/README.md`; `engine/06_PROTOTYPE_SCOPE_AND_VALIDATION.md` § 1 |
| **Engine layer** | One-player mode requirement |
| **Authoring layer** | Solo narrative package rules; `EVT_908` exclusion |
| **Compiler layer** | Stage 2 reachability per mode; `play_modes` in output package |
| **Gameplay impact** | Solo routes, eligibility, and artifact set undefined |
| **Implementation impact** | `PROTOTYPE_BRIEF.md` lists solo play; logic is two-player-native |

### ER-11 — Public condition tag instance registry

| Field | Value |
|---|---|
| **Affected files** | New adventure-level registry (planned `PLAYER/` or `LOGIC/`); references `LOGIC/01_WORLD_STATE_VARIABLES.md`, `LOGIC/12_CLUE_DEPENDENCY_GRAPH.md`, `engine/04` § 4 |
| **Engine layer** | Public condition tag format |
| **Authoring layer** | `NAR_PUBLIC_*` records |
| **Compiler layer** | Stage 4–6 condition-gated choices |
| **Gameplay impact** | Players cannot check gated choices from record sheet without mappings |
| **Implementation impact** | Internal conditions (`T_MINA >= +1`, etc.) have no player-facing names |

### ER-12 — Formal narrative record schema

| Field | Value |
|---|---|
| **Affected files** | `data_dictionary/` (new schema files); `CONTENT_GENERATION_SPEC.md` § 11 (reference only) |
| **Engine layer** | Pipeline layering (`engine/03` § 3.12) |
| **Authoring layer** | V-N1 machine validation |
| **Compiler layer** | Stage 3 input contract |
| **Gameplay impact** | None directly |
| **Implementation impact** | `NAR_*` field names normative in spec only; not executable |

### ER-13 — Formal Public Static Node schema

| Field | Value |
|---|---|
| **Affected files** | `data_dictionary/` (new schema files); `BOOK_COMPILER_SPEC.md` § 9.1 (reference only) |
| **Engine layer** | Compiler–formatter handoff (`engine/03` § 3.7–3.8) |
| **Authoring layer** | None |
| **Compiler layer** | Stage 6–7 output validation |
| **Gameplay impact** | None directly |
| **Implementation impact** | Compiler output shape documented in prose only |

### ER-14 — Two-player delivery model declaration

| Field | Value |
|---|---|
| **Affected files** | `adventures/The_Last_Witness/README.md` or `PLAYER/` config; `engine/03` § 3.15 |
| **Engine layer** | Delivery models A / B / C |
| **Authoring layer** | Booklet partitioning of `NAR_EVT_*` records |
| **Compiler layer** | Stage 6–7 artifact packaging |
| **Gameplay impact** | None on logic; affects physical artifact shape |
| **Implementation impact** | Cannot emit one book vs two booklets vs shared+companion |

### ER-15 — Record sheet and time tracker layouts

| Field | Value |
|---|---|
| **Affected files** | `adventures/The_Last_Witness/PLAYER/` (new printable templates) |
| **Engine layer** | `engine/04` § 7 prototype constraint |
| **Authoring layer** | `record_sheet_line` and `visible_update_instructions` field targets |
| **Compiler layer** | Stage 6 visible state update emission |
| **Gameplay impact** | Players lack defined fields for clock, clues, shared state |
| **Implementation impact** | Alpha 0.4 package incomplete |

### ER-16 — Alpha 0.3 Narrative Record Package

| Field | Value |
|---|---|
| **Affected files** | `adventures/The_Last_Witness/PLAYER/narrative/` (or equivalent Alpha 0.3 layer) |
| **Engine layer** | Authoring vs compilation separation (`engine/02` § 2.14) |
| **Authoring layer** | `NAR_EVT_*`, `NAR_CHOICE_*`, `NAR_CLUE_*`, `NAR_DEDUCTION_*`, `NAR_END_*` (except ER-17 subset) |
| **Compiler layer** | Stage 3 narrative binding — **primary compiler input gap** |
| **Gameplay impact** | No player-readable content exists |
| **Implementation impact** | Alpha 0.3 not started per `README.md` |

### ER-17 — Wrong-accusation rebuttal player passages

| Field | Value |
|---|---|
| **Affected files** | Narrative layer (`NAR_END_*` variants for `EVT_907`); sources `06_ENDING_FRAMEWORK.md` END-07, `14` § 7, `07` § 3 |
| **Engine layer** | Fair-play failure explanation |
| **Authoring layer** | Per-category rebuttal prose |
| **Compiler layer** | Stage 6 terminal `EVT_907` |
| **Gameplay impact** | Wrong accusation ending lacks player-readable explanation |
| **Implementation impact** | Categories exist; passages do not. Depends on ER-08 for variant selection keys |

### ER-18 — `DEFINITION_ONLY` clue grant completeness

| Field | Value |
|---|---|
| **Affected files** | `LOGIC/12_CLUE_DEPENDENCY_GRAPH.md`; `LOGIC/07_EVIDENCE_VALIDATION.md` § 6 soft-lock audit |
| **Engine layer** | Clue register completeness |
| **Authoring layer** | No `NAR_CLUE_*` for 23 identifiers (correct skip) |
| **Compiler layer** | None unless mandatory conclusions lack alternate routes |
| **Gameplay impact** | Potential soft-lock if required conclusions need `DEFINITION_ONLY` clues with no alternate path |
| **Implementation impact** | Monitoring item; not a generation halt per `CONTENT_GENERATION_SPEC.md` |

---

## 3. Root cause

| ID | Underlying missing specification (not symptom) |
|---|---|
| **ER-01** | Authoritative directed edge list from each of eleven `INTERMEDIATE` nodes to specific target `EVT_*` identifiers |
| **ER-02** | Declared `CHK_*` records binding skill, DC, pass outcome, fail outcome, and fallback route for every check referenced in logic |
| **ER-03** | Explicit `scene_mode` field value on every playable `EVT_*` node |
| **ER-04** | Explicit `split_terminator` value on every split-branch exit in logic |
| **ER-05** | Per synchronization window: start condition, maximum duration, and single authoritative leftover-time resolution rule |
| **ER-06** | Named variant keys enumerating every distinct player-facing outcome for multi-result nodes (which clues, which costs, which failure states) |
| **ER-07** | Accurate `ACTIVE` / `DEFINITION_ONLY` status for all eight `END_*` families consistent with terminal node references |
| **ER-08** | Complete accusation-target → rebuttal-category mapping and `Outgoing` edges at `EVT_440` |
| **ER-09** | Populated per-block metrics: decisions per player, unique clues per player, challenge counts, waiting time, final-act responsibility |
| **ER-10** | Solo-mode reachability graph, player-merge rules, excluded nodes (`EVT_908`), and solo artifact set declaration |
| **ER-11** | Instance table mapping each internal condition expression and `CLUE_*` / `ITEM_*` to a player-facing public name and condition tag |
| **ER-12** | Machine-readable JSON/YAML schema for `NAR_*` narrative record types in `data_dictionary/` |
| **ER-13** | Machine-readable schema for Public Static Node Package in `data_dictionary/` |
| **ER-14** | Declared selection of delivery Model A, B, or C for The Last Witness |
| **ER-15** | Field-level layout for one shared record sheet, one private knowledge sheet per player, and time tracker |
| **ER-16** | Authored narrative records: scene prose, choice labels, and clue card text for all compilable nodes and `ACTIVE` clues |
| **ER-17** | Authored player-readable rebuttal passage per `14` § 7 rebuttal category |
| **ER-18** | Verified proof that no mandatory conclusion depends solely on `DEFINITION_ONLY` clues without alternate routes in `07` § 6 |

---

## 4. Dependency graph

```text
                    ER-07 (END_* status)
                           │
ER-01 (Outgoing) ─────────┼──────────────────────────────┐
         │                 │                              │
         ├──────────────── ER-08 (accusation wiring)        │
         │                        │                       │
         │                        └──────────┐            │
         │                                   ▼            │
ER-06 (variant keys) ──────────────► ER-16 (narrative) ◄──┤
         ▲                                   ▲            │
         │                                   │            │
ER-02 (CHK_*) ─────────────────────────────┤            │
         │                                   │            │
ER-03 (scene mode) ──────────────────────────┤            │
         │                                   │            │
ER-04 (split terminators) ─────────────────┤            │
         │                                   │            │
ER-05 (sync windows) ──────────────────────┤            │
         │                                   │            │
ER-11 (public names) ──────────────────────┘            │
         │                                                │
ER-08 ──────────────────────────────► ER-17 (rebuttals)  │
                                                          │
ER-12 (NAR schema) ───► ER-16 (validates package)         │
                                                          │
ER-16 ──────────────────────────────► ER-13 (compiler    │
         │                              output schema    │
         │                              validation)       │
         ▼                                                │
ER-14 (delivery model) ◄── ER-16 complete                 │
         │                                                │
         ▼                                                │
ER-15 (record sheets) ◄── ER-11 + ER-16                   │
                                                          │
ER-09 (participation audit) ──► ER-16 (pre-gen gate)     │
                                                          │
ER-10 (solo mode) ──────────────► ER-16 (solo variants)  │
                                                          │
ER-18 (DEFINITION_ONLY audit) ──► independent monitor    │
```

### Dependency summary

| Blocker | Depends on |
|---|---|
| ER-01 | — |
| ER-02 | — |
| ER-03 | — |
| ER-04 | ER-03 (split scenes must be identified first) |
| ER-05 | ER-03, ER-04 |
| ER-06 | — |
| ER-07 | — |
| ER-08 | ER-01 |
| ER-09 | — (should complete before ER-16 gate) |
| ER-10 | — |
| ER-11 | — |
| ER-12 | — (enables validation; not content prerequisite) |
| ER-13 | ER-12 (narrative schema should precede compiler output schema) |
| ER-14 | ER-16 |
| ER-15 | ER-11, ER-16 |
| ER-16 | ER-01, ER-02, ER-06, ER-03, ER-04, ER-05, ER-11; ER-09 gate |
| ER-17 | ER-08, ER-16 (framework) |
| ER-18 | — |

### Recommended implementation order

```text
ER-07
  ↓
ER-01 → ER-06 → ER-02
  ↓
ER-03 → ER-04 → ER-05
  ↓
ER-08 → ER-09 → ER-10
  ↓
ER-11 → ER-12 → ER-13
  ↓
ER-16 → ER-17
  ↓
ER-14 → ER-15
  ↓
ER-18 (parallel monitor throughout)
```

---

## 5. Priority

| ID | Priority | Rationale |
|---|---|---|
| **ER-01** | **Critical** | Compiler and author cannot resolve edges; graph structurally incomplete |
| **ER-02** | **Critical** | Check-gated failure paths undefined; variant expansion blocked |
| **ER-06** | **Critical** | Clue subset selection is a gameplay decision without variant keys |
| **ER-07** | **Critical** | Identifier validation contradicts terminal references |
| **ER-16** | **Critical** | No narrative input exists; compilation cannot bind Stage 3 |
| **ER-03** | **High** | Engine-mandated field missing on all nodes |
| **ER-04** | **High** | Engine-mandated split terminator missing |
| **ER-05** | **High** | Window caps and leftover-time rule unresolved |
| **ER-08** | **High** | Final-act accusation routing incomplete |
| **ER-11** | **High** | Condition-gated choices cannot compile |
| **ER-17** | **High** | Terminal ending `EVT_907` lacks bindable prose |
| **ER-09** | **Medium** | Pre-compile gate; does not block partial authoring |
| **ER-10** | **Medium** | Two-player path is primary prototype; solo required by engine but deferrable for two-player-only release |
| **ER-12** | **Medium** | Tooling validation; manual authoring possible without schema |
| **ER-13** | **Medium** | Tooling validation; compiler implementable from prose spec |
| **ER-14** | **Medium** | Blocks final packaging only |
| **ER-15** | **Medium** | Blocks playable package; not narrative binding |
| **ER-18** | **Low** | Monitoring; generation correctly skips `DEFINITION_ONLY` clues |

---

## 6. Resolution strategy

For each blocker: files to modify, expected new sections, expected validation changes. **No content is written here.**

### ER-01

| Item | Description |
|---|---|
| **Files to modify** | `LOGIC/10_INVESTIGATION_NODE_GRAPH.md` |
| **New sections** | Per-node `**Outgoing**` block under each of the eleven nodes; optional § 16 assertion update confirming 40/40 `INTERMEDIATE` nodes |
| **Validation changes** | V3 strict per-node `Outgoing` pass; reachability re-run for affected subgraph |

### ER-02

| Item | Description |
|---|---|
| **Files to modify** | `LOGIC/00_ENTITY_KEY_TABLE.md` (prefix row if needed); new check register document or § in `10`; nodes with failure transformations |
| **New sections** | `CHK_*` register: skill, DC, pass/fail effects, fallback `EVT_*`; cross-reference from each node's **Failure transformation** |
| **Validation changes** | New V-CHK gate: every failure transformation referencing a check resolves to a `CHK_*` record |

### ER-03

| Item | Description |
|---|---|
| **Files to modify** | `LOGIC/10_INVESTIGATION_NODE_GRAPH.md` § 1 conventions; every node |
| **New sections** | `**Scene mode**:` field (`Joint` / `Split` / `Solo`) in graph conventions and on all 48 playable nodes |
| **Validation changes** | New V-SM gate: every `EVT_*` declares exactly one scene mode |

### ER-04

| Item | Description |
|---|---|
| **Files to modify** | `LOGIC/10_INVESTIGATION_NODE_GRAPH.md`; `LOGIC/13_SPLIT_AND_REGROUP_FLOW.md` |
| **New sections** | `**Split terminator**:` on every `Split` / applicable `Solo` node |
| **Validation changes** | New V-ST gate: every split branch declares a terminator from closed set |

### ER-05

| Item | Description |
|---|---|
| **Files to modify** | `LOGIC/04_TIME_COST_MATRIX.md`; `LOGIC/13_SPLIT_AND_REGROUP_FLOW.md` |
| **New sections** | Per-window maximum duration table; single leftover-time resolution rule reconciling `04` § 3 with `engine/05` § 4 |
| **Validation changes** | V8 promoted from deferred to active |

### ER-06

| Item | Description |
|---|---|
| **Files to modify** | `LOGIC/10_INVESTIGATION_NODE_GRAPH.md` (affected nodes) |
| **New sections** | Named **Variants** block per multi-outcome node listing variant key, conditions, clue grants, and costs |
| **Validation changes** | Variant enumeration completeness check against `GRANT_CLUE` statements |

### ER-07

| Item | Description |
|---|---|
| **Files to modify** | `LOGIC/14_ENDING_TRIGGER_MATRIX.md` § 9 |
| **New sections** | Corrected status table: eight `END_*` families `ACTIVE` where terminal nodes exist |
| **Validation changes** | V2 pass without override rules |

### ER-08

| Item | Description |
|---|---|
| **Files to modify** | `LOGIC/10_INVESTIGATION_NODE_GRAPH.md` (`EVT_440`); `LOGIC/14_ENDING_TRIGGER_MATRIX.md` § 7 |
| **New sections** | Accusation target list with `Outgoing` per target; target → rebuttal category mapping table |
| **Validation changes** | Every `EVT_440` outgoing target maps to one `14` § 7 category |

### ER-09

| Item | Description |
|---|---|
| **Files to modify** | `LOGIC/08_TWO_PLAYER_CORE_RULES.md` § 9; `LOGIC/13_SPLIT_AND_REGROUP_FLOW.md` |
| **New sections** | Populated audit table per major block (opening, split one, regroup one, midgame, final act) |
| **Validation changes** | Pre-compile participation parity gate |

### ER-10

| Item | Description |
|---|---|
| **Files to modify** | `LOGIC/10_INVESTIGATION_NODE_GRAPH.md`; `LOGIC/13_SPLIT_AND_REGROUP_FLOW.md`; `adventures/The_Last_Witness/README.md` |
| **New sections** | Solo eligibility rules; merged-player routing; `EVT_908` exclusion; solo `play_modes` declaration |
| **Validation changes** | Reachability pass for solo mode; solo artifact set declared |

### ER-11

| Item | Description |
|---|---|
| **Files to modify** | New `LOGIC/17_PUBLIC_CONDITION_REGISTRY.md` or `PLAYER/public_names.yaml` |
| **New sections** | Instance table: internal ref → `public_name` → condition tag template |
| **Validation changes** | Every entry condition in `10` has a public mapping or is marked compiler-internal |

### ER-12

| Item | Description |
|---|---|
| **Files to modify** | `data_dictionary/` (new files); `data_dictionary/README.md` |
| **New sections** | Schemas for `NAR_EVT`, `NAR_CHOICE`, `NAR_CLUE`, `NAR_DEDUCTION`, `NAR_END`, `NAR_PUBLIC`, `NAR_CHK` |
| **Validation changes** | V-N1 machine schema validation |

### ER-13

| Item | Description |
|---|---|
| **Files to modify** | `data_dictionary/` (new files); `data_dictionary/README.md` |
| **New sections** | Public Static Node Package schema per `BOOK_COMPILER_SPEC.md` § 9.1 |
| **Validation changes** | Compiler output schema validation |

### ER-14

| Item | Description |
|---|---|
| **Files to modify** | `adventures/The_Last_Witness/README.md` or `PLAYER/delivery_config.yaml` |
| **New sections** | Declared model: `A`, `B`, or `C` with booklet assignment rules |
| **Validation changes** | Formatter packaging rule selected |

### ER-15

| Item | Description |
|---|---|
| **Files to modify** | `PLAYER/02_SHARED_CASE_FILE.md` (new); `PLAYER/printable/` sheets |
| **New sections** | Shared sheet fields; private knowledge sheet fields; time tracker; field name glossary |
| **Validation changes** | Every `record_sheet_line` in narrative package resolves to a sheet field |

### ER-16

| Item | Description |
|---|---|
| **Files to modify** | `PLAYER/narrative/` (new directory and records) |
| **New sections** | Complete Narrative Record Package per `CONTENT_GENERATION_SPEC.md` § 11 |
| **Validation changes** | V-N1 through V-N5 pass; `BOOK_COMPILER_SPEC.md` Stage 3 dry-run bindable |

### ER-17

| Item | Description |
|---|---|
| **Files to modify** | `PLAYER/narrative/endings/` or `NAR_END_*` variants for `EVT_907` |
| **New sections** | One rebuttal passage per `14` § 7 category |
| **Validation changes** | Compiler selects rebuttal variant without invention |

### ER-18

| Item | Description |
|---|---|
| **Files to modify** | `LOGIC/12_CLUE_DEPENDENCY_GRAPH.md`; `LOGIC/07_EVIDENCE_VALIDATION.md` § 6 |
| **New sections** | Soft-lock audit row per `DEFINITION_ONLY` clue: alternate route reference or intentional deferral |
| **Validation changes** | Soft-lock audit gate; no mandatory conclusion sole-dependent on `DEFINITION_ONLY` clue |

---

## 7. Milestones

Each milestone leaves the repository in a **valid state**: no contradictions introduced, validation gates pass for scope completed.

### Milestone A — Logic graph integrity

**Blockers:** ER-07, ER-01, ER-06

**Deliverable state:** All `INTERMEDIATE` nodes have authoritative `Outgoing`; multi-outcome nodes have variant keys; `END_*` status accurate.

**Validation:** V2 pass; V3 strict per-node pass; variant enumeration check.

**Repository validity:** Logic layer internally consistent; no narrative required yet.

---

### Milestone B — Engine-required logic fields

**Blockers:** ER-02, ER-03, ER-04, ER-05, ER-08, ER-09, ER-10

**Deliverable state:** Checks, scene modes, split terminators, sync windows, accusation wiring, participation audit, and solo rules declared in logic.

**Validation:** V-CHK, V-SM, V-ST, V8, participation gate, solo reachability.

**Repository validity:** Adventure logic satisfies engine § 3 and § 5 requirements for The Last Witness.

---

### Milestone C — Schema and public naming infrastructure

**Blockers:** ER-11, ER-12, ER-13

**Deliverable state:** Public condition registry authored; machine schemas for narrative input and compiler output.

**Validation:** V-N1 schema validation enabled; public mapping completeness.

**Repository validity:** Pipeline contracts machine-verifiable; still no player prose required.

---

### Milestone D — Alpha 0.3 narrative layer

**Blockers:** ER-16, ER-17

**Deliverable state:** Complete Narrative Record Package including wrong-accusation rebuttals.

**Validation:** V-N1 through V-N5; `BOOK_COMPILER_SPEC.md` Stage 3 bindable for all 48 nodes.

**Repository validity:** **AUTHORING READY** (see § 8).

---

### Milestone E — Alpha 0.4 playable package

**Blockers:** ER-14, ER-15

**Deliverable state:** Delivery model declared; record sheets match narrative record sheet lines.

**Validation:** Sheet field resolution; formatter packaging rule applied.

**Repository validity:** **COMPILER READY** for packaging handoff (see § 8).

---

### Milestone F — Ongoing quality monitor

**Blockers:** ER-18

**Deliverable state:** `DEFINITION_ONLY` clue audit documented with alternate-route proof.

**Validation:** Soft-lock audit gate.

**Repository validity:** **GAMEBOOK READY** confidence increased; not a hard gate for Milestone D or E.

---

## 8. Completion criteria

### AUTHORING READY

All must be true:

| # | Criterion | Measurement |
|---|---|---|
| A1 | ER-01 through ER-11 resolved | Zero open Critical/High logic and infrastructure blockers |
| A2 | ER-12 narrative schema published | `data_dictionary/` contains valid `NAR_*` schemas |
| A3 | Every `EVT_*` with complete logic fields has generatable structure | 48 nodes have `Outgoing`, `scene_mode`, and variant keys where applicable |
| A4 | Every `ACTIVE` `CLUE_*` has a defined grant path | 43 clues with granting nodes in `12` |
| A5 | Public name registry covers all condition-gated choices | 100% of gated entry conditions in `10` have `NAR_PUBLIC_*` mapping |
| A6 | Participation audit populated | `08` § 9 table complete for all major blocks |
| A7 | `CONTENT_GENERATION_SPEC.md` V-N1–V-N5 can run without logic halts | `incomplete_nodes` list empty |

**Does not require:** ER-16 content, ER-14, ER-15, ER-17, ER-18.

---

### COMPILER READY

All AUTHORING READY criteria, plus:

| # | Criterion | Measurement |
|---|---|---|
| C1 | ER-16 resolved | Narrative Record Package exists for all 48 playable `EVT_*` and required variants |
| C2 | ER-17 resolved | Six rebuttal passages (per `14` § 7 categories) bound to `EVT_907` variants |
| C3 | ER-13 resolved | Public Static Node schema validates compiler output |
| C4 | `BOOK_COMPILER_SPEC.md` Stage 3 binds 100% of nodes | `halted_nodes` empty in compiler dry-run |
| C5 | `BOOK_COMPILER_SPEC.md` Stages 1–2 pass | V1–V7, V9–V11 pass (V8 per ER-05) |
| C6 | ER-10 resolved or explicitly scoped out | Solo mode graph declared **or** `play_modes: [two_player]` declared with engine exception documented |

**Does not require:** ER-14, ER-15 (packaging), ER-18.

---

### GAMEBOOK READY

All COMPILER READY criteria, plus:

| # | Criterion | Measurement |
|---|---|---|
| G1 | ER-14 resolved | Delivery model A/B/C declared and applied |
| G2 | ER-15 resolved | Shared + private sheets + time tracker exist in `PLAYER/` |
| G3 | Compiler produces complete Public Static Node Package | Zero `halted_nodes`; all `ACTIVE` clues emitted |
| G4 | Formatter produces all planned artifacts | `PLAYER_1_BOOK.md`, `PLAYER_2_BOOK.md`, `02_SHARED_CASE_FILE.md`, sheets per `07_PROTOTYPE_BUILD_PLAN.md` Alpha 0.4 |
| G5 | ER-18 resolved or signed off | Soft-lock audit documents alternate route for every `DEFINITION_ONLY` clue used in mandatory paths |
| G6 | End-to-end playtest questionnaire completed | `07_PROTOTYPE_BUILD_PLAN.md` § First internal review questions answered |

---

## 9. Final assessment

### Current readiness

| Layer | Score | Justification |
|---|---:|---|
| **Engine** | **88%** | Engine specification (`engine/00`–`06`) is complete for defining compiler and authoring behaviour. Deduction: engine rules exist; adventure-level fields mandated by `engine/05` are not yet populated in logic (−8%); data dictionary schemas deferred (−4%). |
| **Authoring** | **22%** | World Bible, character DB, location DB, and logic bullets provide rich constraints (+22%). No narrative records exist (ER-16); eleven nodes lack `Outgoing` (ER-01); checks, scene modes, terminators, variant keys, and public registry missing (−78% of authoring pipeline). Partial scene drafting possible for ~37 nodes with complete edges only. |
| **Compiler** | **35%** | Logic graph mostly traversable (+25%); validation gates V1, V2 (with metadata defect), V4, V6, V7, V9–V11 pass (+10%). No Stage 3 narrative binding (−50%); packaging schemas and sheets absent (−15%). Matches `BOOK_COMPILER_SPEC.md` NOT READY. |

**Overall deterministic gamebook pipeline today: ~32%** (weighted: authoring input 40%, logic 30%, compiler tooling 30%).

---

### After completing all ER blockers

| Layer | Score | Justification |
|---|---:|---|
| **Engine** | **98%** | All engine-mandated adventure fields populated; schemas registered; V8 active. Remaining 2%: engine spec itself may need revision only if playtesting reveals spec-level defects — out of scope for this plan. |
| **Authoring** | **95%** | Full Narrative Record Package generatable and validatable. Remaining 5%: creative QA (tone, pacing, fair-play feel) requires human playtest — not machine-verifiable. |
| **Compiler** | **92%** | Full bind and emit for two-player mode; formatter produces artifacts. Remaining 8%: typography, page numbering, print layout quality — formatter responsibility; optional solo if ER-10 scoped out reduces to 88%. |

**Overall deterministic gamebook pipeline after ER-01–ER-18: ~95%** (two-player, delivery model declared, sheets present). Remaining gap is playtest quality assurance and print formatting polish, not specification completeness.

---

### Readiness state summary

| State | Current | After all ER blockers |
|---|---|---|
| AUTHORING READY | No | Yes (after Milestone C) |
| COMPILER READY | No | Yes (after Milestone D) |
| GAMEBOOK READY | No | Yes (after Milestone E + F) |

---

## Appendix A — Blocker quick reference

| ID | Priority | Milestone | MS | AR |
|---|---|---|---|---|
| ER-01 | Critical | A | MS-14 | AR-01 |
| ER-02 | Critical | B | MS-04 | AR-02 |
| ER-03 | High | B | MS-08 | AR-04 |
| ER-04 | High | B | MS-09 | AR-03 |
| ER-05 | High | B | MS-11 | AR-06 |
| ER-06 | Critical | A | — | AR-07 |
| ER-07 | Critical | A | MS-16 | AR-13 |
| ER-08 | High | B | — | AR-15 |
| ER-09 | Medium | B | MS-13 | AR-12 |
| ER-10 | Medium | B | MS-10 | AR-05 |
| ER-11 | High | C | MS-05 | AR-09 |
| ER-12 | Medium | C | — | AR-08 |
| ER-13 | Medium | C | MS-15 | — |
| ER-14 | Medium | E | MS-07 | AR-10 |
| ER-15 | Medium | E | MS-06 | AR-11 |
| ER-16 | Critical | D | MS-01–03 | — |
| ER-17 | High | D | MS-12 | — |
| ER-18 | Low | F | — | AR-14 |

---

## Appendix C — Milestone B design decisions (Alpha 0.2c)

Owner-approved design decisions MBD-01 through MBD-06 are implemented in adventure logic per `MILESTONE_B_IMPLEMENTATION_V2_REPORT.md`.

| ID | ER mapping | Resolution |
|---|---|---|
| MBD-01 | ER-02 | D20 check resolution; `CHK_115_PERCEPTION` DC 10 (Medium) |
| MBD-02 | ER-03 | Scene mode as narrative-role metadata; 48/48 nodes classified |
| MBD-03 | ER-04 | Split completion = wait until no legal actions; window-level sync mechanics |
| MBD-04 | ER-05 | Single shared world clock; no per-player timeline math |
| MBD-05 | ER-09 | Participation audit across all valid paths; developer-only |
| MBD-06 | ER-10 | `two_player` only; solo deferred with documented exception (C6) |

Milestone B validation gates V-CHK, V-SM, V-ST, V8, participation gate, and C6 are satisfied for declared `two_player` scope.

---

## Appendix B — Document revision

| Version | Change |
|---|---|
| 1.0 | Initial unified readiness plan merging MS-01–MS-16 and AR-01–AR-15 |
