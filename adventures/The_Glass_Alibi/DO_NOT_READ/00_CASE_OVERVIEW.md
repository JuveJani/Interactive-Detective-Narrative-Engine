# DO NOT READ: Case Overview

## Case identity

**Case title:** The Glass Alibi  
**Primary location:** Helix Meridian Campus, Meridian Dynamics (smart manufacturing and automation R&D)  
**Playable investigation window:** Saturday 19:00 to Sunday 00:30  
**Narrative deadline:** the campus incident report locks at 00:30 and corporate counsel briefs county investigators at 01:00  
**Apparent crime:** industrial accident during after-hours firmware validation in Automated Test Bay 3  
**Actual situation:** deliberate homicide staged as a CO₂ purge failure during solo calibration  
**Central question:** Can the investigators prove that Dr. Elena Park was murdered, identify who had motive and access to stage the scene, and stop the official accident narrative before evidence is sealed?

## The truth in one page

Dr. **Elena Park**, Chief Automation Architect at Meridian Dynamics, discovered a phantom-vendor embezzlement scheme in campus procurement logs. **Dana Cole**, the CFO liaison embedded at Helix Meridian, had been routing purchase orders through shell suppliers and skimming margin through inflated automation spares and consulting fees. Elena traced duplicate vendor identifiers and mismatched delivery receipts back to Dana's approval chain.

Elena planned to present her findings at Monday's executive audit. On Saturday evening she remained alone in **Automated Test Bay 3** to complete firmware validation on a safety-critical purge controller—the same subsystem whose logs Dana would need to falsify.

At approximately **21:14**, Dana executed a prepared plan:

1. Clone Elena's active badge credential from a prior shoulder-surfing capture and a lifted RFID trace.
2. Spoof occupancy and motion sensors in Test Bay 3 so the building automation system believed Elena was alone and stationary at her bench.
3. Enter the bay through the maintenance corridor using Dana's legitimate finance-liaison escort privileges.
4. Manually trigger the CO₂ fire-suppression purge while Elena was at the calibration console with her hearing protection engaged.
5. Exit before atmospheric alarms fully propagated.
6. Inject a staged **PLC fault** record into the validation log to explain the purge as an automated safety response.

Elena died from oxygen displacement and chemical exposure. The scene was consistent with a tragic but plausible after-hours industrial accident—except for four independent problems Dana could not fully erase:

- **Sensor spoofing** left micro-gaps in the occupancy timeline.
- **Manual override timestamps** in the purge controller do not align with the staged PLC fault.
- **Elena's badge** was used at a side reader after her estimated time of death.
- A **camera gap** on the loading-dock approach coincides with Dana's movement, while a night analyst's break-room witness places Dana away from her stated location.

No one initially knows the complete situation:

- **Marcus Hale**, Operations Director, believes the purge was a catastrophic failure he may be blamed for because of an earlier safety-override scandal.
- **Dr. Priya Nair**, rival architect, resented Elena's promotion but did not know about the fraud.
- **Vince Calder**, security contractor, knows the camera system has blind spots he has been paid not to report.
- **Tom Reyes**, night maintenance technician, was in the maint tunnel during the incident and is mistaken for a suspect because he reset a jammed dock door.
- **Dana Cole** presents as the cooperative executive liaison while steering investigators toward accident closure.

The players can expose Dana and the fraud, accuse the wrong person, accept the accident verdict, expose fraud without proving murder, or fail to stop Dana from leaving campus before external investigators arrive.

## Principal antagonism

There is no supernatural force and no single obvious theatrical killer.

- **Dana Cole** is the murderer and architect of the financial scheme. She is calm, prepared, and uses institutional authority to frame the incident.
- **Marcus Hale** is not the killer but carries real guilt over a prior safety-override cover-up that makes him obstructive.
- **Dr. Priya Nair** had professional motive and opportunity to resent Elena but lacks knowledge of the fraud until late.
- **Vince Calder** enabled blind spots and delayed alarm routing for cash; he did not trigger the purge.
- **Tom Reyes** is a red herring with legitimate access and suspicious timing.

The case's institutional antagonist is **Meridian Dynamics' desire to close the incident as an accident** before Monday's audit and a pending defense-contract review.

## Fair solution

A strong solution requires the players to combine at least three independent chains:

### Chain A: the death was not an accident

- occupancy sensor spoof artifacts in the bay telemetry;
- manual purge override timestamps inconsistent with automated fault logic;
- atmospheric alarm delay inconsistent with a genuine PLC cascade;
- Elena's body position inconsistent with evacuation behavior.

### Chain B: phantom-vendor financial fraud connects to the murder

- duplicate supplier identifiers in procurement exports;
- shell-vendor registration addresses matching Dana's prior consulting LLC;
- Elena’s annotated audit workbook referencing vendor **Glassline Industrial Supply**;
- approval signatures routed through Dana's liaison account after hours.

### Chain C: credential abuse after death

- badge reader event at the maint tunnel door after 21:20 while Elena was already incapacitated;
- cloned credential signature mismatch on the security desk's secondary validator;
- Dana's own badge logged at `LOC_FINANCE_HUB` while claiming to be on a vendor call in the security office.

### Chain D: timeline and witness contradiction

- night analyst **Sable Ortiz** saw Dana near the loading dock, not in the security office;
- camera gap on dock camera 4 between 21:08 and 21:19;
- Tom Reyes's maintenance ticket proves he was resetting the dock lift, not in Test Bay 3;
- Priya's access log shows she was in `LOC_SCADA_ROOM` during the purge window.

No single clue reveals the entire solution.

## Principal questions

1. Did Elena die because of an automated safety failure, or because someone manually triggered a lethal environment?
2. Who benefited from Elena's death before Monday's audit?
3. Whose credentials and sensor data were manipulated during the purge window?
4. Which suspect's alibi breaks when witness time, camera coverage, and badge logs are compared?
5. Will the investigators stop the incident report from sealing the truth before external review?

## Intended emotional core

The case is not primarily about a puzzle-box locked room. It is about whether truth can survive inside a facility designed to measure everything except the people who control the logs.

The final moral tension is:

- prove murder and fraud before counsel seals the record;
- expose fraud without enough evidence to charge Dana;
- protect a frightened witness who works inside Meridian;
- or accuse the loudest suspect and let the real killer walk out with a clean incident summary.

## Player character context (world only)

The investigators are external specialists contracted after the purge alarm. Neither is bound to a fixed player slot in this document.

- **Investigator A** is emphasized in automation, electronics, firmware, and industrial troubleshooting. The campus expects them to read controllers, logs, and sensor chains credibly.
- **Investigator B** is emphasized in athletic fieldwork, physical access, observation, and spatial reconstruction. Environmental detail may include meticulous noticing of alignment, labeling, and order—consistent with an OCD trait expressed as scene texture, not as a mechanical game bonus.
- Both investigators are **level 1** and enter without prior relationships to the suspects.
