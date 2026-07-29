# Implementation Readiness — P5 to P10 (final)

**Specification:** `IMPLEMENTATION_PLAN.md` v2.4, `status: Approved`
**Date:** 2026-07-28
**Question:** can P5 through P10 proceed without any further specification changes?

---

## Answer

**Yes.** All of P5, P6, P7, P8, P9 and P10 can be executed against v2.4 as written. No ratification is `OPEN`, no phase depends on an unresolved decision, and every gate that any phase must pass has an assigned phase.

This supersedes the previous readiness report, which recorded P8 as blocked by § 14.3.

---

## Phase-by-phase

| Phase | Commit | Ratifications required | Status | Proceed |
|---|---|---|---|---|
| P5 | C5 | § 14.5, § 14.7, § 14.9 | all RESOLVED | Yes |
| P6 | C6 | § 14.4 | RESOLVED | Yes |
| P7 | C7 | § 14.1, § 14.2, § 14.8 | all RESOLVED | Yes |
| P8 | C8 | § 14.3 | RESOLVED | Yes |
| P9 | C9 | none | — | Yes |
| P10 | none | none | — | Yes |

§ 14.6, the duplicate-root-file policy, is `DEFERRABLE` and required by no phase. Its deferral is recorded in § 16.2, which is what § 3.2 and § 14.6 ask for.

---

## Ratification status

Nine of ten resolved, one deferrable, none open.

| § | Item | Status | Resolved in |
|---|---|---|---|
| 14.1 | `END_SILENT_TERMINAL` terminal type | RESOLVED | v2.3 |
| 14.2 | Split-branch terminator vocabulary | RESOLVED | v2.3 |
| 14.3 | Low and Medium confidence mapping rows | RESOLVED | v2.4 |
| 14.4 | Passphrase as a fifth solution chain | RESOLVED | v2.3 |
| 14.5 | Point values | RESOLVED | v2.2 |
| 14.6 | Duplicate-root-file policy | DEFERRABLE | recorded v2.1, deferral logged v2.2 |
| 14.7 | Multi-class clue diversity behaviour | RESOLVED | v2.2 |
| 14.8 | Ending-trigger precedence | RESOLVED | v2.3 |
| 14.9 | Umbrella conclusion identifiers | RESOLVED | v2.2 |
| 14.10 | Route A classification | RESOLVED | v2.1 |

---

## Validation gate coverage

| Gate | Phase or phases | Note |
|---|---|---|
| `V1` | P3, P6 | — |
| `V2` | P3, P4; full coverage P10 | Staged by identifier family per § 8.7 |
| `V3` | P7 | — |
| `V4` | P4, P5 | — |
| `V5` | P7 | Evaluated per declared play mode |
| `V6` | P8 | Satisfiable now that all nineteen mapping rows are High |
| `V7` | P5, P6 | — |
| `V8` | **none** | `DEFERRED` by § 13. Not a pass requirement for any phase |
| `V9` | P5, P6 | — |
| `V10` | P1, staged to P7; full coverage P10 | — |
| `V11` | P7 | Satisfiable now that § 14.8 declares a priority order |

`V8` remains the only gate without a phase, deliberately. Its blockers — the leftover-time conflict between `04_TIME_COST_MATRIX.md` § 3 and `engine/05_TWO_PLAYER_SYNCHRONIZATION.md` § 4, and the absence of declared maximum split-window durations — are recorded in § 15. Promoting `V8` would be a scope change, not a specification fix, so it is not a precondition for any remaining phase.

---

## What each remaining phase will do

Stated so the executor needs no further interpretation.

**P5 (C5)** converts the progress model and assigns clue classes atomically. Every clue is worth 1 point per § 14.5, with computed maxima given there. The class-diversity counting rule from § 14.7 is written into `07_EVIDENCE_VALIDATION.md` § 1: one class per clue, assignment chosen to maximise diversity, N classes requiring at least N clues. Forty-four clues gain class tags, all 65 gain a point value, and `CON_MARCUS_LEAK` and `CON_ROOK_COMPROMISED` are marked `DEPRECATED` with `CON_REED_PRESENT` reglossed, per § 14.9.

**P6 (C6)** authors the two passphrase routes, the threshold, and the failure transformation. `00_CASE_OVERVIEW.md` is not touched, per § 14.4.

**P7 (C7)** adds `NODE_TYPE` to all 40 nodes, creates the eight terminal ending nodes with `END_SILENT_TERMINAL` typed `TIME_EXPIRED` per § 14.1, normalises all 40 `Outgoing` blocks, and writes the ending priority order into `14_ENDING_TRIGGER_MATRIX.md` § 1 per § 14.8. Split-branch terminators are out of scope per § 14.2, so C7 touches three files.

**P8 (C8)** publishes the backbone mapping with all nineteen rows at High confidence, records three unimplemented backbone elements, and corrects `02_MASTER_TIMELINE.md` § 20:05 to drop Café Orpheus from Player 2's starting leads per § 14.3.

**P9 (C9)** writes the release metadata: `adventure_schema_version` 0.1 → 1.0 in `adventures/The_Last_Witness/README.md` frontmatter, the changelog entry, and the README status corrections.

**P10** runs the full validation gate, including full-coverage `V2` and `V10`.

---

## Residual items, none of which block a phase

- **§ 14.6 duplicate-root-file policy.** `DEFERRABLE`. No commit in C1–C9 edits any of the eight byte-identical root copies or their twins, because this revision edits no engine file.
- **The `V8` cluster in § 15.** Split-window durations, the parallel-action conflict, scene-mode declarations and the split-branch terminator vocabulary. Four related two-player items, all deferred together.
- **Three unimplemented backbone elements**, now formally tracked in § 12.2: the fixed 22:10 trigger of `ARC_200`, the 21:45 Nadia failsafe inside `ARC_170`, and the "contact police first" option of `ARC_110`.
- **Other items in § 15**, including solo mode, the two-player delivery model and the complexity-budget overruns.

---

## Conclusion

The specification is complete for the remaining work. P5 through P10 may be executed in order against v2.4 with no further specification changes required.
