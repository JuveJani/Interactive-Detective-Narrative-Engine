---
title: Book Compiler Specification
version: 1.0
status: Draft
depends_on:
  - engine/03_ARCHITECTURE.md
  - engine/04_EXECUTION_MODEL_AND_BOUNDARIES.md
  - engine/05_TWO_PLAYER_SYNCHRONIZATION.md
  - adventures/The_Last_Witness/README.md
used_by:
  - adventures/The_Last_Witness/PLAYER/
last_review:
reviewer:
---

# Book Compiler Specification

## 0. Purpose and scope

This document specifies how an automated system compiles an IDNE adventure from its existing repository sources into a **fully playable static gamebook**, without making gameplay decisions or inventing content.

### 0.1 What this document is

- The formal specification for the **Narrative Compiler** layer defined in `engine/03_ARCHITECTURE.md` § 3.6.
- The authoritative handoff contract to the **Book Formatter** layer defined in `engine/03_ARCHITECTURE.md` § 3.8.
- A deterministic rule set for a future AI or tool chain.

### 0.2 What this document is not

- A redesign of the IDNE engine.
- A narrative authoring guide. It does not author prose, choice labels, or check instructions that the repository does not already contain.
- An implementation of the compiler. No compiler executable exists in this repository.
- A substitute for adventure logic. If logic is missing, the compiler reports an engine or documentation defect; it does not infer gameplay.

### 0.3 Reference adventure

All examples and file paths refer to **The Last Witness** at `adventures/The_Last_Witness/`, the only adventure with compiler-ready logic in this repository (Prototype Alpha 0.2c per `adventures/The_Last_Witness/README.md`).

### 0.4 Engine completeness assumption

The IDNE **engine specification** is treated as implementation complete. This specification evaluates whether the **repository as a whole** — engine plus adventure sources — contains every input required for deterministic compilation.

---

## 1. Source documents

### 1.1 Authoritative pipeline

Compilation consumes sources only in this dependency order (`engine/04_EXECUTION_MODEL_AND_BOUNDARIES.md` § 2):

```text
Engine Specification
        ↓
Data Dictionary and Schemas
        ↓
World Bible
        ↓
Adventure Logic
        ↓
Narrative Compiler  ← this specification
        ↓
Book Formatter
        ↓
Player Output
```

A lower layer must not override objective facts owned by a higher layer.

### 1.2 Engine inputs (normative rules)

| Document | Role in compilation |
|---|---|
| `engine/00_ENGINE_SPECIFICATION_2.0.md` | Master index; compile-time vs play-time boundary |
| `engine/01_INTRODUCTION_AND_SCOPE.md` | Scope, fair-play, D20 expectation, two-player use case |
| `engine/02_DESIGN_PRINCIPLES.md` | Authoring vs compilation separation (§ 2.14) |
| `engine/03_ARCHITECTURE.md` | Layer responsibilities; Public Static Node definition (§ 3.7); terminal types (§ 3.18); two-player delivery models (§ 3.15); time architecture (§ 3.16) |
| `engine/04_EXECUTION_MODEL_AND_BOUNDARIES.md` | Compile-time tasks; variant merging (§ 5); public condition tags (§ 4); formatter boundary (§ 6); record-sheet constraint (§ 7) |
| `engine/05_TWO_PLAYER_SYNCHRONIZATION.md` | Shared world time; scene modes (§ 3); synchronization windows (§ 4); split terminators (§ 5); knowledge isolation (§ 6) |
| `engine/06_PROTOTYPE_SCOPE_AND_VALIDATION.md` | Prototype validation gates; defect classification |

**Precedence:** Where engine chapters conflict, `engine/03_ARCHITECTURE.md` governs layer boundaries. Where engine chapters conflict with adventure logic on **objective gameplay structure**, adventure logic governs for that adventure only. Engine rules govern **how** compilation works; adventure logic governs **what** is compiled.

**Excluded:** Root-level duplicates (`00_ENGINE_SPECIFICATION_2.0.md`, `README (n).md`, etc.). Use canonical paths under `engine/` only.

### 1.3 Data dictionary inputs

| Document | Role |
|---|---|
| `data_dictionary/SCHEMA_VERSIONING.md` | Required adventure-root version fields; compatibility rules |
| `data_dictionary/README.md` | Planned record types (Event, Decision, Check, Clue, etc.) — **declarative only; no executable schemas exist** |

Version fields are read from `adventures/The_Last_Witness/README.md` frontmatter:

```yaml
engine_spec_version: "2.0"
data_dictionary_version: "0.3"
adventure_schema_version: "1.0"
```

### 1.4 World and narrative foundation inputs

Located under `adventures/The_Last_Witness/DO_NOT_READ/`. These define **objective truth and reference material**. They do not define graph edges, triggers, or player choices.

| Document | Authority |
|---|---|
| `01_WORLD_BIBLE.md` | **Authoritative** for immutable objective facts, setting, corruption scheme, passphrase custody (§ 4), tone constraints |
| `00_CASE_OVERVIEW.md` | Non-authoritative summary; must not override World Bible or logic |
| `02_MASTER_TIMELINE.md` | Authoritative for fixed and conditional timeline events |
| `03_CHARACTER_DATABASE.md` | Authoritative for character identity, relationships, knowledge boundaries |
| `04_LOCATION_DATABASE.md` | Authoritative for location description, access, atmosphere |
| `05_CLUE_ARCHITECTURE.md` | **Non-authoritative** pointer; clue classes and counting owned by `LOGIC/07_EVIDENCE_VALIDATION.md` § 1 |
| `06_ENDING_FRAMEWORK.md` | **Authoritative for narrative outcome text only** (END-01–END-08); triggers owned by `LOGIC/14_ENDING_TRIGGER_MATRIX.md` |
| `07_PROTOTYPE_BUILD_PLAN.md` | Production sequencing; defines Alpha 0.3 narrative-compiler pass scope |

### 1.5 Adventure logic inputs (primary compilation input)

Located under `adventures/The_Last_Witness/DO_NOT_READ/LOGIC/`. This layer is **authoritative for all playable structure**.

| Document | Owns |
|---|---|
| `00_ENTITY_KEY_TABLE.md` | Prefix registry; NPC, LOC, ITEM, CON identifiers; ownership rules |
| `01_WORLD_STATE_VARIABLES.md` | All variables; `CLK_*` triggers; derived progress totals; knowledge sets |
| `02_ITEM_STATE_MATRIX.md` | Item movement and state |
| `03_NPC_KNOWLEDGE_AND_DISCLOSURE.md` | `FACT_*` identifiers; NPC disclosure stages |
| `04_TIME_COST_MATRIX.md` | Travel and action durations; parallel-action rules |
| `05_CORE_EVENT_GRAPH.md` | `ARC_*` backbone arcs |
| `06_NPC_SCHEDULE_AND_PRIORITY.md` | Off-screen schedules; `EVT_801`–`EVT_804` |
| `07_EVIDENCE_VALIDATION.md` | Clue-class vocabulary (§ 1); conclusion thresholds (§ 2); `EVAL_*` evaluators (§ 7) |
| `08_TWO_PLAYER_CORE_RULES.md` | Split safety, communication modes, regroup gates, participation audit requirements |
| `09_PRE_LOGIC_AUDIT_RESOLUTION.md` | Resolved audit categories |
| `10_INVESTIGATION_NODE_GRAPH.md` | **`EVT_*` node identity, fields, `Outgoing` edges, terminal nodes** |
| `11_LOCATION_STATE_MACHINE.md` | Location state variables; `TR_*` transitions |
| `12_CLUE_DEPENDENCY_GRAPH.md` | **`CLUE_*` register; `GRANT_CLUE` semantics** |
| `13_SPLIT_AND_REGROUP_FLOW.md` | Split/regroup architecture and independence tests |
| `14_ENDING_TRIGGER_MATRIX.md` | **`END_*` triggers; `EVAL_ENDING`; priority order** |
| `15_ALPHA_0.2B_REVIEW_DISPOSITION.md` | Review-handling rules |
| `16_EVENT_GRAPH_MAPPING.md` | `ARC_*` ↔ `EVT_*` mapping; unimplemented backbone elements |

### 1.6 Templates (structural reference only)

| Document | Role |
|---|---|
| `templates/EVENT_TEMPLATE.md` | Illustrative YAML field list; **not populated for The Last Witness** |
| `templates/DOCUMENT_TEMPLATE.md` | Document metadata pattern |
| `templates/ISSUE_TEMPLATE.md` | Review issue pattern |

The compiler does not read templates as runtime data. They document intended record shapes only.

### 1.7 Explicitly excluded sources

| Path | Reason |
|---|---|
| `IMPLEMENTATION_PLAN.md`, `IMPLEMENTATION_REPORT_*.md`, `IMPLEMENTATION_READINESS_*.md`, `IMPLEMENTATION_PLAN_CHANGELOG.md` | Historical migration records; not gameplay authority |
| `reviews/` | Review layer per `engine/03_ARCHITECTURE.md` § 3.10; non-authoritative |
| `CHANGELOG.md`, root `README.md` | Repository metadata |
| `docs/STYLE_GUIDE.md` | Formatting conventions for authors; not gameplay logic |
| `adventures/The_Last_Witness/DO_NOT_READ/LOGIC/05_CORE_EVENT_GRAPH.md` backbone arcs | **Not directly compiled to pages.** Mapped to `EVT_*` via `16_EVENT_GRAPH_MAPPING.md` only |
| `adventures/The_Last_Witness/PLAYER/` | Output destination; currently placeholder only |

### 1.8 Precedence when multiple documents describe the same object

Apply in order:

1. **Prefix ownership table** in `LOGIC/00_ENTITY_KEY_TABLE.md` § "Ownership rules".
2. **Declaring document** for the identifier family (see § 1.5).
3. **World Bible** for objective facts about the world that logic references but does not restate.
4. **Marked non-authoritative summaries** (`05_CLUE_ARCHITECTURE.md` § 2–3, `06_ENDING_FRAMEWORK.md` pointer blocks) — never override logic.

| Object | Authoritative owner | Non-authoritative references |
|---|---|---|
| Playable node identity and `Outgoing` | `10_INVESTIGATION_NODE_GRAPH.md` | `16_EVENT_GRAPH_MAPPING.md`, `05_CORE_EVENT_GRAPH.md` |
| Clue classes and thresholds | `07_EVIDENCE_VALIDATION.md` | `05_CLUE_ARCHITECTURE.md`, `12_CLUE_DEPENDENCY_GRAPH.md` (register only) |
| Clue identity, class tags, granting nodes | `12_CLUE_DEPENDENCY_GRAPH.md` | — |
| Ending trigger conditions and priority | `14_ENDING_TRIGGER_MATRIX.md` | `06_ENDING_FRAMEWORK.md` (narrative text only) |
| Terminal node identity and `TERMINAL_TYPE` | `10_INVESTIGATION_NODE_GRAPH.md` § 14 | `14_ENDING_TRIGGER_MATRIX.md` § 6 (cross-reference) |
| Ending narrative epilogue | `06_ENDING_FRAMEWORK.md` | — |
| Variable declarations and writers/readers | `01_WORLD_STATE_VARIABLES.md` | `10_INVESTIGATION_NODE_GRAPH.md` § 15 (node-side write table) |
| Immutable world facts | `01_WORLD_BIBLE.md` | `00_CASE_OVERVIEW.md` |

If two authoritative documents conflict, compilation **halts** and reports a documentation defect. The compiler does not reconcile conflicts.

---

## 2. Compilation pipeline

### 2.1 End-to-end transformation

```text
┌─────────────────────────────────────────────────────────────┐
│ STAGE 0: Repository intake                                   │
│  Read version fields; verify engine_spec_version match       │
└────────────────────────────┬────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────┐
│ STAGE 1: Logic ingestion                                     │
│  Parse LOGIC/* into normalized records:                      │
│  EVT_ nodes, CLUE_ rows, variables, evaluators, edges        │
└────────────────────────────┬────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────┐
│ STAGE 2: Structural validation (compile-time)                │
│  Identifier resolution; graph integrity; reachability;       │
│  writer/reader wiring; threshold satisfiability              │
└────────────────────────────┬────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────┐
│ STAGE 3: Narrative source binding                            │
│  Attach World Bible, character, location material to nodes     │
│  Bind END-* outcome text to terminal families                │
│  **HALT if player-facing prose or choice labels missing**    │
└────────────────────────────┬────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────┐
│ STAGE 4: Variant expansion                                   │
│  For each EVT_* × eligible world-state slice where           │
│  player-facing outcome materially differs, emit a variant      │
└────────────────────────────┬────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────┐
│ STAGE 5: Variant merge                                       │
│  Merge variants with identical player-facing consequences      │
└────────────────────────────┬────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────┐
│ STAGE 6: Public Static Node emission                         │
│  Strip internal IDs; emit public condition tags;             │
│  attach visible state-update instructions; partition P1/P2     │
└────────────────────────────┬────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────┐
│ STAGE 7: Book Formatter handoff (out of compiler scope)        │
│  Page numbers, layout, booklet division, print artifacts       │
└────────────────────────────┬────────────────────────────────┘
                             ↓
                      Player Output
```

Stages 0–6 are **Narrative Compiler** responsibility. Stage 7 is **Book Formatter** responsibility per `engine/04_EXECUTION_MODEL_AND_BOUNDARIES.md` § 3.1.

### 2.2 Stage 1 — Logic ingestion rules

The compiler builds an internal graph from `10_INVESTIGATION_NODE_GRAPH.md`:

- **Nodes:** every `### \`EVT_…\`` heading (48 declared: 40 `INTERMEDIATE`, 8 `TERMINAL`).
- **Edges:** every `**Outgoing**` list on a node, plus section-level `**Outgoing**` blocks that list targets for hub sections (§§ 3–11). When a node lacks its own `Outgoing` block, the compiler **does not infer edges**. It halts and reports a structural defect (see § 8).
- **Off-screen events:** `EVT_801`–`EVT_804` from `06_NPC_SCHEDULE_AND_PRIORITY.md` § 4 are ingested but excluded from player reachability per `10` § 16.
- **Fields per node:** immutable event key, `NODE_TYPE`, `TERMINAL_TYPE` (if terminal), availability window, location (`LOC_*`), player eligibility, entry conditions, time cost, information gained / reveals, state changes, failure transformation, `Outgoing`.

The graph is **not final prose** (`10` § 1). Ingestion treats bullet lists under **Reveals**, **Purpose**, **Decision**, **Core decision**, etc. as **logic annotations**, not as printable player text.

### 2.3 Stage 2 — Structural validation

The compiler must verify, at minimum, the gates defined in `IMPLEMENTATION_PLAN.md` § 13 (as applied to The Last Witness logic):

| Gate | Compile-time requirement |
|---|---|
| Identifier resolution | Every `NPC_`, `LOC_`, `ITEM_`, `CON_`, `CLUE_`, `ARC_`, `EVT_`, `END_`, `CLK_`, `TR_`, `EVAL_` reference resolves |
| Declaration status | Every identifier carries exactly one status |
| Node declaration | Every node has `NODE_TYPE`; terminals have `TERMINAL_TYPE` and `Outgoing: None` |
| Writer/reader resolution | Every variable has non-`INIT` writer and reader |
| Reachability | Every terminal reachable from `EVT_100_SHARED_BRIEFING` per declared play mode |
| Backbone mapping | Every `ARC_*` mapped or marked unimplemented in `16` § 4 |
| Clue integrity | Every `ACTIVE` clue has granting node; uniform point value; idempotent `GRANT_CLUE` |
| Solvability | Every conclusion threshold satisfiable from reachable clues |
| Single source | No duplicate authoritative owners |
| Ending precedence | Priority order in `14` § 1 resolves overlaps |

`V8` (time-integrity split-window conflict) is **deferred** per `IMPLEMENTATION_PLAN.md` § 13. The compiler records the deferral but does not block on `V8` unless a future engine revision promotes it.

### 2.4 Stage 3 — Narrative source binding

For each `EVT_*`, the compiler requires **authored player-facing material** not present in logic-only bullets. Acceptable sources, in precedence order:

1. **Dedicated narrative records** in `PLAYER/` or a future Alpha 0.3 narrative layer (not yet authored).
2. **Nowhere else.** World Bible, character database, and location database supply **reference facts** for authoring; they are not themselves player-page text and must not be concatenated into scenes without a narrative record that selects and frames them.

If Stage 3 cannot bind printable narrative text and choice labels for a node, compilation **halts** for that node.

### 2.5 Stage 4 — Variant expansion

Per `engine/04_EXECUTION_MODEL_AND_BOUNDARIES.md` § 5, create a separate public variant only when player-facing outcome materially changes:

- available choices;
- revealed clues;
- time cost;
- item or state updates;
- NPC presence or behavior;
- terminal outcome.

Material difference is evaluated from **logic fields**, not from hypothetical player knowledge.

### 2.6 Stage 5 — Variant merge

Merge variants with identical:

- choice set (same targets and public labels);
- visible clue grants;
- visible time cost;
- visible state-update instructions;
- terminal type (if terminal).

### 2.7 Stage 6 — Public Static Node emission

Each emitted Public Static Node (`engine/03_ARCHITECTURE.md` § 3.7) contains:

| Field | Source |
|---|---|
| Public node identity | Compiler-generated stable slug; **not** `EVT_*` |
| Narrative text | Bound narrative record (Stage 3) |
| Visible conditions | Translated from entry conditions using public condition tags (§ 4 of `engine/04`) |
| Choices | Bound choice labels + public target references |
| Check instructions | Bound check records, if any |
| Visible state updates | Translated from **State changes** the adventure marks as player-recordable |
| Outgoing public references | Public identities of target nodes |

Internal identifiers (`EVT_*`, `CLUE_*`, variable names) are **removed** from player-visible fields.

---

## 3. Page generation

### 3.1 Definition

In IDNE terminology, a **gamebook page** is a **Public Static Node** after Stage 6, before the Book Formatter assigns physical page numbers.

One `EVT_*` logic node may compile to:

- zero public nodes (if compilation halts — missing narrative);
- one public node (default);
- multiple public nodes (if variant expansion produces materially different player-facing outcomes that cannot be merged).

### 3.2 Page identity

| Layer | Identity | Visibility |
|---|---|---|
| Logic | `EVT_*` immutable key | **Hidden** from players (`engine/03_ARCHITECTURE.md` § 3.14) |
| Compiler output | Public node slug, e.g. `pub_opening_briefing` | Internal to compiler/formatter pipeline |
| Formatter output | Public event number or page reference | **Visible** to players; may change between builds |

The compiler assigns a **stable public slug** per Public Static Node. The Book Formatter assigns **page numbers**; the compiler must not assign final page numbers (`engine/03_ARCHITECTURE.md` § 3.6).

### 3.3 Page numbering strategy

**Outside compiler responsibility.** Assigned by Book Formatter per `engine/03_ARCHITECTURE.md` § 3.8.

The formatter may use sequential numbering, section-based numbering, or booklet-specific numbering. The compiler emits cross-references as public slugs; the formatter resolves slugs to page numbers.

### 3.4 Displayed title

| Source | Rule |
|---|---|
| Logic `EVT_*` heading | Internal only; never displayed |
| Narrative record `title_player` field | **Required compiler dependency** — not present in current repository |
| Formatter heading | Derived from narrative record title at layout time |

If no player title is authored, compilation halts. The compiler does not generate titles from `Purpose` bullets.

### 3.5 Narrative source

For each public node, narrative text must originate from an **authored narrative record** bound to the `EVT_*` key.

**Permitted reference inputs** (for human or AI authoring of that record, not for direct concatenation by the compiler):

| Reference | Use |
|---|---|
| `10` node fields: **Reveals**, **Purpose**, **Core decision**, **Core tension**, **Observable facts** | Logic constraints on what the scene may state |
| `01_WORLD_BIBLE.md` | Objective facts the scene may reveal |
| `03_CHARACTER_DATABASE.md` | Character voice and knowledge limits |
| `04_LOCATION_DATABASE.md` | Sensory and spatial detail (`11` § 1 instructs compiler to combine location dimensions into scene text) |
| `02_MASTER_TIMELINE.md` | Time-anchored background events |

The compiler **copies none of these automatically** into player text. They constrain authoring. Absent authored text, compilation halts.

### 3.6 Player-visible content

A compiled page exposes only:

- narrative prose from the narrative record;
- public condition tags (`engine/04` § 4);
- choice labels;
- check instructions (if `CHK_*` records exist);
- explicit record-sheet instructions (time advance, clue card issuance, tick boxes);
- visible world-time statements derived from `CLOCK` when the logic node specifies a cost or window.

A compiled page must **not** expose:

- raw variable names (`T_NADIA`, `P_ROOK`, `A_ROOK_PLAYERS`, etc.);
- internal evaluator names (`EVAL_*`);
- `GRANT_CLUE` syntax;
- `ARC_*` backbone identifiers;
- off-screen `EVT_8xx` resolution logic.

### 3.7 Hidden engine data retained internally

The compiler retains, internal to its build artifact:

- full `EVT_*` → public slug mapping;
- entry conditions in internal form;
- complete state-change scripts;
- `GRANT_CLUE` targets and knowledge-set routing;
- conclusion evaluator bindings;
- variant merge provenance;
- play-mode flags (solo vs two-player reachability).

Players never see this data (`engine/04` § 3.2).

### 3.8 Page transitions

| Logic field | Compiled behavior |
|---|---|
| `**Outgoing**` list | Becomes the **choice set** (after binding labels) |
| Entry conditions on target nodes | Become public condition tags on choices or target pages |
| `NODE_TYPE: TERMINAL` + `Outgoing: None` | Terminal page; no forward choices |
| Time cost on traversed edge | Visible instruction: advance shared clock by N minutes when players move to the page |

The compiler does not create transitions not present in `Outgoing`. It does not add "go back" links unless authored.

### 3.9 Terminal pages

Terminal nodes (`10` § 14) compile to terminal public pages.

| `EVT_*` | `END_*` family | `TERMINAL_TYPE` | Narrative source |
|---|---|---|---|
| `EVT_901` | `END_WITNESS_SPEAKS` | `VICTORY` | `06` END-01 |
| `EVT_902` | `END_EVIDENCE_WITHOUT_WITNESS` | `PARTIAL_SUCCESS` | `06` END-02 |
| `EVT_903` | `END_LIFE_SAVED_TRUTH_DELAYED` | `PARTIAL_SUCCESS` | `06` END-03 |
| `EVT_904` | `END_PROTECTIVE_CUSTODY` | `NARRATIVE_FAILURE` | `06` END-04 |
| `EVT_905` | `END_PUBLIC_LEAK` | `PARTIAL_SUCCESS` | `06` END-05 |
| `EVT_906` | `END_SILENT_TERMINAL` | `TIME_EXPIRED` | `06` END-06 |
| `EVT_907` | `END_WRONG_ACCUSATION` | `CASE_UNRESOLVED` | `06` END-07 + rebuttal logic from `14` § 7 |
| `EVT_908` | `END_FRACTURED_TRUTH` | `PARTIAL_SUCCESS` | `06` END-08 |

**Ending dispatch** (`EVT_900`) is an internal routing node. The compiler resolves `EVAL_ENDING` at compile time over all reachable world-state slices, emitting the appropriate terminal public page variant per `14` § 1 priority order. Players receive a terminal page, not a dispatch menu.

`EVT_908` is reachable only in two-player mode (`10` § 14). Solo play artifacts must exclude or mark unreachable this terminal per `IMPLEMENTATION_PLAN.md` § 15.

---

## 4. Choices

### 4.1 Logic-to-choice mapping

Each identifier in a node's `**Outgoing**` list becomes **one player choice** leading to the compiled public page for that target `EVT_*`.

If a node has N outgoing targets, the compiled page has at most N forward choices (fewer if entry conditions make a target impossible — those become condition-gated choices or separate variants per § 2.4).

**Decision blocks** (e.g. `EVT_100` **Decision** with "split immediately" vs "investigate together") are not separate `Outgoing` edges today. They are expressed via `EVT_100` section-level `Outgoing` to `EVT_110` and `EVT_120`. The compiler requires **authored choice labels** for each outgoing target. It does not derive labels from logic bullets such as "split immediately".

### 4.2 Choice wording origin

| Required input | Status in repository |
|---|---|
| Player-facing choice label per outgoing target | **Missing** — compiler dependency |
| Public target reference (slug or formatter page number) | Produced by compiler/formatter |
| Condition gating text | Produced from entry conditions only when a public condition tag is defined |

**Rule:** If choice wording is not authored, compilation halts. The compiler must not:

- paraphrase **Decision** bullets into labels;
- use `EVT_*` suffixes as labels;
- use location or NPC names alone as labels unless a narrative record specifies them as the label.

### 4.3 Condition-gated choices

When a target's **Entry conditions** reference player-visible state, the compiler emits a public condition tag per `engine/04` § 4:

```text
[IF YOU HAVE <public item/clue reference>]
[IF PLAYER 2 KNOWS <public clue reference>]
[IF WORLD TIME IS <visible time> OR LATER]
```

Public references use **player-facing clue/item names** from narrative records, not `CLUE_*` identifiers.

If an entry condition references state that has no public tag mapping authored, compilation halts.

### 4.4 Checks as choices

`engine/01_INTRODUCTION_AND_SCOPE.md` § 1.2 expects a D20 resolution system. Adventure logic defines check resolution in `adventures/The_Last_Witness/DO_NOT_READ/LOGIC/17_CHECK_REGISTER.md` (MBD-01): `roll = d20 + character_modifier`; success when `roll >= dc`; bands Easy 5 / Medium 10 / Hard 15. One `ACTIVE` record: `CHK_115_PERCEPTION` (DC 10).

Check-gated branches without a complete `CHK_*` record in `17_CHECK_REGISTER.md` remain blocked at compile time.

---

## 5. Hidden engine state

### 5.1 Principle

Play-time has **no runtime compiler** (`engine/04` § 3.2). The compiler resolves all hidden evaluation at compile time where possible, and emits **explicit player instructions** for state that players must record on sheets.

### 5.2 Variables

| Category | Examples | Compiler handling |
|---|---|---|
| Stored variables | `CLOCK`, `T_NADIA`, `ELIAS_STATE`, `APT_STATE`, … | Evaluate at compile time for variants; emit visible update instructions only where logic specifies player-recordable changes |
| Derived totals | `P_STAGED`, `P_HARBOR`, … | **Never exposed**; evaluated only via conclusion evaluators |
| Knowledge sets | `P1_PRIVATE_KNOWLEDGE_SET`, `P2_PRIVATE_KNOWLEDGE_SET`, `SHARED_KNOWLEDGE_SET` | Drive clue visibility; emit clue cards/passages, not set names |

`01_WORLD_STATE_VARIABLES.md` § 2: derived totals are computed from held clues, never stored. The compiler must not emit point counters.

### 5.3 State changes

Logic **State changes** blocks may contain:

- variable assignments (`P1_LOCATION = LOC_ELIAS_APT`);
- `GRANT_CLUE(CLUE_…)`;
- trust/awareness deltas described in prose (`T_NADIA +1`).

| Syntax | Player visibility |
|---|---|
| `GRANT_CLUE(CLUE_X)` | Clue card or bounded passage; record clue on sheet using **public clue name** |
| `T_NADIA +1` | **Compiler dependency** — requires authored record-sheet instruction unless auto-applied at compile time with no player tracking |
| `P1_LOCATION = …` | Internal; affects eligibility only |
| `ELIAS_STATE`, `ROOM_4B_STATE` transitions | Emit only if logic marks visible effect |

The compiler must not invent record-sheet fields. `engine/04` § 7 requires all state to fit one shared sheet plus one private sheet per player — **sheet layouts are not authored** (compiler dependency).

### 5.4 Clue acquisition

`GRANT_CLUE` (`12` § 1) rules:

1. Idempotent — duplicate grants are no-ops.
2. Writes to acting player's private set, or `SHARED_KNOWLEDGE_SET` for joint scenes.
3. `EVT_150` and `EVT_300` move private clues to shared set at regroup.

Compiled output:

- **Private clue:** inserted into the eligible player's booklet section or issued as a knowledge card (`08` § 7).
- **Shared clue:** inserted into shared case file material.
- Clue **wording** must come from a narrative clue record — **not present** for most clues (compiler dependency). Logic register rows name identifiers and classes only.

`DEFINITION_ONLY` clues (`23` of 66) have no granting node. The compiler never emits acquisition text for them.

### 5.5 Conclusions

Conclusions (`CON_*`) are **never player-visible mechanics**. They are evaluated at compile time (for variant generation) and at play-time only through **authored diegetic outcomes** (e.g. a scene that becomes available when thresholds are met).

Evaluators in `07` § 7 read held clue sets. The compiler implements evaluator logic internally; players see only resulting public pages whose entry conditions are satisfied.

### 5.6 Progress

Progress is clue-based only. No mutable point totals. Compiler enforces idempotence and derived totals per `12` § 1.

### 5.7 Identifier status

`ACTIVE`, `DEFINITION_ONLY`, `RESERVED`, `DEPRECATED` affect compilation:

| Status | Compiler behavior |
|---|---|
| `ACTIVE` | Normal compilation path |
| `DEFINITION_ONLY` | Register only; no acquisition emission; must not appear as granted |
| `DEPRECATED` | Must not appear in new conditions (`CON_MARCUS_LEAK`, `CON_ROOK_COMPROMISED`) |
| `RESERVED` | Not used in The Last Witness |

### 5.8 Internal bookkeeping

The compiler maintains:

- world-state slice index for variant expansion;
- `EVAL_ENDING` simulation traces;
- mapping tables (public slug ↔ `EVT_*` ↔ formatter page);
- play-mode matrix (solo / two-player);
- audit log of halted nodes and missing dependencies.

None of this is player-facing.

---

## 6. Multiplayer handling

### 6.1 Delivery model

`engine/03_ARCHITECTURE.md` § 3.15 requires declaring one model before production:

| Model | Description |
|---|---|
| A — Shared book | Mostly shared scenes; private info via cards/sections |
| B — Separate booklets | Separate narrative streams per player |
| C — Shared book plus companion | Shared core + private companion |

**Status:** No model is declared for The Last Witness. This is a **compiler blocker** for final artifact packaging (see § 10).

The compiler must still partition content by **Players** field on each `EVT_*` node.

### 6.2 Player eligibility field

Each node declares **Players:** `both`, `Player 1`, `Player 2`, or equivalent.

| Value | Compilation partition |
|---|---|
| `both` | Shared public node in both streams (or shared book) |
| `Player 1` | P1 booklet section only |
| `Player 2` | P2 booklet section only |
| `Player 1, or both if chosen` | Shared node with optional P1-only entry path — requires authored fork text |

### 6.3 Split paths

Split architecture is defined in `13_SPLIT_AND_REGROUP_FLOW.md` and `08_TWO_PLAYER_CORE_RULES.md`:

| Split | Window | P1 branch nodes | P2 branch nodes | Regroup |
|---|---|---|---|---|
| Split One | Opening | `EVT_110`–`EVT_115` | `EVT_120`–`EVT_123` | `EVT_150` (~21:20–21:40) |
| Split Two | Midgame | § 6 harbor / § 7 police / § 8 medical / § 9 Marcus-Reed clusters | (paired per `13` § 4) | `EVT_300` (≤23:15) |
| Final act | Terminal | Parallel roles per `08` § 6 | Parallel roles per `08` § 6 | Converge at `EVT_900` dispatch |

**Engine requirement not met:** `engine/05_TWO_PLAYER_SYNCHRONIZATION.md` § 3 requires every scene declare **Joint**, **Split**, or **Solo** mode. No `EVT_*` node declares scene mode. Compiler cannot emit split-scene boundaries or communication legality banners without this field.

**Engine requirement not met:** § 5 requires split branches terminate in `REJOIN`, `REMOTE_CONTACT`, `WAIT_UNTIL_SYNC`, `EMERGENCY_INTERRUPT`, or `TERMINAL_OUTCOME`. These terminators are not declared on nodes (`IMPLEMENTATION_PLAN.md` § 14.2 — deferred).

### 6.4 Synchronization

Shared clock (`CLOCK` / `WORLD_TIME`) advances per `engine/03_ARCHITECTURE.md` § 3.16:

1. Both branches start at same timestamp.
2. Each action has a duration from `04_TIME_COST_MATRIX.md` and node **Cost**.
3. Branch defines next synchronization point.
4. Clock advances to synchronization timestamp at regroup.
5. Shorter branch gets only predefined waiting/communication options.

`04` § 3: compiler must avoid free extra turns from shorter parallel actions.

**Deferred:** Maximum split-window durations are not declared (`V8` deferred). Compiler cannot validate window bounds deterministically.

### 6.5 Regroup events

| Node | Function | Compiled behavior |
|---|---|---|
| `EVT_150` | Regroup One | Shared page; instruction to merge private clues into shared case file; joint deduction prompts |
| `EVT_300` | Regroup Two | Shared page; mandatory planning outputs listed in logic |

Regroup pages require **authored narrative** (compiler dependency).

### 6.6 Shared vs independent information

| Set | Owner | Compiled as |
|---|---|---|
| `P1_PRIVATE_KNOWLEDGE_SET` | Player 1 | P1-only passages/cards |
| `P2_PRIVATE_KNOWLEDGE_SET` | Player 2 | P2-only passages/cards |
| `SHARED_KNOWLEDGE_SET` | Both | Shared case file entries |

Communication modes (`08` § 4): physical regroup (10 min), phone (5 min, one clue), message (delayed), emergency broadcast. Compiled books must state when each mode is legal — requires **authored callout text** per scene (compiler dependency).

`13` § 8: player books must not assume unrestricted table talk during isolated scenes.

### 6.7 Ending evaluation

`EVAL_ENDING` (`14` § 1) runs over ending variables in `01` § 9 and `ELIAS_STATE`. Resolution order:

1. Medical outcome
2. Ledger/transfer
3. Rescue controller
4. Rook proof
5. Krell/Vale proof
6. Public accusation
7. Secondary character consequences
8. Select family by priority table (§ 1)

Compiler emits one terminal public page per reachable outcome slice. `14` § 8 modifiers enrich epilogue but do not replace the main family.

Wrong-accusation path (`EVT_907`): compiler must select rebuttal category from `14` § 7 based on missing proof — **requires authored rebuttal text per category** (compiler dependency).

---

## 7. Validation

### 7.1 Compiler must preserve engine invariants

After compilation, the following must remain true:

| Invariant | Source |
|---|---|
| Objective truth unchanged | `engine/02_DESIGN_PRINCIPLES.md` § 2.1 |
| No invented consequences | `engine/03_ARCHITECTURE.md` § 3.6 |
| Every public choice resolves to valid target | `engine/04` § 3.1 |
| Clue redundancy for mandatory conclusions | `07` § 6, `12` § 12 |
| At least two terminal access routes in every legal state | `07` § 6 |
| No single skill gate on mandatory conclusions | `07` § 5 |
| Terminal nodes typed per `engine/03` § 3.18 | `10` § 14 |
| Ending priority first-match-wins | `14` § 1 |
| Internal IDs hidden from players | `engine/03` § 3.14 |
| Two-player split safety (no cross-player live puzzle lock) | `08` § 3, `13` § 2 |
| Parallel action anti-exploit | `04` § 3 |

### 7.2 Post-compilation checks

The compiler runs:

1. **Reference integrity** — every public choice target exists.
2. **Spoiler partition** — P1 booklet contains no P2-private nodes; vice versa.
3. **Terminal reachability** — every emitted terminal corresponds to a valid `EVAL_ENDING` outcome.
4. **Clue emission audit** — every emitted clue maps to an `ACTIVE` `GRANT_CLUE` path.
5. **No orphan public nodes** — every public node reachable from opening slug except declared terminals.
6. **Variant merge audit** — no merged variants that differ in material outcomes.

### 7.3 Formatter validation (handoff)

The Book Formatter additionally verifies page references, layout constraints, and booklet boundaries. Those checks are outside this specification.

---

## 8. Error handling

### 8.1 Absolute rules

When required information is missing, the compiler must:

1. **Never invent** data, prose, choices, routes, checks, or timings.
2. **Never infer** gameplay from World Bible prose alone.
3. **Never guess** `Outgoing` edges not declared in logic.
4. **Never silently skip** a node.

### 8.2 Error classification

Per `engine/06_PROTOTYPE_SCOPE_AND_VALIDATION.md` § 9:

| Class | Meaning | Action |
|---|---|---|
| `ENGINE_RULE_DEFECT` | Engine requires field adventure does not provide | Halt; report engine/adventure gap |
| `ADVENTURE_LOGIC_DEFECT` | Graph integrity, missing writer, unsatisfiable threshold | Halt; report logic file and identifier |
| `COMPILER_REQUIREMENT` | Logic complete but narrative/label/sheet artifact missing | Halt; report missing dependency name |
| `FORMATTER_DEFECT` | Invalid handoff artifact | Formatter stage only |

### 8.3 Error record format

Each halt emits:

```text
ERROR <CLASS>
  stage: <pipeline stage 0–6>
  file: <repository path>
  section: <heading or § reference>
  identifier: <EVT_*, CLUE_*, etc. if applicable>
  missing: <what is absent>
  reason: <why deterministic compilation is impossible>
```

### 8.4 Non-fatal warnings

Warnings (compilation may proceed for other nodes) are permitted only for:

- `DEFINITION_ONLY` clues ungranted by design;
- unimplemented backbone elements listed in `16` § 4;
- deferred `V8` time-window validation.

Warnings must not waive missing narrative text or choice labels.

---

## 9. Output

### 9.1 Compiler output artifact

The Narrative Compiler produces a **Public Static Node Package**:

```yaml
adventure_id: the_last_witness
engine_spec_version: "2.0"
adventure_schema_version: "1.0"
play_modes: [two_player]  # solo not implemented
delivery_model: null        # must be set before formatting
public_nodes:
  - public_slug: ...
    source_evt: EVT_...    # internal; stripped before player delivery
  - title_player: ...
    players: [shared | p1 | p2]
    scene_mode: null       # required by engine; missing in logic
    narrative_text: ...
    conditions: [...]
    choices: [...]
    checks: [...]
    visible_updates: [...]
    terminal_type: null | VICTORY | ...
    ending_family: null | END_...
knowledge_cards: [...]
shared_case_entries: [...]
halted_nodes: [...]
warnings: [...]
```

### 9.2 Formatter output (reference)

The Book Formatter consumes the package and produces **Player Output** (`engine/03` § 3.9):

| Artifact | Planned path | Status |
|---|---|---|
| Spoiler-free readme | `PLAYER/00_READ_ME_FIRST.md` | Not authored |
| Quick rules | `PLAYER/01_QUICK_RULES.md` | Not authored |
| Shared case file | `PLAYER/02_SHARED_CASE_FILE.md` | Not authored |
| Player 1 book | `PLAYER/PLAYER_1_BOOK.md` | Not authored |
| Player 2 book | `PLAYER/PLAYER_2_BOOK.md` | Not authored |
| Printable investigation sheets | `PLAYER/` | Not authored |

Per `07_PROTOTYPE_BUILD_PLAN.md` Alpha 0.4.

### 9.3 What the compiler does not output

- PDF layout or typography
- Page numbers (formatter)
- Index
- Facilitator scripts
- Digital runtime
- Any content not traceable to repository sources

---

## 10. Compilation Readiness Assessment

### NOT READY

The IDNE engine specification is sufficient to define **how** compilation must work. The repository, taken as the complete input corpus for The Last Witness, **does not yet contain every specification required to compile a complete playable gamebook without making gameplay decisions or inventing content.**

Logic-layer structure (Alpha 0.2c) is unusually complete. The **narrative and player-artifact layer** (Alpha 0.3 and Alpha 0.4 in `07_PROTOTYPE_BUILD_PLAN.md`) is not started. The compiler cannot lawfully bridge that gap by generating prose, choice labels, or record-sheet layouts from logic bullets alone.

---

### Missing specifications

#### MS-01 — Player-facing narrative text

| Field | Detail |
|---|---|
| **Missing information** | Authored scene prose for all 48 playable `EVT_*` nodes (and any variant splits) |
| **Affected stage** | Stage 3 (Narrative source binding); Stage 6 (emission) |
| **Why deterministic compilation is impossible** | Logic nodes contain purpose/reveal bullets, not printable text. Engine forbids compiler from inventing wording (`engine/03` § 3.6). `adventures/The_Last_Witness/README.md` states narrative compilation is reserved for Alpha 0.3 |
| **Issue type** | Documentation / content gap (planned Alpha 0.3) |

#### MS-02 — Player-facing choice labels

| Field | Detail |
|---|---|
| **Missing information** | One authored label per `Outgoing` target per node; decision labels for branch forks |
| **Affected stage** | Stage 3; Stage 6 (choices) |
| **Why deterministic compilation is impossible** | `Outgoing` lists name only `EVT_*` targets. Engine requires player-facing choice wording from compiler output, not internal IDs. No label registry exists |
| **Issue type** | Documentation / content gap (planned Alpha 0.3) |

#### MS-03 — Clue and knowledge-card text

| Field | Detail |
|---|---|
| **Missing information** | Player-readable text for each `CLUE_*` granted via `GRANT_CLUE` |
| **Affected stage** | Stage 5–6 (clue emission) |
| **Why deterministic compilation is impossible** | `12_CLUE_DEPENDENCY_GRAPH.md` registers identifiers, classes, and granting nodes only. `08` § 7 requires knowledge cards or bounded passages |
| **Issue type** | Documentation / content gap (planned Alpha 0.3) |

#### MS-04 — Check (`CHK_*`) records

| Field | Detail |
|---|---|
| **Missing information** | Check definitions (skill, DC, pass/fail outcomes, player instructions) for branches referenced in failure transformations |
| **Affected stage** | Stage 3–4 (variant expansion) |
| **Why deterministic compilation is impossible** | Resolved for `CHK_115_PERCEPTION` via `17_CHECK_REGISTER.md` (MBD-01). Other failure transformations without `CHK_*` records remain blocked. |
| **Issue type** | Engine/adventure gap |

#### MS-05 — Public condition tag mapping

| Field | Detail |
|---|---|
| **Missing information** | Mapping from internal entry conditions to player-facing public condition tags and public clue/item names |
| **Affected stage** | Stage 4–6 |
| **Why deterministic compilation is impossible** | `engine/04` § 4 defines tag format but adventure provides no instance mappings. Entry conditions reference internal variables (`T_MINA >= +1`, etc.) |
| **Issue type** | Documentation / content gap |

#### MS-06 — Record sheet and tracker layouts

| Field | Detail |
|---|---|
| **Missing information** | Shared record sheet, private knowledge sheet, and time tracker layouts with field names matching visible update instructions |
| **Affected stage** | Stage 6 (visible state updates) |
| **Why deterministic compilation is impossible** | `engine/04` § 7 mandates fit on one shared plus one private sheet. No sheet templates exist in `PLAYER/` |
| **Issue type** | Documentation / content gap (planned Alpha 0.4) |

#### MS-07 — Two-player delivery model declaration

| Field | Detail |
|---|---|
| **Missing information** | Declared choice among Model A, B, or C (`engine/03` § 3.15) |
| **Affected stage** | Stage 6–7 (artifact packaging) |
| **Why deterministic compilation is impossible** | Compiler cannot determine whether to emit one book, two booklets, or shared+companion without a declared model |
| **Issue type** | Documentation gap |

#### MS-08 — Scene mode per node

| Field | Detail |
|---|---|
| **Missing information** | `Joint`, `Split`, or `Solo` declaration on every playable scene |
| **Affected stage** | Stage 6 (multiplayer partition); split communication callouts |
| **Why deterministic compilation is impossible** | `engine/05` § 3 requires scene mode on every scene. No `EVT_*` node declares it |
| **Issue type** | Engine/adventure gap |

#### MS-09 — Split-branch terminator vocabulary

| Field | Detail |
|---|---|
| **Missing information** | Per-branch terminator: `REJOIN`, `REMOTE_CONTACT`, `WAIT_UNTIL_SYNC`, `EMERGENCY_INTERRUPT`, or `TERMINAL_OUTCOME` |
| **Affected stage** | Stage 6 (split flow); synchronization validation |
| **Why deterministic compilation is impossible** | `engine/05` § 5 requires every split branch to declare a terminator. Deferred per `IMPLEMENTATION_PLAN.md` § 14.2 / § 15 |
| **Issue type** | Engine/adventure gap (deferred) |

#### MS-10 — Solo play mode implementation

| Field | Detail |
|---|---|
| **Missing information** | Solo-mode graph, eligibility rules, and artifact set |
| **Affected stage** | Stage 2 (reachability per mode); Stage 6–7 |
| **Why deterministic compilation is impossible** | `engine/06` § 1 requires one-player mode. Logic is two-player-native. `EVT_908` is unreachable in solo. No solo routes authored |
| **Issue type** | Engine/adventure gap |

#### MS-11 — Synchronization window durations

| Field | Detail |
|---|---|
| **Missing information** | Maximum duration per split window (`engine/05` § 4) |
| **Affected stage** | Stage 2 (`V8` validation); Stage 6 (timing instructions) |
| **Why deterministic compilation is impossible** | `04_TIME_COST_MATRIX.md` § 3 and `engine/05` § 4 conflict on leftover-time handling; no maximum window durations declared (`V8` deferred) |
| **Issue type** | Documentation/engine gap (deferred) |

#### MS-12 — Wrong-accusation rebuttal text

| Field | Detail |
|---|---|
| **Missing information** | Authored rebuttal passages per `14` § 7 category (wrong timeline, missing physical presence, etc.) |
| **Affected stage** | Stage 6 (terminal `EVT_907`) |
| **Why deterministic compilation is impossible** | `14` § 7 instructs compiler to select rebuttal by missing proof but provides categories only, not player text. `07` § 3 lists NPC-specific rebuttal facts, not compiled passages |
| **Issue type** | Documentation / content gap |

#### MS-13 — Participation audit fields

| Field | Detail |
|---|---|
| **Missing information** | Per major block: decisions per player, unique clues per player, challenge counts, waiting time, final-act responsibility (`08` § 9) |
| **Affected stage** | Stage 2 (pre-compilation gate); Stage 6 (parity validation) |
| **Why deterministic compilation is impossible** | `08` requires audit **before compilation**. Fields are not populated. Compiler cannot verify participation parity |
| **Issue type** | Documentation gap |

#### MS-14 — Per-node `Outgoing` completeness

| Field | Detail |
|---|---|
| **Missing information** | `**Outgoing**` block on eleven `INTERMEDIATE` nodes: `EVT_115`, `EVT_123`, `EVT_150`, `EVT_212`, `EVT_223`, `EVT_232`, `EVT_243`, `EVT_300`, `EVT_314`, `EVT_331`, `EVT_440` |
| **Affected stage** | Stage 1 (ingestion); Stage 2 (reachability) |
| **Why deterministic compilation is impossible** | `10` § 1 and `engine/03` § 3.18 require every `INTERMEDIATE` node to declare outgoing targets. Compiler must not infer edges (`§ 8.1`) |
| **Issue type** | Adventure logic defect |

#### MS-15 — Formal Public Static Node schema

| Field | Detail |
|---|---|
| **Missing information** | Executable schema for compiler output records |
| **Affected stage** | Stage 6–7 handoff |
| **Why deterministic compilation is impossible** | `data_dictionary/README.md` lists planned types but states schemas are deferred. No machine-readable contract for formatter input |
| **Issue type** | Documentation gap (deferred per `engine/06` § 3) |

#### MS-16 — Ending identifier status stale metadata

| Field | Detail |
|---|---|
| **Missing information** | `14_ENDING_TRIGGER_MATRIX.md` § 9 lists seven `END_*` families as `DEFINITION_ONLY` although terminal nodes now reference them |
| **Affected stage** | Stage 2 (`V2` declaration status) |
| **Why deterministic compilation is impossible** | Contradictory status breaks deterministic identifier validation unless compiler applies override rules not present in repository |
| **Issue type** | Documentation defect |

---

### Readiness summary

| Layer | Status |
|---|---|
| Engine specification | Complete for defining compiler behavior |
| Adventure logic (Alpha 0.2c) | Structurally complete with known defects (MS-14, MS-16) |
| Narrative layer (Alpha 0.3) | **Not started** (MS-01, MS-02, MS-03, MS-05, MS-12) |
| Playable package (Alpha 0.4) | **Not started** (MS-06, MS-07) |
| Two-player engine fields on nodes | **Missing** (MS-08, MS-09, MS-11) |
| Solo mode | **Not implemented** (MS-10) |
| Check system | **Specified** for `CHK_115_PERCEPTION` (`17_CHECK_REGISTER.md`; MBD-01) |
| Output schema | **Deferred** (MS-15) |

**Conclusion:** Compilation must be classified **NOT READY** until MS-01 through MS-16 are resolved. The compiler specification in this document is sufficient to guide implementation; the repository inputs are not yet sufficient to produce output without invention.

---

## Appendix A — Quick reference: `EVT_*` node inventory

The compiler ingests exactly these playable nodes from `10_INVESTIGATION_NODE_GRAPH.md`:

`EVT_100`, `EVT_110`–`EVT_115`, `EVT_120`–`EVT_123`, `EVT_150`, `EVT_210`–`EVT_212`, `EVT_220`–`EVT_223`, `EVT_230`–`EVT_232`, `EVT_240`–`EVT_243`, `EVT_300`, `EVT_310`–`EVT_314`, `EVT_330`–`EVT_331`, `EVT_400`, `EVT_410`, `EVT_420`, `EVT_430`, `EVT_440`, `EVT_900`, `EVT_901`–`EVT_908`.

Off-screen: `EVT_801`–`EVT_804` (not player pages).

---

## Appendix B — Compiler responsibilities the engine explicitly forbids

From `engine/03_ARCHITECTURE.md` § 3.6 and `engine/04` § 6, the compiler must never:

- change objective truth;
- invent consequences;
- remove required logic;
- expose raw internal state;
- assign final page numbers;
- resolve broken graph structure by inference;
- evaluate hidden conditions at play-time;
- alter time costs;
- modify clue content;
- decide which narrative variant is correct at format time.

---

## Appendix C — Document revision

| Version | Change |
|---|---|
| 1.0 | Initial compiler specification for The Last Witness reference adventure |
