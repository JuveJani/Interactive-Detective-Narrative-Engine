# Systems Investigator Booklet

**Private — systems-role player only.**  
Do not read ahead of your current scene code.

---

## S-110 — SCADA Room Entry

**Time cost:** +15 minutes (travel + scan)  
**After:** J-100 split

You badge into the climate-controlled monitoring bay. Server fans whisper. Three wall screens mirror Test Bay 3's environmental state — still showing **OCCUPIED** long after Elena's death, a detail Kevin notices you noticing.

Kevin Marsh looks young for the responsibility on his shoulders. Marcus Hale's **export hold** order blinks on the ops channel: *No raw historian to external counsel without ops sign-off.*

### What you learn

- Bay layout from the mirror terminal.
- Kevin is mid-rotation on the purge historian.
- A stepped sensor anomaly registered at **18:51** — dismissed as calibration drift in the official log.

**Go to S-111.**

---

## S-111 — Kevin First Contact

**Time cost:** +10 minutes

Kevin speaks in careful acronyms. Official story: validation fault triggered automated purge. He mentions, almost offhand, that Elena and Priya argued **Friday** about validation priorities — professional, not violent.

### Decision

| Choice | Effect |
|---|---|
| **Request historian export now** | Kevin hesitates; Marcus's hold applies. Proceed to S-112 with friction noted. |
| **Defer export; escort to bay first** | Kevin appreciates caution. Same next scene. |

**Go to S-112.**

---

## S-112 — Historian Access

**Time cost:** +20 minutes

Kevin grants read-only historian access. The purge event flag is visible, but **authorization detail** is locked behind a metadata layer — something about maintenance scheduling tokens.

If the clock is **20:30** or later, Kevin mentions rotation policy may tighten access.

**Go to S-113** (requires escort to bay — coordinate with field partner at regroup if they hold bay access, or Kevin escorts you now per your credentials).

---

## S-113 — Test Bay Forensics

**Time cost:** +35 minutes (travel + review)

In the observation bay, Elena remains at the calibration console. Hearing protection still seated. No defensive wounds. The active validation session was never aborted — as if she never saw the purge coming.

A tablet sits in the evidence lockup cage, screen dark.

### Clues

Record on your private notes, then case file at regroup:

- **C-04** — Elena injury / posture inconsistency  
- **C-14** — Tablet sync timestamps (if you image the tablet successfully — automatic on careful review)

**Go to S-115.**

---

## S-115 — Test Bay Physical Search

**Time cost:** +25 minutes

Supervised search of nozzle housings and cable tray. CO₂ discharge pattern is **wrong** for a staged PLC cascade — too simultaneous, too complete.

### Clue

- **C-01** — Test bay CO₂ discharge anomaly (automatic)

### Check — Perception (DC 10)

Roll **d20 + Perception modifier**.

| Result | Read |
|---|---|
| **Success** | Fibre residue on a sensor housing clip matches finance audit hardware mounts. Record **C-03**. |
| **Failure** | You note possible tamper but cannot identify residue. **C-03** may be recovered later at **S-220**. |

**Go to S-123.**

---

## S-123 — SCADA Metadata Depth

**Time cost:** +20 minutes  
**Split terminator — then go to J-150**

Deep metadata pass on the historian. If Kevin trusts you (+1 rapport from cooperative behavior), he stays quiet while you work.

### Check — Technology (DC 10)

Roll **d20 + Technology modifier**.

| Result | Read |
|---|---|
| **Success** | Manual purge override at **18:52** — before the fault frame. Auth token does not match maintenance schedule. Record **C-02** and **C-15**. |
| **Failure** | Purge flag visible; auth locked. Kevin may help later at **S-220**. |

Kevin's trust increases if you shared findings without shouting about murder yet.

**Stop. Wait for field partner. Go to J-150 together.**

---

## S-210 — Finance Hub Ledger

**Time cost:** +20 minutes  
**After:** J-150 finance assignment

Dana's glass office overlooks the procurement floor. She offers tea. The terminal hums with after-hours exception queues.

Browse the ledger. Glassline Industrial Supply appears with weights that do not match delivery receipts Elena flagged.

### Check — Investigation (DC 15)

Roll **d20 + Investigation modifier**.

| Result | Read |
|---|---|
| **Success** | Duplicate line items and shell routing obvious. Record **C-05**. |
| **Failure** | Summary discrepancy only. Full detail may come at **S-260** or from partner's **F-271**. |

**Go to S-230** or **S-260** (your choice; both before regroup two).

---

## S-230 — Dana Pressure Interview

**Time cost:** +20 minutes

You sit across from Dana. She admits "process shortcuts" in vendor onboarding — never murder. She redirects toward **Vince's cameras** or **Tom's tunnel access**.

### Clue

- **C-16** — Finance liaison admission fragment

Aggressive confrontation increases corporate attention — note on case file.

**Go to S-260** or **J-300** if audit complete.

---

## S-260 — Evening Audit Window

**Time cost:** +25 minutes  
**Split terminator — then go to J-300**

Evening audit memo queue shows approval bursts from Dana's liaison account after **22:00** on recent Fridays. Shell vendors route through the same mailbox cluster.

### Clue

- **C-07** — After-hours approval pattern

If you name shell vendors aloud, Dana's composure tightens — note increased suspicion.

**Stop. Wait for partner. Go to J-300.**

---

## S-240 — Witness Acceleration

**Time cost:** +10 minutes  
**Optional — after J-150**

At the security desk or SCADA room, you press **Sable** or **Kevin** for faster disclosure.

### Check — Persuasion (DC 10)

Roll **d20 + Persuasion modifier** (either player may roll if both present; highest success wins).

| Result | Read |
|---|---|
| **Success** | Witness agrees to Stage 1 acceleration — export scheduling or alert detail. +1 rapport with chosen witness. |
| **Failure** | Procedural walls remain; proof-based unlock still possible later. |

**Go to S-220** or **J-300** when your Split Two assignment is done.

---

## S-220 — Historian and Footage Preservation

**Time cost:** +20 minutes  
**After:** J-300 preservation assignment  
**Split terminator — go to J-410 or J-420**

Kevin runs a covert USB export while Sable pulls an unaltered camera subset. If you missed override clues earlier, Kevin flatlines the purge channel here — enough to confirm manual intervention.

### Effects

- Mark historian and/or footage on case file for **J-420**.
- If **C-02** or **C-03** was missing, you may record them now with Kevin's help.

**Stop. Wait for partner. Go to J-410** (or **J-420** if accusation already happened).

---

## End of Systems Booklet

Return to `JOINT_SCENES.md` at the code your scene directs.
