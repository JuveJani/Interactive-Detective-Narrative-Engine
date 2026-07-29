# DO NOT READ: Location State Machine

## 1. Purpose

This file defines how investigation locations change over time and through player or off-screen actions. A compiled player node must select the correct location variant from current state, not assume the first-visit description remains valid forever.

## 1a. Variable bindings

Each machine below holds its state in exactly one variable, declared in `01_WORLD_STATE_VARIABLES.md` § 7.

| Machine | Section | Variable |
|---|---|---|
| Test bay | § 2 | `TEST_BAY_STATE` |
| SCADA room | § 3 | `SCADA_STATE` |
| Finance hub | § 4 | `FINANCE_STATE` |
| Security desk | § 5 | `SECURITY_STATE` |
| Maintenance shed | § 6 | `MAINT_STATE` |
| Operations floor | § 7 | `OPS_STATE` |
| Architect lab | § 8 | `ARCHITECT_STATE` |

`LOC_START` has no state variable; it is a briefing waypoint only.

## 1b. Transition register

Every state change in this document is a declared transition. Clock-driven transitions are fired by the `CLK_*` triggers in `01_WORLD_STATE_VARIABLES.md` § 1. Condition-driven transitions carry a `TR_*` identifier.

| Transition | Variable | From | To | Fired by |
|---|---|---|---|---|
| `TR_TEST_BAY_LOCKDOWN` | `TEST_BAY_STATE` | `CORDON_ACTIVE` | `EVIDENCE_LOCKDOWN` | `CLK_1930` |
| `TR_TEST_BAY_SEALED` | `TEST_BAY_STATE` | `EVIDENCE_LOCKDOWN` | `PLAYER_SEALED` | players file formal challenge at `EVT_410` or `EVT_420` |
| `TR_TEST_BAY_CORPORATE` | `TEST_BAY_STATE` | `EVIDENCE_LOCKDOWN` or `PLAYER_SEALED` | `CORPORATE_SEALED` | `A_CORPORATE >= 3` |
| `TR_SCADA_ROTATION` | `SCADA_STATE` | `NORMAL_ACCESS` | `HISTORIAN_ROTATION` | `CLK_2030` |
| `TR_SCADA_LEGAL_HOLD` | `SCADA_STATE` | `HISTORIAN_ROTATION` | `LEGAL_HOLD` | `A_CORPORATE >= 2` or clock past 22:30 without export |
| `TR_FINANCE_AUDIT` | `FINANCE_STATE` | `OPEN_LIAISON` | `AUDIT_WINDOW` | `CLK_2130` while `A_CORPORATE < 2` |
| `TR_FINANCE_RESTRICTED` | `FINANCE_STATE` | `OPEN_LIAISON` or `AUDIT_WINDOW` | `RESTRICTED` | `A_CORPORATE >= 2` |
| `TR_FINANCE_SEALED` | `FINANCE_STATE` | any | `SEALED` | `A_CORPORATE >= 3` or Dana off-screen cleanup succeeds |
| `TR_SECURITY_LIMITED` | `SECURITY_STATE` | `DESK_STAFFED` | `RECORDS_LIMITED` | `CLK_2030` |
| `TR_SECURITY_LOCKED` | `SECURITY_STATE` | `RECORDS_LIMITED` | `RECORDS_LOCKED` | `A_SECURITY >= 2` |
| `TR_MAINT_ALARM` | `MAINT_STATE` | `OPEN_UNSUPERVISED` | `TOOL_CRIB_ALARMED` | unauthorized forced entry at `EVT_312` failure variant |
| `TR_MAINT_DENIED` | `MAINT_STATE` | `TOOL_CRIB_ALARMED` | `ACCESS_DENIED` | security backup arrives; players lack challenge filing |
| `TR_OPS_NIGHT` | `OPS_STATE` | `DAY_CREW` | `NIGHT_SKELETON` | `CLK_2200` |
| `TR_OPS_INCIDENT` | `OPS_STATE` | `NIGHT_SKELETON` | `INCIDENT_COMMAND` | `A_CORPORATE >= 1` and formal challenge active |
| `TR_ARCHITECT_RESTRICTED` | `ARCHITECT_STATE` | `LAB_OPEN` | `LAB_RESTRICTED` | `CLK_2200` |
| `TR_ARCHITECT_SEALED` | `ARCHITECT_STATE` | `LAB_RESTRICTED` | `LAB_SEALED` | `A_CORPORATE >= 2` without player challenge |

Clock-driven transitions with no separate `TR_` identifier: `CLK_1930` → `TEST_BAY_STATE`; `CLK_2030` → `SCADA_STATE`, `SECURITY_STATE`; `CLK_2130` → `FINANCE_STATE`; `CLK_2200` → `OPS_STATE`, `ARCHITECT_STATE`.

---

## 2. Test bay (`LOC_TEST_BAY`)

### `CORDON_ACTIVE`

**Typical window:** 19:00–19:30  
**Available:** cordoned visual scan; Kevin escort request; corporate liaison messaging.

### `EVIDENCE_LOCKDOWN`

**From:** `TR_TEST_BAY_LOCKDOWN` at 19:30  
**Available:** supervised entry; forensic search at `EVT_115`; tablet path at `EVT_113`; challenge filing.

**Unavailable without cost:** unsupervised deep search; RF-shielded remote contact.

### `PLAYER_SEALED`

**From:** `TR_TEST_BAY_SEALED`  
**Available:** player-controlled evidence hold; imaging at `EVT_113`; external counsel notification.

### `CORPORATE_SEALED`

**From:** `TR_TEST_BAY_CORPORATE`  
**Available:** photographic records already taken; coroner summary via Marcus; no new physical recovery.

Evidence found before transition remains in player knowledge. `ELENA_STATUS` may advance to `EVIDENCE_CORPORATE_SEIZED`.

---

## 3. SCADA room (`LOC_SCADA_ROOM`)

### `NORMAL_ACCESS`

**Typical window:** 19:00–20:30  
**Available:** Kevin interview; historian export at `EVT_112`; metadata depth at `EVT_123`.

### `HISTORIAN_ROTATION`

**From:** `TR_SCADA_ROTATION`  
**Available:** export with Kevin trust +1 or `CHK_123_TECHNOLOGY` success; Marcus hold messaging.

### `LEGAL_HOLD`

**From:** `TR_SCADA_LEGAL_HOLD`  
**Available:** previously copied logs; Kevin covert USB route at `EVT_220`; legal challenge unlock.

Direct export blocked. Murder proof survives through copies and Kevin testimony.

---

## 4. Finance hub (`LOC_FINANCE_HUB`)

### `OPEN_LIAISON`

**Typical window:** 19:00–21:30  
**Available:** Dana liaison contact; terminal browse at `EVT_210`; approval pattern review.

### `AUDIT_WINDOW`

**From:** `TR_FINANCE_AUDIT`  
**Available:** tier-2 ledger export; shell vendor search; evening audit memo queue.

### `RESTRICTED`

**From:** `TR_FINANCE_RESTRICTED`  
**Available:** read-only summaries; Dana misdirection at `EVT_230`; challenge filing.

### `SEALED`

**From:** `TR_FINANCE_SEALED`  
**Available:** previously copied ledger; Elena memo from tablet; Priya email at `EVT_271`.

No critical fraud conclusion depends exclusively on intact terminal access after seal.

---

## 5. Security desk (`LOC_SECURITY_DESK`)

### `DESK_STAFFED`

**Typical window:** 19:00–20:30  
**Available:** Sable interview at `EVT_140`; incident log; badge record preview.

### `RECORDS_LIMITED`

**From:** `TR_SECURITY_LIMITED`  
**Available:** badge mismatch at `EVT_141` with procedural proof; Dana desk-visit fact.

### `RECORDS_LOCKED`

**From:** `TR_SECURITY_LOCKED`  
**Available:** Sable Stage 2 export if trust earned; warrant-equivalent challenge; Kevin cross-reference.

Footage alteration from `EVT_802` degrades one segment; alternate export routes remain (`02_ITEM_STATE_MATRIX.md`).

---

## 6. Maintenance shed (`LOC_MAINTENANCE_SHED`)

### `OPEN_UNSUPERVISED`

**Typical window:** 19:00–20:30  
**Available:** Tom interview at `EVT_122`; work-order comparison; tool crib search path.

### `TOOL_CRIB_ALARMED`

**From:** `TR_MAINT_ALARM`  
**Available:** Tom summons; authorized search with Tom present; clone device route at `EVT_312`.

### `ACCESS_DENIED`

**From:** `TR_MAINT_DENIED`  
**Available:** Tom testimony; shed CCTV via Sable; auth log contradiction only.

Physical clone discovery may be lost if `EVT_801` succeeds; credential proof survives via logs and work order.

---

## 7. Operations floor (`LOC_OPS_FLOOR`)

### `DAY_CREW`

**Typical window:** 19:00–22:00  
**Available:** Marcus incident command at `EVT_250`; export hold discussion; corporate framing.

### `NIGHT_SKELETON`

**From:** `TR_OPS_NIGHT`  
**Available:** skeleton crew statements; Marcus evening pressure; Priya summons log.

### `INCIDENT_COMMAND`

**From:** `TR_OPS_INCIDENT`  
**Available:** formal challenge coordination; Marcus Stage 2 admission with fraud+credential proof.

---

## 8. Architect lab (`LOC_ARCHITECT_LAB`)

### `LAB_OPEN`

**Typical window:** 19:00–22:00  
**Available:** Priya interview at `EVT_270`; design approval records; safety dispute context.

### `LAB_RESTRICTED`

**From:** `TR_ARCHITECT_RESTRICTED`  
**Available:** escorted interview; email thread retrieval at `EVT_271` with Priya cooperation.

### `LAB_SEALED`

**From:** `TR_ARCHITECT_SEALED`  
**Available:** queued email copies via Priya phone; Elena vendor warning fact already shared.

Priya never becomes inaccessible for documentary corroboration; access costs time after seal.
