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
- `Outgoing`.

`NODE_TYPE` and `Outgoing` are mandatory on every node. A node declares `Outgoing` as a list of node identifiers, or `Outgoing: None` when it is terminal. An `INTERMEDIATE` node with no outgoing target is a structural defect. A `TERMINAL` node declares exactly one `TERMINAL_TYPE` drawn from `engine/03_ARCHITECTURE.md` § 3.18 and never declares a target.

The graph is not final prose. It is the authoritative gameplay skeleton from which player-facing nodes will later be compiled.

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

**Node type:** `INTERMEDIATE`

**Outgoing**

- `EVT_440_FINAL_PUBLIC_POSITION`;
- `EVT_900_RESOLVE_ENDING`.
### `EVT_440_FINAL_PUBLIC_POSITION`


**Backbone:** `ARC_440` (1:1)
Players choose what they are prepared to assert publicly.

A target-specific accusation option appears only if its evidence gate is met. Unsupported suspicion may be voiced, but cannot compile into a prosecution-victory ending.

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
