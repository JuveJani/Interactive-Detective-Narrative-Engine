"""Investigation Core validation (Milestone 5A)."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

ALLOWED_RELATIONSHIP_TYPES = frozenset(
    {
        "supports",
        "contradicts",
        "derives_from",
        "same_source",
        "independent_of",
        "requires",
    }
)
KNOWLEDGE_SOURCES = frozenset(
    {
        "observation",
        "physical_evidence",
        "testimony",
        "hypothesis",
        "world_fact",
        "synthesis",
    }
)


@dataclass
class ValidationResult:
    adventure_root: Path
    status: str
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    checks: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "adventure_root": str(self.adventure_root),
            "status": self.status,
            "errors": self.errors,
            "warnings": self.warnings,
            "checks": self.checks,
        }


def load_investigation_manifest(root: Path) -> dict[str, Any] | None:
    for name in ("investigation_manifest.json", "INVESTIGATION_MANIFEST.json"):
        path = root / name
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    gen = root / "generation_manifest.json"
    if gen.exists():
        data = json.loads(gen.read_text(encoding="utf-8"))
        inv = data.get("investigation_core")
        if isinstance(inv, dict) and inv.get("enabled"):
            return {
                "schema_version": data.get("schema_version", "1.0"),
                "investigation_method": "canonical",
                "package_path": inv.get(
                    "package_path", "DO_NOT_READ/investigation_core_package.json"
                ),
            }
    return None


def load_package(root: Path, manifest: dict[str, Any]) -> dict[str, Any] | None:
    rel = manifest.get("package_path", "DO_NOT_READ/investigation_core_package.json")
    path = root / rel
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _index_by_id(items: list[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for item in items:
        iid = item.get(key)
        if iid:
            out[str(iid)] = item
    return out


def validate_investigation_core(adventure_root: str | Path) -> ValidationResult:
    root = Path(adventure_root).resolve()
    result = ValidationResult(adventure_root=root, status="PASS")

    manifest = load_investigation_manifest(root)
    if not manifest:
        result.status = "SKIP"
        result.warnings.append("no investigation_manifest — Investigation Core not declared")
        return result

    if manifest.get("investigation_method") != "canonical":
        result.status = "SKIP"
        result.warnings.append("investigation_method not canonical")
        return result

    package = load_package(root, manifest)
    if not package:
        result.status = "FAIL"
        result.errors.append("investigation_core_package missing")
        result.checks["INV-PKG-PRESENT"] = "FAIL"
        return result
    result.checks["INV-PKG-PRESENT"] = "PASS"

    world_facts = package.get("world_facts", [])
    observations = package.get("observations", [])
    evidence = package.get("physical_evidence", [])
    testimony = package.get("testimony", [])
    knowledge = package.get("knowledge", [])
    relationships = package.get("relationships", [])
    hypotheses = package.get("hypotheses", [])
    conclusions = package.get("conclusions", [])
    proofs = package.get("proofs", [])
    clue_map = package.get("compatibility_clue_map", [])
    acquisitions = package.get("acquisition_rules", [])

    wf_ids = {str(f["fact_id"]) for f in world_facts if f.get("fact_id")}
    obs_ids = {str(o["observation_id"]) for o in observations if o.get("observation_id")}
    evd_ids = {str(e["evidence_id"]) for e in evidence if e.get("evidence_id")}
    test_ids = {str(t["testimony_id"]) for t in testimony if t.get("testimony_id")}
    know_ids = {str(k["knowledge_id"]) for k in knowledge if k.get("knowledge_id")}
    hyp_ids = {str(h["hypothesis_id"]) for h in hypotheses if h.get("hypothesis_id")}
    concl_ids = {str(c["conclusion_id"]) for c in conclusions if c.get("conclusion_id")}
    proof_ids = {str(p["proof_id"]) for p in proofs if p.get("proof_id")}

    # --- Entity presence ---
    ent_ok = bool(world_facts and knowledge and conclusions and proofs)
    if not world_facts:
        result.errors.append("world_facts empty")
        ent_ok = False
    if not conclusions:
        result.errors.append("conclusions empty")
        ent_ok = False
    if not proofs:
        result.errors.append("proofs empty")
        ent_ok = False
    result.checks["INV-ENTITIES"] = "PASS" if ent_ok else "FAIL"

    # --- Evidence provenance ---
    prov_ok = True
    for ev in evidence:
        eid = ev.get("evidence_id")
        prov = ev.get("provenance", {})
        if not prov.get("world_fact_id") and not prov.get("source_event_id"):
            result.errors.append(f"physical_evidence {eid} missing provenance")
            prov_ok = False
        if prov.get("world_fact_id") and str(prov["world_fact_id"]) not in wf_ids:
            result.errors.append(f"evidence {eid} provenance world_fact invalid")
            prov_ok = False
    result.checks["INV-EVIDENCE-PROV"] = "PASS" if prov_ok else "FAIL"

    # --- Testimony source (no dialogue system — source NPC required) ---
    test_ok = True
    for t in testimony:
        tid = t.get("testimony_id")
        if not t.get("source_npc_id"):
            result.errors.append(f"testimony {tid} missing source_npc_id")
            test_ok = False
        if not t.get("content_knowledge_id") and not t.get("asserts_world_fact_id"):
            result.errors.append(f"testimony {tid} missing content reference")
            test_ok = False
    result.checks["INV-TESTIMONY-SRC"] = "PASS" if test_ok else "FAIL"

    # --- Knowledge acquisition paths ---
    acq_ok = True
    know_by_id = _index_by_id(knowledge, "knowledge_id")
    for k in knowledge:
        kid = k.get("knowledge_id")
        if not k.get("acquisition"):
            result.errors.append(f"knowledge {kid} missing acquisition block")
            acq_ok = False
            continue
        acq = k["acquisition"]
        src_type = acq.get("source_type")
        if src_type not in KNOWLEDGE_SOURCES:
            result.errors.append(f"knowledge {kid} invalid acquisition source_type {src_type}")
            acq_ok = False
        src_id = acq.get("source_id")
        if src_type == "observation" and str(src_id) not in obs_ids:
            result.errors.append(f"knowledge {kid} observation source {src_id} missing")
            acq_ok = False
        if src_type == "physical_evidence" and str(src_id) not in evd_ids:
            result.errors.append(f"knowledge {kid} evidence source {src_id} missing")
            acq_ok = False
        if src_type == "testimony" and str(src_id) not in test_ids:
            result.errors.append(f"knowledge {kid} testimony source {src_id} missing")
            acq_ok = False
        if src_type == "world_fact" and str(src_id) not in wf_ids:
            result.errors.append(f"knowledge {kid} world_fact source {src_id} missing")
            acq_ok = False
        if src_type == "hypothesis" and str(src_id) not in hyp_ids:
            result.errors.append(f"knowledge {kid} hypothesis source {src_id} missing")
            acq_ok = False
    for rule in acquisitions:
        if rule.get("knowledge_id") and str(rule["knowledge_id"]) not in know_ids:
            result.errors.append(f"acquisition_rule references unknown knowledge {rule.get('knowledge_id')}")
            acq_ok = False
    result.checks["INV-ACQUISITION"] = "PASS" if acq_ok else "FAIL"

    # --- Hypotheses not auto-proved ---
    hyp_ok = True
    for h in hypotheses:
        if h.get("auto_proven") or h.get("granted_without_synthesis"):
            result.errors.append(f"hypothesis {h.get('hypothesis_id')} auto-proved forbidden")
            hyp_ok = False
        req = {str(x) for x in h.get("requires_knowledge_ids", []) or []}
        if req and not req.issubset(know_ids):
            result.errors.append(f"hypothesis {h.get('hypothesis_id')} requires unknown knowledge")
            hyp_ok = False
    result.checks["INV-HYPOTHESIS"] = "PASS" if hyp_ok else "FAIL"

    # --- Conclusions provable via proofs ---
    concl_ok = True
    proof_for_conclusion: dict[str, list[dict[str, Any]]] = {}
    for p in proofs:
        cid = str(p.get("conclusion_id", ""))
        proof_for_conclusion.setdefault(cid, []).append(p)
        for kid in p.get("required_knowledge_ids", []) or []:
            if str(kid) not in know_ids:
                result.errors.append(f"proof {p.get('proof_id')} references unknown knowledge {kid}")
                concl_ok = False
    for c in conclusions:
        cid = str(c.get("conclusion_id", ""))
        if c.get("legacy_clue_id") and c.get("investigation_driven_by_clue"):
            result.errors.append(f"conclusion {cid} driven by legacy clue_id")
            concl_ok = False
        if not proof_for_conclusion.get(cid):
            result.errors.append(f"conclusion {cid} has no proof definition")
            concl_ok = False
    result.checks["INV-CONCLUSION-PROV"] = "PASS" if concl_ok else "FAIL"

    # --- Proof independence ---
    ind_ok = True
    for cid, plist in proof_for_conclusion.items():
        if len(plist) < 2:
            continue
        sets = [frozenset(str(x) for x in p.get("required_knowledge_ids", []) or []) for p in plist]
        # independent routes must not be identical sets
        if len(sets) >= 2 and all(s == sets[0] for s in sets[1:]):
            if not plist[0].get("same_route_justification"):
                result.errors.append(f"conclusion {cid} proofs not independent (identical knowledge sets)")
                ind_ok = False
        # check declared independence relationships
        for p in plist:
            if p.get("claims_independence") and not p.get("independent_knowledge_subset"):
                result.errors.append(f"proof {p.get('proof_id')} claims independence without subset")
                ind_ok = False
    result.checks["INV-PROOF-INDEP"] = "PASS" if ind_ok else "FAIL"

    # --- Contradiction handling ---
    contra_ok = True
    unresolved = [r for r in relationships if r.get("type") == "contradicts" and not r.get("resolution")]
    for r in unresolved:
        if not r.get("allow_unresolved_red_herring"):
            result.errors.append(
                f"unresolved contradiction {r.get('relationship_id')} between "
                f"{r.get('from_id')} and {r.get('to_id')}"
            )
            contra_ok = False
    for r in relationships:
        if r.get("type") not in ALLOWED_RELATIONSHIP_TYPES:
            result.errors.append(f"relationship {r.get('relationship_id')} invalid type")
            contra_ok = False
    result.checks["INV-CONTRADICTION"] = "PASS" if contra_ok else "FAIL"

    # --- Legacy clue compatibility only ---
    clue_ok = True
    mapped_clues = {str(m.get("legacy_clue_id")) for m in clue_map if m.get("legacy_clue_id")}
    for c in conclusions:
        if c.get("legacy_clue_id") and str(c["legacy_clue_id"]) not in mapped_clues:
            result.errors.append(
                f"conclusion {c.get('conclusion_id')} legacy_clue_id not in compatibility_clue_map"
            )
            clue_ok = False
    for k in knowledge:
        if k.get("primary_driver") == "legacy_clue_id":
            result.errors.append(f"knowledge {k.get('knowledge_id')} uses legacy clue as primary driver")
            clue_ok = False
    if package.get("investigation_driven_by_clues"):
        result.errors.append("package.investigation_driven_by_clues forbidden")
        clue_ok = False
    result.checks["INV-LEGACY-CLUE"] = "PASS" if clue_ok else "FAIL"

    # --- Orphan knowledge (not used in any proof or hypothesis) ---
    orphan_ok = True
    used_knowledge: set[str] = set()
    for p in proofs:
        used_knowledge.update(str(x) for x in p.get("required_knowledge_ids", []) or [])
    for h in hypotheses:
        used_knowledge.update(str(x) for x in h.get("requires_knowledge_ids", []) or [])
        if h.get("yields_knowledge_id"):
            used_knowledge.add(str(h["yields_knowledge_id"]))
    for k in knowledge:
        kid = str(k.get("knowledge_id", ""))
        if kid and kid not in used_knowledge and not k.get("optional_flavour"):
            result.errors.append(f"orphan knowledge {kid} not used in proof/hypothesis chain")
            orphan_ok = False
    result.checks["INV-ORPHAN"] = "PASS" if orphan_ok else "FAIL"

    if result.errors:
        result.status = "FAIL"
    return result


def main(argv: list[str] | None = None) -> int:
    import sys

    args = argv or sys.argv[1:]
    if not args:
        print("Usage: python3 -m idne.investigation_core_validate <adventure_root>")
        return 2
    res = validate_investigation_core(args[0])
    print(json.dumps(res.to_dict(), indent=2))
    return 0 if res.status in ("PASS", "SKIP") else 1


if __name__ == "__main__":
    raise SystemExit(main())
