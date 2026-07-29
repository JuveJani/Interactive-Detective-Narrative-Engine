---
title: Content Generation Specification
version: 1.0
status: Draft
depends_on:
  - BOOK_COMPILER_SPEC.md
  - engine/02_DESIGN_PRINCIPLES.md
  - engine/03_ARCHITECTURE.md
  - engine/05_TWO_PLAYER_SYNCHRONIZATION.md
  - adventures/The_Last_Witness/README.md
used_by:
  - adventures/The_Last_Witness/PLAYER/
last_review:
reviewer:
---

# Content Generation Specification

## 0. Purpose and scope

This document specifies how an automated **authoring system** generates every player-facing artifact required **before** book compilation.

### 0.1 Position in the pipeline

```text
Engine Specification
        ↓
Data Dictionary and Schemas
        ↓
World Bible
        ↓
Adventure Logic
        ↓
Content Generation  ← this specification
        ↓
Narrative Record Package
        ↓
Narrative Compiler (BOOK_COMPILER_SPEC.md)
        ↓
Book Formatter
        ↓
Player Output
```

The generator is an **authoring layer**. It transforms engine information into narrative presentation. It is **not** the Narrative Compiler and **not** the Book Formatter.

### 0.2 What this document is

- The formal specification for producing the **Narrative Record Package** consumed by `BOOK_COMPILER_SPEC.md` Stage 3 (Narrative source binding).
- A deterministic constraint system for AI or human-assisted authoring.
- The bridge between Alpha 0.2 logic and Alpha 0.3 narrative compilation described in `adventures/The_Last_Witness/DO_NOT_READ/07_PROTOTYPE_BUILD_PLAN.md`.

### 0.3 What this document is not

- A gameplay design document. It does not add routes, clues, variables, conditions, timings, state changes, endings, or mechanics.
- A compiler specification. See `BOOK_COMPILER_SPEC.md`.
- A prose output. It defines rules only; it does not generate scenes.
- Permission to modify adventure logic files. Generated content is written to the narrative layer (`PLAYER/` or an equivalent Alpha 0.3 narrative directory), never into `DO_NOT_READ/LOGIC/`.

### 0.4 Core constraint

**Narrative may expand presentation. It must never alter logic.**

Every generated artifact must be traceable to an authoritative repository source. If a required gameplay fact cannot be expressed without invention, generation **halts** and reports an authoring or engine defect.

### 0.5 Reference adventure

All paths and examples refer to **The Last Witness** (`adventures/The_Last_Witness/`), Prototype Alpha 0.2c logic with Alpha 0.3 narrative not yet started per `adventures/The_Last_Witness/README.md`.

---

## 1. Authoring inputs

### 1.1 Authoritative read order

The generator reads sources in dependency order. A lower layer must not override a higher layer.

```text
Engine Specification (presentation rules)
        ↓
World Bible (objective facts, tone)
        ↓
Adventure Logic (playable structure, grants, edges)
        ↓
Reference databases (character, location, timeline detail)
```

The generator **writes** narrative records. It **never writes** logic.

### 1.2 Engine inputs (presentation rules)

| Document | Generator use |
|---|---|
| `engine/00_ENGINE_SPECIFICATION_2.0.md` | Master index; fair-play boundary |
| `engine/01_INTRODUCTION_AND_SCOPE.md` | Genre, D20 expectation, two-player use case, fair-play |
| `engine/02_DESIGN_PRINCIPLES.md` | **§ 2.3** narrator truth rules; **§ 2.14** authoring vs compilation separation; **§ 2.9** print-first transparency; **§ 2.13** two-player equality |
| `engine/03_ARCHITECTURE.md` | **§ 3.6** compiler responsibilities the generator must pre-supply; **§ 3.7** Public Static Node fields; **§ 3.15** delivery models; **§ 3.18** terminal types |
| `engine/04_EXECUTION_MODEL_AND_BOUNDARIES.md` | **§ 4** public condition tag format; **§ 5** variant materiality; **§ 7** record-sheet constraint |
| `engine/05_TWO_PLAYER_SYNCHRONIZATION.md` | Scene modes (§ 3); synchronization windows (§ 4); split terminators (§ 5); knowledge isolation (§ 6); communication as action (§ 7) |
| `engine/06_PROTOTYPE_SCOPE_AND_VALIDATION.md` | Validation mindset; defect classification |

**Precedence:** `engine/02_DESIGN_PRINCIPLES.md` governs narrator behaviour. `engine/03_ARCHITECTURE.md` governs artifact shape. Adventure logic governs facts to present.

### 1.3 World and reference inputs

| Document | Authority | Generator use |
|---|---|---|
| `DO_NOT_READ/01_WORLD_BIBLE.md` | **Authoritative** immutable facts, setting, corruption scheme, tone | Fact ceiling; forbidden contradictions |
| `DO_NOT_READ/02_MASTER_TIMELINE.md` | **Authoritative** fixed and conditional timeline | Clock references; event ordering |
| `DO_NOT_READ/03_CHARACTER_DATABASE.md` | **Authoritative** identity, knowledge, beliefs, lies, disclosure bounds | NPC dialogue limits; fragment wording |
| `DO_NOT_READ/04_LOCATION_DATABASE.md` | **Authoritative** layout, objective clues, time changes | Sensory detail within earned knowledge |
| `DO_NOT_READ/06_ENDING_FRAMEWORK.md` | **Authoritative** narrative outcome text (END-01–END-08) | Ending epilogue source |
| `DO_NOT_READ/00_CASE_OVERVIEW.md` | Non-authoritative summary | Orientation only; never overrides Bible or logic |
| `DO_NOT_READ/05_CLUE_ARCHITECTURE.md` | Non-authoritative pointer | Must not override `LOGIC/07` or `LOGIC/12` |
| `DO_NOT_READ/07_PROTOTYPE_BUILD_PLAN.md` | Production sequencing | Alpha 0.3 scope checklist |

### 1.4 Adventure logic inputs (mandatory per artifact)

| Document | Owns | Required for |
|---|---|---|
| `LOGIC/10_INVESTIGATION_NODE_GRAPH.md` | `EVT_*` identity, fields, `Outgoing`, terminals | Scenes, choices, scene eligibility |
| `LOGIC/12_CLUE_DEPENDENCY_GRAPH.md` | `CLUE_*` register, classes, granting nodes, deduction text | Clue cards |
| `LOGIC/07_EVIDENCE_VALIDATION.md` | Clue classes, conclusion thresholds, wrong-accusation categories | Clue tone; rebuttal categories |
| `LOGIC/14_ENDING_TRIGGER_MATRIX.md` | `END_*` triggers, priority, rebuttal selection logic, partial modifiers | Endings, rebuttals |
| `LOGIC/03_NPC_KNOWLEDGE_AND_DISCLOSURE.md` | Disclosure stages, knowledge bounds | Dialogue, interview scenes |
| `LOGIC/08_TWO_PLAYER_CORE_RULES.md` | Communication modes, regroup gates, knowledge-card rule | Multiplayer callouts |
| `LOGIC/13_SPLIT_AND_REGROUP_FLOW.md` | Split independence, regroup timing | Split and regroup scenes |
| `LOGIC/11_LOCATION_STATE_MACHINE.md` | Location state variants | Scene variant selection by `APT_STATE`, etc. |
| `LOGIC/01_WORLD_STATE_VARIABLES.md` | Variable names, knowledge sets | Internal only; drives public tag mapping |
| `LOGIC/04_TIME_COST_MATRIX.md` | Durations | Time instructions in prose |
| `LOGIC/00_ENTITY_KEY_TABLE.md` | Prefix ownership | Precedence resolution |

### 1.5 Compiler contract input

| Document | Role |
|---|---|
| `BOOK_COMPILER_SPEC.md` | Defines required narrative record fields, halt conditions, and handoff shape the generator must satisfy |

The generator output is valid only if `BOOK_COMPILER_SPEC.md` Stage 3 can bind every record without invention.

### 1.6 Templates (structural reference only)

| Document | Role |
|---|---|
| `templates/EVENT_TEMPLATE.md` | Illustrative field names (`visible_information`, `choices`, `narrative_objective`); **not populated** |
| `templates/DOCUMENT_TEMPLATE.md` | Metadata pattern for narrative record files |

Templates inform record shape. They are not runtime data.

### 1.7 Forbidden sources

| Path | Reason |
|---|---|
| `IMPLEMENTATION_PLAN.md`, `IMPLEMENTATION_REPORT_*.md`, `IMPLEMENTATION_READINESS_*.md` | Migration history; not gameplay authority |
| `reviews/` | Non-authoritative review layer |
| `CHANGELOG.md`, root `README.md` duplicates | Repository metadata |
| `BOOK_COMPILER_SPEC.md` § 10 missing-spec list | Blocker registry, not narrative facts |
| Any document marked non-authoritative when it conflicts with an owning document | See precedence § 1.8 |

The generator must not treat implementation debt notes as permission to infer gameplay.

### 1.8 Precedence when multiple documents describe the same object

Apply in order:

1. `LOGIC/00_ENTITY_KEY_TABLE.md` ownership rules.
2. Declaring document for the identifier family (see § 1.4).
3. `01_WORLD_BIBLE.md` for objective world facts logic references but does not restate.
4. Reference databases (`03`, `04`) for presentation detail within knowledge bounds.
5. Non-authoritative summaries — never override logic.

| Object | Authoritative owner | Generator may use from elsewhere |
|---|---|---|
| Playable node facts | `10_INVESTIGATION_NODE_GRAPH.md` | `16_EVENT_GRAPH_MAPPING.md` for arc context only |
| Clue identity and grant | `12_CLUE_DEPENDENCY_GRAPH.md` | `04_LOCATION_DATABASE.md` for physical description |
| Clue classes | `07_EVIDENCE_VALIDATION.md` § 1 | — |
| Conclusion thresholds | `07` § 2 + `12` deduction blocks | Deduction prose in `12` is authoritative for meaning, not player wording |
| Ending triggers | `14_ENDING_TRIGGER_MATRIX.md` | — |
| Ending epilogue meaning | `06_ENDING_FRAMEWORK.md` | `14` § 8 partial modifiers |
| NPC speakable facts | `03_NPC_KNOWLEDGE_AND_DISCLOSURE.md` + character record | Character database beliefs/lies labelled as such |
| Location physical facts | `04_LOCATION_DATABASE.md` | State-gated availability from `11` |

If authoritative documents conflict, generation **halts**. The generator does not reconcile conflicts.

### 1.9 Required engine fields per generated artifact

| Artifact | Mandatory logic fields | Mandatory reference fields |
|---|---|---|
| Scene record (`NAR_EVT_*`) | `EVT_*` key; `NODE_TYPE`; `Outgoing` targets; **Players**; **Location**; **Cost**; **Reveals**; **State changes**; **Entry conditions** (if any); **Failure transformation** (if any) | Matching `LOC_*` entry; participating `NPC_*` records; timeline window |
| Choice label | Parent `EVT_*`; target `EVT_*` from authoritative `Outgoing` | Parent **Decision** / **Routes** / **Branch choice** bullets describing the fork |
| Clue card (`NAR_CLUE_*`) | `CLUE_*` row in `12`; `ACTIVE` status; granting `EVT_*`; class tags | Matching objective clue in `04` if present; location context from granting node |
| Public name mapping | Internal `CLUE_*`, `ITEM_*`, or condition expression | None — mapping is authored but must not change logic |
| Conclusion reveal (`NAR_DEDUCTION_*`) | `CON_*` deduction block in `12`; threshold in `07` § 2 | Regroup node **Joint deductions** list if present |
| Ending epilogue (`NAR_END_*`) | Terminal `EVT_*`; `TERMINAL_TYPE`; `Ending family` / `END_*` | `06_ENDING_FRAMEWORK.md` matching END section; `14` § 8 modifiers if applicable |
| Wrong-accusation rebuttal | `EVT_907`; accusation target from logic | `07` § 3 per-target facts; `14` § 7 category |
| Check instruction | `CHK_*` record | **None in repository** — generation blocked until authored |
| Communication callout | Scene split status; `08` § 4 modes | `05` § 7 if real-time communication applies |

### 1.10 Forbidden generator actions on sources

The generator **must not**:

- edit files under `DO_NOT_READ/LOGIC/`;
- add `Outgoing` edges, `GRANT_CLUE` calls, variables, or conditions to logic;
- upgrade `DEFINITION_ONLY` clues to `ACTIVE`;
- change ending priority or trigger conditions;
- assign `scene_mode` or split terminators into logic files (these belong in narrative record metadata only until logic adopts them).

---

## 2. Scene generation

### 2.1 Definition

A **scene** is the player-facing narrative bound to one `EVT_*` key (or one compile-time variant of that key). One scene record produces one or more Public Static Nodes after compilation.

### 2.2 Transformation rule

```text
EVT_* logic record
  + authoritative reference material
  + narrative record (this specification)
        ↓
Playable scene text + metadata
```

Every **Reveals** bullet, every `GRANT_CLUE` consequence, every trust or awareness delta described in **State changes**, and every **Failure transformation** outcome must remain expressible in the scene or its linked clue cards without adding new gameplay facts.

### 2.3 Scene purpose

| Source | Use |
|---|---|
| `**Purpose**` field | Primary dramatic objective; must be reflected in opening orientation |
| `**Reveals**` bullets | Minimum fact set the scene must convey |
| `**Core decision**` / `**Core tension**` | Decision framing; not copy-pasted as choices |
| `**Information**` / `**Information routes**` | Investigative content bounds |
| Backbone `ARC_*` in node header | Thematic context only; not player text |

The scene must make the purpose legible without stating internal identifiers (`EVT_*`, `CON_*`, `T_MINA`).

### 2.4 Narrator perspective

Per `engine/02_DESIGN_PRINCIPLES.md` § 2.3:

| Rule | Requirement |
|---|---|
| Sensory facts | May describe only what eligible players can perceive |
| NPC intent | Must not state hidden motives as objective fact |
| Limited perspective | Permitted: "He pauses before answering." Forbidden: "He pauses because he plans to escape." |
| NPC speech | May include lies and beliefs per character record; must be attributable to the speaker |
| Documents | May contain forged content; narrator labels source ("The report states…") |

**Joint scenes (`Players: both`):** second-person plural or neutral second-person address ("You arrive…"). Both players read identical text.

**Split scenes (single-player eligibility):** second-person singular addressed to the acting player ("You reach the service corridor…"). Non-acting player receives no scene text for this record.

**Terminal scenes:** epilogue voice; past tense permitted for outcomes already resolved.

### 2.5 Tense

| Scene type | Tense |
|---|---|
| Active investigation scenes | **Present tense** for action and observation |
| Flashback or document quotation | Past tense inside the quoted frame only |
| Ending epilogues | Past or present; must match `06_ENDING_FRAMEWORK.md` outcome framing |
| Master timeline references | Clock times are wall-clock labels, not verb tense |

### 2.6 Maximum length

The engine does not specify word counts. For The Last Witness prototype scope (`07_PROTOTYPE_BUILD_PLAN.md` § Scope controls; `PROTOTYPE_BRIEF.md` § Target Experience):

| Scene class | Soft maximum | Rationale |
|---|---|---|
| Transit / brief nodes | 120 words | ~15-minute cost nodes |
| Standard investigation scene | 350 words | Majority of graph |
| Interview / confrontation | 500 words | Dialogue-heavy nodes |
| Regroup scene | 400 words plus deduction appendix | Knowledge transfer instructions |
| Terminal ending | 600 words | Epilogue plus modifier lines |

Exceeding a soft maximum is a **warning**, not a halt, unless compression would drop a mandatory **Reveals** fact.

### 2.7 Minimum required information

Every scene record **must** include or reference:

1. **title_player** — distinct heading string; not copied from internal node slug.
2. **prose_body** — narrative text covering all **Reveals** applicable to this variant.
3. **world_time_callout** — explicit clock instruction when the node has a **Window** or advances `CLOCK` by **Cost** (e.g. "Advance the shared clock by 10 minutes.").
4. **eligible_players** — `shared`, `p1`, or `p2`; derived from node **Players** field (see § 7).
5. **scene_mode** — `joint`, `split`, or `solo`; derived per § 7.2.
6. **choices** — one record per authoritative `Outgoing` target (see § 3).
7. **clue_card_refs** — list of `NAR_CLUE_*` IDs for every `GRANT_CLUE` in **State changes** for this variant.
8. **visible_update_instructions** — player-recordable instructions for effects that logic marks as visible (trust shifts only when logic ties them to observable NPC behaviour; never expose raw variable names).
9. **communication_notice** — when split, which communication modes are legal per `08` § 4.
10. **location_state_key** — when `11_LOCATION_STATE_MACHINE.md` applies, the `APT_STATE` (or equivalent) variant used.

### 2.8 Optional flavor text

Permitted when it does not add gameplay facts:

- weather and atmosphere from `04_LOCATION_DATABASE.md`;
- architectural detail from location records;
- NPC mannerisms from character **Public presentation**;
- ambient city texture from World Bible § 2;
- non-investigative colour that does not imply new evidence.

Flavor must not introduce new clues, suspects, times, routes, or consequences.

### 2.9 Forbidden additions

| Forbidden | Example |
|---|---|
| New physical evidence | A bloody knife not in logic or location DB |
| New routes or choices | "Search the basement" without `Outgoing` target |
| New timing | "You have five minutes" without `04` or `05` window |
| New state changes | Granting trust not in **State changes** |
| Hidden intent as fact | "Rook is corrupt" before clues support it |
| Cross-player spoilers in split text | Player 1 scene mentioning Player 2's private clue |
| Internal identifiers | `CLUE_APT_BLOOD_OLD`, `T_NADIA`, `CON_HARBOR_DESTINATION` |
| DEFINITION_ONLY clue content | Clues with no granting node |

### 2.10 Variant scenes

Generate a separate scene variant when `BOOK_COMPILER_SPEC.md` § 2.4 materiality applies:

- different **Reveals** or clue grants (e.g. `EVT_113` careful vs rushed search);
- different **Entry conditions** affecting observable content;
- different location state from `11`;
- different eligible player;
- different failure transformation outcome.

Variant key format: `{EVT_ID}__{variant_slug}` where `variant_slug` is derived from logic text (e.g. `careful_search`, `rushed_search`, `apt_state_restricted`).

The generator must not merge variants with materially different clue grants.

### 2.11 Location-state binding

When `11_LOCATION_STATE_MACHINE.md` defines multiple states for a location, the scene must select description lines consistent with the state declared in **Entry conditions** or node context.

Example: `EVT_112_RESTRICTED_APARTMENT` uses `APT_STATE` after `RESTRICTED_BY_ROOK`; prose must not describe unrestricted bedroom access without the legal routes listed in the node **Routes** block.

### 2.12 Nodes with deferred outgoing edges

Eleven `INTERMEDIATE` nodes lack per-node `**Outgoing**` blocks in `10_INVESTIGATION_NODE_GRAPH.md`:

`EVT_115`, `EVT_123`, `EVT_150`, `EVT_212`, `EVT_223`, `EVT_232`, `EVT_243`, `EVT_300`, `EVT_314`, `EVT_331`, `EVT_440`.

Section-level `**Outgoing**` hub lists exist in §§ 4–11 but do not unambiguously assign edges **from** these specific nodes.

**Rule:** The generator must not invent choices for these nodes. Scene prose may be drafted in isolation, but the scene record is **incomplete** until per-node `Outgoing` is authored in logic. See § 12 AR-01.

---

## 3. Choice generation

### 3.1 Mapping rule

Each identifier in the parent node's authoritative `**Outgoing**` list produces exactly **one** choice label record:

```yaml
choice_id: NAR_CHOICE_{PARENT_EVT}__{TARGET_EVT}
parent_evt: EVT_...
target_evt: EVT_...
label_player: "..."
condition_public: null | public tag reference
```

### 3.2 Label wording sources

Labels must be derived from, in precedence order:

1. Parent node **Decision**, **Routes**, **Branch choice**, or **Approach** bullets that describe the fork leading to this target.
2. Target node **Purpose** or location field when the fork is geographic ("Continue to the harbor archive").
3. Target node title slug converted to natural language **only** when (1) and (2) are silent.

The generator must not:

- use raw `EVT_*` strings as labels;
- paraphrase logic into spoilers (see § 3.5);
- add choices not present in `Outgoing`;
- combine two targets into one label.

### 3.3 Maximum length

| Constraint | Value |
|---|---|
| Hard maximum | 80 characters |
| Recommended | 40–60 characters |
| Words | 3–10 words |

Print-first layout per `engine/02` § 2.9.

### 3.4 Style

| Rule | Requirement |
|---|---|
| Voice | Imperative or concise action phrase |
| Point of view | Second person ("Search the service corridor") or neutral infinitive ("Search the service corridor") — pick one style per adventure and keep consistent |
| Articles | Include definite articles when needed for clarity |
| Proper nouns | Use character and location names from `03` and `04` when the fork is NPC- or place-specific |
| Checks | If a choice leads through a check, label describes the action; check instructions are separate (`CHK_*` record) |

### 3.5 Information hiding and spoiler rules

| Rule | Requirement |
|---|---|
| Unrevealed clues | Must not appear in labels |
| Conclusions | Must not name deductions (`CON_*`) |
| Ending paths | Must not telegraph terminal outcomes |
| Trust variables | Must not expose numeric trust |
| Antagonist guilt | Must not assert undiscovered corruption |
| Other player's private knowledge | Must not reference Player 2's unseen clues in Player 1 labels |

**Example** (`EVT_100`):

- Permitted: "Head to Elias's apartment" / "Go to the newsroom"
- Forbidden: "Split up to find staging evidence" (reveals deduction)
- Forbidden: "EVT_110_P1_APARTMENT_APPROACH"

### 3.6 Condition-gated choices

When a target has **Entry conditions** referencing player-visible state, the choice record includes a `condition_public` field referencing a **Public Name Mapping** record (§ 9.2).

Wording format per `engine/04` § 4:

```text
[IF YOU HAVE <public item/clue name>]
[IF PLAYER 2 KNOWS <public clue name>]
[IF WORLD TIME IS <HH:MM> OR LATER]
```

The label itself stays unchanged; the condition tag prefixes or footnotes the choice in compiled output.

### 3.7 Consistency rules

| Rule | Requirement |
|---|---|
| Same fork, same label | Identical parent→target pair uses identical label across variants unless variant changes the action materially |
| Regroup hub choices | Midgame track choices at `EVT_150` / `EVT_300` must use track names from **Branch choice** bullets, not internal arc IDs |
| No duplicate labels on one page | Two choices from the same node must be distinguishable |
| Parallel routes | When multiple routes reach the same target, each source node still owns its own label record |

### 3.8 Decision blocks without separate edges

Nodes like `EVT_100` express decisions in prose but route through section-level `Outgoing`. Labels for `EVT_110` and `EVT_120` must reflect the **Decision** list ("split immediately" vs "investigate together") without exposing that the canonical route is split.

---

## 4. Clue generation

### 4.1 Scope

Generate player-facing text only for `CLUE_*` entries with `ACTIVE` status and a granting node in `12_CLUE_DEPENDENCY_GRAPH.md`.

`DEFINITION_ONLY` clues (23 of 66) are **out of scope**. The generator must not create cards for them.

### 4.2 Transformation rule

```text
CLUE_* register row
  + class tags from 07 § 1
  + objective clue description from 04 (if any)
  + granting scene context from EVT_*
        ↓
Knowledge card (NAR_CLUE_*)
```

### 4.3 Record shape

```yaml
clue_id: NAR_CLUE_CLUE_APT_BLOOD_OLD
source_clue: CLUE_APT_BLOOD_OLD
public_name: "Preserved blood droplets"
class_tags: [PHYSICAL]           # internal; stripped before player delivery
granting_evt: EVT_113_APARTMENT_SEARCH
visibility: private | shared
owner: p1 | p2 | shared
card_text: |
  ...
record_sheet_line: "Preserved blood droplets — apartment bedroom"
```

### 4.4 Wording rules

| Rule | Requirement |
|---|---|
| Fact source | Physical details from `04_LOCATION_DATABASE.md` objective clues; testimonial content from **Reveals** and NPC disclosure stages |
| Class-appropriate tone | `PHYSICAL`: observable object/trace; `DIGITAL`: file/metadata; `TESTIMONIAL`: attributed statement; `PROCEDURAL`: log or record; `CONTEXTUAL`: background pressure; `BEHAVIOURAL`: observed contradiction |
| Public name | Short catalogue name for record sheet and condition tags; distinct from card body |
| No internal IDs | Never print `CLUE_*` to players (`08` § 7 allows recording ID on share — use public name in prose, numeric card index in layout) |
| Single clue, single grant | Idempotent; same card text for all routes that grant the same clue |

### 4.5 Ambiguity rules

Per `engine/02` § 2.3 and character records:

| Situation | Rule |
|---|---|
| Elias fragments | Must remain ambiguous without supporting clues (`03` NPC-01) |
| NPC beliefs | Label as belief or allegation, not fact |
| False neighbour "abductor" | Card must allow misinterpretation until staging conclusion is earned |
| Partial search failure | `Failure transformation` may produce partial card variant with fewer details |

Ambiguity is permitted when logic requires misinterpretation. It is forbidden when it would invent an alternative truth.

### 4.6 Information limits

The card conveys **only** the knowledge the clue represents — one point, one class assignment for threshold purposes.

Must not include:

- deduction conclusions ("This proves staging");
- unrelated suspect guilt;
- future route hints;
- other clues not granted in the same action.

### 4.7 Spoiler restrictions

| Rule | Requirement |
|---|---|
| Private clues | Issued only in the granting player's booklet section |
| Shared clues | Marked `visibility: shared`; issued at regroup or joint grant per logic |
| Cross-reference | Cards must not name clues the player does not hold |
| DEFINITION_ONLY | No card |

### 4.8 Sharing instruction

When a clue moves to `SHARED_KNOWLEDGE_SET` at `EVT_150` or `EVT_300`, the regroup scene includes explicit instruction per `08` § 7:

> Record `<public_name>` in the shared case file.

---

## 5. Conclusion generation

### 5.1 Principle

`CON_*` identifiers are **never player-visible** (`BOOK_COMPILER_SPEC.md` § 5.5). Players receive **diegetic discoveries** — moments where characters or the narrative acknowledge a deduction the engine has already validated.

### 5.2 Authoritative meaning source

| Source | Use |
|---|---|
| `12_CLUE_DEPENDENCY_GRAPH.md` deduction blocks | What the conclusion means; what it does **not** prove |
| `07_EVIDENCE_VALIDATION.md` § 2 | Threshold semantics |
| Regroup **Joint deductions** lists in `10` | Which conclusions may be articulated at `EVT_150` / `EVT_300` |

Example: `CON_LENA_PROTECTING` establishes "kidnapper is an incomplete model" — not legal innocence.

### 5.3 Reveal timing

| Trigger | Artifact |
|---|---|
| Regroup `EVT_150` / `EVT_300` | `NAR_DEDUCTION_*` optional sidebar or boxed "If you combine…" prompts listing discoverable deductions from **Joint deductions** |
| Node entry gated on conclusion | Scene prose reflects the conclusion as established fact without naming `CON_*` |
| NPC disclosure stage unlocked by evaluator | Dialogue in interview scene (`EVAL_NADIA_DISCLOSURE`, etc.) |
| Terminal or late confrontation | Outcome text assumes conclusions required by **Entry conditions** |

The generator must not issue a deduction prompt before the threshold in `07` § 2 is achievable from held clues listed in `12`.

### 5.4 Wording rules

| Rule | Requirement |
|---|---|
| Voice | In-world analytical ("The timing doesn't match an abduction") not mechanical ("Staged disappearance conclusion unlocked") |
| Negative space | State what is **not** proven when deduction block says so |
| No new evidence | Deduction text recombines existing clue public names only |
| Fair-play | Player must be able to trace each claim to a held clue public name |

### 5.5 Evidence consistency

Before emitting `NAR_DEDUCTION_{CON_ID}`, verify:

1. Every factual claim maps to at least one `CLUE_*` public name in the conclusion's group.
2. Wording does not contradict `01_WORLD_BIBLE.md`.
3. Wording does not exceed NPC knowledge if voiced by a character.
4. Structural gates (`CON_SIGNAL_4B`, `CON_WINDOW_CODE`) describe identifier-plus-route or fragment-plus-interpretation relationships without naming internal totals.

---

## 6. Ending generation

### 6.1 Scope

Generate epilogue narrative for eight terminal `EVT_*` nodes in `10` § 14, bound to `END_*` families in `14_ENDING_TRIGGER_MATRIX.md`.

`EVT_900_RESOLVE_ENDING` is an internal dispatch node. Players never read it. Generate endings only for terminal nodes `EVT_901`–`EVT_908`.

### 6.2 Structure

Each `NAR_END_*` record contains:

```yaml
ending_id: NAR_END_WITNESS_SPEAKS
source_evt: EVT_901_END_WITNESS_SPEAKS
ending_family: END_WITNESS_SPEAKS
terminal_type: VICTORY
framework_source: "06_ENDING_FRAMEWORK.md § END-01"
epilogue_prose: |
  ...
modifier_lines: []          # from 14 § 8 when applicable
rebuttal_category: null     # EVT_907 only
required_outcome_facts: []  # checklist derived from 06 Outcome bullets
forbidden_additions: []     # see § 6.4
```

### 6.3 Required information

Epilogue prose must reflect every **Outcome** bullet in the matching `06_ENDING_FRAMEWORK.md` section:

| END | Framework source | Mandatory themes |
|---|---|---|
| END-01 | § END-01 | Elias testifies; Vale resigns; Krell detained; Rook charged; Lena/Iris investigated with sympathy |
| END-02 | § END-02 | Conspiracy exposed; human cost; Nadia publishes index |
| END-03 | § END-03 | Elias survives; Vale/Krell deny; Rook may remain; delayed testimony hook |
| END-04 | § END-04 | Rook controls rescue; ledger lost; falsified custody; Mina may contact later |
| END-05 | § END-05 | Public outrage; incomplete evidence; Vale frames narrative; Elias endangered |
| END-06 | § END-06 | Elias dies; ledger fate varies; Lena/Iris blamed; retrospective understanding |
| END-07 | § END-07 | Wrong target absorbs attention; conspirators stabilize; contradictions summarized |
| END-08 | § END-08 | Divergent rescue/evidence outcomes; two-player conflict; not automatic punishment |

Apply **partial-success modifiers** from `14` § 8 as optional epilogue sentences when logic state supports them (Marcus confesses, Reed cooperates, etc.). Modifiers enrich; they do not replace the family outcome.

### 6.4 Forbidden additions

| Forbidden | Reason |
|---|---|
| New endings or family merges | Logic owns `14` priority |
| Reversing a terminal type | `TERMINAL_TYPE` is fixed in `10` |
| Villain behaviour contradicting World Bible | Immutable facts |
| Promising sequel hooks not in framework | Except END-03 and END-04 where explicitly allowed |
| Generic "case dismissed" for END-07 | `14` § 7 forbids |

### 6.5 Wrong-accusation ending (`EVT_907`)

Generate variant epilogues keyed by rebuttal category in `14` § 7:

| Category | Source facts |
|---|---|
| Wrong timeline | `07` § 3 + accusation target timeline |
| Missing physical presence | `07` § 3 per target |
| Cannot explain police manipulation | Marcus leak vs Rook proof distinction |
| Cannot explain financial architecture | Reed vs Krell/Vale scope |
| Protective vs initiating conduct | Lena/Nadia categories |
| Confession scope smaller than accusation | Partial admission cases |

Each variant must state which evidence link failed, per `07` § 3 and `06` END-07.

### 6.6 Two-player-only ending (`EVT_908`)

Epilogue must reflect incompatible player objectives per `06` END-08. Solo-mode narrative packages must exclude this record or mark it unreachable per `10` § 14 note.

---

## 7. Multiplayer writing

### 7.1 Delivery context

The generator produces narrative records. Packaging into one book or two booklets is a **compiler/formatter** decision (`BOOK_COMPILER_SPEC.md` MS-07). Narrative records must still declare `eligible_players` and `scene_mode` so any delivery model can be applied.

### 7.2 Scene mode derivation

Until logic files declare scene mode explicitly (`engine/05` § 3), the generator derives it deterministically:

| Node **Players** field | Derived `scene_mode` |
|---|---|
| `both` | `joint` |
| `Player 1` only (Player 2 inactive) | `split` |
| `Player 2` only (Player 1 inactive) | `split` |
| One player acts while other observes per node text | `solo` |

If node text explicitly assigns separate choices to each player in a joint location, use `joint` with per-player choice subsets in the narrative record.

**Caveat:** Derived scene mode is a generation convenience. Logic should eventually declare mode explicitly. Mismatch between derivation and future logic declaration is an engine/adventure issue.

### 7.3 Split paths

| Rule | Requirement |
|---|---|
| Isolation | Player 1 split text must not contain Player 2 private clues, and vice versa |
| Independence | Per `13` § 2 independence test — no split scene requires the other player's undiscovered clue |
| Useful outcome | Each split branch prose must deliver at least one **Reveals** fact or `GRANT_CLUE` from its node |
| Split terminator | Narrative record includes `split_terminator` metadata: `REJOIN`, `REMOTE_CONTACT`, `WAIT_UNTIL_SYNC`, `EMERGENCY_INTERRUPT`, or `TERMINAL_OUTCOME` per `engine/05` § 5 |

**Blocker:** Logic does not declare terminators per branch. Generator may default split scenes in the opening and midgame splits to `REJOIN` toward the next regroup node only when `13_SPLIT_AND_REGROUP_FLOW.md` names that regroup. All other terminators require logic specification (see § 12 AR-03).

### 7.4 Synchronization

| Element | Narrative handling |
|---|---|
| Shared world clock | Regroup and joint scenes include clock advancement from node **Cost** |
| Sync window | Opening prose may state approximate window from `13` ("complete one major scene each before 21:30") |
| Unused time | Do not invent extra actions; reference waiting/regroup per `05` § 4 |
| Real-time pressure | Optional; if referenced, disclose per `engine/02` § 2.11 |

### 7.5 Regroup events

`EVT_150_REGROUP_ONE` and `EVT_300_REGROUP_TWO` scenes must include:

1. Instruction to merge chosen private clues into shared case file (`08` § 7).
2. Optional `NAR_DEDUCTION_*` prompts for **Joint deductions** listed in the node.
3. **Branch choice** presentation for midgame tracks without adding routes.
4. Communication: all modes legal per `08` § 4 unless location forbids.

### 7.6 Shared vs independent information

| Knowledge state | Writing rule |
|---|---|
| Private clue just granted | Card in acting player's section only |
| After regroup share | Joint prose may reference public names recorded in shared case file |
| `SHARED_KNOWLEDGE_SET` grants | Joint scene text |
| NPC lies | Same lie rules as solo; both players hear the same lie in joint scenes |
| Asymmetric interview | Player-specific scene records for split interviews |

### 7.7 Ending evaluation (narrative side)

The generator does not evaluate endings. It authors eight terminal epilogues. Compiler selects which terminal page a playthrough receives.

Epilogues must be written so that no text assumes facts incompatible with the family's trigger conditions in `14`.

---

## 8. Narrative consistency

### 8.1 Global tone

From `01_WORLD_BIBLE.md` § 2 and `PROTOTYPE_BRIEF.md`:

| Attribute | Requirement |
|---|---|
| Genre | Realistic modern detective; no supernatural |
| Mood | Wet, windy coastal city; institutional pressure; economic division |
| Stakes | Personal and civic; corruption with human cost |
| Prose register | Clear, adult, genre-literate; not pulpy pastiche |
| Violence | Present but not gratuitous; medical harm factual per logic |

### 8.2 Vocabulary

| Rule | Requirement |
|---|---|
| Setting terms | Use World Bible institution names (Northstar Renewal, Greyhaven Ledger, etc.) |
| Engine terms | Never expose to players |
| Character names | Full name on first mention in a booklet section; consistent short forms thereafter |
| Class tags | Never expose `PHYSICAL`, `TESTIMONIAL`, etc. to players |

### 8.3 Tense consistency

Present tense for investigation; see § 2.5. Ending epilogues may shift to past tense for "weeks later" outcomes only when framework implies retrospective summary.

### 8.4 Character consistency

Before any NPC speaks, cross-check:

1. `03_CHARACTER_DATABASE.md` knowledge and beliefs.
2. `03_NPC_KNOWLEDGE_AND_DISCLOSURE.md` disclosure stage for current trust/evidence state.
3. Node **Reveals** and **State changes**.

NPCs must not disclose facts outside their stage. Lies must match character **lies** or pressure response records.

### 8.5 Location consistency

Cross-check `04_LOCATION_DATABASE.md` layout and `11_LOCATION_STATE_MACHINE.md` state. Do not describe rooms, items, or access inconsistent with the active state variant.

### 8.6 Timeline consistency

Cross-check `02_MASTER_TIMELINE.md`:

| Rule | Requirement |
|---|---|
| Playable opening | Friday 20:00 |
| Evidence deadline | Saturday 02:00 external reference |
| Fixed events | Cannot be contradicted |
| Node **Window** | Scene must not imply actions outside window without noting unavailability |

### 8.7 Fair-play alignment

Per `engine/01` § 1.5: every solution element must have been fairly obtainable. Generated text must not introduce retroactive facts that make fair-play review fail.

---

## 9. Information boundaries

### 9.1 Permitted invention (presentation only)

| Category | Examples | Constraint |
|---|---|---|
| Dialogue | Interview exchanges, Elias fragments | Within NPC knowledge and disclosure stage |
| Description | Weather, lighting, smells, architecture | Must not contradict `04` or World Bible |
| Atmosphere | Crowd noise, rain, institutional sterility | No new facts |
| Sensory detail | Fibre texture, screen glow | No new evidential meaning unless logic grants a clue |
| Transition prose | Walking between locations | Respect **Cost** time |
| Character mannerisms | Nadia's impatience, Mina's formality | From character **Public presentation** |
| Deduction framing | "Something doesn't fit" | Must map to existing clues when resolved |

### 9.2 Forbidden invention (gameplay)

| Category | Generator must not |
|---|---|
| New clues | Add `CLUE_*` or physical evidence |
| New mechanics | Invent checks, stats, or house rules |
| New routes | Add `Outgoing` targets or hidden pages |
| New deductions | Assert conclusions before threshold |
| New evidence | Objects, witnesses, documents not in logic or Bible |
| New timing | Deadlines, windows, durations not in logic |
| New gameplay consequences | Trust, awareness, state not in **State changes** |
| New endings | Families beyond `END_*` |
| New variables | Record-sheet fields not in mapping |
| Logic repair | Narrative that patches contradictory documents |

### 9.3 Public name mapping records

The generator authors `NAR_PUBLIC_*` records mapping internal identifiers to player-facing names for condition tags and record sheets:

```yaml
mapping_id: NAR_PUBLIC_CLUE_APT_BLOOD_OLD
internal_ref: CLUE_APT_BLOOD_OLD
public_name: "Preserved blood droplets"
public_description_short: "Small preserved blood droplets in the bedroom"
```

Mappings must not change what the clue **means** for thresholds.

### 9.4 Grey areas

| Situation | Rule |
|---|---|
| Logic says "two of" clues on success | Generate variants; do not pick which two in a single universal scene |
| Partial NPC disclosure | Dialogue shows withholding without stating hidden facts |
| Off-screen events `EVT_801`–`804` | May be referenced only after clock triggers make effects visible per `06_NPC_SCHEDULE` |
| Ambiguous fragments | Preserve ambiguity per character record |

---

## 10. Validation

### 10.1 Validation pipeline

```text
Narrative Record Package
        ↓
V-N1: Schema completeness
        ↓
V-N2: Logic fact preservation
        ↓
V-N3: Knowledge boundary compliance
        ↓
V-N4: Multiplayer isolation
        ↓
V-N5: Compiler bindability (BOOK_COMPILER_SPEC Stage 3 dry-run)
        ↓
PASS → handoff to compiler
FAIL → defect report
```

### 10.2 V-N1 — Schema completeness

Every `ACTIVE` playable `EVT_*` has a `NAR_EVT_*` record with all § 2.7 required fields.

Every authoritative `Outgoing` parent→target pair has a `NAR_CHOICE_*` label.

Every `ACTIVE` `CLUE_*` with a granting node has a `NAR_CLUE_*` card.

Every terminal `EVT_901`–`EVT_908` has a `NAR_END_*` epilogue.

Every public condition used has a `NAR_PUBLIC_*` mapping.

### 10.3 V-N2 — Logic fact preservation

For each scene, automated extraction compares:

| Logic field | Narrative obligation |
|---|---|
| **Reveals** | Each bullet has a matching factual statement in prose or linked clue |
| **GRANT_CLUE** | Matching `NAR_CLUE_*` referenced |
| **State changes** (visible) | Matching `visible_update_instructions` or diegetic depiction |
| **Failure transformation** | Variant exists with stated reduced outcome |
| **Entry conditions** | Variant exists or condition tag present |
| **Outgoing** | Choice count equals edge count |

No narrative sentence may assert a gameplay fact absent from logic, Bible, or authorized reference DB.

### 10.4 V-N3 — Knowledge boundary compliance

| Check | Rule |
|---|---|
| NPC dialogue | ⊆ disclosure stage facts for evaluated trust/evidence |
| Narrator | No hidden intent as sensory fact |
| Clue cards | ⊆ objective clue or testimonial source |
| Deductions | ⊆ recombination of held public clue names |
| Endings | ⊆ framework outcome bullets + authorized modifiers |

### 10.5 V-N4 — Multiplayer isolation

| Check | Rule |
|---|---|
| Split scenes | No cross-player private clue leakage |
| Joint scenes | Identical text for both players |
| Regroup | Sharing instructions present |
| `EVT_908` | Marked two-player-only |

### 10.6 V-N5 — Compiler bindability

Dry-run against `BOOK_COMPILER_SPEC.md`:

- Stage 3 can bind every `EVT_*` without invention.
- No MS-01–MS-03 class defects remain for generated artifacts.
- Halt if logic defects (missing `Outgoing`, missing `CHK_*`) remain in repository.

### 10.7 Defect classification

| Class | Action |
|---|---|
| `AUTHORING_DEFECT` | Generated text contradicts logic — fix narrative |
| `LOGIC_DEFECT` | Logic incomplete — halt; do not patch with prose |
| `REFERENCE_DEFECT` | Bible/DB contradicts logic — halt; escalate per `engine/02` § 2.16 |
| `ENGINE_GAP` | Engine requires field logic does not provide — document; halt |

---

## 11. Generator output

### 11.1 Narrative Record Package

The generator produces a versioned package for the compiler:

```yaml
package_id: the_last_witness_narrative
adventure_schema_version: "1.0"
generator_spec_version: "1.0"
engine_spec_version: "2.0"
play_modes: [two_player]
records:
  scenes: []           # NAR_EVT_*
  choices: []          # NAR_CHOICE_*
  clues: []            # NAR_CLUE_*
  deductions: []       # NAR_DEDUCTION_*
  endings: []          # NAR_END_*
  public_mappings: []  # NAR_PUBLIC_*
  checks: []           # NAR_CHK_* — empty until logic defines CHK_*
incomplete_nodes: []   # EVT_* blocked by logic gaps
validation_report: {}
```

### 11.2 Planned output location

Per `07_PROTOTYPE_BUILD_PLAN.md` Alpha 0.3 and `PLAYER/README.md`:

| Artifact | Planned path |
|---|---|
| Narrative record index | `PLAYER/narrative/` or equivalent Alpha 0.3 layer |
| Compiled books | `PLAYER/PLAYER_1_BOOK.md`, `PLAYER/PLAYER_2_BOOK.md` (Alpha 0.4 — compiler output, not generator output) |

The generator writes **records**, not finished booklets.

### 11.3 What the generator does not output

- Page numbers
- Typography or PDF layout
- Modified logic files
- Gameplay patches
- Facilitator scripts not in logic
- Record sheet layouts (Alpha 0.4 — see `BOOK_COMPILER_SPEC.md` MS-06)

---

## 12. Authoring Readiness Assessment

### NOT READY

The repository contains sufficient **reference material** (World Bible, character and location databases, detailed logic bullets) to constrain narrative generation. It does **not** yet contain sufficient **structural specification** for every artifact to be generated deterministically without gameplay inference or creative gap-filling that crosses into logic design.

Logic-layer facts are rich; graph completeness, check definitions, multiplayer engine fields on nodes, and formal narrative record schema remain incomplete. A generator following this specification must **halt** on blocked nodes rather than invent routes, checks, or terminators.

---

### Missing authoring requirements

#### AR-01 — Per-node `Outgoing` on eleven nodes

| Field | Detail |
|---|---|
| **Missing information** | Authoritative `**Outgoing**` list on: `EVT_115`, `EVT_123`, `EVT_150`, `EVT_212`, `EVT_223`, `EVT_232`, `EVT_243`, `EVT_300`, `EVT_314`, `EVT_331`, `EVT_440` |
| **Affected artifact** | `NAR_CHOICE_*` for those nodes; scene completeness |
| **Why deterministic authoring is impossible** | Choice labels require a parent→target pair from logic. Section hub menus do not uniquely assign edges from these nodes. Generator must not infer targets (`§ 2.12`, `§ 3.1`) |
| **Issue type** | Logic defect |

#### AR-02 — Check (`CHK_*`) definitions

| Field | Detail |
|---|---|
| **Missing information** | Skill, DC, pass/fail wording, fallback routes for branches referenced in **Failure transformation** (e.g. `EVT_115` perception check) |
| **Affected artifact** | `NAR_CHK_*`; failure variants of `NAR_EVT_*` |
| **Why deterministic authoring is impossible** | Engine expects D20 checks (`engine/01` § 1.2). Logic references checks in prose only. Generator cannot invent DC or mechanical outcomes |
| **Issue type** | Engine/adventure gap |

#### AR-03 — Split-branch terminator per scene

| Field | Detail |
|---|---|
| **Missing information** | Declared terminator (`REJOIN`, `REMOTE_CONTACT`, `WAIT_UNTIL_SYNC`, `EMERGENCY_INTERRUPT`, `TERMINAL_OUTCOME`) per split branch |
| **Affected artifact** | `split_terminator` metadata; split-scene closing instructions |
| **Why deterministic authoring is impossible** | `engine/05` § 5 requires explicit terminators. Derivation covers regroup-bound splits only partially (`§ 7.3`) |
| **Issue type** | Engine/adventure gap (deferred) |

#### AR-04 — Scene mode on logic nodes

| Field | Detail |
|---|---|
| **Missing information** | `Joint` / `Split` / `Solo` on each `EVT_*` in logic |
| **Affected artifact** | `scene_mode` field; booklet routing |
| **Why deterministic authoring is impossible** | Derivation rules in § 7.2 are a temporary convention. Edge cases (joint location, separate choices) are not fully specified in logic |
| **Issue type** | Engine/adventure gap |

#### AR-05 — Solo play mode graph

| Field | Detail |
|---|---|
| **Missing information** | Solo eligibility, route substitutions, `EVT_908` exclusion rules in logic |
| **Affected artifact** | Entire narrative package for solo mode |
| **Why deterministic authoring is impossible** | `engine/06` § 1 requires one-player mode. Logic is two-player-native. Generator cannot merge player paths without logic |
| **Issue type** | Engine/adventure gap |

#### AR-06 — Synchronization window maximum durations

| Field | Detail |
|---|---|
| **Missing information** | Per-window maximum duration (`engine/05` § 4); resolution of leftover-time conflict between `04_TIME_COST_MATRIX.md` and `engine/05` |
| **Affected artifact** | Split-scene timing instructions |
| **Why deterministic authoring is impossible** | Prose cannot state window limits not declared in logic or engine-owned adventure tables |
| **Issue type** | Documentation/engine gap (deferred) |

#### AR-07 — Multi-outcome clue grants without variant keys

| Field | Detail |
|---|---|
| **Missing information** | Explicit variant enumeration for nodes like `EVT_113` ("two of" clues; careful vs rushed) |
| **Affected artifact** | `NAR_EVT_*` variants; `NAR_CLUE_*` linkage |
| **Why deterministic authoring is impossible** | Without logic variant keys, generator must choose which clues appear in which variant — a gameplay decision |
| **Issue type** | Logic/documentation gap |

#### AR-08 — Formal narrative record schema

| Field | Detail |
|---|---|
| **Missing information** | Executable schema in `data_dictionary/` for `NAR_*` record types |
| **Affected artifact** | Package validation (V-N1) |
| **Why deterministic authoring is impossible** | Field names in this spec are normative here but not yet machine-registered in data dictionary |
| **Issue type** | Documentation gap (deferred) |

#### AR-09 — Public condition tag instance registry

| Field | Detail |
|---|---|
| **Missing information** | Adventure-specific list mapping each internal condition expression to public tag text |
| **Affected artifact** | `NAR_PUBLIC_*`; condition-gated `NAR_CHOICE_*` |
| **Why deterministic authoring is impossible** | Format is defined (`engine/04` § 4) but instances require authoring from variable/clue inventory — cannot be inferred without naming policy |
| **Issue type** | Authoring gap (planned Alpha 0.3) |

#### AR-10 — Two-player delivery model declaration

| Field | Detail |
|---|---|
| **Missing information** | Model A, B, or C selection (`engine/03` § 3.15) |
| **Affected artifact** | Player booklet partitioning; duplicate joint text handling |
| **Why deterministic authoring is impossible** | Same `NAR_EVT_*` records package differently per model; not a narrative wording issue but blocks final artifact assembly |
| **Issue type** | Documentation gap (planned Alpha 0.4) |

#### AR-11 — Record sheet and tracker field names

| Field | Detail |
|---|---|
| **Missing information** | Shared and private sheet layouts with fields matching `visible_update_instructions` and `record_sheet_line` entries |
| **Affected artifact** | Clue card `record_sheet_line`; trust and clock recording instructions |
| **Why deterministic authoring is impossible** | `engine/04` § 7 mandates fit on one shared plus one private sheet; field names are not declared |
| **Issue type** | Documentation gap (planned Alpha 0.4) |

#### AR-12 — Participation audit population

| Field | Detail |
|---|---|
| **Missing information** | Per-block decision counts, unique clues, challenge counts, waiting time, final-act responsibility (`08` § 9) |
| **Affected artifact** | Pre-generation gate; multiplayer balance validation |
| **Why deterministic authoring is impossible** | Generator cannot verify parity before authoring without populated audit fields |
| **Issue type** | Documentation gap |

#### AR-13 — Stale `END_*` identifier status in `14` § 9

| Field | Detail |
|---|---|
| **Missing information** | Correct `ACTIVE` status for seven `END_*` families referenced by terminal nodes |
| **Affected artifact** | `NAR_END_*` binding validation |
| **Why deterministic authoring is impossible** | Contradictory metadata breaks deterministic family→node binding unless generator applies undeclared override rules |
| **Issue type** | Documentation defect |

#### AR-14 — `DEFINITION_ONLY` clues (23 identifiers)

| Field | Detail |
|---|---|
| **Missing information** | Granting nodes for clues marked `DEFINITION_ONLY` in `12` |
| **Affected artifact** | `NAR_CLUE_*` for those identifiers |
| **Why deterministic authoring is impossible** | Not an authoring blocker for generation — generator correctly skips them. Becomes a **playability** gap if mandatory conclusions require those clues with no alternate route |
| **Issue type** | Logic completeness (monitor via `07` soft-lock audit; not a prose-generation halt) |

#### AR-15 — Wrong-accusation target enumeration at `EVT_440`

| Field | Detail |
|---|---|
| **Missing information** | Complete mapping from `EVT_440_FINAL_PUBLIC_POSITION` accusation options to `14` § 7 rebuttal categories per target |
| **Affected artifact** | `NAR_END_*` variants for `EVT_907`; confrontation scene choices |
| **Why deterministic authoring is impossible** | `07` § 3 lists per-target rebuttal facts; full accusation menu wiring in `10` for `EVT_440` lacks per-node `Outgoing` (AR-01) |
| **Issue type** | Logic defect |

---

### Readiness summary

| Layer | Status |
|---|---|
| Engine presentation rules | Complete for constraining generation |
| World Bible and reference DBs | Complete for fact-bound prose |
| Adventure logic (Alpha 0.2c) | Rich **Reveals** and grants; incomplete edges and checks |
| Narrative record schema | Specified here; not in data dictionary |
| Alpha 0.3 narrative layer | **Not started** |
| Multiplayer engine fields on nodes | **Missing** (AR-03, AR-04, AR-06) |
| Solo mode | **Not implemented** (AR-05) |

**Conclusion:** Authoring must be classified **NOT READY** until AR-01 through AR-13 are resolved for full-package generation. Partial generation may proceed for nodes with complete `Outgoing`, defined grants, and no check dependency, but the package cannot be marked complete for compiler handoff.

**Relationship to compilation:** Resolving `BOOK_COMPILER_SPEC.md` MS-01–MS-03 requires a complete Narrative Record Package from this specification. Resolving AR-01–AR-07 is prerequisite to producing that package without gameplay invention.

---

## Appendix A — Artifact inventory for The Last Witness

| Type | Count | Source |
|---|---:|---|
| Playable `EVT_*` scenes | 48 | `10` §§ 2–14 |
| Terminal endings | 8 | `10` § 14 |
| `ACTIVE` clues requiring cards | 43 | `12` (66 total − 23 `DEFINITION_ONLY`) |
| Conclusion deduction prompts | 14 active `CON_*` | `12` deduction blocks |
| Public name mappings | ≥ 43 clues + items + conditions | Derived from register |
| Choice labels | Σ \|Outgoing\| over nodes with authoritative edges | Incomplete until AR-01 fixed |

---

## Appendix B — Generator vs compiler responsibilities

| Task | Generator | Compiler |
|---|---|---|
| Write scene prose | Yes | No |
| Write choice labels | Yes | No |
| Write clue cards | Yes | No |
| Expand ending framework | Yes | No |
| Bind records to `EVT_*` | Yes | Yes |
| Evaluate conclusions | No | Yes (compile-time) |
| Merge variants | Produces variants | Yes |
| Strip internal IDs | Marks fields | Yes |
| Assign page numbers | No | No (formatter) |
| Modify logic | **Never** | **Never** |

---

## Appendix C — Document revision

| Version | Change |
|---|---|
| 1.0 | Initial content generation specification for The Last Witness |
