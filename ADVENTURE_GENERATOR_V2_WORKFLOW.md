# Adventure Generator v2 — Workflow

**Milestone:** 11

---

## 1. Setup

1. Install Python 3.10+ (see `OFFLINE_SETUP_WINDOWS.md` for Windows 11).
2. Clone repository; no pip dependencies required for core tooling.
3. Configure local model endpoint (optional) in JSON config file.

---

## 2. Author brief

Create `adventure_brief.json` with parameters only (no story prose). Example fixture: `tests/fixtures/gen_v2_brief_solo.json`.

---

## 3. Run generation

```bash
python3 -m idne.generate tests/fixtures/gen_v2_brief_solo.json --workspace generated/my_adventure
```

Resume after interruption:

```bash
python3 -m idne.generate tests/fixtures/gen_v2_brief_solo.json --workspace generated/my_adventure --resume
```

Run through a single stage:

```bash
python3 -m idne.generate tests/fixtures/gen_v2_brief_solo.json --workspace generated/my_adventure --stage environment
```

---

## 4. Human approvals

When status is `AWAITING_APPROVAL`, review `human_approval_queue.md` in `.generation/reports/`. Approve by updating generation state or re-run with documented approval workflow (production: human signs off in tracker; tests use `--auto-approve`).

---

## 5. Validation

Integrated validation on adventure root:

```bash
python3 -m idne.validate_adventure generated/my_adventure/adventure
```

Final pipeline stage runs integrated validation automatically.

---

## 6. Package export

Final stage produces `<adventure_id>.idne` in the workspace root.

---

## 7. Repair loop

Automatic repair limited to schema, references, formatting, missing fields, and local consistency. Story-critical changes require human approval.

---

## 8. Downstream invalidation

If approved earlier truth changes, downstream stages are marked `INVALIDATED` and must be regenerated.
