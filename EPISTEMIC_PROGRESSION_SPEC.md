# Epistemic Progression — Generator Notes

Adventure Generator v2 must emit state-gated playable events rather than flattening location menus.

## Required outputs

- `DO_NOT_READ/epistemic_progression_package.json` with `playable_events[]`
- Each event: `unit_id`, `event_kind`, prerequisites, `structured_actions[]`, relevant dependencies
- Separate NPC hub / topic / result events — no dialogue topics on location hubs
- New location variants when declared relevant knowledge or world state changes
- Stable internal unit IDs; new public sections only for new units

## Scene generation context

When generating PLAYER prose for a scene, the context package must include only:

- current player knowledge
- current relevant world state
- directly observable entities
- currently eligible structured actions
- allowed revelations for that event

Do not provide later-stage choices to the prose generator.
