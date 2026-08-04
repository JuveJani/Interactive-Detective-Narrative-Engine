"""Wall-clock playtime estimation engine (Milestone 9)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from idne.playtime_activity import DurationEstimate, sum_activities


@dataclass
class PathEstimate:
    path_id: str
    path_type: str
    play_mode: str
    estimate: DurationEstimate
    in_world_minutes: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "path_id": self.path_id,
            "path_type": self.path_type,
            "play_mode": self.play_mode,
            "in_world_minutes": round(self.in_world_minutes, 2),
            **self.estimate.to_dict(),
        }


@dataclass
class TwoPlayerReport:
    joint_minutes: float
    split_max_sum_minutes: float
    regroup_minutes: float
    ending_minutes: float
    total_expected_minutes: float
    per_player_active: dict[str, float]
    per_player_waiting: dict[str, float]
    split_imbalance_minutes: float
    shared_time_minutes: float
    private_time_minutes: float
    incorrectly_summed_parallel: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "joint_minutes": round(self.joint_minutes, 2),
            "split_max_sum_minutes": round(self.split_max_sum_minutes, 2),
            "regroup_minutes": round(self.regroup_minutes, 2),
            "ending_minutes": round(self.ending_minutes, 2),
            "total_expected_minutes": round(self.total_expected_minutes, 2),
            "per_player_active": {k: round(v, 2) for k, v in self.per_player_active.items()},
            "per_player_waiting": {k: round(v, 2) for k, v in self.per_player_waiting.items()},
            "split_imbalance_minutes": round(self.split_imbalance_minutes, 2),
            "shared_time_minutes": round(self.shared_time_minutes, 2),
            "private_time_minutes": round(self.private_time_minutes, 2),
            "incorrectly_summed_parallel": self.incorrectly_summed_parallel,
        }


@dataclass
class PlaytimeEstimateResult:
    play_mode: str
    target_minutes: float
    paths: list[PathEstimate] = field(default_factory=list)
    two_player: TwoPlayerReport | None = None
    in_world_total_minutes: float = 0.0
    wall_clock_median_minutes: float = 0.0
    wall_clock_shortest_minutes: float = 0.0
    wall_clock_longest_minutes: float = 0.0
    mutually_exclusive_summed: bool = False
    exhaustive_content_minutes: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "play_mode": self.play_mode,
            "target_minutes": self.target_minutes,
            "wall_clock_median_minutes": round(self.wall_clock_median_minutes, 2),
            "wall_clock_shortest_minutes": round(self.wall_clock_shortest_minutes, 2),
            "wall_clock_longest_minutes": round(self.wall_clock_longest_minutes, 2),
            "in_world_total_minutes": round(self.in_world_total_minutes, 2),
            "mutually_exclusive_summed": self.mutually_exclusive_summed,
            "exhaustive_content_minutes": round(self.exhaustive_content_minutes, 2),
            "paths": [p.to_dict() for p in self.paths],
            "two_player": self.two_player.to_dict() if self.two_player else None,
        }


def estimate_two_player(
    package: dict[str, Any],
    assumptions: dict[str, Any],
    class_defaults: dict[str, Any],
) -> TwoPlayerReport:
    tp = package.get("two_player_model", {}) or {}
    joint = sum_activities(tp.get("joint_activities", []) or [], assumptions, class_defaults)
    regroup = sum_activities(tp.get("regroup_activities", []) or [], assumptions, class_defaults)
    ending = sum_activities(tp.get("ending_activities", []) or [], assumptions, class_defaults)

    split_max_sum = 0.0
    per_active: dict[str, float] = {"player_1": 0.0, "player_2": 0.0}
    per_waiting: dict[str, float] = {"player_1": 0.0, "player_2": 0.0}
    max_imbalance = 0.0

    for window in tp.get("split_windows", []) or []:
        branches = window.get("branches", []) or []
        branch_estimates = []
        for br in branches:
            est = sum_activities(br.get("activities", []) or [], assumptions, class_defaults)
            branch_estimates.append((br.get("player_id", ""), est.expected_minutes))
        if branch_estimates:
            max_branch = max(e for _, e in branch_estimates)
            split_max_sum += max_branch
            for pid, e in branch_estimates:
                if pid:
                    per_active[pid] = per_active.get(pid, 0) + e
            if len(branch_estimates) >= 2:
                times = [e for _, e in branch_estimates]
                imbalance = max(times) - min(times)
                max_imbalance = max(max_imbalance, imbalance)
                for pid, e in branch_estimates:
                    wait = max_branch - e
                    if wait > 0 and pid:
                        per_waiting[pid] = per_waiting.get(pid, 0) + wait

    incorrect_sum = float(tp.get("incorrect_parallel_sum_minutes", 0))
    total_correct = (
        joint.expected_minutes + split_max_sum + regroup.expected_minutes + ending.expected_minutes
    )
    incorrectly_summed = bool(tp.get("incorrectly_summed_parallel", False))

    shared = joint.expected_minutes + regroup.expected_minutes
    private = split_max_sum

    return TwoPlayerReport(
        joint_minutes=joint.expected_minutes,
        split_max_sum_minutes=split_max_sum,
        regroup_minutes=regroup.expected_minutes,
        ending_minutes=ending.expected_minutes,
        total_expected_minutes=incorrect_sum if incorrectly_summed else total_correct,
        per_player_active=per_active,
        per_player_waiting=per_waiting,
        split_imbalance_minutes=max_imbalance,
        shared_time_minutes=shared,
        private_time_minutes=private,
        incorrectly_summed_parallel=incorrectly_summed,
    )


def estimate_playtime(package: dict[str, Any]) -> PlaytimeEstimateResult:
    assumptions = package.get("reading_assumptions", {}) or {}
    class_defaults = package.get("activity_class_defaults", {}) or {}
    target = float(package.get("target_playtime_minutes", 0))
    play_modes = package.get("play_modes", []) or []
    play_mode = "two_player" if "two_player" in play_modes and package.get("primary_estimate_mode") == "two_player" else (
        "single_investigator" if "single_investigator" in play_modes else play_modes[0] if play_modes else "single_investigator"
    )

    if "two_player" in play_modes and package.get("estimate_two_player"):
        play_mode = "two_player"

    result = PlaytimeEstimateResult(play_mode=play_mode, target_minutes=target)

    in_world = package.get("in_world_time", {}) or {}
    result.in_world_total_minutes = float(in_world.get("total_available_minutes", 0))

    path_estimates: list[PathEstimate] = []
    for path in package.get("wall_clock_paths", []) or []:
        if path.get("mutually_exclusive") and path.get("summed_with_other_paths"):
            result.mutually_exclusive_summed = True
        acts = path.get("activities", []) or []
        est = sum_activities(acts, assumptions, class_defaults)
        path_estimates.append(
            PathEstimate(
                path_id=str(path.get("path_id", "")),
                path_type=str(path.get("path_type", "")),
                play_mode=str(path.get("play_mode", play_mode)),
                estimate=est,
                in_world_minutes=float(path.get("in_world_minutes", 0)),
            )
        )

    result.paths = path_estimates
    expected_values = [p.estimate.expected_minutes for p in path_estimates if not package.get("wall_clock_paths", []) or not next(
        (x for x in package.get("wall_clock_paths", []) if x.get("path_id") == p.path_id and x.get("mutually_exclusive")), None
    )]
    if path_estimates:
        result.wall_clock_shortest_minutes = min(p.estimate.expected_minutes for p in path_estimates)
        result.wall_clock_longest_minutes = max(p.estimate.expected_minutes for p in path_estimates)
        median_path = next(
            (p for p in path_estimates if p.path_type == "median_expected"),
            path_estimates[len(path_estimates) // 2],
        )
        result.wall_clock_median_minutes = median_path.estimate.expected_minutes

    exhaustive = package.get("coverage_assumptions", {}) or {}
    if exhaustive.get("exhaustive_content_minutes"):
        result.exhaustive_content_minutes = float(exhaustive["exhaustive_content_minutes"])

    if play_mode == "two_player" or package.get("two_player_model"):
        result.two_player = estimate_two_player(package, assumptions, class_defaults)
        if result.two_player:
            result.wall_clock_median_minutes = result.two_player.total_expected_minutes

    return result
