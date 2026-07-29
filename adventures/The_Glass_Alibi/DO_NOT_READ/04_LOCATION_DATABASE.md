# DO NOT READ: Location Database

## Location-state principles

Every location has:

- a base physical state;
- time-dependent changes;
- access requirements;
- available clue classes;
- risks;
- possible off-screen changes.

Locations should not exist only as containers for one clue.

**Authoritative location keys:** `LOGIC/00_ENTITY_KEY_TABLE.md`. State transitions are owned by `LOGIC/11_LOCATION_STATE_MACHINE.md`.

---

## LOC_START: Helix Meridian incident briefing point

### Function

Investigation hub, initial briefing, liaison contact, perimeter orientation, and counsel messaging.

### Physical layout

- glass-walled security lobby adjacent to the South Wing entrance;
- temporary incident command tables;
- phone bank used for vendor reconciliation calls;
- corridor sight lines to the perimeter dock lane and parking slots;
- escort checkpoint for restricted zones.

### Initial state at 19:00

- lockdown has ended but bay access remains restricted;
- Dana Cole is present and cooperative at the briefing edge;
- Sable Ortiz staffs the nearby security desk (`LOC_SECURITY_DESK`);
- default corporate narrative frames the event as PLC fault during validation.

### Objective clues

1. **Preliminary incident export** — classifies event as automated purge after validation fault; omits secondary badge mismatch flag.
2. **Badge reader summary** — Elena's badge at maintenance exit reader ~21:20; Dana's badge at finance hub ~21:18.
3. **Escort privilege policy binder** — finance liaison staff may use maintenance corridors with logged escort exceptions.
4. **Perimeter camera orientation** — dock Camera 4 sync-gap history visible on request through Sable.
5. **Vendor call metadata** — no active reconciliation call on Dana's extension during purge window.

### False lead

Dana's calm presence and liaison authority suggest she is the least likely suspect if investigators trust institutional tone over logs.

### Access requirements

- open at start;
- deeper validator logs require formal request through Sable or counsel.

### Time changes

- 20:45: Dana encourages dashboard "cleanup" messaging.
- 22:45: if trusted, Sable admits alert delay and dock corridor sighting.
- 23:00: counsel calls press for preliminary classification.

---

## LOC_SCADA_ROOM: SCADA monitoring and historian room

### Function

Digital evidence core: PLC exports, occupancy telemetry, procurement archives, purge controller logs. Kevin Marsh primary contact.

### Physical layout

- climate-controlled monitoring bay;
- bay controller mirror terminal;
- procurement export workstation;
- historian tape-style cold archive cabinet;
- restricted VLAN jack for vendor audit tooling.

### Initial state at 19:05

Priya attempted related archive access earlier in the week. Elena's lab workstation session is preserved on a staging VLAN reachable from here.

### Objective clues

1. **Occupancy telemetry micro-gaps** — steady occupied state with missing motion sub-sensor correlation; indicates spoof injection.
2. **Manual purge override timestamp** — override channel active 21:15:04; staged PLC fault frame timestamped 21:15:41.
3. **Procurement export duplicates** — Glassline vendor identifiers repeated with altered line weights; after-hours approvals under Dana's liaison account.
4. **Elena's encrypted folder hint** — naming pattern references "glass vendors" and Monday packet.
5. **Atmospheric alarm propagation delay** — 47-second lag inconsistent with standard HelixSense profile.
6. **Vendor audit hardware checkout log** — finance liaison checked out relay-capable audit tool two weeks prior.

### False lead

Priya's attempted access makes the SCADA room feel like rivalry-driven sabotage until access timestamps clear her during the purge window.

### Access requirements

- automation-technician emphasis for log parsing;
- initial read-only grant from counsel;
- Priya cooperation may accelerate workstation access.

### Risks

- careless export can trigger corporate wipe script if Dana initiates sanitization early (conditional).

### Time changes

- 20:18: Priya arrival creates social tension if investigators bring her here;
- 23:10: partial record lock if fraud exposed without counsel coordination;
- 00:10: sanitization script countdown if Dana not detained.

---

## LOC_TEST_BAY: automation test bay (primary scene)

### Function

Primary scene reconstruction: environmental evidence, console state, purge hardware, body positioning.

### Physical layout

- sealed test chamber with observation glass;
- calibration console and firmware validation rig;
- CO₂ suppression nozzles and atmospheric sensors;
- maintenance corridor access door (badge plus escort exception);
- tool locker and hearing-protection station;
- cable tray access for sensor housing.

### Initial state at 19:05

Elena's body remains until investigators complete imaging. Hearing protection is on the console. No sign of struggle.

### Objective clues

1. **Console login and validation session** — active session; no manual abort attempt; inconsistent with conscious awareness of purge.
2. **Purge nozzle activation pattern** — simultaneous full discharge consistent with manual override, not staged fault cascade.
3. **Spoof device scuff mark** — faint adhesive residue near occupancy sensor housing; matches finance audit hardware mounting clip.
4. **Body position and PPE** — hearing protection still seated; no defensive posture; supports surprise during focused work.
5. **Maintenance door mechanical state** — recent badge use on interior handle; corridor side shows hurried exit scuff.
6. **Air quality logger** — sharp O₂ drop starting 21:15; predates displayed PLC fault export by tens of seconds.

### False lead

Marcus's safety scandal makes operations negligence a plausible first theory.

### Access requirements

- field-investigator emphasis for physical scene work;
- escort from Sable until imaging complete;
- maintenance corridor door requires separate authorization.

### Time changes

- 19:12: medical confirmation of death;
- 21:40 onward: Marcus attempts to view exports through glass;
- 22:00: body may be released to coroner if investigators defer corridor evidence.

---

## LOC_OPS_FLOOR: operations command floor

### Function

Context for Marcus Hale, safety culture, conveyor override history, and witness movement between wings.

### Physical layout

- open operations pit with line monitors;
- Marcus's glass office overlooking the floor;
- safety bulletin boards;
- shift handoff kiosk;
- corridor to South Wing test bays.

### Initial state at 19:20

Marcus is agitated, speaking with counsel on phone. Night staff are minimal.

### Objective clues

1. **Edited safety incident report copy** — Marcus's conveyor bypass duration reduced in filed PDF; Elena's margin note: "Fix or self-report."
2. **Shift handoff entries** — Elena signed after-hours validation request; Marcus approved remotely.
3. **Witness statement drafts** — two technicians place Marcus in his office, not on floor, at alarm time.
4. **Safety interlock bulletin** — explains why manual purge requires override fob and logged reason.
5. **Priya argument witness notes** — professional dispute earlier in the week; no threats.

### False lead

Marcus's visible panic and prior misconduct suggest guilt for murder rather than cover-up of lesser misconduct.

### Access requirements

- generally open;
- Marcus interview required for office drawer access.

### Time changes

- 20:30: Marcus requests legal before further interviews;
- 23:00: operations summary draft favors accident classification.

---

## LOC_FINANCE_HUB: CFO liaison and procurement hub

### Function

Fraud documentation, Dana's workspace, audit workbook recovery, Glassline paper trail.

### Physical layout

- Dana's glass office;
- shared executive assistant station;
- locked filing cabinet for vendor exceptions;
- visitor credenza;
- small kitchenette with shredder;
- secure procurement terminal.

### Initial state at 19:28

Dana presents from here but physically operates between briefing point and hub. Assistant left at 17:00.

### Objective clues

1. **Elena's physical audit workbook** — hidden in assistant's overflow cabinet per Elena's Friday drop; Glassline entries circled; Dana signature initials on exceptions.
2. **Glassline vendor packet copies** — mailbox address match to Dana's old LLC.
3. **Shredder bin partial strip** — not yet emptied; Glassline invoice fragment if recovered carefully.
4. **Calendar printout** — Dana's Saturday "vendor call" block added Thursday afternoon.
5. **Executive vehicle log** — Dana's car unmoved; supports foot movement through dock blind spot.

### False lead

Priya's name appears on a competitive memo draft, suggesting hub plotting unrelated to fraud.

### Access requirements

- Dana escort or counsel warrant;
- forced access creates institutional conflict but may still yield clues before 00:30.

### Time changes

- 23:30: workbook discoverable if investigators obtain access;
- 00:10: Dana attempts remote sanitization from hub terminal if free;
- 00:20: confrontation window if investigators bring Dana here with evidence.

---

## LOC_SECURITY_DESK: night security desk and badge office

### Function

Badge records, camera exports, perimeter timeline reconstruction, Tom Reyes exculpation, Dana movement corridor proof.

### Physical layout

- glass-walled desk facing main lobby (`LOC_START` adjacent);
- HelixSense monitoring wall with default dashboard;
- interview booths;
- badge printer and secondary validator terminal;
- locked cabinet for temporary credential overrides;
- sight line to perimeter dock lane and Camera 4 pole.

### Initial state at 19:05

Sable Ortiz on shift. Dock lift shows recent maintenance. Camera 4 flag shows prior sync faults unremediated.

### Objective clues

1. **Camera 4 sync-gap log** — gap 21:08–21:19; Vince never scheduled repair.
2. **Tom Reyes maintenance ticket** — dock lift jam at 21:11; radio traffic recording; exculpates Tom during purge.
3. **Tunnel exit scuff and CO₂ residue trace** — faint chemical trace on exterior grate; consistent with post-purge exit path.
4. **Vehicle movement partial** — Dana's assigned campus vehicle still in executive slot; she moved on foot through blind spot.
5. **Sable witness support detail** — dock corridor sighting of Dana ~21:17; not visible on camera due to gap.

### False lead

Tom's maintenance corridor access and nervous behavior suggest guilt until ticket and radio timestamps are recovered.

### Access requirements

- field-investigator emphasis;
- exterior perimeter access open from briefing point;
- tunnel exit grate requires safety PPE.

### Time changes

- 21:11: Tom's dock work (fixed background);
- 22:30: Vince summoned if camera records requested;
- 00:00: Dana attempts departure through executive side if not restricted.

---

## LOC_MAINTENANCE_SHED: maintenance workshop and tool crib

### Function

Maintenance corridor network access, override fob checkout, clone device concealment, Tom Reyes interviews.

### Physical layout

- low-lit workshop with conduit racks;
- badge readers at bay door and dock exit (corridor network);
- override fob checkout panel;
- tool crib and falsified work-order clipboard;
- junction where Dana previously asked Tom about "VIP routes."

### Initial state at 19:05

Tunnel corridors are technically restricted but documented liaison escort exceptions exist. Air still carries faint chemical note near bay door.

### Objective clues

1. **Badge reader secondary log** — Elena's credential ~21:20 at dock exit; mismatch flag stored, not on default dashboard.
2. **Override fob panel log** — fob ID checked out to Vince's contract pool; used 21:14–21:16; duplicate unreturned unit.
3. **Sensor relay adhesive fragment** — matched to finance audit hardware.
4. **Foot scuff pattern** — single hurried exit from bay toward dock; inconsistent with emergency evacuation from multiple staff.
5. **Tom's prior note** — Dana asked about tunnel camera coverage last Tuesday; logged informally on punch-card in tool cage.

### False lead

Tom's frequent corridor access makes maintenance sabotage seem plausible until radio and ticket evidence clear him.

### Access requirements

- field-investigator emphasis for traversal;
- safety briefing required for atmospheric residue near bay door;
- liaison escort log needed to explain Dana's legal presence.

### Risks

- poor lighting and trip hazards;
- tool crib alarm if unauthorized forced entry;
- corporate may restrict access if counsel fears contamination.

### Time changes

- 21:14–21:20: murder path (fixed background);
- 22:10: spoof residue discoverable if bay sensor clue already found;
- 23:15: Vince may confess checkout sloppiness when confronted with fob ID.

---

## LOC_ARCHITECT_LAB: automation architecture lab

### Function

Priya Nair context, rivalry documents, Elena's encrypted project hints, vendor warning email thread.

### Physical layout

- bench stations and firmware validation rigs;
- Elena's reserved workstation;
- project rivalry memo drafts;
- archived controller image storage;
- small interview nook.

### Initial state at 19:35

Priya may return for interview. Elena's session artifacts remain on staging VLAN.

### Objective clues

1. **Rivalry witness notes** — professional dispute; no threats.
2. **Encrypted folder naming hint** — "glass vendors" and Monday packet references.
3. **Vendor warning email thread** — Elena flagged duplicate supplier metadata to Dana; Dana deflected.
4. **Access log clearance** — Priya not in bay during purge window.

### False lead

Professional jealousy reads as motive until timeline and fraud chain redirect suspicion.

### Access requirements

- Priya cooperation or counsel warrant;
- restricted after 22:00 without challenge filing.

### Time changes

- 22:00: lab restricted unless players hold challenge filing;
- 22:30: Priya provides folder hint if treated credibly.

---

## Location connectivity

```text
LOC_START ── lobby ── LOC_SECURITY_DESK ── perimeter dock lane
     │                              │
     ├── corridor ── LOC_OPS_FLOOR ── LOC_TEST_BAY
     │                                    │
     ├── VLAN ── LOC_SCADA_ROOM           └── LOC_MAINTENANCE_SHED
     │
LOC_FINANCE_HUB ── executive corridor ── LOC_START
LOC_ARCHITECT_LAB ── ops corridor ── LOC_OPS_FLOOR
```

Investigators should need at least **three locations** to assemble a complete solution, with no single room containing all proof classes.
