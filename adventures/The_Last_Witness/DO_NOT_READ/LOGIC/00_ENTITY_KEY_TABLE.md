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
| `CHK_` | Skill check | `17_CHECK_REGISTER.md` |

## Ownership rules

Every authoritative fact has exactly one owner. Summaries and cross-references are permitted and must be explicitly marked non-authoritative.

| Fact | Authoritative owner |
|---|---|
| Ending trigger conditions | `14_ENDING_TRIGGER_MATRIX.md` |
| Ending node identity and graph edges | `10_INVESTIGATION_NODE_GRAPH.md` |
| Ending narrative outcome text | `../06_ENDING_FRAMEWORK.md` |
| Clue-class vocabulary | `07_EVIDENCE_VALIDATION.md` § 1 |

## Characters

| Key | Display name | Type | Initial location/state | Status |
|---|---|---|---|---|
| `NPC_ELIAS` | Elias Varga | witness/victim | `LOC_SIGNAL_4B`, critical | `ACTIVE` |
| `NPC_NADIA` | Nadia Soren | client/journalist | `LOC_NEWSROOM` | `ACTIVE` |
| `NPC_LENA` | Lena Varga | protector/suspect | `LOC_SIGNAL_4B` | `ACTIVE` |
| `NPC_IRIS` | Dr. Iris Bell | medical helper | `LOC_SIGNAL_4B` | `ACTIVE` |
| `NPC_ROOK` | Inspector Adrian Rook | antagonist/police | `LOC_POLICE_ANNEX` | `DEFINITION_ONLY` |
| `NPC_KRELL` | Jonas Krell | antagonist/contractor | off-screen office | `DEFINITION_ONLY` |
| `NPC_REED` | Silas Reed | fixer | mobile, harbor district | `ACTIVE` |
| `NPC_MARCUS` | Marcus Hale | editor/betrayer | `LOC_NEWSROOM` | `ACTIVE` |
| `NPC_MINA` | Mina Cho | ally/patrol officer | `LOC_ELIAS_APT` or police route | `ACTIVE` |
| `NPC_VALE` | Mara Vale | remote antagonist | off-screen government office | `DEFINITION_ONLY` |
| `NPC_BARISTA` | Café Orpheus barista | secondary witness | `LOC_CAFE_ORPHEUS` | `DEFINITION_ONLY` |
| `NPC_CAFE_OWNER` | Café Orpheus owner | secondary gatekeeper | `LOC_CAFE_ORPHEUS` | `DEFINITION_ONLY` |
| `NPC_CARE_SUPERVISOR` | Iris's supervisor | secondary witness | `LOC_IRIS_WORK` | `DEFINITION_ONLY` |
| `NPC_ARCHIVIST` | Harbor archivist | secondary gatekeeper | `LOC_HARBOR_ARCHIVE` | `DEFINITION_ONLY` |
| `NPC_PARAMEDIC` | independent paramedic | conditional rescue support | mobile | `DEFINITION_ONLY` |
| `NPC_ROOK_NETWORK` | Rook's loyal detectives, acting as a unit | antagonist/police | `LOC_POLICE_ANNEX` | `ACTIVE` |

## Locations

| Key | Display name | Status |
|---|---|---|
| `LOC_START` | private briefing point | `ACTIVE` |
| `LOC_ELIAS_APT` | Elias Varga's apartment | `ACTIVE` |
| `LOC_NEWSROOM` | Greyhaven Ledger newsroom | `ACTIVE` |
| `LOC_CAFE_ORPHEUS` | Café Orpheus | `ACTIVE` |
| `LOC_POLICE_ANNEX` | Greyhaven Police Annex | `ACTIVE` |
| `LOC_REED_OFFICE` | Reed's temporary garage office | `ACTIVE` |
| `LOC_IRIS_WORK` | Iris Bell's workplace | `ACTIVE` |
| `LOC_TERMINAL_EXT` | old ferry terminal exterior | `ACTIVE` |
| `LOC_SIGNAL_4B` | Signal Room 4B | `ACTIVE` |
| `LOC_HARBOR_ARCHIVE` | municipal harbor archive | `ACTIVE` |
| `LOC_HOSPITAL` | St. Orison Medical Centre | `DEFINITION_ONLY` |
| `LOC_HARBOR_STREETS` | abstract harbor transit zone | `DEFINITION_ONLY` |

## Items and evidence objects

| Key | Description | Initial holder/location | Status |
|---|---|---|---|
| `ITEM_LEDGER_PRIMARY` | primary encrypted hardware key | `LOC_SIGNAL_4B` | `ACTIVE` |
| `ITEM_LEDGER_DECOY` | black decoy hardware key | `NPC_REED` after 19:23 | `ACTIVE` |
| `ITEM_FERRY_PHOTO_ORIGINAL` | marked ferry photograph | `NPC_MARCUS` concealed | `ACTIVE` |
| `ITEM_FERRY_PHOTO_ARCHIVE` | historical duplicate | `LOC_HARBOR_ARCHIVE` | `DEFINITION_ONLY` |
| `ITEM_RECOVERY_FRAGMENT_NADIA` | first three recovery digits | knowledge held by `NPC_NADIA` | `DEFINITION_ONLY` |
| `ITEM_RECOVERY_FRAGMENT_ELIAS` | final three digits encoded in photo | virtual clue | `DEFINITION_ONLY` |
| `ITEM_TIMED_CRASH_DEVICE` | apartment staging device | `LOC_ELIAS_APT` | `ACTIVE` |
| `ITEM_PREPAID_PHONE_LENA` | Lena's phone | `NPC_LENA` | `ACTIVE` |
| `ITEM_MEDICAL_KIT_IRIS` | trauma supplies | `NPC_IRIS` | `ACTIVE` |
| `ITEM_REED_PHONE` | Reed's operational phone | `NPC_REED` | `ACTIVE` |
| `ITEM_REED_LAPTOP` | laptop attempting decoy access | `LOC_REED_OFFICE` | `ACTIVE` |
| `ITEM_MINA_REPORT_ORIGINAL` | Mina's original incident notes | digital, police system cache | `ACTIVE` |
| `ITEM_ROOK_REPORT_ALTERED` | altered report version | police system | `ACTIVE` |
| `ITEM_TRANSIT_CARD_ELIAS` | old transit card | discarded near harbor stop | `DEFINITION_ONLY` |
| `ITEM_NADIA_UPLOAD` | incomplete encrypted upload | newsroom server | `ACTIVE` |
| `ITEM_CARRIER_LOG` | external call record | telecom source, abstract access | `DEFINITION_ONLY` |
| `ITEM_PAYMENT_RECORD` | proof of Marcus payment | intermediary account trail | `DEFINITION_ONLY` |
| `ITEM_AMBULANCE_ROUTE` | trusted rescue authorization | conditional procedural asset | `DEFINITION_ONLY` |

## Conclusions

| Key | Conclusion | Status |
|---|---|---|
| `CON_STAGED_DISAPPEARANCE` | apartment abduction was staged | `ACTIVE` |
| `CON_HARBOR_DESTINATION` | Elias travelled voluntarily to harbor | `ACTIVE` |
| `CON_SIGNAL_4B` | Signal Room 4B is the destination | `ACTIVE` |
| `CON_LENA_PROTECTING` | Lena protects rather than abducts Elias | `ACTIVE` |
| `CON_REED_PRESENT` | Reed was present at the confrontation | `ACTIVE` |
| `CON_REED_CAUSED_CONFRONTATION` | Reed caused the confrontation | `ACTIVE` |
| `CON_MARCUS_LEAK` | superseded umbrella; use the tiered pair | `DEPRECATED` |
| `CON_MARCUS_LEAK_PARTIAL` | Marcus leak, partial conclusion | `ACTIVE` |
| `CON_MARCUS_LEAK_PROVABLE` | Marcus leak, provable accusation | `ACTIVE` |
| `CON_ROOK_COMPROMISED` | superseded umbrella; use the tiered pair | `DEPRECATED` |
| `CON_ROOK_OPERATIONALLY_COMPROMISED` | Rook compromised, private operational conclusion | `ACTIVE` |
| `CON_ROOK_PUBLICLY_PROVABLE` | Rook compromised, publicly provable | `ACTIVE` |
| `CON_MEDICAL_EMERGENCY` | Elias needs immediate hospital care | `ACTIVE` |
| `CON_DECOY_KEY` | black key is a decoy | `ACTIVE` |
| `CON_WINDOW_CODE` | final code digits are hidden in window numbers | `ACTIVE` |
| `CON_PASSPHRASE_ACCESS` | the primary archive can be opened, by passphrase or by logged reset | `ACTIVE` |

Sixteen identifiers. Five were registered when the `D_*` namespace was merged into `CON_*`; they already existed in `12_CLUE_DEPENDENCY_GRAPH.md` with their thresholds intact, so registering them changed no threshold, tier or meaning.

`CON_MARCUS_LEAK` and `CON_ROOK_COMPROMISED` are `DEPRECATED`. They are umbrella identifiers superseded by their tiered pairs, they carry no threshold, and no document may gate on them. They are retained rather than deleted so the migration record stays legible.

`CON_REED_PRESENT` covers presence at the confrontation. `CON_REED_CAUSED_CONFRONTATION` is the stronger tier covering causation. The two were previously glossed identically, which misdescribed the first.

## Event key ranges

Two namespaces occupy the event numbering space. Backbone arcs in `05_CORE_EVENT_GRAPH.md` use `ARC_`; playable and off-screen nodes in `10_INVESTIGATION_NODE_GRAPH.md` use `EVT_`. A given number may appear in both namespaces and the two are not interchangeable.

### Backbone arcs

- `ARC_100-199`: opening and first investigation block
- `ARC_200-299`: escalation block
- `ARC_300-399`: convergence and terminal access
- `ARC_400-499`: rescue, evidence transfer, accusation
- `ARC_900-999`: ending resolution

### Event nodes

- `EVT_000-099`: pre-play fixed history
- `EVT_100-199`: opening and first investigation block
- `EVT_200-299`: escalation block
- `EVT_300-399`: convergence and terminal access
- `EVT_400-499`: rescue, evidence transfer, accusation
- `EVT_500-799`: unallocated
- `EVT_800-899`: off-screen resolution events
- `EVT_900-999`: ending resolution

### Checks

- `CHK_100-199`: opening and first investigation block checks
