---
title: Architecture
version: 2.0-draft
status: Draft
depends_on:
  - 01_INTRODUCTION_AND_SCOPE.md
  - 02_DESIGN_PRINCIPLES.md
used_by:
  - ../data_dictionary/
  - ../templates/
  - ../adventures/
last_review:
reviewer:
---

# 3. Architecture

## 3.1 Architectural overview

IDNE uses a layered architecture.

```text
ENGINE SPECIFICATION
        ↓
DATA DICTIONARY
        ↓
WORLD BIBLE
        ↓
ADVENTURE LOGIC
        ↓
NARRATIVE COMPILER
        ↓
BOOK FORMATTER
        ↓
PLAYER OUTPUT
```

Each layer has one primary responsibility.

A lower layer MAY depend on an upper layer. An upper layer MUST NOT depend on adventure-specific data from a lower layer.

## 3.2 Engine Specification

The Engine Specification defines reusable rules, including terminology, world-state rules, time rules, knowledge rules, event rules, decision rules, check rules, two-player rules, compiler boundaries, formatting requirements, testing requirements, and release criteria.

The Engine Specification MUST NOT contain named suspects, adventure locations, case-specific clues, adventure endings, or story-specific timelines.

## 3.3 Data Dictionary

The Data Dictionary defines the formal structure of all records.

It MUST define field names, field meanings, required and optional fields, allowed values, references, validation rules, default values, and examples.

The Data Dictionary MUST NOT define the actual content of one adventure.

## 3.4 World Bible

The World Bible contains objective adventure truth.

It SHOULD contain the complete historical timeline, NPC identities, NPC goals, NPC knowledge, NPC beliefs, locations, items, evidence, factions, relationships, world variables, ending conditions, off-screen conflicts, and fixed causal chains.

The World Bible MUST remain independent of player-facing wording.

## 3.5 Adventure Logic

Adventure Logic defines playable structure.

It includes events, entry conditions, blocking conditions, choices, checks, consequences, time costs, state updates, knowledge updates, delayed effects, terminal states, synchronization points, and route references.

Adventure Logic MUST use stable internal IDs and MUST NOT use public event numbers as primary references.

## 3.6 Narrative Compiler

The Narrative Compiler converts developer logic into player-readable static nodes.

It is responsible for viewpoint filtering, sensory description, uncertainty preservation, information hiding, public condition wording, scene text, player-facing choice wording, and presenting permitted check information.

It MUST NOT change objective truth, invent consequences, remove required logic, expose raw internal state, assign final page numbers, or resolve broken graph structure.

## 3.7 Public Static Nodes

The Narrative Compiler output MUST consist of Public Static Nodes.

A Public Static Node is a printable player-facing unit with public node identity, narrative text, visible conditions, choices, check instructions, visible state updates, and outgoing public references.

Player-facing conditions MUST use only public markers, such as keywords, items, recorded conditions, resource amounts, character identity, and visible time values.

The compiler SHOULD limit conditional variation inside one node.

As a default:

- one node SHOULD contain no more than two major binary conditions;
- greater variation SHOULD be split into separate public nodes;
- trivial wording variation SHOULD be merged where meaning remains accurate.

## 3.8 Book Formatter

The Book Formatter transforms Public Static Nodes into final output.

It is responsible for public event numbering, randomized numbering if used, page references, page breaks, headings, tables, typography, booklet division, print layout, index generation, and reference validation.

The Book Formatter MUST NOT alter story logic, alter consequences, add new choices, change conditions, expose internal IDs, or silently merge semantically different nodes.

## 3.9 Player Output

Player Output includes all playable materials.

Possible outputs include a shared adventure book, Player 1 booklet, Player 2 booklet, character sheets, item cards, clue cards, keyword list, map, reference sheet, and optional digital companion.

Every output MUST declare whether it contains spoilers.

## 3.10 Review Layer

Reviews are not part of the playable engine flow.

Review documents MAY inspect every layer.

They SHOULD report issue ID, severity, affected records, defect description, reproduction path, suggested fix, side effects, and final resolution.

Reviews MUST NOT become hidden authoritative specifications. Accepted corrections MUST be incorporated into the responsible source document.

## 3.11 Changelog and versioning

Every approved change SHOULD be recorded.

A change record SHOULD include date, version, changed documents, reason, affected records, compatibility impact, and migration requirement.

Frozen documents MAY be changed only when a defect is confirmed, an accepted dependency changes, or a new version intentionally replaces the old rule.

## 3.12 Dependency direction

The following dependency direction is allowed:

```text
Engine → Data Dictionary → World Bible → Adventure Logic
→ Narrative Compiler → Book Formatter → Player Output
```

Reverse dependency is prohibited.

Examples:

- Engine rules cannot depend on The Last Witness.
- Data schemas cannot depend on one named NPC.
- World truth cannot depend on final page numbering.
- Adventure logic cannot depend on typography.
- Formatting cannot reinterpret hidden motives.

## 3.13 Single source of truth

Every authoritative fact MUST have one primary source.

Examples:

- record schema: Data Dictionary;
- actual NPC motive: World Bible;
- event trigger: Adventure Logic;
- player-visible wording: Narrative Compiler output;
- final page number: Book Formatter output.

Duplicated summaries MAY exist. A duplicated summary MUST NOT become independently authoritative.

## 3.14 Internal IDs and public references

Internal IDs MUST be stable, unique, machine-readable, survive renaming, and use defined prefixes.

Examples:

```text
NPC_001
LOC_004
ITEM_012
CLUE_008
EVT_047
DEC_103
CHK_022
END_005
```

Public event numbers MAY change between builds. Player-facing material MUST NOT expose internal IDs.

## 3.15 Two-player delivery architecture

A two-player adventure MUST choose one delivery model.

### Model A: Shared book

Suitable for mostly shared scenes. Private information MUST use cards, envelopes, separate marked sections, temporary separation, or another spoiler-safe method.

### Model B: Separate player booklets

Each player receives a separate narrative stream. Shared events MAY be duplicated. Synchronization points MUST be explicit.

### Model C: Shared book plus companion

A shared book contains common play. Private information is delivered through a small second booklet, digital companion, private cards, or QR-linked content.

The chosen model MUST be declared before adventure production.

## 3.16 Time architecture

The authoritative world time MUST be one explicit timestamp.

Six-hour slices MAY trigger background update groups. They MUST NOT create separate local player clocks.

When players split:

1. both branches begin from the same timestamp;
2. each action has a duration;
3. the branch defines its next synchronization point;
4. the shared world clock advances to the synchronization timestamp;
5. a player whose branch ends earlier receives only predefined waiting, travel, or short optional actions;
6. no player may continue indefinitely in an earlier world state after the other branch advances global time.

## 3.17 Off-screen event architecture

A narratively significant off-screen interaction MUST be represented as an event.

It MUST define participants, location, start time, objectives, knowledge, capabilities, resolution factors, state updates, knowledge updates, visible traces, and cancellation conditions.

The result MUST NOT be decided later for convenience.

## 3.18 Terminal architecture

Every playable node MUST declare either `NODE_TYPE = INTERMEDIATE` or `NODE_TYPE = TERMINAL`.

A terminal node MUST declare one terminal type.

Recommended terminal types:

- VICTORY;
- PARTIAL_SUCCESS;
- NARRATIVE_FAILURE;
- CHARACTER_DEATH;
- TIME_EXPIRED;
- CASE_UNRESOLVED;
- CAMPAIGN_CONTINUATION.

A node with no outgoing route and no terminal declaration is a structural defect.

## 3.19 Architecture validation checklist

The architecture passes review only if:

- every layer has a distinct responsibility;
- dependencies point in one direction;
- all authoritative facts have a source;
- internal IDs remain hidden from players;
- print output does not require raw state evaluation;
- two-player delivery has a selected model;
- time has one authoritative clock;
- significant off-screen interactions are predefined;
- terminal nodes are distinguishable from soft locks;
- review findings are incorporated into source documents.

## 3.20 Completion condition for this chapter

This chapter may be marked Approved when:

- all layer boundaries are accepted;
- Public Static Nodes are accepted as compiler output;
- the Book Formatter responsibility is unambiguous;
- the shared-time architecture is accepted;
- the two-player delivery models are accepted;
- terminal node classification is accepted.
