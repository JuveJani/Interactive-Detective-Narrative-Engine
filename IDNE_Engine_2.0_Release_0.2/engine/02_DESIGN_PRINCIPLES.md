---
title: Design Principles
version: 2.0-draft
status: Draft
depends_on:
  - 01_INTRODUCTION_AND_SCOPE.md
used_by:
  - 03_ARCHITECTURE.md
  - 04_WORLD_AND_STATE_MODEL.md
  - 05_TIME_SYSTEM.md
last_review:
reviewer:
---

# 2. Design Principles

## 2.1 Objective truth is fixed

Every adventure MUST define what actually happened before narrative compilation.

Objective truth MUST NOT change because a player missed a clue, a check failed, the author prefers a later branch, a random roll would create a more dramatic result, or a player formed a different theory.

Randomness MAY affect whether information is discovered, interpreted, preserved, or acted upon. Randomness MUST NOT alter the historical truth of the case.

## 2.2 Knowledge is separate from truth

The engine MUST track separately objective truth, each NPC's knowledge, each NPC's beliefs, each player character's knowledge, and shared party knowledge where applicable.

A person MAY know a true fact, believe a false fact, suspect a true fact without knowing it, deliberately lie, correctly observe an event but misunderstand it, or remember inaccurately.

The system MUST record the source of important knowledge.

## 2.3 The narrator does not lie

NPCs MAY lie. Documents MAY be forged. Evidence MAY be manipulated.

The narrator MUST NOT present a false interpretation as an objective sensory fact.

The narrator MAY use limited perspective.

Acceptable example:

> He looks at the door twice before answering.

Unacceptable example:

> He looks at the door because he plans to escape.

The second sentence exposes hidden intent.

## 2.4 The world continues independently

NPCs, factions, locations, and evidence MAY change while the players are elsewhere.

World progression MUST follow time, defined triggers, known motivations, physical possibility, available resources, and information available to the acting entity.

The world MUST NOT wait indefinitely for player arrival unless a reason exists.

## 2.5 Every meaningful change requires a cause

Every state transition MUST have a traceable cause.

Examples:

- an item moves because a person moves it;
- an NPC learns a fact because a source communicates it;
- a door becomes locked because someone locks it;
- public panic rises because an event becomes known;
- evidence is destroyed because a defined action succeeds.

Uncaused state changes are defects.

## 2.6 Decisions must be meaningful

A player choice SHOULD differ in at least one of these dimensions: time, risk, information, resources, morality, trust, relationship, legal exposure, physical danger, or future opportunity.

Two choices that produce the same result with the same cost are not meaningfully distinct.

False choices MAY be used only when the lack of real control is itself narratively intentional and visible.

## 2.7 Failure changes the path

Failure SHOULD usually create a consequence rather than a dead end.

Valid failure consequences include time loss, injury, damaged evidence, suspicion, lost trust, reduced options, increased cost, incomplete information, forced route change, partial success, and narrative failure endings.

A failed check MUST NOT silently remove the only possible route to the solution unless the adventure intentionally allows a fair failure ending.

## 2.8 Complexity must justify itself

Every tracked variable, state, branch, and rule SHOULD create meaningful gameplay value.

The engine SHOULD avoid variables that never affect a choice, states that only rename the same condition, branches that immediately rejoin without meaningful difference, redundant numerical precision, simulation detail the player cannot perceive, and author workload that does not improve fairness, tension, replayability, or clarity.

If a rule cannot be tested or used, it SHOULD be removed or rewritten as guidance.

## 2.9 Print-first transparency

The player MUST be able to operate all required player-facing mechanics from printed material and character sheets.

The player MUST NOT be required to evaluate internal Boolean expressions.

Player-facing conditions MUST use visible concepts such as a keyword, an item, a resource threshold, a public condition, or a clearly recorded character state.

## 2.10 Controlled hidden mechanics

Hidden mechanics MAY exist, including delayed consequences, hidden NPC suspicion, hidden real-time pressure, off-screen movement, and concealed thresholds.

A hidden mechanic MUST:

1. have a defined cause;
2. have a defined activation rule;
3. produce perceivable consequences;
4. remain testable by developers;
5. avoid impossible player obligations;
6. not depend on knowledge the player was never given.

## 2.11 Optional real-time pressure

Real-time pressure is OPTIONAL at the adventure or group level.

The rulebook MUST allow players to disable real-time enforcement.

If real-time enforcement is disabled:

- elapsed real time MUST NOT trigger negative consequences;
- all related expiry instructions MUST be ignored;
- the adventure MUST remain fully playable.

A real-time event MAY be announced in advance, announced when it begins, or revealed only after the choice is complete.

Hidden real-time pressure is allowed only if:

- the rulebook discloses that hidden timed moments may occur;
- the group has not disabled the mechanic;
- timing starts from a clearly defined player action;
- unrelated interruptions cannot fairly count against the player;
- the result does not require impossible precision;
- an untimed mode exists.

## 2.12 Replayability comes from consequence, not noise

Replayability SHOULD arise from different decisions, clue access, trust relationships, timing, character capabilities, interpretations, resource use, and endings.

Replayability SHOULD NOT depend primarily on arbitrary random world truth.

## 2.13 Two-player equality

In a two-player adventure, both characters MUST remain meaningful protagonists.

The design SHOULD avoid one permanent leader, one character acting only as support, long inactivity, private scenes so long that the other player disengages, mechanically identical characters, and one character owning all critical skills.

Different roles are encouraged. Unequal importance is not.

## 2.14 Authoring is separate from compilation

The author defines truth, state, logic, conditions, consequences, and narrative objectives.

The Narrative Compiler defines what the character can perceive, what wording is appropriate, what uncertainty remains visible, and which static public node is produced.

The Book Formatter defines public event numbering, page layout, references, printable structure, and navigation.

No layer may silently perform the responsibilities of another.

## 2.15 Testing is part of design

Testing MUST begin before the adventure is fully written.

The engine SHOULD support schema validation, graph validation, world-state simulation, knowledge-origin validation, timeline validation, ending reachability, fair-play review, two-player pacing review, and physical usability review.

A story that reads well but cannot pass consistency testing is not complete.

## 2.16 Root-cause correction

A defect MUST be corrected in the deepest responsible layer.

Examples:

- impossible NPC knowledge is fixed in knowledge or event logic;
- contradictory item location is fixed in state updates;
- broken public references are fixed in formatting;
- misleading narration is fixed in the Narrative Compiler;
- weak clue access is fixed in adventure logic.

Narrative rewriting MUST NOT be used to conceal an unresolved logical defect.

## 2.17 Completion condition for this chapter

This chapter may be marked Approved when:

- every principle is accepted;
- optional mechanics are clearly separated from mandatory rules;
- hidden timing rules are considered fair;
- two-player equality is accepted;
- complexity control is accepted;
- no principle contradicts the Introduction and Scope chapter.
