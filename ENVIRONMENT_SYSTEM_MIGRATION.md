# Environment System — Migration Guide

## New adventures

1. Author `environment_package.json` after World-First layers (or parallel with world states).
2. Declare `environment_manifest.json`.
3. Run `python3 -m idne.environment_validate`.
4. Delivery scenes reference locations — do not invent state.

## Legacy adventures

Harborview and Glass Alibi lack environment manifests → validator `SKIP`. **Do not auto-migrate.**

## World-First

Environment locations MUST link via `world_first_provenance`. World-State Timeline snapshots should align with `location_states`.

## Play modes

One environment package per adventure. Split booklets compile views of the same locations.

## Milestone 4

Object interactions will attach to `feature_id` with `has_further_interaction: true` — not defined in Milestone 3.
