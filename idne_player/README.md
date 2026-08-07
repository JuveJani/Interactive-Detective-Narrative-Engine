# IDNE Offline Player

Generic offline player for IDNE static gamebook adventures.

## Quick start (developer build)

```bash
# Generate structured player delivery for adventures (if not already built)
python -c "from pathlib import Path; from idne.gamebook_nav.build import build_gamebook_package as b; b(Path('adventures/The_Cold_Storage_Alarm/adventure'))"

# Build an offline player package with bundled adventures
python scripts/build_offline_player_package.py

# Open the package
# dist/idne-player/index.html
```

## Quick start (player user)

1. Copy the `dist/idne-player/` folder to a laptop.
2. Open `index.html` in Chrome, Firefox, Edge, or Safari.
3. Choose an adventure and press **Start** or **Continue**.

No internet connection, Python, Node, or developer tools are required after the package is copied.

## Load a custom adventure

If an adventure is not bundled, use **Load adventure file…** and select its `PLAYER/gamebook.json`.

## Structured delivery format

Player runtime data lives at `PLAYER/gamebook.json`, generated from the same public
delivery projection as `PLAYER/GAMEBOOK.md`.

### Authority direction (no reverse dependency)

```text
canonical adventure logic (DO_NOT_READ/*.json)
        ↓
epistemic / materialized public delivery state
  (epistemic_progression_package.json + PLAYER template prose)
        ↓
player delivery projection (build_gamebook_package)
        ↓
generated artifacts:
  - player_mapping_manifest.json
  - PLAYER/GAMEBOOK.md
  - PLAYER/gamebook.json
```

`player_mapping_manifest.json`, `GAMEBOOK.md`, and `gamebook.json` are **downstream
projections only**. Canonical and epistemic generation do not read them.

The common build-time representation is the in-memory delivery graph produced by
`load_materialized_delivery()` / `build_navigation_graph()` from canonical packages
and epistemic snapshots. Both markdown and JSON artifacts are rendered from that
graph plus template prose.

## Save / resume

- Autosave on every choice (Continue on the opening screen)
- Three manual save slots per adventure (browser local storage)

## Offline architecture

Bundled adventures ship as `library/adventures/<id>.js` files because browsers block `fetch()` for local `file://` pages. Script tags load these adventure payloads without a web server.

## Browser support

Tested approach targets current Chromium, Firefox, Edge, and Safari on desktop/laptop screens.
