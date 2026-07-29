# DO NOT READ: Investigation Node Graph

## 1. Graph conventions

Each node has:

- immutable event key;
- `NODE_TYPE`, either `INTERMEDIATE` or `TERMINAL`;
- `TERMINAL_TYPE`, on terminal nodes only;
- availability window;
- location;
- player eligibility;
- entry conditions;
- time cost;
- information gained;
- state changes;
- failure transformation;
- `Outgoing`;
- `Scene mode` (authoritative values in § 1b–§ 1c);
- `Split terminator`, when `Scene mode` is `Split` and the terminator is defined (see § 1d);
- `Variants`, when a node has materially distinct player-facing outcomes (see § 1a).

`NODE_TYPE` and `Outgoing` are mandatory on every node. A node declares `Outgoing` as a list of node identifiers, or `Outgoing: None` when it is terminal. An `INTERMEDIATE` node with no outgoing target is a structural defect. A `TERMINAL` node declares exactly one `TERMINAL_TYPE` and never declares a target.

The graph is not final prose. It is the authoritative gameplay skeleton from which player-facing nodes will later be compiled.

**Playable node count:** 34 (`INTERMEDIATE` 29, `TERMINAL` 5). Off-screen nodes `EVT_801`–`EVT_804` are excluded.

---

## 1a. Variant conventions

When a node admits materially distinct outcomes, it declares a `**Variants**` block. Each variant row has:

- `variant_key` — stable snake-case identifier;
- `condition` — the existing logic condition that selects the variant;
- `grants` — clue or state effects for that variant only;
- `cost` — only when it differs from the node default.

Variant keys formalize outcomes already described in **State changes**, **Failure transformation**, or **Outcome levels**. They do not add routes, clues, thresholds, or mechanics.

---

## 1b. Scene mode conventions

Every playable `EVT_*` node must declare exactly one scene mode:

| Value | Meaning |
|---|---|
| `Joint` | Both players present; shared content unless separate choices are explicitly assigned |
| `Split` | Separate player-facing content; private knowledge isolated; must end at a synchronization point |

**MBD-02:** Scene mode describes **narrative role**, not player identity. Either player may occupy a role when the story permits. Scene mode is not permanently bound to Player 1 or Player 2.

**Historical identifiers:** `EVT_110` and `EVT_120` retain opening-cluster numbering from an earlier `_P1_` / `_P2_` naming pass. Suffixes are **historical only** and do not assign node ownership.

The `Solo` scene mode is **not used** in this adventure (`§ 18`).

Modes are assigned from narrative structure, split-window track placement in `13_SPLIT_AND_REGROUP_FLOW.md`, and collective ending resolution. Authoritative values are in § 1c.

---

## 1c. Scene mode registry

Authoritative `Scene mode` for all thirty-four playable nodes.

| Node | `Scene mode` | Narrative role / basis |
|---|---|---|
| `EVT_100` | `Joint` | shared incident briefing |
| `EVT_110` | `Split` | tech/SCADA cluster entry — Split One |
| `EVT_111` | `Split` | Kevin first contact |
| `EVT_112` | `Split` | SCADA historian access |
| `EVT_113` | `Split` | test-bay forensics |
| `EVT_115` | `Split` | test-bay physical search |
| `EVT_123` | `Split` | SCADA metadata depth |
| `EVT_120` | `Split` | field/perimeter cluster entry — Split One |
| `EVT_121` | `Split` | perimeter and loading orientation |
| `EVT_140` | `Split` | Sable desk interview |
| `EVT_141` | `Split` | badge record export |
| `EVT_130` | `Joint` | corporate pressure interrupt |
| `EVT_150` | `Joint` | Regroup One |
| `EVT_122` | `Split` | maintenance shed / Tom — Split Two credential |
| `EVT_210` | `Split` | finance hub ledger — Split Two finance |
| `EVT_230` | `Split` | Dana pressure ladder |
| `EVT_260` | `Split` | finance audit window |
| `EVT_250` | `Split` | ops floor Marcus — Split Two ops |
| `EVT_270` | `Split` | architect lab Priya |
| `EVT_271` | `Split` | vendor warning email thread |
| `EVT_240` | `Split` | witness persuasion — Split Two |
| `EVT_220` | `Split` | Kevin witness preservation — Split Three |
| `EVT_300` | `Joint` | Regroup Two |
| `EVT_312` | `Split` | maintenance cable-tray / clone — Split Three |
| `EVT_330` | `Split` | final parallel assignment — Split Three |
| `EVT_410` | `Joint` | formal accusation |
| `EVT_420` | `Joint` | evidence preservation |
| `EVT_430` | `Joint` | Dana apprehension coordination |
| `EVT_900` | `Joint` | ending dispatch |
| `EVT_901` | `Joint` | terminal epilogue — justice |
| `EVT_902` | `Joint` | terminal epilogue — wrong accusation |
| `EVT_903` | `Joint` | terminal epilogue — accident verdict |
| `EVT_904` | `Joint` | terminal epilogue — partial exposure |
| `EVT_905` | `Joint` | terminal epilogue — escape |

**Summary:** 13 `Joint`, 21 `Split`, 0 `UNCLASSIFIED`, 0 `Solo`.

---

## 1d. Split branch completion and terminators

**MBD-03:** During a split window, each player continues until they have no remaining legal actions. When finished, they **wait**.

`WAIT_UNTIL_SYNC`, `REMOTE_CONTACT`, and `EMERGENCY_INTERRUPT` are **window-level mechanics** only (`08` § 4; `13` § 5). They are **not** per-node metadata.

### Node-level terminators

Split branches that reach a regroup or convergence declare one node-level terminator from:

| Terminator | Use |
|---|---|
| `REJOIN` | Branch exit lists a regroup or convergence target in `Outgoing` |
| `TERMINAL_OUTCOME` | Branch resolves to a terminal ending without regroup |

### Split One — `REJOIN` → `EVT_150`

| Node | `Split terminator` | `Regroup target` |
|---|---|---|
| `EVT_123` | `REJOIN` | `EVT_150` |
| `EVT_141` | `REJOIN` | `EVT_150` |

In-window nodes (`EVT_110`–`EVT_115`, `EVT_120`–`EVT_140`) omit a terminator; branch completion flows through child nodes above.

### Split Two — `REJOIN` → `EVT_300`

| Node | `Split terminator` | `Regroup target` |
|---|---|---|
| `EVT_260` | `REJOIN` | `EVT_300` |
| `EVT_271` | `REJOIN` | `EVT_300` |
| `EVT_122` | `REJOIN` | `EVT_300` |
| `EVT_220` | `REJOIN` | `EVT_300` |
| `EVT_240` | `REJOIN` | `EVT_300` |

Track entry nodes (`EVT_210`, `EVT_250`, `EVT_270`, `EVT_230`) omit terminators.

### Split Three — `REJOIN` → convergence

| Node | `Split terminator` | Convergence target(s) |
|---|---|---|
| `EVT_312` | `REJOIN` | `EVT_410`, `EVT_420` per `Outgoing` |
| `EVT_330` | `REJOIN` | `EVT_410`, `EVT_420` per `Outgoing` |
| `EVT_220` | `REJOIN` | `EVT_410`, `EVT_420` per `Outgoing` |

---

## 2. Opening — `EVT_100`

**Backbone:** `ARC_100` (1:1)  
**Node type:** `INTERMEDIATE`  
**Window:** 19:00–19:15  
**Location:** `LOC_START`  
**Scene mode:** `Joint`  
**Cost:** 10 minutes  

**Entry conditions**

- always available at game start.

**Reveals**

- Elena Park deceased in automation test bay;
- corporate framing: tragic PLC fault during authorized validation;
- Dana Cole present as CFO liaison;
- Kevin Marsh maintaining SCADA historian; Sable Ortiz at security desk.

**State changes**

- `P1_LOCATION = LOC_START`;
- `P2_LOCATION = LOC_START`.

**Decision**

Players may:

1. split immediately (canonical two-player route);
2. investigate one opening cluster together at the cost of the other cluster's early-access advantage.

**Outgoing**

- `EVT_110`;
- `EVT_120`.

---

## 3. Tech / SCADA cluster — Split One

### `EVT_110`

**Backbone:** `ARC_130` (partial)  
**Node type:** `INTERMEDIATE`  
**Window:** 19:10–20:30  
**Location:** `LOC_SCADA_ROOM`  
**Scene mode:** `Split` — tech/SCADA narrative role  
**Cost:** 10 minutes travel + 5 minutes scan  

**Entry conditions**

- chosen at `EVT_100` split;
- occupying role proceeds independently on shared `CLOCK`.

**Reveals**

- SCADA room layout;
- Kevin at historian terminal;
- Marcus hold order posted on ops channel.

**State changes**

- acting role `P1_LOCATION` or `P2_LOCATION` = `LOC_SCADA_ROOM` per schema assignment.

**Outgoing**

- `EVT_111`.

---

### `EVT_111`

**Node type:** `INTERMEDIATE`  
**Window:** 19:15–20:30  
**Location:** `LOC_SCADA_ROOM`  
**Scene mode:** `Split`  
**Cost:** 10 minutes  

**Entry conditions**

- `EVT_110` complete.

**Reveals**

- Kevin's official automation timeline;
- sensor stepped anomaly at 18:51;
- Priya/Elena Friday dispute mentioned in passing.

**State changes**

- none until trust change at later nodes.

**Decision**

- request historian export now;
- defer export for test-bay escort path.

**Outgoing**

- `EVT_112`.

---

### `EVT_112`

**Node type:** `INTERMEDIATE`  
**Window:** 19:15–20:30  
**Location:** `LOC_SCADA_ROOM`  
**Scene mode:** `Split`  
**Cost:** 20 minutes  

**Entry conditions**

- `EVT_111` complete;
- `SCADA_STATE = NORMAL_ACCESS` or `HISTORIAN_ROTATION`.

**Reveals**

- partial historian visible;
- purge event flag present but auth detail locked behind metadata pass.

**State changes**

- if `SCADA_STATE = NORMAL_ACCESS` and clock ≥ 20:30, `SCADA_STATE` follows `TR_SCADA_ROTATION`.

**Outgoing**

- `EVT_113`.

---

### `EVT_113`

**Backbone:** `ARC_120` (partial)  
**Node type:** `INTERMEDIATE`  
**Window:** 19:20–20:00  
**Location:** `LOC_TEST_BAY`  
**Scene mode:** `Split`  
**Cost:** 15 minutes travel + 20 minutes forensic review  

**Entry conditions**

- Kevin escort or corporate liaison clearance;
- `TEST_BAY_STATE` not `CORPORATE_SEALED`.

**Reveals**

- Elena console position inconsistent with automated fault;
- tablet in evidence lockup;
- injury pattern inconsistent with slow automation failure.

**State changes**

- `GRANT_CLUE(CLUE_ELENA_INJURY_PATTERN)`;
- `GRANT_CLUE(CLUE_DANA_TABLET_SYNC)` on tablet imaging success.

**Outgoing**

- `EVT_115`.

---

### `EVT_115`

**Backbone:** `ARC_120`  
**Node type:** `INTERMEDIATE`  
**Window:** 19:20–20:00  
**Location:** `LOC_TEST_BAY`  
**Scene mode:** `Split`  
**Cost:** 25 minutes  

**Entry conditions**

- `EVT_113` complete;
- `TEST_BAY_STATE` permits supervised search.

**Reveals**

- CO₂ discharge pattern anomaly;
- cable-tray tamper signs;
- optional sensor spoof fragment.

**State changes**

- `GRANT_CLUE(CLUE_TEST_BAY_CO2_ANOMALY)`;
- may advance `ELENA_STATUS` toward `EVIDENCE_PARTIALLY_CLEARED` if rushed search chosen.

**Failure transformation**

- binds `CHK_115_PERCEPTION` (`17_CHECK_REGISTER.md`).

**Variants**

| variant_key | condition | grants |
|---|---|---|
| `perception_success` | `CHK_115_PERCEPTION` pass | `GRANT_CLUE(CLUE_SENSOR_SPOOF_TRACE)` |
| `perception_failure` | `CHK_115_PERCEPTION` fail | anomaly only; spoof confirmable at `EVT_220` |

**Outgoing**

- `EVT_123`.

---

### `EVT_123`

**Backbone:** `ARC_130`  
**Node type:** `INTERMEDIATE`  
**Window:** 19:30–22:30  
**Location:** `LOC_SCADA_ROOM`  
**Scene mode:** `Split`  
**Split terminator:** `REJOIN` → `EVT_150`  
**Cost:** 20 minutes  

**Entry conditions**

- tech-cluster path reached via `EVT_115`;
- `SCADA_STATE` not `LEGAL_HOLD`, or Kevin trust ≥ +1.

**Reveals**

- manual purge override at 18:52;
- auth token mismatch vs maintenance schedule;
- duplicate session metadata.

**State changes**

- `T_KEVIN +1` on cooperative export;
- may write `SCADA_STATE` toward `HISTORIAN_ROTATION` if not already;
- `GRANT_CLUE(CLUE_PURGE_MANUAL_OVERRIDE)` on pass;
- `GRANT_CLUE(CLUE_CO2_OVERRIDE_AUTH)` on pass.

**Failure transformation**

- binds `CHK_123_TECHNOLOGY`.

**Variants**

| variant_key | condition | grants |
|---|---|---|
| `technology_success` | `CHK_123_TECHNOLOGY` pass | both override clues |
| `technology_failure` | `CHK_123_TECHNOLOGY` fail | purge flag only; full auth at `EVT_220` |

**Outgoing**

- `EVT_150`.

---

## 4. Field / perimeter cluster — Split One

### `EVT_120`

**Backbone:** `ARC_110` (partial)  
**Node type:** `INTERMEDIATE`  
**Window:** 19:10–20:30  
**Location:** `LOC_START` → perimeter  
**Scene mode:** `Split` — field/perimeter narrative role  
**Cost:** 10 minutes  

**Entry conditions**

- chosen at `EVT_100` split.

**Reveals**

- loading dock camera coverage map;
- Vince contractor van logged 18:35;
- maintenance shed route open.

**Outgoing**

- `EVT_121`.

---

### `EVT_121`

**Node type:** `INTERMEDIATE`  
**Window:** 19:10–20:30  
**Location:** perimeter / loading  
**Scene mode:** `Split`  
**Cost:** 15 minutes  

**Reveals**

- after-hours badge activity summary from public incident log;
- Tom Reyes visible near shed, not in bay.

**Outgoing**

- `EVT_140`.

---

### `EVT_140`

**Backbone:** `ARC_130` (partial)  
**Node type:** `INTERMEDIATE`  
**Window:** 19:00–22:00  
**Location:** `LOC_SECURITY_DESK`  
**Scene mode:** `Split`  
**Cost:** 10 minutes  

**Reveals**

- Sable's incident timeline;
- Dana visited desk twice re badge audit timing;
- Vince blind-spot request on file.

**State changes**

- `T_SABLE +1` on procedural courtesy or leverage shown;
- `GRANT_CLUE(CLUE_AFTER_HOURS_ACCESS)`.

**Outgoing**

- `EVT_141`.

---

### `EVT_141`

**Node type:** `INTERMEDIATE`  
**Window:** 19:15–22:30  
**Location:** `LOC_SECURITY_DESK`  
**Scene mode:** `Split`  
**Split terminator:** `REJOIN` → `EVT_150`  
**Cost:** 20 minutes  

**Entry conditions**

- `EVT_140` complete;
- `SECURITY_STATE` not `RECORDS_LOCKED`, or Sable trust ≥ +1.

**Reveals**

- impossible badge swipe overlap for Elena's credential;
- Dana presence window near bay corridor;
- suppressed audit flag if Sable trust ≥ +1.

**State changes**

- `A_SECURITY +1` if records pulled without challenge filing;
- `GRANT_CLUE(CLUE_BADGE_SWIPE_MISMATCH)`;
- `GRANT_CLUE(CLUE_DANA_PRESENCE_WINDOW)`.

**Outgoing**

- `EVT_150`.

---

## 5. Regroup One — `EVT_150`

**Backbone:** `ARC_150` (1:1)  
**Node type:** `INTERMEDIATE`  
**Window:** 20:20–20:40 recommended; available when both Split One branches complete  
**Location:** any regroup point (`LOC_START` default)  
**Scene mode:** `Joint`  
**Cost:** 10 minutes  

**Entry conditions**

- both Split One branches complete (no remaining legal actions per role);
- player agreement to regroup;
- optional world-clock ≥ 20:30 makes node **available**.

**State changes**

- merges `P1_PRIVATE_KNOWLEDGE_SET` and `P2_PRIVATE_KNOWLEDGE_SET` into `SHARED_KNOWLEDGE_SET` for all clues players choose to share;
- runs conclusion evaluators on shared set.

**Decision**

Assign Split Two tracks:

1. finance hub (`EVT_210`);
2. ops / architect (`EVT_250`);
3. optional credential maintenance (`EVT_122`);
4. optional witness acceleration (`EVT_240`).

**Outgoing**

- `EVT_210`;
- `EVT_250`;
- `EVT_122`;
- `EVT_240`;
- `EVT_130` (if `A_CORPORATE >= 1` and not yet resolved).

---

## 6. Corporate pressure — `EVT_130`

**Backbone:** `ARC_200` (1:1)  
**Node type:** `INTERMEDIATE`  
**Window:** 21:00–23:00  
**Location:** `LOC_OPS_FLOOR` or liaison call  
**Scene mode:** `Joint`  
**Cost:** 15 minutes  

**Entry conditions**

- `A_CORPORATE >= 1` or clock ≥ 21:15;
- may interrupt between `EVT_150` and `EVT_300`.

**Reveals**

- settlement offer;
- supervised access trade;
- legal observer assignment if awareness high.

**State changes**

- `A_CORPORATE +1` unless players file formal challenge intent;
- may trigger `TR_FINANCE_RESTRICTED`.

**Decision**

- accept supervised access;
- challenge with partial proof;
- split to preserve off-network copies.

**Outgoing**

- `EVT_210`;
- `EVT_250`;
- `EVT_300` (if Split Two tracks already complete).

---

## 7. Split Two — finance track

### `EVT_210`

**Backbone:** `ARC_140`  
**Node type:** `INTERMEDIATE`  
**Window:** 19:30–21:30  
**Location:** `LOC_FINANCE_HUB`  
**Scene mode:** `Split` — finance-track role  
**Cost:** 20 minutes  

**Reveals**

- procurement ledger browse;
- Elena-flagged anomalies;
- Glassline vendor entries.

**State changes**

- `GRANT_CLUE(CLUE_FINANCE_DISCREPANCY)` on deep search success.

**Failure transformation**

- binds `CHK_210_INVESTIGATION`.

**Variants**

| variant_key | condition | grants |
|---|---|---|
| `investigation_success` | `CHK_210_INVESTIGATION` pass | `CLUE_FINANCE_DISCREPANCY` |
| `investigation_failure` | `CHK_210_INVESTIGATION` fail | summary only; full detail deferred |

**Outgoing**

- `EVT_230`;
- `EVT_260`.

---

### `EVT_230`

**Backbone:** `ARC_230` (1:1)  
**Node type:** `INTERMEDIATE`  
**Window:** 20:00–23:00  
**Location:** `LOC_FINANCE_HUB`  
**Scene mode:** `Split`  
**Cost:** 20 minutes  

**Reveals**

- Dana liability talking points;
- partial admission of "process shortcuts";
- redirect toward Vince or Tom.

**State changes**

- `A_CORPORATE +1` on aggressive confrontation;
- `A_DANA +1`;
- `GRANT_CLUE(CLUE_DANA_FINANCE_LINK)`.

**Outgoing**

- `EVT_260`;
- `EVT_300`.

---

### `EVT_260`

**Node type:** `INTERMEDIATE`  
**Window:** 20:30–22:00  
**Location:** `LOC_FINANCE_HUB`  
**Scene mode:** `Split`  
**Split terminator:** `REJOIN` → `EVT_300`  
**Cost:** 25 minutes  

**Entry conditions**

- `FINANCE_STATE` not `SEALED`, or players hold challenge filing.

**Reveals**

- Dana approval bursts;
- shell vendor routing;
- evening audit memo queue.

**State changes**

- `A_DANA +1` if shell vendors named aloud;
- `GRANT_CLUE(CLUE_DANA_APPROVAL_PATTERN)`.

**Outgoing**

- `EVT_300`.

---

## 8. Split Two — ops / architect track

### `EVT_250`

**Node type:** `INTERMEDIATE`  
**Window:** 19:30–22:30  
**Location:** `LOC_OPS_FLOOR`  
**Scene mode:** `Split` — ops-track role  
**Cost:** 15 minutes  

**Reveals**

- Marcus incident command posture;
- export hold on SCADA;
- Tom work-order signature on file.

**State changes**

- `T_MARCUS +1` if shown good-faith safety concern;
- may advance `OPS_STATE` toward `NIGHT_SKELETON` after 22:00.

**Outgoing**

- `EVT_270`.

---

### `EVT_270`

**Backbone:** `ARC_220` (partial)  
**Node type:** `INTERMEDIATE`  
**Window:** 19:30–22:30  
**Location:** `LOC_ARCHITECT_LAB`  
**Scene mode:** `Split`  
**Cost:** 20 minutes  

**Reveals**

- Priya rivalry context;
- Dana expedited approval channel;
- Vince lab camera disable request.

**Outgoing**

- `EVT_271`.

---

### `EVT_271`

**Backbone:** `ARC_220`  
**Node type:** `INTERMEDIATE`  
**Window:** 19:30–23:00  
**Location:** `LOC_ARCHITECT_LAB`  
**Scene mode:** `Split`  
**Split terminator:** `REJOIN` → `EVT_300`  
**Cost:** 15 minutes  

**Entry conditions**

- Priya cooperation or fraud thread shown.

**Reveals**

- Elena's vendor warning email (`FACT_ELENA_VENDOR_WARNING`);
- shell company names cross-linked to Vince payment.

**State changes**

- `GRANT_CLUE(CLUE_VENDOR_SHELL_COMPANY)`;
- `GRANT_CLUE(CLUE_ELENA_AUDIT_THREAD)` if not already held from tablet.

**Outgoing**

- `EVT_300`.

---

## 9. Split Two — credential and witness tracks

### `EVT_122`

**Backbone:** `ARC_210` (partial)  
**Node type:** `INTERMEDIATE`  
**Window:** 20:30–23:00  
**Location:** `LOC_MAINTENANCE_SHED`  
**Scene mode:** `Split`  
**Split terminator:** `REJOIN` → `EVT_300`  
**Cost:** 20 minutes  

**Reveals**

- Tom schedule contradiction;
- forged work order on clipboard;
- Dana panel walkthrough fact on confrontation.

**State changes**

- `GRANT_CLUE(CLUE_MAINT_WORKORDER_FORGED)`.

**Outgoing**

- `EVT_300`.

---

### `EVT_240`

**Backbone:** `ARC_240` (partial)  
**Node type:** `INTERMEDIATE`  
**Window:** 20:00–22:30  
**Location:** `LOC_SECURITY_DESK` or `LOC_SCADA_ROOM`  
**Scene mode:** `Split`  
**Split terminator:** `REJOIN` → `EVT_300`  
**Cost:** 10 minutes  

**Reveals**

- accelerated witness Stage 1;
- export scheduling;
- procedural inconsistency confirmation.

**State changes**

- `T_SABLE +1` or `T_KEVIN +1` on success.

**Failure transformation**

- binds `CHK_240_PERSUASION`.

**Variants**

| variant_key | condition | grants |
|---|---|---|
| `persuasion_success` | `CHK_240_PERSUASION` pass | trust +1 chosen witness |
| `persuasion_failure` | `CHK_240_PERSUASION` fail | Stage 0; proof-based unlock remains |

**Outgoing**

- `EVT_220`;
- `EVT_300`.

---

## 10. Regroup Two — `EVT_300`

**Backbone:** `ARC_250` (1:1)  
**Node type:** `INTERMEDIATE`  
**Window:** deadline 22:45 recommended  
**Location:** regroup point  
**Scene mode:** `Joint`  
**Cost:** 10 minutes  

**Entry conditions**

- Split Two branches complete and player agreement;
- optional clock ≥ 22:45 makes node **available**.

**State changes**

- merges newly chosen private clues into `SHARED_KNOWLEDGE_SET`;
- runs all conclusion evaluators.

**Decision — final-act assignment**

Players assign Split Three roles:

1. `EVT_330` confront / document / challenge variant;
2. `EVT_312` credential recovery;
3. `EVT_220` historian and footage preservation.

**Planning checklist (not a D20 roll)**

- murder thread status;
- fraud/credential thread status;
- Dana suspicion level;
- preservation plan.

**Outgoing**

- `EVT_330`;
- `EVT_312`;
- `EVT_220`;
- `EVT_410` (if both roles agree to skip Split Three and accuse early with sufficient proof).

---

## 11. Split Three — final parallel

### `EVT_220`

**Backbone:** `ARC_240`  
**Node type:** `INTERMEDIATE`  
**Window:** 21:00–23:30  
**Location:** `LOC_SCADA_ROOM` / `LOC_SECURITY_DESK`  
**Scene mode:** `Split`  
**Split terminator:** `REJOIN` → `EVT_410`, `EVT_420`  
**Cost:** 20 minutes  

**Reveals**

- Kevin Stage 2 historian export;
- Sable unaltered footage subset;
- failsafe manual purge confirmation if tech branch missed override clues.

**State changes**

- `T_KEVIN +1` on successful covert export;
- `ITEM_PURGE_LOG` digital state → `COPIED` when export succeeds;
- `ITEM_SECURITY_FOOTAGE` → `COPIED` when Sable Stage 2 met.

**Outgoing**

- `EVT_410`;
- `EVT_420`.

---

### `EVT_312`

**Backbone:** `ARC_210`  
**Node type:** `INTERMEDIATE`  
**Window:** 21:00–23:30  
**Location:** `LOC_MAINTENANCE_SHED`  
**Scene mode:** `Split`  
**Split terminator:** `REJOIN` → `EVT_410`, `EVT_420`  
**Cost:** 15–25 minutes  

**Entry conditions**

- `MAINT_STATE` not `ACCESS_DENIED`, or Tom present.

**Reveals**

- badge-cloning device in tool crib void;
- Dana stash trace;
- cable-tray adjacency to bay RF path.

**State changes**

- `A_SECURITY +1` on forced unauthorized entry failure variant;
- `MAINT_STATE` may follow `TR_MAINT_ALARM`;
- `GRANT_CLUE(CLUE_BADGE_CLONE_DEVICE)` on success.

**Failure transformation**

- binds `CHK_312_ATHLETICS`.

**Variants**

| variant_key | condition | grants |
|---|---|---|
| `athletics_success` | `CHK_312_ATHLETICS` pass | clone device clue |
| `athletics_failure` | `CHK_312_ATHLETICS` fail | Tom-assisted search path (+15 min) |

**Outgoing**

- `EVT_410`;
- `EVT_420`.

---

### `EVT_330`

**Backbone:** `ARC_300`, `ARC_320` (partial)  
**Node type:** `INTERMEDIATE`  
**Window:** 22:00–23:30  
**Location:** `LOC_FINANCE_HUB`, parking, or `LOC_TEST_BAY` per variant  
**Scene mode:** `Split`  
**Split terminator:** `REJOIN` → `EVT_410`, `EVT_420`  
**Cost:** 20–30 minutes  

**Variants**

| variant_key | condition | state effects |
|---|---|---|
| `confront_dana` | players assigned confront role | `A_DANA +1`; Dana flee risk if clock ≥ 22:45 |
| `document_chain` | players assigned documentation role | test-bay/tablet chain logged for accusation support |
| `file_challenge` | players assigned relay role | `REPORT_STATE = CHALLENGED` if murder proof met |

**State changes**

- `A_DANA +1` on confront variant;
- may trigger off-screen `EVT_803` if flee conditions met and no intercept.

**Outgoing**

- `EVT_410`;
- `EVT_420`.

---

## 12. Accusation, preservation, custody

### `EVT_410`

**Backbone:** `ARC_400`, `ARC_440` (absorbed)  
**Node type:** `INTERMEDIATE`  
**Window:** 22:30–00:30  
**Location:** `LOC_OPS_FLOOR` or formal hearing room  
**Scene mode:** `Joint`  
**Cost:** 20 minutes  

**Entry conditions**

- Split Three complete or players agreed to early accusation at `EVT_300`;
- at least one conclusion threshold under evaluation.

**Decision**

Players name one `NPC_*` as culprit or primary responsible party.

**State changes**

- `PUBLIC_ACCUSATION_TARGET` set;
- `PUBLIC_ACCUSATION_SUPPORT` computed from held culprit clues and preserved artifacts;
- `WRONG_ACCUSATION = true` if target ≠ `NPC_DANA` or Dana accusation below `CON_CULPRIT_DANA`;
- `A_CORPORATE +1` on any public accusation;
- `REPORT_STATE = CHALLENGED` if murder proof met and challenge chosen;
- `REPORT_STATE = SUBMITTED_HOMICIDE` if supported Dana accusation with institutional backing.

**Outgoing**

- `EVT_420`;
- `EVT_430`;
- `EVT_900`.

---

### `EVT_420`

**Backbone:** `ARC_420` (1:1)  
**Node type:** `INTERMEDIATE`  
**Window:** any time before `CLK_0030`  
**Location:** network egress point  
**Scene mode:** `Joint`  
**Cost:** 15 minutes  

**State changes**

- `EVIDENCE_PRESERVED = true` when at least one artifact among ledger, historian, footage, tablet memo reaches `COPIED` or `TRANSMITTED` external state.

**Outgoing**

- `EVT_430`;
- `EVT_900`.

---

### `EVT_430`

**Node type:** `INTERMEDIATE`  
**Window:** 22:30–00:30  
**Location:** parking / security intercept  
**Scene mode:** `Joint`  
**Cost:** 10 minutes  

**Entry conditions**

- `PUBLIC_ACCUSATION_TARGET = NPC_DANA` with support ≥ 2, or security intercept authorized;
- `EVT_803` not already fired.

**State changes**

- `DANA_APPREHENDED = true` on success;
- on failure, `EVT_803` may fire per `06` § 4.

**Outgoing**

- `EVT_900`.

---

## 13. Ending dispatch — `EVT_900`

**Backbone:** `ARC_900` (partial)  
**Node type:** `INTERMEDIATE`  
**Window:** at or after `CLK_0030`, or immediately after `EVT_410`/`EVT_420`/`EVT_430` chain  
**Location:** n/a — resolver node  
**Scene mode:** `Joint`  
**Cost:** 0 minutes  

**Entry conditions**

- accusation and preservation chain resolved, or case clock closed.

**State changes**

- invokes `EVAL_ENDING` (`14_ENDING_TRIGGER_MATRIX.md` § 1);
- selects exactly one terminal node.

**Outgoing**

- `EVT_901`;
- `EVT_902`;
- `EVT_903`;
- `EVT_904`;
- `EVT_905`.

(Exactly one target taken per `EVAL_ENDING` priority.)

---

## 14. Terminal epilogues

### `EVT_901` — `END_JUSTICE`

**Node type:** `TERMINAL`  
**Terminal type:** `VICTORY`  
**Scene mode:** `Joint`  
**Outgoing:** None  

Narrative outcome owned by `06_ENDING_FRAMEWORK.md` § `END_JUSTICE`.

---

### `EVT_902` — `END_WRONG_ACCUSATION`

**Node type:** `TERMINAL`  
**Terminal type:** `CASE_UNRESOLVED`  
**Scene mode:** `Joint`  
**Outgoing:** None  

Target-specific rebuttal variant keyed to `PUBLIC_ACCUSATION_TARGET`.

---

### `EVT_903` — `END_ACCIDENT_VERDICT`

**Node type:** `TERMINAL`  
**Terminal type:** `TIME_EXPIRED`  
**Scene mode:** `Joint`  
**Outgoing:** None  

---

### `EVT_904` — `END_PARTIAL_EXPOSURE`

**Node type:** `TERMINAL`  
**Terminal type:** `PARTIAL_SUCCESS`  
**Scene mode:** `Joint`  
**Outgoing:** None  

---

### `EVT_905` — `END_ESCAPE`

**Node type:** `TERMINAL`  
**Terminal type:** `NARRATIVE_FAILURE`  
**Scene mode:** `Joint`  
**Outgoing:** None  

---

## 15. Variable writes summary

| Variable | Writers among playable nodes |
|---|---|
| `CLOCK` | all nodes with declared time cost |
| `T_SABLE` | `EVT_140`, `EVT_240` |
| `T_KEVIN` | `EVT_123`, `EVT_220` |
| `T_MARCUS` | `EVT_250` |
| `A_CORPORATE` | `EVT_130`, `EVT_230`, `EVT_410` |
| `A_DANA` | `EVT_230`, `EVT_260`, `EVT_330` |
| `A_SECURITY` | `EVT_141`, `EVT_312` |
| `ELENA_STATUS` | `EVT_115` |
| `REPORT_STATE` | `EVT_410`, `EVT_330` (challenge variant) |
| `TEST_BAY_STATE` | via `EVT_113`, `EVT_115` player actions triggering `TR_TEST_BAY_SEALED` |
| `SCADA_STATE` | `EVT_123` |
| `MAINT_STATE` | `EVT_312` |
| `SHARED_KNOWLEDGE_SET` | `EVT_150`, `EVT_300` |
| `P1_PRIVATE_KNOWLEDGE_SET` / `P2_PRIVATE_KNOWLEDGE_SET` | all `Split` nodes with `GRANT_CLUE` |
| `PUBLIC_ACCUSATION_TARGET` | `EVT_410` |
| `PUBLIC_ACCUSATION_SUPPORT` | `EVT_410` |
| `EVIDENCE_PRESERVED` | `EVT_420` |
| `DANA_APPREHENDED` | `EVT_430` |
| `WRONG_ACCUSATION` | `EVT_410` |

`P1_AVAILABLE_AT` and `P2_AVAILABLE_AT` are **not written** (MBD-04).

---

## 16. Graph integrity

### Reachability

- Every `INTERMEDIATE` node is reachable from `EVT_100` along at least one legal path.
- Every `Outgoing` target resolves to a declared node identifier in this file.
- Terminal nodes declare `Outgoing: None` only.

### Clue coverage

- All 16 `ACTIVE` clues from `12_CLUE_DEPENDENCY_GRAPH.md` are granted by at least one node via `GRANT_CLUE`.
- No node grants a clue not declared in `00_ENTITY_KEY_TABLE.md`.

### Split safety

- No `Split` node grants a clue required for the other role's immediate live puzzle in the same window.
- Regroup gates `EVT_150` and `EVT_300` are the only nodes that merge private knowledge sets.

### Off-screen exclusion

- `EVT_801`–`EVT_804` are declared in `06_NPC_SCHEDULE_AND_PRIORITY.md` § 4 and are excluded from playable reachability.

### Target existence audit

All thirty-four playable nodes and all `Outgoing` edges verified:

| Source | Targets | Status |
|---|---|---|
| `EVT_100` | `EVT_110`, `EVT_120` | OK |
| `EVT_110`–`EVT_115`, `EVT_123` | tech cluster chain | OK |
| `EVT_115` | `EVT_123` | OK |
| `EVT_123` | `EVT_150` | OK |
| `EVT_120`–`EVT_140` | linear chain | OK |
| `EVT_141` | `EVT_150` | OK |
| `EVT_150` | `EVT_210`, `EVT_250`, `EVT_122`, `EVT_240`, `EVT_130` | OK |
| `EVT_130` | `EVT_210`, `EVT_250`, `EVT_300` | OK |
| `EVT_210` | `EVT_230`, `EVT_260` | OK |
| `EVT_230` | `EVT_260`, `EVT_300` | OK |
| `EVT_260` | `EVT_300` | OK |
| `EVT_250` | `EVT_270` | OK |
| `EVT_270` | `EVT_271` | OK |
| `EVT_271` | `EVT_300` | OK |
| `EVT_122` | `EVT_300` | OK |
| `EVT_240` | `EVT_220`, `EVT_300` | OK |
| `EVT_300` | `EVT_330`, `EVT_312`, `EVT_220`, `EVT_410` | OK |
| `EVT_220`, `EVT_312`, `EVT_330` | `EVT_410`, `EVT_420` | OK |
| `EVT_410` | `EVT_420`, `EVT_430`, `EVT_900` | OK |
| `EVT_420` | `EVT_430`, `EVT_900` | OK |
| `EVT_430` | `EVT_900` | OK |
| `EVT_900` | `EVT_901`–`EVT_905` | OK |
| `EVT_901`–`EVT_905` | None | OK |

---

## 17. Identifier status

This document owns the playable `EVT_*` namespace (excluding off-screen `EVT_800` band except references).

| Status | Count | Range |
|---|---:|---|
| `ACTIVE` playable | 34 | `EVT_100`–`EVT_430`, `EVT_900`–`EVT_905` |
| Off-screen referenced | 4 | `EVT_801`–`EVT_804` in `06` § 4 |

Every playable `EVT_*` identifier carries `ACTIVE` status and appears in § 1c.

---

## 18. Play modes

| Mode | Status |
|---|---|
| `two_player` | **ACTIVE** — sole supported mode for Alpha 0.2 |
| `solo` | **DEFERRED** — not authored; scene modes assume two roles |

Solo deferral does not alter node declarations. A future solo pass would duplicate regroup nodes as AI-sync gates or merge split branches with explicit cost penalties.
