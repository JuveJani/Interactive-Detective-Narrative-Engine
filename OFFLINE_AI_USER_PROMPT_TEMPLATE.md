# Offline AI User Prompt Template

Copy this template and fill in the bracketed sections.

---

I am debugging an IDNE adventure offline on Android Termux.

**Finding ID:** [e.g. SIM-TRUST-DOWNGRADE]

**Context file attached:** finding_context_[ID].md

**Simulator trustworthy:** [true/false from context]

Please:

1. Explain the finding in simple language for a non-programmer.
2. List what is **proven** vs **only suspected**.
3. Suggest the **smallest safe repair** without changing the engine unless an engine rule is clearly violated.
4. List **risks** of each suggestion.
5. Tell me what **human approval** is required before I edit files.
6. Give **exact validation commands** to rerun after a fix.

If I ask for a patch, provide step-by-step edit instructions only — do not claim you modified my repository.

---

Optional follow-up:

> Based on repair option [REP-...-...], write exact patch instructions for the files listed.
