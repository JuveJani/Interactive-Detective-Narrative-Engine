# DO NOT READ: World Bible

## 1. Authority

**World Bible version:** 1.0

This document defines objective reality for `The Glass Alibi`. Player narration, NPC testimony, clues, and endings may reveal only portions of these facts. No later document may contradict this file without an explicit version change.

### Version history

| Version | Change |
|---|---|
| 1.0 | Initial objective reality, Prototype Alpha 0.1. |

## 2. Setting

### Meridian Dynamics

Meridian Dynamics is a mid-size American automation and smart-manufacturing company headquartered outside a major metropolitan area. It designs robotic assembly cells, industrial vision systems, and factory orchestration software for defense-adjacent and commercial clients.

The company presents itself as a safety leader. Internally it is under pressure from a pending **Helix defense-integration contract** and a Monday-morning procurement audit requested by an outside director.

There are no supernatural elements, hidden occult histories, or non-natural explanations anywhere in this setting. Every event in the case is explicable through human action, industrial systems, and institutional behavior.

### Helix Meridian Campus

Helix Meridian is Meridian Dynamics' primary R&D and validation campus. It occupies a converted industrial park with three connected buildings:

- **North Wing:** executive offices, finance liaison suite, visitor security.
- **Central Wing:** operations floor, fabrication bays, loading dock.
- **South Wing:** server rooms, automated test bays, maintenance tunnels.

The campus runs a unified building automation stack branded **HelixSense**. It integrates badge access, occupancy sensors, camera management, environmental monitoring, and safety interlocks for CO₂-based fire suppression in high-value test areas.

Saturday night staffing is minimal: one security desk officer, one night operations analyst, one maintenance technician on call, and occasional after-hours engineering access for validation work.

### Relevant institutions

- **Meridian Dynamics corporate security**
- **Helix Meridian campus operations**
- **County industrial safety office**, external but not present during play
- **Glassline Industrial Supply**, a phantom vendor used in the fraud scheme
- **Calder Secure Systems**, Vince Calder's contractor firm

## 3. The purge and sensor system

Automated Test Bay 3 validates firmware for purge controllers used in sealed manufacturing environments. The bay can simulate fault conditions and trigger a **CO₂ suppression discharge** when heat or chemical thresholds are exceeded.

### Normal safety behavior

Under normal operation:

1. Occupancy sensors must read **occupied** before manual purge tests are disabled.
2. A PLC fault may trigger an automated safety purge if configured thresholds are exceeded.
3. Atmospheric alarms propagate to the security desk within seconds.
4. All purge events generate redundant logs in the PLC, the bay controller, and the central HelixSense archive.

### What happened on Saturday

Dana Cole exploited three properties of the system:

1. **Sensor spoofing:** a short-range relay device injected false steady-state occupancy readings long enough to satisfy interlocks.
2. **Manual override:** Dana used a maintenance-grade override fob borrowed through Vince Calder's blind-spot remediation work to initiate purge manually while the spoof held.
3. **Log staging:** Dana later pushed a synthetic PLC fault frame into the validation export through a finance-liaison maintenance account tied to vendor audit tooling.

The purge killed Elena Park. The staged logs make the event appear to be an automated response to a validation fault during authorized solo work.

## 4. Financial fraud scheme

Eight months before the adventure, Dana Cole created a procurement laundering route for automation spares and consulting services.

### Mechanism

- Purchase orders are issued to **Glassline Industrial Supply**, a vendor with a legitimate-looking website and tax identifier.
- Glassline invoices Meridian at inflated prices for common parts available elsewhere at standard cost.
- Fulfillment records show deliveries that either never occurred or were rerouted to Dana-controlled storage.
- Dana approves exceptions through the CFO liaison workflow when standard vendor checks flag delays.

### Elena's discovery

Elena did not begin as a fraud investigator. While tracing inconsistent spare-part serials in a robotics line, she found duplicate vendor metadata and mismatched shipment weights in HelixSense procurement exports.

Her private workbook identified:

- repeated PO numbers with altered line items;
- Glassline's registered address matching a mailbox suite linked to Dana's former consulting LLC;
- after-hours approvals on nights Dana claimed to be off-campus.

Elena told no one except a calendar entry labeled **"Audit packet — Monday"** and a encrypted note on her lab machine. She planned to deliver the packet to the outside director through a neutral compliance channel.

Dana learned Elena was close when Elena requested raw vendor certificate logs normally outside an architect's role.

## 5. Dana Cole's murder plan

Dana concluded that Elena would survive the audit and that Dana's liaison access would be traced. Murder was chosen to:

- stop the audit packet;
- preserve the accident narrative long enough to sanitize procurement records;
- exploit Elena's known habit of after-hours validation work.

### Preparation over two weeks

- Dana captured Elena's badge RF signature during a escorted tour.
- Vince Calder documented camera blind spots on the loading-dock approach in exchange for continued contract favorability; Dana did not tell him the purpose.
- Dana acquired a maintenance override fob by reporting it "lost" and receiving a replacement while retaining the old unit through Vince's sloppy checkout log.
- Dana rehearsed the sensor spoof using vendor audit hardware legally checked out to finance liaison staff.

### Execution constraints

Dana needed:

- Elena alone in Test Bay 3;
- a narrow window before night staff completed rounds;
- enough time to exit via the maintenance tunnel toward the loading dock;
- the security desk distracted by a staged vendor-call alibi.

Dana did not intend to kill anyone else. The plan fails forensically because Dana could not simultaneously be on a vendor call in the security office, at the loading dock, and in Test Bay 3—but those contradictions require investigators to compare logs rather than accept the first plausible accident story.

## 6. Elena Park

Dr. Elena Park, 41, was Chief Automation Architect. She led firmware validation for safety interlocks across Helix product lines.

Public reputation: brilliant, exacting, emotionally reserved.  
Actual personality: fair, stubborn, more trusting of systems than people.

She was not romantically involved with any suspect. She had no known drug use, no secret criminal history, and no supernatural or occult associations.

She died in Test Bay 3 between **21:14** and **21:18** campus time.

## 7. Supporting immutable facts

### Marcus Hale's safety override scandal

Six months earlier, Marcus authorized a temporary bypass on a conveyor safety interlock to meet a demo deadline. The bypass was removed, but Marcus edited the incident report to omit the duration of exposure. Elena discovered the edit during a unrelated review and told Marcus she would include it in a safety culture memo unless he self-reported. Marcus did not self-report. This gives him motive to fear Elena's notebook without making him the killer.

### Priya Nair rivalry

Dr. Priya Nair, 39, was passed over for Elena's promotion eighteen months ago. She resented Elena but continued to collaborate professionally. Priya did not know about the fraud until after the death, when she noticed Elena's encrypted audit folder naming pattern.

### Vince Calder's contract pressure

Vince's firm maintains camera and access hardware at Helix. Meridian corporate was considering rebidding the contract. Vince delayed reporting three blind spots and accepted cash for "expedited service" without documenting it. He did not know Dana planned murder.

### Tom Reyes red herring

Tom Reyes, 28, is the on-call maintenance technician. At 21:11 he responded to a jammed loading-dock lift that triggered a minor equipment alarm. His tool checkout and radio traffic place him at the dock, not in Test Bay 3. Dana later encouraged suspicion toward Tom because he has maint-tunnel access.

## 8. Investigator presence

The two investigators arrive at campus security after the purge alarm and initial medical response. They are not Meridian employees. They have read-only access grants negotiated by corporate counsel under pressure from the outside director.

Their investigation is legitimate but time-limited. At **00:30**, counsel will classify the incident packet for county review. Dana intends to leave campus before external law enforcement can interview her.

## 9. What cannot happen

The following are excluded from this adventure's reality:

- supernatural possession, curses, or premonitions;
- secret societies or occult motives;
- undiscovered sci-fi technology that invalidates sensor and badge evidence;
- Elena faking her death;
- a second unknown killer unrelated to the fraud scheme;
- automated systems acting with intent independent of human configuration.

## 10. Tone and plausibility

The case uses realistic industrial and corporate details. Jargon should remain comprehensible through context. Violence is serious and consequential. The facility's glass-walled aesthetic and log-rich environment justify the title **The Glass Alibi**—Dana's story is transparent only if investigators look at the right reflections.
