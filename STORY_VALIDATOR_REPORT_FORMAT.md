# Story Validator — Report Format

**Harness:** `python3 -m idne.story_validate <adventure_root>`  
**Exit codes:** `0` PASS/SKIP/CONDITIONAL_PASS; `1` FAIL; `2` BLOCKED

---

## Top-level report

```json
{
  "adventure_root": "/path/to/adventure",
  "status": "PASS",
  "findings": [],
  "warnings": [],
  "checks": {
    "SV-PKG-PRESENT": "PASS",
    "SV-PLAYER-PRESENT": "PASS",
    "SV-FRAME": "PASS",
    "SV-TIMELINE": "PASS",
    "SV-CAUSAL": "PASS",
    "SV-INFORMATION": "PASS",
    "SV-KNOWLEDGE-ORDER": "PASS",
    "SV-NPC": "PASS",
    "SV-CONTINUITY": "PASS",
    "SV-NEUTRALITY": "PASS",
    "SV-INFERENCE": "PASS",
    "SV-TRANSITIONS": "PASS",
    "SV-ENDING": "PASS",
    "SV-PLAIN-LANGUAGE": "PASS",
    "SV-PLAY-MODE": "PASS"
  },
  "tier_b_pending": [],
  "player_files_scanned": ["PLAYER/OPENING.md", "PLAYER/INVESTIGATION.md"]
}
```

`SV-PLAYER-PRESENT` may be `BLOCKED` when PLAYER text is absent.

---

## Representative finding IDs

| ID | Scenario |
|---|---|
| `SV-AMBIGUOUS-DAY` | Incident time without clear day |
| `SV-START-INCIDENT-CONFUSED` | Investigation start confused with incident |
| `SV-CONTRADICTORY-TIMELINE` | Contradictory dates/times |
| `SV-RELATIVE-NO-ANCHOR` | Relative date without anchor |
| `SV-FACT-BEFORE-INTRO` | Fact used before introduction |
| `SV-UNDEFINED-ENTITY` | Undefined person/object/term |
| `SV-HALF-INFORMATION` | Half-information without source |
| `SV-NPC-BEYOND-KNOWLEDGE` | NPC testimony beyond knowledge |
| `SV-NPC-MOTIVATION` | Behaviour contradicts motivation |
| `SV-SUSPICIOUS-INNOCENT` | Unexplained suspicious innocent behaviour |
| `SV-OBJECT-MOVES` | Object moves without event |
| `SV-REVISIT-IGNORES-STATE` | Revisit ignores state change |
| `SV-INFERENCE-UNDEFINED-TERM` | Inference uses undefined term |
| `SV-INFERENCE-UNCLEAR` | Grammatically unclear question |
| `SV-OPENING-LACKS-CONTEXT` | Opening lacks incident context |
| `SV-TRANSITION-NO-CAUSE` | Transition without causal explanation |
| `SV-ENDING-CONTRADICTS-TRUTH` | Ending contradicts Fixed Truth |
| `SV-IMPERFECT-LEAK` | Imperfect ending leaks full truth |
| `SV-LOADED-DESCRIPTION` | Loaded suspect description (Tier B) |
| `SV-QUOTATION-EMPHASIS` | Suspicious quotation emphasis (Tier B) |
| `SV-UNDEFINED-ACRONYM` | Undefined acronym |
| `SV-EXCESSIVE-JARGON` | Excessive jargon |
| `SV-INCONSISTENT-NAMING` | Inconsistent entity naming |
| `SV-PLAYER-ABSENT` | PLAYER text absent → BLOCKED |
| `SV-ASSUMES-UNAVAILABLE-KNOWLEDGE` | Scene assumes unavailable knowledge |

Tier B prefix: `SV-TIER-B-<review_id>`.
