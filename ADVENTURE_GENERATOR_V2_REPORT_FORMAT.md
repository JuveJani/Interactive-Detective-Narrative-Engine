# Adventure Generator v2 — Report Format

**Milestone:** 11

Reports are written to `<workspace>/.generation/reports/`.

---

## generation_summary.md

Human-readable overview: adventure ID, readiness status, logic validation flag, per-stage status list.

---

## stage_status.json

Machine-readable map of stage IDs to status strings.

---

## validator_summary.md

Integrated validator table (from `validate_adventure` when run standalone or at final validation).

---

## repair_history.md

Chronological repair attempts: auto vs manual, stage, finding IDs, invalidate-downstream events.

---

## human_approval_queue.md

Stages requiring approval and APPROVED/PENDING status.

---

## unresolved_findings.json

Invalidated stages, validator status summary, Tier B/C gaps.

---

## model_usage.json

Per-stage context token estimates and model metadata.

---

## package_manifest.json

Index of report paths and readiness status.

---

## Stage output artifacts

`<workspace>/.generation/stages/<stage_id>/model_response.json`  
`<workspace>/.generation/stages/<stage_id>/applied_files.json` (mock backend)
