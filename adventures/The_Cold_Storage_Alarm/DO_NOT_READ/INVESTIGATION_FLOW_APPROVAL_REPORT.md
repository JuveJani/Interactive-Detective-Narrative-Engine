# Investigation Flow and Endings Approval Report — AUTHOR-ONLY / SPOILER-CONTAINING

**Adventure:** The Cold Storage Alarm  
**Stage gate:** `investigation_flow`  
**Status:** `AWAITING_APPROVAL`  
**Do not distribute to players.**

---

## Flow architecture

| Component | Count |
|-----------|------:|
| Investigation clocks | 5 (arrival → archive sync → dock restrict → security break → deadline) |
| Scene chains | 4 time-gated chains |
| World-state variants | 3 (security archive, dock access, control escort) |
| Location revisit rules | 8 across 5 locations |
| Inference flow gates | 6 (aligned to Investigation Core inferences) |
| Recovery routes | 9 diegetic actions |
| Flow states | 3 (ACTIVE, ACCUSATION, RESOLUTION) |

Clocks map to EVT-018 through EVT-022; `no_earlier_time_travel: true`.

---

## Ending graph (author map)

| Ending | Type | Trigger summary |
|--------|------|-----------------|
| END-PERFECT | perfect | Full accusation (Lori + CMD-CZ1-MUTE-STAGE) + KNOW-PERFECT-RECONSTRUCTION + full proof knowledge set |
| END-PARTIAL-TECH-ONLY | partial | Staging inference resolved; technical knowledge only; wrong accusation allowed |
| END-PARTIAL-MOTIVE-GAP | partial | Manifest known; relabel inference incomplete |
| END-PARTIAL-WRONG-CULPRIT | partial | Accuses NPC-DEV with badge-timing knowledge |
| END-PARTIAL-INCOMPLETE | partial | Min 3 knowledge; wrong accusation; capped reveal |
| END-HIDDEN-RECORDS | hidden | IT records-only archive sync route completed |
| END-NARRATIVE-CONTINUE | narrative_failure | Decorative — investigation continues without accusation |
| END-TIMEOUT | deadline | T_DEADLINE expired; no full truth |

Perfect ending requires `inference_perfect_resolved` — no automatic unlock from accusation alone.

---

## Accusation questionnaire

Four components: Q-WHO, Q-HOW, Q-WHAT, Q-MOTIVE mapped to CONC-WHO/HOW/WHAT/MOTIVE.

Correct perfect answers: NPC-LORI (who/motive), CMD-CZ1-MUTE-STAGE (how/what).

---

## Failure preservation

- Check failures set `check_label_failed` / `check_trend_failed` with alternate object actions in revisit rules
- Inference failures preserve investigation via recovery routes; imperfect endings remain available
- END-NARRATIVE-CONTINUE allows deferred accusation before deadline

---

## Placeholder resolution

Flow package re-exports Investigation Core `placeholder_resolution` for NPC conversation gate evaluation at flow runtime without modifying NPC package.

---

## Validation status

- Investigation Flow (includes Ending validation) — **PASS**
- Investigation Validator — **PASS**
- Investigation Core — **PASS**
- World First — **PASS**
- NPC — **PASS**
- Environment — **PASS**
- Object Interaction — **PASS**

No capability checks, PLAYER, playtime, DM-feeling, or package export generated.

**Do not proceed to capability_checks until investigation_flow gate approved.**
