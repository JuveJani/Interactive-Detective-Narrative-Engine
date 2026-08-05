# NPC Approval Report — PLAYER TEST OWNER (Spoiler-Free)

**Adventure:** The Cold Storage Alarm  
**Stage gate:** `npcs`  
**Status:** `AWAITING_APPROVAL`

---

## NPC count and role coverage

| Metric | Status |
|--------|--------|
| On-scene NPCs | 5 — security, contractor, logistics, supervisor, cleaning lead |
| Records-only role | 1 — badge archive administrator |
| Role coverage | Operational, security, vendor, management, facilities, records |

All approved brief scale targets are met.

---

## Relationship complexity

- Supervisor ↔ staff reporting edges (logistics, security)
- Vendor ↔ facility relationship (contractor)
- Colleague edge (security ↔ cleaning)
- Trust modifiers include **positive and negative** deltas (not globally positive)
- Relationship reactions on accusation and testimony challenge

No melodrama edges; relationships are workplace-grounded.

---

## Knowledge-boundary quality

- 18 information entries each declare provenance category (observation, action, assumption, told, inferred, policy)
- Records-only NPC holds policy knowledge only; no on-site conversation graph
- High-deception NPC has separate evasive vs pressure-gated admission topics
- Mistaken-honest NPC has explicit incorrect-assumption entry
- Player knowledge placeholders documented for cross-layer linking (no investigation core duplication yet)

---

## Testimony diversity

| Category | Present |
|----------|---------|
| Truthful incomplete | Yes (security rounds) |
| Believable mistakes | Yes (latch vs reader gap) |
| Evasive denial | Yes (logistics coordinator) |
| Reluctant / embarrassed truth | Yes (contractor badge/session) |
| Partial observation | Yes (cleaning lead silhouette) |
| Institutional pressure framing | Yes (supervisor urgency) |
| Records-only policy | Yes (archive sync) |

No exposition-dump nodes; repeat policies set where needed.

---

## Trust / pressure system coverage

- Per-NPC initial trust, suspicion, pressure values
- Trust thresholds on sensitive topics
- Player-action gates for high-pressure admissions
- State effects on select nodes (trust/suspicion deltas)
- Accusation modifiers with relationship-conditioned sign

Social success changes disclosure and cooperation only — no truth mutation.

---

## Contradiction support

- Linked topic pairs for door testimony vs badge records
- Follow-up node requiring player documentary knowledge before mistake admission
- Multiple independent NPC perspectives on overlapping time window

---

## Time-dependent availability

- Segments aligned to approved investigation window (01:00–05:00)
- Security desk gap during mandatory break
- Dock restriction enforcement mid-investigation
- Contractor remote-then-onsite transition
- Cleaning lead departure reduces interview access
- Archive sync opens records route

Availability changes investigation opportunities, not only flavor.

---

## Remaining structural risks

1. Investigation Core package not yet generated — knowledge/testimony IDs are placeholders pending linkage.  
2. Player knowledge placeholders require environment/object/records layers to grant documentary knowledge.  
3. `player_action` pressure IDs require capability-check mapping in a later stage.  
4. NPC-IT records delivery mechanism depends on investigation-flow routing (not yet authored).

---

## Exact approval choices

| Choice | Options |
|--------|---------|
| **Approve NPC layer** | Proceed to environment generation |
| **Request revision** | Specify NPC, topic, or availability changes |
| **Reject** | Halt pipeline; do not generate environment |

**Current gate:** `npcs` — **AWAITING_APPROVAL**

---

## Validation status

- `python3 -m idne.npc_investigation_validate` — **PASS**
- World-first validation (unchanged truth package) — **PASS**

No environment, object, investigation-flow, PLAYER, or `.idne` content generated.
