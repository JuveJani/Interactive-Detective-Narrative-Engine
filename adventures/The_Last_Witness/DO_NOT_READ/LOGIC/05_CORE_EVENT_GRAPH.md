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

This file defines the backbone only. Alpha 0.2b will expand location-level nodes.

---

## EVT_100: Nadia's briefing

**Time:** 20:00-20:10  
**Participants:** both players, Nadia  
**Effects:** opens apartment and newsroom/café lead clusters; sets Nadia trust according to response.  
**Private split:** Player 1 receives Mina access route. Player 2 receives newsroom access route.  
**Failure transformation:** refusing Nadia's framing still begins the case through Mina's official request and a public missing-person bulletin.

## EVT_110: First split decision

Players may:

- split between apartment and newsroom/café;
- investigate together;
- contact police first.

No time-critical puzzle depends on information held only by the other player during the split. Each branch yields an independent route toward `CON_STAGED_DISAPPEARANCE` or `CON_HARBOR_DESTINATION`.

## EVT_120: Apartment cluster

Potential gains:

- staging evidence;
- Mina trust;
- service-corridor route;
- timed-device clue before removal.

Risks:

- Rook awareness;
- evidence restriction after 21:00;
- timed-device removal after 22:15.

Alternative if access denied:

- neighbour interview;
- laundry-service records;
- Mina's original observations outside the scene.

## EVT_130: Newsroom cluster

Potential gains:

- Nadia staged-disappearance admission;
- upload mechanism;
- missing photograph;
- Marcus pressure/motive.

Risks:

- Marcus deletes data;
- Nadia trust loss;
- Rook learns of archive searches.

Alternative if Marcus blocks access:

- Nadia provides account extract;
- external carrier log route;
- later Marcus meeting event.

## EVT_140: Café cluster

Potential gains:

- tide note;
- footage of Elias and Nadia;
- Lena reflection;
- old-line power question.

Soft-lock prevention:

- if footage overwrites, barista testimony and receipt remain;
- if owner refuses access, delivery driver supplies the reflection/timing clue;
- no lockpicking is mandatory.

## EVT_170: First synchronization gate

**Recommended time:** 21:20-21:40.  
Players regroup physically or perform a legal remote exchange. At least one piece of private information from each route enters shared knowledge.

The next-stage lead set is calculated:

- harbor route if `P_HARBOR >= 2`;
- Rook suspicion route if `P_ROOK >= 1`;
- Reed route if decoy/vehicle evidence exists;
- Marcus route if leak indicators exist.

Failsafe: Nadia reveals that Elias had discussed old ferry infrastructure, at a cost of trust and time, if no harbor route has been formed by 21:45.

## EVT_200: Rook pressure

Triggered by `A_ROOK_PLAYERS >= 2` or fixed no later than 22:10.

Rook offers cooperation and frames Lena as abductor. Players may:

- accept limited access;
- challenge him;
- conceal progress;
- route information through Mina.

This event never proves Rook's corruption by itself.

## EVT_210: Reed office opportunity

Available from 21:30.

Entry vectors:

- lawful cooperation from garage manager;
- Reed invitation/negotiation;
- visible abandoned door after 22:30;
- alternate network trace if physical office becomes unavailable.

Potential gains:

- decoy key;
- Krell message;
- harbor grit/blood;
- tracker evidence.

No unique critical conclusion depends solely on forced entry.

## EVT_220: Iris trail

Triggered by missing supplies, Lena phone trace, or workplace witness.

Routes:

- workplace interview;
- parking camera;
- medical inventory;
- independent phone-record request.

Conclusion: someone is treating a concealed head injury near the harbor.

## EVT_230: Marcus disclosure ladder

Marcus can provide:

- low-risk financial pressure facts;
- partial admission of archive access;
- full leak confession after two hard pressures.

If he flees, the carrier record and intermediary meeting remain.

## EVT_240: Mina evidence preservation

Available after players provide at least one procedural inconsistency.

Mina may:

- preserve her report version;
- identify camera authorization problem;
- later create trusted rescue route.

At low trust she provides a hint but not direct operational help.

## EVT_270: Second synchronization gate

**Latest recommended time:** 23:15.

Players must exchange all essential route information before entering terminal convergence. Split-only clues cannot be required for a live puzzle before this gate.

Possible shared conclusions:

- terminal strongly identified;
- room number partially identified;
- Rook compromised to threshold;
- concealed injured person inferred;
- trusted rescue option prepared or still missing.

## EVT_300: Terminal route selection

Available access routes:

1. cable corridor via map/photo;
2. drainage route before 23:30;
3. north maintenance gate through archivist/maintenance clue;
4. main entrance under confrontation conditions;
5. emergency service entry with Mina/paramedic.

At least two routes remain possible in every legal state. Losing one item never blocks the terminal completely.

## EVT_320: Off-screen hostile convergence

Reed and Rook advance according to awareness and schedules. Priority resolution is defined in `06_NPC_SCHEDULE_AND_PRIORITY.md`.

Players may encounter:

- Reed alone;
- Lena/Iris before Reed;
- Rook's team outside;
- both hostile factions in sequence;
- neither, if they moved quickly and quietly.

## EVT_340: Signal Room discovery

Upon entry, `CON_MEDICAL_EMERGENCY` becomes apparent without a difficult diagnostic gate.

Immediate choices:

- stabilize and dispatch rescue;
- secure/copy primary ledger;
- negotiate with Lena;
- protect entrance;
- split duties.

One player can manage medical/rescue coordination while the other handles evidence or external threat. Neither should become a spectator.

## EVT_400: Trusted rescue validation

A safe rescue requires one of:

- Mina trust + preserved Rook evidence;
- public exposure reducing Rook's control;
- independent paramedic/hospital contact;
- physical diversion plus direct hospital delivery.

Calling generic police without safeguards routes toward `END_PROTECTIVE_CUSTODY`.

## EVT_420: Evidence transfer

Complete transfer requires:

- primary archive accessible;
- complete code;
- Nadia or equivalent trusted endpoint;
- sufficient remaining time.

Partial transfer remains possible without all components and should have meaningful consequences.

## EVT_440: Final accusation or public statement

The player may name a target, but result depends on evidence support, not selection alone.

- correct and supported: exposure event;
- correct but under-supported: contested partial ending;
- wrong but evidence-linked: specific rebuttal scene;
- arbitrary accusation: credibility collapse without pretending the case itself vanishes.

## EVT_900+: Ending resolution

Ending variables are evaluated after rescue, transfer, confrontation, and accusation. Multiple achievements can succeed or fail independently.
