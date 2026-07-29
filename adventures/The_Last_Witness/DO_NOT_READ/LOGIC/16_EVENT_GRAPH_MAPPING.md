# DO NOT READ: Core-to-Investigation Graph Mapping

## 1. Purpose

This document is the authoritative mapping between the backbone layer in `05_CORE_EVENT_GRAPH.md` (`ARC_*`) and the playable and off-screen event layer in `10_INVESTIGATION_NODE_GRAPH.md` and `06_NPC_SCHEDULE_AND_PRIORITY.md` (`EVT_*`).

The core graph is retained as a backbone layer, not retired. It holds the phase-level view of the case and the only cross-reference into `06_NPC_SCHEDULE_AND_PRIORITY.md`. The investigation graph holds location-level nodes from which player-facing material will be compiled.

## 2. Mapping table

| Backbone | Investigation nodes | Relationship | Confidence |
|---|---|---|---|
| `ARC_100` Nadia's briefing | `EVT_100` | 1:1 | High |
| `ARC_110` First split decision | Absorbed into the **Decision** block of `EVT_100`; realised by `EVT_110`, `EVT_120` | Absorbed; one option unimplemented | High |
| `ARC_120` Apartment cluster | `EVT_110`, `EVT_111`, `EVT_112`, `EVT_113`, `EVT_114`, `EVT_115` | Expanded 1:6 | High |
| `ARC_130` Newsroom cluster | `EVT_120`, `EVT_121`, `EVT_122`, `EVT_123` | Expanded 1:4 | High |
| `ARC_140` Café cluster | `EVT_211` | Relocated, opening block to midgame; timeline corrected in C8 | High |
| `ARC_170` First synchronization gate | `EVT_150` | 1:1, renumbered | High |
| `ARC_200` Rook pressure | `EVT_223` | 1:1 on content; trigger partly unimplemented | High |
| `ARC_210` Reed office opportunity | `EVT_242` | 1:1 | High |
| `ARC_220` Iris trail | `EVT_230`, `EVT_231`, `EVT_232` | Expanded 1:3 | High |
| `ARC_230` Marcus disclosure ladder | `EVT_240`, `EVT_241` | Expanded 1:2 | High |
| `ARC_240` Mina evidence preservation | `EVT_220`, `EVT_221`, `EVT_400` | Expanded 1:3 | High |
| `ARC_270` Second synchronization gate | `EVT_300` | 1:1, renumbered | High |
| `ARC_300` Terminal route selection | `EVT_310`–`EVT_314` | Expanded 1:5 | High |
| `ARC_320` Off-screen hostile convergence | `EVT_420`, `EVT_801`–`EVT_804` | Expanded 1:5 across two documents | High |
| `ARC_340` Signal Room discovery | `EVT_330`, `EVT_331` | Expanded 1:2, renumbered | High |
| `ARC_400` Trusted rescue validation | `EVT_400` | 1:1 | High |
| `ARC_420` Evidence transfer | `EVT_410`, `EVT_430` | Expanded 1:2 | High |
| `ARC_440` Final accusation | `EVT_440` | 1:1 | High |
| `ARC_900` Ending resolution | `EVT_900` plus eight terminal nodes | Expanded 1:9 | High |

## 3. Investigation additions

These `EVT_*` nodes have no backbone origin. They are authored expansions of the playable graph.

| Investigation node | Role |
|---|---|
| `EVT_210_HARBOR_ARCHIVE_ENTRY` | Harbor archive research cluster entry |
| `EVT_212_TERMINAL_RECON` | Terminal exterior reconnaissance |
| `EVT_222_PROTECTION_ORDER_AUDIT` | Protection-order audit route |
| `EVT_243_REED_NEGOTIATION` | Reed negotiation alternative to office search |

## 4. Unimplemented backbone elements

These backbone elements are recorded with a reason. The next revision must implement or delete each one.

| Backbone element | Reason |
|---|---|
| `ARC_110` option "contact police first" | `EVT_100`'s Decision block offers split or joint investigation only; no police-first route is authored |
| `ARC_200` fixed no-later-than-22:10 trigger | Awareness trigger is wired; the fixed 22:10 alternative has no authored node |
| `ARC_170` 21:45 Nadia ferry-infrastructure failsafe | No node implements the failsafe that reveals harbor infrastructure when `P_HARBOR < 2` by 21:45 |

## 5. Per-node back-reference index

Authoritative back-references are declared on each node in `10_INVESTIGATION_NODE_GRAPH.md`. Off-screen nodes `EVT_801`–`EVT_804` are declared in `06_NPC_SCHEDULE_AND_PRIORITY.md` § 4 and map to `ARC_320`.
