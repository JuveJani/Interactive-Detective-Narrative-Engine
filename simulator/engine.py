"""Core simulation engine."""

from __future__ import annotations

import random
from typing import Any, Callable

from simulator.checks import apply_check_outcome, roll_check
from simulator.config import SimConfig, DEFAULT_CONFIG
from simulator.follow_ups import apply_follow_up, eligible_follow_up_options
from simulator.endings import evaluate_ending
from simulator.state import GameState


class SimulationLimitError(Exception):
    """Raised when max_states or path limits are exceeded."""


ChoiceFn = Callable[[GameState, list[dict[str, Any]], str], dict[str, Any]]


def _path_node_ids(path: list[str]) -> set[str]:
    nodes: set[str] = set()
    for entry in path:
        nodes.add(entry.split(":")[-1] if ":" in entry else entry)
    return nodes


def _apply_partner_conditional_flags(
    merged: GameState,
    people: GameState,
    records: GameState,
    nodes: dict[str, Any],
) -> None:
    """Grant flags from partner_conditional_flags when partner lacks required state."""
    for role_path, partner_flags in (
        (_path_node_ids(people.path), records.flags),
        (_path_node_ids(records.path), people.flags),
    ):
        for nid in role_path:
            spec = nodes.get(nid, {})
            for rule in spec.get("partner_conditional_flags", []):
                flag = rule["flag"]
                when_lacks = rule.get("when_partner_lacks", flag)
                expected_partner = rule.get("partner_role", "records")
                partner_state = records.flags if expected_partner == "records" else people.flags
                if when_lacks not in partner_state and flag not in merged.flags:
                    merged.grant_flag(flag)


class SimulationEngine:
    def __init__(
        self,
        package: dict[str, Any],
        rng: random.Random,
        config: SimConfig = DEFAULT_CONFIG,
    ):
        self.root = package["root"]
        self.adapter = package["adapter"]
        self.nodes = self.adapter["nodes"]
        self.checks = self.adapter.get("checks", {})
        self.rng = rng
        self.config = config
        self.hub_targets = self._build_hub_targets()
        self.cost_policy = self.adapter.get("cost_policy", "hub_authoritative")
        self.follow_up_max = self.adapter.get("follow_up_max", 2)
        self._state_counter = 0

    def _build_hub_targets(self) -> dict[tuple[int | str, str], dict[str, Any]]:
        """Map (hub_id, destination node) -> hub choice metadata."""
        mapping: dict[tuple[int | str, str], dict[str, Any]] = {}
        for nid, spec in self.nodes.items():
            if spec.get("type") != "hub":
                continue
            hub_id = spec.get("hub_id", nid)
            for ch in spec.get("choices", []):
                mapping[(hub_id, ch["target"])] = {
                    "hub_id": hub_id,
                    "hub_node": nid,
                    "choice_id": ch.get("id", ""),
                    "minutes": ch.get("minutes", 0),
                    "additive_cost": ch.get("additive_cost", False),
                    "once_per_hub": ch.get("once_per_hub", False),
                }
        return mapping

    def _path_nodes(self, state: GameState) -> set[str]:
        nodes: set[str] = set()
        for p in state.path:
            nodes.add(p.split(":")[-1] if ":" in p else p)
        nodes.add(state.node)
        return nodes

    def _hub_target_meta(self, hub_id: int | str, target: str) -> dict[str, Any] | None:
        return self.hub_targets.get((hub_id, target))

    def _at_deadline(self, state: GameState) -> bool:
        return state.clock >= self.adapter.get("deadline_clock", 1380)

    def _tick_state_limit(self, state: GameState) -> None:
        self._state_counter += 1
        state.states_explored = self._state_counter
        if self._state_counter > self.config.max_states:
            raise SimulationLimitError(f"max_states exceeded ({self.config.max_states})")

    def new_state(self) -> GameState:
        st = GameState(
            node=self.adapter["start_node"],
            clock=self.adapter.get("start_clock", 1140),
        )
        st.visited.add(st.node)
        st.path.append(st.node)
        return st

    def public_options(self, options: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Expose only information legally visible before choosing."""
        public = []
        for o in options:
            public.append(
                {
                    "id": o.get("id", ""),
                    "target": o.get("target", ""),
                    "minutes": o.get("minutes", 0),
                    "label": o.get("label", o.get("id", "")),
                    "once_per_hub": o.get("once_per_hub", False),
                    "risky": o.get("id") in ("press", "boot", "duplicates", "whereabouts", "skim"),
                }
            )
        return public

    def hub_options(self, state: GameState, spec: dict[str, Any]) -> list[dict[str, Any]]:
        hub_id = spec.get("hub_id", state.node)
        used = state.hub_visits.get(hub_id, set())
        deadline = self.adapter.get("deadline_clock", 1380)
        at_deadline = state.clock >= deadline
        options = []
        for ch in spec.get("choices", []):
            if ch.get("once_per_hub") and ch.get("id") in used:
                continue
            if ch.get("id") == "decline":
                options.append(ch)
                continue
            if at_deadline:
                continue
            options.append(ch)
        if at_deadline:
            decline = [ch for ch in spec.get("choices", []) if ch.get("id") == "decline"]
            options = decline
        follow_opts = [] if at_deadline else eligible_follow_up_options(state, state.node, self.adapter)
        return self.public_options(options) + follow_opts

    def advance_minutes(self, state: GameState, minutes: int, joint: bool = True) -> None:
        if minutes <= 0:
            return
        deadline = self.adapter.get("deadline_clock", 1380)
        before = state.clock
        state.clock = min(state.clock + minutes, deadline)
        applied = state.clock - before
        if joint:
            state.joint_minutes += applied
        state.apply_thresholds(self.adapter)

    def apply_node_effects(
        self,
        state: GameState,
        spec: dict[str, Any],
        role: str | None,
        *,
        skip_entry_minutes: bool = False,
    ) -> int:
        extra = 0
        if "sets_clock" in spec:
            state.clock = spec["sets_clock"]
        for clue in spec.get("clues", []):
            state.grant_clue(clue)
        for flag in spec.get("flags", []):
            state.grant_flag(flag)
        if spec.get("check"):
            passed, roll = roll_check(
                self.rng,
                spec.get("role", role or "people"),
                self.checks[spec["check"]]["dc"],
            )
            state.rng_roll = roll
            extra += apply_check_outcome(state, spec["check"], passed, self.checks)
            if not passed:
                fail_spec = self.checks[spec["check"]].get("fail", {})
                state.grant_flag(f"CHECK_FAIL_{spec['check']}")
                follow = fail_spec.get("needs_followup")
                path_nodes = self._path_nodes(state)
                if follow and follow not in path_nodes:
                    state.pending_followup = follow
        minutes = spec.get("minutes", 0) + extra
        if skip_entry_minutes and not spec.get("additive_entry_cost"):
            minutes = extra
        if role:
            return minutes
        self.advance_minutes(state, minutes, joint=True)
        return minutes

    def _resolve_follow_up(self, state: GameState, node: str) -> int:
        return 0

    def run_role_path(
        self,
        state: GameState,
        start: str,
        sync: str,
        role: str,
        choose: ChoiceFn,
    ) -> tuple[GameState, int]:
        local = state.clone()
        local.role_minutes = {"people": 0, "records": 0}
        node = start
        window_minutes = 0
        depth = 0
        while node != sync and depth < self.config.max_path_steps:
            depth += 1
            spec = self.nodes[node]
            local.visited.add(node)
            local.path.append(f"{role}:{node}")

            if getattr(local, "pending_followup", None) == node:
                local.pending_followup = None

            if getattr(local, "pending_followup", None) and node != local.pending_followup:
                pending = local.pending_followup
                if pending in self.nodes:
                    node = pending
                    continue

            gate = spec.get("gate")
            if gate:
                if gate.get("if_clock_gte") and local.clock >= gate["if_clock_gte"]:
                    branch_choices = gate.get("branch_choices")
                    if branch_choices:
                        options = [
                            {
                                "id": c["id"],
                                "target": c.get("skip_to", node),
                                "minutes": c.get("minutes", 0),
                                "label": c.get("label", c["id"]),
                            }
                            for c in branch_choices
                        ]
                        pick = choose(local, self.public_options(options), role)
                        chosen = next(c for c in branch_choices if c["id"] == pick["id"])
                        node = chosen["skip_to"]
                        window_minutes += chosen.get("minutes", 0)
                        for pc in chosen.get("partial_clues", chosen.get("alt_partial", [])):
                            local.grant_clue(pc)
                        continue
                    if "skip_to" in gate:
                        node = gate["skip_to"]
                        if gate.get("alt_minutes"):
                            window_minutes += gate["alt_minutes"]
                        for pc in gate.get("alt_partial", []):
                            local.grant_clue(pc)
                        continue
                if gate.get("requires_flag") and gate["requires_flag"] not in local.flags:
                    if gate.get("penalty_minutes"):
                        window_minutes += gate["penalty_minutes"]
                        local.grant_flag("ACCESS_MANAGER_KEY")

            if spec.get("early_finish") and spec.get("sync") == sync:
                window_minutes += self.apply_node_effects(local, spec, role)
                break

            if "choices" in spec and spec.get("type") in ("people", "records"):
                if getattr(local, "pending_followup", None):
                    node = local.pending_followup
                    continue
                available = []
                for ch in spec.get("choices", []):
                    choice_key = (node, ch.get("id", ch["target"]))
                    if ch.get("once_per_role_path") and choice_key in local.role_choices_used:
                        continue
                    available.append(ch)
                if not available:
                    break
                options = self.public_options(available)
                pick = choose(local, options, role)
                choice_key = (node, pick.get("id", pick.get("target", "")))
                local.role_choices_used.add(choice_key)
                node = pick["target"]
                continue

            added = self.apply_node_effects(local, spec, role)
            window_minutes += added
            window_minutes += self._resolve_follow_up(local, node)

            if spec.get("type") == "ending":
                break

            nxt = spec.get("next")
            if nxt:
                node = nxt
                continue

            opts = spec.get("next_options", [])
            if opts:
                pick = choose(
                    local,
                    self.public_options([{"id": o, "target": o} for o in opts]),
                    role,
                )
                node = pick["target"]
                continue

            if getattr(local, "pending_followup", None):
                node = local.pending_followup
                continue

            break

        return local, window_minutes

    def resolve_split(
        self,
        state: GameState,
        split_id: str,
        choose: ChoiceFn,
    ) -> GameState:
        sp = self.adapter["splits"][split_id]
        sync = sp["sync"]
        people, people_window = self.run_role_path(state, sp["people_start"], sync, "people", choose)
        records, records_window = self.run_role_path(state, sp["records_start"], sync, "records", choose)

        merged = state.clone()
        merged.clues |= people.clues | records.clues
        merged.flags |= people.flags | records.flags
        _apply_partner_conditional_flags(merged, people, records, self.nodes)
        merged.hub_visits = {k: set(v) for k, v in state.hub_visits.items()}
        for hid, used in people.hub_visits.items():
            merged.hub_visits.setdefault(hid, set()).update(used)
        for hid, used in records.hub_visits.items():
            merged.hub_visits.setdefault(hid, set()).update(used)

        parallel = max(people_window, records_window)
        overhead = self.adapter.get("regroup_overhead_minutes", 5)
        merged.split_segments.append(
            {
                "split": split_id,
                "people_minutes": people_window,
                "records_minutes": records_window,
                "wall_minutes": parallel + overhead,
            }
        )
        merged.role_minutes["people"] = state.role_minutes.get("people", 0) + people_window
        merged.role_minutes["records"] = state.role_minutes.get("records", 0) + records_window
        self.advance_minutes(merged, parallel + overhead, joint=True)
        merged.node = sync
        merged.path.extend(people.path[-3:] + records.path[-3:])
        return merged

    def _complete_infer(self, state: GameState, infer_id: str) -> bool:
        if state.can_complete_infer(infer_id, self.adapter):
            state.infers_done.add(infer_id)
            return True
        if infer_id == "I-01":
            bailout = self.adapter["infer_requirements"]["I-01"]
            if "C-06" not in state.clues:
                self.advance_minutes(state, bailout.get("bailout_minutes", 15))
                for c in bailout.get("bailout_grants", []):
                    state.grant_clue(c)
            if state.can_complete_infer(infer_id, self.adapter):
                state.infers_done.add(infer_id)
                return True
        return False

    def step(self, state: GameState, choose: ChoiceFn) -> GameState:
        spec = self.nodes[state.node]
        ntype = spec.get("type")
        state.steps += 1

        if ntype == "split_launch":
            return self.resolve_split(state, spec["split"], choose)

        if ntype == "regroup":
            state.node = spec["next"]
            state.path.append(state.node)
            return state

        if ntype == "infer":
            infer_id = spec["infer"]
            if infer_id == "I-03":
                if not state.accused:
                    state.accused = choose(state, [], "accuse").get("target")
                self._complete_infer(state, infer_id)
            elif infer_id == "I-02":
                if not self._complete_infer(state, infer_id):
                    blocked_mins = spec.get("blocked_minutes")
                    if blocked_mins is not None:
                        self.advance_minutes(state, blocked_mins)
                    state.node = spec.get("blocked_return", "J-300")
                    state.path.append(f"{state.node}:blocked-I-02")
                    return state
            else:
                self._complete_infer(state, infer_id)
            self.advance_minutes(state, spec.get("minutes", 0))
            if infer_id != "I-02" or "I-02" in state.infers_done:
                state.node = spec["next"]
                state.path.append(state.node)
            return state

        if ntype == "ending_dispatch":
            state.node = evaluate_ending(state, self.adapter)
            state.path.append(state.node)
            return state

        if ntype == "hub":
            if self._at_deadline(state):
                state.node = "J-600"
                state.path.append("J-600:deadline")
                return state
            options = self.hub_options(state, spec)
            if not options:
                state.node = "J-600"
                state.path.append("J-600:deadline-no-options")
                return state
            pick = choose(state, options, "joint")
            if pick.get("type") == "follow_up" or pick.get("id", "").startswith("FU_"):
                minutes = apply_follow_up(state, pick["id"], self.adapter)
                self.advance_minutes(state, minutes)
                return state
            selected = pick
            for ch in spec.get("choices", []):
                if ch["target"] == pick.get("target") and ch.get("id") == pick.get("id"):
                    selected = ch
                    break
                if ch["target"] == pick.get("target"):
                    selected = ch
            hub_id = spec.get("hub_id", state.node)
            state.hub_visits.setdefault(hub_id, set()).add(selected.get("id", pick.get("id", "")))
            if pick.get("id") == "decline" or selected.get("sets"):
                state.filed_without_accusation = True
            self.advance_minutes(state, selected.get("minutes", pick.get("minutes", 0)))
            target = pick["target"]
            meta = self._hub_target_meta(hub_id, target)
            state.entry_cost_prepaid = (
                self.cost_policy == "hub_authoritative"
                and meta is not None
                and not selected.get("additive_cost", False)
            )
            if selected.get("once_per_hub") and hub_id != 1:
                state.return_hub = state.node
            else:
                state.return_hub = None
            state.node = target
            state.path.append(state.node)
            return state

        if "choices" in spec and spec.get("type") in ("people", "records"):
            pick = choose(state, self.public_options(spec["choices"]), spec.get("role", "joint"))
            state.node = pick["target"]
            state.path.append(state.node)
            return state

        skip = state.entry_cost_prepaid
        state.entry_cost_prepaid = False
        role = spec.get("role")
        added = self.apply_node_effects(state, spec, role, skip_entry_minutes=skip)
        if role:
            state.role_minutes[role] = state.role_minutes.get(role, 0) + added

        if state.return_hub and spec.get("next") and not spec.get("choices"):
            ret = state.return_hub
            state.return_hub = None
            state.node = ret
            state.path.append(ret)
            return state

        nxt = spec.get("next")
        if nxt:
            state.node = nxt
            state.path.append(state.node)
            return state

        opts = spec.get("next_options", [])
        if opts:
            pick = choose(
                state,
                self.public_options([{"id": o, "target": o} for o in opts]),
                "joint",
            )
            state.node = pick["target"]
            state.path.append(state.node)
        return state

    def run(
        self,
        choose: ChoiceFn,
        max_steps: int | None = None,
    ) -> GameState:
        limit = max_steps or self.config.max_path_steps
        state = self.new_state()
        for _ in range(limit):
            self._tick_state_limit(state)
            if self._at_deadline(state) and not state.node.startswith("E-"):
                if state.node != "J-600":
                    state.node = "J-600"
                    state.path.append("J-600:deadline-forced")
            spec = self.nodes.get(state.node, {})
            if spec.get("type") == "ending" or state.node.startswith("E-"):
                break
            state = self.step(state, choose)
            if state.node.startswith("E-"):
                break
        if not state.node.startswith("E-"):
            state.node = evaluate_ending(state, self.adapter)
        return state
