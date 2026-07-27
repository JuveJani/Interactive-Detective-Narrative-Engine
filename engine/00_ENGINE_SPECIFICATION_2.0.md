---
title: Engine Specification 2.0
version: 2.0-draft
status: Draft
depends_on:
  - ../docs/STYLE_GUIDE.md
used_by:
  - ../data_dictionary/
  - ../templates/
  - ../adventures/
last_review:
reviewer:
---

# Engine Specification 2.0

## 1. Purpose

IDNE is a reusable framework for creating fair-play interactive detective gamebooks with persistent world state, meaningful decisions, traceable information, and support for two-player play.

## 2. Scope

The engine defines:

- objective world state;
- player and NPC knowledge;
- event and decision logic;
- time advancement;
- checks and consequences;
- two-player synchronization;
- narrative compilation;
- print-oriented formatting;
- testing and release standards.

The engine MUST NOT contain adventure-specific plot facts.

## 3. Current design decisions

### 3.1 Shared world time

The game MUST maintain one authoritative world clock.

Parallel player branches MAY contain different activities, but they MUST begin from a shared timestamp and MUST rejoin at a defined synchronization point.

Six-hour periods MAY be used as background-world update milestones, but they MUST NOT replace the authoritative timestamp.

### 3.2 Real-time pressure

Real-time pressure is OPTIONAL.

A player group that disables real-time play MUST ignore expiry consequences based only on real elapsed time.

Real-time events MAY be announced before they begin.

A real-time event MAY also be revealed only after the decision, provided that:

- the general existence of optional hidden real-time mechanics is disclosed in the rulebook;
- disabling real-time play prevents the expiry consequence from activating;
- ordinary interruptions, accessibility needs, reading speed, or rules consultation cannot create an unavoidable penalty;
- the event remains playable without real-time enforcement.

### 3.3 Separate player information

Character knowledge MUST be tracked separately while characters are physically separated.

An adventure MUST define how private information is delivered. Supported methods MAY include:

- separate player booklets;
- private cards or envelopes;
- short alternating split scenes;
- digital companion material.

### 3.4 Printable conditional text

The Narrative Compiler MUST output static, printable public nodes.

Player-facing conditions MUST refer only to visible inventory items, keywords, resources, or character-sheet states.

Raw world variables and internal IDs MUST NOT appear in player-facing conditions.

### 3.5 Progression

Short, time-critical standalone adventures SHOULD disable permanent skill training during the case.

Persistent development SHOULD occur between adventures or in a campaign module.

### 3.6 Clue redundancy

Clue redundancy depends on importance:

- final case conclusions MUST have at least two independent supporting routes;
- major intermediate deductions SHOULD have one primary and one fallback route;
- local or optional information MAY have one fair route.

### 3.7 Off-screen NPC conflicts

A significant off-screen conflict MUST be represented as a defined event with participants, objectives, timing, resolution factors, and outcome.

A generic initiative number alone MUST NOT determine narratively significant conflicts.

### 3.8 Terminal nodes

Every node MUST be identified as either intermediate or terminal.

A terminal node MUST declare a terminal type.

A non-terminal node without a valid outgoing route is a structural defect.

## 4. Development status

This file is the initial consolidated foundation. Remaining chapters will expand these rules without contradicting them.
