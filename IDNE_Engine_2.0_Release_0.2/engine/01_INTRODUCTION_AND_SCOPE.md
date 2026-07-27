---
title: Introduction and Scope
version: 2.0-draft
status: Draft
depends_on:
  - ../docs/STYLE_GUIDE.md
used_by:
  - 02_DESIGN_PRINCIPLES.md
  - 03_ARCHITECTURE.md
last_review:
reviewer:
---

# 1. Introduction and Scope

## 1.1 Purpose

The Interactive Detective Narrative Engine (IDNE) is a reusable specification for creating fair-play interactive detective gamebooks.

The engine is designed for adventures in which:

- the world continues independently of the players;
- objective truth is fixed;
- player knowledge is incomplete;
- NPC knowledge may be incomplete or incorrect;
- decisions create meaningful consequences;
- time affects opportunity;
- evidence can be missed, misunderstood, damaged, hidden, or recovered;
- two players may cooperate, separate, and exchange information;
- the final solution must be derivable from information that was fairly obtainable.

IDNE is not a single adventure, setting, or story. It is a reusable design and production system.

## 1.2 Primary use case

The primary use case is a realistic, print-oriented detective gamebook for one or two players.

The first reference implementation is expected to be a two-player modern detective adventure with:

- approximately 48 hours of in-world time;
- approximately two hours of real-world playtime;
- a D20-based resolution system;
- no supernatural mechanics;
- no hidden digital automation required for basic play.

Future implementations MAY use different settings, durations, character systems, or optional digital support.

## 1.3 Engine goals

IDNE MUST support:

1. logically consistent world state;
2. fair-play mystery construction;
3. meaningful branching;
4. traceable information flow;
5. deterministic objective reality;
6. controlled randomness;
7. explicit time advancement;
8. persistent consequences;
9. spoiler-safe player output;
10. structured testing;
11. reusable adventure production;
12. two-player cooperation without mandatory digital tools.

## 1.4 Non-goals

IDNE is not intended to:

- simulate every physical action in extreme detail;
- replace authorial creativity;
- generate stories without human review;
- guarantee that every player sees every clue;
- make every failed check harmless;
- support unlimited player freedom;
- function as a general-purpose tabletop RPG system;
- expose internal state variables to players;
- use hidden improvisation to repair broken logic during play.

## 1.5 Fair-play requirement

A mystery is fair only if the player could reasonably obtain enough information to reach the correct conclusion before the conclusion is revealed.

The engine MUST NOT:

- introduce decisive evidence only in the ending;
- retroactively change objective truth;
- declare an NPC guilty based on hidden author knowledge;
- punish players for failing to interpret information that was never presented;
- require real-world specialist knowledge unless the game teaches or provides it.

The engine MAY contain red herrings, unreliable witnesses, incomplete records, forged evidence, mistaken beliefs, inaccessible clues, costly clue routes, partial success, and bad endings. These remain fair only when they follow defined causes and do not require the narrator to lie.

## 1.6 Player-facing and developer-facing material

Player-facing material MAY contain narrative text, choices, public event numbers, visible items, visible resources, public keywords, character-sheet states, player instructions, checks, and consequences the player is allowed to know.

Player-facing material MUST NOT contain internal IDs, raw variables, objective truth not yet discovered, NPC private knowledge, hidden motives, developer notes, test tags, graph metadata, branch names, or unrevealed consequences.

Developer-facing material MAY contain full spoilers and internal structure. It MUST be clearly separated from player material.

## 1.7 Physical and digital compatibility

The base engine MUST remain playable in physical form.

Digital tools MAY improve private information delivery, timers, automated state tracking, randomized event numbering, accessibility, validation, and save-state management.

Digital support MUST NOT become mandatory unless the adventure is explicitly labelled as digitally assisted.

## 1.8 Single-player and two-player compatibility

The engine SHOULD support one-player and two-player adaptations.

A two-player adventure MUST define:

- whether both characters are always present;
- how split scenes work;
- how private information is delivered;
- how time is synchronized;
- how communication occurs;
- how long one player may remain inactive;
- how the adventure behaves if one character becomes unavailable.

## 1.9 Normative interpretation

The keywords MUST, MUST NOT, SHOULD, SHOULD NOT, MAY, OPTIONAL, and DEPRECATED have the meanings defined in the IDNE Documentation Style Guide.

When two rules conflict:

1. physical possibility has priority;
2. explicit adventure rules have priority over default engine recommendations only where the engine allows extension;
3. mandatory engine rules have priority over optional modules;
4. the more specific rule has priority over the general rule;
5. unresolved conflicts are specification defects and MUST be documented.

## 1.10 Completion condition for this chapter

This chapter may be marked Approved when:

- scope is unambiguous;
- the primary use case is accepted;
- non-goals are accepted;
- fair-play boundaries are accepted;
- physical print compatibility is accepted;
- no rule in this chapter conflicts with the architecture chapter.
