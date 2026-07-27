# DO NOT READ: Location State Machine

## 1. Purpose

This file defines how investigation locations change over time and through off-screen actions. A compiled player node must select the correct location variant from current state, not assume the first-visit description remains valid forever.

## 2. Elias apartment

### State A: `SEALED_ACCESSIBLE_WITH_MINA`

**Typical window:** 20:05-20:45  
**Available**

- cooperative access;
- Mina interview;
- full physical search;
- service-corridor inspection.

**Transitions**

- clock threshold or Rook awareness -> `RESTRICTED_BY_ROOK`;
- key evidence found remains found even after transition.

### State B: `RESTRICTED_BY_ROOK`

**Available**

- common-area clues;
- Mina-mediated access;
- procedural challenge;
- risky unauthorized entry.

**Unavailable without cost**

- unrestricted bedroom search.

**Transition**

At 22:15, if timed device not discovered, loyal detective attempts removal:

- device state becomes `SEIZED_BY(NPC_ROOK_NETWORK)`;
- removal trace remains discoverable;
- conclusion route survives through other clues.

### State C: `EVIDENCE_PARTIALLY_REMOVED`

**Available**

- disturbed cabinet;
- service route;
- witness timing;
- forensic inconsistencies from photographs or Mina notes.

### State D: `INACCESSIBLE`

Late-game state. No new physical search, but report/photo routes remain.

---

## 3. Newsroom

### State A: `OPEN_SUPERVISED`

Marcus and Nadia present.

**Available**

- interviews;
- visible debt context;
- archive gap;
- limited server access.

### State B: `MARCUS_DELETING`

Triggered around 20:35 if players have not engaged him.

**Effect**

- local call entry becomes deleted-recoverable;
- Marcus's anxiety becomes observable;
- recovery costs more time or requires external carrier route.

### State C: `MARCUS_ABSENT`

Triggered around 23:20.

**Effect**

- office access becomes physically easier;
- direct interrogation unavailable;
- intermediary-meeting trail unlocks.

### State D: `UPLOAD_ACTIVE`

Triggered at 00:00.

**Effect**

- evidence transfer UI available;
- incorrect or incomplete input may consume time;
- Rook cannot silently erase already transmitted external copies.

---

## 4. Café Orpheus

### State A: `OPEN_FULL_RECORDS`

Before 22:00.

**Available**

- staff;
- receipt;
- footage;
- tide note;
- Lena reflection.

### State B: `CLOSING_LIMITED`

22:00-22:30.

**Available**

- staff testimony;
- receipt;
- overwritten footage remnants if copied in time;
- physical tide note if not removed.

### State C: `CLOSED`

After 22:30.

**Available through**

- owner cooperation;
- Nadia contact;
- return next day only in failure epilogue.

The branch loses convenience, not all mandatory clues.

---

## 5. Police annex

### State A: `NORMAL_ACCESS`

Low Rook awareness.

**Available**

- Mina contact;
- public metadata;
- protection-order questions.

### State B: `CONTROLLED_ACCESS`

At `A_ROOK_PLAYERS >= 2`.

**Effects**

- questioning pressure;
- records may require external preservation;
- police-system searches increase awareness.

### State C: `HOSTILE_PROCEDURAL`

At `A_ROOK_PLAYERS >= 3`.

**Effects**

- false holds;
- evidence-surrender demands;
- Mina's cooperation becomes covert.

### State D: `ROOK_CHALLENGED`

At sufficient private or public proof.

**Effects**

- Rook loses uncontested authority;
- rescue options expand;
- loyal officers still create friction.

---

## 6. Reed office

### State A: `EMPTY_INTACT`

Before Reed's brief return.

**Available**

- physical residue;
- laptop;
- message traces.

### State B: `REED_PRESENT`

Creates interview, surveillance, or confrontation option.

### State C: `ABANDONED`

Reed has left. Core traces remain.

### State D: `SEARCHED_BY_KRELL`

Strongest items may be removed, but fallback evidence remains:

- wiped-device metadata;
- residue;
- discarded packaging;
- external message/carrier records.

No critical conclusion depends exclusively on the intact state.

---

## 7. Iris workplace

### State A: `SHIFT_ACTIVE`

Before missing supplies are reported.

**Available**

- staff conversation;
- direct inventory comparison;
- parking footage.

### State B: `INCIDENT_REPORTED`

After 22:00.

**Effects**

- police visibility;
- records may be seized;
- witness testimony and external footage remain.

### State C: `ROOK_SEIZED_RECORDS`

Late hostile state.

**Fallback**

- supervisor's memory;
- care logs;
- phone record;
- parking camera copy through external vendor.

---

## 8. Harbor archive

### State A: `OPEN_PUBLIC`

Normal access.

### State B: `CLOSING_ARCHIVIST_PRESENT`

Requires persuasion or urgency.

### State C: `CLOSED_EMERGENCY`

Access through:

- Nadia credentials;
- Mina;
- exterior reference plaques;
- copied municipal plan;
- late generator-trace failsafe.

---

## 9. Terminal exterior

State is a combination of three dimensions.

### Weather

- `DRY`
- `SURGE`
- `DRAINAGE_CLOSED`

### Hostile presence

- `NONE`
- `REED`
- `ROOK_TEAM`
- `REED_AND_ROOK`

### Known access routes

Set containing:

- `MAIN`
- `NORTH_GATE`
- `DRAINAGE`
- `CABLE_CORRIDOR`
- `EMERGENCY`

### Transition rules

- 22:45 -> `SURGE`;
- 23:30 -> `DRAINAGE_CLOSED`;
- 00:20 -> Reed enters unless interrupted;
- 01:20 -> Rook team enters if terminal exposure threshold reached.

The compiler combines these dimensions into scene text rather than maintaining dozens of separate hand-authored location IDs.

---

## 10. Signal Room 4B

### `HIDDEN_STABLE`

Before major deterioration.

### `HIDDEN_MEDICAL_DECLINE`

Elias worsens; Iris knows rescue is urgent.

### `FOUND_SECURE`

Players arrive before hostile actors.

### `FOUND_CONTESTED`

Reed or Rook threatens the scene.

### `EVACUATED`

Elias and/or ledger removed.

### `OVERRUN`

Hostile control established.

A transition to `OVERRUN` does not automatically end the game. Players may still preserve partial evidence or expose wrongdoing, producing a weaker but resolved ending.
