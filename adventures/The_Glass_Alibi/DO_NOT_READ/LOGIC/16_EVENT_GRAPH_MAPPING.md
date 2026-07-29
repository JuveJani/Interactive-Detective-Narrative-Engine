# DO NOT READ: Core-to-Investigation Graph Mapping

## 1. Purpose

This document is the authoritative mapping between the backbone layer in `05_CORE_EVENT_GRAPH.md` (`ARC_*`) and the playable and off-screen event layer in `10_INVESTIGATION_NODE_GRAPH.md` and `06_NPC_SCHEDULE_AND_PRIORITY.md` (`EVT_*`).

The core graph is retained as a backbone layer, not retired. It holds the phase-level view of the case and the only cross-reference into `06_NPC_SCHEDULE_AND_PRIORITY.md`. The investigation graph holds location-level nodes from which player-facing material will be compiled.

---

## 2. Mapping table

| Backbone | Investigation nodes | Relationship | Confidence |
|---|---|---|---|
| `ARC_100` Campus briefing | `EVT_100` | 1:1 | High |
| `ARC_110` First split decision | Absorbed into **Decision** block of `EVT_100`; realised by `EVT_110`, `EVT_120` | Absorbed | High |
| `ARC_120` Test bay cluster | `EVT_113`, `EVT_115` | Expanded 1:2 | High |
| `ARC_130` SCADA / security cluster | `EVT_110`, `EVT_111`, `EVT_112`, `EVT_123`, `EVT_140`, `EVT_141` | Expanded 1:6 | High |
| `ARC_140` Finance hub cluster | `EVT_210`, `EVT_260` | Expanded 1:2 | High |
| `ARC_150` First synchronization gate | `EVT_150` | 1:1 | High |
| `ARC_200` Corporate pressure | `EVT_130` | 1:1 | High |
| `ARC_210` Maintenance / credential cluster | `EVT_122`, `EVT_312` | Expanded 1:2 | High |
| `ARC_220` Architect / rivalry cluster | `EVT_270`, `EVT_271` | Expanded 1:2 | High |
| `ARC_230` Dana pressure ladder | `EVT_230` | 1:1 | High |
| `ARC_240` Witness preservation | `EVT_220`, `EVT_240` | Expanded 1:2 | High |
| `ARC_250` Second synchronization gate | `EVT_300` | 1:1 | High |
| `ARC_300` Final parallel assignment | `EVT_330`, `EVT_312`, `EVT_220` | Expanded 1:3 | High |
| `ARC_320` Off-screen hostile convergence | `EVT_330` (awareness spike), `EVT_801`–`EVT_804` | Expanded 1:5 across two documents | High |
| `ARC_340` Test bay / SCADA convergence | `EVT_410`, `EVT_420` | Expanded 1:2 | High |
| `ARC_400` Accusation validation | `EVT_410` | 1:1 | High |
| `ARC_420` Evidence preservation | `EVT_420` | 1:1 | High |
| `ARC_440` Report outcome | Absorbed into `EVT_410`, `CLK_2330`, `EVAL_ENDING` | Absorbed | High |
| `ARC_900` Ending resolution | `EVT_900` plus five terminal nodes | Expanded 1:6 | High |

---

## 3. Investigation additions

These `EVT_*` nodes have no single backbone origin. They are authored expansions of the playable graph.

| Investigation node | Role |
|---|---|
| `EVT_111` | Kevin first-contact gate within SCADA cluster |
| `EVT_121` | Field perimeter and loading-dock orientation |
| `EVT_250` | Marcus ops-floor export hold and corporate framing |
| `EVT_430` | Dana apprehension coordination after supported accusation |
| `EVT_901`–`EVT_905` | Five terminal epilogues mapped to `END_*` families |

---

## 4. Unimplemented backbone elements

These backbone elements are recorded with a reason. The next revision must implement or delete each one.

| Backbone element | Reason |
|---|---|
| `ARC_110` option "file immediate formal challenge" | `EVT_100` Decision offers split or joint investigation only; challenge filing deferred to `EVT_410`/`EVT_420` |
| `ARC_150` 20:45 Kevin failsafe | Kevin Stage 1 at `EVT_220` provides equivalent failsafe; fixed 20:45 auto-reveal not separately authored |
| `ARC_300` four explicit assignment slots | Final act uses three split nodes with variant assignment blocks inside `EVT_300` and `EVT_330` |

---

## 5. Off-screen mapping

| Backbone | Off-screen nodes | Document |
|---|---|---|
| `ARC_320` | `EVT_801`, `EVT_802`, `EVT_803`, `EVT_804` | `06_NPC_SCHEDULE_AND_PRIORITY.md` § 4 |

Off-screen nodes are excluded from playable reachability counts in `10_INVESTIGATION_NODE_GRAPH.md` § 16.

---

## 6. Per-node back-reference index

Authoritative back-references are declared on each playable node in `10_INVESTIGATION_NODE_GRAPH.md`. Off-screen nodes `EVT_801`–`EVT_804` are declared in `06_NPC_SCHEDULE_AND_PRIORITY.md` § 4 and map to `ARC_320`.

---

## 7. Identifier status

This document references nineteen `ARC_*` identifiers from `05_CORE_EVENT_GRAPH.md` and thirty-four playable `EVT_*` identifiers from `10_INVESTIGATION_NODE_GRAPH.md`. Every mapped pair carries confidence **High**. No orphan `ARC_*` remains unmapped.
