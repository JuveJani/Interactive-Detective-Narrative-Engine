"""Resolve playable unit destinations against epistemic state snapshots."""

from __future__ import annotations

from idne.epistemic_progression.fingerprint import StateFingerprint, materialized_unit_id, template_unit_id
from idne.epistemic_progression.materialize import lookup_materialized_unit
from idne.epistemic_progression.model import EpistemicPackage, EpistemicState


def resolve_playable_unit(
    package: EpistemicPackage,
    state: EpistemicState,
    dest_unit_id: str,
    *,
    initial_state: EpistemicState | None = None,
) -> str:
    """Return the materialized unit id for dest template at the given state."""
    if initial_state is None:
        from idne.epistemic_progression.loader import initial_epistemic_state

        initial_state = initial_epistemic_state(package)

    tpl = template_unit_id(dest_unit_id)
    matched = lookup_materialized_unit(package, tpl, state, initial_state=initial_state)
    if matched:
        return matched

    initial_fp = StateFingerprint.from_state(initial_state)
    fp = StateFingerprint.from_state(state)
    candidate = materialized_unit_id(tpl, fp, initial=initial_fp)
    if candidate in package.events_by_unit:
        return candidate

    # Legacy packages without materialized snapshots.
    if dest_unit_id in package.events_by_unit:
        return dest_unit_id
    return candidate
