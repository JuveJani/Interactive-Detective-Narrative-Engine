# 05. Two-Player Synchronization Model

## 1. Purpose

This chapter defines a practical two-player mode for a static detective gamebook without requiring players to simulate a software engine with pencils and misplaced optimism.

## 2. Shared Authoritative World Time

The adventure uses one authoritative world clock.

```text
WORLD_TIME = shared campaign time
```

Player actions may have individual durations, but time advances globally only through synchronization points defined by the adventure.

## 3. Scene Modes

Every playable scene must declare one of the following modes.

### 3.1 Joint Scene

Both players are present and read the same public content. They make a shared decision unless the scene explicitly assigns separate choices.

### 3.2 Split Scene

Each player receives separate player-facing content. Private information is isolated. Split scenes must end at a synchronization point.

### 3.3 Solo Scene

One player acts while the other player is temporarily inactive, observing only information the scene permits.

## 4. Synchronization Windows

Split play is organized into synchronization windows.

Each window has:

- a start timestamp;
- a maximum duration;
- one action sequence per player;
- a defined reunion or communication point;
- a deterministic rule for unused time.

Example:

```text
Window start: 16:00
Window duration: 30 minutes
Player 1 action cost: 20 minutes
Player 2 action cost: 30 minutes
Next shared time: 16:30
```

The shorter action does not allow unlimited extra actions. Any remaining time is resolved only through an explicitly offered waiting, preparation, travel, or communication option.

## 5. No Free Asynchronous Drift

Players must not independently advance the global clock by following separate node chains indefinitely.

Every split branch must terminate in one of these outcomes:

- REJOIN;
- REMOTE_CONTACT;
- WAIT_UNTIL_SYNC;
- EMERGENCY_INTERRUPT;
- TERMINAL_OUTCOME.

This prevents temporal drift and contradictory world states.

## 6. Knowledge Isolation

Each player has a private knowledge state.

```text
K_P1 = facts known by Player 1
K_P2 = facts known by Player 2
K_SHARED = facts explicitly exchanged
```

Information moves into `K_SHARED` only when:

- players are together and choose to exchange it;
- a communication action succeeds;
- a rule explicitly marks the information as shared.

Physical play should use separate player booklets or clearly separated player sections for split scenes. The first prototype may use two PDF files or two individually delivered text files.

## 7. Communication Rules

Communication is an action when players are split. It may have:

- time cost;
- availability conditions;
- range or equipment requirements;
- interruption risk;
- a limit on how much information can be exchanged.

Players may not share private information out of character unless the adventure explicitly allows unrestricted table discussion.

## 8. Conflict Resolution

If both players affect the same world entity during one synchronization window, Adventure Logic must define priority using this order:

1. earlier timestamp;
2. explicit interrupt priority;
3. simultaneous-event rule;
4. predetermined tie-break rule.

The players must never improvise hidden-world resolution.

## 9. Prototype Rule Set

For the first two-hour prototype:

- use no more than three split-scene windows;
- keep each window between 10 and 30 world minutes;
- provide a forced synchronization endpoint;
- use separate Player 1 and Player 2 outputs during split scenes;
- keep communication rules simple;
- use one shared clock and one shared world-state record.

## 10. Adventure-scoped profile — The Last Witness (Alpha 0.2c)

For **Prototype Alpha 0.2c** logic (`adventures/The_Last_Witness/`), owner-approved Milestone B decisions (MBD-01–06) apply the following **adventure-scoped** interpretations. They do not amend this engine chapter globally.

| Engine rule (this chapter) | Alpha 0.2c adventure interpretation |
|---|---|
| § 4 maximum duration and leftover-time micro-rules | **Not simulated**; pacing uses `04_TIME_COST_MATRIX.md` § 5 block targets (`MBD-04`) |
| § 4 per-player action-cost synchronization example | **Not used**; single shared `CLOCK` only |
| § 5 branch terminators `REMOTE_CONTACT`, `WAIT_UNTIL_SYNC`, `EMERGENCY_INTERRUPT` | **Window-level only** (`08` § 4; `13` § 5); not per-node metadata (`MBD-03`) |
| § 5 node-level terminators | `REJOIN` and `TERMINAL_OUTCOME` only (`10` § 1d) |
| § 3.3 Solo scene mode | **Not used** in this adventure; `play_modes: [two_player]` only (`MBD-06`) |

See `MILESTONE_B_IMPLEMENTATION_V2_REPORT.md` and `ENGINE_READINESS_PLAN.md` Appendix C.
