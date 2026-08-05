# Investigation Core Approval Report — AUTHOR-ONLY / SPOILER-CONTAINING

**Adventure:** The Cold Storage Alarm  
**Stage gate:** `investigation_core`  
**Status:** `AWAITING_APPROVAL`  
**Do not distribute to players.**

---

## Entity inventory

| Entity | Count |
|--------|------:|
| World facts | 22 (FACT-001–022 from approved truth) |
| Physical evidence | 9 (EVD-* aligned to world truth) |
| Observations | 15 (object-interaction sourced) |
| Testimony | 18 (TEST-* linked to NPC topics) |
| Knowledge | 40 canonical KNOW-* records |
| Relationships | 9 (supports / contradicts / independent_of) |
| Hypotheses | 6 (player synthesis required) |
| Inferences | 6 (with recovery routes) |
| Conclusions | 5 (what, how, who, motive, perfect reconstruction) |
| Proofs | 9 (≥2 independent routes on major conclusions) |

---

## Placeholder resolution

| Legacy placeholder | Canonical knowledge |
|--------------------|---------------------|
| KNOW-BADGE-ENTRY-RECORD | KNOW-BADGE-COLD-ENTRY |
| KNOW-BMS-COMMAND-LOG | KNOW-BMS-COMMAND |
| KNOW-CONTROL-ROOM-ENTRY | KNOW-CONTROL-ENTRY |
| KNOW-DOOR-AJAR-ALARM | KNOW-DOOR-AJAR |
| KNOW-LABEL-RESIDUE | KNOW-LABEL-RESIDUE |
| KNOW-MANIFEST-POD-GAP | KNOW-MANIFEST-GAP |

Object INFO-* IDs map to KNOW-* via `object_interaction_links.info_id_to_knowledge_id`.

---

## Proof structure (author map)

**Culprit (NPC-LORI):** PROOF-WHO-DOC (badge misattribution + control entry + manifest) vs PROOF-WHO-PHYS (label fraud + residue + manifest).

**Method (CMD-CZ1-MUTE-STAGE):** PROOF-HOW-TECH (BMS command + staging + maint session + access mismatch) vs PROOF-HOW-PHYS (door alarm + command + staging + control entry).

**Product-risk cause:** PROOF-WHAT-TECH (temp trend + staging root cause + door ajar) vs PROOF-WHAT-OPS (BMS command + staging suspend + door ajar).

**Motive (manifest fraud):** PROOF-MOTIVE-DOC (manifest gap + recon exception + relabel fraud) vs PROOF-MOTIVE-PHYS (residue + timestamp + relabel fraud).

**Perfect reconstruction:** PROOF-PERFECT-FULL requires synthesis KNOW-PERFECT-RECONSTRUCTION.

---

## Inference chain

1. **INF-BADGE-MISATTRIBUTED** — contractor exit vs cold entry credential  
2. **INF-STAGING-ROOT-CAUSE** — staging suspension drives sustained rise  
3. **INF-RELABEL-FRAUD** — relabeling hides short-ship  
4. **INF-CONTROL-ACCESS-MISMATCH** — logistics badge in engineering room during mute  
5. **INF-CULPRIT-SUPPORTED** — independent streams identify logistics coordinator  
6. **INF-PERFECT-RECONSTRUCTION** — full supported timeline for perfect ending gate  

Failed inference leaves imperfect conclusions uncertain; recovery routes name executable object/NPC actions.

---

## Contradiction handling

- KNOW-MARCUS-LATCH-CHECK contradicts KNOW-BADGE-COLD-ENTRY → resolved_by_knowledge (badge log)

---

## Validation support artifact

`investigation_validator_package.json` created solely to run integrated Investigation Validator against linked layers. Not an authored player-facing stage. Ending reachability intentionally empty (endings not generated).

---

## Validation status

- Investigation Core — **PASS**
- Investigation Validator — **PASS**
- World First — **PASS**
- NPC — **PASS**
- Environment — **PASS**
- Object Interaction — **PASS**

No investigation flow, capability checks, PLAYER, playtime, DM-feeling, or package export generated.

**Do not proceed to investigation_flow until investigation_core gate approved.**
