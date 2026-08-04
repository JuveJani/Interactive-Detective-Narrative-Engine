# Capability Check System — Migration

**From:** inline `check_binding` blocks in Object Interaction only  
**To:** canonical `capability_check_package.json` + manifest

## Steps

1. Add `capability_check_manifest.json` with `capability_check_method: canonical`.
2. Move full check definitions to `DO_NOT_READ/capability_check_package.json`.
3. Retain `check_id` references in Object Interaction `check_binding` (Milestone 4 compatibility).
4. Add `information_trace` for each knowledge-granting check.
5. Split declaration units from success/failure `destination_units`.
6. Run `python3 -m idne.capability_check_validate`.

## Legacy adventures

Harborview, Glass Alibi: **SKIP** (not FAIL) until migrated.

## Not migrated in Milestone 6

Paid retries, false checks, inventory capacity — schema fields reserved via `retry_extension_point`.
