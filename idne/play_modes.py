"""Play mode identifiers and normalization."""

from __future__ import annotations

PLAY_MODE_SINGLE = "single_investigator"
PLAY_MODE_TWO_PLAYER = "two_player"

VALID_PLAY_MODES = frozenset({PLAY_MODE_SINGLE, PLAY_MODE_TWO_PLAYER})


def normalize_play_modes(modes: list[str] | None) -> list[str]:
    """Return deduplicated play modes in canonical order."""
    if not modes:
        return []
    out: list[str] = []
    seen: set[str] = set()
    for m in modes:
        if m not in VALID_PLAY_MODES:
            raise ValueError(f"invalid play_mode: {m}")
        if m not in seen:
            seen.add(m)
            out.append(m)
    return out
