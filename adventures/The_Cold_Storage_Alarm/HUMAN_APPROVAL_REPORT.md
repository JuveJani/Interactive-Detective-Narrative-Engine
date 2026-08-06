# Human Approval Report — The Cold Storage Alarm

**Stage:** `adventure_brief`  
**Status:** `AWAITING_APPROVAL`  
**Generator:** Adventure Generator v2  
**Canonical brief:** `adventure_brief.json`

---

## Three concept candidates

### Concept A — The Cold Storage Alarm (recommended)

A regional cold-chain warehouse calls in a facilities automation technician after hours when refrigeration fails and access alarms fire, but nothing obvious is missing. Investigation runs through badge logs, building-management exports, refrigeration controls, and witness interviews while storage temperature climbs toward a compliance deadline.

| Criterion | Assessment |
|-----------|------------|
| Investigation depth | High — logs, sensors, overrides, and testimony cross-check naturally |
| Object-interaction potential | High — doors, chillers, BMS panels, badge readers, maintenance tags |
| NPC complexity | Moderate — five on-scene roles plus records-based sixth actor |
| Time-pressure potential | High — rising temperature closes options in-world |
| Two-hour size risk | Low–moderate — single-building scale is bounded |
| Engine compatibility | Strong — locations, objects, NPC knowledge, capability checks, time costs |

### Concept B — The Campus Lab Containment

A community-college facilities technician responds on a weekend when HVAC isolation triggers in a chemistry prep lab and restricted-storage access is questioned. Routes include fume-hood sensors, chemical inventory, badge logs, and staff schedules before a Monday inspection.

| Criterion | Assessment |
|-----------|------------|
| Investigation depth | Moderate — strong records, fewer industrial objects |
| Object-interaction potential | Moderate — hoods, storage locks, environmental sensors |
| NPC complexity | Moderate — five academic and facilities roles |
| Time-pressure potential | Moderate — Monday reopening deadline |
| Two-hour size risk | Low — compact campus footprint |
| Engine compatibility | Strong — may feel smaller than target depth |

### Concept C — The Ferry Terminal Blackout

A port automation technician investigates a municipal ferry terminal where power and ticketing systems failed during peak commute and backup generation did not engage. Evidence spans generator maintenance, load-shed relays, CCTV, and crew logs before the next sailing window.

| Criterion | Assessment |
|-----------|------------|
| Investigation depth | High — mechanical and digital traces |
| Object-interaction potential | High — generators, relays, ticketing systems |
| NPC complexity | Moderate–high — six maritime and operations roles |
| Time-pressure potential | High — next-morning sailings |
| Two-hour size risk | Moderate — pier and mechanical scope may expand |
| Engine compatibility | Good — slightly broader domain than maintenance-tech home turf |

---

## Recommended concept

**Concept A — The Cold Storage Alarm**

Best balance of investigation depth, object interaction, technician role fit, bounded single-building scale, and urgent time pressure without defaulting to murder or unsupported mechanics. The warehouse setting gives natural access to automation expertise, physical evidence, and institutional NPCs while staying within a two-hour static adventure footprint.

**This recommendation is not approval.** Human sign-off is required before Fixed Truth generation.

---

## Brief parameters (approved-schema fields only)

| Field | Value |
|-------|-------|
| Intended wall-clock duration | ~120 minutes (`target_playtime_minutes`: 120) |
| Intended in-world duration | One night shift (~4 in-world hours) |
| Setting | Regional cold-chain distribution warehouse and attached offices, after hours |
| Central incident | Critical cold-storage failure plus unauthorized access alarms without obvious theft or violence |
| Investigator role | Facilities automation and refrigeration maintenance technician |
| Location count | 5 primary + 1 secondary hub (see structure below) |
| NPC count | 5 primary on-scene + 1 records-only access administrator |
| Player mode | `single_investigator` |

### Intended location structure

1. Loading dock  
2. Cold storage hall  
3. Automation control room  
4. Security office  
5. Warehouse manager office  
6. Staff break room (secondary hub)

### Intended investigation structure

- Technician arrives to diagnose automation fault under institutional pressure.  
- Multiple fair routes: badge/access logs, BMS trend exports, refrigeration setpoints, witness interviews, physical inspection of doors/sensors/override panels.  
- Testimony must be compared with physical and logged evidence.  
- At least one important contradiction between a witness account and badge or sensor records.  
- Multiple routes to partial or full conclusions; imperfect endings preserve investigation; one fully supported perfect ending.

### Intended time pressure

Rising storage temperature and an approaching write-off or compliance deadline progressively closes interviews and deep inspections. Missed windows change available choices and world state rather than arbitrary lockouts.

### Planned aha structure type (no solution revealed)

**Delayed-significance correlation:** a routine maintenance timestamp that first appears administratively benign becomes meaningful only when cross-referenced with an override sequence and access timing. Players reconstruct significance; the engine does not deliver the conclusion directly.

### Major content boundaries

- No graphic violence; no supernatural resolution.  
- Adult workplace themes: negligence, fraud, institutional pressure.  
- No unsupported inventory, retry, false-check, or puzzle-system mechanics.  
- No clue-counting or narrator solution delivery.

---

## Assumptions requiring human approval

1. **Incident type** — Industrial/access/compliance mystery rather than homicide is acceptable for the first real adventure.  
2. **Location and NPC counts** — Five primary locations and five on-scene NPCs (plus records-only sixth) fit the two-hour target.  
3. **In-world duration** — Four in-world hours mapped to ~120 wall-clock minutes is acceptable pacing.  
4. **Tone** — Methodical, urgent workplace realism without sensational violence.  
5. **Ending policy** — One perfect ending plus several imperfect endings that preserve investigation aligns with IDNE design philosophy.  
6. **Technician protagonist** — Single investigator with automation/maintenance skills (no separate player roles).  
7. **author_notes design intent** — Structural notes in the brief JSON are author-facing only and do not pre-approve story resolution.

---

## Exact human approvals required

| Gate | Action required |
|------|-----------------|
| `adventure_brief` | Review this report and `adventure_brief.json`; approve concept and parameters before Fixed Truth generation |
| Future: `fixed_truth` | Approve immutable world truth, timeline, and story-critical facts |
| Future: `npcs` | Approve major NPC motivations, relationships, and knowledge |
| Future: `investigation_flow` | Approve ending structure and route logic |
| Future: `package_export` | Approve Pre-Playtest package export |

**To approve the brief stage:** record approval in generation state (`human_approvals.adventure_brief`) or re-run the generator with documented sign-off per `ADVENTURE_GENERATOR_V2_WORKFLOW.md`.

---

## Generation status

Pipeline initialized at brief approval gate. **No later stages have been run.**

- Fixed Truth: not created  
- Timeline layers: not created  
- NPC package: not created  
- Environment / objects / investigation layers: not created  
- PLAYER content: not created  
- `.idne` package: not created  

**Current status:** `AWAITING_APPROVAL` at stage `adventure_brief`.
