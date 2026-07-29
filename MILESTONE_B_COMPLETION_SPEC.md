> **SUPERSEDED.** Proposed rules before owner approval of MBD-01–06. Authoritative implementation: `MILESTONE_B_IMPLEMENTATION_V2_REPORT.md`, adventure logic `17_CHECK_REGISTER.md` and `10` §1b–§1d.

# Milestone B Completion Specification

**Document type:** Engine specification (missing rules only)  
**Status:** **Superseded** — not implemented; retained for history only  
**Scope:** Resolves remaining Milestone B blockers ER-02, ER-03, ER-04, ER-05, ER-09, ER-10  
**Authority:** Subordinate to `IMPLEMENTATION_PLAN.md`, `ENGINE_READINESS_PLAN.md`, and existing adventure logic. Does not modify gameplay, routes, narrative, or repository files.

**Source baseline:** `MILESTONE_B_IMPLEMENTATION_REPORT.md` (branch `cursor/milestone-b-logic-bad4`, commit `d10a72f`).

---

## 1. Purpose

This document defines the **minimum deterministic rules** required to complete Milestone B without:

- changing any `EVT_*` route, clue grant, threshold, timing outcome, or ending condition;
- inventing narrative content;
- implementing changes in the repository.

Each section resolves one ER blocker by specifying **ownership**, **assignment method**, and **validation criteria**. Where the repository already implies a solution, that solution is documented. Where it does not, the smallest new rule is declared.

---

## 2. ER-02 — Check (`CHK_*`) records

### 2.1 Repository finding

| Question | Answer | Evidence |
|---|---|---|
| Global DC system required? | **No** | `ENGINE_READINESS_PLAN.md` ER-02 assigns checks to adventure logic (`17_CHECK_REGISTER.md`). No engine DC table exists. `engine/README.md` ch. 11 (Decisions and checks) is not authored. |
| D20 resolution required? | **Yes** | `engine/01_INTRODUCTION_AND_SCOPE.md` § 1.2: first reference implementation expects a D20-based resolution system. |
| How many checks in this adventure? | **Exactly one** | Only `EVT_115_SERVICE_CORRIDOR` **Failure transformation** names a skill check ("perception check"). |
| Is `EVT_113` careful/rushed a check? | **No** | `17_CHECK_REGISTER.md` § 2; `10` describes pace choice with variant keys, not roll language. |
| Is `EVT_123` "technical check" a `CHK_*`? | **No** | Failure transformation grants `failure_alert` without naming a failed roll. "Without a technical check" describes an observational bypass path, not a `CHK_*` binding. |

### 2.2 Minimum new specification

#### 2.2.1 Check resolution model (adventure-local, D20)

Adopt the model already implied by `engine/01` § 1.2:

1. Player rolls one d20.
2. **Pass** if `roll >= dc`.
3. **Fail** otherwise.
4. No modifiers unless a `CHK_*` record declares a `modifier` field (none in this adventure).
5. Rolling player = the player eligible at the parent `EVT_*` node (`Player 1` for `EVT_115`).
6. Outcome selects the existing `variant_key` (`perception_success` / `perception_failure`). No new routes or grants.

This model does not change gameplay; it names the procedure for outcomes already declared in `10` § 1a.

#### 2.2.2 DC ownership

| Field | Owner |
|---|---|
| `dc` | `17_CHECK_REGISTER.md` — per `CHK_*` record |
| Resolution procedure | This specification § 2.2.1 (adventure convention until `engine/` ch. 11 is authored) |

No engine-global DC table is required for Milestone B.

#### 2.2.3 Prototype DC band table (adventure-local)

Because the repository contains **zero** DC values, one adventure-local band table is the minimum specification needed to complete `CHK_115_PERCEPTION`:

| Band | DC | Use when |
|---|---:|---|
| `routine` | 10 | Single-action physical observation under time pressure in the opening block |
| `challenging` | 14 | Reserved — no `CHK_*` in this adventure |
| `hard` | 18 | Reserved — no `CHK_*` in this adventure |

**Assignment for `CHK_115_PERCEPTION`:** `dc: 10` (`routine`).

**Justification (non-gameplay):** `EVT_115` cost is 15 minutes (`10`), matching `04_TIME_COST_MATRIX.md` § 2 "standard scene search" (15 min). Failure already grants partial success per `07_EVIDENCE_VALIDATION.md` § 5 and `10` **Failure transformation**; any DC 1–19 produces the same graph topology. The band table fixes one integer for compilation without altering pass/fail effects.

#### 2.2.4 Check census rule

A `CHK_*` record is required **if and only if** a node's **Failure transformation** field contains the word `check` referring to a player roll (e.g. "perception check", "failed forensics check").

Excluded by this rule:

- pace choices (`careful` / `rushed` on `EVT_113`);
- implied checks not named in **Failure transformation** (`EVT_123`);
- planning checklists (`13` § 6 Regroup Two);
- narrative constraints ("routine check" in `03_NPC_KNOWLEDGE_AND_DISCLOSURE.md`).

**Completed record after implementation:**

| Field | Value |
|---|---|
| `check_id` | `CHK_115_PERCEPTION` |
| `parent_evt` | `EVT_115_SERVICE_CORRIDOR` |
| `skill` | `perception` |
| `dc` | `10` |
| `pass_variant_key` | `perception_success` |
| `fail_variant_key` | `perception_failure` |
| `fallback_route` | same node; Mina fallback per `10` |

### 2.3 ER-02 validation

| Gate | Result after spec applied |
|---|---|
| **V-CHK** | **PASS** — one `CHK_*` record complete; `EVT_115` cross-reference resolves |

No gameplay change: pass/fail variants and grants are unchanged.

---

## 3. ER-03 — Scene mode per playable node

### 3.1 Repository finding

| Question | Answer | Evidence |
|---|---|---|
| Engine values | `Joint`, `Split`, `Solo` | `engine/05_TWO_PLAYER_SYNCHRONIZATION.md` § 3 |
| Current owner | `10_INVESTIGATION_NODE_GRAPH.md` § 1c | `MILESTONE_B_IMPLEMENTATION_REPORT.md` |
| Why 27 nodes are `UNCLASSIFIED` | No `Players` field; track/role chosen at regroup | `10` § 1c; `13` § 4, § 7 |
| Temporary derivation | `CONTENT_GENERATION_SPEC.md` § 7.2 | Generator convenience only; not logic-authoritative per `ENGINE_READINESS_PLAN.md` ER-03 |

### 3.2 Minimum new specification

#### 3.2.1 Ownership

| Item | Owner |
|---|---|
| `Scene mode` field | `10_INVESTIGATION_NODE_GRAPH.md` § 1c — **explicit per node** |
| Assignment rules | This specification § 3.2.2 |
| `Solo` value | Declared only where § 3.2.2 rule 5 applies |

Scene mode is **explicit**, not runtime-derived. The § 7.2 generator derivation is superseded for logic validation once § 1c is updated per this spec.

#### 3.2.2 Assignment rules (deterministic)

Scene mode describes **canonical two-player booklet routing** for the adventure logic graph. It is not session-state-dependent.

Apply rules in order; first match wins:

| Rule | Condition | `Scene mode` |
|---|---|---|
| 1 | Node has `Players: both` | `Joint` |
| 2 | Node is a terminal `EVT_90x` or `EVT_900_RESOLVE_ENDING` | `Joint` |
| 3 | Node is `EVT_150_REGROUP_ONE` or `EVT_300_REGROUP_TWO` | `Joint` |
| 4 | Node is in `13_SPLIT_AND_REGROUP_FLOW.md` § 2 Player 1 or Player 2 opening branch | `Split` |
| 5 | Node is in `13` § 4 midgame track node sets (any pair A/B/C) | `Split` |
| 6 | Node is in `13` § 7 final-act parallel role node sets | `Split` |
| 7 | Node is `EVT_310`–`EVT_314` or `EVT_330_FIND_SIGNAL_4B` or `EVT_440_FINAL_PUBLIC_POSITION` | `Joint` |
| 8 | `EVT_110_P1_APARTMENT_APPROACH` | `Split` — canonical route per `EVT_100` **Decision** ("canonical two-player route is a split") |

**`Solo` rule:** Use `Solo` only when node text assigns one player to act and the other to observe without receiving separate parallel content. **No node in this adventure satisfies rule 5 of `CONTENT_GENERATION_SPEC.md` § 7.2.** All forty-eight nodes are `Joint` or `Split`.

**Joint-path exception at `EVT_100`:** When players choose "investigate one branch together," the compiler treats P1-branch nodes as `Joint` for **that playthrough's narrative package only**. The logic-layer `Scene mode` in § 1c remains `Split` for P1-branch nodes per rule 4/8. This does not change routes; it is a compile-time delivery override already implied by `EVT_100` **Decision**.

#### 3.2.3 Complete scene mode registry

After applying § 3.2.2, **no node remains `UNCLASSIFIED`:**

| Node | `Scene mode` | Rule |
|---|---|---|
| `EVT_100_SHARED_BRIEFING` | `Joint` | 1 |
| `EVT_110_P1_APARTMENT_APPROACH` | `Split` | 8 |
| `EVT_111_MINA_FIRST_CONTACT` | `Split` | 4 |
| `EVT_112_RESTRICTED_APARTMENT` | `Split` | 4 |
| `EVT_113_APARTMENT_SEARCH` | `Split` | 4 |
| `EVT_114_NEIGHBOUR_INTERVIEW` | `Split` | 4 |
| `EVT_115_SERVICE_CORRIDOR` | `Split` | 4 |
| `EVT_120_P2_NEWSROOM_ENTRY` | `Split` | 4 |
| `EVT_121_NADIA_INTERVIEW` | `Split` | 4 |
| `EVT_122_MARCUS_OBSERVATION` | `Split` | 4 |
| `EVT_123_NEWSROOM_RECORDS` | `Split` | 4 |
| `EVT_150_REGROUP_ONE` | `Joint` | 3 |
| `EVT_210_HARBOR_ARCHIVE_ENTRY` | `Split` | 5 |
| `EVT_211_CAFE_ORPHEUS` | `Split` | 5 |
| `EVT_212_TERMINAL_RECON` | `Split` | 5 |
| `EVT_220_MINA_REPORT_COMPARISON` | `Split` | 5 |
| `EVT_221_CAMERA_REQUEST_AUDIT` | `Split` | 5 |
| `EVT_222_PROTECTION_ORDER_AUDIT` | `Split` | 5 |
| `EVT_223_ROOK_INTERVIEW` | `Split` | 5 |
| `EVT_230_IRIS_WORKPLACE` | `Split` | 5 |
| `EVT_231_PREPAID_PHONE_TRACE` | `Split` | 5 |
| `EVT_232_MEDICAL_INTERPRETATION` | `Split` | 5 |
| `EVT_240_MARCUS_PRESSURE_STAGE_ONE` | `Split` | 5 |
| `EVT_241_MARCUS_FULL_DISCLOSURE` | `Split` | 5 |
| `EVT_242_REED_OFFICE_SEARCH` | `Split` | 5 |
| `EVT_243_REED_NEGOTIATION` | `Split` | 5 |
| `EVT_300_REGROUP_TWO` | `Joint` | 3 |
| `EVT_310_CABLE_CORRIDOR_ENTRY` | `Joint` | 7 |
| `EVT_311_NORTH_GATE_ENTRY` | `Joint` | 7 |
| `EVT_312_DRAINAGE_ENTRY` | `Joint` | 7 |
| `EVT_313_EMERGENCY_ENTRY` | `Joint` | 7 |
| `EVT_314_MAIN_ENTRY_CONFRONTATION` | `Joint` | 7 |
| `EVT_330_FIND_SIGNAL_4B` | `Joint` | 7 |
| `EVT_331_LENA_IRIS_NEGOTIATION` | `Split` | 6 |
| `EVT_400_RESCUE_CONTROL` | `Split` | 6 |
| `EVT_410_LEDGER_RECOVERY` | `Split` | 6 |
| `EVT_420_REED_OR_ROOK_CONFRONTATION` | `Split` | 6 |
| `EVT_430_COMPLETE_TRANSFER` | `Split` | 6 |
| `EVT_440_FINAL_PUBLIC_POSITION` | `Joint` | 7 |
| `EVT_900_RESOLVE_ENDING` | `Joint` | 2 |
| `EVT_901`–`EVT_908` | `Joint` | 2 |

**Summary:** 15 `Joint`, 33 `Split`, 0 `Solo`, 0 `UNCLASSIFIED`.

§ 5 midgame node sets (rule 5): `{210,211,212}`, `{220,221,222,223}`, `{230,231,232}`, `{240,241,242,243}`.

§ 7 final-act node sets (rule 6): `{331}`, `{400}`, `{410}`, `{420}`, `{430}` per role-pair patterns in `13` § 7.

### 3.3 ER-03 validation

| Gate | Result after spec applied |
|---|---|
| **V-SM** | **PASS** — every `EVT_*` declares exactly one `Scene mode` |

No gameplay change: modes classify existing delivery structure only.

---

## 4. ER-04 — Split-branch terminators

### 4.1 Repository finding

| Question | Answer | Evidence |
|---|---|---|
| Closed terminator set | `REJOIN`, `REMOTE_CONTACT`, `WAIT_UNTIL_SYNC`, `EMERGENCY_INTERRUPT`, `TERMINAL_OUTCOME` | `engine/05` § 5 |
| Current owner | `10_INVESTIGATION_NODE_GRAPH.md` § 1d | Milestone B implementation |
| Midgame blocked | Terminators tied to unresolved `Scene mode` | `MILESTONE_B_IMPLEMENTATION_REPORT.md` § 6 |

### 4.2 Minimum new specification

#### 4.2.1 Ownership

| Item | Owner |
|---|---|
| Per-node `Split terminator` | `10_INVESTIGATION_NODE_GRAPH.md` § 1d — **explicit where applicable** |
| Window-level communication | `13_SPLIT_AND_REGROUP_FLOW.md` § 5 (not a per-node terminator) |
| Assignment rules | This specification § 4.2.2 |

Terminators are **derived by rule** from `Scene mode` + `Outgoing`, then **written explicitly** to § 1d. They are not player choices.

#### 4.2.2 Assignment rules

Apply only when `Scene mode` = `Split`:

| Rule | Condition | `Split terminator` | `Regroup target` |
|---|---|---|---|
| T1 | `Outgoing` includes `EVT_150_REGROUP_ONE` | `REJOIN` | `EVT_150_REGROUP_ONE` |
| T2 | `Outgoing` includes `EVT_300_REGROUP_TWO` | `REJOIN` | `EVT_300_REGROUP_TWO` |
| T3 | `Outgoing` includes `EVT_900_RESOLVE_ENDING` or `EVT_440_FINAL_PUBLIC_POSITION` without a nearer regroup in `Outgoing` | `REJOIN` | first listed convergence target among `{EVT_440, EVT_900}` in `Outgoing` |
| T4 | `NODE_TYPE` = `TERMINAL` | `TERMINAL_OUTCOME` | — |
| T5 | Split node with no regroup/convergence target in `Outgoing` (in-window continuation) | *(omit field)* | — |

**When to use other terminators:**

| Terminator | When |
|---|---|
| `REMOTE_CONTACT` | Not a per-node field. Invoked as a **window-level action** during any split window per `08` § 4 / `13` § 5 (phone, message). |
| `WAIT_UNTIL_SYNC` | Not a per-node field. Invoked when a player elects to wait for the regroup clock trigger (`13` § 2: ~21:30; `13` § 6: deadline 23:15) without taking another node. |
| `EMERGENCY_INTERRUPT` | Only on nodes that declare emergency-broadcast effects in **State changes** during a split window. **No such node exists** in the current graph. |
| `TERMINAL_OUTCOME` | Terminal nodes only (rule T4). |

#### 4.2.3 Derived terminator table (all `Split` nodes)

| Node | `Split terminator` | `Regroup target` | Rule |
|---|---|---|---|
| `EVT_110` | — | — | T5 (in-window) |
| `EVT_111` | — | — | T5 |
| `EVT_112` | `REJOIN` | `EVT_150` | T1 |
| `EVT_113` | `REJOIN` | `EVT_150` | T1 |
| `EVT_114` | `REJOIN` | `EVT_150` | T1 |
| `EVT_115` | `REJOIN` | `EVT_150` | T1 |
| `EVT_120` | — | — | T5 |
| `EVT_121` | `REJOIN` | `EVT_150` | T1 |
| `EVT_122` | `REJOIN` | `EVT_150` | T1 |
| `EVT_123` | `REJOIN` | `EVT_150` | T1 |
| `EVT_210`–`EVT_212` | `REJOIN` | `EVT_300` | T2 |
| `EVT_220`–`EVT_223` | `REJOIN` | `EVT_300` | T2 |
| `EVT_230`–`EVT_232` | `REJOIN` | `EVT_300` | T2 |
| `EVT_240`–`EVT_243` | `REJOIN` | `EVT_300` | T2 |
| `EVT_331` | `REJOIN` | `EVT_900` or peer per `Outgoing` | T3 |
| `EVT_400` | `REJOIN` | `EVT_440` or `EVT_900` per `Outgoing` | T3 |
| `EVT_410` | `REJOIN` | `EVT_440` or `EVT_900` per `Outgoing` | T3 |
| `EVT_420` | `REJOIN` | `EVT_440` or `EVT_900` per `Outgoing` | T3 |
| `EVT_430` | `REJOIN` | `EVT_440` or `EVT_900` per `Outgoing` | T3 |

`Joint` nodes do not declare `Split terminator`.

### 4.3 ER-04 validation

| Gate | Result after spec applied |
|---|---|
| **V-ST** | **PASS** — every `Split` branch exit that reaches a regroup or convergence declares a terminator |

No gameplay change: terminators name existing regroup/convergence edges.

---

## 5. ER-05 — Synchronization windows

### 5.1 Repository finding

| Question | Answer | Evidence |
|---|---|---|
| Conflict | `04` § 3 example permits chained action; `engine/05` § 4 forbids unless explicit option | `04` § 3b |
| Missing max durations | No per-window caps declared | `04` § 3a; `MILESTONE_B_IMPLEMENTATION_REPORT.md` |
| `engine/05` § 9 (10–30 min) | Prototype guidance | Appears to contradict Split One ~80 min span |
| Pacing blocks | Four blocks with clock ranges | `04` § 5 |

### 5.2 Minimum new specification

#### 5.2.1 Ownership

| Item | Owner |
|---|---|
| Synchronization window table | `04_TIME_COST_MATRIX.md` § 3a (adventure timing authority) |
| Window triggers and deadlines | `13_SPLIT_AND_REGROUP_FLOW.md` § 2, § 6 (cross-reference) |
| Leftover-time rule | `engine/05_TWO_PLAYER_SYNCHRONIZATION.md` § 4 — **authoritative** |
| `04` § 3 example | **Superseded** for action permission; retained only as clock-alignment illustration |

#### 5.2.2 Maximum duration — authoritative rule

**Maximum window duration** = clock span from window start to the **earliest** of:

1. the regroup trigger time declared in `13`; or
2. the regroup deadline declared in `13` / node **Deadline** fields.

**Window start times** (derived from existing pacing, not invented):

| Window | Start | End (earliest of) | **Maximum duration** |
|---|---|---|---|
| Split One | `20:10` (`EVT_100` complete) | `21:30` (`13` § 2 regroup trigger) | **80 minutes** |
| Split Two | `21:40` (end of Regroup One availability window per `08` § 5) | `23:15` (`13` § 6 deadline) | **95 minutes** |
| Final-act parallel | `23:15` (`EVT_300` complete) | `02:00` (`04` § 5 block 4 end) | **165 minutes** |

**`engine/05` § 9 reinterpretation:** The "10–30 world minutes" cap applies to a **single player action cost** within a window (consistent with `04` § 2 action costs), not to the full macro split phase. Macro window spans are governed by `04` § 5 pacing blocks. No conflict once scoped correctly.

#### 5.2.3 Leftover-time rule — single authoritative rule

**Authoritative rule** (`engine/05` § 4):

> The shorter action does not allow unlimited extra actions. Any remaining time is resolved only through explicitly offered waiting, preparation, travel, or communication options.

**Explicit leftover-time options** (closed set from existing docs):

| Option | Cost | Source |
|---|---|---|
| Phone call | 5 min | `08` § 4, `13` § 5 |
| Text message | 1 clue transfer; delayed delivery | `13` § 5 |
| Physical regroup (early) | 10 min | `08` § 4 |
| Wait for sync clock | 0 min action; advance to trigger/deadline | `13` § 2, § 6 |
| Emergency broadcast | immediate; awareness cost | `08` § 4, `13` § 5 |

**Superseded text:** `04` § 3 bullet "Player 1 may take another action that ends no later than 21:25" is **not** permission to take an additional investigation node. It illustrates clock alignment only. Implementation must add a footnote in `04` § 3 when applied.

### 5.3 ER-05 validation

| Gate | Result after spec applied |
|---|---|
| **V8** | **PASS** — each window has start, maximum duration, and one leftover-time rule |

No gameplay change: caps and rule codify existing pacing blocks and engine authority.

---

## 6. ER-09 — Participation audit

### 6.1 Repository finding

| Question | Answer | Evidence |
|---|---|---|
| Required fields | decisions, clues, challenges, waiting, final-act responsibility per player | `08` § 9; `13` § 9 |
| Partially populated | Opening / regroup only | `MILESTONE_B_IMPLEMENTATION_REPORT.md` |
| Blocked | Midgame track binding; waiting time; role assignment | Same |

### 6.2 Minimum new specification

#### 6.2.1 Ownership

| Item | Owner |
|---|---|
| Audit requirements | `08_TWO_PLAYER_CORE_RULES.md` § 9 |
| Computed audit table | `13_SPLIT_AND_REGROUP_FLOW.md` § 9 |
| Calculation rules | This specification § 6.2.2 |
| Player attribution | Canonical pair assignments in `13` § 4 |

#### 6.2.2 Required fields and calculation

Audit is computed for **five blocks**: Opening/Split One, Regroup One, Midgame/Split Two, Regroup Two, Final act.

**Player attribution:**

| Block | P1 node set | P2 node set | Source |
|---|---|---|---|
| Opening | `EVT_111`–`EVT_115` | `EVT_121`, `EVT_123` (and `120`/`122` transit) | `13` § 2 |
| Midgame | Per `13` § 4 Pair **A** (canonical audit reference) | Per Pair **A** | `13` § 4 |
| Final act | Role **A** nodes from chosen pair at `EVT_300` | Role **B** nodes | `13` § 7 |

**Pair A midgame attribution** (deterministic reference path):

- P1: `EVT_220`, `EVT_221`, `EVT_222`, `EVT_223`
- P2: `EVT_210`, `EVT_211`, `EVT_212`

**Final-act role mapping** (from `13` § 7; player chooses pair at `EVT_300`):

| Role pair pattern | Role A nodes | Role B nodes |
|---|---|---|
| Rescue / Evidence | `EVT_400` | `EVT_410` |
| Interior / Exterior | `EVT_331` | `EVT_420` |
| Proof / Protection | `EVT_430` | `EVT_400` |

Audit reports **one row per final-act pair pattern** (three rows). Gate passes if each pattern satisfies `13` § 7 parity requirements.

**Field calculations:**

| Field | Method |
|---|---|
| Decisions per player | Count nodes in player set with `Decision`, `Core decision`, `Approach outcomes`, `Routes`, or `Branch choice` fields |
| Unique clues per player | Count distinct `ACTIVE` `CLUE_*` in `12` granted at nodes in player set (max along any valid path) |
| Social challenges | Count approach-choice nodes (`EVT_111`, `EVT_121`, `EVT_243` leverage levels count as 1 decision not a check) |
| Technical challenges | Count `CHK_*` with `skill` in `{digital, technical, computer}` → **0** in this adventure |
| Physical challenges | Count `CHK_*` with `skill: perception` on player's nodes → P1: **1** (`CHK_115`); P2: **0** |
| Communication opportunities | Count legal modes available in block per `08` § 4 / `13` § 5 |
| Final-act responsibility | Role A / Role B label from `13` § 7 for the pattern being audited |

**Waiting-time calculation (deterministic):**

```
waiting_minutes(player, block) =
  Σ max(0, partner_available_at − player_available_at)
```

Summed over each completed node in the block, where:

- `player_available_at` = `CLOCK` after player's node **Cost** (cumulative along path);
- `partner_available_at` = partner's cumulative clock at the same wall-clock checkpoint;
- For `Joint` blocks (regroup): waiting = **0**.

**Inactive reading time** = `waiting_minutes` during `Split` blocks (non-acting player has no node to execute). **0** during `Joint` blocks.

#### 6.2.3 Reference audit values (Pair A; opening max path)

| Block | P1 decisions | P2 decisions | P1 clues (max) | P2 clues (max) | P1 waiting | P2 waiting |
|---|---:|---:|---:|---:|---:|---:|
| Opening | 3–8 | 2–5 | 4 | 5 | derived | derived |
| Regroup One | 1 (joint) | 1 (joint) | 0 | 0 | 0 | 0 |
| Midgame (Pair A) | 4 | 3 | 6+ | 5+ | derived | derived |
| Regroup Two | 1 (joint) | 1 (joint) | 0 | 0 | 0 | 0 |
| Final act (per pattern) | per role A set | per role B set | per `12` grants | per `12` grants | derived | derived |

Exact waiting integers are **computed**, not authored — removing the "no per-block values" blocker.

### 6.3 ER-09 validation

| Gate | Result after spec applied |
|---|---|
| **Participation gate** (A6) | **PASS** — all five blocks have deterministic calculation rules and reference values |

No gameplay change: audit counts existing nodes and grants.

---

## 7. ER-10 — Solo play mode

### 7.1 Repository finding

| Source | Statement |
|---|---|
| `engine/06_PROTOTYPE_SCOPE_AND_VALIDATION.md` § 1 | Prototype must support one-player and two-player mode |
| `PROTOTYPE_BRIEF.md` | "playable solo or cooperatively" |
| `IMPLEMENTATION_PLAN.md` § 15 | Solo mode **out of scope** for Alpha 0.2c logic revision |
| `ENGINE_READINESS_PLAN.md` C6 | ER-10 resolved **or** `play_modes: [two_player]` with documented engine exception |
| `MILESTONE_B_IMPLEMENTATION_REPORT.md` | `play_modes: [two_player]` already declared; solo graph absent |
| `README.md` | `Players: 2`; `play_modes: two_player` |

### 7.2 Decision: Option A — Permanent out of scope for Alpha 0.2c

**Recommend Option A** (scoped out for this release, not permanent for the engine).

**Justification:**

1. **`IMPLEMENTATION_PLAN.md` § 1.1** targets **Prototype Alpha 0.2c** as a logic revision, not a solo authoring pass. § 15 explicitly lists solo as out of scope.
2. **`ENGINE_READINESS_PLAN.md` C6** provides an approved resolution path: declare `play_modes: [two_player]` with a documented engine exception. Milestone B already took this path.
3. **Solo requires new routing rules** (merged-player graph, role collapse, `EVT_908` exclusion) that do not exist in logic. Authoring them would be gameplay design, violating the constraint not to invent routes.
4. **`PROTOTYPE_BRIEF.md` production sequence** step 6 ("Build solo and two-player adventure logic") follows logic revision and compilation — solo is a **later production phase**, not Alpha 0.2c.
5. **`engine/06` § 1** remains the long-term engine goal; Option A defers implementation, not the engine requirement.
6. **Two-player is the primary validation path** per `ENGINE_READINESS_PLAN.md` ER-10 priority (Medium; deferrable for two-player-only release).

Option B (required now) would demand a solo reachability graph, player-merge rules, and artifact set none of which can be derived without inventing routes.

### 7.3 Minimum new specification (Option A)

| Item | Specification |
|---|---|
| `play_modes` | `[two_player]` in `adventures/The_Last_Witness/README.md` |
| Engine exception | Document in `10` § 18: solo deferred to post–Alpha 0.2c per `IMPLEMENTATION_PLAN.md` § 15; `engine/06` § 1 remains future requirement |
| `EVT_908` | Reachable only in `two_player` mode; excluded from solo artifacts when solo is implemented |
| `V5` reachability | Evaluated for `two_player` only until solo graph is authored |
| Milestone B ER-10 status | **Resolved by scope declaration** — not blocked |

### 7.4 ER-10 validation

| Gate | Result after spec applied |
|---|---|
| **ER-10 / C6** | **PASS** — `play_modes: [two_player]` with documented engine exception |

No gameplay change: affirms existing two-player-only declaration.

---

## 8. Validation summary

| Blocker | Gate | Current | After this spec | Gameplay change required? |
|---|---|---|---|---|
| ER-02 | V-CHK | BLOCKED | **PASS** | No |
| ER-03 | V-SM | FAIL | **PASS** | No |
| ER-04 | V-ST | PARTIAL | **PASS** | No |
| ER-05 | V8 | BLOCKED | **PASS** | No |
| ER-09 | Participation (A6) | PARTIAL | **PASS** | No |
| ER-10 | C6 | BLOCKED | **PASS** | No |

**Milestone A regression:** V1–V7, V9–V11 remain **PASS** — this spec adds metadata rules only.

---

## 9. Implementation handoff

When Milestone B is completed per this specification, update **only** these files (no route or grant changes):

| File | Changes |
|---|---|
| `17_CHECK_REGISTER.md` | Set `dc: 10` on `CHK_115_PERCEPTION`; mark compilation unblocked |
| `10_INVESTIGATION_NODE_GRAPH.md` | Replace § 1c/§ 1d per § 3.2.3 and § 4.2.3; add `04` § 3 footnote cross-reference |
| `04_TIME_COST_MATRIX.md` | Populate § 3a durations; add § 3b authoritative rule; footnote § 3 example |
| `13_SPLIT_AND_REGROUP_FLOW.md` | Populate sync window durations; complete § 9 audit table |
| `08_TWO_PLAYER_CORE_RULES.md` | Reference § 6.2 calculation rules in § 9 |
| `README.md` | Confirm `play_modes: [two_player]` and exception pointer |

**Do not implement in this task.** This document is the specification only.

---

## 10. Document control

| Field | Value |
|---|---|
| Version | 1.0 |
| Depends on | `IMPLEMENTATION_PLAN.md`, `ENGINE_READINESS_PLAN.md`, `MILESTONE_B_IMPLEMENTATION_REPORT.md` |
| Resolves | ER-02, ER-03, ER-04, ER-05, ER-09, ER-10 remaining blockers |
| Does not resolve | ER-08 (already complete), Milestones C–F |
