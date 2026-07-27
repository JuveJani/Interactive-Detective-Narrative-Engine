# DO NOT READ: NPC Knowledge and Disclosure Matrix

## 1. Knowledge rule

An NPC may state a fact only if it is present in their knowledge state. Every non-obvious fact requires one of:

- direct observation;
- prior participation;
- received communication;
- document access;
- justified inference.

Rumours and beliefs must be labelled internally as beliefs, not truth.

## 2. Nadia Soren

### Initial knowledge at 20:00

Knows:

- Elias planned a voluntary disappearance;
- the intended general harbor destination;
- Signal Room 4B was proposed;
- evidence transfer is scheduled for 02:00;
- first three recovery digits;
- police protection may be compromised.

Does not know:

- Elias reached the room successfully;
- Lena followed him;
- Reed confronted him;
- Elias is injured;
- Marcus leaked the plan.

### Disclosure stages

**Stage 0, guarded:** says Elias distrusted the protection plan.  
**Stage 1, evidence confronted or trust +1:** admits she helped him avoid pickup.  
**Stage 2, trust +2 or proof of harbor:** reveals Signal Room 4B and her code fragment.  
**Emergency override:** if credible evidence shows Elias is injured, she reveals all rescue-relevant information regardless of legal risk.

No ordinary single persuasion roll produces Stage 2.

## 3. Mina Cho

### Initial knowledge

- apartment forced entry looked weak;
- blood volume was small;
- report was submitted;
- Rook took unusual control.

### Knowledge updates

- 21:05: notices official report differs from her notes if she checks system;
- after player evidence: infers Rook may be manipulating case;
- after unauthorized-camera proof: can state procedural misconduct;
- after contact proof: may accept corruption conclusion.

Mina cannot name the full conspiracy merely because she distrusts Rook.

## 4. Lena Varga

### Initial knowledge

- Elias contacted her;
- he intended to hide at terminal;
- Reed confronted them;
- Elias fell;
- Iris is treating him;
- police cannot be trusted according to Elias.

### Beliefs

- Nadia may have leaked the plan;
- official hospital transfer will place Elias in Rook's custody;
- evidence matters to Elias more than his life.

### Disclosure stages

- hostile: denies location and contact;
- pressured without trust: supplies misleading route;
- shown proof against Rook plus rescue plan: confirms Elias alive;
- trusted rescue control: opens Signal Room 4B.

## 5. Iris Bell

Knows only the medical and immediate concealment facts. She does not know who designed the corruption scheme.

Disclosure is controlled by patient safety, not generic persuasion:

- credible rescue route;
- trustworthy medical contact;
- proof Rook cannot seize Elias;
- or Elias's condition becoming immediately fatal.

## 6. Adrian Rook

### Initial knowledge at 20:00

- Elias missed official pickup;
- disappearance may be voluntary;
- transit data points toward harbor;
- Krell is conducting parallel recovery;
- Nadia is likely involved.

### Updates

- learns player searches through police systems;
- learns archive request if made openly;
- learns terminal location from exposed calls, captured NPC, or surveillance;
- does not know room number without a specific ingestion event.

### Disclosure behavior

Rook never confesses under a routine check. He may:

- admit procedural shortcuts while denying corruption;
- blame urgency;
- offer partial truth to gain evidence;
- make a deal only when confronted with preserved external proof and loss of institutional control.

## 7. Silas Reed

### Initial knowledge

- confrontation occurred;
- Elias fell;
- Lena moved him;
- decoy key was taken;
- Krell expects recovery.

### Cooperation gate

Reed provides critical testimony only after at least one hard lever:

- proof Krell is framing him;
- proof decoy key tracks him;
- credible immunity/protection route;
- immediate threat from Rook or Krell demonstrated in scene.

Before that, he may reveal low-risk details but not Krell's complete role.

## 8. Marcus Hale

### Initial knowledge

- he leaked timing and harbor direction;
- he received money;
- Nadia's photograph matters;
- evidence transfer exists.

### Confession gate

Full confession requires two independent pressures:

- payment/call proof;
- Nadia confrontation;
- Reed/intermediary corroboration;
- evidence that the leak caused immediate physical harm.

A single persuasion failure or success cannot erase his self-preservation motive.

## 9. Information-ingestion records

The Adventure Logic must encode updates in this form:

```text
KNOWLEDGE_UPDATE
actor: NPC_MINA
fact: FACT_REPORT_ALTERED
source: ITEM_MINA_REPORT_ORIGINAL + ITEM_ROOK_REPORT_ALTERED
start_time: 21:05
condition: system_checked OR player_provides_versions
```

No dialogue node may introduce a fact without a matching initial state or update record.
