> **SUPERSEDED.** Pre-approval design options only. Authoritative decisions: approved MBD-01–06 and `MILESTONE_B_IMPLEMENTATION_V2_REPORT.md`.

# Milestone B Design Decision Packet

**Document type:** Owner approval packet (design decisions only)  
**Status:** Proposed — **not approved**  
**Scope:** Consolidates Classification **B** rules from the audit of `MILESTONE_B_COMPLETION_SPEC.md`  
**Does not modify:** any repository file, route, clue, grant, threshold, or ending

**Inputs:**

- `ENGINE_READINESS_PLAN.md`
- `MILESTONE_B_IMPLEMENTATION_REPORT.md`
- `MILESTONE_B_COMPLETION_SPEC.md`
- Classification audit (38 rules **A**, 42 rules **B**)

Classification **A** facts are preserved below as authoritative context only. Classification **B** rules are **not approved** until an owner selects an option in this packet.

---

## MBD-01 — Check Resolution Model

### 1. Decision ID and title

**MBD-01 — Check Resolution Model**

### 2. Blockers resolved

| Item | Gate |
|---|---|
| ER-02 | V-CHK |
| ER-09 (partial) | Participation gate A6 — physical-challenge count |

### 3. Existing authoritative facts (Classification A)

| Fact | Source |
|---|---|
| First reference implementation expects a D20-based resolution system | `engine/01_INTRODUCTION_AND_SCOPE.md` § 1.2 |
| `CHK_*` records are adventure-local; owned by `17_CHECK_REGISTER.md` | `ENGINE_READINESS_PLAN.md` ER-02; `00_ENTITY_KEY_TABLE.md` |
| Exactly one roll-named check: perception on `EVT_115` | `10_INVESTIGATION_NODE_GRAPH.md` `EVT_115` **Failure transformation** |
| Pass/fail outcomes already exist as `perception_success` / `perception_failure` variant keys | `10` § 1a **Variants** |
| Failure grants partial success; Mina fallback | `10` **Failure transformation**; `07_EVIDENCE_VALIDATION.md` § 5 |
| `EVT_113` careful/rushed is not a check; `EVT_123` has no `CHK_*` binding | `17_CHECK_REGISTER.md` § 2 |
| Check census: only **Failure transformation** roll-language creates `CHK_*` | `17_CHECK_REGISTER.md` § 2 |
| No `dc` value exists in repository | `17_CHECK_REGISTER.md` § 3; `MILESTONE_B_IMPLEMENTATION_REPORT.md` § 6 |
| Engine ch. 11 (Decisions and checks) not authored | `engine/README.md` |

### 4. Conflict or missing rule

`engine/01` § 1.2 names D20 but does not define roll procedure, pass/fail comparison, modifiers, rolling-player assignment, or DC scale. `BOOK_COMPILER_SPEC.md` MS-04 requires `CHK_*` with DC and pass/fail text before check branches compile. Without an approved procedure and DC, `CHK_115_PERCEPTION` cannot complete and V-CHK remains blocked.

### 5. Available options

#### Option A — Minimal adventure-local D20 (single check)

| Dimension | Detail |
|---|---|
| **Behavior** | One d20 roll; pass if `roll >= dc`; no modifiers; rolling player = P1 (apartment branch); `dc: 10` on `CHK_115_PERCEPTION`; three-band table (10/14/18) reserved for future checks |
| **Gameplay** | Adds probability to an outcome that is already pass/fail-bifurcated in logic; graph topology unchanged |
| **Compiler** | Emits one check instruction; unblocks V-CHK |
| **Authoring** | One player-facing roll instruction at `EVT_115` |
| **Validation** | V-CHK PASS; physical challenge count = 1 for P1 |
| **Files** | `17_CHECK_REGISTER.md`; `10` `EVT_115` cross-reference (no grant changes) |

#### Option B — Variant-only (no roll)

| Dimension | Detail |
|---|---|
| **Behavior** | Remove roll requirement; `perception_success` / `perception_failure` selected by player choice or automatic branch; no `dc` field |
| **Gameplay** | **Changes** fair-play randomness expectation from `engine/01` § 1.2 |
| **Compiler** | Check instruction omitted; V-CHK may FAIL or require gate exception |
| **Authoring** | No roll prose |
| **Validation** | Conflicts with D20 expectation |
| **Files** | `17_CHECK_REGISTER.md`; possibly `ENGINE_READINESS_PLAN.md` exception note |

#### Option C — Defer checks to post–Alpha 0.2c

| Dimension | Detail |
|---|---|
| **Behavior** | Leave `CHK_115_PERCEPTION` blocked; compiler treats check branch as blocked per `BOOK_COMPILER_SPEC.md` § 4.4 |
| **Gameplay** | None at compile time |
| **Compiler** | Check-gated branch remains blocked |
| **Authoring** | No check prose until later milestone |
| **Validation** | V-CHK remains BLOCKED; Milestone B incomplete |
| **Files** | None |

### 6. Recommended option

**Option A — Minimal adventure-local D20 (single check).**

> **This is a new design decision, not an existing repository rule.**

Rationale: smallest scope (one `CHK_*`, one DC); preserves existing variant keys and grants; satisfies `engine/01` D20 expectation; unblocks V-CHK without new routes.

### 7. Dependent rules (Classification B resolved by Option A)

- D20 single-roll procedure
- Pass if `roll >= dc`
- No modifiers unless declared on `CHK_*`
- Rolling player = eligible player at parent `EVT_*`
- Prototype DC band table (10 / 14 / 18)
- `routine` band assignment rule
- `CHK_115_PERCEPTION` `dc: 10`
- Physical-challenge audit mapping to `CHK_*` perception (with MBD-05)

---

## MBD-02 — Scene Mode and Player Assignment

### 1. Decision ID and title

**MBD-02 — Scene Mode and Player Assignment**

### 2. Blockers resolved

| Item | Gate |
|---|---|
| ER-03 | V-SM |
| ER-04 (partial) | V-ST — prerequisite for terminator derivation |
| ER-09 (partial) | A6 — player attribution |

### 3. Existing authoritative facts (Classification A)

| Fact | Source |
|---|---|
| Engine values: `Joint`, `Split`, `Solo` | `engine/05_TWO_PLAYER_SYNCHRONIZATION.md` § 3 |
| `Players: both` → joint delivery | `CONTENT_GENERATION_SPEC.md` § 7.2 |
| Opening P1/P2 branches | `13_SPLIT_AND_REGROUP_FLOW.md` § 2 |
| Midgame tracks in Pairs A/B/C | `13` § 4 |
| Final-act parallel role pairs | `13` § 7; `08_TWO_PLAYER_CORE_RULES.md` § 6 |
| Canonical two-player route is split at `EVT_100` | `10` `EVT_100` **Decision** |
| Logic should own explicit scene mode (derivation temporary) | `ENGINE_READINESS_PLAN.md` ER-03 |
| 27 nodes currently `UNCLASSIFIED` | `10` § 1c; `MILESTONE_B_IMPLEMENTATION_REPORT.md` |
| Regroup and terminal nodes are collective | `10` § 14; `ARC_170` / `ARC_270` |

### 4. Conflict or missing rule

Scene mode must be declared on every `EVT_*` (`ENGINE_READINESS_PLAN.md` ER-03), but most nodes lack a `Players` field. `EVT_100` allows joint investigation; `13` § 4 recommends but does not mandate pairings. `08` § 6 describes parallel enter/secure roles at Signal Room without binding `EVT_330`–`EVT_440`. The repository cannot determine whether scene mode is **fixed per node** or **session-selected**, nor how to classify terminal-access and final-act nodes.

### 5. Available options

#### Option A — Fixed canonical two-player routing (metadata only)

| Dimension | Detail |
|---|---|
| **Behavior** | Each node gets one fixed `Scene mode` for the canonical split structure: opening/midgame/final-parallel = `Split`; regroup/terminals/accusation dispatch = `Joint`; `EVT_110` = `Split`; `EVT_310`–`314`, `EVT_330`, `EVT_440` = `Joint`; `EVT_100` joint-path = compile-time `Joint` override on P1 nodes only |
| **Gameplay** | **No route change.** Player freedom at `EVT_100` / `EVT_150` / `EVT_300` unchanged; mode labels booklet delivery |
| **Compiler** | Stable per-node `scene_mode`; V-SM PASS |
| **Authoring** | Split vs joint prose routing deterministic |
| **Validation** | V-SM PASS; enables MBD-03 terminator rules |
| **Files** | `10` § 1c (replace `UNCLASSIFIED` rows); `CONTENT_GENERATION_SPEC.md` § 7.2 cross-ref note |

#### Option B — Session-parameterized scene mode

| Dimension | Detail |
|---|---|
| **Behavior** | `Scene mode` computed at compile/play from regroup choices (pair A/B/C, role pattern, `EVT_100` joint vs split) |
| **Gameplay** | Same routes; mode varies per playthrough |
| **Compiler** | Requires mode variants per node per session path — large surface |
| **Authoring** | Multiple narrative packages per node |
| **Validation** | V-SM requires variant matrix; high complexity |
| **Files** | `10`; new session-state register; generator/compiler contract |

#### Option C — Defer unclassified nodes

| Dimension | Detail |
|---|---|
| **Behavior** | Keep 27 `UNCLASSIFIED`; only classify nodes with `Players` field |
| **Gameplay** | None |
| **Compiler** | Split packaging for midgame/final blocked |
| **Authoring** | Blocked |
| **Validation** | V-SM FAIL; Milestone B incomplete |
| **Files** | None |

### 6. Recommended option

**Option A — Fixed canonical two-player routing (metadata only).**

> **This is a new design decision, not an existing repository rule.**

Rationale: completes V-SM with no route edits; distinguishes metadata (fixed canonical mode) from player freedom (unchanged regroup choices); minimal Alpha 0.2c scope; `Joint` assignment for terminal-access nodes matches joint route selection at `EVT_300`.

### 7. Dependent rules (Classification B resolved by Option A)

- Scene mode = canonical two-player booklet routing, not session state
- Ordered first-match assignment rule list
- Rule 7: `EVT_310`–`314`, `EVT_330`, `EVT_440` → `Joint`
- `EVT_100` joint-path compile-time `Joint` override; logic-layer `Split` on P1-branch nodes
- All § 3.2.3 per-node assignments that depend on Rule 7
- Enables MBD-03 terminator derivation from fixed `Scene mode`

---

## MBD-03 — Split Termination

### 1. Decision ID and title

**MBD-03 — Split Termination**

### 2. Blockers resolved

| Item | Gate |
|---|---|
| ER-04 | V-ST |

### 3. Existing authoritative facts (Classification A)

| Fact | Source |
|---|---|
| Closed terminator set: `REJOIN`, `REMOTE_CONTACT`, `WAIT_UNTIL_SYNC`, `EMERGENCY_INTERRUPT`, `TERMINAL_OUTCOME` | `engine/05_TWO_PLAYER_SYNCHRONIZATION.md` § 5 |
| `REJOIN` default toward named regroup when split ends | `CONTENT_GENERATION_SPEC.md` § 7.3 |
| Opening split exits with `EVT_150` in `Outgoing` → `REJOIN` | `10` § 1d; `13` § 2 |
| Midgame nodes exit with `EVT_300` in `Outgoing` | `10` midgame `Outgoing` |
| `REMOTE_CONTACT` is communication during split, not graph edge | `08` § 4; `13` § 5; `10` § 1d |
| In-window nodes (`EVT_111`, `EVT_120`) omit terminator until branch exit | `10` § 1d |
| `TERMINAL` nodes → `TERMINAL_OUTCOME` | `engine/05` § 5 |
| Terminator owner: `10` § 1d | `ENGINE_READINESS_PLAN.md` ER-04 |

### 4. Conflict or missing rule

Midgame and final-act terminators were blocked pending scene mode (`MILESTONE_B_IMPLEMENTATION_REPORT.md`). No rule defines: (1) convergence when `Outgoing` lists both `EVT_440` and `EVT_900`; (2) when `WAIT_UNTIL_SYNC` is invoked; (3) `EMERGENCY_INTERRUPT` binding; (4) whether terminators are authored explicitly or derived by algorithm.

### 5. Available options

#### Option A — Explicit `REJOIN` table + window-level optional actions

| Dimension | Detail |
|---|---|
| **Behavior** | Author explicit `Split terminator` + `Regroup target` in `10` § 1d for every `Split` node with regroup/convergence in `Outgoing`. `REJOIN` → `EVT_150` or `EVT_300` by `Outgoing`. Final-act `Split` nodes: `REJOIN` → **both** `EVT_440` and `EVT_900` listed (no priority). `WAIT_UNTIL_SYNC` / `EMERGENCY_INTERRUPT` are **window-level player actions** per `08`/`13`, not per-node fields. In-window nodes omit terminator (T5). |
| **Gameplay** | None — names existing edges |
| **Compiler** | V-ST PASS without inventing convergence priority |
| **Authoring** | Regroup/convergence instructions cite listed targets |
| **Validation** | V-ST PASS |
| **Files** | `10` § 1d; `13` § 5 cross-ref for window actions |

#### Option B — Derived terminators with `Outgoing` order priority

| Dimension | Detail |
|---|---|
| **Behavior** | Algorithm derives terminator from `Scene mode` + `Outgoing`; when multiple convergence targets, **first listed** in `Outgoing` wins |
| **Gameplay** | **Could change** which convergence is authoritative if order is wrong |
| **Compiler** | Fully automatic |
| **Authoring** | Depends on edge list order |
| **Validation** | V-ST PASS but order sensitivity risk |
| **Files** | `10` § 1d; derivation spec in logic conventions |

#### Option C — Defer final-act terminators

| Dimension | Detail |
|---|---|
| **Behavior** | Opening `REJOIN` only; final-act `Split` nodes omit terminators |
| **Gameplay** | None |
| **Compiler** | Final-act split validation incomplete |
| **Validation** | V-ST PARTIAL |
| **Files** | `10` § 1d partial |

### 6. Recommended option

**Option A — Explicit `REJOIN` table + window-level optional actions.**

> **This is a new design decision, not an existing repository rule.**

Rationale: avoids inferring convergence priority from `Outgoing` order; uses closed engine set without inventing per-node `WAIT_UNTIL_SYNC`/`EMERGENCY_INTERRUPT`; completes V-ST when combined with MBD-02 Option A.

### 7. Dependent rules (Classification B resolved by Option A)

- Terminator derivation algorithm (replaced by explicit table)
- T3 first-listed convergence priority (rejected)
- `WAIT_UNTIL_SYNC` as player wait-for-clock window action (with MBD-04)
- `EMERGENCY_INTERRUPT` only via window-level emergency broadcast (no per-node binding)
- § 4.2.3 rows using T3 (`EVT_331`, `EVT_400`–`430`) — replaced by dual-target `REJOIN`

---

## MBD-04 — Synchronization and Time

### 1. Decision ID and title

**MBD-04 — Synchronization and Time**

### 2. Blockers resolved

| Item | Gate |
|---|---|
| ER-05 | V8 |
| ER-09 (partial) | A6 — waiting-time formula inputs |

### 3. Existing authoritative facts (Classification A)

| Fact | Source |
|---|---|
| Split windows need start, max duration, leftover-time rule | `engine/05_TWO_PLAYER_SYNCHRONIZATION.md` § 4 |
| Shorter action does not allow unlimited extra actions | `engine/05` § 4 |
| Split One regroup trigger ~21:30 | `13_SPLIT_AND_REGROUP_FLOW.md` § 2 |
| Regroup One window 21:20–21:40 | `08_TWO_PLAYER_CORE_RULES.md` § 5 |
| Regroup Two deadline 23:15 | `13` § 6; `10` `EVT_300` **Deadline** |
| Pacing blocks: 20:00–21:30, 21:30–23:00, 23:00–00:30, 00:30–02:00 | `04_TIME_COST_MATRIX.md` § 5 |
| `EVT_100` ends ~20:10 (10 min from 20:00) | `10` `EVT_100` **Cost** |
| Leftover options: phone 5 min, regroup 10 min, message, emergency broadcast | `08` § 4; `13` § 5; `04` § 2 |
| **Conflict:** `04` § 3 example permits chained action before slower player ends | `04_TIME_COST_MATRIX.md` § 3 |
| **Conflict:** `engine/05` § 9 caps split windows at 10–30 min | `engine/05_TWO_PLAYER_SYNCHRONIZATION.md` § 9 |
| V8 BLOCKED on conflict + missing max durations | `04` § 3b; `MILESTONE_B_IMPLEMENTATION_REPORT.md` |

### 4. Conflict or missing rule

Three contradictions/missing pieces: (1) `04` § 3 vs `engine/05` § 4 on leftover actions; (2) `engine/05` § 9 (10–30 min) vs adventure macro phases (~80+ min Split One); (3) no formula for maximum window duration or Split Two / final-act window boundaries.

### 5. Available options

#### Option A — Adventure pacing authoritative; engine § 9 scoped to per-action

| Dimension | Detail |
|---|---|
| **Behavior** | **Leftover-time:** `engine/05` § 4 authoritative; `04` § 3 example footnoted as clock-alignment only. **Max duration:** macro window = pacing-block span: Split One 20:10→21:30 (80 min); Split Two 21:40→23:15 (95 min); Final-act parallel 23:15→02:00 (165 min). **§ 9 reinterpretation:** 10–30 min applies to single action costs (`04` § 2), not macro phases. **Wait-for-clock:** listed leftover option advancing to trigger/deadline. |
| **Gameplay** | **Clarifies** play; does not add routes. Effectively restricts extra investigation nodes vs `04` § 3 example |
| **Compiler** | V8 PASS; timing prose citeable |
| **Authoring** | Window limits in player instructions |
| **Validation** | V8 PASS |
| **Files** | `04` § 3a–3b; `13` § 2, § 6 sync tables; footnote on `04` § 3 |

#### Option B — Engine § 9 caps macro windows at 30 minutes

| Dimension | Detail |
|---|---|
| **Behavior** | Force Split One/Two into 10–30 min regardless of pacing blocks |
| **Gameplay** | **Conflicts** with existing node costs and pacing (`04` § 5) |
| **Compiler** | Timing validation fails against current graph |
| **Validation** | Requires graph/time redesign — out of scope |
| **Files** | Many logic files |

#### Option C — Defer V8

| Dimension | Detail |
|---|---|
| **Behavior** | Document conflict; leave max durations blank |
| **Gameplay** | None |
| **Validation** | V8 BLOCKED; Milestone B incomplete |
| **Files** | None |

### 6. Recommended option

**Option A — Adventure pacing authoritative; engine § 9 scoped to per-action.**

> **This is a new design decision, not an existing repository rule.**

Rationale: resolves documented conflict without route changes; uses existing clock anchors; unblocks V8; aligns with `04` § 5 four-block structure.

### 7. Dependent rules (Classification B resolved by Option A)

- `04` § 3 superseded for action permission
- Maximum-duration formula (pacing-block span)
- Split One 80 min; Split Two 95 min; Final-act 165 min
- `engine/05` § 9 macro reinterpretation
- Wait-for-clock as leftover option (feeds MBD-03 Option A)
- Waiting-time formula inputs (feeds MBD-05)

---

## MBD-05 — Participation Audit

### 1. Decision ID and title

**MBD-05 — Participation Audit**

### 2. Blockers resolved

| Item | Gate |
|---|---|
| ER-09 | A6 (participation gate) |

### 3. Existing authoritative facts (Classification A)

| Fact | Source |
|---|---|
| Required fields: decisions, clues, challenges, waiting, final-act responsibility per player | `08_TWO_PLAYER_CORE_RULES.md` § 9 |
| Per-block fields also: communication, inactive reading time | `13_SPLIT_AND_REGROUP_FLOW.md` § 9 |
| Five logical blocks (opening, regroup ×2, midgame, final) | `13` structure; `08` § 5 |
| Opening P1/P2 branch attribution | `13` § 2 |
| Pair A node sets: P1 police `220`–`223`; P2 harbor `210`–`212` | `13` § 4 Pair A |
| Final-act role pairs (Rescue/Evidence, Interior/Exterior, Proof/Protection) | `13` § 7 |
| Opening clue/decision ranges partially populated | `13` § 9; `MILESTONE_B_IMPLEMENTATION_REPORT.md` |
| Parity requirement: no passive middle third | `13` § 7; `08` § 9 |
| No counting formulas in repository | `MILESTONE_B_IMPLEMENTATION_REPORT.md` § 6 |

### 4. Conflict or missing rule

`08` § 9 mandates an audit but does not define: normative vs informational purpose; canonical path vs all paths; decision/clue/challenge counting methods; challenge taxonomy; waiting/inactive-time formulas; mapping `13` § 7 roles to `EVT_*` nodes.

### 5. Available options

#### Option A — Informational pre-compile audit on canonical Pair A + three final patterns

| Dimension | Detail |
|---|---|
| **Behavior** | Audit is **informational** (pre-compile gate, not gameplay balancer). **Canonical path:** Pair A midgame + three `13` § 7 role patterns. **Counts:** decisions = nodes with choice fields in attributed set; clues = max distinct `ACTIVE` `CLUE_*` from `12` on attributed nodes; challenges: social = approach-choice nodes, physical = `CHK_*` perception, technical = 0; communication = modes legal in block; waiting = Σ max(0, partner_clock − player_clock) per MBD-04; inactive reading = waiting in `Split` blocks. **Role→EVT:** Rescue/Evidence `400`/`410`; Interior/Exterior `331`/`420`; Proof/Protection `430`/`400`. |
| **Gameplay** | **None** — audit only |
| **Compiler** | A6 PASS when table populated |
| **Authoring** | Informs parity review |
| **Validation** | A6 PASS |
| **Files** | `08` § 9; `13` § 9; cross-ref MBD-01/02/04 |

#### Option B — Normative gate blocking compile on imbalance

| Dimension | Detail |
|---|---|
| **Behavior** | Same counts; compile fails if thresholds exceeded |
| **Gameplay** | None directly; could force logic edits later |
| **Compiler** | Hard gate with numeric thresholds TBD |
| **Validation** | Requires threshold design — new scope |
| **Files** | Above + compiler gate config |

#### Option C — Opening block only

| Dimension | Detail |
|---|---|
| **Behavior** | Keep partial audit (current state) |
| **Validation** | A6 PARTIAL; Milestone B incomplete |
| **Files** | None |

### 6. Recommended option

**Option A — Informational pre-compile audit on canonical Pair A + three final patterns.**

> **This is a new design decision, not an existing repository rule.**

Rationale: satisfies A6 without gameplay changes; `08` § 9 already allows playtest tuning; Pair A is the smallest complete midgame reference named in `13` § 4.

### 7. Dependent rules (Classification B resolved by Option A)

- Pair A as canonical audit reference only
- Final-act `EVT_*` role mapping (three patterns)
- Three rows per final-act pattern
- Decision / clue / challenge counting methods
- Social vs physical vs technical challenge taxonomy
- Communication count per block
- `waiting_minutes` formula and cumulative clock rule
- Waiting = 0 in `Joint` blocks
- Inactive reading time = waiting in `Split` blocks

---

## MBD-06 — Solo Scope

### 1. Decision ID and title

**MBD-06 — Solo Scope**

### 2. Blockers resolved

| Item | Gate |
|---|---|
| ER-10 | C6 |
| V5 (mode scope) | Per-mode reachability |

### 3. Existing authoritative facts (Classification A)

| Fact | Source |
|---|---|
| Prototype must support one-player and two-player | `engine/06_PROTOTYPE_SCOPE_AND_VALIDATION.md` § 1 |
| Target: playable solo or cooperatively | `PROTOTYPE_BRIEF.md` |
| Solo out of scope for Alpha 0.2c logic revision | `IMPLEMENTATION_PLAN.md` § 15 |
| C6: ER-10 resolved **or** `play_modes: [two_player]` with documented exception | `ENGINE_READINESS_PLAN.md` C6 |
| `play_modes: [two_player]` already declared | `adventures/The_Last_Witness/README.md` |
| `EVT_908` two-player-only | `10` § 14; `06_ENDING_FRAMEWORK.md` END-08 |
| Solo blocker documented in `10` § 18 | `MILESTONE_B_IMPLEMENTATION_REPORT.md` |
| No solo graph, merge rules, or artifact set | `MILESTONE_B_IMPLEMENTATION_REPORT.md` § 6 |

### 4. Conflict or missing rule

`engine/06` § 1 and `PROTOTYPE_BRIEF.md` require solo capability; `IMPLEMENTATION_PLAN.md` § 15 defers solo for Alpha 0.2c; `README.md` declares two-player only. The repository presents **two valid resolution paths** (C6). Owner must choose whether Alpha 0.2c Milestone B closes with solo deferred or blocked until a solo graph is authored.

### 5. Available options

#### Option A — Solo explicitly deferred to a later milestone (Alpha 0.2c = two-player only)

| Dimension | Detail |
|---|---|
| **Behavior** | `play_modes: [two_player]`; engine exception in `10` § 18; `V5` evaluated for `two_player` only; `EVT_908` excluded from future solo artifacts |
| **Gameplay** | Two-player only for this release |
| **Compiler** | Two-player package only |
| **Authoring** | No solo narrative package |
| **Validation** | C6 PASS via scope exception; ER-10 closed for Alpha 0.2c |
| **Files** | `README.md`; `10` § 18 (confirm exception text) |

#### Option B — Solo required for Alpha 0.2c

| Dimension | Detail |
|---|---|
| **Behavior** | Author solo eligibility, merged-player routing, solo reachability, artifact set; implement before Milestone B close |
| **Gameplay** | **Requires new routing rules** not in repository |
| **Compiler** | Solo + two-player packages |
| **Authoring** | Full solo narrative path |
| **Validation** | C6 PASS via solo graph; large new scope |
| **Files** | `10`; `13`; `README.md`; new solo rules section |

### 6. Recommended option

**Option A — Solo explicitly deferred to a later milestone.**

> **This is a new design decision, not an existing repository rule.**

Rationale: matches `IMPLEMENTATION_PLAN.md` § 15 and existing `README.md` declaration; C6 explicitly permits this path; avoids inventing solo routes; preserves two-player quality for Alpha 0.2c; `engine/06` long-term goal deferred, not cancelled.

### 7. Dependent rules (Classification B resolved by Option A)

- Option A solo out-of-scope for Alpha 0.2c
- `V5` evaluated for `two_player` only until solo graph exists
- ER-10 resolved by scope declaration (not blocked)

---

## Approval table

| Decision | Recommended option | Owner approval required | Blocks |
|---|---|---|---|
| **MBD-01** Check Resolution Model | A — Minimal adventure-local D20; `dc: 10` on `CHK_115_PERCEPTION` | **Yes** | ER-02 / V-CHK; ER-09 challenge count |
| **MBD-02** Scene Mode and Player Assignment | A — Fixed canonical routing; compile override for `EVT_100` joint-path | **Yes** | ER-03 / V-SM; ER-04 prerequisite; ER-09 attribution |
| **MBD-03** Split Termination | A — Explicit `REJOIN` table; window-level wait/emergency | **Yes** | ER-04 / V-ST |
| **MBD-04** Synchronization and Time | A — Pacing authoritative; `engine/05` § 4 leftover rule; per-action § 9 scope | **Yes** | ER-05 / V8; ER-09 waiting |
| **MBD-05** Participation Audit | A — Informational audit; Pair A + three final patterns | **Yes** | ER-09 / A6 |
| **MBD-06** Solo Scope | A — Solo deferred; `two_player` only for Alpha 0.2c | **Yes** | ER-10 / C6; V5 mode scope |

**None of the recommended options are repository-authoritative until approved.**

---

## Implementation order

Dependencies between decision groups:

```text
MBD-06 (Solo scope)          ── independent; approve first
        │
MBD-01 (Check resolution)   ── independent; approve early
        │
MBD-04 (Sync/time)          ── independent of MBD-02/03
        │
MBD-02 (Scene mode)         ── requires MBD-06 only
        │
MBD-03 (Split termination)  ── requires MBD-02
        │
MBD-05 (Participation audit)── requires MBD-01, MBD-02, MBD-04
```

| Order | Decision | Prerequisite approvals |
|---:|---|---|
| 1 | **MBD-06** Solo scope | None |
| 2 | **MBD-01** Check resolution | None |
| 3 | **MBD-04** Synchronization and time | None |
| 4 | **MBD-02** Scene mode | MBD-06 |
| 5 | **MBD-03** Split termination | MBD-02 |
| 6 | **MBD-05** Participation audit | MBD-01, MBD-02, MBD-04 |

After all six approvals: update `MILESTONE_B_COMPLETION_SPEC.md` (or successor spec) to replace Classification **B** rules with approved options, then implement per `MILESTONE_B_COMPLETION_SPEC.md` § 9 handoff.

---

## Document control

| Field | Value |
|---|---|
| Version | 1.0 |
| Classification A rules preserved | Yes — cited per decision § 3 |
| Classification B rules consolidated | 42 → 6 decision groups |
| New design recommendations | All labeled in § 6 of each group |
