# Fixed Truth Approval Report — AUTHOR-ONLY / SPOILER-CONTAINING

**Adventure:** The Cold Storage Alarm  
**Stage gate:** `fixed_truth` (+ causal and world-state timelines)  
**Status:** `AWAITING_APPROVAL` (revision 2)  
**Do not distribute to players.**

---

## Concise truth summary

Logistics coordinator **Lori Okonkwo (NPC-LORI)** discovered a real carrier short-delivery on **MNF-IN-4471** (8 of 48 cases received). She did not create missing stock. She relabeled pallets so WMS scans would show a full **L-4471** lot, then used **Dev Santos's** forgotten badge for cold-room access and his **unattended BMS maintenance session** on **CTRL-TERM-02** to issue **CMD-CZ1-MUTE-STAGE**, intending to silence a door-ajar alarm. The command suspended CZ-1 compressor staging and caused gradual warming. Non-violent shipment fraud with accidental refrigeration failure.

---

## 1. Shipment-fraud mechanism (precise)

| Element | Detail |
|---------|--------|
| **SKU** | SKU-FBC-12KG (frozen boneless chicken 12 kg cases) |
| **Batch** | BATCH-2026-0310-A |
| **Inbound manifest** | MNF-IN-4471 / lot L-4471 / pallet PLT-4471-A |
| **Carrier record** | POD-4471 lists 48 cases delivered |
| **Physical truth** | Only **8 cases** arrived on PLT-4471-A (40-case carrier short-ship — pre-existing discrepancy) |
| **Quarantine pallet** | PLT-Q118-B holds 48 damaged cases, lot Q-118, scheduled destruction |
| **Labels removed** | LBL-4471-A (serial NL-20260312-4471A) from 8-case partial; LBL-Q118-B from quarantine pallet |
| **Labels applied** | LBL-4471-A → PLT-Q118-B (48 cases); LBL-Q118-B → 8-case partial stack |
| **False WMS appearance** | Scan at aisle C bay 3 reads full L-4471 on the 48-case quarantine pallet |
| **Audit deception** | Quarterly audit uses random pallet-label scan + manifest match; mislabeled 48-case pallet would initially pass |
| **Later visibility** | Discrepancy surfaces via label serial print history (NL-20260312-4471A receipt绑定 to 8-case partial), POD vs receiving count, case-weight sampling, or Q-118 destruction paperwork mismatch |
| **Physical evidence** | Adhesive backing NL-20260312-4471A in aisle C; mismatched label re-application timestamp; MNF-IN-4471 vs POD-4471 documents |

**Important:** Label swap **reassigns identity**; it does not manufacture 40 missing cases.

---

## 2. Lori's BMS access (precise)

| Element | Detail |
|---------|--------|
| **Terminal** | CTRL-TERM-02 (engineering workstation, refrigeration maintenance bay) |
| **Session** | SVC-REFRG-MAINT (Dev's maintenance session, left unlocked at CLO-1847 close) |
| **Lori's credential** | BADGE-LORI — logistics coordinator; **no REFRG_TECH privilege** |
| **Access type** | **Opportunistic** use of unattended contractor session; not authorized engineering access |
| **Door log** | BADGE-LORI recorded at control room door 23:20:41 (proves presence, not command authorship) |
| **Command log** | Records terminal CTRL-TERM-02 + session SVC-REFRG-MAINT + CMD-CZ1-MUTE-STAGE; **does not record Lori's personal badge** |
| **Why log alone insufficient** | Any person in control room could use unlocked session; Dev's session expected during maintenance windows; Lori must be linked via badge entry timing + cold-room badge misuse + manifest motive + relabel physical evidence |

---

## 3. Alarm and control sequence (explicit chain)

| Step | Detail |
|------|--------|
| **1. First alarm** | ALM-COLD-DOOR-AJAR at 23:18:45 |
| **2. Cause** | Cold storage door held open >90 s during relabeling (cart wedge) |
| **3. Why Lori acted** | Door-ajar annunciates to security desk; would document extended presence during fraud |
| **4. Action selected** | CMD-CZ1-MUTE-STAGE on CTRL-TERM-02 (zone test mute + staging hold) |
| **5. Intended effect** | Silence door-ajar alarm for 15-minute "test" window |
| **6. Actual control effect** | Door alarm muted **and** CZ-1 demand staging suspended |
| **7. Staging disruption** | Compressor rotation disabled; lead unit runs fixed stage until suction pressure rises |
| **8. Gradual warming** | Glycol loop and pallet thermal mass delay supply-air inflection until ~23:27 |
| **9. Lori's misunderstanding** | Believed mute affected annunciation only; exited terminal without clearing staging hold |
| **10. Resulting states** | ALM-COLD-DOOR-AJAR silenced 23:22; ALM-CZ1-STAGE-SUSP 23:24; ALM-COLD-HIGH 23:30 at -14C threshold |

---

## 4. Proof-independence summary

| Question | Evidence type | Key facts | Does NOT alone prove |
|----------|---------------|-----------|----------------------|
| **What happened** | Alarm + trend | FACT-020, FACT-010, FACT-011 | Identity |
| **How (refrigeration)** | BMS + maintenance | FACT-008, FACT-009, FACT-018 | Who pressed key |
| **How (fraud)** | Physical + manifest | FACT-006, FACT-019, FACT-021 | Who relabeled |
| **Who (access)** | Badge logs | FACT-005, FACT-002, FACT-007 | Lori as badge user (Dev credential) |
| **Who (author)** | Correlation | FACT-007 + FACT-005 + FACT-006 + FACT-019 + timing | Any single log |
| **Motive** | Workflow | FACT-019, FACT-022, FACT-012 | Refrigeration failure |

**Perfect conclusion (Q-WHO):** requires FACT-005 + FACT-007 + FACT-006 + FACT-019 — badge misuse, control-room presence, physical relabel, manifest short-ship. BMS log (FACT-008) supports method (Q-HOW) with FACT-018 + FACT-009 but does not name Lori.

---

## Responsible actor / action chain

| Actor | Role |
|-------|------|
| **NPC-LORI** | Relabeling fraud + opportunistic BMS mute command |
| **NPC-DEV** | Innocent — forgot badge; left maintenance session unlocked |
| **NPC-MARCUS** | Innocent — latch check vs badge reader contradiction |
| **NPC-PAT** | Innocent witness |
| **NPC-ELENA** | Innocent operational response |
| **Carrier** | Source of real 40-case short-ship (off-screen) |

---

## Causal timeline summary

22 events (EVT-001–EVT-022). Investigation window unchanged **01:00–05:00**. Key revision: EVT-009 door-ajar alarm; EVT-011 CMD-CZ1-MUTE-STAGE on unattended session; EVT-013 gradual temp inflection 23:27.

---

## Deadline mechanics (unchanged)

- **02:30** badge archive sync  
- **03:15** dock restriction  
- **04:30** Marcus unavailable  
- **05:00** write-off threshold (FACT-015)  
- Temperature curve revised for gradual rise compatible with staging suspension

---

## Plausibility review findings

| Check | Finding |
|-------|---------|
| Fraud mechanism | Short-ship pre-exists; relabel misassigns identity only |
| BMS access | Opportunistic session use; no implausible engineering privileges |
| Control chain | Explicit mute-staging interlock; gradual thermal mass warming |
| Proof independence | BMS log does not name Lori; multi-source Q-WHO |
| Validator | World-first PASS (G-WF1–G-WF7) |
| Remaining concern | Full WMS/POD field names may need environment-stage alignment later |

---

## Assumptions requiring human approval

1. Carrier short-ship (40 cases) as pre-existing physical fact.  
2. CMD-CZ1-MUTE-STAGE behavior as documented in FACT-009.  
3. Unattended SVC-REFRG-MAINT session policy on CTRL-TERM-02.  
4. Relabel mechanism sufficient for audit deception until sampling.  
5. Lori as sole deliberate actor (unchanged).

---

## Exact approvals required

| Gate | Action |
|------|--------|
| **`fixed_truth`** | Approve revised immutable truth, timelines, and proof structure |
| **`npcs`** | Blocked until fixed_truth approved |

**Do not proceed to `npcs` until this revision is human-approved.**
