# BENCHMARK_CHECKLIST.md

**Adventure:** Harborview Arcade (`CASE_BENCHMARK_v0.4`)  
**Purpose:** Trace where each IDNE v0.4 philosophy principle, P0 engine requirement, and Adventure Brief mandate is exercised in play.

---

## 1. Design Philosophy (Category A)

| Principle | Where exercised |
|---|---|
| **A1 Fair mystery — reconstruct, do not receive** | C-05/C-11 (motive docs) + C-06/C-12 (opportunity) + C-01/C-10 (method) must combine via I-01, I-02, I-03 before E-901; no single gift clue |
| **A2 Equal suspect weight** | J-121 neutral one-line intros for Mira, James, Diane, Tomás; P-212 Tomás not uniquely "calm villain" |
| **A3 Suspicious innocents** | P-111a Mira nervous (C-07); P-211a James evasive (C-08); P-112 Diane defensive — all innocent |
| **A4 Believable behaviour** | James hides affair not murder; Diane hides inspection lapse; Tomás lies with cover story tied to job access |
| **A5 Player-directed investigation** | Hubs J-120, J-300, J-500 — diegetic actions, ≥4 options each; no page-code choices |
| **A6 DM simulator, not branching novel** | Hub action space + time costs + ask-the-world follow-ups on case file; logic in `DO_NOT_READ/LOGIC/` |
| **A7 Scarcity creates decisions** | 19:00–23:00 clock; cannot do all interviews + full basement + boot cast without tradeoffs; T1–T3 gates |
| **A8 Discovery and connection** | Clues Observe/Earn dominant; 0 Auto major; three infer worksheets |
| **A9 Cooperative mystery** | J-210, J-410, J-510 joint synthesis; 45% joint clue/infer units per `LOGIC/13` |
| **A10 Neutrality — no steering** | No "recommended" text; P-212 Tomás does not name next location; Park neutral |
| **A11 Fair play** | Two proof routes in `05_CLUE_ARCHITECTURE.md`; fail paths degrade not delete (`CHK_INVOICE` → C-14) |
| **A12 Knowledge ≠ truth** | NPCs believe accident; players infer homicide |
| **A13 World continues** | Thresholds fire on clock regardless of player location |
| **A14 Failure changes path** | Check fails → CERTAINTY_DEGRADED, +time, alternate clues |
| **A15 Private info for perspective** | Splits P-*/R-*; regroup requires spoken sharing |
| **A16 No coaching** | Hubs list actions only; endings cite player sheet tags |
| **A17 Stakes without twist density** | SETUP stakes sentences; E-904 institutional cost; no mid-act shock reveal |

---

## 2. IDNE Engine v0.4 — Immutable principles (U1–U12)

| ID | Where exercised |
|---|---|
| U1 Fixed truth | `DO_NOT_READ/00_CASE_OVERVIEW.md` — Tomás guilty before play |
| U2 Knowledge ≠ truth | Witness beliefs in `03_CHARACTER_DATABASE.md`; player inference required |
| U3 Fair play | `05_CLUE_ARCHITECTURE.md` redundancy; E-903 if proof incomplete |
| U4 Narrator honesty | J-110 physical facts only; no lying narrator |
| U5 Off-screen world | Thresholds, Tomás 19:42 push in timeline |
| U6 Traceable causes | Every clue tied to scene action in PLAYER booklets |
| U7 Failure paths | `17_CHECK_REGISTER.md` fail branches |
| U8 Suspicious innocents | Mira, James, Diane arcs |
| U9 Equal weight | J-121 + equal suspect design rules |
| U10 No coaching | §9.2 audit across PLAYER files |
| U11 DM simulation | Hub + logic layer architecture |
| U12 Layer ownership | DO_NOT_READ vs PLAYER separation |

---

## 3. Engine v0.4 — P0 / experience gates (§13.2)

| Gate | Requirement | Where exercised |
|---|---|---|
| Wall-clock estimate | §5.4 formula | `LOGIC/10` segment table ~120 min; `COMPILATION_REPORT.md` |
| Shared investigation | ≥40% Joint clue units | `LOGIC/13` — 45% (5/11) |
| Split balance | ≤5 min delta | Split 1: 10/10 min; Split 2: 12/12 min; early-finish P-113, R-213 |
| Decision isolation | No consequence on decision units | J-120, J-300, J-500, P-111, P-211, R-211, R-212 — actions only; outcomes in lettered destinations |
| No steering | Ban recommended language | Grep-clean; NPCs state facts not destinations |
| Visible mechanics | Sheet-checkable conditionals | `CASE_FILE.md` tags; WITNESS_COOPERATIVE/SHUT_DOWN; thresholds T1–T3 |
| Time teeth | Thresholds gate options | J-300 T1 bakery, T2 Holt lobby, T3 basement key |
| Discovery / Infer | ≥1 Infer on fair path | I-01, I-02, I-03 worksheets; 0 Auto major clues |
| Ending clarity | Sheet-checkable + causal chain | J-600 dispatch; E-901 narrates C-01/C-05/C-06 chain |
| Suspect weight | Equal intro review | `03_CHARACTER_DATABASE.md` word-budget rule; J-121 |
| Human playtest | Recorded session | *Pending — package ready for playtest* |

---

## 4. Adventure Brief — structural requirements

| Brief § | Requirement | Implementation |
|---|---|---|
| 2.1 | People + Records roles | `SETUP.md`, booklets P-* / R-* |
| 2.2 | Participation parity | Both required for METHOD/MOTIVE/OPPORTUNITY on fair path |
| 3.1 | Mixed-use building | Harborview Arcade — bakery, units, manager, basement |
| 3.2 | 5 primary locations | LOBBY, STAIRWELL, BAKERY, MANAGER, BASEMENT |
| 4.1 | Whodunit method+motive+opportunity | Proof tags on case file |
| 4.3 | 4 major suspects | Mira, James, Diane, Tomás |
| 4.3 | ≥2 nervous innocents | Mira, James (+ Diane defensive) |
| 5.1 | 3 hubs ≥4 actions | J-120 (5), J-300 (5), J-500 (4) |
| 5.1 | Revisit once per hub | J-110 revisit from J-300 |
| 5.1 | Ask-the-world ×2 | Case file follow-up table in JOINT |
| 5.2 | 14 clues | C-01–C-14 |
| 5.2 | Observe ≥4 | C-01, C-02, C-03, C-04 |
| 5.2 | Earn ≥6 | C-05–C-14 (10 Earn) |
| 5.2 | Infer ≥3 | I-01, I-02, I-03 |
| 5.2 | Auto major ≤3 | **0** major Auto |
| 5.3 | Infer beats 1–3 | J-210, J-410, J-510 |
| 5.4 | Checks 3–4 | CHK_INVOICE, JAMES_PRESS, BOOT_MATCH, MIRA_CALM |
| 6.1 | ≥45% Joint clue share | `LOGIC/13` audit |
| 6.1 | ≥2 joint reasoning | J-210, J-410 |
| 6.3 | 2 split windows | J-130, J-330 |
| 6.3 | ≤4 min balance | 10/10 and 12/12 estimates |
| 6.4 | ~120 min wall-clock | `LOGIC/10` estimate table |
| 7.2 | 3 thresholds T1–T3 | 20:00, 21:00, 22:00 in J-300 |
| 7.4 | Visible stakes | SETUP.md opening stakes |
| 8.1 | 5 endings | E-901–E-905 |
| 8.3 | Causal ending text | `ENDINGS.md` each cites clue chain |
| 11 | Anti-patterns avoided | No mastermind, no coincidence guilt, no NPC steering |
| 12 | Content budget | Matches summary table in brief §12 |

---

## 5. Refactoring Plan P0 items (C-01–C-07)

| ID | Where exercised |
|---|---|
| C-01 Philosophy normative | Adventure targets v0.4 gates; `README.md` engine version |
| C-02 Ready ≠ structural PASS | `BENCHMARK_CHECKLIST.md` experience matrix |
| C-03 Decision isolation | Hub and split decision/destination split throughout PLAYER |
| C-04 No steering | PLAYER prose audit |
| C-05 Wall-clock max formula | `LOGIC/10` + `COMPILATION_REPORT.md` |
| C-06 Visible mechanics | `CASE_FILE.md` all conditionals |
| C-07 Delivery Adapter | Logic in DO_NOT_READ; PLAYER compiled from graph |

---

## 6. Playtest comparison targets (vs Glass Alibi)

| Dimension | Benchmark exercise location |
|---|---|
| Wall-clock accuracy | 120 min design; not summed-role estimate |
| Shared investigation | Joint opening 20+ min; infer scenes; 45% joint clue share |
| Split balance | Matched split estimates + early-finish actions |
| Diegetic choices | All hubs |
| Earn/Observe clues | Stairwell, basement, interviews — not entry dumps |
| Inference | Three worksheets, not checkbox |
| Time teeth | T1 bakery, T2 Holt, T3 basement |
| Ending clarity | E-901 causal narration + sheet dispatch |
| Plain language | Short sentences in PLAYER scenes |
| Investment | SETUP stakes + E-904 cost |

---

## 7. Files to open for human playtest validation

| Reviewer question | Open |
|---|---|
| Is the solution fair? | `DO_NOT_READ/00_CASE_OVERVIEW.md` |
| Do gates pass on paper? | This checklist + `LOGIC/13`, `LOGIC/10` |
| Is play spoiler-safe? | `PLAYER/` only for players |
| Clock math | `LOGIC/10` wall-clock table |
| Ending logic | `LOGIC/14_ENDING_TRIGGER_MATRIX.md` |

---

*End of benchmark checklist.*
