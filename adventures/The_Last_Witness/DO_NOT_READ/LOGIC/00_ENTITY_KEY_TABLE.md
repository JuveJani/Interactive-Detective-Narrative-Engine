# DO NOT READ: Entity Key Table

## Purpose

All logic-layer documents reference immutable keys rather than display names. Display names may change during editing; keys must not.

Identifiers are frozen at creation and survive display-name changes. A key may become a historical misnomer if a character is renamed; that is accepted.

## Prefix registry

Every identifier in this adventure uses one of the prefixes below. The registry is closed and extensible only by amendment.

| Prefix | Entity | Owner |
|---|---|---|
| `NPC_` | Character | `00_ENTITY_KEY_TABLE.md` |
| `LOC_` | Location | `00_ENTITY_KEY_TABLE.md` |
| `ITEM_` | Item or evidence object | `00_ENTITY_KEY_TABLE.md` |
| `CLUE_` | Clue | `12_CLUE_DEPENDENCY_GRAPH.md` |
| `CON_` | Conclusion | `00_ENTITY_KEY_TABLE.md` |
| `FACT_` | NPC-knowledge fact | `03_NPC_KNOWLEDGE_AND_DISCLOSURE.md` |
| `ARC_` | Backbone arc | `05_CORE_EVENT_GRAPH.md` |
| `EVT_` | Playable or off-screen event node | `10_INVESTIGATION_NODE_GRAPH.md` |
| `END_` | Ending family | `14_ENDING_TRIGGER_MATRIX.md` |
| `CLK_` | Clock-threshold trigger | `01_WORLD_STATE_VARIABLES.md` § 1 |
| `TR_` | State-machine transition | `11_LOCATION_STATE_MACHINE.md` |
| `EVAL_` | Gate evaluator | `07_EVIDENCE_VALIDATION.md`, `14_ENDING_TRIGGER_MATRIX.md` |

## Ownership rules

Every authoritative fact has exactly one owner. Summaries and cross-references are permitted and must be explicitly marked non-authoritative.

| Fact | Authoritative owner |
|---|---|
| Ending trigger conditions | `14_ENDING_TRIGGER_MATRIX.md` |
| Ending node identity and graph edges | `10_INVESTIGATION_NODE_GRAPH.md` |
| Ending narrative outcome text | `../06_ENDING_FRAMEWORK.md` |
| Clue-class vocabulary | `07_EVIDENCE_VALIDATION.md` § 1 |

## Characters

| Key | Display name | Type | Initial location/state |
|---|---|---|---|
| `NPC_ELIAS` | Elias Varga | witness/victim | `LOC_SIGNAL_4B`, critical |
| `NPC_NADIA` | Nadia Soren | client/journalist | `LOC_NEWSROOM` |
| `NPC_LENA` | Lena Varga | protector/suspect | `LOC_SIGNAL_4B` |
| `NPC_IRIS` | Dr. Iris Bell | medical helper | `LOC_SIGNAL_4B` |
| `NPC_ROOK` | Inspector Adrian Rook | antagonist/police | `LOC_POLICE_ANNEX` |
| `NPC_KRELL` | Jonas Krell | antagonist/contractor | off-screen office |
| `NPC_REED` | Silas Reed | fixer | mobile, harbor district |
| `NPC_MARCUS` | Marcus Hale | editor/betrayer | `LOC_NEWSROOM` |
| `NPC_MINA` | Mina Cho | ally/patrol officer | `LOC_ELIAS_APT` or police route |
| `NPC_VALE` | Mara Vale | remote antagonist | off-screen government office |
| `NPC_BARISTA` | Café Orpheus barista | secondary witness | `LOC_CAFE_ORPHEUS` |
| `NPC_CAFE_OWNER` | Café Orpheus owner | secondary gatekeeper | `LOC_CAFE_ORPHEUS` |
| `NPC_CARE_SUPERVISOR` | Iris's supervisor | secondary witness | `LOC_IRIS_WORK` |
| `NPC_ARCHIVIST` | Harbor archivist | secondary gatekeeper | `LOC_HARBOR_ARCHIVE` |
| `NPC_PARAMEDIC` | independent paramedic | conditional rescue support | mobile |

## Locations

| Key | Display name |
|---|---|
| `LOC_START` | private briefing point |
| `LOC_ELIAS_APT` | Elias Varga's apartment |
| `LOC_NEWSROOM` | Greyhaven Ledger newsroom |
| `LOC_CAFE_ORPHEUS` | Café Orpheus |
| `LOC_POLICE_ANNEX` | Greyhaven Police Annex |
| `LOC_REED_OFFICE` | Reed's temporary garage office |
| `LOC_IRIS_WORK` | Iris Bell's workplace |
| `LOC_TERMINAL_EXT` | old ferry terminal exterior |
| `LOC_SIGNAL_4B` | Signal Room 4B |
| `LOC_HARBOR_ARCHIVE` | municipal harbor archive |
| `LOC_HOSPITAL` | St. Orison Medical Centre |
| `LOC_HARBOR_STREETS` | abstract harbor transit zone |

## Items and evidence objects

| Key | Description | Initial holder/location |
|---|---|---|
| `ITEM_LEDGER_PRIMARY` | primary encrypted hardware key | `LOC_SIGNAL_4B` |
| `ITEM_LEDGER_DECOY` | black decoy hardware key | `NPC_REED` after 19:23 |
| `ITEM_FERRY_PHOTO_ORIGINAL` | marked ferry photograph | `NPC_MARCUS` concealed |
| `ITEM_FERRY_PHOTO_ARCHIVE` | historical duplicate | `LOC_HARBOR_ARCHIVE` |
| `ITEM_RECOVERY_FRAGMENT_NADIA` | first three recovery digits | knowledge held by `NPC_NADIA` |
| `ITEM_RECOVERY_FRAGMENT_ELIAS` | final three digits encoded in photo | virtual clue |
| `ITEM_TIMED_CRASH_DEVICE` | apartment staging device | `LOC_ELIAS_APT` |
| `ITEM_PREPAID_PHONE_LENA` | Lena's phone | `NPC_LENA` |
| `ITEM_MEDICAL_KIT_IRIS` | trauma supplies | `NPC_IRIS` |
| `ITEM_REED_PHONE` | Reed's operational phone | `NPC_REED` |
| `ITEM_REED_LAPTOP` | laptop attempting decoy access | `LOC_REED_OFFICE` |
| `ITEM_MINA_REPORT_ORIGINAL` | Mina's original incident notes | digital, police system cache |
| `ITEM_ROOK_REPORT_ALTERED` | altered report version | police system |
| `ITEM_TRANSIT_CARD_ELIAS` | old transit card | discarded near harbor stop |
| `ITEM_NADIA_UPLOAD` | incomplete encrypted upload | newsroom server |
| `ITEM_CARRIER_LOG` | external call record | telecom source, abstract access |
| `ITEM_PAYMENT_RECORD` | proof of Marcus payment | intermediary account trail |
| `ITEM_AMBULANCE_ROUTE` | trusted rescue authorization | conditional procedural asset |

## Conclusions

| Key | Conclusion |
|---|---|
| `CON_STAGED_DISAPPEARANCE` | apartment abduction was staged |
| `CON_HARBOR_DESTINATION` | Elias travelled voluntarily to harbor |
| `CON_SIGNAL_4B` | Signal Room 4B is the destination |
| `CON_LENA_PROTECTING` | Lena protects rather than abducts Elias |
| `CON_REED_PRESENT` | Reed caused the confrontation |
| `CON_MARCUS_LEAK` | Marcus leaked partial plan |
| `CON_ROOK_COMPROMISED` | Rook is compromised |
| `CON_MEDICAL_EMERGENCY` | Elias needs immediate hospital care |
| `CON_DECOY_KEY` | black key is a decoy |
| `CON_WINDOW_CODE` | final code digits are hidden in window numbers |

## Event key ranges

- `EVT_000-099`: pre-play fixed history
- `EVT_100-199`: opening and first investigation block
- `EVT_200-299`: escalation block
- `EVT_300-399`: convergence and terminal access
- `EVT_400-499`: rescue, evidence transfer, accusation
- `EVT_900-999`: ending resolution
