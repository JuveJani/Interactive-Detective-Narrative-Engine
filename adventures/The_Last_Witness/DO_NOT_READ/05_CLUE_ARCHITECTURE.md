# DO NOT READ: Clue Architecture

## 1. Purpose

This document defines conclusion-level redundancy. It is not yet the final node graph. It ensures the case remains solvable after failed checks, missed locations, or one unavailable NPC.

## 2. Clue classes

- **Physical:** object, trace, document, recording.
- **Testimonial:** statement from an NPC.
- **Procedural:** metadata, logs, authorization records.
- **Contextual:** motive, history, financial pressure.
- **Behavioural:** contradiction or action observed by players.

Critical conclusions require at least two independent classes.

## 3. Required conclusions

### CON-01: The apartment abduction was staged

Primary clues:

- CLU-01 preserved blood;
- CLU-02 missing medication and passport;
- CLU-03 internal service-latch disturbance;
- CLU-04 timed crash device.

Fallback clues:

- neighbour sighting matches Elias's size;
- broken-phone trace contradicts struggle;
- Nadia admits Elias planned to avoid pickup.

Minimum proof: two strong clues, or one strong clue plus Nadia's admission.

### CON-02: Elias travelled to the harbor voluntarily

Primary clues:

- transit-card record;
- Café Orpheus tide note;
- rear-lane sighting;
- tram camera image.

Fallback clues:

- Elias searched ferry schedules;
- harbor grit on his spare shoes;
- Nadia's incomplete confession.

### CON-03: Signal Room 4B is the destination

Primary clues:

- missing ferry photograph;
- historical window numbering;
- “Four-B” verbal fragment;
- cable-corridor map;
- maintenance battery record.

Fallback clues:

- generator vibration at terminal;
- medical-package trail;
- Lena or Iris cooperation.

No one clue should provide both the room and the safest route.

### CON-04: Lena is protecting, not abducting, Elias

Primary clues:

- prepaid-phone call to Iris;
- timing showing Elias arrived first;
- injury blood pattern;
- Iris's medical supplies;
- Lena's attempts to divert Reed rather than demand money.

Fallback clues:

- Reed admits confrontation;
- Elias fragment naming “not Lena” in an expanded version;
- Lena gives verifiable details about the fall.

### CON-05: Reed caused the confrontation

Primary clues:

- harbor grit and blood on clothing;
- decoy key in his possession;
- Krell's recovery messages;
- terminal access trace.

Fallback clues:

- Lena testimony;
- partial camera silhouette;
- Reed's own negotiated confession.

### CON-06: Marcus leaked the plan

Primary clues:

- external carrier call record;
- payment transfer;
- deleted newsroom log;
- access to Nadia's archive.

Fallback clues:

- intermediary voicemail;
- Reed naming source channel;
- Marcus's inconsistent timeline.

### CON-07: Rook is compromised

Primary clues:

- unauthorized camera request;
- altered report metadata;
- false witness-transfer paperwork;
- contact with Krell;
- fabricated bulletin about Lena.

Fallback clues:

- Reed says Rook protects Krell;
- Mina testimony;
- evidence-room photograph provenance.

Minimum fair exposure: three clues from at least two classes.

### CON-08: Elias needs immediate hospital care

Primary clues:

- Iris assessment;
- progressive symptoms;
- medical reference available to Player 2;
- observed unequal pupils and unconsciousness.

This conclusion should not require a difficult check after Elias is found. The challenge is acting safely, not diagnosing an obscure condition.

### CON-09: The black key is a decoy

Primary clues:

- limited document contents;
- tracker process;
- Elias fragment “black one is false”;
- mismatch with archive hash list.

Fallback clues:

- Nadia knows Elias prepared a decoy;
- Reed's failed decryption attempt.

### CON-10: The final recovery code is hidden in window numbers

Primary clues:

- Nadia's three-digit fragment;
- ferry photograph markings;
- archive description of window numbering;
- Elias fragment “windows.”

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
