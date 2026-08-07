"""Deterministic scrambled public section numbering."""

from __future__ import annotations

import hashlib
import random
from typing import Iterable


def assign_public_sections(
    unit_ids: Iterable[str],
    adventure_id: str,
    *,
    seed_override: str | None = None,
    existing_map: dict[str, int] | None = None,
    min_section: int = 101,
    max_section: int | None = None,
) -> dict[str, int]:
    """Assign stable opaque public section numbers without chronological order."""
    units = sorted(set(unit_ids))
    if not units:
        return {}

    existing_map = existing_map or {}
    retained = {uid: existing_map[uid] for uid in units if uid in existing_map}
    new_units = [uid for uid in units if uid not in retained]
    if not new_units and len(retained) == len(units):
        return retained

    if max_section is None:
        max_section = max(999, min_section + len(units) + 50)
    span = max_section - min_section + 1
    if len(units) > span:
        max_section = min_section + len(units) - 1
        span = max_section - min_section + 1

    seed_material = seed_override or adventure_id
    digest = hashlib.sha256(f"{seed_material}:{'|'.join(units)}".encode()).hexdigest()
    rng = random.Random(int(digest[:16], 16))

    used_numbers = set(retained.values())
    pool = [n for n in range(min_section, max_section + 1) if n not in used_numbers]
    rng.shuffle(pool)
    if len(pool) < len(new_units):
        raise ValueError("insufficient section numbers after retaining existing assignments")

    chosen = pool[: len(new_units)]
    paired = list(zip(new_units, chosen))
    paired.sort(key=lambda x: x[0])
    numbers_sorted = sorted(chosen)
    fresh = {uid: numbers_sorted[i] for i, (uid, _) in enumerate(paired)}
    return {**retained, **fresh}
