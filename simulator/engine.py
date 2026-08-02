"""Core simulation engine."""

from __future__ import annotations

import random
from typing import Any, Callable

from simulator.checks import apply_check_outcome, roll_check
from simulator.endings import evaluate_ending
from simulator.state import GameState


ChoiceFn = Callable[[GameState, list[dict[str, Any]], str], dict[str, Any]]


class SimulationEngine:
    def __init__(self, package: dict[str, Any], rng: random.Random):
        self.root = package["root"]
        self.adapter = package["adapter"]
        self.nodes = self.adapter["nodes"]
        self.checks = self.adapter.get("checks", {})
        self.rng = rng

    def new_state(self) -> GameState:
        st = GameState(
            node=self.adapter["start_node"],
            clock=self.adapter.get("start_clock", 1140),
        )
        st.visited.add(st.node)
        st.path.append(st.node)
        return st

    def enrich_options(self, options: list[dict[str, Any]]) -> list[dict[str, Any]]:
        enriched = []
        for o in options:
            tgt = o.get("target", "")
            spec = self.nodes.get(tgt, {})
            grants = list(spec.get("clues", []))
            if spec.get("check"):
                chk = self.checks.get(spec["check"], {})
                for branch in (chk.get("pass", {}), chk.get("fail", {})):
                    grants.extend(branch.get("clues", []))
            enriched.append({**o, "grants_clues": grants, "type": spec.get("type")})
        return enriched

    def advance_minutes(self, state: GameState, minutes: int, joint: bool = True) -> None:
        if minutes <= 0:
            return
        state.clock += minutes
        if joint:
            state.joint_minutes += minutes
        state.apply_thresholds(self.adapter)

    def apply_node_effects(self, state: GameState, spec: dict[str, Any], role: str | None) -> int:
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
        minutes = spec.get("minutes", 0) + extra
        if role:
            state.role_minutes[role] = state.role_minutes.get(role, 0) + minutes
        else:
            self.advance_minutes(state, minutes, joint=True)
        return minutes

    def run_role_path(
        self,
        state: GameState,
        start: str,
        sync: str,
        role: str,
        choose: ChoiceFn,
    ) -> GameState:
        local = state.clone()
        local.role_nodes[role] = start
        node = start
        depth = 0
        while node != sync and depth < 500:
            depth += 1
            spec = self.nodes[node]
            local.visited.add(node)
            local.path.append(f"{role}:{node}")

            gate = spec.get("gate")
            if gate:
                if gate.get("if_clock_gte") and local.clock >= gate["if_clock_gte"]:
                    if "skip_to" in gate:
                        node = gate["skip_to"]
                        if gate.get("alt_minutes"):
                            local.role_minutes[role] += gate["alt_minutes"]
                        for pc in gate.get("alt_partial", []):
                            local.grant_clue(pc)
                        continue
                if gate.get("requires_flag") and gate["requires_flag"] not in local.flags:
                    if gate.get("penalty_minutes"):
                        local.role_minutes[role] += gate["penalty_minutes"]
                        local.grant_flag("ACCESS_MANAGER_KEY")

            if spec.get("early_finish") and spec.get("sync") == sync:
                self.apply_node_effects(local, spec, role)
                break

            if "choices" in spec and spec.get("type") in ("people", "records", "hub"):
                options = self.enrich_options(spec["choices"])
                pick = choose(local, options, role)
                node = pick["target"]
                continue

            self.apply_node_effects(local, spec, role)

            if spec.get("type") == "ending":
                break

            nxt = spec.get("next")
            if nxt:
                node = nxt
                continue

            opts = spec.get("next_options", [])
            if opts:
                pick = choose(local, self.enrich_options([{"id": o, "target": o} for o in opts]), role)
                node = pick["target"]
                continue

            break

        return local

    def resolve_split(
        self,
        state: GameState,
        split_id: str,
        choose: ChoiceFn,
    ) -> GameState:
        sp = self.adapter["splits"][split_id]
        launch = sp["launch"]
        sync = sp["sync"]
        people = self.run_role_path(state, sp["people_start"], sync, "people", choose)
        records = self.run_role_path(state, sp["records_start"], sync, "records", choose)

        merged = state.clone()
        merged.clues |= people.clues | records.clues
        merged.flags |= people.flags | records.flags
        merged.role_minutes["people"] += people.role_minutes.get("people", 0)
        merged.role_minutes["records"] += records.role_minutes.get("records", 0)
        parallel = max(people.role_minutes.get("people", 0), records.role_minutes.get("records", 0))
        overhead = self.adapter.get("regroup_overhead_minutes", 5)
        merged.split_segments.append(
            {
                "split": split_id,
                "people_minutes": people.role_minutes.get("people", 0),
                "records_minutes": records.role_minutes.get("records", 0),
                "wall_minutes": parallel + overhead,
            }
        )
        self.advance_minutes(merged, parallel + overhead, joint=True)
        merged.node = sync
        merged.path.extend(people.path[-3:] + records.path[-3:])
        return merged

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
            if state.can_complete_infer(infer_id, self.adapter):
                state.infers_done.add(infer_id)
            elif infer_id == "I-01":
                bailout = self.adapter["infer_requirements"]["I-01"]
                if "C-06" not in state.clues:
                    self.advance_minutes(state, bailout.get("bailout_minutes", 15))
                    for c in bailout.get("bailout_grants", []):
                        state.grant_clue(c)
                if state.can_complete_infer(infer_id, self.adapter):
                    state.infers_done.add(infer_id)
            elif infer_id == "I-02":
                pass
            elif infer_id == "I-03":
                pass
            self.advance_minutes(state, spec.get("minutes", 0))
            if infer_id == "I-03" and not state.accused:
                state.accused = choose(state, [], "accuse").get("target")
            state.node = spec["next"]
            state.path.append(state.node)
            return state

        if ntype == "ending_dispatch":
            state.node = evaluate_ending(state, self.adapter)
            state.path.append(state.node)
            return state

        if ntype == "hub":
            options = []
            for ch in spec.get("choices", []):
                if ch.get("id") == "decline":
                    options.append(ch)
                    continue
                if state.clock >= self.adapter.get("deadline_clock", 1380):
                    continue
                options.append(ch)
            if not options:
                options = spec.get("choices", [])
            pick = choose(state, self.enrich_options(options), "joint")
            selected = pick
            for ch in spec.get("choices", []):
                if ch["target"] == pick.get("target"):
                    selected = ch
                    break
            if pick.get("id") == "decline" or selected.get("sets"):
                state.filed_without_accusation = True
            self.advance_minutes(state, selected.get("minutes", pick.get("minutes", 0)))
            state.node = pick["target"]
            state.path.append(state.node)
            return state

        if "choices" in spec:
            pick = choose(state, self.enrich_options(spec["choices"]), spec.get("role", "joint"))
            state.node = pick["target"]
            state.path.append(state.node)
            return state

        self.apply_node_effects(state, spec, spec.get("role"))
        nxt = spec.get("next")
        if nxt:
            state.node = nxt
            state.path.append(state.node)
        return state

    def run(
        self,
        choose: ChoiceFn,
        max_steps: int = 500,
    ) -> GameState:
        state = self.new_state()
        for _ in range(max_steps):
            spec = self.nodes.get(state.node, {})
            if spec.get("type") == "ending" or state.node.startswith("E-"):
                break
            state = self.step(state, choose)
            if state.node.startswith("E-"):
                break
        if not state.node.startswith("E-"):
            state.node = evaluate_ending(state, self.adapter)
        return state
