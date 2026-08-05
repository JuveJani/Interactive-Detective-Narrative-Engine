# Simulator v2 Schema

## Package input

Canonical `.idne` ZIP or unpacked directory with:

- `package_manifest.json`, `package_checksum.sha256`
- Layer manifests and `DO_NOT_READ/*_package.json` for: world_truth, environment, object_interaction, investigation_core, npc_investigation, investigation_flow, capability_check
- Optional validator manifests: investigation, story, playtime, dm_feeling

## Finding record (`findings.json`)

| Field | Type | Description |
|-------|------|-------------|
| finding_id | string | Unique ID |
| severity | string | critical, major, minor, info |
| confidence | string | proven, suspected |
| canonical_source | string | Canonical entity ID |
| source_file | string | Package file path |
| affected_entity | string | Entity impacted |
| affected_paths | string[] | Trace paths |
| simulation_evidence | string | Evidence text |
| expected_behavior | string | Expected rule |
| observed_behavior | string | Observed issue |
| trust_impact | string | Trust effect |
| likely_owner | string | SIMULATOR, PACKAGE, GENERATOR, UNDETERMINED |
| repair_eligible | bool | Safe to suggest repair |
| human_approval_required | bool | Requires human sign-off |
| validator | string | Source validator |

## Output manifest (`run_manifest.json`)

Adventure ID, play mode, trust summary, finding count, file list.

## Metrics (`metrics.json`)

In-world time, wall-clock estimates, player active time, session time, steps, simulation mode summaries.
