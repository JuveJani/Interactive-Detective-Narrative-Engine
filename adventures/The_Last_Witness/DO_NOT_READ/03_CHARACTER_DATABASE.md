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

## NPC-01: Elias Varga

**Role:** missing witness  
**Age:** 38  
**Occupation:** financial controller, Northstar Renewal  
**Initial state:** critically injured in Signal Room 4B  
**Public reputation:** precise, anxious, politically neutral  
**Actual personality:** stubborn, morally serious, controlling under stress

### Motivation

Expose the corruption scheme without allowing Greyhaven Police to seize or destroy the evidence.

### Private history

Elias and Lena grew up with a father who accepted small corrupt payments while working at the port. Elias responded by becoming rigidly honest. Lena responded by learning that survival often requires compromise.

### Knowledge

Elias knows:

- the complete corruption structure;
- Rook is compromised;
- Nadia's recovery-code fragment;
- the signal-room route;
- that Lena followed him;
- that Reed caused the struggle;
- the final three recovery-code digits.

### Incorrect beliefs

- He believes he can delay hospital treatment until 02:00.
- He believes Nadia's upload is safer than it actually is.
- He does not know Marcus betrayed them.

### Statements while conscious

Elias can produce only fragments after 21:15. Each fragment must be ambiguous without supporting clues.

Potential fragments:

- “Four-B.”
- “Windows.”
- “Not Rook.”
- “The black one is false.”
- “Nadia has three.”

### Branch states

- hidden_alive;
- found_critical;
- evacuated;
- dead;
- conscious_testimony;
- unconscious_survivor.

---

## NPC-02: Nadia Soren

**Role:** investigative journalist and initial client  
**Age:** 34  
**Public presentation:** confident, sharp, impatient  
**Private motive:** expose Northstar and protect Elias  
**Hidden flaw:** treats people as components of a story when under pressure

### Knowledge

Nadia knows:

- Elias planned to disappear voluntarily;
- Signal Room 4B was the intended hideout;
- the first three recovery-code digits;
- the evidence-transfer time;
- the ferry photograph contains a hidden code;
- Rook may be compromised.

She does not know:

- Lena is involved;
- Elias is injured;
- Marcus leaked information;
- Reed reached the terminal.

### Lies and omissions

At the opening, Nadia withholds that she helped Elias disappear. She tells the players only that Elias “did not trust the official plan.”

Reason: admitting involvement could make her an accessory and cause the players to abandon her.

### Pressure response

- If accused with evidence, she admits the staged disappearance.
- If accused without evidence, she becomes defensive and restricts access.
- If Elias is found dying, she prioritizes rescue.
- If the ledger is available but rescue is delayed, she may insist on copying it first, creating a moral choice.

### Trust variable

`NADIA_TRUST` ranges from -2 to +2.

High trust grants:

- recovery-code fragment;
- direct access to archived files;
- confession about the plan.

Low trust causes:

- withheld code;
- independent interference at the terminal;
- possible public leak.

---

## NPC-03: Lena Varga

**Role:** Elias's sister and apparent kidnapper  
**Age:** 31  
**Occupation:** maritime logistics dispatcher in another city  
**Public presentation:** direct, hostile, protective  
**Private motive:** keep Elias alive and prevent institutions from using him

### Knowledge

Lena knows:

- Elias disappeared voluntarily;
- Elias is inside Signal Room 4B;
- Reed confronted them;
- Elias fell;
- Iris is treating him;
- the ledger is hidden in the room;
- Elias distrusts Rook.

She does not understand the full ledger or upload process.

### Secret

Their father accepted money connected to Krell. Lena fears disclosure will destroy the remaining family reputation and may implicate her in an old customs offence.

### Lies

- Claims she arrived in Greyhaven after 20:00.
- Denies contacting Elias.
- If cornered, claims Reed deliberately pushed Elias.
- May say Elias is already gone to divert pursuit.

### Pressure response

Lena cooperates only if players demonstrate both:

1. knowledge that Rook is compromised; and
2. a credible medical rescue plan that does not hand Elias directly to Rook.

Threatening arrest hardens her resistance.

### Branch states

- concealed;
- cooperative;
- barricaded;
- arrested;
- escaped;
- injured during terminal confrontation.

---

## NPC-04: Dr. Iris Bell

**Role:** clandestine medical helper  
**Age:** 46  
**Occupation:** elder-care clinician; formerly emergency physician  
**Public presentation:** calm, tired, clinically blunt  
**Private motive:** save Elias without exposing Lena to corrupt police

### Background

Iris lost her hospital position after altering records to protect an abused teenage patient from a politically connected parent. Her action was ethically understandable but legally indefensible.

### Knowledge

Iris knows:

- Elias has a life-threatening head injury;
- Lena's account of the fall;
- Signal Room 4B;
- an ambulance is necessary;
- police are searching for medical supplies.

She does not know the corruption details.

### Lies

- Tells her employer she is ill.
- If questioned early, denies leaving the care facility.
- May minimize Elias's condition to prevent panic.

### Medical rule

Iris can provide credible assessment and stabilization but cannot solve the injury. Her presence buys time; it does not replace surgery.

### Cooperation triggers

Iris cooperates if players:

- identify a hospital route not controlled by Rook;
- secure Mina Cho or another trustworthy escort;
- or expose Rook sufficiently that normal emergency services become viable.

---

## NPC-05: Inspector Adrian Rook

**Role:** compromised police inspector and active antagonist  
**Age:** 52  
**Public presentation:** composed, paternal, authoritative  
**Private motive:** preserve his position and prevent the ledger reaching external investigators

### Knowledge

Rook knows:

- Elias missed pickup deliberately or was taken before it;
- Elias used transit near the harbor;
- Krell is searching independently;
- Nadia is connected;
- the players are investigating.

He does not initially know:

- Signal Room 4B;
- Lena's role;
- Elias's injury;
- that the decoy key tracks access.

### Methods

- uses legal language to conceal improper orders;
- isolates witnesses;
- alters reports;
- creates urgency;
- offers apparently reasonable cooperation;
- avoids overt violence when documentation exists.

### Lies

- Claims he personally requested Elias's protection.
- Claims camera searches were authorized.
- Claims Lena has a violent history.
- Claims Regional Public Integrity asked police to seize all evidence.
- May claim Elias is wanted for embezzlement after midnight.

### Exposure threshold

Rook should not be conclusively exposed by one clue. The minimum fair combination is:

- altered report metadata;
- unauthorized camera request;
- contact with Krell or false transfer paperwork.

### Branch states

- unsuspected;
- questioned;
- exposed_privately;
- exposed_publicly;
- controls_rescue;
- arrested_later;
- destroys_partial_evidence.

---

## NPC-06: Jonas Krell

**Role:** contractor and corruption beneficiary  
**Age:** 49  
**Public presentation:** civic entrepreneur and donor  
**Private motive:** recover the ledger and contain the scandal  
**Physical presence:** optional phone/video appearance; may appear near final confrontation only in an expanded version

### Knowledge

Krell knows:

- Marcus leaked the harbor direction;
- Reed recovered a black key;
- the key appears incomplete;
- Lena may have Elias;
- Rook is handling the police side.

He does not know the exact room or code.

### Operational rule

Krell prefers:

1. purchase;
2. intimidation;
3. evidence theft;
4. controlled violence.

He avoids unnecessary killing because a dead witness creates attention.

---

## NPC-07: Silas Reed

**Role:** fixer who caused the terminal struggle  
**Age:** 36  
**Public presentation:** private security consultant  
**Private motive:** finish the recovery job and avoid being blamed for Elias's injury

### Knowledge

Reed knows:

- Elias fell during their struggle;
- Lena moved him;
- the decoy bag was planted;
- Krell will sacrifice him if necessary;
- the approximate terminal area.

### Emotional state

Reed is frightened rather than sadistic. Once he realizes Elias may die, he becomes increasingly willing to trade information for protection.

### Lies

- Initially claims he never entered the terminal.
- Claims Lena attacked without warning.
- Claims Elias had a firearm.
- Claims the fall occurred before he arrived.

### Cooperation path

Players can turn Reed by proving:

- the decoy key contains a tracker;
- Krell has already described him as a rogue contractor;
- Rook intends to arrest or eliminate him.

Reed can provide one important link to Krell but not the whole conspiracy.

---

## NPC-08: Marcus Hale

**Role:** editor who betrayed Nadia  
**Age:** 58  
**Public presentation:** principled, exhausted newspaper veteran  
**Private motive:** save the Greyhaven Ledger from closure  
**Moral position:** guilty and self-deceiving, but not aligned with the full conspiracy

### Knowledge

Marcus knows:

- he leaked the harbor direction and transfer time;
- Krell paid through an intermediary;
- Nadia used an old terminal photograph;
- the newsroom account holds part of the encrypted archive.

He does not know:

- the precise hiding room;
- Elias's injury;
- Rook's full role.

### Lies

- Says Nadia never discussed the harbor.
- Claims the deleted call data was routine cleanup.
- Blames an intern for moving the photograph.
- Says the newspaper received an anonymous donation.

### Confession triggers

Two of the following:

- carrier call record;
- payment proof;
- recovered deleted voicemail;
- Reed naming the intermediary;
- Nadia confronting him after discovering the missing photograph.

### Branch states

- concealing;
- partial_confession;
- full_confession;
- fleeing;
- public_statement.

---

## NPC-09: Mina Cho

**Role:** honest patrol officer and potential ally  
**Age:** 27  
**Public presentation:** careful, procedural, observant  
**Private motive:** do her job without destroying her career  
**Starting position:** uncertain whether Rook is corrupt or simply aggressive

### Knowledge

Mina knows:

- the apartment showed weak signs of forced entry;
- her original report was altered;
- Rook requested camera data unusually quickly;
- the players have legitimate concerns.

### Trust conditions

Mina's trust increases when players:

- share evidence rather than speculation;
- avoid publicly accusing her;
- protect her identity;
- correctly identify a detail from her original report.

It decreases when players:

- trespass recklessly;
- threaten her;
- publish her name;
- lie about evidence.

### Function in final act

Mina can:

- arrange a safe ambulance route;
- preserve evidence;
- detain Rook temporarily;
- authenticate altered records.

She must not become an all-purpose rescue mechanism. Players still need to locate Elias and understand the danger.

---

## NPC-10: Mara Vale

**Role:** architect of the corruption scheme  
**Age:** 45  
**Public presentation:** reformist deputy mayor  
**Private motive:** retain political power and avoid prosecution  
**Active presence:** remote

### Knowledge

Vale knows:

- Elias is a threat;
- Rook and Krell are handling containment;
- an evidence transfer may happen after midnight.

She does not know operational details.

### Story rule

Vale is not available for a normal interview during the two-hour prototype. Her influence appears through records, statements, calls, and the final public response. This prevents the cast from expanding beyond manageable scope.

---

## Relationship summary

- Elias trusts Nadia but hides Lena's involvement.
- Nadia trusts Elias but underestimates his medical and emotional risk.
- Lena distrusts Nadia and all police.
- Iris trusts Lena more than institutions.
- Rook and Krell cooperate while preparing to blame one another.
- Krell uses Reed and intends to discard him.
- Marcus admires Nadia but betrays her work.
- Mina respects Rook at the opening but is disturbed by his actions.
- Vale considers everyone replaceable.
