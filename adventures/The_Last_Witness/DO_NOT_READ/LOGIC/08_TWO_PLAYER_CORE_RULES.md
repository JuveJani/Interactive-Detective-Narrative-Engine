# DO NOT READ: Two-Player Core Rules

## 1. Design goal

Both players must make independent meaningful decisions, hold useful private information, and participate in the final act. Separation creates perspective, not administrative waiting.

## 2. Starting asymmetry

Default **role suggestions** at briefing (either player may take either role per MBD-02):

### Apartment-cluster emphasis

- field access;
- physical scene interpretation;
- Mina contact;
- confrontation and route security.

### Newsroom-cluster emphasis

- newsroom/archive research;
- digital/procedural evidence;
- Nadia and Marcus interaction;
- upload/code interpretation.

These are emphasis areas for character sheets, not exclusive locks or node ownership.

## 3. Split safety rule

During a split:

- no player receives a clue required for the other player's immediate live puzzle;
- time-critical combination puzzles occur only after regroup or legal communication;
- each branch has an independent useful outcome;
- one player's failure cannot trap the other in a waiting loop.

### Split completion (MBD-03)

Each player continues until they have no remaining legal actions. When finished, they **wait** — no forced movement, no automatic jump, no timer-based interruption, and no pressure on the other player. `WAIT_UNTIL_SYNC`, `REMOTE_CONTACT`, and `EMERGENCY_INTERRUPT` are window-level options (§ 4 below; `04` § 3a), not per-node rules.

## 4. Communication modes

Window-level constant mapping (MBD-03):

| Window constant | Player-facing mode |
|---|---|
| `REMOTE_CONTACT` | phone call; text message |
| `EMERGENCY_INTERRUPT` | emergency broadcast |
| `WAIT_UNTIL_SYNC` | finished player waits until partner completes branch or players agree to regroup |

- **Physical regroup:** all chosen information may be shared; costs 10 minutes.
- **Phone call:** one concise clue or decision; costs 5 minutes; unavailable in Signal Room 4B.
- **Message:** may be delayed by scene rules; cannot support real-time puzzle coordination.
- **Emergency broadcast:** one-way, may raise antagonist awareness.

The books must clearly tell players when communication is legal.

## 5. Required regroup gates

### Regroup 1

Around 21:20-21:40 after initial investigation. Purpose: combine staging and harbor evidence.

### Regroup 2

No later than 23:15. Purpose: combine terminal route, Rook evidence, medical trail, and rescue preparation.

Players may choose to remain split after Regroup 2, but the choice is explicit and the final act assigns parallel responsibilities.

## 6. Final-act parity

Possible simultaneous roles:

- one player enters Signal Room 4B while the other secures the route;
- one coordinates medical rescue while the other completes evidence transfer;
- one negotiates with Lena/Iris while the other confronts Reed/Rook;
- one preserves public proof while the other physically evacuates Elias.

Both roles must contain decisions, not merely skill checks.

## 7. Knowledge-card rule

Private clues should be formatted as small numbered knowledge cards or clearly bounded passages. On sharing, the player records the clue ID in the shared case file. This avoids handing over whole player books like humans exchanging classified encyclopedias at a bus stop.

## 8. Conflict resolution

When players disagree at a shared decision:

1. discuss within any stated real-time limit;
2. each chooses a priority if no agreement;
3. apply the branch that reflects actual actions, allowing objectives to diverge;
4. do not use random coin flips unless the physical actions are mutually exclusive and simultaneous.

## 9. Participation audit (MBD-05)

The participation audit is a **developer validation tool**. Players never see it. Its purpose is validating adventure balance before compilation.

The audit evaluates **all valid story paths** — it does **not** use a single canonical reference path and does **not** privilege any one midgame pair (e.g. Pair A). It is **informational only** and must not modify gameplay.

### Metrics per path

For each valid path, compare the two narrative roles regarding:

- decisions;
- clues;
- locations visited;
- challenges (`CHK_*` and approach-choice nodes);
- gameplay time (action-cost sum along path);
- communication opportunities;
- overall participation.

Small differences are acceptable. Large systematic imbalance across paths should fail validation. Flags in `13` § 9 are for **manual author review only**; the audit does not auto-correct gameplay.

### Valid paths evaluated

| Block | Paths | Source |
|---|---|---|
| Opening / Split One | apartment role vs newsroom role | `13` § 2 |
| Midgame / Split Two | Pair A, Pair B, Pair C track assignments | `13` § 4 |
| Final act | Rescue/Evidence; Interior/Exterior; Proof/Protection role pairs | `13` § 7 |

### Audit summary

Authoritative per-path tables are in `13_SPLIT_AND_REGROUP_FLOW.md` § 9.

| Block | Status | Notes |
|---|---|---|
| Opening / Split One | **Complete** | Two roles compared; two manual-review flags in `13` § 9 |
| Regroup One | **Complete** | Joint decisions; clue transfer only |
| Midgame / Split Two | **Complete** | Pairs A, B, C compared with full metrics |
| Regroup Two | **Complete** | Joint assignment; final-act role responsibility per path |
| Final act | **Complete** | Three role-pair patterns compared with full metrics |

**Validation rule:** If any metric differs by more than 2× between roles on the same path, or if one role has zero decisions across an entire block, flag for author review in `13` § 9. The audit does not auto-correct gameplay.
