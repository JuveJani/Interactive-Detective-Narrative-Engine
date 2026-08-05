# NPC Approval Report — AUTHOR-ONLY / SPOILER-CONTAINING

**Adventure:** The Cold Storage Alarm  
**Stage gate:** `npcs`  
**Status:** `AWAITING_APPROVAL`  
**Do not distribute to players.**

---

## NPC roster (6)

| ID | Name | Role | Deception profile |
|----|------|------|-----------------|
| NPC-LORI | Lori Okonkwo | Logistics coordinator | High evasion; hides relabeling and terminal use |
| NPC-MARCUS | Marcus Hale | Night security | Honest but mistaken on door security |
| NPC-DEV | Dev Santos | Refrigeration contractor | Honest; hides forgotten badge and unlocked session |
| NPC-ELENA | Elena Morales | On-call supervisor | Institutional pressure; protects staff initially |
| NPC-PAT | Pat Nguyen | Cleaning lead | Partial witness; silhouette only |
| NPC-IT | Jordan Reeves | Records-only | Archive sync policy; no on-site dialogue |

---

## Knowledge and testimony provenance

Each `information_known_model` entry declares `provenance_category`:

- **direct_action** — Lori relabeling, Dev maintenance/exit, Elena restriction
- **direct_observation** — Marcus latch/alarm, Pat dock activity
- **incorrect_assumption** — Marcus badge review gap
- **told** — Elena alarm notification
- **inferred** — Elena on Lori working late (no relabel knowledge)
- **policy** — IT sync schedule

Lori **cannot** testify to Dev's private actions without source. Pat **cannot** identify Lori. Dev **does not know** relabeling.

---

## Contradiction support

- **Marcus latch testimony** vs **badge entry record** (TOPIC-DOOR-ROUNDS ↔ TOPIC-BADGE-RECORDS)
- **Lori denial** of cold access vs **badge log** and **label residue**
- **Dev implied by badge** vs **exit scan timeline**

---

## Trust and relationship effects

- Accusing **Dev** increases **Lori** trust (+10) — scapegoat incentive
- Accusing **Lori** decreases **Elena** trust (−15) — supervisor protection
- Accusing **Dev** decreases **Elena** trust (−20) — vendor defense
- Dismissing urgency decreases **Elena** trust (−12)

---

## Availability tied to world-state timeline

| NPC | Investigation impact |
|-----|------------------------|
| Marcus | Available LOC-SECURITY until 04:30; unavailable during break |
| Elena | High pressure from arrival; enforces dock restriction after 03:15 |
| Dev | Phone-only briefly, then on-site at dock |
| Lori | Evasive at manager office throughout |
| Pat | Available until 03:00, then off-site |
| IT | Records-only after 02:30 archive sync |

---

## Conversation structure summary

- **18 topics** with mixed unlock types (world_time, trust, knowledge_held, player_action)
- **6 conversation graphs** (IT records-only via topic/policy; no dialogue graph)
- **6 testimony links** to conversation nodes
- Pressure-sensitive Lori nodes require player_action gates plus documentary/physical knowledge placeholders

---

## Assumptions requiring approval

1. Investigation Core knowledge IDs (`KNOW-*`) placeholders link in a later stage.  
2. Player knowledge placeholders (`KNOW-BADGE-ENTRY-RECORD`, etc.) supplied by environment/object/records layers.  
3. `player_action` pressure gates map to capability checks in a later stage.  
4. NPC-IT records-only delivery via archive topic, not live conversation.

**Do not proceed to environment stage until NPC gate approved.**
