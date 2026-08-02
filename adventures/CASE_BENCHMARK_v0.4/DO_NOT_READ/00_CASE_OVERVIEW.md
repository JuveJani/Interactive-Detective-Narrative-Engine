# Case Overview — Harborview Arcade

**Classification:** INTERNAL — DO NOT READ before play  
**Engine:** IDNE v0.4  
**Truth status:** Fixed objective truth (U1)

---

## Premise

Saturday evening at Harborview Arcade, a four-story mixed-use building. Elena Voss, part-time association bookkeeper and third-floor tenant, is found at the base of the rear service stairwell with fatal head trauma. First responders treat it as a possible fall. Players are a county pair of **building-safety investigators** called in because the association carries public grant funding.

## Objective truth

| Element | Fact |
|---|---|
| **Crime** | Intentional homicide by pushing from the basement landing onto the concrete stairwell pad |
| **Perpetrator** | Tomás Reyes (`NPC_TOMAS`), building handyman |
| **Motive** | Elena discovered duplicate vendor invoices and petty-cash siphoning in maintenance accounts; confronted Tomás in the basement storage room |
| **Method** | Struggle at landing; push; staged to look like a slip on wet concrete |
| **Time of death window** | 19:35–19:50 |
| **Initial ambiguity** | Wet mop, poor lighting, and no immediate witness support accident theory |

## Fair solution requirements

Correct accusation requires connecting:

1. **Opportunity** — Tomás signed tools out until 20:15 but claimed he left by 19:30 (`CLUE_C06`); basement access during death window.
2. **Method** — Scuff pattern and wet-concrete transfer inconsistent with solo slip (`CLUE_C01`, `CLUE_C10`); mop placed after struggle (`CLUE_C04`).
3. **Motive** — Invoice duplicates and Elena's draft complaint (`CLUE_C05`, `CLUE_C11`); not the rent dispute (`CLUE_C07` red herring).

## Major suspects

| Key | Role | Guilt | Suspicious behaviour |
|---|---|---|---|
| `NPC_MIRA` | Bakery tenant | Innocent | Nervous about rent arrears; loud 16:00 argument |
| `NPC_JAMES` | Fourth-floor tenant | Innocent | Evasive; visited building 17:00 hiding affair |
| `NPC_DIANE` | Building manager | Innocent | Defensive about records; hid minor code issues |
| `NPC_TOMAS` | Handyman | **Guilty** | Calm, helpful; no tone leak |

## Red herrings (credible)

- Rent dispute with Mira (motive misdirection)
- James's secret visit (opportunity misdirection)
- Diane's altered visitor log copy (records anxiety, not murder)

## Endings (truth layer)

| ID | Condition summary |
|---|---|
| `END_CORRECT` | Accuse Tomás with method+motive+opportunity proof set |
| `END_WRONG` | Accuse innocent with partial proof |
| `END_INCOMPLETE` | Accuse with insufficient categories |
| `END_TIMEOUT` | Clock ≥ 23:00 without resolution |
| `END_DECLINE` | Choose not to accuse at Hub 3 |

## Play structure

- 3 investigation hubs (diegetic menus, ≥4 actions each)
- 2 split windows (People / Records)
- 3 clock thresholds (T1 20:00, T2 21:00, T3 22:00)
- 15 active clues, 3 infer beats, 4 checks, 5 terminals
