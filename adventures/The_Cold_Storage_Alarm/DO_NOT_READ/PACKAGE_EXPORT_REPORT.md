# Package Export Report — The Cold Storage Alarm

**Stage:** `package_export`  
**Date:** 2026-08-06  
**Package status:** `PRE_PLAYTEST`

---

## Exported artifact

| Field | Value |
|-------|-------|
| **File** | `adventures/The_Cold_Storage_Alarm/The_Cold_Storage_Alarm.idne` |
| **Adventure ID** | `The_Cold_Storage_Alarm` |
| **Package schema version** | `1.0` |
| **Archive entries** | 51 manifest-tracked files (52 ZIP members incl. manifest + checksum) |
| **SHA-256** | `61868211e1685c3c0565df8b040a8df3bcb9a6e07255a9ead53f92b28618da49` |
| **Size** | ~89 KB |

---

## Package integrity validation

| Check | Result |
|-------|--------|
| `package_manifest.json` present | PASS |
| `package_checksum.sha256` present | PASS |
| Per-entry SHA-256 vs manifest | PASS |
| Checksum file vs extracted files | PASS |
| `read_idne_package` status | PASS |
| `verify_extracted_package` | PASS |

---

## Required layers included

### Adventure root (`adventure/`)

- `generation_manifest.json`
- `play_manifest.json`
- `PLAYER/` — full player-facing prose (96 mapped units)
- Logic packages under `DO_NOT_READ/`:
  - world_truth
  - environment
  - object_interaction
  - investigation_core
  - npc_investigation
  - investigation_flow
  - capability_check
  - story_validator
  - playtime_calibration
  - dm_feeling_validator
  - investigation_validator (IV harness)
- Manifests for each layer

### Extra roots

| Prefix | Source | Purpose |
|--------|--------|---------|
| `generation/` | `.generation/` | Generation state and reports |
| `brief/` | `brief/` | Canonical adventure brief |

---

## Build command (reproducible)

```bash
python3 -c "
from pathlib import Path
from idne.idne_package import build_idne_package

workspace = Path('adventures/The_Cold_Storage_Alarm')
build_idne_package(
    workspace / 'adventure',
    workspace / 'The_Cold_Storage_Alarm.idne',
    'The_Cold_Storage_Alarm',
    extra_roots={
        'generation': workspace / '.generation',
        'brief': workspace / 'brief',
    },
)
"
```

---

## Simulator v2 load verification

| Field | Value |
|-------|-------|
| Load status | READY |
| Play mode | single_investigator |
| Package version | 1.0 |
| Integrated validation | CONDITIONAL_PASS |
| Missing simulation layers | none |

---

## Export policy applied

- Export **not** downgraded for Tier C pending.
- Export **not** downgraded for playtime above 120-minute target.
- CONDITIONAL_PASS preserved on playtime and dm_feeling validators.
- Package status set to **PRE_PLAYTEST**, not ADVENTURE_READY.
- No PLAYER or upstream logic modifications for time reduction.

---

## Post-export requirements

1. Human playtest using spoiler-free guide and playtime recording sheet.
2. Record actual wall-clock time (breaks excluded).
3. Complete Tier C questionnaire after session.
4. Re-run integrated validation after any post-playtest fixes.
5. Do not mark Adventure Ready until Tier C evidence exists and integrated status is PASS.
