# Environment and Object Interaction Approval Report — AUTHOR-ONLY / SPOILER-CONTAINING

**Adventure:** The Cold Storage Alarm  
**Stage gates:** `environment`, `objects`  
**Status:** `AWAITING_APPROVAL`  
**Do not distribute to players.**

---

## Environment layer summary

| Metric | Value |
|--------|-------|
| Primary investigation locations | 5 — dock, cold storage, control room, security office, manager office |
| Hub location | 1 — staff break room |
| Start location | LOC-DOCK (EVT-018 investigator arrival) |
| Navigation routes | 20 bidirectional pairs with diegetic labels |
| Time/state variants | Dock restriction (EVT-020), archive sync (EVT-019), security unstaffed (EVT-021), cold emergency (EVT-022), control escort clearance (player_action) |
| Features | 12 — each primary location has interactable feature refs |

### Access and routing design

- **Control room:** Requires supervisor escort until `ACT-REQUEST-CONTROL-ESCORT` at dock briefing; cleared state enables cold-side and security-side engineering routes.
- **Security archive:** Partial records before EVT-019; full archive after sync — meaningful revisit gate for badge queries.
- **Optional branch:** Break-room locker path (Dev badge) and dock-view window; not mandatory for conclusion facts.
- **Multiple routes:** Dock ↔ cold/security/manager/break; break hub shortcuts; cold ↔ control after escort.

### World-first alignment

All locations trace to causal timeline events or explicit adventure extension (LOC-FACILITY container). State transitions reference EVT-019/020/021/022 and player escort action tied to FACT-007 access pattern.

---

## Object interaction layer summary

| Metric | Value |
|--------|-------|
| Objects | 14 (4 nested) |
| Actions | 24 |
| Result units | 34 |
| Capability checks | 4 (perception ×3, technical ×1) — one attempt each |
| Player knowledge placeholders granted | All 6 KNOW-* placeholders from NPC package |
| Mandatory conclusion information | 12 info IDs with interaction paths |

### Evidence routing (author map)

| Information | Source object / action | Canonical evidence | Facts |
|-------------|------------------------|-------------------|-------|
| INFO-BADGE-COLD-ENTRY | OBJ-BADGE-ARCHIVE / ACT-QUERY-COLD-ENTRY | EVD-BADGE-LOG | FACT-005 |
| INFO-CONTROL-ENTRY | OBJ-BADGE-ARCHIVE / ACT-QUERY-CONTROL-ENTRY | EVD-CONTROL-ENTRY | FACT-007 |
| INFO-EXIT-SCAN | OBJ-BADGE-ARCHIVE / ACT-QUERY-EXIT-SCAN | EVD-EXIT-SCAN | FACT-002 |
| INFO-BMS-COMMAND | OBJ-CTRL-TERM-02 / ACT-REVIEW-BMS-COMMAND-LOG | EVD-BMS-COMMAND | FACT-008 |
| INFO-STAGING-SUSPEND | Terminal log + staging panel | EVD-BMS-COMMAND | FACT-009 |
| INFO-MAINT-SESSION | OBJ-CTRL-TERM-02 / ACT-REVIEW-MAINT-TICKET | EVD-MAINT-CLO1847 | FACT-018 |
| INFO-TEMP-TREND | OBJ-CTRL-TERM-02 / ACT-EXPORT-TEMP-TREND (CHK-TECH) | EVD-TEMP-TREND | FACT-010, FACT-017 |
| INFO-DOOR-AJAR | OBJ-ALARM-PANEL / ACT-REVIEW-ALARM-HISTORY | EVD-DOOR-ALARM | FACT-020 |
| INFO-LABEL-RESIDUE | OBJ-COLD-AISLE-C / ACT-SEARCH-LABEL-RESIDUE (CHK-PERCEPTION) | EVD-LABEL-RESIDUE | FACT-006 |
| INFO-LABEL-TIMESTAMP | OBJ-LABEL-RESIDUE / ACT-EXAMINE-RESIDUE-DETAIL | EVD-LABEL-RESIDUE | FACT-021 |
| INFO-MANIFEST-GAP | OBJ-MANIFEST-WORKSTATION / ACT-REVIEW-MNF-4471 | EVD-MANIFEST-POD | FACT-019, FACT-022 |
| INFO-BADGE-LOCKER (optional) | OBJ-LOCKER-BANK / ACT-INSPECT-LOCKER-14 | — | FACT-003 |

No single object resolves the case. Lori implication requires correlating badge log (misleading credential), control-room entry, manifest gap, label residue, and BMS command sequence.

### Hidden detail protection

- Failed perception checks (label, latch, locker) use empty failure units with `hints_missed_content: false`.
- Label residue child object concealed until successful search.
- Badge archive queries blocked until location records=full_archive (post-02:30).

### Revisit design

- Security office return after archive sync for badge queries.
- Cold aisle return after manifest review to interpret residue detail.
- Object and location states persist per revisit_rules.

---

## Investigation route sketch

1. **Records-first:** Security alarm history → wait/revisit archive → badge + control entries → correlate with manifest office.
2. **Physical-first:** Cold door + aisle search → manager manifest → security badge cross-check.
3. **Technical-first:** Escort to control → BMS command + temp trend + staging panel → alarm timeline corroboration.
4. **Optional shortcut context:** Break-room locker explains Dev badge availability without naming culprit.

---

## Assumptions requiring approval

1. Control-room escort granted via dock briefing action (supervisor present per NPC-ELENA schedule) — NPC conversation not required for access clearance.
2. Capability check DCs are placeholders until capability_checks stage.
3. Information IDs map to Investigation Core in a later stage; PLAYER prose not authored here.
4. `INFO-LATCH-DISTURBANCE` supports testimony contradiction only — not conclusion-mandatory.

**Do not proceed to investigation_core until environment and object gates approved.**

---

## Validation status

- `python3 -m idne.environment_validate` — **PASS**
- `python3 -m idne.object_interaction_validate` — **PASS**
- `python3 -m idne.world_first_validate` — **PASS**
- `python3 -m idne.npc_investigation_validate` — **PASS**

No investigation core, flow, PLAYER, playtime, DM-feeling, or package export generated.
