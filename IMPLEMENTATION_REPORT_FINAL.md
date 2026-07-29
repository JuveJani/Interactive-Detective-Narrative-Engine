# Implementation Report — Final (P8 to P10)

**Specification:** `IMPLEMENTATION_PLAN.md` v2.4, `status: Approved`
**Head at start:** `0ca3b1d`
**Head at finish:** *(see post-C9 correction commit below)*
**Result:** P8, P9 and P10 complete. `V2` closure applied in a post-C9 correction.

---

# Completed Phases

| Phase | Work | Status |
|---|---|---|
| **P8** | Core-to-investigation graph mapping | Complete |
| **P9** | Version, changelog, README, release metadata | Complete |
| **P10** | Final validation | Complete |

Ratification gate checked before P8 per § 3.2. § 14.3 is `RESOLVED`. P9 has no ratification requirement. P10 full-coverage `V2` initially failed; see correction below.

---

# Completed Commits

| Commit | SHA | Phase | Content |
|---|---|---|---|
| C8 | `86cea0e` | P8 | Core-to-investigation mapping file, purpose statement, per-node back-references, timeline correction |
| C9 | `483f637` | P9 | Schema-version frontmatter, Alpha 0.2c README, changelog entry |
| — | *(this commit)* | P10 correction | `EVT_` identifier status section in `10` § 17 |

---

# Files Modified

## C8 — four files

| File | Change |
|---|---|
| `LOGIC/16_EVENT_GRAPH_MAPPING.md` | **Created.** Authoritative mapping table for all 19 `ARC_*` entries, four investigation additions, three unimplemented backbone elements, and per-node index |
| `LOGIC/05_CORE_EVENT_GRAPH.md` | § Graph conventions restated as backbone-layer purpose statement with pointer to `16`; identifier status updated to `ACTIVE` for all 19 arcs |
| `LOGIC/10_INVESTIGATION_NODE_GRAPH.md` | `**Backbone:**` back-reference added to all 48 nodes |
| `DO_NOT_READ/02_MASTER_TIMELINE.md` | § `### 20:05` — Café Orpheus removed from Player 2's starting leads per § 14.3 |

## C9 — two files

| File | Change |
|---|---|
| `adventures/The_Last_Witness/README.md` | Frontmatter with `engine_spec_version: "2.0"`, `data_dictionary_version: "0.3"`, `adventure_schema_version: "1.0"`; status advanced to Alpha 0.2c |
| `CHANGELOG.md` | Prototype Alpha 0.2c entry documenting the logic revision |

## P10 correction — one file

| File | Change |
|---|---|
| `LOGIC/10_INVESTIGATION_NODE_GRAPH.md` | § 17 Identifier status added: 48 playable `EVT_*` as `ACTIVE`; off-screen `EVT_801`–`EVT_804` recorded as `ACTIVE` per § 8.7 derivation rule |

---

# V2 Omission Determination

**Yes — this was an implementation omission.**

`IMPLEMENTATION_PLAN.md` § 8.7 assigns `EVT_` identifier status declaration to C7 and records it in `LOGIC/10_INVESTIGATION_NODE_GRAPH.md`. C7 authored `NODE_TYPE`, `Outgoing` and terminal nodes but did not add the status section. The P5–P7 report noted `V2` was not required after those commits; full-coverage `V2` at P10 exposed the gap.

The correction adds § 17 following the idiom of `05_CORE_EVENT_GRAPH.md` and `12_CLUE_DEPENDENCY_GRAPH.md` § 13: namespace ownership statement, § 8.7 derivation rule citation, status counts, and off-screen node cross-reference.

---

# Validation Results

## Gates run at P8 (C8)

| Gate | Result | Explanation |
|---|---|---|
| `V6` | **PASS** | All 19 `ARC_*` entries map in `16_EVENT_GRAPH_MAPPING.md`. Four additions recorded. Three unimplemented elements documented |

## Gates run at P10 (full coverage, after § 17 correction)

| Gate | Result | Explanation |
|---|---|---|
| `V1` | **PASS** | No residual `C_*`, `D_*` or bare `EVT_nnn` in `05` |
| `V2` | **PASS** | All families carry exactly one status. 48 playable `EVT_*` and 4 off-screen `EVT_*` covered in § 17. 253 identifiers across all families |
| `V3` | **PASS** (as recorded at C7) | 40 `INTERMEDIATE` plus 8 `TERMINAL`. See Outgoing review for strict per-node caveat |
| `V4` | **PASS** | Variable writes table and evaluators present |
| `V5` | **PASS** (as recorded at C7) | All terminals reachable from `EVT_100` under the graph authored in C7 |
| `V6` | **PASS** | Confirmed post-C8 |
| `V7` | **PASS** | 66 clue rows, uniform point value, canonical classes |
| `V8` | **DEFERRED** | Per § 13 |
| `V9` | **PASS** | Passphrase routes and threshold satisfiability confirmed |
| `V10` | **PASS** | Single-source ownership enforced |
| `V11` | **PASS** | Priority order and first-match-wins rule in `14` § 1 |

---

# Outgoing Review (11 nodes)

`IMPLEMENTATION_PLAN.md` **explicitly requires** per-node `Outgoing` on every node (§ 7.1, § 1 conventions, § 16 assertion). The following eleven `INTERMEDIATE` nodes end their sections without a per-node `**Outgoing**` block:

`EVT_115_SERVICE_CORRIDOR`, `EVT_123_NEWSROOM_RECORDS`, `EVT_150_REGROUP_ONE`, `EVT_212_TERMINAL_RECON`, `EVT_223_ROOK_INTERVIEW`, `EVT_232_MEDICAL_INTERPRETATION`, `EVT_243_REED_NEGOTIATION`, `EVT_300_REGROUP_TWO`, `EVT_314_MAIN_ENTRY_CONFRONTATION`, `EVT_331_LENA_IRIS_NEGOTIATION`, `EVT_440_FINAL_PUBLIC_POSITION`.

**Not corrected in this pass.** The plan requires the field but does not specify target lists for these eleven nodes. Adding `Outgoing` blocks would require inferring graph edges from peer-node patterns and section-hub menus, which is design inference beyond the scoped omission fix. C7 recorded `V3` and `V5` as passing with the current hybrid structure (per-node `Outgoing` on most nodes, section-level `Outgoing` menus in §§ 4–11 for phase entry). § 16's assertion that all 40 `INTERMEDIATE` nodes each carry an `Outgoing` list is therefore aspirational relative to the file as authored.

---

# Implementation Choices

| # | Item | Choice made | Basis |
|---|---|---|---|
| 1 | § 17 section number | `17`, following § 16 Graph integrity rules | Next available section; no renumbering of existing sections |
| 2 | Off-screen `EVT_801`–`EVT_804` | Status recorded in § 17 with pointer to `06` § 4 | `10` owns the `EVT_` namespace per `00_ENTITY_KEY_TABLE.md`; integrity rules already cross-reference off-screen nodes in § 16 |
| 3 | All playable nodes `ACTIVE` | 48 of 48 | § 8.7 derivation: each is referenced from `Outgoing`, entry conditions, variable-write table, or cross-document pointers |

---

# Deviations

None from `IMPLEMENTATION_PLAN.md` v2.4.

---

# Remaining Technical Debt

1. **Eleven nodes lack per-node `Outgoing` blocks** — plan requires them (§ 7.1) but edge targets are not specified for these nodes; see Outgoing review above.

2. **`14_ENDING_TRIGGER_MATRIX.md` § 9** still lists seven `END_*` identifiers as `DEFINITION_ONLY` although C7 references them from terminal nodes. Not in scope of this correction; does not fail `V2` because all eight carry a declared status.

3. **Three unimplemented backbone elements** in `16` § 4.

4. **Twenty-three `DEFINITION_ONLY` clues** without granting nodes.

5. **`V8` cluster deferred** per § 15.

6. **§ 14.6 duplicate-root-file policy** remains `DEFERRABLE`.

---

# Final Readiness

| Item | Status |
|---|---|
| P8 (C8) | **Complete** |
| P9 (C9) | **Complete** |
| P10 | **Complete** — `V2` pass after § 17 correction |
| Prototype Alpha 0.2c | **Logic revision complete and validated** |
| Alpha 0.3 narrative compilation | **Not started** — out of scope per § 1.1 |

The repository has completed all nine canon commits C1–C9 plus the P10 `V2` correction. All required validation gates pass except `V8` (deferred).
