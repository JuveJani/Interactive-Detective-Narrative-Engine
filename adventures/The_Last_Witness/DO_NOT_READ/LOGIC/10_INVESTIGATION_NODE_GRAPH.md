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
- `Scene mode`, when deterministically classifiable (see § 1b–§ 1c);
- `Split terminator`, when `Scene mode` is `Split` and the terminator is defined (see § 1d);
- `Variants`, when a node has materially distinct player-facing outcomes (see § 1a).

`NODE_TYPE` and `Outgoing` are mandatory on every node. A node declares `Outgoing` as a list of node identifiers, or `Outgoing: None` when it is terminal. An `INTERMEDIATE` node with no outgoing target is a structural defect. A `TERMINAL` node declares exactly one `TERMINAL_TYPE` drawn from `engine/03_ARCHITECTURE.md` § 3.18 and never declares a target.

The graph is not final prose. It is the authoritative gameplay skeleton from which player-facing nodes will later be compiled.

## 1a. Variant conventions

When a node admits materially distinct outcomes, it declares a `**Variants**` block. Each variant row has:

- `variant_key` — stable snake-case identifier;
- `condition` — the existing logic condition that selects the variant;
- `grants` — clue or state effects for that variant only;
- `cost` — only when it differs from the node default.

Variant keys formalize outcomes already described in **State changes**, **Failure transformation**, **Outcome levels**, or equivalent fields. They do not add routes, clues, thresholds, or mechanics.

## 1b. Scene mode conventions

Every playable `EVT_*` node must declare exactly one scene mode drawn from `engine/05_TWO_PLAYER_SYNCHRONIZATION.md` § 3:

| Value | Meaning |
|---|---|
| `Joint` | Both players present; shared content unless separate choices are explicitly assigned |
| `Split` | Separate player-facing content; private knowledge isolated; must end at a synchronization point |

**MBD-02 (Alpha 0.2c):** Scene mode describes **narrative role**, not player identity. Nodes represent story roles or locations. Either player may occupy a role when the story permits. Scene mode is metadata for narrative structure. It is **not** permanently bound to Player 1 or Player 2.

The `Solo` scene mode exists in `engine/05` § 3.3 but is **not used** in this adventure for Alpha 0.2c (`two_player` only; see § 18).

Modes are assigned from narrative structure: regroup gates, split-window track placement in `13_SPLIT_AND_REGROUP_FLOW.md`, and collective ending resolution. Authoritative values are in § 1c.

## 1c. Scene mode registry

Authoritative `Scene mode` for all forty-eight playable nodes. Classification uses **narrative role or location**, not permanent player identity (MBD-02).

| Node | `Scene mode` | Narrative role / basis |
|---|---|---|
| `EVT_100_SHARED_BRIEFING` | `Joint` | shared briefing; both players present |
| `EVT_110_P1_APARTMENT_APPROACH` | `Split` | apartment-cluster approach during Split One |
| `EVT_111_MINA_FIRST_CONTACT` | `Split` | apartment cluster — Mina contact role |
| `EVT_112_RESTRICTED_APARTMENT` | `Split` | apartment cluster — restricted access role |
| `EVT_113_APARTMENT_SEARCH` | `Split` | apartment cluster — search role |
| `EVT_114_NEIGHBOUR_INTERVIEW` | `Split` | apartment cluster — neighbour interview role |
| `EVT_115_SERVICE_CORRIDOR` | `Split` | apartment cluster — service corridor role |
| `EVT_120_P2_NEWSROOM_ENTRY` | `Split` | newsroom-cluster entry during Split One |
| `EVT_121_NADIA_INTERVIEW` | `Split` | newsroom cluster — Nadia interview role |
| `EVT_122_MARCUS_OBSERVATION` | `Split` | newsroom cluster — Marcus observation role |
| `EVT_123_NEWSROOM_RECORDS` | `Split` | newsroom cluster — records recovery role |
| `EVT_150_REGROUP_ONE` | `Joint` | Regroup One; `ARC_170` sync gate |
| `EVT_210_HARBOR_ARCHIVE_ENTRY` | `Split` | midgame harbor-archive track (`13` § 4) |
| `EVT_211_CAFE_ORPHEUS` | `Split` | midgame café-research track (`13` § 4) |
| `EVT_212_TERMINAL_RECON` | `Split` | midgame terminal-reconnaissance track (`13` § 4) |
| `EVT_220_MINA_REPORT_COMPARISON` | `Split` | midgame police-procedure track (`13` § 4) |
| `EVT_221_CAMERA_REQUEST_AUDIT` | `Split` | midgame police-procedure track (`13` § 4) |
| `EVT_222_PROTECTION_ORDER_AUDIT` | `Split` | midgame police-procedure track (`13` § 4) |
| `EVT_223_ROOK_INTERVIEW` | `Split` | midgame police-procedure track (`13` § 4) |
| `EVT_230_IRIS_WORKPLACE` | `Split` | midgame medical-trail track (`13` § 4) |
| `EVT_231_PREPAID_PHONE_TRACE` | `Split` | midgame medical-trail track (`13` § 4) |
| `EVT_232_MEDICAL_INTERPRETATION` | `Split` | midgame medical-trail track (`13` § 4) |
| `EVT_240_MARCUS_PRESSURE_STAGE_ONE` | `Split` | midgame newsroom-investigation track (`13` § 4) |
| `EVT_241_MARCUS_FULL_DISCLOSURE` | `Split` | midgame newsroom-investigation track (`13` § 4) |
| `EVT_242_REED_OFFICE_SEARCH` | `Split` | midgame Reed-office track (`13` § 4) |
| `EVT_243_REED_NEGOTIATION` | `Split` | midgame Reed-office track (`13` § 4) |
| `EVT_300_REGROUP_TWO` | `Joint` | Regroup Two; `ARC_270` sync gate |
| `EVT_310_CABLE_CORRIDOR_ENTRY` | `Split` | final-act terminal entry — cable corridor role |
| `EVT_311_NORTH_GATE_ENTRY` | `Split` | final-act terminal entry — north gate role |
| `EVT_312_DRAINAGE_ENTRY` | `Split` | final-act terminal entry — drainage role |
| `EVT_313_EMERGENCY_ENTRY` | `Split` | final-act terminal entry — emergency role |
| `EVT_314_MAIN_ENTRY_CONFRONTATION` | `Split` | final-act terminal entry — main gate role |
| `EVT_330_FIND_SIGNAL_4B` | `Split` | final-act interior location role (`13` § 7) |
| `EVT_331_LENA_IRIS_NEGOTIATION` | `Split` | final-act negotiation role (`13` § 7) |
| `EVT_400_RESCUE_CONTROL` | `Split` | final-act rescue-control role (`13` § 7) |
| `EVT_410_LEDGER_RECOVERY` | `Split` | final-act evidence-recovery role (`13` § 7) |
| `EVT_420_REED_OR_ROOK_CONFRONTATION` | `Split` | final-act exterior confrontation role (`13` § 7) |
| `EVT_430_COMPLETE_TRANSFER` | `Split` | final-act evidence-transfer role (`13` § 7) |
| `EVT_440_FINAL_PUBLIC_POSITION` | `Joint` | collective public accusation |
| `EVT_900_RESOLVE_ENDING` | `Joint` | collective ending dispatch |
| `EVT_901_END_WITNESS_SPEAKS` | `Joint` | terminal epilogue; collective outcome |
| `EVT_902_END_EVIDENCE_WITHOUT_WITNESS` | `Joint` | terminal epilogue; collective outcome |
| `EVT_903_END_LIFE_SAVED_TRUTH_DELAYED` | `Joint` | terminal epilogue; collective outcome |
| `EVT_904_END_PROTECTIVE_CUSTODY` | `Joint` | terminal epilogue; collective outcome |
| `EVT_905_END_PUBLIC_LEAK` | `Joint` | terminal epilogue; collective outcome |
| `EVT_906_END_SILENT_TERMINAL` | `Joint` | terminal epilogue; collective outcome |
| `EVT_907_END_WRONG_ACCUSATION` | `Joint` | terminal epilogue; collective outcome |
| `EVT_908_END_FRACTURED_TRUTH` | `Joint` | terminal epilogue; collective outcome; two-player-only reachability per § 14 |

**Summary:** 13 `Joint`, 35 `Split`, 0 `UNCLASSIFIED`, 0 `Solo`.

## 1d. Split branch completion and terminators

**MBD-03 (Alpha 0.2c):** During a split window, each player continues until they have no remaining legal actions. When a player has finished, they **wait** — no forced movement, no automatic jump, no timer-based interruption, and no pressure on the other player.

`WAIT_UNTIL_SYNC`, `REMOTE_CONTACT`, and `EMERGENCY_INTERRUPT` are **window-level mechanics** only (`08_TWO_PLAYER_CORE_RULES.md` § 4; `13_SPLIT_AND_REGROUP_FLOW.md` § 5–§ 6). They are **not** per-node metadata.

### Node-level terminators

Per `engine/05_TWO_PLAYER_SYNCHRONIZATION.md` § 5, split branches that reach a regroup or convergence declare one node-level terminator from:

| Terminator | Use |
|---|---|
| `REJOIN` | Branch exit lists a regroup or convergence target in `Outgoing` |
| `TERMINAL_OUTCOME` | Branch resolves to a terminal ending without regroup |

`REMOTE_CONTACT`, `WAIT_UNTIL_SYNC`, and `EMERGENCY_INTERRUPT` are excluded from this table.

### Split One — `REJOIN` → `EVT_150_REGROUP_ONE`

| Node | `Split terminator` | `Regroup target` |
|---|---|---|
| `EVT_112_RESTRICTED_APARTMENT` | `REJOIN` | `EVT_150_REGROUP_ONE` |
| `EVT_113_APARTMENT_SEARCH` | `REJOIN` | `EVT_150_REGROUP_ONE` |
| `EVT_114_NEIGHBOUR_INTERVIEW` | `REJOIN` | `EVT_150_REGROUP_ONE` |
| `EVT_115_SERVICE_CORRIDOR` | `REJOIN` | `EVT_150_REGROUP_ONE` |
| `EVT_121_NADIA_INTERVIEW` | `REJOIN` | `EVT_150_REGROUP_ONE` |
| `EVT_122_MARCUS_OBSERVATION` | `REJOIN` | `EVT_150_REGROUP_ONE` |
| `EVT_123_NEWSROOM_RECORDS` | `REJOIN` | `EVT_150_REGROUP_ONE` |

In-window nodes (`EVT_110`, `EVT_111`, `EVT_120`) omit a terminator; branch completion flows through child nodes above.

### Split Two — `REJOIN` → `EVT_300_REGROUP_TWO`

Every midgame `Split` node (`EVT_210`–`EVT_243`) whose `Outgoing` includes `EVT_300_REGROUP_TWO` declares `REJOIN` → `EVT_300_REGROUP_TWO`.

### Final act — `REJOIN` → convergence

| Node | `Split terminator` | Convergence target(s) |
|---|---|---|
| `EVT_310`–`EVT_314` | `REJOIN` | `EVT_330_FIND_SIGNAL_4B` and/or `EVT_314_MAIN_ENTRY_CONFRONTATION` per `Outgoing` |
| `EVT_330`–`EVT_430` | `REJOIN` | `EVT_440_FINAL_PUBLIC_POSITION` and/or `EVT_900_RESOLVE_ENDING` per `Outgoing` |

## 2. Opening nodes

### `EVT_100_SHARED_BRIEFING`


**Backbone:** `ARC_100` (1:1)
**Window:** 20:00-20:10  
**Location:** `LOC_START`  
**Players:** both  
**Cost:** 10 minutes  
**Purpose:** establish the missing-witness case and split the first leads.

**Entry conditions**

- always available at game start.

**Reveals**

- Elias vanished before entering official protection;
- police claim probable abduction;
- Nadia disputes the official account;
- Elias failed to make a scheduled contact.

**State changes**

- `T_NADIA` remains 0;
- `P1_LOCATION = LOC_START`;
- `P2_LOCATION = LOC_START`.

**Decision**

Players may:

1. split immediately;
2. investigate one branch together at the cost of losing the other branch's early access advantage.

The canonical two-player route is a split.

---

## 3. Player 1 opening branch

**Node type:** `INTERMEDIATE`

**Outgoing**

- `EVT_110_P1_APARTMENT_APPROACH`;
- `EVT_120_P2_NEWSROOM_ENTRY`.
### `EVT_110_P1_APARTMENT_APPROACH`


**Backbone:** `ARC_110`, `ARC_120` (absorbed split decision; apartment cluster)
**Window:** 20:10-20:25  
**Location:** transit to `LOC_ELIAS_APT`  
**Players:** Player 1, or both if chosen  
**Cost:** 15 minutes

**Entry conditions**

- `EVT_100_SHARED_BRIEFING` completed.

**State changes**

- `P1_LOCATION = LOC_ELIAS_APT`;
- Mina is still present if arrival is no later than 20:30.

**Node type:** `INTERMEDIATE`

**Outgoing**

- `EVT_111_MINA_FIRST_CONTACT`;
- `EVT_112_RESTRICTED_APARTMENT`.
### `EVT_111_MINA_FIRST_CONTACT`


**Backbone:** `ARC_120` (apartment cluster)
**Window:** before 20:30  
**Location:** `LOC_ELIAS_APT`  
**Cost:** 10 minutes

**Core decision**

Player 1 chooses approach:

- procedural cooperation;
- direct challenge to police narrative;
- private appeal to Mina.

**Outcomes**

- cooperative or evidence-focused approach: `T_MINA +1`;
- reckless accusation: `T_MINA -1`, `A_ROOK_PLAYERS +1`.

**Variants**

| `variant_key` | `condition` | `grants` |
|---|---|---|
| `approach_cooperative` | procedural cooperation or private appeal to Mina | `T_MINA +1` |
| `approach_reckless` | direct challenge to police narrative without proof | `T_MINA -1`, `A_ROOK_PLAYERS +1` |

**Reveals**

- Mina's initial impression did not match a violent abduction;
- Rook took control unusually quickly.

**Node type:** `INTERMEDIATE`

**Outgoing**

- `EVT_113_APARTMENT_SEARCH`;
- `EVT_114_NEIGHBOUR_INTERVIEW`;
- `EVT_115_SERVICE_CORRIDOR`.
### `EVT_112_RESTRICTED_APARTMENT`


**Backbone:** `ARC_120` (apartment cluster)
**Window:** after 20:30  
**Location:** `LOC_ELIAS_APT`  
**Cost:** 10-20 minutes

**Purpose**

Late-access fallback.

**Routes**

- persuade Mina if `T_MINA >= 0`;
- inspect common areas legally;
- return later with stronger procedural proof;
- unauthorized entry, increasing `A_ROOK_PLAYERS`.

This node never permanently removes apartment evidence. It changes cost and antagonist awareness.

**Node type:** `INTERMEDIATE`

**Outgoing**

- `EVT_113_APARTMENT_SEARCH`;
- `EVT_114_NEIGHBOUR_INTERVIEW`;
- `EVT_115_SERVICE_CORRIDOR`;
- `EVT_150_REGROUP_ONE`.
### `EVT_113_APARTMENT_SEARCH`


**Backbone:** `ARC_120` (apartment cluster)
**Cost:** 20 minutes  
**Information routes**

A successful careful search reveals two of:

- missing medication/travel preparation;
- preserved blood anomaly;
- broken-phone inconsistency;
- empty passport concealment.

A failed or rushed search reveals one suspicious category and costs an additional corroboration requirement later.

**State changes**

- `GRANT_CLUE` for two of `CLUE_APT_MEDICATION_MISSING`, `CLUE_APT_BLOOD_OLD`, `CLUE_APT_PASSPORT_MISSING` on a successful careful search, one on a failed or rushed search;
- may unlock `CON_STAGED_DISAPPEARANCE` later.

**Variants**

| `variant_key` | `condition` | `grants` |
|---|---|---|
| `careful_medication_blood` | successful careful search; categories medication and blood | `GRANT_CLUE(CLUE_APT_MEDICATION_MISSING)`, `GRANT_CLUE(CLUE_APT_BLOOD_OLD)` |
| `careful_medication_passport` | successful careful search; categories medication and passport | `GRANT_CLUE(CLUE_APT_MEDICATION_MISSING)`, `GRANT_CLUE(CLUE_APT_PASSPORT_MISSING)` |
| `careful_blood_passport` | successful careful search; categories blood and passport | `GRANT_CLUE(CLUE_APT_BLOOD_OLD)`, `GRANT_CLUE(CLUE_APT_PASSPORT_MISSING)` |
| `rushed_medication` | failed or rushed search; one category medication | `GRANT_CLUE(CLUE_APT_MEDICATION_MISSING)` |
| `rushed_blood` | failed or rushed search; one category blood | `GRANT_CLUE(CLUE_APT_BLOOD_OLD)` |
| `rushed_passport` | failed or rushed search; one category passport | `GRANT_CLUE(CLUE_APT_PASSPORT_MISSING)` |

**Node type:** `INTERMEDIATE`

**Outgoing**

- `EVT_114_NEIGHBOUR_INTERVIEW`;
- `EVT_115_SERVICE_CORRIDOR`;
- `EVT_150_REGROUP_ONE`.
### `EVT_114_NEIGHBOUR_INTERVIEW`


**Backbone:** `ARC_120` (apartment cluster)
**Cost:** 10 minutes

**Reveals**

- hooded person exited rear lane;
- body size and gait may match Elias rather than an attacker;
- crash was heard after the sighting.

**State changes**

- `GRANT_CLUE(CLUE_NEIGHBOUR_EXIT_BEFORE_CRASH)`;
- grants nothing toward `P_HARBOR` until combined with transit evidence.

**Node type:** `INTERMEDIATE`

**Outgoing**

- `EVT_113_APARTMENT_SEARCH`;
- `EVT_115_SERVICE_CORRIDOR`;
- `EVT_150_REGROUP_ONE`.
### `EVT_115_SERVICE_CORRIDOR`


**Backbone:** `ARC_120` (apartment cluster)
**Cost:** 15 minutes

**Entry**

- available through shared laundry room;
- no lockpick dependency.

**Reveals**

- latch disturbed from inside;
- damp fibre trace;
- route bypasses front police pickup.

**State changes**

- `GRANT_CLUE(CLUE_APT_SERVICE_LATCH)`;
- if combined with either missing medication or neighbour timing, unlocks staged-disappearance deduction.

**Failure transformation**

A failed perception check still reveals that the corridor exists, but not the fibre trace. Mina can later confirm the latch direction.

**Check:** `CHK_115_PERCEPTION` (`17_CHECK_REGISTER.md`) — Medium (DC 10); see MBD-01 resolution procedure.

**Variants**

| `variant_key` | `condition` | `grants` |
|---|---|---|
| `perception_success` | perception check succeeds | `GRANT_CLUE(CLUE_APT_SERVICE_LATCH)` including fibre trace |
| `perception_failure` | perception check fails | corridor route known; latch direction confirmable later via Mina; no fibre trace |

**Node type:** `INTERMEDIATE`

**Outgoing**

- `EVT_113_APARTMENT_SEARCH`;
- `EVT_114_NEIGHBOUR_INTERVIEW`;
- `EVT_150_REGROUP_ONE`.

---

## 4. Player 2 opening branch

**Node type:** `INTERMEDIATE`

**Outgoing**

- `EVT_113_APARTMENT_SEARCH`;
- `EVT_114_NEIGHBOUR_INTERVIEW`;
- `EVT_150_REGROUP_ONE`.
### `EVT_120_P2_NEWSROOM_ENTRY`


**Backbone:** `ARC_110`, `ARC_130` (absorbed split decision; newsroom cluster)
**Window:** 20:10-20:25  
**Location:** transit to `LOC_NEWSROOM`  
**Cost:** 15 minutes

**Node type:** `INTERMEDIATE`

**Outgoing**

- `EVT_121_NADIA_INTERVIEW`;
- `EVT_122_MARCUS_OBSERVATION`;
- `EVT_123_NEWSROOM_RECORDS`.
### `EVT_121_NADIA_INTERVIEW`


**Backbone:** `ARC_130` (newsroom cluster)
**Cost:** 15 minutes

**Core tension**

Nadia admits distrust of official protection but withholds her role in the disappearance.

**Approach outcomes**

- empathetic but evidence-focused: `T_NADIA +1`;
- moral condemnation without proof: `T_NADIA -1`;
- showing evidence of staging later unlocks fuller disclosure.

**Variants**

| `variant_key` | `condition` | `grants` |
|---|---|---|
| `approach_empathetic` | empathetic but evidence-focused interview | `T_NADIA +1` |
| `approach_condemnation` | moral condemnation without proof | `T_NADIA -1` |

**Information**

- Elias feared someone inside police;
- a contact was expected before 19:30;
- harbor-related research had occurred.

**State changes**

- `GRANT_CLUE(CLUE_NADIA_HARBOR_RESEARCH)`;
- full Signal Room disclosure remains locked.

**Node type:** `INTERMEDIATE`

**Outgoing**

- `EVT_122_MARCUS_OBSERVATION`;
- `EVT_123_NEWSROOM_RECORDS`;
- `EVT_150_REGROUP_ONE`.
### `EVT_122_MARCUS_OBSERVATION`


**Backbone:** `ARC_130` (newsroom cluster)
**Cost:** 10 minutes

**Observable facts**

- Marcus is unusually attentive to Nadia's files;
- printer debt documents are visible;
- he reacts to mention of the harbor.

**State changes**

- no clue grant. The observable facts raise suspicion and gate `EVT_240` entry leverage; they do not prove the leak.

**Node type:** `INTERMEDIATE`

**Outgoing**

- `EVT_121_NADIA_INTERVIEW`;
- `EVT_123_NEWSROOM_RECORDS`;
- `EVT_150_REGROUP_ONE`.
### `EVT_123_NEWSROOM_RECORDS`


**Backbone:** `ARC_130` (newsroom cluster)
**Cost:** 20 minutes

**Routes**

- server access with Nadia;
- archive-room search;
- office-call metadata request.

**Possible results**

- partial upload status;
- missing ferry photograph;
- Marcus accessed Nadia's account;
- deleted but recoverable office-call entry.

**State changes**

- `GRANT_CLUE(CLUE_MARCUS_ACCOUNT_ACCESS)` if the server log is read;
- `GRANT_CLUE(CLUE_MARCUS_DELETED_CALL)` if the deleted office-call entry is recovered;
- `GRANT_CLUE(CLUE_PHOTO_WINDOW_MARKS)` if missing-photo significance is identified;
- `GRANT_CLUE(CLUE_UPLOAD_RECOVERY_INSTRUCTIONS)` if upload instructions are recovered.

**Failure transformation**

Failure alerts Marcus or consumes time. At least the missing-photo gap remains observable without a technical check.

**Variants**

| `variant_key` | `condition` | `grants` |
|---|---|---|
| `grant_account_access` | server log is read | `GRANT_CLUE(CLUE_MARCUS_ACCOUNT_ACCESS)` |
| `grant_deleted_call` | deleted office-call entry is recovered | `GRANT_CLUE(CLUE_MARCUS_DELETED_CALL)` |
| `grant_photo_marks` | missing-photo significance is identified | `GRANT_CLUE(CLUE_PHOTO_WINDOW_MARKS)` |
| `grant_upload_instructions` | upload instructions are recovered | `GRANT_CLUE(CLUE_UPLOAD_RECOVERY_INSTRUCTIONS)` |
| `failure_alert` | failure transformation | missing-photo gap observable; Marcus may be alerted |

**Node type:** `INTERMEDIATE`

**Outgoing**

- `EVT_121_NADIA_INTERVIEW`;
- `EVT_122_MARCUS_OBSERVATION`;
- `EVT_150_REGROUP_ONE`.

---

## 5. First regroup

**Node type:** `INTERMEDIATE`

**Outgoing**

- `EVT_121_NADIA_INTERVIEW`;
- `EVT_122_MARCUS_OBSERVATION`;
- `EVT_150_REGROUP_ONE`.
### `EVT_150_REGROUP_ONE`


**Backbone:** `ARC_170` (1:1)
**Recommended window:** 21:20-21:40  
**Location:** selected neutral meeting point  
**Players:** both  
**Cost:** 10 minutes

**Purpose**

Transfer private clues into `SHARED_KNOWLEDGE_SET`.

**Unlock conditions**

At least one player has completed one substantial scene.

**Joint deductions**

Possible:

- `CON_STAGED_DISAPPEARANCE`;
- `CON_HARBOR_DESTINATION`;
- suspicion that Nadia knows more;
- suspicion that police procedure is compromised.

**Branch choice**

Choose two primary midgame tracks:

1. harbor destination and access;
2. police corruption;
3. medical trail;
4. Marcus/Reed operational link.

Players may split again, but each branch is independently useful.

**Node type:** `INTERMEDIATE`

**Outgoing**

- `EVT_210_HARBOR_ARCHIVE_ENTRY`;
- `EVT_211_CAFE_ORPHEUS`;
- `EVT_212_TERMINAL_RECON`;
- `EVT_220_MINA_REPORT_COMPARISON`;
- `EVT_221_CAMERA_REQUEST_AUDIT`;
- `EVT_222_PROTECTION_ORDER_AUDIT`;
- `EVT_223_ROOK_INTERVIEW`;
- `EVT_230_IRIS_WORKPLACE`;
- `EVT_231_PREPAID_PHONE_TRACE`;
- `EVT_232_MEDICAL_INTERPRETATION`;
- `EVT_240_MARCUS_PRESSURE_STAGE_ONE`;
- `EVT_242_REED_OFFICE_SEARCH`.

---

## 6. Harbor and archive branch

**Node type:** `INTERMEDIATE`

**Outgoing**

- `EVT_210_HARBOR_ARCHIVE_ENTRY`;
- `EVT_211_CAFE_ORPHEUS`;
- `EVT_212_TERMINAL_RECON`;
- `EVT_220_MINA_REPORT_COMPARISON`;
- `EVT_221_CAMERA_REQUEST_AUDIT`;
- `EVT_222_PROTECTION_ORDER_AUDIT`;
- `EVT_223_ROOK_INTERVIEW`;
- `EVT_230_IRIS_WORKPLACE`;
- `EVT_231_PREPAID_PHONE_TRACE`;
- `EVT_232_MEDICAL_INTERPRETATION`;
- `EVT_240_MARCUS_PRESSURE_STAGE_ONE`;
- `EVT_242_REED_OFFICE_SEARCH`.
### `EVT_210_HARBOR_ARCHIVE_ENTRY`


**Backbone:** Addition — no `ARC_*` origin
**Window:** before 23:20 normal access; later emergency access  
**Location:** `LOC_HARBOR_ARCHIVE`  
**Cost:** transit plus 20 minutes

**Entry routes**

- archivist cooperation;
- public historical material;
- Nadia's professional credentials;
- after-hours emergency request.

**Reveals**

- Signal Room 4B designation;
- cable-corridor map;
- window numbering system;
- battery/generator record.

**State changes**

- `GRANT_CLUE(CLUE_ARCHIVE_ROOM_INDEX)`;
- `GRANT_CLUE(CLUE_CABLE_CORRIDOR_MAP)`;
- `GRANT_CLUE(CLUE_ARCHIVE_WINDOW_NUMBERING)`;
- unlocks cable-corridor access.

**Node type:** `INTERMEDIATE`

**Outgoing**

- `EVT_211_CAFE_ORPHEUS`;
- `EVT_212_TERMINAL_RECON`;
- `EVT_300_REGROUP_TWO`.
### `EVT_211_CAFE_ORPHEUS`


**Backbone:** `ARC_140` (relocated to midgame)
**Window:** before 22:00 for full footage  
**Location:** `LOC_CAFE_ORPHEUS`  
**Cost:** transit plus 20 minutes

**Reveals**

- Elias and Nadia met;
- tide note;
- old line/power question;
- possible image of Lena nearby.

**State changes**

- `GRANT_CLUE(CLUE_CAFE_TIDE_NOTE)`;
- `GRANT_CLUE(CLUE_CAFE_OLD_LINE_QUESTION)`;
- `GRANT_CLUE(CLUE_CAFE_FOOTAGE)` while `CAFE_STATE` is `OPEN_FULL_RECORDS`;
- `T_NADIA` may fall if players interpret the meeting as betrayal without confronting her.

**Fallback**

After footage overwrite, receipt, witness testimony, and tide note remain.

**Variants**

| `variant_key` | `condition` | `grants` |
|---|---|---|
| `footage_full_records` | `CAFE_STATE` is `OPEN_FULL_RECORDS` | `GRANT_CLUE(CLUE_CAFE_FOOTAGE)` plus tide note and old-line question clues |
| `footage_after_overwrite` | after footage overwrite | receipt, witness testimony, and tide note remain; no `CLUE_CAFE_FOOTAGE` |

**Node type:** `INTERMEDIATE`

**Outgoing**

- `EVT_210_HARBOR_ARCHIVE_ENTRY`;
- `EVT_212_TERMINAL_RECON`;
- `EVT_300_REGROUP_TWO`.
### `EVT_212_TERMINAL_RECON`


**Backbone:** Addition — no `ARC_*` origin
**Window:** 21:30 onward  
**Location:** `LOC_TERMINAL_EXT`  
**Cost:** transit plus 15 minutes

**Reveals depending on time**

- fresh access trace;
- medical packaging;
- vehicle residue;
- generator vibration;
- storm-affected routes.

**State changes**

- `GRANT_CLUE(CLUE_GENERATOR_TRACE)`;
- `GRANT_CLUE(CLUE_MEDICAL_SUPPLY_TRAIL)` if medical packaging is found;
- `GRANT_CLUE(CLUE_TERMINAL_ACCESS_TRACE)` if vehicle or access trace is linked;
- may expose players to Reed or Rook later.

This node does not permit blind discovery of the room without at least one identifier or route clue.

**Variants**

| `variant_key` | `condition` | `grants` |
|---|---|---|
| `generator_only` | default reconnaissance | `GRANT_CLUE(CLUE_GENERATOR_TRACE)` |
| `generator_and_medical` | medical packaging found | `GRANT_CLUE(CLUE_GENERATOR_TRACE)`, `GRANT_CLUE(CLUE_MEDICAL_SUPPLY_TRAIL)` |
| `generator_and_access_trace` | vehicle or access trace linked | `GRANT_CLUE(CLUE_GENERATOR_TRACE)`, `GRANT_CLUE(CLUE_TERMINAL_ACCESS_TRACE)` |
| `generator_medical_and_access` | medical packaging and access trace both found | `GRANT_CLUE(CLUE_GENERATOR_TRACE)`, `GRANT_CLUE(CLUE_MEDICAL_SUPPLY_TRAIL)`, `GRANT_CLUE(CLUE_TERMINAL_ACCESS_TRACE)` |

**Node type:** `INTERMEDIATE`

**Outgoing**

- `EVT_210_HARBOR_ARCHIVE_ENTRY`;
- `EVT_211_CAFE_ORPHEUS`;
- `EVT_300_REGROUP_TWO`.

---

## 7. Police corruption branch

**Node type:** `INTERMEDIATE`

**Outgoing**

- `EVT_210_HARBOR_ARCHIVE_ENTRY`;
- `EVT_211_CAFE_ORPHEUS`;
- `EVT_300_REGROUP_TWO`.
### `EVT_220_MINA_REPORT_COMPARISON`


**Backbone:** `ARC_240` (Mina evidence preservation)
**Window:** 21:30 onward  
**Location:** remote, police annex, or secure meeting  
**Cost:** 15 minutes

**Entry**

- `T_MINA >= +1`; or
- present a contradiction from apartment evidence.

**Reveals**

- original report differs from the filed version;
- modification occurred after Rook took control.

**State changes**

- `GRANT_CLUE(CLUE_ROOK_REPORT_ALTERED)`;
- `T_MINA +1` if her identity is protected.

**Node type:** `INTERMEDIATE`

**Outgoing**

- `EVT_221_CAMERA_REQUEST_AUDIT`;
- `EVT_222_PROTECTION_ORDER_AUDIT`;
- `EVT_223_ROOK_INTERVIEW`;
- `EVT_300_REGROUP_TWO`.
### `EVT_221_CAMERA_REQUEST_AUDIT`


**Backbone:** `ARC_240` (Mina evidence preservation)
**Cost:** 20 minutes

**Routes**

- Mina's help;
- public request metadata;
- newsroom source;
- external city-camera administrator.

**Reveals**

- camera search initiated before formal authorization.

**State changes**

- `GRANT_CLUE(CLUE_ROOK_CAMERA_UNAUTHORIZED)`;
- `A_ROOK_PLAYERS +1` if queried through police channels.

**Node type:** `INTERMEDIATE`

**Outgoing**

- `EVT_220_MINA_REPORT_COMPARISON`;
- `EVT_222_PROTECTION_ORDER_AUDIT`;
- `EVT_223_ROOK_INTERVIEW`;
- `EVT_300_REGROUP_TWO`.
### `EVT_222_PROTECTION_ORDER_AUDIT`


**Backbone:** Addition — no `ARC_*` origin
**Cost:** 20 minutes

**Reveals**

- witness-transfer paperwork contains a timing or origin inconsistency;
- Rook's office generated or amended it.

**State changes**

- `GRANT_CLUE(CLUE_ROOK_PROTECTION_ORDER_FALSE)`;
- combined with report comparison allows private operational conclusion.

**Node type:** `INTERMEDIATE`

**Outgoing**

- `EVT_220_MINA_REPORT_COMPARISON`;
- `EVT_221_CAMERA_REQUEST_AUDIT`;
- `EVT_223_ROOK_INTERVIEW`;
- `EVT_300_REGROUP_TWO`.
### `EVT_223_ROOK_INTERVIEW`


**Backbone:** `ARC_200` (1:1 on content)
**Window:** after first contact or at Rook's initiative  
**Cost:** 15 minutes

**Purpose**

Give Rook a fair opportunity to misdirect without narrator dishonesty.

**Rook's tactics**

- offers cooperation;
- frames Lena as dangerous;
- demands surrender of evidence;
- asks what players know.

**Player risk**

Revealing the terminal or room raises antagonist awareness.

**No confession path**

Rook cannot be talked into confessing. Contradictions may strengthen player suspicion but require external evidence.

**Node type:** `INTERMEDIATE`

**Outgoing**

- `EVT_220_MINA_REPORT_COMPARISON`;
- `EVT_221_CAMERA_REQUEST_AUDIT`;
- `EVT_222_PROTECTION_ORDER_AUDIT`;
- `EVT_300_REGROUP_TWO`.

---

## 8. Medical trail branch

**Node type:** `INTERMEDIATE`

**Outgoing**

- `EVT_220_MINA_REPORT_COMPARISON`;
- `EVT_221_CAMERA_REQUEST_AUDIT`;
- `EVT_222_PROTECTION_ORDER_AUDIT`;
- `EVT_300_REGROUP_TWO`.
### `EVT_230_IRIS_WORKPLACE`


**Backbone:** `ARC_220` (Iris trail)
**Window:** 21:30 onward  
**Location:** `LOC_IRIS_WORK`  
**Cost:** transit plus 20 minutes

**Reveals**

- trauma supplies missing;
- Iris left after a call;
- supplies selected for serious head injury;
- vehicle direction toward harbor district.

**State changes**

- `GRANT_CLUE(CLUE_IRIS_SUPPLY_SELECTION)`;
- `GRANT_CLUE(CLUE_IRIS_DIRECTION_HARBOR)`;
- `GRANT_CLUE(CLUE_MEDICAL_SUPPLY_TRAIL)`;
- may increase Rook awareness if police records are used.

**Node type:** `INTERMEDIATE`

**Outgoing**

- `EVT_231_PREPAID_PHONE_TRACE`;
- `EVT_232_MEDICAL_INTERPRETATION`;
- `EVT_300_REGROUP_TWO`.
### `EVT_231_PREPAID_PHONE_TRACE`


**Backbone:** `ARC_220` (Iris trail)
**Cost:** 20 minutes

**Routes**

- telecom source;
- call timing from workplace;
- taxi-dispatch record;
- consensual access through Mina.

**Reveals**

- Lena contacted Iris after the terminal confrontation;
- contact occurred after Elias reached the harbor.

**State changes**

- `GRANT_CLUE(CLUE_LENA_CALLED_IRIS_AFTER_INJURY)`;
- `GRANT_CLUE(CLUE_ELIAS_ARRIVED_BEFORE_LENA)`;
- does not reveal exact room by itself.

**Node type:** `INTERMEDIATE`

**Outgoing**

- `EVT_230_IRIS_WORKPLACE`;
- `EVT_232_MEDICAL_INTERPRETATION`;
- `EVT_300_REGROUP_TWO`.
### `EVT_232_MEDICAL_INTERPRETATION`


**Backbone:** `ARC_220` (Iris trail)
**Cost:** 5-10 minutes

**Entry**

- medical-supply evidence or later observation of Elias.

**Reveals**

- likely head trauma;
- delay is dangerous;
- definitive hospital treatment is necessary.

**State changes**

- `GRANT_CLUE(CLUE_IRIS_ASSESSMENT)`;
- `GRANT_CLUE(CLUE_MEDICAL_REFERENCE)`;
- `CON_MEDICAL_EMERGENCY` unlocks at `P_MEDICAL >= 2`, or automatically on entering `EVT_330`.

**Node type:** `INTERMEDIATE`

**Outgoing**

- `EVT_230_IRIS_WORKPLACE`;
- `EVT_231_PREPAID_PHONE_TRACE`;
- `EVT_300_REGROUP_TWO`.

---

## 9. Marcus and Reed branch

**Node type:** `INTERMEDIATE`

**Outgoing**

- `EVT_230_IRIS_WORKPLACE`;
- `EVT_231_PREPAID_PHONE_TRACE`;
- `EVT_300_REGROUP_TWO`.
### `EVT_240_MARCUS_PRESSURE_STAGE_ONE`


**Backbone:** `ARC_230` (Marcus disclosure ladder)
**Cost:** 15 minutes

**Entry leverage**

At least one of:

- account-access evidence;
- deleted-call evidence;
- payment context;
- missing photograph.

**Outcome**

Marcus gives a partial admission only:

- confirms he discussed Nadia's work;
- denies knowing the exact room;
- identifies an intermediary only if pressure is credible.

**State changes**

- no clue grant. The partial admission opens `EVT_241` entry leverage;
- possible `T_MARCUS +1` from -1 toward neutral.

**Node type:** `INTERMEDIATE`

**Outgoing**

- `EVT_241_MARCUS_FULL_DISCLOSURE`;
- `EVT_242_REED_OFFICE_SEARCH`;
- `EVT_300_REGROUP_TWO`.
### `EVT_241_MARCUS_FULL_DISCLOSURE`


**Backbone:** `ARC_230` (Marcus disclosure ladder)
**Cost:** 20 minutes, the full structured interview cost in `04_TIME_COST_MATRIX.md` § 2

**Entry**

Requires two independent leverage classes and one self-preservation trigger:

- proof Krell is preparing to blame him;
- Nadia confrontation;
- recovered payment/call record;
- intermediary meeting consequence.

**Outcome**

Marcus reveals the harbor-direction leak and transfer-time disclosure.

**State changes**

- `GRANT_CLUE(CLUE_MARCUS_CONFESSION)`;
- `MARCUS_CONFESSED` set true;
- may expose route to Reed/Krell operations;
- does not directly prove Rook's corruption.

**Node type:** `INTERMEDIATE`

**Outgoing**

- `EVT_242_REED_OFFICE_SEARCH`;
- `EVT_243_REED_NEGOTIATION`;
- `EVT_300_REGROUP_TWO`.
### `EVT_242_REED_OFFICE_SEARCH`


**Backbone:** `ARC_210` (1:1)
**Window:** state-dependent  
**Location:** `LOC_REED_OFFICE`  
**Cost:** transit plus 20 minutes

**Reveals**

Possible routes:

- decoy hardware key;
- failed decryption attempt;
- harbor residue;
- Krell's recovery instruction;
- message shifting blame onto Reed.

**State changes**

- `GRANT_CLUE(CLUE_REED_DECOY_KEY)`;
- `GRANT_CLUE(CLUE_REED_HARBOR_RESIDUE)`;
- `GRANT_CLUE(CLUE_KRELL_RECOVERY_MESSAGE)`;
- `GRANT_CLUE(CLUE_DECOY_LIMITED_CONTENT)` if the failed decryption attempt is read;
- unlocks Reed leverage.

**Failure transformation**

If office has been searched by Krell's people, players still find residue, device traces, or deleted-message metadata. The strongest physical evidence may be gone, producing a weaker route rather than a dead end.

**Variants**

| `variant_key` | `condition` | `grants` |
|---|---|---|
| `search_intact` | office not yet searched by Krell's people | full clue set in **State changes** |
| `search_after_krell` | office searched by Krell's people | residue, device traces, or deleted-message metadata only; strongest physical evidence may be absent |

**Node type:** `INTERMEDIATE`

**Outgoing**

- `EVT_240_MARCUS_PRESSURE_STAGE_ONE`;
- `EVT_243_REED_NEGOTIATION`;
- `EVT_300_REGROUP_TWO`.
### `EVT_243_REED_NEGOTIATION`


**Backbone:** Addition — no `ARC_*` origin
**Window:** late midgame or terminal act  
**Cost:** 10-20 minutes

**Entry leverage**

At least two of:

- proof decoy key tracks him;
- proof Krell is blaming him;
- evidence linking him to terminal;
- credible protection through Mina.

**Outcome levels**

- no leverage: denial and flight;
- moderate leverage: admits terminal confrontation;
- strong leverage: identifies Krell instruction and Rook connection known to him.

**State changes**

- `GRANT_CLUE(CLUE_REED_CONFRONTATION_ADMISSION)` at moderate leverage or better;
- `GRANT_CLUE(CLUE_REED_PARTIAL_ADMISSION)` at moderate leverage or better;
- `GRANT_CLUE(CLUE_REED_NAMES_ROOK_LINK)` at strong leverage;
- `REED_COOPERATED` set true at strong leverage.

No generic persuasion roll unlocks full disclosure.

**Variants**

| `variant_key` | `condition` | `grants` |
|---|---|---|
| `no_leverage` | fewer than two leverage factors | denial and flight |
| `moderate_leverage` | at least two leverage factors | `GRANT_CLUE(CLUE_REED_CONFRONTATION_ADMISSION)`, `GRANT_CLUE(CLUE_REED_PARTIAL_ADMISSION)` |
| `strong_leverage` | moderate leverage plus credible protection through Mina or equivalent | moderate grants plus `GRANT_CLUE(CLUE_REED_NAMES_ROOK_LINK)`, `REED_COOPERATED` set true |

**Node type:** `INTERMEDIATE`

**Outgoing**

- `EVT_241_MARCUS_FULL_DISCLOSURE`;
- `EVT_242_REED_OFFICE_SEARCH`;
- `EVT_300_REGROUP_TWO`.

---

## 10. Second regroup

**Node type:** `INTERMEDIATE`

**Outgoing**

- `EVT_300_REGROUP_TWO`;
- `EVT_420_REED_OR_ROOK_CONFRONTATION`.
### `EVT_300_REGROUP_TWO`


**Backbone:** `ARC_270` (1:1)
**Deadline:** recommended no later than 23:15  
**Cost:** 10 minutes

**Purpose**

Combine:

- exact terminal route;
- room identifier;
- medical urgency;
- degree of Rook compromise;
- rescue-control options;
- evidence-transfer status.

**Minimum forward state**

The team must leave regroup with at least one route toward each:

- finding Elias;
- arranging rescue;
- preserving or transferring evidence.

If one is absent, a late failsafe branch remains but costs time or ending quality.

**Decision**

Choose final-act assignments.

**Node type:** `INTERMEDIATE`

**Outgoing**

- `EVT_310_CABLE_CORRIDOR_ENTRY`;
- `EVT_311_NORTH_GATE_ENTRY`;
- `EVT_312_DRAINAGE_ENTRY`;
- `EVT_313_EMERGENCY_ENTRY`;
- `EVT_314_MAIN_ENTRY_CONFRONTATION`.

---

## 11. Terminal access nodes

**Node type:** `INTERMEDIATE`

**Outgoing**

- `EVT_310_CABLE_CORRIDOR_ENTRY`;
- `EVT_311_NORTH_GATE_ENTRY`;
- `EVT_312_DRAINAGE_ENTRY`;
- `EVT_313_EMERGENCY_ENTRY`;
- `EVT_314_MAIN_ENTRY_CONFRONTATION`.
### `EVT_310_CABLE_CORRIDOR_ENTRY`


**Backbone:** `ARC_300` (terminal route selection)
**Entry**

- route map or trusted guide.

**Cost:** 15 minutes

**Risks**

- narrow passage;
- delayed communication;
- possible separation.

**Node type:** `INTERMEDIATE`

**Outgoing**

- `EVT_330_FIND_SIGNAL_4B`;
- `EVT_314_MAIN_ENTRY_CONFRONTATION`.
### `EVT_311_NORTH_GATE_ENTRY`


**Backbone:** `ARC_300` (terminal route selection)
**Entry**

- maintenance record;
- archivist clue;
- physical recon.

**Cost:** 15-25 minutes depending on hostile presence.

**State changes**

- `GRANT_CLUE(CLUE_NORTH_GATE_RECORD)`;
- `TERMINAL_ROUTES_KNOWN` gains `NORTH_GATE`.

**Node type:** `INTERMEDIATE`

**Outgoing**

- `EVT_330_FIND_SIGNAL_4B`;
- `EVT_314_MAIN_ENTRY_CONFRONTATION`.
### `EVT_312_DRAINAGE_ENTRY`


**Backbone:** `ARC_300` (terminal route selection)
**Window:** only before 23:30  
**Cost:** 20 minutes

**Risk**

Fast but weather-sensitive. Failure returns player to exterior with lost time, not permanent entrapment.

**State changes**

- `GRANT_CLUE(CLUE_DRAINAGE_TIDE_WINDOW)`.

**Node type:** `INTERMEDIATE`

**Outgoing**

- `EVT_330_FIND_SIGNAL_4B`;
- `EVT_314_MAIN_ENTRY_CONFRONTATION`.
### `EVT_313_EMERGENCY_ENTRY`


**Backbone:** `ARC_300` (terminal route selection)
**Entry**

- Mina or trusted emergency support;
- sufficient medical evidence.

**Cost:** 10-20 minutes

**Risk**

May expose location to Rook unless his control is already challenged.

**State changes**

- `GRANT_CLUE(CLUE_EMERGENCY_ENTRY_AUTH)`;
- `TERMINAL_ROUTES_KNOWN` gains `EMERGENCY`.

**Node type:** `INTERMEDIATE`

**Outgoing**

- `EVT_330_FIND_SIGNAL_4B`;
- `EVT_314_MAIN_ENTRY_CONFRONTATION`.
### `EVT_314_MAIN_ENTRY_CONFRONTATION`


**Backbone:** `ARC_300` (terminal route selection)
**Cost:** 10-20 minutes, the risky alternate access cost in `04_TIME_COST_MATRIX.md` § 2

**Entry**

Always available in late final act.

**Purpose**

Guaranteed but dangerous route. It may trigger Reed, police, or both.

This is the final anti-soft-lock access route.

**Node type:** `INTERMEDIATE`

**Outgoing**

- `EVT_330_FIND_SIGNAL_4B`.

---

## 12. Signal Room discovery

**Node type:** `INTERMEDIATE`

**Outgoing**

- `EVT_330_FIND_SIGNAL_4B`;
- `EVT_420_REED_OR_ROOK_CONFRONTATION`.
### `EVT_330_FIND_SIGNAL_4B`


**Backbone:** `ARC_340` (Signal Room discovery)
**Entry**

- room identifier plus access route;
- or late failsafe with generator/cable trace.

**Cost:** 10 minutes

**Reveals**

- Elias is alive;
- Lena and Iris concealed him;
- primary ledger remains in the room;
- medical crisis is immediate.

**State changes**

- `ROOM_4B_STATE = FOUND_SECURE` or `FOUND_CONTESTED`;
- `GRANT_CLUE(CLUE_ELIAS_VOMITING_CONFUSION)`;
- `GRANT_CLUE(CLUE_ELIAS_UNEQUAL_PUPILS)`;
- `GRANT_CLUE(CLUE_ELIAS_FRAGMENT_PASSPHRASE)` while `ELIAS_STATE` is not `CRITICAL_UNRESPONSIVE`;
- `CON_MEDICAL_EMERGENCY` automatic on entry, independent of `P_MEDICAL`;
- unlocks rescue/evidence parallel tasks.

**Variants**

| `variant_key` | `condition` | `grants` |
|---|---|---|
| `elias_responsive` | `ELIAS_STATE` is not `CRITICAL_UNRESPONSIVE` | includes `GRANT_CLUE(CLUE_ELIAS_FRAGMENT_PASSPHRASE)` |
| `elias_critical_unresponsive` | `ELIAS_STATE` is `CRITICAL_UNRESPONSIVE` | medical and room clues only; no passphrase fragment |

**Node type:** `INTERMEDIATE`

**Outgoing**

- `EVT_331_LENA_IRIS_NEGOTIATION`;
- `EVT_400_RESCUE_CONTROL`;
- `EVT_410_LEDGER_RECOVERY`;
- `EVT_420_REED_OR_ROOK_CONFRONTATION`.
### `EVT_331_LENA_IRIS_NEGOTIATION`


**Backbone:** `ARC_340` (Signal Room discovery)
**Cost:** 10 minutes

**Entry**

Always upon discovery unless hostile interruption is active.

**Cooperation conditions**

Players need:

- evidence or credible basis that Rook is compromised;
- a rescue plan not controlled solely by Rook.

**Outcomes**

- cooperation;
- partial cooperation with delay;
- barricade if players demand immediate surrender to Rook.

No single social check overrides their core fear.

**Variants**

| `variant_key` | `condition` | `grants` |
|---|---|---|
| `cooperation` | credible Rook compromise and rescue plan not Rook-controlled | cooperation |
| `partial_cooperation_delay` | partial trust only | partial cooperation with delay |
| `barricade` | players demand immediate surrender to Rook | barricade |

**Node type:** `INTERMEDIATE`

**Outgoing**

- `EVT_400_RESCUE_CONTROL`;
- `EVT_410_LEDGER_RECOVERY`;
- `EVT_420_REED_OR_ROOK_CONFRONTATION`.

---

## 13. Final parallel tasks

**Node type:** `INTERMEDIATE`

**Outgoing**

- `EVT_400_RESCUE_CONTROL`;
- `EVT_410_LEDGER_RECOVERY`;
- `EVT_420_REED_OR_ROOK_CONFRONTATION`.
### `EVT_400_RESCUE_CONTROL`


**Backbone:** `ARC_240`, `ARC_400` (Mina evidence preservation; trusted rescue validation)
Possible routes:

- Mina-secured ambulance;
- independent hospital/paramedic route;
- public exposure limiting Rook;
- private transport fallback.

**Cost:** route-dependent.

**Success quality**

Depends on time, trust, and whether hostile actors control the exterior.

**Node type:** `INTERMEDIATE`

**Outgoing**

- `EVT_410_LEDGER_RECOVERY`;
- `EVT_420_REED_OR_ROOK_CONFRONTATION`;
- `EVT_430_COMPLETE_TRANSFER`;
- `EVT_440_FINAL_PUBLIC_POSITION`;
- `EVT_900_RESOLVE_ENDING`.
### `EVT_410_LEDGER_RECOVERY`


**Backbone:** `ARC_420` (evidence transfer)
Tasks:

- identify primary versus decoy;
- establish `CON_PASSPHRASE_ACCESS`, by the passphrase itself or by the documented reset;
- combine code fragments;
- preserve authenticated copy.

**State changes**

- `GRANT_CLUE(CLUE_HASH_MISMATCH)` when primary and decoy are compared.

**No instant success**

The complete transfer requires the correct key, code, and sufficient time.

**Node type:** `INTERMEDIATE`

**Outgoing**

- `EVT_420_REED_OR_ROOK_CONFRONTATION`;
- `EVT_430_COMPLETE_TRANSFER`;
- `EVT_440_FINAL_PUBLIC_POSITION`.
### `EVT_420_REED_OR_ROOK_CONFRONTATION`


**Backbone:** `ARC_320` (off-screen hostile convergence)
Triggered by antagonist awareness and clock.

Possible player roles:

- delay hostile entry;
- negotiate Reed's cooperation;
- expose Rook to Mina/public;
- conceal evacuation route;
- preserve evidence copy.

**Node type:** `INTERMEDIATE`

**Outgoing**

- `EVT_400_RESCUE_CONTROL`;
- `EVT_410_LEDGER_RECOVERY`;
- `EVT_430_COMPLETE_TRANSFER`;
- `EVT_440_FINAL_PUBLIC_POSITION`;
- `EVT_900_RESOLVE_ENDING`.
### `EVT_430_COMPLETE_TRANSFER`


**Backbone:** `ARC_420` (evidence transfer)
**Entry**

- primary key available;
- `CON_PASSPHRASE_ACCESS` established;
- recovery code complete;
- Nadia upload accessible;
- clock no later than 01:45 for reliable completion.

**Quality tiers**

- Route B of `CON_PASSPHRASE_ACCESS` preserves authentication and permits full authenticated transfer;
- Route A performs a logged reset, costs 20 additional minutes, and caps the outcome at partial official evidence.

**Outcomes**

- full authenticated transfer;
- partial transfer;
- intercepted attempt;
- public leak fallback.

**Variants**

| `variant_key` | `condition` | `grants` |
|---|---|---|
| `full_authenticated_transfer` | Route B passphrase access and complete requirements met | full authenticated transfer |
| `partial_transfer` | logged reset or incomplete authentication | partial transfer |
| `intercepted_attempt` | hostile interception succeeds | intercepted attempt |
| `public_leak_fallback` | transfer blocked with public exposure route | public leak fallback |

**Node type:** `INTERMEDIATE`

**Outgoing**

- `EVT_440_FINAL_PUBLIC_POSITION`;
- `EVT_900_RESOLVE_ENDING`.
### `EVT_440_FINAL_PUBLIC_POSITION`


**Backbone:** `ARC_440` (1:1)
Players choose what they are prepared to assert publicly.

A target-specific accusation option appears only if its evidence gate is met. Unsupported suspicion may be voiced, but cannot compile into a prosecution-victory ending.

**Accusation options**

Each option sets `PUBLIC_ACCUSATION_TARGET` and advances to `EVT_900_RESOLVE_ENDING`. Wrong or unsupported accusations dispatch to `EVT_907_END_WRONG_ACCUSATION` via `EVAL_ENDING` when the gate is not met or the rebuttal category applies.

| Option key | Target | Evidence gate (`14` § 5) | Rebuttal category when wrong (`14` § 7) | Rebuttal fact (`07` § 3) |
|---|---|---|---|---|
| `accuse_rook` | `NPC_ROOK` | `CON_ROOK_PUBLICLY_PROVABLE` | missing physical presence; inability to explain police manipulation | Rook requires authenticated public proof |
| `accuse_krell_vale` | `NPC_KRELL`, `NPC_VALE` | `FULL_LEDGER_TRANSFERRED`, or multiple authenticated financial and contact routes | inability to explain financial architecture | Reed/Krell/Vale scope distinction |
| `accuse_marcus` | `NPC_MARCUS` | `CON_MARCUS_LEAK_PROVABLE` | inability to explain police manipulation | leak is real but cannot explain police-system manipulation |
| `accuse_reed` | `NPC_REED` | `CON_REED_CAUSED_CONFRONTATION` | confession scope smaller than accusation scope; inability to explain financial architecture | caused confrontation but lacks authority and financial architecture |
| `accuse_lena` | `NPC_LENA` | obstruction if supported; `CON_LENA_PROTECTING` contradicts sole-architect claim | evidence showing protective rather than initiating conduct | timing and medical trail show concealment after injury, not initial abduction |
| `accuse_nadia` | `NPC_NADIA` | obstruction if supported; not sole architect without contradictory failure text | evidence showing protective rather than initiating conduct; wrong timeline | helped stage disappearance but did not transmit location to Reed |
| `accuse_unsupported` | none | none (arbitrary suspicion) | wrong timeline; credibility collapse per `05_CORE_EVENT_GRAPH.md` `ARC_440` | no specific rebuttal fact — unsupported public claim |

**Node type:** `INTERMEDIATE`

**Outgoing**

- `EVT_900_RESOLVE_ENDING` (all accusation options).

---

## 14. Ending dispatch

**Node type:** `INTERMEDIATE`

**Outgoing**

- `EVT_900_RESOLVE_ENDING`.
### `EVT_900_RESOLVE_ENDING`


**Backbone:** `ARC_900` (ending dispatch)
Reads:

- Elias medical outcome;
- evidence-transfer status;
- rescue control;
- Rook proof level;
- broader conspiracy proof;
- public accusation;
- ally states.

Dispatches to the eight terminal nodes below. Trigger conditions and the priority order that selects between them are owned by `14_ENDING_TRIGGER_MATRIX.md`; narrative outcome text is owned by `../06_ENDING_FRAMEWORK.md`. This section owns node identity, type and edges only.

**Node type:** `INTERMEDIATE`

**Outgoing**

- `EVT_901_END_WITNESS_SPEAKS`;
- `EVT_902_END_EVIDENCE_WITHOUT_WITNESS`;
- `EVT_903_END_LIFE_SAVED_TRUTH_DELAYED`;
- `EVT_904_END_PROTECTIVE_CUSTODY`;
- `EVT_905_END_PUBLIC_LEAK`;
- `EVT_906_END_SILENT_TERMINAL`;
- `EVT_907_END_WRONG_ACCUSATION`;
- `EVT_908_END_FRACTURED_TRUTH`.

### `EVT_901_END_WITNESS_SPEAKS`


**Backbone:** `ARC_900` (terminal node)
**Node type:** `TERMINAL`
**Terminal type:** `VICTORY`
**Ending family:** `END_WITNESS_SPEAKS`
**Outgoing:** None

### `EVT_902_END_EVIDENCE_WITHOUT_WITNESS`


**Backbone:** `ARC_900` (terminal node)
**Node type:** `TERMINAL`
**Terminal type:** `PARTIAL_SUCCESS`
**Ending family:** `END_EVIDENCE_WITHOUT_WITNESS`
**Outgoing:** None

### `EVT_903_END_LIFE_SAVED_TRUTH_DELAYED`


**Backbone:** `ARC_900` (terminal node)
**Node type:** `TERMINAL`
**Terminal type:** `PARTIAL_SUCCESS`
**Ending family:** `END_LIFE_SAVED_TRUTH_DELAYED`
**Outgoing:** None

### `EVT_904_END_PROTECTIVE_CUSTODY`


**Backbone:** `ARC_900` (terminal node)
**Node type:** `TERMINAL`
**Terminal type:** `NARRATIVE_FAILURE`
**Ending family:** `END_PROTECTIVE_CUSTODY`
**Outgoing:** None

### `EVT_905_END_PUBLIC_LEAK`


**Backbone:** `ARC_900` (terminal node)
**Node type:** `TERMINAL`
**Terminal type:** `PARTIAL_SUCCESS`
**Ending family:** `END_PUBLIC_LEAK`
**Outgoing:** None

### `EVT_906_END_SILENT_TERMINAL`


**Backbone:** `ARC_900` (terminal node)
**Node type:** `TERMINAL`
**Terminal type:** `TIME_EXPIRED`
**Ending family:** `END_SILENT_TERMINAL`
**Outgoing:** None

The terminating condition is temporal: Elias is never located, or never rescued in time. A terminal type classifies why the branch terminates, not what happens to a character. Elias's death is narrative outcome, owned by `../06_ENDING_FRAMEWORK.md`, and his medical state is read from `ELIAS_STATE`.

### `EVT_907_END_WRONG_ACCUSATION`


**Backbone:** `ARC_900` (terminal node)
**Node type:** `TERMINAL`
**Terminal type:** `CASE_UNRESOLVED`
**Ending family:** `END_WRONG_ACCUSATION`
**Outgoing:** None

### `EVT_908_END_FRACTURED_TRUTH`


**Backbone:** `ARC_900` (terminal node)
**Node type:** `TERMINAL`
**Terminal type:** `PARTIAL_SUCCESS`
**Ending family:** `END_FRACTURED_TRUTH`
**Outgoing:** None

Reachable only in two-player mode, because `../06_ENDING_FRAMEWORK.md` § END-08 requires two players to reach incompatible final decisions. Reachability is therefore evaluated per declared play mode.

## 15. Variable writes by node

Every non-progress variable write performed by a node is declared here. Variables are owned by `01_WORLD_STATE_VARIABLES.md`; this table is the node-side declaration of the writers that document lists.

Every node writes `CLOCK` through its declared time cost, and writes `P1_AVAILABLE_AT` or `P2_AVAILABLE_AT` according to the eligible player. Those two writes are universal and are not repeated per row.

| Node | Writes |
|---|---|
| `EVT_100_SHARED_BRIEFING` | `P1_LOCATION`, `P2_LOCATION` |
| `EVT_110_P1_APARTMENT_APPROACH` | `P1_LOCATION` |
| `EVT_111_MINA_FIRST_CONTACT` | `T_MINA`, `A_ROOK_PLAYERS` |
| `EVT_112_RESTRICTED_APARTMENT` | `A_ROOK_PLAYERS` |
| `EVT_120_P2_NEWSROOM_ENTRY` | `P2_LOCATION` |
| `EVT_121_NADIA_INTERVIEW` | `T_NADIA` |
| `EVT_210_HARBOR_ARCHIVE_ENTRY` | `TERMINAL_ROUTES_KNOWN` |
| `EVT_211_CAFE_ORPHEUS` | `T_NADIA` |
| `EVT_212_TERMINAL_RECON` | `TERMINAL_ROUTES_KNOWN` |
| `EVT_220_MINA_REPORT_COMPARISON` | `T_MINA` |
| `EVT_221_CAMERA_REQUEST_AUDIT` | `A_ROOK_PLAYERS` |
| `EVT_223_ROOK_INTERVIEW` | `A_ROOK_PLAYERS` |
| `EVT_240_MARCUS_PRESSURE_STAGE_ONE` | `T_MARCUS` |
| `EVT_241_MARCUS_FULL_DISCLOSURE` | `MARCUS_CONFESSED` |
| `EVT_243_REED_NEGOTIATION` | `REED_COOPERATED` |
| `EVT_311_NORTH_GATE_ENTRY` | `TERMINAL_ROUTES_KNOWN` |
| `EVT_313_EMERGENCY_ENTRY` | `TERMINAL_ROUTES_KNOWN` |
| `EVT_330_FIND_SIGNAL_4B` | `ELIAS_STATE`, `ROOM_4B_STATE` |
| `EVT_331_LENA_IRIS_NEGOTIATION` | `LENA_STATUS`, `IRIS_STATUS` |
| `EVT_400_RESCUE_CONTROL` | `ELIAS_STATE`, `ROOM_4B_STATE`, `TRUSTED_RESCUE_CONTROL`, `IRIS_STATUS` |
| `EVT_420_REED_OR_ROOK_CONFRONTATION` | `ROOM_4B_STATE`, `LENA_STATUS` |
| `EVT_430_COMPLETE_TRANSFER` | `FULL_LEDGER_TRANSFERRED`, `KRELL_VALE_EXPOSED` |
| `EVT_440_FINAL_PUBLIC_POSITION` | `A_PUBLIC`, `ROOK_EXPOSED_PUBLIC`, `KRELL_VALE_EXPOSED`, `PUBLIC_ACCUSATION_TARGET`, `PUBLIC_ACCUSATION_SUPPORT` |

Nodes not listed write no variable other than the universal clock and availability writes. Clue grants and progress totals are declared separately when the progress model is converted.

## 16. Graph integrity rules

Stated as assertions over the explicit edge set above, so each is checkable rather than aspirational.

| Assertion | How it is checked |
|---|---|
| Every node declares exactly one `NODE_TYPE` | 40 `INTERMEDIATE` plus 8 `TERMINAL`, 48 in total |
| Every `TERMINAL` node declares one `TERMINAL_TYPE` and `Outgoing: None` | § 14, eight nodes |
| No `INTERMEDIATE` node declares a `TERMINAL_TYPE` | § 14 is the only section declaring terminal types |
| Every `INTERMEDIATE` node declares at least one target | 40 nodes, each with an `Outgoing` list |
| Every `Outgoing` target resolves to a declared node | targets are drawn from the 48 declared identifiers |
| Every terminal node is reachable from `EVT_100_SHARED_BRIEFING` | `EVT_900_RESOLVE_ENDING` targets all eight, and is reached from `EVT_400`, `EVT_420`, `EVT_430` and `EVT_440` |
| No player-facing node is unreachable | every node is a target of at least one other node, except `EVT_100`, which is the entry |
| Every mandatory conclusion has at least two independent routes | `12_CLUE_DEPENDENCY_GRAPH.md` § 12 |
| Every critical location retains a late fallback entry | `EVT_314_MAIN_ENTRY_CONFRONTATION` is a target of every terminal-access node |
| Failed checks alter time, certainty, trust or awareness | failure transformations per node |
| No split player waits on information held only by the other player | `13_SPLIT_AND_REGROUP_FLOW.md` § 2 independence test |
| No NPC provides a high-risk confession through persuasion alone | `03_NPC_KNOWLEDGE_AND_DISCLOSURE.md` disclosure gates |
| No player can earn the best ending through an unsupported guess | `EVT_901` requires `CON_ROOK_PUBLICLY_PROVABLE` and a full authenticated transfer |

Off-screen nodes `EVT_801`–`EVT_804`, owned by `06_NPC_SCHEDULE_AND_PRIORITY.md` § 4, are not player-reachable and are excluded from reachability.

## 17. Identifier status

This document owns the playable `EVT_` namespace. Forty-eight identifiers are declared in §§ 2–14.

Status is assigned per `IMPLEMENTATION_PLAN.md` § 8.7: an identifier referenced at least once outside its declaring heading is `ACTIVE`; one declared but never referenced is `DEFINITION_ONLY`.

| Status | Count | Scope |
|---|---:|---|
| `ACTIVE` | 48 | playable nodes in §§ 2–14 |

Every playable node is `ACTIVE`. Each is referenced from at least one other node's `Outgoing` block, `Entry conditions`, variable-write table, or cross-document pointer.

Off-screen nodes `EVT_801`–`EVT_804` are declared in `06_NPC_SCHEDULE_AND_PRIORITY.md` § 4. All four are `ACTIVE`: `EVT_803` is referenced as a writer in `01_WORLD_STATE_VARIABLES.md`; `EVT_801`, `EVT_802` and `EVT_804` are referenced from `16_EVENT_GRAPH_MAPPING.md` and § 16 above.

No `EVT_` identifier is `DEFINITION_ONLY`, `RESERVED` or `DEPRECATED`.

## 18. Play modes (MBD-06)

Alpha 0.2c officially supports **`two_player` only**. Solo mode is intentionally deferred to a post–Alpha 0.2c production phase per `IMPLEMENTATION_PLAN.md` § 15.

| Field | Value |
|---|---|
| Declared `play_modes` | `[two_player]` (`adventures/The_Last_Witness/README.md`) |
| Validation scope | Reachability and participation audits evaluate `two_player` only |
| `EVT_908_END_FRACTURED_TRUTH` | Reachable only in `two_player` mode (§ 14); excluded from future solo artifacts |
| `Scene mode` value `Solo` | Not used on any node (§ 1c) |

**Engine note:** `engine/06_PROTOTYPE_SCOPE_AND_VALIDATION.md` § 1 and `PROTOTYPE_BRIEF.md` describe long-term solo capability. That requirement remains a future engine goal; it does not block Alpha 0.2c logic closure under `ENGINE_READINESS_PLAN.md` C6 when `play_modes: [two_player]` is declared with this documented exception.

Solo eligibility rules, merged-player routing, solo reachability graph, and solo artifact set are **not authored** and are out of scope for Milestone B.
