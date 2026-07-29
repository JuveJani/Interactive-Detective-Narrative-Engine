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
| `NPC_ELENA` | Dr. Elena Park | victim | deceased, `LOC_TEST_BAY` | `ACTIVE` |
| `NPC_DANA` | Dana Cole | culprit / CFO liaison | mobile, finance circuit | `ACTIVE` |
| `NPC_MARCUS` | Marcus Hale | suspect / operations lead | `LOC_OPS_FLOOR` | `ACTIVE` |
| `NPC_PRIYA` | Priya Nair | suspect / rival architect | `LOC_ARCHITECT_LAB` | `ACTIVE` |
| `NPC_VINCE` | Vince Calder | suspect / security contractor | mobile, perimeter | `ACTIVE` |
| `NPC_TOM` | Tom Reyes | suspect / maintenance | `LOC_MAINTENANCE_SHED` | `ACTIVE` |
| `NPC_SABLE` | Sable Ortiz | supporting / night security desk | `LOC_SECURITY_DESK` | `ACTIVE` |
| `NPC_KEVIN` | Kevin Marsh | supporting / SCADA analyst | `LOC_SCADA_ROOM` | `ACTIVE` |

## Locations

| Key | Display name | Status |
|---|---|---|
| `LOC_START` | Helix Meridian incident briefing point | `ACTIVE` |
| `LOC_TEST_BAY` | automation test bay (primary scene) | `ACTIVE` |
| `LOC_SCADA_ROOM` | SCADA monitoring and historian room | `ACTIVE` |
| `LOC_FINANCE_HUB` | CFO liaison and procurement hub | `ACTIVE` |
| `LOC_SECURITY_DESK` | night security desk and badge office | `ACTIVE` |
| `LOC_MAINTENANCE_SHED` | maintenance workshop and tool crib | `ACTIVE` |
| `LOC_OPS_FLOOR` | operations command floor | `ACTIVE` |
| `LOC_ARCHITECT_LAB` | automation architecture lab | `ACTIVE` |

## Items and evidence objects

| Key | Description | Initial holder/location | Status |
|---|---|---|---|
| `ITEM_BADGE_CLONE` | portable badge-cloning device | concealed near `LOC_MAINTENANCE_SHED` | `ACTIVE` |
| `ITEM_ELENA_TABLET` | Elena's encrypted project tablet | `LOC_TEST_BAY` evidence lockup after 19:15 | `ACTIVE` |
| `ITEM_PURGE_LOG` | CO₂ purge controller and override log export | `LOC_SCADA_ROOM` historian | `ACTIVE` |
| `ITEM_SENSOR_SPOOF` | RF sensor-spoof module (partial) | hidden in test-bay cable tray | `ACTIVE` |
| `ITEM_FINANCE_LEDGER` | procurement and approval trail showing discrepancies | `LOC_FINANCE_HUB` secure terminal | `ACTIVE` |
| `ITEM_CO2_OVERRIDE` | manual purge override fob / auth token | last held by authorized maintainer | `ACTIVE` |
| `ITEM_SECURITY_FOOTAGE` | badge-camera and bay perimeter recordings | security server, abstract access via `LOC_SECURITY_DESK` | `ACTIVE` |
| `ITEM_MAINT_WORKORDER` | falsified maintenance work order for bay access | `LOC_MAINTENANCE_SHED` clipboard / digital twin | `ACTIVE` |
| `ITEM_DANA_BADGE_RECORD` | badge issue and clone-audit record | `LOC_SECURITY_DESK` | `ACTIVE` |
| `ITEM_ELENA_AUDIT_MEMO` | Elena's draft fraud audit memo | on `ITEM_ELENA_TABLET` and mail archive | `ACTIVE` |

## Conclusions

| Key | Conclusion | Status |
|---|---|---|
| `CON_MURDER_NOT_ACCIDENT` | Elena's death was staged; automation failure was deliberate | `ACTIVE` |
| `CON_FINANCIAL_FRAUD` | ongoing embezzlement through vendor shells and approval abuse | `ACTIVE` |
| `CON_CREDENTIAL_ABUSE` | badge clone and credential spoof enabled unauthorized bay access | `ACTIVE` |
| `CON_CULPRIT_DANA` | Dana Cole orchestrated fraud and murder | `ACTIVE` |

Four conclusion identifiers. Each maps to a derived total in `01_WORLD_STATE_VARIABLES.md` § 2 and thresholds in `07_EVIDENCE_VALIDATION.md` § 2.

## Clue inventory (summary)

Sixteen clues are `ACTIVE`. Full dependency graph, classes, and granting nodes are owned by `12_CLUE_DEPENDENCY_GRAPH.md`.

| Key | Summary group | Status |
|---|---|---|
| `CLUE_TEST_BAY_CO2_ANOMALY` | murder / not accident | `ACTIVE` |
| `CLUE_PURGE_MANUAL_OVERRIDE` | murder / not accident | `ACTIVE` |
| `CLUE_SENSOR_SPOOF_TRACE` | murder / not accident | `ACTIVE` |
| `CLUE_ELENA_INJURY_PATTERN` | murder / not accident | `ACTIVE` |
| `CLUE_FINANCE_DISCREPANCY` | financial fraud | `ACTIVE` |
| `CLUE_VENDOR_SHELL_COMPANY` | financial fraud | `ACTIVE` |
| `CLUE_DANA_APPROVAL_PATTERN` | financial fraud | `ACTIVE` |
| `CLUE_ELENA_AUDIT_THREAD` | financial fraud | `ACTIVE` |
| `CLUE_BADGE_CLONE_DEVICE` | credential abuse | `ACTIVE` |
| `CLUE_BADGE_SWIPE_MISMATCH` | credential abuse | `ACTIVE` |
| `CLUE_AFTER_HOURS_ACCESS` | credential abuse | `ACTIVE` |
| `CLUE_MAINT_WORKORDER_FORGED` | credential abuse | `ACTIVE` |
| `CLUE_DANA_PRESENCE_WINDOW` | culprit / Dana | `ACTIVE` |
| `CLUE_DANA_TABLET_SYNC` | culprit / Dana | `ACTIVE` |
| `CLUE_CO2_OVERRIDE_AUTH` | culprit / Dana | `ACTIVE` |
| `CLUE_DANA_FINANCE_LINK` | culprit / Dana | `ACTIVE` |

## Check inventory (summary)

Five checks are `ACTIVE`. Full records are owned by `17_CHECK_REGISTER.md`.

| Key | Skill | Status |
|---|---|---|
| `CHK_115_PERCEPTION` | Perception | `ACTIVE` |
| `CHK_123_TECHNOLOGY` | Technology | `ACTIVE` |
| `CHK_210_INVESTIGATION` | Investigation | `ACTIVE` |
| `CHK_240_PERSUASION` | Persuasion | `ACTIVE` |
| `CHK_312_ATHLETICS` | Athletics | `ACTIVE` |

## Event key ranges

Two namespaces occupy the event numbering space. Backbone arcs in `05_CORE_EVENT_GRAPH.md` use `ARC_`; playable and off-screen nodes in `10_INVESTIGATION_NODE_GRAPH.md` use `EVT_`. A given number may appear in both namespaces and the two are not interchangeable.

### Backbone arcs

- `ARC_100-199`: opening and first investigation block
- `ARC_200-299`: escalation block
- `ARC_300-399`: convergence and terminal access
- `ARC_400-499`: accusation and evidence preservation
- `ARC_900-999`: ending resolution

### Event nodes (~34 playable nodes target)

- `EVT_000-099`: pre-play fixed history
- `EVT_100-199`: opening and Split One (~10 nodes)
- `EVT_200-299`: midgame and Split Two (~12 nodes)
- `EVT_300-399`: convergence, Split Three, accusation (~8 nodes)
- `EVT_400-499`: terminal accusation and dispatch (~4 nodes)
- `EVT_800-899`: off-screen resolution events
- `EVT_900-999`: ending resolution

### Checks

- `CHK_100-199`: opening block checks
- `CHK_200-399`: midgame and convergence checks
