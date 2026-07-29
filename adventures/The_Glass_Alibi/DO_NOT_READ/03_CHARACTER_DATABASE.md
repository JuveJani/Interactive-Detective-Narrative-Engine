# DO NOT READ: Character Database

## Character-state model

Each character record separates:

- objective identity;
- public presentation;
- private motive;
- knowledge;
- beliefs;
- lies;
- pressure response;
- branch variables.

Only information explicitly earned by players may appear in player-facing text.

---

## NPC_ELENA: Dr. Elena Park

**Role:** victim  
**Age:** 41  
**Occupation:** Chief Automation Architect, Meridian Dynamics  
**Time of death:** approximately 21:15–21:18, Saturday  
**Location of death:** Automated Test Bay 3 (LOC_TEST_BAY)  
**Public reputation:** brilliant, exacting, fair  
**Actual personality:** system-trusting, morally serious, slow to suspect colleagues

### Motivation (before death)

Complete Monday's audit packet exposing procurement irregularities without triggering premature retaliation.

### Private history

Elena built her career on safety-critical firmware. She believed Meridian's public safety culture mostly matched its marketing. The Marcus Hale report edit shook that belief but did not convince her murder was plausible inside her own campus.

### Knowledge at time of death

Elena knew:

- Glassline vendor entries were fraudulent;
- Dana Cole's liaison approvals appeared in after-hours exception logs;
- Marcus Hale edited a safety incident report;
- Priya resented her but remained professionally competent;
- Vince Calder's camera remediation reports were overdue.

She did not know:

- Dana had cloned her badge;
- Dana planned to kill her;
- Vince accepted cash for blind-spot delays;
- Tom Reyes would be near the dock during validation.

### Physical evidence on body

- hearing protection still seated;
- no defensive wounds;
- chemical exposure and oxygen displacement consistent with CO₂ purge;
- workstation login still active;
- no evidence of sexual assault or unrelated trauma.

### Branch states

- body_in_bay;
- body_released_to_coroner;
- audit_workbook_recovered;
- audit_workbook_destroyed.

---

## NPC_DANA: Dana Cole

**Role:** CFO liaison / culprit  
**Age:** 44  
**Occupation:** embedded finance and procurement liaison, Helix Meridian  
**Public presentation:** calm, helpful, institutionally fluent  
**Private motive:** prevent exposure of Glassline embezzlement and retain freedom

### Knowledge

Dana knows:

- she murdered Elena;
- she cloned Elena's badge and spoofed occupancy sensors;
- she manually triggered the purge and staged the PLC fault;
- Glassline is her laundering vehicle;
- Vince's blind spots and fob checkout sloppiness enabled the plan;
- Sable Ortiz delayed one mismatch alert at Dana's request.

She does not know:

- whether Elena told anyone else before death;
- exactly how much of the audit workbook survived;
- whether investigators can prove manual override rather than infer it.

### Incorrect beliefs

- She believes the vendor-call alibi is sufficient if investigators stay tired and rushed.
- She believes sanitization scripts can erase Glassline if she reaches Sunday morning off-campus.

### Lies

At opening:

- "Elena insisted on working alone tonight to meet Monday's audit."
- "I was on a vendor reconciliation call from the security office when the alarm triggered."
- "This looks like a tragic validation fault, not anything personnel-related."

Reason: delay murder proof and preserve fraud cleanup time.

### Pressure response

- If accused without sensor, credential, and timeline evidence, Dana expresses hurt professionalism and invokes counsel.
- If fraud is exposed but murder unproven, Dana pivots to "financial irregularities unrelated to the accident."
- If cornered with manual override proof and badge mismatch, Dana requests counsel and stops speaking.
- If allowed to leave before 00:30, Dana initiates record sanitization remotely.

### Branch states

- cooperative_liaison;
- fraud_exposed;
- murder_proven;
- detained;
- escaped_campus.

---

## NPC_MARCUS: Marcus Hale

**Role:** Operations Director / suspect  
**Age:** 47  
**Occupation:** campus operations director  
**Public presentation:** commanding, defensive about safety record  
**Private motive:** avoid blame for both the purge and his earlier override scandal

### Knowledge

Marcus knows:

- he edited a conveyor safety incident report six months ago;
- Elena discovered the edit and planned to mention it in a culture memo;
- Elena requested after-hours validation alone;
- initial HelixSense export shows PLC fault;
- purge propagation timing looked wrong to him, but he lacks proof.

He does not know:

- Dana murdered Elena;
- Glassline is fraudulent;
- badge cloning occurred;
- Vince took cash for blind spots.

### Incorrect beliefs

- He believes Meridian leadership will sacrifice him to protect the Helix contract.
- He believes Priya might have sabotaged Elena's project.

### Lies

- "I had no concerns about tonight's validation." (He did, but approved anyway.)
- "Elena and I were fine." (They were in conflict over his memo.)
- "I was on the Operations Floor when the alarm sounded." (He was in his office reviewing exports.)

Reason: protect career and avoid connecting himself to earlier safety misconduct.

### Pressure response

- If confronted with the edited report, Marcus admits the cover-up but denies murder.
- If treated as primary suspect, he becomes rigid and lawyer-silent.
- If shown Tom Reyes's dock alibi and Priya's server log, Marcus redirects investigators toward system logs rather than personnel.

### Branch states

- obstructive;
- partial_confession_on_override;
- cleared_of_murder;
- wrongly_accused.

---

## NPC_PRIYA: Dr. Priya Nair

**Role:** rival architect / suspect  
**Age:** 39  
**Occupation:** senior automation architect  
**Public presentation:** precise, proud, emotionally controlled  
**Private motive:** professional survival and legacy after losing promotion to Elena

### Knowledge

Priya knows:

- she resented Elena's promotion;
- Elena kept a private audit folder on the lab machine;
- she left campus before 18:00 and returned after the death;
- Elena's project used purge-controller firmware she also maintained.

She does not know until later:

- Glassline fraud details;
- Dana killed Elena;
- Marcus edited a safety report.

After reviewing Elena's folder naming pattern, Priya can infer Elena was investigating procurement, not firmware.

### Incorrect beliefs

- She initially believes Elena may have discovered dangerous negligence in Marcus's org and been silenced by operations.
- She believes investigators will assume rivalry equals guilt.

### Lies

- "Elena and I had no conflicts." (They argued regularly about architecture priorities.)
- "I did not access her files." (She attempted after death to preserve project continuity.)

Reason: avoid being blamed for professional jealousy.

### Pressure response

- If accused with only motive evidence, Priya becomes cold and demands her lawyer.
- If shown server access logs clearing her during the purge window, she becomes cooperative.
- If trusted, she provides the encrypted folder hint and Elena's note about "glass vendors."

### Branch states

- hostile;
- cooperative;
- cleared;
- wrongly_accused.

---

## NPC_VINCE: Vince Calder

**Role:** security contractor / suspect  
**Age:** 52  
**Occupation:** owner, Calder Secure Systems  
**Public presentation:** affable, technical, slightly evasive about paperwork  
**Private motive:** keep Meridian contract and hide ethical compromises

### Knowledge

Vince knows:

- three dock cameras have sync-gap blind spots he never fully fixed;
- he accepted cash for "expedited service" without documentation;
- maintenance override fob checkout logs are sloppy;
- Dana pressed him for urgent blind-spot reports twice in the last month.

He does not know:

- Dana murdered Elena;
- Dana used the retained fob and spoof hardware;
- Elena investigated fraud.

### Incorrect beliefs

- He believes Dana wanted blind spots for discreet executive visits, not murder.
- He believes the purge was a genuine industrial accident.

### Lies

- "All cameras were fully operational tonight." (Known sync faults existed.)
- "Equipment checkout logs are complete." (They are not.)
- "I was not on campus." (True for physical presence, false implication of full remote oversight.)

Reason: protect contract and avoid admitting bribery-adjacent behavior.

### Pressure response

- If shown checkout gaps and cash transfer references, Vince admits negligence and blind spots.
- If accused of murder without timeline support, he demands corporate counsel and provides remote login proof.
- Under pressure, he identifies Dana's unusual interest in maint tunnel camera coverage.

### Branch states

- evasive;
- partial_confession;
- cleared;
- contract_terminated.

---

## NPC_TOM: Tom Reyes

**Role:** night maintenance technician / red herring  
**Age:** 28  
**Occupation:** on-call maintenance, Helix Meridian  
**Public presentation:** tired, practical, nervous under authority  
**Private motive:** keep job and avoid being blamed for a death in an area he services

### Knowledge

Tom knows:

- he reset a jammed dock lift at 21:11;
- maint tunnel doors were functioning oddly earlier in the week;
- Dana asked him last month which tunnel routes bypassed camera coverage "for a VIP walkthrough";
- he was not in Test Bay 3 during the purge.

He does not know:

- Dana murdered Elena;
- badge cloning occurred;
- Glassline exists.

### Incorrect beliefs

- He believes he might be fired because his maint access looks suspicious.
- He believes the purge was accidental.

### Lies

- "I didn't see anything unusual." (He saw Dana near the tunnel junction Tuesday but thought it was authorized.)
- "Dana never asked me about tunnels." (She did, casually.)

Reason: fear of implicating an executive liaison without proof.

### Pressure response

- If accused aggressively, Tom clams up and asks for union rep.
- If investigators compare his radio log and ticket timestamps, he tells the truth about the dock lift and Dana's odd question.

### Branch states

- frightened;
- exculpated;
- wrongly_accused.

---

## NPC_SABLE: Sable Ortiz

**Role:** night security desk analyst / supporting witness  
**Age:** 26  
**Occupation:** HelixSense monitoring and security desk analyst  
**Public presentation:** conscientious, overworked, deferential to executives  
**Private motive:** keep job and avoid being scapegoated for delayed alerts

### Knowledge

Sable knows:

- default dashboard hid the secondary badge mismatch flag;
- Dana asked them to delay pushing that alert "until reconciliation finished";
- Dana was not visible at the security office phone bank during the purge despite claiming a vendor call;
- Sable saw Dana near the loading dock corridor at approximately 21:17 while fetching coffee;
- lockdown was initiated at 21:22;
- maint corridor escort privileges exist for finance liaison staff.

Sable does not know:

- Dana entered Test Bay 3;
- fraud motive;
- manual override details;
- murder details.

### Incorrect beliefs

- Sable initially believes the delay request was standard executive nuisance, not obstruction.

### Lies

- "All alerts were handled normally." (One was delayed at Dana's request.)
- "Dana was on her call the whole time." (False.)

Reason: fear of losing clearance and being blamed for Elena's death.

### Pressure response

- If pressured by Dana's authority alone, Sable repeats the official story.
- If investigators offer procedural protection or show badge mismatch evidence, Sable admits the delay and dock sighting.
- Provides access logs, escort policy, and lockdown timeline when formally requested.
- Refuses illegal entry without counsel approval.

### Branch states

- loyal_to_story;
- partial_witness;
- full_witness;
- procedural;
- cooperative;
- restrictive.

---

## NPC_KEVIN: Kevin Marsh

**Role:** SCADA analyst / supporting witness  
**Age:** 29  
**Occupation:** night SCADA and historian analyst, Helix Meridian  
**Public presentation:** technical, cautious, loyal to procedure  
**Private motive:** preserve accurate logs without becoming corporate collateral

### Knowledge

Kevin knows:

- historian exports show manual purge override before staged PLC fault frame;
- occupancy telemetry has motion sub-sensor micro-gaps during purge window;
- Marcus may order export holds if corporate is unaware;
- Elena had an active validation session with hearing protection engaged;
- procurement duplicate vendor metadata exists in archived exports.

Kevin does not know:

- Dana murdered Elena;
- badge cloning occurred;
- Glassline LLC ownership until finance clues surface.

### Incorrect beliefs

- Kevin initially trusts the default PLC fault narrative until override timestamps are compared.

### Lies

None significant. Kevin may **withhold** deep exports until trust threshold or formal challenge is met.

### Pressure response

- If Marcus hold is active, Kevin defers to counsel unless investigators file challenge or earn trust.
- If shown badge mismatch or fraud thread, Kevin accelerates covert USB export at `EVT_220`.
- Provides VLAN access hints for Elena's encrypted folder if treated credibly.

### Branch states

- procedural;
- cooperative;
- witness_preserved;
- export_blocked.

---

## NPC_COUNSEL: Corporate counsel liaison (off-screen)

**Role:** institutional pressure / phone contact  
**Name:** Margaret Cho (voice only in alpha design)  
**Function:** reminds investigators of the 00:30 report lock and pushes accident classification unless evidence forces escalation.

Not a suspect. Not present physically during play.

---

## Cross-character truth table

| Fact | Dana | Marcus | Priya | Vince | Tom | Sable | Kevin |
|---|---|---|---|---|---|---|---|
| Murdered Elena | yes | no | no | no | no | no | no |
| Glassline fraud | yes | no | partial late | no | no | no | partial |
| At purge window in bay | yes | no | no | no | no | no | no |
| Credible alibi during purge | no | weak | strong | strong | strong | n/a | strong |
| Knows badge cloned | yes | no | no | no | no | partial | no |
| Knows camera gap | yes | no | no | yes | partial | partial | no |
