# Implementation Readiness — P5 to P10

**Specification:** `IMPLEMENTATION_PLAN.md` v2.3
**Date:** 2026-07-28
**Question:** can P5 through P10 be executed without further specification changes?

---

## Answer

**No. P5, P6 and P7 can be executed now. P8 cannot, and P10 inherits that block by running last.**

One ratification remains open: **§ 14.3, Low and Medium confidence mapping rows**, required by P8 (C8). It was not in the set this revision was scoped to resolve.

---

## Phase-by-phase

| Phase | Commit | Ratifications required | Status | Executable now |
|---|---|---|---|---|
| P5 | C5 | § 14.5, § 14.7, § 14.9 | all RESOLVED | **Yes** |
| P6 | C6 | § 14.4 | RESOLVED | **Yes** |
| P7 | C7 | § 14.1, § 14.2, § 14.8 | all RESOLVED | **Yes** |
| P8 | C8 | § 14.3 | **OPEN** | **No** |
| P9 | C9 | none | — | Yes, once P8 completes |
| P10 | none | none | — | Yes, once P8 and P9 complete |

P9 and P10 have no ratification of their own. They are blocked only transitively, because § 3 makes the phase order strict.

---

## What § 14.3 needs

`IMPLEMENTATION_PLAN.md` § 12.2 carries five backbone mapping rows below High confidence, and § 14.3 is the decision on all five:

| Row | Relationship | Confidence |
|---|---|---|
| `ARC_110` First split decision | Absorbed into `EVT_100`'s Decision block, realised by `EVT_110` and `EVT_120` | Medium |
| `ARC_140` Café cluster | Relocated from the opening block to the midgame | **Low** |
| `ARC_200` Rook pressure | Partial, maps to `EVT_223` only | Medium |
| `ARC_240` Mina evidence preservation | Partial and split across `EVT_220` and `EVT_400` | Medium |
| `ARC_320` Off-screen hostile convergence | Split across `EVT_420` and `EVT_801`–`EVT_804` | Medium |

The `ARC_140` row is the one with a content consequence, recorded in § 12.4: `02_MASTER_TIMELINE.md` § 20:05 assigns Café Orpheus to Player 2 as a starting lead, while the investigation graph places it in the midgame harbor branch. Either the timeline changes or the node moves back. The other four rows are classification judgements about how a backbone arc expanded, with no content effect.

Resolving § 14.3 unblocks P8, and with it P9 and P10.

---

## Validation gate coverage

Every gate has an assigned phase except one, and that exception is deliberate.

| Gate | Phase or phases | Note |
|---|---|---|
| `V1` | P3, P6 | — |
| `V2` | P3, P4; full coverage P10 | Staged by family per § 8.7 |
| `V3` | P7 | — |
| `V4` | P4, P5 | — |
| `V5` | P7 | Evaluated per declared play mode |
| `V6` | P8 | Blocked with P8 |
| `V7` | P5, P6 | — |
| `V8` | **none** | `DEFERRED` by § 13. Not a pass requirement for any phase |
| `V9` | P5, P6 | — |
| `V10` | P1, staged to P7; full coverage P10 | — |
| `V11` | P7 | Satisfiable now that § 14.8 declares a priority order |

`V8` is the only gate without a phase. Its blockers — the leftover-time conflict between `04_TIME_COST_MATRIX.md` § 3 and `engine/05_TWO_PLAYER_SYNCHRONIZATION.md` § 4, and the absence of declared maximum split-window durations — are out of scope for this revision and recorded in § 15. Promoting `V8` to a required gate would need those blockers brought into scope, which is a scope change, not a specification fix.

---

## Dependencies that are settled

These were open before v2.3 and are now decided, so no phase waits on them:

- The terminal type for `END_SILENT_TERMINAL` is `TIME_EXPIRED`, and the governing rule that a terminal type classifies the terminating condition rather than a character's fate also discharges the last Medium row in § 6.2. All eight rows are now High.
- The split-branch terminator vocabulary is out of scope for C7 and deferred to § 15, so C7 authors `Outgoing` without it and `V3` and `V5` validate C7 as written.
- The passphrase adds no chain to `00_CASE_OVERVIEW.md`, so C6 gains no file and no work from that question.
- Ending-family precedence is a declared priority order written into `14_ENDING_TRIGGER_MATRIX.md` § 1 by C7, which is what makes `V11` satisfiable.

---

## Recommendation

Execute P5, P6 and P7 now. They have no unresolved dependency, every gate they run is assigned, and the specification requires no further change to support them.

Before P8, resolve § 14.3. It is a single decision covering five mapping rows, only one of which — the café relocation — has a content consequence to settle.

Two items already recorded remain outside this revision and do not block any phase: § 14.6, the duplicate-root-file policy, marked `DEFERRABLE` because no commit in C1–C9 edits an affected file; and the `V8` cluster in § 15.
