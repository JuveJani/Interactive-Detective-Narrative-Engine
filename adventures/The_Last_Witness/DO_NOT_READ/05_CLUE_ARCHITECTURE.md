# DO NOT READ: Clue Architecture

## 1. Purpose

This document defines conclusion-level redundancy. It is not yet the final node graph. It ensures the case remains solvable after failed checks, missed locations, or one unavailable NPC.

## 2. Clue classes

**Non-authoritative summary.** The clue-class vocabulary is owned by `LOGIC/07_EVIDENCE_VALIDATION.md` § "1. Proof classes". That section is canonical. The gloss below is a convenience summary and must not be treated as a declaration.

- **Physical:** object, trace, document.
- **Digital:** recording, file, metadata payload, transmitted data.
- **Testimonial:** statement from an NPC.
- **Procedural:** metadata, logs, authorization records.
- **Contextual:** motive, history, financial pressure.
- **Behavioural:** contradiction or action observed by players.

Critical conclusions require at least two independent classes.

## 3. Required conclusions

**Narrative rationale only.** Clue identifiers, class tags, point values, granting nodes and every threshold are owned by `LOGIC/12_CLUE_DEPENDENCY_GRAPH.md` and `LOGIC/07_EVIDENCE_VALIDATION.md` § 2. This section explains why each conclusion matters to the case and must not be read as a count.

### `CON_STAGED_DISAPPEARANCE`: the apartment abduction was staged

The first thing the players must stop believing. Until the official abduction narrative breaks, every later route reads as a search for a kidnapper rather than for a man who left on purpose. The evidence is deliberately mundane: `CLUE_APT_BLOOD_OLD`, `CLUE_APT_MEDICATION_MISSING`, `CLUE_APT_PASSPORT_MISSING`, `CLUE_APT_SERVICE_LATCH`, `CLUE_APT_TIMED_DEVICE` and `CLUE_NEIGHBOUR_EXIT_BEFORE_CRASH`, with `CLUE_NADIA_PLAN_ADMISSION` as the testimonial route.

### `CON_HARBOR_DESTINATION`: Elias travelled to the harbor voluntarily

Converts a city-wide search into a targeted one. Nothing here names the room, only the direction, which is what keeps the room a separate deduction.

### `CON_SIGNAL_4B`: Signal Room 4B is the destination

Deliberately split into an identifier and a route, so that knowing where he is and being able to reach him remain two achievements. No single clue supplies both.

### `CON_LENA_PROTECTING`: Lena is protecting, not abducting

The case's central misreading. The deduction does not declare her legally innocent; it establishes that "kidnapper" is an incomplete model.

### `CON_REED_PRESENT` and `CON_REED_CAUSED_CONFRONTATION`

Two tiers, because presence at the terminal and causing the fall are different claims with different evidential weight. The stronger tier must not be reachable from testimony alone.

### `CON_MARCUS_LEAK_PARTIAL` and `CON_MARCUS_LEAK_PROVABLE`

Two tiers, because a leak the players believe in and a leak they can prove publicly have different consequences. Either way the ending must clarify that Marcus transmitted partial operational information, not the room or the scheme.

### `CON_ROOK_OPERATIONALLY_COMPROMISED` and `CON_ROOK_PUBLICLY_PROVABLE`

The load-bearing pair. The private tier lets players act — refuse official rescue, route through Mina. The public tier is what a prosecution needs, and it is deliberately harder, requiring class diversity and a preserved copy rather than volume alone.

### `CON_MEDICAL_EMERGENCY`: Elias needs immediate hospital care

Must never require a difficult diagnostic check. The challenge is acting safely, not diagnosing an obscure condition, which is why entering the room satisfies it outright.

### `CON_DECOY_KEY`: the black key is a decoy

Prevents the transfer accepting the wrong hardware key, so that a player who recovered something feels the difference between something and the right thing.

### `CON_WINDOW_CODE`: the final digits are hidden in window numbers

Split between Nadia and Elias by design, so neither can complete the archive alone.

## 4. Red-herring policy

Red herrings must arise from genuine secrets, not fabricated nonsense.

### Red herring RH-01: Lena as kidnapper

Plausible because:

- she followed Elias;
- she lies about arrival;
- police bulletin names her;
- she hides him.

Resolution: her actions are obstructive but protective.

### RH-02: Nadia sacrificed Elias for a story

Plausible because:

- she planned the disappearance;
- she withholds information;
- she pressures the transfer.

Resolution: she made risky choices but did not leak the plan.

### RH-03: Marcus is the mastermind

Plausible because:

- he leaked information;
- received money;
- manipulates records.

Resolution: he is culpable but lacks control over police and contracts.

### RH-04: Elias embezzled funds

Plausible because:

- Rook releases selected financial records;
- Elias moved encrypted files;
- he fled official protection.

Resolution: the records are selectively framed and contradicted by the full ledger.

## 5. Failure transformation

Failed checks should generally change cost or certainty.

Examples:

- failed apartment forensics check: player notices blood is suspicious but not why; later medical help can clarify.
- failed newsroom computer check: data recovery takes more time or alerts Marcus.
- failed persuasion with Mina: she withholds active help but leaves a procedural hint.
- failed terminal navigation: player reaches a dangerous access route and spends time.
- failed Reed confrontation: Reed flees but drops a phone or key clue.

## 6. Soft-lock prevention

The engine must preserve at least one route to:

- identify the harbor;
- identify Signal Room 4B;
- discover Elias's medical danger;
- expose Rook enough to question official rescue.

Failsafe mechanisms are diegetic:

- Nadia remembers a photograph detail;
- Mina releases altered metadata;
- the storm reveals generator noise;
- Reed's decoy-key tracker points toward the terminal;
- Elias briefly repeats “Four-B.”

Failsafes should cost time, trust, or ending quality. They must not provide a perfect solution for free.
