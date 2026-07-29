# DO NOT READ: Core Event Graph

## Graph conventions

Each event record includes:

- trigger;
- earliest/latest time;
- participants;
- preconditions;
- state effects;
- knowledge effects;
- outgoing routes;
- failure transformation.

This file defines the **backbone layer only**. It is retained alongside the playable investigation graph in `10_INVESTIGATION_NODE_GRAPH.md`. The authoritative mapping between `ARC_*` and `EVT_*` is owned by `16_EVENT_GRAPH_MAPPING.md`.

---

## ARC_100: Campus briefing

**Time:** 19:00-19:10  
**Participants:** both roles, corporate liaison (NPC Marcus voice)  
**Effects:** opens test bay, SCADA, and security lead clusters; sets initial corporate framing as automation accident.  
**Private split:** Role A (field/scene emphasis) receives test-bay access route. Role B (systems/finance emphasis) receives SCADA or security desk route.  
**Failure transformation:** refusing corporate framing still begins investigation through Kevin's mandatory historian export request and Sable's public incident log.

## ARC_110: First split decision

Players may:

- split between test bay and SCADA/security;
- investigate together at briefing wing;
- file immediate formal challenge (costly, opens legal observer path).

No time-critical puzzle depends on information held only by the other role during the split. Each branch yields an independent route toward `CON_MURDER_NOT_ACCIDENT` or `CON_CREDENTIAL_ABUSE`.

## ARC_120: Test bay cluster

Potential gains:

- CO₂ anomaly and injury pattern;
- sensor spoof fragment;
- Elena tablet access path;
- `CHK_115_PERCEPTION` on concealed spoof.

Risks:

- corporate evidence seal after 19:30;
- partial scene clearance if `A_CORPORATE >= 2`.

Alternative if access denied:

- Kevin historian cross-reference;
- Sable perimeter camera stills;
- Priya's emailed safety dispute.

## ARC_130: SCADA / security cluster

Potential gains:

- manual purge log;
- badge swipe mismatch;
- after-hours access record;
- Sable/Kevin disclosure stages.

Risks:

- Marcus export hold;
- Vince camera gap exploitation;
- `A_SECURITY` escalation.

Alternative if blocked:

- maintenance shed work-order route;
- finance hub approval pattern;
- Tom schedule contradiction.

## ARC_140: Finance hub cluster

Potential gains:

- ledger discrepancy;
- shell vendor trail;
- Dana approval bursts;
- Elena audit memo unlock.

Risks:

- evening audit window closes 21:30;
- Dana misdirection;
- corporate seal.

Alternative:

- tablet memo alone can open partial fraud thread;
- Priya email thread via architect lab.

## ARC_150: First synchronization gate (`EVT_150`)

**Recommended time:** 20:20-20:40.  
Players regroup physically or perform a legal remote exchange. At least one private clue from each route enters shared knowledge.

Next-stage lead set:

- murder thread if `P_MURDER >= 2`;
- fraud thread if `P_FRAUD >= 1`;
- credential thread if `P_CREDENTIAL >= 1`;
- Dana focus if any two threads have started.

Failsafe: Kevin reveals manual purge flag at cost of corporate hostility if no thread has 2 points by 20:45.

## ARC_200: Corporate pressure

Triggered by `A_CORPORATE >= 1` or fixed no later than 21:15.

Corporate liaison frames accident narrative and offers settlement. Players may:

- accept supervised access;
- challenge with partial proof;
- route through formal incident challenge;
- split to preserve copies off-network.

This event never proves murder or fraud by itself.

## ARC_210: Maintenance / credential cluster

Available from 20:30.

Entry vectors:

- Tom interview;
- shed search (`CHK_312_ATHLETICS` for cable-tray adjacency);
- forged work-order comparison;
- badge clone discovery.

Potential gains:

- `ITEM_BADGE_CLONE`;
- forged work order;
- Tom auth contradiction;
- Dana panel walkthrough fact.

No unique critical conclusion depends solely on athletics success.

## ARC_220: Architect / rivalry cluster

Triggered by Priya lab access or Elena tablet thread.

Routes:

- Priya interview;
- design approval records;
- vendor warning email;
- Vince calibration excuse cross-check.

Conclusion support: fraud motive and Dana expedite channel, not Priya as killer.

## ARC_230: Dana pressure ladder

Dana can provide:

- liability minimization talking points;
- partial admission of "process shortcuts";
- redirect toward Vince or Tom;
- full exposure only when cornered with `CON_CULPRIT_DANA` evidence at `EVT_410`.

If Dana flees, off-screen events `EVT_801-803` apply.

## ARC_240: Witness preservation (Sable / Kevin)

Available after players provide procedural inconsistency.

Witnesses may:

- preserve unaltered footage;
- export complete historian;
- later support formal challenge.

At low trust they provide hints but not operational exports.

## ARC_250: Second synchronization gate (`EVT_300`)

**Latest recommended time:** 22:45.

Players exchange all essential threads before final parallel assignment. Split-only clues cannot be required for a live puzzle before this gate.

Possible shared conclusions:

- murder not accident at threshold;
- fraud and credential threads converging;
- Dana as primary suspect;
- evidence preservation plan or gap identified.

## ARC_300: Final parallel assignment

Roles divide for Split Three:

1. confront / trace Dana at finance or parking;
2. secure external evidence transmission;
3. detain or document Vince/Tom as cutouts;
4. preserve SCADA + security copies.

At least two assignment pairs remain valid in every legal state. Losing one export path never blocks terminal accusation completely.

## ARC_320: Off-screen hostile convergence

Dana and Vince advance per `06_NPC_SCHEDULE_AND_PRIORITY.md`. Players may encounter cleanup in progress, missed flee, or intact evidence.

## ARC_340: Test bay / SCADA convergence

Upon sufficient proof, players choose:

- file homicide challenge before `CLK_2330`;
- preserve copies externally;
- coordinate security apprehension;
- split interior documentation vs exterior relay.

Both roles must hold decisions, not merely checks.

## ARC_400: Accusation validation

Formal accusation at `EVT_410` requires naming `NPC_*`. Result depends on evidence support:

- correct and supported: `CON_CULPRIT_DANA`, custody path;
- correct but under-supported: contested partial ending;
- wrong but evidence-linked: specific rebuttal (`07` § 3);
- arbitrary: credibility collapse without erasing discovered truth.

## ARC_420: Evidence preservation

External durable copy requires at least one preserved `COPIED` or `TRANSMITTED` artifact among ledger, historian, footage, or tablet memo before `CLK_0030`.

## ARC_440: Report outcome

`REPORT_STATE` resolves at `CLK_2330` unless players filed challenge. Homicide submission requires `CON_MURDER_NOT_ACCIDENT`; fraud exposure requires `CON_FINANCIAL_FRAUD`.

## ARC_900+: Ending resolution

Ending variables evaluated after accusation, preservation, and deadline. Multiple achievements can succeed or fail independently.

---

## Identifier status

This document owns the `ARC_` namespace. Nineteen backbone identifiers are declared:

`ARC_100`, `ARC_110`, `ARC_120`, `ARC_130`, `ARC_140`, `ARC_150`, `ARC_200`, `ARC_210`, `ARC_220`, `ARC_230`, `ARC_240`, `ARC_250`, `ARC_300`, `ARC_320`, `ARC_340`, `ARC_400`, `ARC_420`, `ARC_440`, `ARC_900`.

Every one is `ACTIVE`. Each is referenced from at least one investigation node in `10_INVESTIGATION_NODE_GRAPH.md` or from `16_EVENT_GRAPH_MAPPING.md`.

The `ARC_` prefix distinguishes these backbone arcs from playable and off-screen `EVT_` nodes. A given number may appear in both namespaces and the two are not interchangeable.
