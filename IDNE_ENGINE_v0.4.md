---
title: IDNE Engine Specification
version: "0.4"
status: Draft
normative_philosophy: IDNE_DESIGN_PHILOSOPHY.md
supersedes: engine/ 2.0-draft chapters 00–06 (as global engine text)
last_review:
reviewer:
---

# IDNE Engine Specification — Version 0.4

This document is the **normative engine** for Version 0.4.

It replaces the global authority of Engine Specification 2.0 draft chapters for new work. Pre-0.4 adventures are **prototype-era** unless upgraded (see §16).

**Normative identity:** `IDNE_DESIGN_PHILOSOPHY.md` (Category A). Where this engine and that philosophy conflict, **philosophy wins** and this document must be corrected.

---

## 0. Identity

### 0.1 What IDNE is

IDNE is a reusable specification for **Dungeon Master–style fair-play detective simulation**.

The engine simulates a living mystery world: fixed truth, incomplete knowledge, advancing time, believable people, and player-directed investigation under scarcity.

Delivery may be print, digital, or hybrid. Delivery format is **not** the product identity.

### 0.2 What IDNE is not

IDNE is not primarily:

- a branching novel;
- a choose-your-own-adventure;
- a page-code tour;
- a general-purpose tabletop RPG;
- an improvisational storyteller that invents truth during play.

### 0.3 Primary use case (0.4)

- realistic modern detective fiction;
- no supernatural mechanics unless an adventure explicitly opts in and labels itself;
- one or two investigators depending on declared `play_modes` (see §0.5);
- two-player cooperative is the validated focus for 0.4 reference adventures;
- single-investigator mode is supported when explicitly declared and validated (see §6.8);
- physical play without mandatory digital tools;
- approximately one to three hours of **wall-clock** play for a short case (sizing is Category B).

### 0.4 Normative keywords

MUST, MUST NOT, SHOULD, SHOULD NOT, MAY, OPTIONAL, DEPRECATED have Style Guide meanings.

Conflict resolution order:

1. physical possibility;
2. Category A philosophy;
3. this engine specification;
4. adventure-allowed extensions where this engine permits;
5. more specific rule over general;
6. unresolved conflict is a specification defect.

### 0.5 Play modes

Every adventure MUST declare supported play modes in `play_manifest.json` at the adventure root.

| Mode ID | Meaning |
|---|---|
| `two_player` | Cooperative two-investigator play with split/regroup mechanics as defined in §6 |
| `single_investigator` | One investigator, one knowledge state, no split/regroup (§6.8) |

**MUST:** `play_modes` MUST list only modes the adventure actually supports.

**MUST NOT:** Infer solo playability from a two-player adventure. Removing Player 2 content without a full solo routing package is not valid `single_investigator` support.

**MAY:** Declare both modes only when the adventure provides complete, validated routing for each (`play_manifest.json` blocks `two_player` and `single_investigator`).

---

## 1. Immutable principles

These MUST NOT be violated by adventures, compilers, or validators.

| ID | Principle |
|---|---|
| U1 | Objective truth is fixed before play. Play does not rewrite history. |
| U2 | Knowledge is separate from truth. Players and NPCs may be wrong. |
| U3 | Fair play: the correct conclusion must be reachable from information obtainable in play. |
| U4 | The narrator MUST NOT lie about objective sensory facts. NPCs and documents MAY lie. |
| U5 | The world MAY continue while players are elsewhere. |
| U6 | Every meaningful state change requires a traceable cause. |
| U7 | Failure changes the path; it MUST NOT silently erase the only fair solution unless a fair failure ending was an intentional, visible risk. |
| U8 | Innocent people MAY behave suspiciously. Believable behaviour outweighs dramatic convenience. |
| U9 | Major suspects MUST receive equal narrative weight in presentation. Tone MUST NOT telegraph guilt. |
| U10 | The engine and player text MUST NOT coach the “correct” move. |
| U11 | Long-term identity is DM simulation, not branching novel. |
| U12 | Authoritative facts have one owning layer (see §3). |

---

## 2. Fair play and mystery construction

### 2.1 Fair mystery

A mystery is fair only if players could reasonably obtain enough information to justify the correct conclusion before that conclusion is revealed as ending text.

The engine MUST NOT:

- introduce decisive proof only in an ending;
- retroactively change objective truth;
- declare guilt from hidden author knowledge;
- punish players for failing to use information never presented;
- require specialist real-world knowledge unless taught or provided in play.

Red herrings, lies, forgeries, missing clues, costly routes, partial success, and bad endings remain fair when they have defined causes.

### 2.2 Discovery and connection

Observations MAY be revealed by successful investigation.

Conclusions MUST primarily be **player-reconstructed**.

Adventures MUST NOT routinely auto-deliver case conclusions or “you realize X is guilty” narration without prior obtainable evidence that supports that synthesis.

Clue acquisition modes (legacy delivery taxonomy; **compatibility only** when Investigation Core is declared):

| Mode | Meaning |
|---|---|
| Observe | Sensory/detail found by being present and looking |
| Earn | Found through check, cost, leverage, or risk |
| Infer | Requires combining two or more held facts (player synthesis) |
| Auto | Granted merely by entering a scene |

When `investigation_method: canonical` is declared (`INVESTIGATION_CORE_SPEC.md`), **Knowledge IDs** and **Proof** records are the primary investigation drivers. Legacy `CLUE-*` IDs MUST map through `compatibility_clue_map` only.

**MUST:** Final case conclusion MUST require at least one **Infer** step somewhere on a fair path (at regroup, accusation prep, or equivalent), not only Auto grants.

**SHOULD:** Prefer Observe/Earn over Auto for major clues.

### 2.3 Clue redundancy

- Final case conclusions MUST have at least two independent supporting routes.
- Major intermediate deductions SHOULD have a primary route and a fallback.
- Local or optional information MAY have one fair route.

Critical facts MUST NOT be permanently lost through an uninformed choice without alternative route, recovery, substitute, degraded solvable outcome, or explicit intentional failure ending.

### 2.4 Suspect presentation

Major suspects MUST feel equally believable at introduction.

Player-facing introductions MUST NOT use asymmetric emphasis, unique “villain diction,” or spotlight stage business that leaks narrative importance.

Suspicious innocents are valid and encouraged when psychologically credible.

---

## 3. Architecture

### 3.1 Layers

```text
ENGINE SPECIFICATION (this document + Design Philosophy)
        ↓
DATA DICTIONARY (schemas)
        ↓
WORLD TRUTH PACKAGE (World-First Generation — Milestone 2)
        ↓
ENVIRONMENT PACKAGE (Environment System — Milestone 3)
        ↓
OBJECT INTERACTION PACKAGE (Object Interaction — Milestone 4)
        ↓
CAPABILITY CHECK PACKAGE (Capability Check System — Milestone 6)
        ↓
INVESTIGATION CORE PACKAGE (Investigation Core — Milestone 5A)
        ↓
NPC INVESTIGATION PACKAGE (NPC Investigation — Milestone 5B)
        ↓
INVESTIGATION FLOW PACKAGE (Investigation Flow & Endings — Milestone 5C)
        ↓
WORLD BIBLE (objective adventure truth — human-readable summary)
        ↓
ADVENTURE LOGIC (playable simulation structure)
        ↓
DELIVERY ADAPTER (Narrative Compiler + Book Formatter)
        ↓
PLAYER OUTPUT
```

For adventures using World-First Generation (`WORLD_FIRST_GENERATION_SPEC.md`), the **World Truth Package** is the machine-authoritative source. World Bible prose MUST NOT contradict the package.

Lower layers MUST NOT redefine facts owned by higher layers.

### 3.2 Layer responsibilities

| Layer | Owns | MUST NOT |
|---|---|---|
| Engine | Reusable rules, readiness, identity | Adventure plot facts |
| Data Dictionary | Record shapes | Adventure content |
| World Truth Package | Fixed truth, timeline, NPC knowledge, evidence provenance (machine) | Player wording |
| Environment Package | Locations, states, features, navigation, revisit rules (machine) | Inventing location state at delivery |
| Object Interaction Package | Objects, actions, check bindings, result units (machine) | Creating evidence via checks; clue grants in scenes |
| Capability Check Package | Check definitions, DC, destinations, fixed-world invariants (machine) | Changing Fixed Truth, document contents, or evidence existence |
| Investigation Core Package | Knowledge, proof, conclusions, relationships (machine) | Legacy clue-ID-driven investigation |
| NPC Investigation Package | NPC static/dynamic state, trust, topics, conversation routes (machine) | Redefining Investigation Core knowledge or proof |
| Investigation Flow Package | State-driven flow, scene chains, ending graph, accusation eval (machine) | Redefining Investigation Core proof or NPC conversation models |
| World Bible | What actually happened; NPC knowledge/beliefs; fixed timeline (human summary) | Player wording |
| Adventure Logic | Actions, conditions, costs, state updates, knowledge grants, endings triggers | Public page numbers as primary IDs |
| Delivery Adapter | Viewpoint filtering, player wording, public conditions, layout | Invent consequences; change truth; expose internal IDs |
| Player Output | Playable artifacts | Spoilers unmarked |

### 3.3 Delivery Adapter (formerly “Narrative Compiler as product center”)

**Change (C-07 / Philosophy A6):** The compiler and formatter are a **Delivery Adapter**. They translate simulated world actions into playable artifacts. They do **not** define investigation shape.

Investigation shape is owned by World Truth Package (when World-First) + World Bible + Adventure Logic under player-directed scarcity (§5, §7).

Printable Public Static Nodes remain a **valid delivery form**, not the identity of IDNE.

### 3.4 Single source of truth

Every authoritative fact MUST have one owner. Summaries MAY exist and MUST be marked non-authoritative.

### 3.5 Internal IDs

Internal IDs MUST be stable and hidden from players.

Public navigation labels (page numbers, scene codes) MAY exist for delivery. They are Category B packaging.

Player-facing **choices** MUST NOT be written as “choose page code X vs Y” (§7).

---

## 4. World state and knowledge

### 4.1 State model

Adventure Logic MUST maintain:

- objective world state;
- per-character knowledge and beliefs;
- shared party knowledge when applicable;
- item and location states;
- clocks and declared thresholds;
- ending-relevant flags derived from evaluators or explicit records.

### 4.2 Causes

Every meaningful transition MUST cite a cause (action, clock trigger, off-screen event, or evaluator).

Uncaused changes are defects.

### 4.3 Player-visible mechanics (C-06, M-02)

**MUST:** Any condition referenced in player-facing text MUST be checkable from:

- the shared record sheet;
- a private knowledge sheet;
- a public condition tag derived from those.

**MUST NOT:** Player text may not say “if they trust you,” “if nervousness is low,” or similar unless the sheet defines how that state is recorded and changed.

Hidden internal variables MAY exist for simulation. They MUST remain invisible at play-time unless compiled into public tags/sheet fields.

### 4.4 Record sheet budget

Playable state SHOULD fit on:

- one shared case/record sheet;
- one private knowledge sheet per player.

Mechanics that exceed this MUST be simplified, compiled away, or deferred.

### 4.5 Complexity control

Tracked variables SHOULD affect play. Unused variables SHOULD be removed.

---

## 5. Time and scarcity

### 5.1 One world clock

There is exactly one authoritative world clock.

Parallel player activity does **not** create independent world timelines.

### 5.2 Scarcity as primary decision engine (Philosophy A7, M-03)

Meaningful decisions SHOULD arise from **many possible actions and insufficient time (or other scarce resources)** more often than from artificial binary forks.

Declared clock thresholds MUST change at least one player-visible option, access, risk, or cost when they fire (“time with teeth”).

Thresholds that appear only as flavour text are defects.

### 5.3 Advancing time

Adventures MUST define how completed actions advance the shared clock.

For parallel split activity in Version 0.4:

```text
At synchronization, WORLD_TIME advances by max(role_A_elapsed, role_B_elapsed)
  relative to the window start, plus any declared sync costs.
```

Adventures MUST NOT invent player-facing clock values that are not declared thresholds.

### 5.4 Wall-clock playtime estimate (C-05)

Estimated real cooperative playtime MUST be computed as:

```text
estimated_wall_clock =
    sum(joint_scene_play_estimates)
  + sum_over_split_windows( max(role_A_estimate, role_B_estimate) )
  + endgame_estimate
```

Reports MUST also state **longest individual branch** separately.

**MUST NOT:** estimate session length by summing both players’ full path times.

Applies when `play_modes` includes `two_player`.

### 5.4.1 Wall-clock estimate — single investigator

When `play_modes` includes `single_investigator`:

```text
estimated_wall_clock =
    sum(sequential_scene_play_estimates_along_legal_paths)
  + endgame_estimate
```

**MUST NOT:** use the cooperative split-window `max(role_A, role_B)` formula for solo adventures.

Reports MUST state **longest legal path** separately.

### 5.5 Optional real-time pressure

Real-time (wall-clock) pressure is OPTIONAL and MUST be disableable without making the adventure unplayable.

---

## 6. Two-player cooperation

### 6.1 Equality

Both characters MUST remain meaningful protagonists. Different roles are encouraged; unequal importance is not.

### 6.2 Scene modes

Every playable unit MUST declare:

- **Joint** — both present; shared content;
- **Split** — separate content; private knowledge isolated; ends at sync;
- **Solo** — OPTIONAL; one acts, the other inactive only as the scene permits.

Version 0.4 reference adventures MAY defer Solo.

### 6.3 Shared investigation target (M-01)

For two-player cooperative adventures:

**SHOULD:** At least **40%** of clue-granting playable units are Joint (shared investigation), measured by unit count or by declared adventure metric documented in the brief.

**MUST NOT:** Design the case as two nearly complete solo adventures that only meet to swap notes.

Split exists to create perspective and reunite synthesis (Philosophy A9, A15).

### 6.4 Split balance (M-04)

For each split window, estimated wall-clock engagement per role SHOULD differ by **no more than 5 minutes**.

If one role finishes early, that player MAY only take predefined wait / short prep / legal communication actions. Idle waiting without such options is a pacing defect when the delta exceeds the balance target.

### 6.5 Knowledge isolation

Private knowledge stays private until regroup, successful communication, or an explicit share rule.

### 6.6 Communication

While split, communication is an action with cost and limits defined by the adventure.

### 6.7 Sync terminators

Every split branch MUST end in a defined sync outcome (rejoin, remote contact, wait-until-sync, emergency interrupt, or terminal). Free asynchronous drift is forbidden.

Applies only when `play_modes` includes `two_player`.

### 6.8 Single Investigator Mode

When `play_modes` includes `single_investigator`, the adventure MUST implement the following. This is **not** a two-player adventure with one booklet removed.

| Requirement | Rule |
|---|---|
| Investigator count | Exactly one player character |
| Knowledge state | One investigator knowledge state; no private role booklets |
| Inventory | One inventory owned by the investigator |
| World clock | One shared world clock (§5.1); sequential action costing only |
| Split / regroup | **MUST NOT** use split windows, regroup scenes, parallel role paths, or wait-for-partner mechanics |
| Navigation | Player-directed investigation among authored locations (Philosophy A5) |
| Scarcity | Time and other declared scarce resources are primary limits (Philosophy A7) |
| Checks | Same fixed-world check principle (§7); one investigator performs all checks |
| Conclusions | Infer and ending evaluation use one investigator sheet |
| Playtime | Wall-clock estimate uses §5.4.1 formula |

**MUST NOT:** Require information, items, or conclusions only obtainable by an absent second role.

**MUST:** Pass mandatory Single Investigator validation (`IDNE_ADVENTURE_QA_SPEC.md` §5.11; `SINGLE_INVESTIGATOR_MODE_SPEC.md`).

---

## 7. Actions, decisions, and checks

### 7.1 Player-directed investigation (Philosophy A5)

Player materials MUST present **available investigative actions** (“talk to…”, “search…”, “request…”), not tour itineraries (“go to S-210”).

Navigation codes MAY appear as destinations after an action label. They MUST NOT be the choice itself.

### 7.2 Decision isolation (C-03)

A decision unit MUST list only:

- diegetic action labels;
- destinations (or public references);
- optional public condition tags.

A decision unit MUST NOT explain consequences of those actions in the same unit.

Consequences MUST appear only in destination units (or later units reached thereby).

### 7.3 No steering (C-04, Philosophy A10)

Player-facing text MUST NOT mark choices as recommended, preferred, optimal, suggested, or “best.”

In-world pressure (NPC urging, deadline threat) is allowed. Meta coaching is not.

### 7.4 Meaningful decisions

Choices that produce the same result at the same cost are not meaningfully distinct and MUST NOT be presented as alternatives unless the lack of control is intentional and visible.

### 7.5 Checks

Checks are OPTIONAL Category B resolution tools.

When used:

- procedure MUST be player-visible;
- failure SHOULD change path/cost/certainty;
- failure MUST NOT silently remove the only fair route to a required conclusion (unless intentional fair failure ending).

Version 0.4 does not mandate D20 specifically.

---

## 8. Endings

### 8.1 Terminal units

Every playable unit is Intermediate or Terminal.

Terminals MUST declare a terminal type (e.g. victory, partial success, narrative failure, time expired, case unresolved).

### 8.2 Ending logic ownership

Ending **trigger conditions** are owned by Adventure Logic.

Ending **player wording** is owned by the Delivery Adapter / Player Output.

### 8.3 Ending communication (M-07)

Player-facing ending resolution MUST:

- use only sheet-checkable conditions / public tags;
- follow a declared priority order when multiple endings could apply;
- make the link between play and outcome intelligible (cite which recorded conditions selected the ending).

Players MUST NOT be asked to judge hidden correctness (“were you right?”) without a sheet mapping.

### 8.4 Reachability

Every declared ending MUST be reachable on at least one legal path.

---

## 9. Off-screen world

Narratively significant off-screen conflicts MUST be predefined events (participants, timing, objectives, resolution factors, outcomes, visible traces).

Results MUST NOT be invented later for convenience.

---

## 10. Delivery Adapter rules

### 10.1 Compile-time vs play-time

**Compile-time:** validate references; bind player wording; emit public units; strip internal IDs; verify redundancy and terminals.

**Play-time:** players read public units, choose actions, record exposed updates, advance clock as instructed, resolve declared checks, follow destinations.

Players MUST NEVER evaluate raw internal variables or simulate hidden off-screen logic manually.

### 10.2 Public condition tags

Tags MUST reference only sheet-visible information and MUST provide a false-path alternative when needed.

### 10.3 Variant control

Emit separate public variants only for material player-facing differences. Merge identical outcomes.

### 10.4 Language

Player prose SHOULD be clear and accessible.

Technical terms MUST be explained in plain language on first use when required for play.

Prose MUST NOT expose graph metadata, branch names, or internal IDs.

---

## 11. Two-player delivery models

Adventures MUST declare one model:

- **A** Shared book + private cards/sections;
- **B** Separate player booklets;
- **C** Shared book + companion.

Private split content MUST remain spoiler-safe.

### 10.5 Play manifest (Delivery Adapter)

The Delivery Adapter MUST emit or preserve `play_manifest.json` declaring:

- `play_modes[]`
- `two_player` routing artifacts when applicable (joint scenes, role booklets)
- `single_investigator` routing artifacts when applicable (§6.8; `SINGLE_INVESTIGATOR_MODE_SPEC.md`)

Compilers MUST NOT emit `single_investigator` in `play_modes` unless solo validation prerequisites are satisfied.

---

## 12. Authoring separation

Authors define truth, logic, conditions, and consequences.

The Delivery Adapter defines perception wording and public presentation.

The formatter defines layout and public numbering.

No layer may silently perform another’s job. Narrative rewriting MUST NOT conceal unresolved logic defects.

---

## 13. Readiness and validation (C-02)

### 13.1 Hygiene checks (necessary, not sufficient)

Identifier resolution, graph reachability, terminal completeness, clue redundancy, single-source ownership, and sheet fit remain required hygiene.

### 13.2 Experience gates (required for 0.4 Ready)

An adventure is **not Ready** for playtest release unless:

| Gate | Requirement |
|---|---|
| Wall-clock estimate | Uses §5.4 for `two_player`, §5.4.1 for `single_investigator`; longest branch reported separately |
| Shared investigation | Meets §6.3 target or documents an approved waiver |
| Split balance | Meets §6.4 or documents waiver with mitigation |
| Decision isolation | No consequence spoilers on decision units |
| No steering | No recommended/preferred choice language |
| Visible mechanics | No undefined player conditionals |
| Time teeth | Every declared threshold gates a visible option |
| Discovery | Final conclusion path includes Infer step (§2.2) |
| Ending clarity | Ending selection is sheet-checkable (§8.3) |
| Suspect weight | Introductions pass equal-weight review (§2.4) |
| Human playtest | Recorded session against these gates exists |

Structural file inventory alone MUST NOT produce PASS / Ready.

### 13.3 Playtest classification

Post-playtest issues classify as content, adventure logic, engine rule, delivery adapter, formatter, or usability defects. Only justified engine defects expand this specification.

---

## 14. Deferred beyond 0.4

- Full digital DM runtime;
- Full JSON Schema + CI automation for all layers;
- Multi-case campaigns;
- Competitive / traitor modes;
- Commercial print optimization;
- Playtime Calibration, Investigation Validator, Story Validator (later milestones);

**Milestone 1 (Single Investigator Mode):** normative rules and validation are defined in v0.4 via `SINGLE_INVESTIGATOR_MODE_SPEC.md` and §6.8. Reference solo adventures are not required for 0.4 closure.

**Milestone 2 (World-First Generation):** normative generation order, schema, and validation are defined via `WORLD_FIRST_GENERATION_SPEC.md` and `generation_manifest.json`. Reference World-First adventures are not required for closure.

**Milestone 3 (Environment System):** normative location model, schema, and validation are defined via `ENVIRONMENT_SYSTEM_SPEC.md` and `environment_manifest.json`. Reference environment adventures are not required for closure.

**Milestone 4 (Object Interaction System):** normative object model, schema, and validation are defined via `OBJECT_INTERACTION_SYSTEM_SPEC.md` and `object_interaction_manifest.json`. Reference object-interaction adventures are not required for closure.

**Milestone 5A (Investigation Core):** normative investigation data model replacing clue-driven logic; see `INVESTIGATION_CORE_SPEC.md` and `investigation_manifest.json`.

**Milestone 5B (NPC Investigation System):** normative NPC graph, conversation graph, trust model, InformationKnown, topic unlocking, and relationship reactions; see `NPC_INVESTIGATION_SYSTEM_SPEC.md` and `npc_investigation_manifest.json`.

**Milestone 5C (Investigation Flow & Ending System):** normative state-driven investigation flow and ending architecture; see `INVESTIGATION_FLOW_SPEC.md`, `ENDING_SYSTEM_SPEC.md`, and `investigation_flow_manifest.json`.

**Milestone 6 (Capability Check System):** normative capability-check model with fixed-world invariants; see `CAPABILITY_CHECK_SYSTEM_SPEC.md` and `capability_check_manifest.json`.

**Milestone 7 (Investigation Validator):** integrated end-to-end investigability validator; see `INVESTIGATION_VALIDATOR_SPEC.md` and `investigation_validator_manifest.json`.

**Milestone 8 (Story Validator):** story understandability and coherence validator; see `STORY_VALIDATOR_SPEC.md` and `story_validator_manifest.json`.

**Milestone 9 (Playtime Calibration):** canonical wall-clock playtime estimation and validation; see `PLAYTIME_CALIBRATION_SPEC.md` and `playtime_calibration_manifest.json`.

---

## 15. Complexity budget (guidance, not identity)

Short-case guidance (Category B sizing):

- ~2 investigators;
- 3–5 major suspects;
- 4–7 primary locations;
- 12–20 meaningful clues;
- ≤3 split windows unless scarcity model replaces windowing;
- 3–6 terminal outcomes;
- public tracked fields kept within sheet budget.

---

## 16. Compatibility

| Era | Status under 0.4 |
|---|---|
| Adventures authored to Engine 2.0 / Alpha 0.2c | **Prototype-era** — may remain for history; MUST NOT claim 0.4 Ready without upgrade |
| New adventures | MUST follow this specification |
| Companion docs (`BOOK_COMPILER_SPEC`, etc.) | Valid only where they do not contradict this document; Delivery Adapter role supersedes compiler-as-identity language |

---

## 17. Creed (normative summary)

1. Simulate a world; do not author a tour.  
2. Players investigate; the book does not investigate for them.  
3. Evidence is found and connected; conclusions are earned.  
4. Every suspect can be believed; tone never winks.  
5. Innocent people may look guilty; that is realism.  
6. Behaviour stays believable even when plot wants drama.  
7. Time and scarcity create decisions; menus are last resorts.  
8. Partners share a case; splits create perspective, not isolation.  
9. Never coach the “right” move.  
10. If it only works as a branching novel, it is not yet IDNE.

---

*End of IDNE Engine Specification Version 0.4 (first draft).*
