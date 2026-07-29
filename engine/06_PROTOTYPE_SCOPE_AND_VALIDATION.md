# 06. Prototype Scope and Validation Gate

## 1. Objective

The immediate objective is not to finish every possible future engine feature. It is to produce and test one complete, approximately two-hour detective adventure that supports:

- one-player mode (long-term engine goal);
- two-player cooperative mode;
- fair-play investigation;
- meaningful choices;
- deterministic world behavior;
- limited replayability;
- a complete playable ending.

The prototype is the next architecture test. Engine work that does not materially improve this prototype may be deferred.

**Alpha 0.2c adventure logic revision:** `adventures/The_Last_Witness/` officially supports **`two_player` only** for this release (`MBD-06`). Solo mode remains a future engine goal; validation for Alpha 0.2c evaluates `two_player` paths only. See `LOGIC/10_INVESTIGATION_NODE_GRAPH.md` § 18.

## 2. Required Before Adventure Production

The following must be defined before compiling the prototype:

- authoritative world clock;
- compile-time versus play-time boundary;
- two-player synchronization rules;
- public and private knowledge separation;
- event, clue, item, NPC, location, and terminal identifiers;
- clue redundancy requirements;
- terminal node types;
- soft-lock prevention and recovery rules;
- minimal schema version metadata.

## 3. Deferred Until After Playtest

The following are valuable but not required for the first prototype:

- full JSON Schema implementation;
- automated CLI or GUI compiler;
- CI/CD integration;
- campaign save migration;
- arbitrary player counts;
- complex event queues;
- extensive procedural generation;
- full multilingual build automation;
- commercial print-layout optimization.

They remain planned architectural directions rather than current blockers.

## 4. Prototype Complexity Budget

The first prototype should target:

- approximately 90 to 150 minutes of play;
- 2 playable investigators;
- 1 central case;
- 3 to 5 major suspects;
- 4 to 7 locations;
- 12 to 20 meaningful clues;
- no more than 30 tracked public state fields;
- no more than 8 critical state fields;
- no more than 3 split-scene windows;
- 3 to 6 terminal outcomes;
- 1 primary solution with fair evidence;
- optional controlled seed variation only where it does not multiply authoring cost excessively.

These numbers are design targets, not permanent engine limits.

## 5. Soft-Lock Prevention

Every critical deduction must have at least two independent acquisition routes unless the clue is guaranteed by the main path.

A critical item or fact must not be permanently lost through an uninformed choice without one of the following:

- an alternative route;
- a recovery scene;
- a substitute clue;
- a degraded but still solvable outcome;
- an explicit intentional failure ending.

The adventure must never silently become impossible while still pretending to be solvable.

## 6. Fallback Handler

The prototype shall use authored fallback events rather than a universal runtime handler.

Fallback events may trigger when:

- time reaches a threshold;
- all normal clue routes are exhausted;
- a critical NPC leaves or becomes unavailable;
- players lose access to a required location;
- the investigation reaches a defined low-information state.

Fallbacks may preserve solvability at a cost, such as lost time, reduced score, danger, or a less favorable ending.

## 7. Replayability Policy

The first prototype may use controlled seed variables, but replayability is secondary to fairness and playability.

Permitted seeded elements include:

- location of a non-critical clue;
- optional suspect secret;
- secondary obstacle;
- safe combination source;
- order of selected off-screen events.

The primary culprit or core causal truth should remain fixed in Prototype 1 unless the adventure is explicitly authored and validated for multiple culprit seeds.

## 8. Playtest Exit Criteria

Prototype 1 is considered successful when:

- both solo and two-player modes can reach valid endings (full prototype goal; **Alpha 0.2c logic evaluates `two_player` only** per `MBD-06`);
- no player must inspect internal IDs or hidden state;
- the shared clock remains consistent;
- no split scene creates contradictory timing;
- the central solution can be logically deduced;
- missing one clue does not automatically break the case;
- bookkeeping does not dominate play;
- all links, choices, and terminal nodes resolve correctly;
- players can explain what confused them after the session.

## 9. Post-Playtest Review

After the first complete playthrough, every issue shall be classified as:

- CONTENT_DEFECT;
- ADVENTURE_LOGIC_DEFECT;
- ENGINE_RULE_DEFECT;
- COMPILER_REQUIREMENT;
- FORMATTER_DEFECT;
- PLAYER_USABILITY_DEFECT.

Only observed or strongly justified engine defects should expand the core specification before the next prototype.
