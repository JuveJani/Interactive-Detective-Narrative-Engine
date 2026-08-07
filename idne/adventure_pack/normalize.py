"""Normalize adventure pack spec content into validator-compliant canonical packages."""

from __future__ import annotations

from typing import Any

from idne.adventure_pack.spec import AdventurePackSpec

CAPABILITY_CATEGORY_MAP = {
    "reasoning_analysis": "reasoning_interpretation",
    "reasoning_interpretation": "reasoning_interpretation",
    "technical_systems": "technical_operation",
    "technical_operation": "technical_operation",
    "perception_observation": "perception_observation",
}

CAPABILITY_ACTION_TYPE = {
    "reasoning_interpretation": "interpret",
    "technical_operation": "operate",
    "perception_observation": "search",
}

NPC_STATIC_DEFAULTS = {
    "motivation": "Protect personal interests during the investigation",
    "honesty": 0.55,
    "deception": 0.35,
    "manipulation": 0.25,
    "loyalty": "employer",
    "fear": "disciplinary_action",
}


def normalize_locations(spec: AdventurePackSpec) -> list[dict[str, Any]]:
    timeline = spec.fixed_truth.get("causal_timeline") or {}
    events = timeline.get("events") or []
    loc_events: dict[str, list[str]] = {}
    for evt in events:
        eid = evt.get("event_id")
        loc = evt.get("location_id")
        if eid and loc:
            loc_events.setdefault(str(loc), []).append(str(eid))

    out: list[dict[str, Any]] = []
    for loc in spec.locations:
        entry = dict(loc)
        loc_id = str(entry["location_id"])
        if not entry.get("world_first_provenance"):
            event_ids = loc_events.get(loc_id, [])
            if event_ids:
                entry["world_first_provenance"] = {"event_ids": event_ids, "fact_ids": []}
            else:
                entry["world_first_provenance"] = {
                    "event_ids": [],
                    "fact_ids": [],
                    "explicit_adventure_extension": True,
                }
        entry.setdefault("state_owner", "environment_package")
        out.append(entry)
    return out


def normalize_navigation(spec: AdventurePackSpec) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for edge in spec.navigation:
        if edge.get("source_location_id") and edge.get("player_label"):
            out.append(dict(edge))
            continue
        out.append(
            {
                "nav_id": edge.get("nav_id") or edge.get("edge_id"),
                "source_location_id": edge.get("source_location_id") or edge.get("from_location_id"),
                "destination_location_id": edge.get("destination_location_id") or edge.get("to_location_id"),
                "player_label": edge.get("player_label") or edge.get("direction_label") or "Travel.",
                "travel_cost_minutes": edge.get("travel_cost_minutes", 2),
                "access_condition": edge.get("access_condition") or {"type": "always"},
                "return_nav_id": edge.get("return_nav_id"),
                "hidden_destination_id": edge.get("hidden_destination_id"),
            }
        )
    return out


def normalize_mandatory_locations(spec: AdventurePackSpec) -> list[dict[str, Any]]:
    raw = spec.raw.get("mandatory_locations")
    if raw:
        return list(raw)
    return [
        {
            "location_id": loc["location_id"],
            "access": "reachable",
            "reason": loc.get("reason") or "investigation",
        }
        for loc in spec.locations
    ]


def normalize_objects(spec: AdventurePackSpec) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for obj in spec.objects:
        parent = obj.get("parent_id") or obj.get("location_id")
        entry = {
            "object_id": obj["object_id"],
            "parent_id": parent,
            "parent_type": obj.get("parent_type", "location"),
            "public_name": obj.get("public_name") or obj["object_id"],
            "object_type": obj.get("object_type") or obj.get("interaction_type") or "interactive_object",
            "initial_state": obj.get("initial_state", "available"),
            "current_state": obj.get("current_state", "available"),
            "visible_description": obj.get("visible_description") or f"DESC-{obj['object_id']}",
            "visibility_requirement": obj.get("visibility_requirement", "on_arrival"),
            "interaction_depth_required": obj.get("interaction_depth_required", "approached"),
        }
        if obj.get("provenance"):
            entry["provenance"] = obj["provenance"]
        if obj.get("world_first_source_event"):
            entry["world_first_source_event"] = obj["world_first_source_event"]
        out.append(entry)
    return out


def _object_name(spec: AdventurePackSpec, object_id: str) -> str:
    for obj in spec.objects:
        if obj["object_id"] == object_id:
            return str(obj.get("public_name") or object_id)
    return object_id


def normalize_object_actions(spec: AdventurePackSpec) -> list[dict[str, Any]]:
    check_by_parent: dict[str, dict[str, Any]] = {}
    for chk in spec.checks:
        pid = chk.get("parent_action_id")
        if pid:
            check_by_parent[str(pid)] = chk

    out: list[dict[str, Any]] = []
    for action in spec.object_actions:
        action_id = str(action["action_id"])
        object_id = str(action["object_id"])
        chk = check_by_parent.get(action_id)
        label = action.get("player_label") or action.get("player_action_label")
        if not label and chk:
            label = chk.get("player_action_label")
        if not label:
            label = f"Examine {_object_name(spec, object_id)}."

        entry: dict[str, Any] = {
            "action_id": action_id,
            "object_id": object_id,
            "player_label": label,
            "interaction_depth": action.get("interaction_depth", "examined"),
            "time_cost_minutes": action.get("time_cost_minutes", 2),
            "cost_applied_once": action.get("cost_applied_once", True),
            "eligibility": action.get("eligibility") or {"type": "always"},
        }

        if chk:
            entry["check_binding"] = {
                "check_id": chk["check_id"],
                "success_destination": chk["success_unit_id"],
                "failure_destination": chk["failure_unit_id"],
                "one_attempt": True,
                "information_on_success": chk.get("success_grants_knowledge_ids") or [],
            }
            entry["destination_unit"] = chk["declaration_unit_id"]
        else:
            dest = (
                action.get("destination_unit")
                or action.get("menu_unit_id")
                or action.get("result_unit_id")
            )
            if dest:
                entry["destination_unit"] = dest
            if action.get("return_destination"):
                entry["return_destination"] = action["return_destination"]
                entry["requires_return"] = action.get("requires_return", True)
        out.append(entry)
    return out


def _knowledge_by_id(spec: AdventurePackSpec) -> dict[str, dict[str, Any]]:
    return {k["knowledge_id"]: k for k in spec.knowledge.get("knowledge_items") or [] if k.get("knowledge_id")}


def _testimony_by_knowledge(spec: AdventurePackSpec) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for t in spec.knowledge.get("testimony") or []:
        kid = t.get("grants_knowledge_id")
        if kid:
            out[str(kid)] = t
    return out


def _observation_by_knowledge(spec: AdventurePackSpec) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for obs in spec.knowledge.get("observations") or []:
        kid = obs.get("establishes_knowledge_id")
        if kid:
            out[str(kid)] = obs
    return out


def _action_for_object(spec: AdventurePackSpec, object_id: str) -> str | None:
    for action in spec.object_actions:
        if action.get("object_id") == object_id:
            return str(action["action_id"])
    return None


def normalize_investigation_core(spec: AdventurePackSpec) -> dict[str, Any]:
    k = spec.knowledge
    knowledge_items = list(k.get("knowledge_items") or [])
    testimony_raw = list(k.get("testimony") or [])
    evidence_raw = list(k.get("evidence") or [])
    observations_raw = list(k.get("observations") or [])
    hypotheses_raw = list(k.get("hypotheses") or [])
    conclusions_raw = list(k.get("conclusions") or [])
    proofs_raw = list(k.get("proofs") or [])
    facts = list(k.get("facts") or [])

    testimony_by_k = _testimony_by_knowledge(spec)
    obs_by_k = _observation_by_knowledge(spec)
    knowledge_by_id = _knowledge_by_id(spec)

    # Evidence with provenance
    evidence: list[dict[str, Any]] = []
    evidence_to_object = {e["evidence_id"]: e for e in evidence_raw}
    for ev in evidence_raw:
        eid = ev["evidence_id"]
        fact_ids = []
        for item in knowledge_items:
            if eid.replace("EVD-", "") in item.get("knowledge_id", "") or ev.get("location_id"):
                fact_ids.extend(item.get("establishes_fact_ids") or [])
        fact_id = (fact_ids[0] if fact_ids else None) or f"FACT-{eid.split('-', 1)[-1]}"
        evidence.append(
            {
                "evidence_id": eid,
                "description": ev.get("description") or ev.get("name") or eid,
                "evidence_type": ev.get("evidence_type", "document"),
                "provenance": ev.get("provenance")
                or {"world_fact_id": fact_id, "source_event_id": ev.get("source_event_id")},
                "establishes_knowledge_ids": ev.get("establishes_knowledge_ids") or [],
            }
        )

    # Testimony normalized
    testimony: list[dict[str, Any]] = []
    for t in testimony_raw:
        kid = t.get("grants_knowledge_id")
        testimony.append(
            {
                "testimony_id": t["testimony_id"],
                "source_npc_id": t.get("source_npc_id") or t.get("npc_id"),
                "content_knowledge_id": t.get("content_knowledge_id") or kid,
                "topic_id": t.get("topic_id"),
                "dialogue_system": t.get("dialogue_system", False),
            }
        )

    # Observations with acquisition
    observations: list[dict[str, Any]] = []
    for obs in observations_raw:
        kid = obs.get("establishes_knowledge_id")
        obj_id = None
        action_id = None
        for ev in evidence_raw:
            if ev.get("establishes_knowledge_id") == kid or kid in (ev.get("establishes_knowledge_ids") or []):
                loc = ev.get("location_id")
                for obj in spec.objects:
                    if obj.get("location_id") == loc:
                        obj_id = obj["object_id"]
                        action_id = _action_for_object(spec, obj_id)
                        break
        entry = {
            "observation_id": obs["observation_id"],
            "description": obs.get("description") or obs["observation_id"],
            "location_id": obs.get("location_id"),
            "acquisition": obs.get("acquisition")
            or {
                "via": "object_interaction",
                "action_id": action_id or f"ACT-{obs['observation_id']}",
                "object_id": obj_id,
                "interaction_required": True,
            },
        }
        observations.append(entry)

    # Hypotheses
    hypotheses: list[dict[str, Any]] = []
    hyp_yields: dict[str, str] = {
        "HYP-DEPARTURE-FALSE": "KNOW-DEPARTURE-IMPOSSIBLE",
        "HYP-GALLERY-FALL": "KNOW-GALLERY-FALL",
        "HYP-TOM-COVERUP": "KNOW-TOM-COVERUP",
        "HYP-PERFECT-RECON": "KNOW-PERFECT-RECON",
    }
    for hyp in hypotheses_raw:
        hid = hyp["hypothesis_id"]
        hypotheses.append(
            {
                "hypothesis_id": hid,
                "statement": hyp.get("statement") or hid,
                "requires_knowledge_ids": hyp.get("requires_knowledge_ids")
                or hyp.get("related_knowledge_ids")
                or [],
                "yields_knowledge_id": hyp.get("yields_knowledge_id") or hyp_yields.get(hid),
                "player_synthesis_required": hyp.get("player_synthesis_required", True),
            }
        )

    # Knowledge with acquisition blocks
    knowledge: list[dict[str, Any]] = []
    proof_knowledge: set[str] = set()
    for proof in proofs_raw:
        proof_knowledge.update(proof.get("required_knowledge_ids") or [])

    for item in knowledge_items:
        kid = item["knowledge_id"]
        entry = {
            "knowledge_id": kid,
            "statement": item.get("statement") or item.get("summary") or kid,
            "category": item.get("category") or item.get("source_type") or "investigation",
        }
        if item.get("establishes_fact_ids"):
            entry["establishes_fact_ids"] = item["establishes_fact_ids"]

        if item.get("acquisition"):
            entry["acquisition"] = item["acquisition"]
        elif kid in obs_by_k:
            entry["acquisition"] = {
                "source_type": "observation",
                "source_id": obs_by_k[kid]["observation_id"],
                "interaction_required": True,
            }
        elif kid in testimony_by_k:
            entry["acquisition"] = {
                "source_type": "testimony",
                "source_id": testimony_by_k[kid]["testimony_id"],
            }
            if kid not in proof_knowledge:
                entry["optional_flavour"] = True
        elif item.get("source_type") == "briefing" or kid.startswith("KNOW-OPEN-"):
            entry["acquisition"] = {
                "source_type": "world_fact",
                "source_id": (item.get("establishes_fact_ids") or ["FACT-001"])[0]
                if item.get("establishes_fact_ids")
                else "FACT-001",
            }
            entry["optional_flavour"] = True
        elif item.get("source_type") == "inference":
            for hyp in hypotheses:
                if hyp.get("yields_knowledge_id") == kid:
                    entry["acquisition"] = {
                        "source_type": "synthesis",
                        "source_id": hyp["hypothesis_id"],
                        "interaction_required": True,
                    }
                    break
            else:
                entry["acquisition"] = {
                    "source_type": "synthesis",
                    "source_id": "HYP-PERFECT-RECON",
                    "interaction_required": True,
                }
        elif item.get("source_type") in ("document", "physical"):
            obs_id = obs_by_k.get(kid, {}).get("observation_id")
            if obs_id:
                entry["acquisition"] = {
                    "source_type": "observation",
                    "source_id": obs_id,
                    "interaction_required": True,
                }
            else:
                ev_match = next(
                    (e for e in evidence if kid in (e.get("establishes_knowledge_ids") or [])),
                    None,
                )
                if not ev_match and evidence_raw:
                    ev_id = evidence_raw[0]["evidence_id"]
                else:
                    ev_id = ev_match["evidence_id"] if ev_match else f"EVD-{kid.replace('KNOW-', '')}"
                entry["acquisition"] = {
                    "source_type": "physical_evidence",
                    "source_id": ev_id,
                    "interaction_required": True,
                }
        else:
            entry["acquisition"] = {
                "source_type": "world_fact",
                "source_id": (item.get("establishes_fact_ids") or ["FACT-001"])[0],
            }
            if kid not in proof_knowledge:
                entry["optional_flavour"] = True

        knowledge.append(entry)

    # Conclusions
    category_map = {
        "CONC-WHO": "culprit",
        "CONC-WHAT": "incident",
        "CONC-HOW": "method",
        "CONC-WHEN": "timeline",
    }
    question_map = {
        "CONC-WHO": "Q-WHO",
        "CONC-WHAT": "Q-WHAT",
        "CONC-HOW": "Q-HOW",
        "CONC-WHEN": "Q-WHEN",
    }
    conclusions: list[dict[str, Any]] = []
    for conc in conclusions_raw:
        cid = conc["conclusion_id"]
        entry = {
            "conclusion_id": cid,
            "category": conc.get("category") or category_map.get(cid, "incident"),
            "question_ref": conc.get("question_ref") or question_map.get(cid),
            "investigation_driven_by_clue": conc.get("investigation_driven_by_clue", False),
        }
        if conc.get("answer_entity_id") or (conc.get("correct_answer", "").startswith("NPC-")):
            entry["answer_entity_id"] = conc.get("answer_entity_id") or conc.get("correct_answer")
        else:
            entry["answer_text"] = conc.get("answer_text") or conc.get("correct_answer")
        conclusions.append(entry)

    # Proofs — ensure every conclusion has at least one proof
    proofs: list[dict[str, Any]] = list(proofs_raw)
    proofs_by_conc = {p["conclusion_id"]: p for p in proofs}
    proof_templates = {
        "CONC-WHO": ["KNOW-TOM-COVERUP", "KNOW-PERFECT-RECON", "KNOW-DEPARTURE-IMPOSSIBLE"],
        "CONC-WHAT": ["KNOW-GALLERY-FALL", "KNOW-RAIL-DAMAGE", "KNOW-LOG-LENS-ENTRY"],
        "CONC-HOW": ["KNOW-TOM-COVERUP", "KNOW-LOG-DEPARTURE-LINE", "KNOW-RADIO-DEPARTURE"],
        "CONC-WHEN": ["KNOW-GALLERY-FALL", "KNOW-LOG-LENS-ENTRY", "KNOW-RADIO-DEPARTURE"],
    }
    for conc in conclusions:
        cid = conc["conclusion_id"]
        if cid not in proofs_by_conc:
            proofs.append(
                {
                    "proof_id": f"PROOF-{cid.split('-', 1)[-1]}",
                    "conclusion_id": cid,
                    "required_knowledge_ids": proof_templates.get(cid, ["KNOW-PERFECT-RECON"]),
                }
            )

    # Relationships between knowledge (drop NPC entity relationships)
    relationships: list[dict[str, Any]] = []
    for rel in k.get("relationships") or []:
        if rel.get("type") in ("supports", "contradicts", "derives_from", "same_source", "independent_of", "requires"):
            relationships.append(dict(rel))
            continue
        from_id = rel.get("from_id") or rel.get("from_entity")
        to_id = rel.get("to_id") or rel.get("to_entity")
        if from_id and to_id and str(from_id).startswith("KNOW-") and str(to_id).startswith("KNOW-"):
            relationships.append(
                {
                    "relationship_id": rel.get("relationship_id", f"REL-{from_id}-{to_id}"),
                    "type": rel.get("type", "supports"),
                    "from_id": from_id,
                    "to_id": to_id,
                }
            )

    return {
        "world_facts": facts,
        "observations": observations,
        "physical_evidence": evidence,
        "testimony": testimony,
        "knowledge": knowledge,
        "hypotheses": hypotheses,
        "conclusions": conclusions,
        "proofs": proofs,
        "relationships": relationships,
        "optional_knowledge": list(k.get("optional_knowledge") or []),
    }


def normalize_npcs(spec: AdventurePackSpec) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for npc in spec.npcs:
        entry = dict(npc)
        static = dict(entry.get("static_properties") or {})
        for key, default in NPC_STATIC_DEFAULTS.items():
            static.setdefault(key, default)
        entry["static_properties"] = static
        dynamic = dict(entry.get("initial_dynamic_state") or {})
        dynamic.setdefault("trust", 50)
        dynamic.setdefault("information_known", entry.get("information_known") or [])
        dynamic.setdefault("revealed_topics", [])
        dynamic.setdefault("suspicion", 30)
        dynamic.setdefault("pressure", 40)
        entry["initial_dynamic_state"] = dynamic
        out.append(entry)
    return out


def normalize_topics(spec: AdventurePackSpec) -> list[dict[str, Any]]:
    topics: list[dict[str, Any]] = []
    for conv in spec.conversations:
        npc_id = conv.get("npc_id")
        for topic in conv.get("topics") or []:
            unlock = topic.get("unlock_conditions")
            if not unlock:
                unlock = [{"type": "trust_threshold", "npc_id": npc_id, "min": 0}]
            topics.append(
                {
                    "topic_id": topic["topic_id"],
                    "unlock_conditions": unlock,
                }
            )
    return topics


def normalize_conversation_graph(spec: AdventurePackSpec) -> list[dict[str, Any]]:
    graphs: list[dict[str, Any]] = []
    for conv in spec.conversations:
        npc_id = conv.get("npc_id")
        nodes = []
        for i, topic in enumerate(conv.get("topics") or []):
            nodes.append(
                {
                    "node_id": topic.get("node_id") or f"CN-{topic['topic_id']}",
                    "player_label": topic.get("player_label") or topic.get("player_prompt") or "Ask a question.",
                    "npc_response_unit": topic.get("npc_response_unit") or topic.get("response_unit_id"),
                    "grants_knowledge_id": topic.get("grants_knowledge_id"),
                    "topic_id": topic.get("topic_id"),
                    "time_cost_minutes": topic.get("time_cost_minutes", 2),
                    "unlock_conditions": topic.get("unlock_conditions")
                    or [{"type": "trust_threshold", "npc_id": npc_id, "min": 0}],
                }
            )
        graphs.append(
            {
                "conversation_id": conv.get("conversation_id", f"CONV-{npc_id}"),
                "npc_id": npc_id,
                "entry_topic_id": (conv.get("topics") or [{}])[0].get("topic_id"),
                "route_conditions": conv.get("route_conditions")
                or [{"type": "trust", "npc_id": npc_id, "min": 0}],
                "hub_unit_id": conv.get("hub_unit_id"),
                "nodes": nodes,
            }
        )
    return graphs


def normalize_info_known_model(spec: AdventurePackSpec) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for conv in spec.conversations:
        npc_id = conv.get("npc_id")
        for topic in conv.get("topics") or []:
            kid = topic.get("grants_knowledge_id")
            if kid:
                out.append(
                    {
                        "info_id": f"INFO-{topic['topic_id']}",
                        "npc_id": npc_id,
                        "knowledge_id": kid,
                        "topic_id": topic["topic_id"],
                    }
                )
    return out


def normalize_flow(spec: AdventurePackSpec) -> dict[str, Any]:
    flow = dict(spec.flow)
    flow.setdefault("schema_version", "1.0")
    flow.setdefault("adventure_id", spec.pack_id)

    endings = []
    for ending in flow.get("endings") or []:
        e = dict(ending)
        if e.get("ending_id") == "END-TIMEOUT" or e.get("ending_type") == "timeout":
            e["ending_type"] = "deadline"
            e["reveals_full_truth"] = False
            e["truth_reveal_scope"] = "none"
            trigger = dict(e.get("trigger") or {})
            trigger["type"] = "deadline_expired"
            e["trigger"] = trigger
        elif e.get("ending_type") == "perfect":
            e.setdefault("reveals_full_truth", True)
            e.setdefault("truth_reveal_scope", "complete")
        elif e.get("ending_type") == "partial":
            e.setdefault("reveals_full_truth", False)
            e.setdefault("truth_reveal_scope", "partial")
        endings.append(e)
    flow["endings"] = endings

    ending_ids = [e["ending_id"] for e in endings]
    flow["ending_graph"] = flow.get("ending_graph") or {
        "nodes": ending_ids,
        "evaluation_order": sorted(ending_ids, key=lambda x: next(
            (e.get("priority", 0) for e in endings if e["ending_id"] == x), 0
        ), reverse=True),
    }
    return flow


def build_result_units(spec: AdventurePackSpec) -> list[dict[str, Any]]:
    """Build object_interaction result_units registry for check and menu destinations."""
    units: dict[str, dict[str, Any]] = {}
    for unit in spec.units:
        uid = unit.get("unit_id")
        if not uid:
            continue
        if uid.endswith("-BASE"):
            units[uid] = {"unit_id": uid, "return_destination": uid}
            continue
        choices = unit.get("choices") or []
        if choices:
            ret = choices[0].get("destination_unit_id")
            entry: dict[str, Any] = {"unit_id": uid}
            if ret:
                entry["return_destination"] = ret
                entry["requires_return"] = True
            units[uid] = entry

    for chk in spec.checks:
        for key in ("declaration_unit_id", "success_unit_id", "failure_unit_id"):
            uid = chk.get(key)
            if not uid or uid in units:
                continue
            unit = spec.unit_by_id.get(uid, {})
            ret = None
            for choice in unit.get("choices") or []:
                ret = choice.get("destination_unit_id")
                if ret:
                    break
            entry = {"unit_id": uid}
            if ret:
                entry["return_destination"] = ret
                if key != "declaration_unit_id":
                    entry["requires_return"] = True
            if key == "failure_unit_id":
                entry["hints_missed_content"] = False
            units[uid] = entry

    for action in spec.object_actions:
        menu = action.get("menu_unit_id") or action.get("destination_unit")
        if menu and menu not in units:
            units[menu] = {"unit_id": menu, "requires_return": True}

    return list(units.values())


def normalize_checks(spec: AdventurePackSpec) -> list[dict[str, Any]]:
    knowledge_by_id = _knowledge_by_id(spec)
    out: list[dict[str, Any]] = []
    for chk in spec.checks:
        cat = CAPABILITY_CATEGORY_MAP.get(
            chk.get("capability_category") or "",
            chk.get("capability_category") or "perception_observation",
        )
        action_type = CAPABILITY_ACTION_TYPE.get(cat, "search")
        entry = dict(chk)
        entry["capability_category"] = cat
        entry["parent_action_type"] = chk.get("parent_action_type") or action_type
        grants = chk.get("success_grants_knowledge_ids") or []
        if grants and not entry.get("information_trace"):
            kid = grants[0]
            item = knowledge_by_id.get(kid, {})
            fact = (item.get("establishes_fact_ids") or ["FACT-001"])[0]
            entry["information_trace"] = {
                "fixed_truth_ref": fact,
                "source_id": chk.get("parent_action_id", "").replace("ACT-", "OBJ-"),
            }
        out.append(entry)
    return out
