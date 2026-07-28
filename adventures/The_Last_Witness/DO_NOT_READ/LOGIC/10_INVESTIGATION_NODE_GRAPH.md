# DO NOT READ: Investigation Node Graph

## 1. Graph conventions

Each node has:

- immutable event key;
- availability window;
- location;
- player eligibility;
- entry conditions;
- time cost;
- information gained;
- state changes;
- failure transformation;
- outgoing routes.

The graph is not final prose. It is the authoritative gameplay skeleton from which player-facing nodes will later be compiled.

## 2. Opening nodes

### `EVT_100_SHARED_BRIEFING`

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
- `P2_LOCATION = LOC_START`;
- unlocks `EVT_110_P1_APARTMENT_APPROACH`;
- unlocks `EVT_120_P2_NEWSROOM_ENTRY`.

**Decision**

Players may:

1. split immediately;
2. investigate one branch together at the cost of losing the other branch's early access advantage.

The canonical two-player route is a split.

---

## 3. Player 1 opening branch

### `EVT_110_P1_APARTMENT_APPROACH`

**Window:** 20:10-20:25  
**Location:** transit to `LOC_ELIAS_APT`  
**Players:** Player 1, or both if chosen  
**Cost:** 15 minutes

**Entry conditions**

- `EVT_100_SHARED_BRIEFING` completed.

**State changes**

- `P1_LOCATION = LOC_ELIAS_APT`;
- Mina is still present if arrival is no later than 20:30.

**Outgoing**

- `EVT_111_MINA_FIRST_CONTACT`;
- late arrival goes to `EVT_112_RESTRICTED_APARTMENT`.

### `EVT_111_MINA_FIRST_CONTACT`

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

**Outgoing**

- `EVT_113_APARTMENT_SEARCH`;
- `EVT_114_NEIGHBOUR_INTERVIEW`;
- `EVT_115_SERVICE_CORRIDOR`.

### `EVT_112_RESTRICTED_APARTMENT`

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

### `EVT_113_APARTMENT_SEARCH`

**Cost:** 20 minutes  
**Information routes**

A successful careful search reveals two of:

- missing medication/travel preparation;
- preserved blood anomaly;
- broken-phone inconsistency;
- empty passport concealment.

A failed or rushed search reveals one suspicious category and costs an additional corroboration requirement later.

**State changes**

- `P_STAGED +1` or `+2`;
- may unlock `CON_STAGED_DISAPPEARANCE` later.

### `EVT_114_NEIGHBOUR_INTERVIEW`

**Cost:** 10 minutes

**Reveals**

- hooded person exited rear lane;
- body size and gait may match Elias rather than an attacker;
- crash was heard after the sighting.

**State changes**

- `P_STAGED +1`;
- `P_HARBOR +0` until combined with transit evidence.

### `EVT_115_SERVICE_CORRIDOR`

**Cost:** 15 minutes

**Entry**

- available through shared laundry room;
- no lockpick dependency.

**Reveals**

- latch disturbed from inside;
- damp fibre trace;
- route bypasses front police pickup.

**State changes**

- `P_STAGED +1`;
- if combined with either missing medication or neighbour timing, unlocks staged-disappearance deduction.

**Failure transformation**

A failed perception check still reveals that the corridor exists, but not the fibre trace. Mina can later confirm the latch direction.

---

## 4. Player 2 opening branch

### `EVT_120_P2_NEWSROOM_ENTRY`

**Window:** 20:10-20:25  
**Location:** transit to `LOC_NEWSROOM`  
**Cost:** 15 minutes

**Outgoing**

- `EVT_121_NADIA_INTERVIEW`;
- `EVT_122_MARCUS_OBSERVATION`;
- `EVT_123_NEWSROOM_RECORDS`.

### `EVT_121_NADIA_INTERVIEW`

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

- `P_HARBOR +1`;
- full Signal Room disclosure remains locked.

### `EVT_122_MARCUS_OBSERVATION`

**Cost:** 10 minutes

**Observable facts**

- Marcus is unusually attentive to Nadia's files;
- printer debt documents are visible;
- he reacts to mention of the harbor.

**State changes**

- `P_MARCUS +1` contextual;
- does not prove the leak.

### `EVT_123_NEWSROOM_RECORDS`

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

- `P_MARCUS +1` or `+2`;
- `P_ROOM_4B +1` if missing-photo significance identified;
- `P_CODE +1` if upload instructions recovered.

**Failure transformation**

Failure alerts Marcus or consumes time. At least the missing-photo gap remains observable without a technical check.

---

## 5. First regroup

### `EVT_150_REGROUP_ONE`

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

### `EVT_210_HARBOR_ARCHIVE_ENTRY`

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

- `P_ROOM_4B +2`;
- `P_CODE +1`;
- unlocks cable-corridor access.

### `EVT_211_CAFE_ORPHEUS`

**Window:** before 22:00 for full footage  
**Location:** `LOC_CAFE_ORPHEUS`  
**Cost:** transit plus 20 minutes

**Reveals**

- Elias and Nadia met;
- tide note;
- old line/power question;
- possible image of Lena nearby.

**State changes**

- `P_HARBOR +1` or `+2`;
- `T_NADIA` may fall if players interpret the meeting as betrayal without confronting her.

**Fallback**

After footage overwrite, receipt, witness testimony, and tide note remain.

### `EVT_212_TERMINAL_RECON`

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

- `P_ROOM_4B +1`;
- `P_REED +1` if vehicle/trace linked;
- may expose players to Reed or Rook later.

This node does not permit blind discovery of the room without at least one identifier or route clue.

---

## 7. Police corruption branch

### `EVT_220_MINA_REPORT_COMPARISON`

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

- `P_ROOK +1 procedural`;
- `T_MINA +1` if her identity is protected.

### `EVT_221_CAMERA_REQUEST_AUDIT`

**Cost:** 20 minutes

**Routes**

- Mina's help;
- public request metadata;
- newsroom source;
- external city-camera administrator.

**Reveals**

- camera search initiated before formal authorization.

**State changes**

- `P_ROOK +1 procedural`;
- `A_ROOK_PLAYERS +1` if queried through police channels.

### `EVT_222_PROTECTION_ORDER_AUDIT`

**Cost:** 20 minutes

**Reveals**

- witness-transfer paperwork contains a timing or origin inconsistency;
- Rook's office generated or amended it.

**State changes**

- `P_ROOK +1 procedural`;
- combined with report comparison allows private operational conclusion.

### `EVT_223_ROOK_INTERVIEW`

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

### `EVT_230_IRIS_WORKPLACE`

**Window:** 21:30 onward  
**Location:** `LOC_IRIS_WORK`  
**Cost:** transit plus 20 minutes

**Reveals**

- trauma supplies missing;
- Iris left after a call;
- supplies selected for serious head injury;
- vehicle direction toward harbor district.

**State changes**

- `P_MEDICAL +1`;
- `P_HARBOR +1`;
- may increase Rook awareness if police records are used.

### `EVT_231_PREPAID_PHONE_TRACE`

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

- `P_LENA_PROTECTING` represented through conclusion tags;
- `P_MEDICAL +1`;
- does not reveal exact room by itself.

### `EVT_232_MEDICAL_INTERPRETATION`

**Cost:** 5-10 minutes

**Entry**

- medical-supply evidence or later observation of Elias.

**Reveals**

- likely head trauma;
- delay is dangerous;
- definitive hospital treatment is necessary.

**State changes**

- `CON_MEDICAL_EMERGENCY` unlocks at `P_MEDICAL >= 2`, or automatically upon observing Elias's late symptoms.

---

## 9. Marcus and Reed branch

### `EVT_240_MARCUS_PRESSURE_STAGE_ONE`

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

- `P_MARCUS +1`;
- possible `T_MARCUS +1` from -1 toward neutral.

### `EVT_241_MARCUS_FULL_DISCLOSURE`

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

- `P_MARCUS` reaches full threshold;
- may expose route to Reed/Krell operations;
- does not directly prove Rook's corruption.

### `EVT_242_REED_OFFICE_SEARCH`

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

- `P_REED +2` possible;
- `P_DECOY` represented through conclusion state;
- unlocks Reed leverage.

**Failure transformation**

If office has been searched by Krell's people, players still find residue, device traces, or deleted-message metadata. The strongest physical evidence may be gone, producing a weaker route rather than a dead end.

### `EVT_243_REED_NEGOTIATION`

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

No generic persuasion roll unlocks full disclosure.

---

## 10. Second regroup

### `EVT_300_REGROUP_TWO`

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

### `EVT_310_CABLE_CORRIDOR_ENTRY`

**Entry**

- route map or trusted guide.

**Cost:** 15 minutes

**Risks**

- narrow passage;
- delayed communication;
- possible separation.

### `EVT_311_NORTH_GATE_ENTRY`

**Entry**

- maintenance record;
- archivist clue;
- physical recon.

**Cost:** 15-25 minutes depending on hostile presence.

### `EVT_312_DRAINAGE_ENTRY`

**Window:** only before 23:30  
**Cost:** 20 minutes

**Risk**

Fast but weather-sensitive. Failure returns player to exterior with lost time, not permanent entrapment.

### `EVT_313_EMERGENCY_ENTRY`

**Entry**

- Mina or trusted emergency support;
- sufficient medical evidence.

**Cost:** 10-20 minutes

**Risk**

May expose location to Rook unless his control is already challenged.

### `EVT_314_MAIN_ENTRY_CONFRONTATION`

**Cost:** 10-20 minutes, the risky alternate access cost in `04_TIME_COST_MATRIX.md` § 2

**Entry**

Always available in late final act.

**Purpose**

Guaranteed but dangerous route. It may trigger Reed, police, or both.

This is the final anti-soft-lock access route.

---

## 12. Signal Room discovery

### `EVT_330_FIND_SIGNAL_4B`

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
- `P_MEDICAL = 2`;
- `CON_MEDICAL_EMERGENCY` automatic;
- unlocks rescue/evidence parallel tasks.

### `EVT_331_LENA_IRIS_NEGOTIATION`

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

### `EVT_400_RESCUE_CONTROL`

Possible routes:

- Mina-secured ambulance;
- independent hospital/paramedic route;
- public exposure limiting Rook;
- private transport fallback.

**Cost:** route-dependent.

**Success quality**

Depends on time, trust, and whether hostile actors control the exterior.

### `EVT_410_LEDGER_RECOVERY`

Tasks:

- identify primary versus decoy;
- retrieve passphrase information;
- combine code fragments;
- preserve authenticated copy.

**No instant success**

The complete transfer requires the correct key, code, and sufficient time.

### `EVT_420_REED_OR_ROOK_CONFRONTATION`

Triggered by antagonist awareness and clock.

Possible player roles:

- delay hostile entry;
- negotiate Reed's cooperation;
- expose Rook to Mina/public;
- conceal evacuation route;
- preserve evidence copy.

### `EVT_430_COMPLETE_TRANSFER`

**Entry**

- primary key available;
- recovery code complete;
- Nadia upload accessible;
- clock no later than 01:45 for reliable completion.

**Outcomes**

- full authenticated transfer;
- partial transfer;
- intercepted attempt;
- public leak fallback.

### `EVT_440_FINAL_PUBLIC_POSITION`

Players choose what they are prepared to assert publicly.

A target-specific accusation option appears only if its evidence gate is met. Unsupported suspicion may be voiced, but cannot compile into a prosecution-victory ending.

---

## 14. Ending dispatch

### `EVT_900_RESOLVE_ENDING`

Reads:

- Elias medical outcome;
- evidence-transfer status;
- rescue control;
- Rook proof level;
- broader conspiracy proof;
- public accusation;
- ally states.

Dispatches to ending variants defined in `06_ENDING_FRAMEWORK.md` and the later terminal matrix.

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

- every mandatory conclusion has at least two independent routes;
- every critical location retains a late fallback entry;
- failed checks alter time, certainty, trust, or awareness;
- no split player waits on information held only by the other player;
- no NPC provides a high-risk confession through persuasion alone;
- no player can earn the best ending through an unsupported guess.
