# DO NOT READ: NPC Knowledge and Disclosure Matrix

## 1. Knowledge rule

An NPC may state a fact only if it is present in their knowledge state. Every non-obvious fact requires one of:

- direct observation;
- prior participation;
- received communication;
- document access;
- justified inference.

Rumours and beliefs must be labelled internally as beliefs, not truth.

## 2. Sable Ortiz (night security desk)

### Initial knowledge at 19:00

Knows:

- Elena entered test bay at 18:40 under valid-looking badge;
- alarm cascade at 18:53;
- official story is automation fault;
- Vince's contractor team requested camera blind spots last week;
- Dana visited desk twice Saturday asking about badge audit timing.

Does not know:

- badge was cloned;
- Dana triggered manual purge;
- finance fraud scope;
- Tom's fob was duplicated in auth log.

### Disclosure stages

**Stage 0, guarded:** confirms timeline; withholds contractor friction notes.  
**Stage 1, trust +1 or procedural proof:** shares camera blind-spot request and Dana's desk visits (`FACT_DANA_DESK_VISITS`).  
**Stage 2, trust +2 or badge mismatch shown:** exports unaltered badge-camera subset and suppressed audit flag (`FACT_BADGE_AUDIT_SUPPRESSED`).

No ordinary single persuasion roll produces Stage 2.

## 3. Kevin Marsh (SCADA analyst)

### Initial knowledge

- sensor readings showed nominal until 18:51 then stepped anomaly;
- manual purge override at 18:52;
- historian retains full export;
- Marcus ordered ops silence pending corporate comms;
- Priya argued with Elena about architecture sign-off Friday.

Does not know:

- who held override token;
- Dana's financial motive;
- Vince installed spoof hardware personally.

### Disclosure stages

**Stage 0, neutral:** provides official automation timeline.  
**Stage 1, trust +1 or `CLUE_TEST_BAY_CO2_ANOMALY`:** admits purge was manual, not algorithmic (`FACT_MANUAL_PURGE`).  
**Stage 2, trust +2 or fraud thread shown:** exports complete historian including suppressed pre-incident sensor flatline (`FACT_SENSOR_FLATLINE`).

`CHK_123_TECHNOLOGY` success accelerates Stage 1 metadata recovery but does not bypass trust for Stage 2.

## 4. Marcus Hale (operations lead)

### Initial knowledge

- Elena was testing Priya's revised safety interlock;
- Marcus received corporate hold on external statements;
- Tom signed work order for bay access;
- Vince's team serviced camera network Tuesday.

### Beliefs

- Priya's design change may have caused real fault;
- Dana is only worried about liability exposure.

### Disclosure stages

- hostile: repeats corporate accident framing;
- shown sensor spoof or manual purge: admits hold order came from finance liaison (`FACT_CORP_HOLD_FINANCE`);
- shown fraud + credential proof: states Dana pressured him to lock SCADA exports before 21:00.

Marcus has `T_MARCUS` initial `−1`. Full cooperation requires two independent pressures, not one persuasion success.

## 5. Priya Nair (rival architect)

### Initial knowledge

- safety interlock change was approved through Dana's expedited channel;
- Elena emailed concerns about vendor spend tied to test hardware;
- Priya was not on-site at death;
- Vince requested after-hours lab camera disable for "calibration."

### Beliefs

- Elena may have been set up to discredit her architecture;
- Marcus protected ops metrics over safety review.

### Disclosure stages

- default: professional rivalry visible; denies sabotage;
- shown forged work order or finance shell: shares Elena's email thread (`FACT_ELENA_VENDOR_WARNING`);
- shown credential abuse: identifies Dana as only approver with override authority path.

Priya never confesses to murder; she provides documentary corroboration only.

## 6. Vince Calder (security contractor)

### Initial knowledge

- installed camera configuration per Dana's written request;
- knew badge audit was scheduled Monday;
- received bonus payment through shell vendor;
- did not operate purge console.

### Cooperation gate

Vince provides critical testimony only after at least one hard lever:

- shell vendor proof linking his payment;
- badge audit suppression record;
- proof Dana used his camera gaps.

Before that, he cites contract confidentiality and NDA.

## 7. Tom Reyes (maintenance)

### Initial knowledge

- did not personally enter bay Saturday evening;
- fob still on his belt;
- work order on clipboard looks like his signature;
- Dana asked him to "stand by" on CO₂ panel weeks ago.

### Beliefs

- automation killed Elena;
- he might lose job if fob mismatch surfaces.

### Disclosure stages

- default: defensive; confirms schedule;
- shown auth log mismatch: admits Dana borrowed panel walkthrough (`FACT_DANA_PANEL_WALKTHROUGH`);
- shown clone device or forged order: states Dana had shed access Friday night.

Tom cannot name Dana as murderer without credential and timeline proof presented together.

## 8. Dana Cole (CFO liaison / culprit)

### Initial knowledge at 19:00

- full embezzlement architecture;
- staged accident plan;
- badge clone and sensor spoof deployment;
- Elena was close to external audit;
- players are external investigators, not yet dangerous.

### Updates

- learns of SCADA export attempts through Marcus;
- learns badge audit restoration if Sable cooperates;
- learns players hold tablet memo or ledger copy.

### Disclosure behavior

Dana never confesses under a routine check. She may:

- offer accident settlement framing;
- implicate Vince or Tom as operational cutouts;
- admit "procedural shortcuts" while denying intent;
- flee or surrender only when `CON_CULPRIT_DANA` threshold met and exit blocked.

## 9. FACT_ identifier registry

This document owns the `FACT_` namespace.

| Key | Summary | Status |
|---|---|---|
| `FACT_MANUAL_PURGE` | CO₂ purge was manually overridden, not autonomous | `ACTIVE` |
| `FACT_SENSOR_FLATLINE` | pre-incident sensor flatline indicates spoof | `ACTIVE` |
| `FACT_DANA_DESK_VISITS` | Dana queried badge audit timing | `ACTIVE` |
| `FACT_BADGE_AUDIT_SUPPRESSED` | audit flag was suppressed | `ACTIVE` |
| `FACT_CORP_HOLD_FINANCE` | export hold originated from finance liaison | `ACTIVE` |
| `FACT_ELENA_VENDOR_WARNING` | Elena flagged vendor spend to Priya | `ACTIVE` |
| `FACT_DANA_PANEL_WALKTHROUGH` | Dana inspected CO₂ panel with Tom | `ACTIVE` |

## 10. Information-ingestion records

The Adventure Logic must encode updates in this form:

```text
KNOWLEDGE_UPDATE
actor: NPC_KEVIN
fact: FACT_MANUAL_PURGE
source: ITEM_PURGE_LOG
start_time: 19:15
condition: SCADA access OR trust T_KEVIN >= 1
```

No dialogue node may introduce a fact without a matching initial state or update record.
