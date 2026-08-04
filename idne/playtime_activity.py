"""Activity taxonomy and duration estimation (Milestone 9)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

# Reusable wall-clock activity classes
ACTIVITY_CLASSES = frozenset(
    {
        "simple_reading",
        "complex_reading",
        "rereading",
        "action_selection",
        "trivial_decision",
        "meaningful_decision",
        "page_navigation_lookup",
        "dice_check_resolution",
        "short_note_taking",
        "detailed_record_update",
        "object_search_decision",
        "clue_information_comparison",
        "callback_lookup",
        "inference_answer",
        "simple_puzzle",
        "medium_puzzle",
        "complex_puzzle",
        "npc_conversation_choice",
        "player_discussion",
        "failed_inference_recovery",
        "revisit",
        "ending_questionnaire",
        "ending_reading",
        "joint_scene",
        "regroup_discussion",
        "setup_opening",
    }
)


@dataclass
class DurationEstimate:
    lower_minutes: float
    expected_minutes: float
    upper_minutes: float
    components: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return {
            "lower_minutes": round(self.lower_minutes, 2),
            "expected_minutes": round(self.expected_minutes, 2),
            "upper_minutes": round(self.upper_minutes, 2),
            "components": self.components,
        }


def _reading_seconds(
    word_count: int,
    complexity: str,
    reread_expected: bool,
    assumptions: dict[str, Any],
) -> tuple[float, float, float]:
    wc = max(0, int(word_count))
    if complexity == "complex":
        spw = float(assumptions.get("complex_seconds_per_word", 2))
    else:
        spw = float(assumptions.get("simple_seconds_per_word", 1))
    base = wc * spw
    if reread_expected:
        extra = float(assumptions.get("reread_add_full_reading_plus_seconds", 10))
        base = base * 2 + extra
    low = base * 0.85
    exp = base
    high = base * 1.15
    return low / 60.0, exp / 60.0, high / 60.0


def estimate_activity(
    activity: dict[str, Any],
    assumptions: dict[str, Any],
    class_defaults: dict[str, Any],
) -> DurationEstimate:
    """Estimate one authored activity's wall-clock range."""
    cls = str(activity.get("activity_class", ""))
    components: list[dict[str, Any]] = []

    # Authored explicit bounds override computation
    if activity.get("authored_expected_minutes") is not None or activity.get("authored_lower_minutes") is not None:
        exp = float(activity.get("authored_expected_minutes", activity.get("authored_lower_minutes", 0)))
        low = float(activity.get("authored_lower_minutes", exp * 0.9))
        high = float(activity.get("authored_upper_minutes", exp * 1.1))
        components.append({"type": cls, "method": "authored", "expected_minutes": exp})
        return DurationEstimate(low, exp, high, components)

    defaults = (class_defaults.get(cls) or {}) if class_defaults else {}
    low = float(defaults.get("lower_minutes", 0.5))
    exp = float(defaults.get("expected_minutes", 1.0))
    high = float(defaults.get("upper_minutes", 1.5))

    if cls in ("simple_reading", "complex_reading", "rereading", "ending_reading", "setup_opening"):
        complexity = "complex" if cls in ("complex_reading", "rereading") else activity.get("complexity", "simple")
        if activity.get("complexity_misclassified_as_complex") and complexity == "complex":
            complexity = "simple"
        reread = cls == "rereading" or activity.get("reread_expected", False)
        rl, re, rh = _reading_seconds(
            int(activity.get("word_count", 0)),
            complexity,
            reread,
            assumptions,
        )
        low, exp, high = rl, re, rh
        components.append({"type": cls, "method": "reading_model", "word_count": activity.get("word_count", 0)})

    elif cls == "callback_lookup":
        age = str(activity.get("callback_age", "recent"))
        threshold = float(assumptions.get("callback_old_threshold_minutes", 60))
        if age == "old" or float(activity.get("minutes_since_introduction", 0)) >= threshold:
            m = float(assumptions.get("callback_old_minutes", 5))
        else:
            m = float(assumptions.get("callback_recent_minutes", 2))
        low, exp, high = m * 0.9, m, m * 1.1
        components.append({"type": cls, "method": "callback_model", "minutes": m})

    elif cls in ("trivial_decision", "meaningful_decision", "action_selection", "npc_conversation_choice"):
        if activity.get("bare_destination_code"):
            low, exp, high = 0.1, 0.15, 0.25
        elif cls == "meaningful_decision" or activity.get("strategic", False):
            low = float(activity.get("decision_lower_minutes", defaults.get("lower_minutes", 2)))
            exp = float(activity.get("decision_expected_minutes", defaults.get("expected_minutes", 4)))
            high = float(activity.get("decision_upper_minutes", defaults.get("upper_minutes", 8)))
        else:
            opts = int(activity.get("option_count", 2))
            exp = min(exp, 0.5 + opts * 0.25)
            low, high = exp * 0.8, exp * 1.2
        components.append({"type": cls, "method": "decision_model"})

    elif cls in ("simple_puzzle", "medium_puzzle", "complex_puzzle"):
        if activity.get("checkbox_masquerade"):
            low, exp, high = 0.2, 0.3, 0.5
        else:
            low = float(activity.get("puzzle_lower_minutes", defaults.get("lower_minutes", low)))
            exp = float(activity.get("puzzle_expected_minutes", defaults.get("expected_minutes", exp)))
            high = float(activity.get("puzzle_upper_minutes", defaults.get("upper_minutes", high)))
        components.append({"type": cls, "method": "puzzle_authored"})

    elif cls == "inference_answer":
        facts = int(activity.get("facts_to_compare", 1))
        base = float(defaults.get("expected_minutes", 2)) + facts * 0.5
        low, exp, high = base * 0.8, base, base * 1.3
        components.append({"type": cls, "method": "inference_facts", "facts": facts})

    else:
        components.append({"type": cls, "method": "class_defaults"})

    return DurationEstimate(low, exp, high, components)


def sum_activities(
    activities: list[dict[str, Any]],
    assumptions: dict[str, Any],
    class_defaults: dict[str, Any],
) -> DurationEstimate:
    total = DurationEstimate(0, 0, 0, [])
    for act in activities:
        est = estimate_activity(act, assumptions, class_defaults)
        total.lower_minutes += est.lower_minutes
        total.expected_minutes += est.expected_minutes
        total.upper_minutes += est.upper_minutes
        total.components.extend(est.components)
    return total
