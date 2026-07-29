# DO NOT READ: Clue Architecture

## 1. Purpose

This document defines conclusion-level redundancy at the narrative-design layer. It is **not authoritative** for clue identifiers, thresholds, validation rules, or dependency edges.

## 2. Authority split

The following logic documents own all machine-checkable clue architecture:

- **`DO_NOT_READ/LOGIC/07_EVIDENCE_VALIDATION.md`** — proof classes, evidence validation rules, check interactions, and conclusion thresholds.
- **`DO_NOT_READ/LOGIC/12_CLUE_DEPENDENCY_GRAPH.md`** — clue identifiers (`CLUE_*`), conclusion nodes (`CON_*`), granting nodes, redundancy paths, and soft-lock prevention edges.

This file must not duplicate counts, point values, node IDs, or trigger conditions from those documents. When this file and the logic layer disagree, the logic layer wins.

## 3. Non-authoritative design intent

The case requires players to break four independent misreadings:

1. **Accident misread:** the purge was a tragic PLC fault during authorized work.
2. **Operations misread:** Marcus Hale killed Elena to silence safety scrutiny.
3. **Rivalry misread:** Priya Nair sabotaged Elena's validation session.
4. **Maintenance misread:** Tom Reyes used tunnel access to trigger the bay environment.

Fair play demands that each misread remain plausible until at least two independent evidence classes contradict it.

## 4. Required conclusion families (narrative only)

These families correspond to logic-layer conclusions but are named here only by investigative meaning:

| Family | Investigative meaning |
|---|---|
| Not an accident | Manual intervention caused the purge; telemetry and hardware disagree with the official fault export. |
| Fraud motive | Glassline and liaison approvals connect Elena's audit to Dana Cole. |
| Credential abuse | Elena's badge and/or override tools were used inconsistent with her death timeline. |
| Timeline break | Witness, camera, and badge data exclude alternate suspects and break Dana's alibi. |
| Culprit identification | Dana Cole is the only suspect consistent with all four families. |

Critical terminal outcomes should require at least **three** of the four families at validated strength. Murder proof against Dana should require class diversity, not volume alone.

## 5. Red-herring policy

Red herrings must arise from genuine secrets, not fabricated nonsense.

- **Marcus Hale:** real safety cover-up, false murder inference.
- **Dr. Priya Nair:** real professional rivalry, false sabotage inference.
- **Tom Reyes:** real tunnel access and nervous behavior, false maintenance-sabotage inference.
- **Vince Calder:** real blind spots and sloppy checkout, false direct-killer inference unless players stop at negligence.

## 6. Failure transformation

Failed checks should change cost, certainty, or institutional friction—not remove all routes.

Examples at narrative level:

- failed server log parse: players see inconsistency but not manual override timestamp until they retry or ask Priya for VLAN access;
- failed dock reconstruction: players notice camera gap but not its overlap with Dana's movement until Sable cooperates;
- failed executive suite access: workbook remains discoverable later through counsel pressure at time cost;
- failed Marcus interview: he admits override cover-up but not timeline details, narrowing rather than ending the case.

## 7. Soft-lock prevention

The logic layer (`LOGIC/12_CLUE_DEPENDENCY_GRAPH.md`) must preserve at least one validated route to each conclusion family if players miss a single location or fail one major check.

Diegetic failsafes at design intent:

- Sable Ortiz can admit alert delay and dock sighting;
- Tom Reyes's ticket exonerates him once loading dock is visited;
- Priya can provide Elena's folder hint if treated credibly;
- Vince can identify fob checkout sloppiness under contract pressure;
- Marcus can deliver the edited safety report without proving murder.

Failsafes should cost time, trust, or ending quality. They must not deliver a perfect solution for free.

## 8. Pointer summary

| Topic | Authoritative document |
|---|---|
| Proof classes and validation | `LOGIC/07_EVIDENCE_VALIDATION.md` |
| Clue IDs, edges, redundancy | `LOGIC/12_CLUE_DEPENDENCY_GRAPH.md` |
| Ending triggers | `LOGIC/14_ENDING_TRIGGER_MATRIX.md` (when authored) |
| Narrative outcome prose | `06_ENDING_FRAMEWORK.md` |

Do not treat this file as a clue checklist for implementation or playtest scoring.
