"""Knowledge- and world-state-gated scene progression."""

from idne.epistemic_progression.eligibility import (
    action_eligible,
    event_enterable,
    filter_eligible_actions,
)
from idne.epistemic_progression.loader import load_epistemic_package, load_epistemic_manifest
from idne.epistemic_progression.model import (
    EpistemicState,
    PlayableEvent,
    StructuredAction,
)
from idne.epistemic_progression.resolve import resolve_playable_unit
from idne.epistemic_progression.signatures import (
    knowledge_signature,
    world_state_signature,
)

__all__ = [
    "EpistemicState",
    "PlayableEvent",
    "StructuredAction",
    "action_eligible",
    "event_enterable",
    "filter_eligible_actions",
    "knowledge_signature",
    "load_epistemic_manifest",
    "load_epistemic_package",
    "resolve_playable_unit",
    "world_state_signature",
]
