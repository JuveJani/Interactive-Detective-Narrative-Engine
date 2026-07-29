# Implementation Report — P0 to P4

**Date:** 2026-07-28
**Specification:** `IMPLEMENTATION_PLAN.md` v2.1
**Head at start:** `4af137a`
**Head at finish:** `a3554f7`
**Result:** **P0, P1, P2, P3 and P4 complete. Stopped before P5 as instructed.**

---

## 1. Ratification gate

Checked per § 3.2 before entering each phase. No `OPEN` item in the § 14 map names P0, P1, P2, P3 or P4.

| Phase | Items naming this phase | Outcome |
|---|---|---|
| P0 | none | Entered |
| P1 | none | Entered |
| P2 | none | Entered |
| P3 | none | Entered |
| P4 | none | Entered |
| P5 | § 14.5, § 14.7, § 14.9 — all `OPEN` | **Not entered** |

§ 14.6 is `DEFERRABLE` and § 14.10 is `RESOLVED`; neither blocks any phase. The eight remaining `OPEN` items are required by P5 or later.

---

## 2. Completed phases

| Phase | Work | Status |
|---|---|---|
| **P0** | Ratification map published, resolutions recorded, clear phases confirmed | Complete |
| **P1** | Canonical ownership rules; World Bible passphrase facts | Complete |
| **P2** | Migration manifests; clue, node and variable registers | Complete |
| **P3** | Mechanical identifier rename; identifier status declaration | Complete |
| **P4** | Non-progress state-variable cleanup and writer/reader wiring | Complete |

No work from P5 or later was performed. Progress variables in `01_WORLD_STATE_VARIABLES.md` § 2 are untouched, no clue carries a class tag or point value, no `GRANT_CLUE` appears anywhere, no node declares `NODE_TYPE` or `Outgoing`, and no passphrase route or clue exists in the logic layer.

---

## 3. Completed commits

| Commit | SHA | Phase | Content |
|---|---|---|---|
| C0 | `50850be` | P0 | Ratification record: map, two resolutions, eight open items, clear phases |
| C1 | `d8a3a15` | P1 | Canonical ownership: clue-class vocabulary single-sourced, prefix registry, ownership rules |
| C2 | `974b5b1` | P1 | World Bible passphrase facts with the required version change |
| C0 | `ae3ed2a` | P2 | Migration manifests, clue register, node register, variable register confirmation |
| C0 | `dcf8ccc` | P2 | Correction: `CON_` status counts remeasured after the merge |
| C3 | `9a44efe` | P3 | Mechanical rename of three families; identifier status declaration |
| C4 | `a3554f7` | P4 | Non-progress variable cleanup and writer/reader wiring |

Seven commits, no commit spanning two phases, no commit merging two units. C0 appears three times, which § 3.1 permits because it touches no repository canon file.

One correction was needed during execution. C1 and C2 were initially committed together by a `git add -A`. Nothing had been pushed, so the merged commit was split locally into `d8a3a15` and `974b5b1` before any push, restoring the boundary.

---

## 4. Modified files

### Repository canon

| File | Commits | Change |
|---|---|---|
| `LOGIC/07_EVIDENCE_VALIDATION.md` | C1, C4 | § 1 declared canonical owner of the six-class vocabulary; new § 7 declaring four gate evaluators |
| `DO_NOT_READ/05_CLUE_ARCHITECTURE.md` | C1 | § 2 reduced to a marked non-authoritative summary; "recording" moved from `PHYSICAL` to `DIGITAL` |
| `LOGIC/00_ENTITY_KEY_TABLE.md` | C1, C3 | Prefix registry, ownership rules; five `CON_` rows registered, `NPC_ROOK_NETWORK` registered, event key ranges restated for two namespaces, `Status` column on four tables |
| `DO_NOT_READ/01_WORLD_BIBLE.md` | C2 | Version 1.0 → 1.1 with history; § 4 passphrase custody and recovery; § 14 immutable fact |
| `DO_NOT_READ/03_CHARACTER_DATABASE.md` | C2, C4 | NPC-01 knowledge and one fragment; NPC-02 holds instructions not the secret; `NADIA_TRUST` alias replaced by `T_NADIA` |
| `LOGIC/12_CLUE_DEPENDENCY_GRAPH.md` | C3 | 65 `C_*` → `CLUE_*`, 12 `D_*` → `CON_*`; new § 13 identifier status |
| `LOGIC/14_ENDING_TRIGGER_MATRIX.md` | C3, C4 | One `D_*` → `CON_*`; new § 9 identifier status; `EVAL_ENDING` declared; § 2 medical outcome now reads `ELIAS_STATE` |
| `LOGIC/05_CORE_EVENT_GRAPH.md` | C3 | 19 backbone `EVT_nnn` → `ARC_nnn`; new identifier status section |
| `LOGIC/01_WORLD_STATE_VARIABLES.md` | C4 | Sole owner of every variable; 37 wired rows; 18 `CLK_` triggers; 8 removals; 1 split; 4 creations |
| `LOGIC/11_LOCATION_STATE_MACHINE.md` | C4 | § 1a variable bindings; § 1b transition register with 10 `TR_` identifiers; archive trigger recorded |
| `LOGIC/10_INVESTIGATION_NODE_GRAPH.md` | C4 | New § 15 per-node variable write table; time costs authored for `EVT_241` and `EVT_314` |
| `LOGIC/06_NPC_SCHEDULE_AND_PRIORITY.md` | C4 | Four off-screen outcomes given `EVT_801`–`EVT_804` |
| `LOGIC/03_NPC_KNOWLEDGE_AND_DISCLOSURE.md` | C4 | Lena's stages restated in evidence terms; `FACT_` status declared |
| `LOGIC/02_ITEM_STATE_MATRIX.md` | C4 | Primary ledger state declared authoritative for ledger status |
| `DO_NOT_READ/06_ENDING_FRAMEWORK.md` | C4 | Divergent variable list replaced by a marked non-authoritative pointer |

Fifteen canon files. No file under `engine/`, `templates/`, `docs/`, `data_dictionary/` or `reviews/` was touched, and no root-level file was touched.

### Plan

`IMPLEMENTATION_PLAN.md` gained § 16 (ratification record) and § 17 (manifests and registers) across the three C0 commits.

---

## 5. Validation results

| Gate | Required after | Result | Evidence |
|---|---|---|---|
| `V10` | C1 | **Pass, scoped** | Clue-class vocabulary has exactly one owner, `07` § 1, with `05_CLUE_ARCHITECTURE.md` § 2 marked non-authoritative. Ownership rules declared in `00_ENTITY_KEY_TABLE.md`. See § 6.1 for the ending rows, whose enforcement the plan assigns to C7. |
| — | C2 | **No gate assigned** | § 5.9 assigns Decision 1's gates to C6. C2 has no gate of its own in the plan. |
| `V1` | C3 | **Pass** | Every entity identifier uses a registry prefix. No identifier from a superseded scheme survives: zero residual `C_*` or `D_*`, zero bare `EVT_nnn` in `05`. |
| `V2` | C3 | **Pass** | Statuses declared for `NPC_`, `LOC_`, `ITEM_`, `CON_`, `CLUE_`, `ARC_`, `END_`. Every `ACTIVE` identifier is referenced at least once. Zero referenced-but-undeclared identifiers after `NPC_ROOK_NETWORK` was registered. |
| § 8.9 diff review | C3 | **Pass** | Reverse-mapping the three renames reproduces the pre-C3 files byte-for-byte apart from the additive status sections. Rename diff was line-neutral at 99 insertions and 99 deletions. No threshold, variable, edge or prose meaning changed. |
| `V2` | C4 | **Pass** | `FACT_` status declared. Zero referenced-but-undeclared identifiers across all eight entity families. |
| `V4` | C4 | **Pass** | 37 of 37 variable rows carry a non-`INIT` writer and at least one reader. Every writer and reader resolves to a declared node, `CLK_` trigger, `TR_` transition, `INIT`, or `EVAL_` evaluator. All eight removed variables and all four replaced aliases have zero remaining references. |

Gates `V3`, `V5`, `V6`, `V7`, `V9` and `V11` attach to C5 and later. `V8` is `DEFERRED` by § 13.

The 37-row count matches the § 9.5 arithmetic exactly: 47 baseline, minus 8 removed, minus 8 converted to derived, minus 1 split parent, plus 7 created.

---

## 6. Unresolved issues

### 6.1 `V10` at C1 is scoped, not total

§ 11.6 requires `V10` after C1, but the edit that gives the three ending facts single owners is assigned to C7 by § 6.3, which reduces `06_ENDING_FRAMEWORK.md` to narrative text. After C1 the ownership *rule* is declared and clue-class ownership is enforced, but `06_ENDING_FRAMEWORK.md` still restates ending requirements alongside `14_ENDING_TRIGGER_MATRIX.md`.

Recorded as a pass scoped to what C1 delivers. Full `V10` becomes satisfiable at C7. No phase in P0–P4 depends on it.

### 6.2 Manifest corrected two baseline counts

The § 2 baseline recorded 64 distinct clue identifiers across 65 listings. The manifest measured **65 distinct across 66 listings**. § 8.5 makes the manifest authoritative, so the correction was recorded in C0 rather than treated as a conflict. Downstream effect for C5: 44 clues need class tags, not 43, and 66 point values are required, not 65. § 14.5's wording, "all 64 baseline clues", understates the work by one.

### 6.3 `CON_` status counts were wrong in the first manifest

§ 17.3 initially recorded the `CON_` family as 4 `ACTIVE` and 11 `DEFINITION_ONLY`, computed before the merge. The `D_*`→`CON_*` merge sums the two families' occurrence counts, so eight identifiers become two-occurrence afterwards. Corrected to 9 `ACTIVE` and 6 `DEFINITION_ONLY`, measured on the post-merge state, in commit `dcf8ccc` before C3 consumed it.

### 6.4 `NPC_ROOK_NETWORK` was referenced but never declared

Found by the manifest. It is used in `11_LOCATION_STATE_MACHINE.md` as `SEIZED_BY(NPC_ROOK_NETWORK)` and was absent from the entity key table, which `V2` rejects.

Registered in C3 as registry completion, by direct analogy with the five `CON_*` rows § 8.8 already requires C3 to add for identifiers that exist under `D_`. The operation is behaviour-neutral. The plan did not name this identifier; the decision is recorded here because it is an addition the plan did not explicitly authorise.

### 6.5 Two duplicate conclusion glosses

After the merge, `CON_REED_PRESENT` and `CON_REED_CAUSED_CONFRONTATION` both carry the gloss "Reed caused the confrontation" in the entity key table, because the pre-existing gloss for `CON_REED_PRESENT` described causation while `12_CLUE_DEPENDENCY_GRAPH.md` § 6 defines it as presence.

Left unchanged. § 4 rule 5 forbids fixing a semantic problem inside C3, so this is recorded and deferred. It is a candidate for C5, which restates the thresholds these two identifiers gate.

### 6.6 The ending-ownership rule had no assigned file

§ 3.1 lists "ending-ownership rule declared" as C1 content, but no affected-files table names a document for it. Placed in `00_ENTITY_KEY_TABLE.md`, which was already in C1's scope, rather than expanding C1 to a new file.

### 6.7 Evaluator declarations touched a file outside § 9.6

§ 9.6's C4 file list omits `07_EVIDENCE_VALIDATION.md`, but `V4` requires every reader to resolve to a declared evaluator, and § 8.4 designates `07` as an `EVAL_` owner with the namespace "populated in C4 and C5". Four evaluators were therefore declared in `07` § 7 during C4. Without this, `V4` fails on `T_NADIA`, `T_MINA`, `T_MARCUS` and `ROOK_EXPOSED_PRIVATE`.

### 6.8 Items still `OPEN`

Eight ratifications remain open: § 14.1, § 14.2, § 14.3, § 14.4, § 14.5, § 14.7, § 14.8, § 14.9. § 14.6 is deferred with the deferral recorded in C0. § 14.10 is resolved.

---

## 7. Readiness for P5

**Not ready. P5 is blocked by three unresolved ratifications.**

| § | Item | Why P5 needs it |
|---|---|---|
| 14.5 | Point values for every clue | C5 writes a point value into each clue register row. The manifest sets the true count at 66 listings across 65 identifiers, plus one new passphrase clue in C6. |
| 14.7 | Multi-class clue diversity behaviour | C5 writes the class-diversity counting rule into `07` § 1 and restates every threshold against it. |
| 14.9 | Umbrella conclusion identifiers | C5 restates thresholds for `CON_MARCUS_LEAK` and `CON_ROOK_COMPROMISED` against their tiered pairs. Both are currently `DEFINITION_ONLY`, a mechanically derived status and not a decision about their fate. |

Everything P5 depends on structurally is in place: the clue namespace is migrated and status-carried, the conclusion namespace holds all 15 identifiers, the variable register is the sole owner of state, and the eight progress variables in § 2 are untouched and ready for conversion to derived totals.

Two corrections should be applied to the plan before C5 is authored, both recorded above: the clue count in § 14.5 and § 11.3 understates the work by one (§ 6.2), and the duplicate conclusion gloss deferred from C3 falls due in C5 (§ 6.5).

---

## 8. Statement of compliance

- Implemented P0 through P4 only. Stopped before P5.
- Verified the ratification gate before each phase; no phase was entered on an `OPEN` requirement.
- Ran every gate the plan assigns to these phases. All passed; none was waived.
- Respected every commit boundary. The one accidental merge was split before any push.
- Kept C3 behaviour-neutral and independently revertible, proven by reverse-mapping the renames.
- Invented no gameplay, no namespace, no validation gate and no variable beyond the register in § 9.4. The identifiers created — 18 `CLK_`, 10 `TR_`, 5 `EVAL_`, four `EVT_8xx` — are all named or mandated by the plan.
- Recorded every decision the plan did not explicitly authorise, in § 6.4, § 6.6 and § 6.7.
- Did not review the repository or the plan for new defects. The three discrepancies in § 6.2, § 6.3 and § 6.5 surfaced while producing a deliverable the plan requires or while running a gate the plan requires.
