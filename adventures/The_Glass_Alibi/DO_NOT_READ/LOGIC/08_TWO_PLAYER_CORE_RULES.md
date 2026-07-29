# DO NOT READ: Two-Player Core Rules

## 1. Design goal

Both players must make independent meaningful decisions, hold useful private information, and participate in the final act. Separation creates perspective, not administrative waiting.

**Play mode:** `two_player` only. Solo mode is deferred (`10_INVESTIGATION_NODE_GRAPH.md` § 18).

Scene modes use **narrative roles**, not `P1`/`P2` labels in player-facing text. Schema keys `P1_*` / `P2_*` map to Role A / Role B for engine compatibility.

## 2. Starting asymmetry

Default **role suggestions** at briefing (either player may take either role per MBD-02):

### Field / scene emphasis (Role A)

- test bay and maintenance access;
- physical evidence interpretation;
- Tom and Vince field contact;
- athletics-gated routes.

### Systems / finance emphasis (Role B)

- SCADA and security desk research;
- digital/procedural evidence;
- Kevin and Sable interaction;
- finance hub and ledger analysis.

These are emphasis areas for character sheets, not exclusive locks or node ownership.

## 3. Split safety rule

During a split:

- no role receives a clue required for the other role's immediate live puzzle;
- time-critical combination puzzles occur only after regroup or legal communication;
- each branch has an independent useful outcome;
- one role's failure cannot trap the other in a waiting loop.

### Split completion (MBD-03)

Each player continues until they have no remaining legal actions. When finished, they **wait** — no forced movement, no automatic jump, no timer-based interruption, and no pressure on the other player. `WAIT_UNTIL_SYNC`, `REMOTE_CONTACT`, and `EMERGENCY_INTERRUPT` are window-level options (§ 4 below; `04` § 3a), not per-node rules.

Regroup requires **branch completion** plus **player agreement** to enter `EVT_150` or `EVT_300`. Deprecated `P1_AVAILABLE_AT` / `P2_AVAILABLE_AT` are not used.

## 4. Communication modes

Window-level constant mapping (MBD-03):

| Window constant | Player-facing mode |
|---|---|
| `REMOTE_CONTACT` | campus phone; secure text where noted |
| `EMERGENCY_INTERRUPT` | incident PA or security broadcast |
| `WAIT_UNTIL_SYNC` | finished player waits until partner completes branch or players agree to regroup |

- **Physical regroup:** all chosen information may be shared; costs 10 minutes.
- **Phone call:** one concise clue or decision; costs 5 minutes; unavailable inside RF-shielded test bay.
- **Message:** may be delayed by scene rules; cannot support real-time puzzle coordination.
- **Emergency broadcast:** one-way; may raise `A_CORPORATE` or `A_SECURITY`.

The books must clearly tell players when communication is legal.

## 5. Required regroup gates

### Regroup 1 (`EVT_150`)

Around 20:20-20:40 after initial investigation. Purpose: combine murder/credential and systems evidence.

### Regroup 2 (`EVT_300`)

No later than 22:45. Purpose: combine fraud thread, Dana suspicion, witness exports, and final-act assignment.

### Split Three

After Regroup 2 assignment; converges at `EVT_410` / `EVT_900`. Players may remain split until explicit convergence choice.

## 6. Final-act parity

Possible simultaneous roles:

- one role secures SCADA/footage copies while the other confronts Dana;
- one files formal challenge while the other preserves physical device;
- one interviews Vince at perimeter while the other traces finance exit;
- one documents test bay while the other transmits external proof.

Both roles must contain decisions, not merely skill checks.

## 7. Knowledge-card rule

Private clues should be formatted as small numbered knowledge cards or clearly bounded passages. On sharing, the player records the clue ID in the shared case file.

## 8. Conflict resolution

When players disagree at a shared decision:

1. discuss within any stated real-time limit;
2. each chooses a priority if no agreement;
3. apply the branch that reflects actual actions, allowing objectives to diverge;
4. do not use random coin flips unless physical actions are mutually exclusive and simultaneous.

## 9. Participation audit (MBD-05)

The participation audit is a **developer validation tool**. Players never see it. Its purpose is validating adventure balance before compilation.

The audit evaluates **all valid story paths** — it does **not** use a single canonical reference path. It is **informational only** and must not modify gameplay.

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
| Opening / Split One | field/scene role vs systems/finance role | `13` § 2 |
| Midgame / Split Two | Pair A (bay + maintenance), Pair B (SCADA + finance), Pair C (security + architect) | `13` § 4 |
| Final act | Confront/Preserve; Interior/Exterior; Proof/Custody role pairs | `13` § 7 |

### Audit summary

Authoritative per-path tables are in `13_SPLIT_AND_REGROUP_FLOW.md` § 9.

| Block | Status | Notes |
|---|---|---|
| Opening / Split One | **Pending** | Two roles compared; flags TBD at node authoring |
| Regroup One | **Pending** | Joint decisions; clue transfer only |
| Midgame / Split Two | **Pending** | Pairs A, B, C compared at Alpha 0.2b |
| Regroup Two | **Pending** | Joint assignment; final-act role responsibility per path |
| Final act | **Pending** | Three role-pair patterns compared at Alpha 0.2b |

**Validation rule:** If any metric differs by more than 2× between roles on the same path, or if one role has zero decisions across an entire block, flag for author review in `13` § 9. The audit does not auto-correct gameplay.

When `13` is authored, update this summary to **Complete** per block.
