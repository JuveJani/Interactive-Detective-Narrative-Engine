"""Regression tests for Simulator v2 integration fixes."""

from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from idne.sim_v2.cli import main as cli_main
from simulator_v2.modes import ExhaustiveConfig, SimulationModes
from simulator_v2.package_loader import load_simulator_package
from simulator_v2.reports import write_all_reports
from simulator_v2.runner import _diagnostic_report, cmd_trace
from simulator_v2.config import RunnerConfig
from simulator_v2.trust_gate import ensure_trust_blockers, evaluate_trust

FIXTURES = Path(__file__).resolve().parent / "fixtures"
SOLO = FIXTURES / "sim_v2_solo"
SOLO_IDNE = FIXTURES / "sim_v2_solo.idne"
VALIDATION_FAIL = FIXTURES / "sim_v2_validation_fail"


class TestSimulatorV2IntegrationFixes(unittest.TestCase):
    def test_trust_false_when_integrated_validation_fail(self):
        load = load_simulator_package(VALIDATION_FAIL)
        trust = evaluate_trust(load, None, coverage="validate").to_dict()
        self.assertFalse(trust["trusted"])
        self.assertTrue(any("integrated_validation" in b for b in trust["blockers"]))

    def test_untrusted_always_has_blockers(self):
        trust = ensure_trust_blockers({"trusted": False, "blockers": []})
        self.assertTrue(trust["blockers"])

    def test_trace_includes_trust_and_integrated_validation(self):
        modes = SimulationModes(str(SOLO))
        result = modes.trace("random_legal", seed=42)
        self.assertTrue(result.trust)
        self.assertEqual(result.integrated_validation.get("status"), "PASS")
        self.assertTrue(result.trust.get("trusted"))
        self.assertIn("integrated_validation_status", result.trust)

    def test_trace_deterministic_byte_identical(self):
        modes = SimulationModes(str(SOLO))
        r1 = modes.trace("random_legal", seed=42).to_dict()
        r2 = modes.trace("random_legal", seed=42).to_dict()
        self.assertEqual(r1["path"], r2["path"])
        self.assertEqual(r1["metrics"], r2["metrics"])
        self.assertEqual(r1["final_state_key"], r2["final_state_key"])

    def test_compare_skips_two_player_strategy_on_solo(self):
        modes = SimulationModes(str(SOLO))
        result = modes.compare_strategies(runs_per_strategy=3, seed=10)
        coop = result["strategies"]["cooperative_two_player"]
        self.assertEqual(coop["status"], "SKIPPED_INCOMPATIBLE_MODE")
        self.assertIn("integrated_validation", result)
        self.assertIn("trust", result)

    def test_incomplete_includes_reason_and_state(self):
        modes = SimulationModes(str(SOLO))
        result = modes.compare_strategies(runs_per_strategy=2, seed=1)
        for name, data in result["strategies"].items():
            if data.get("status") == "SKIPPED_INCOMPATIBLE_MODE":
                continue
            for detail in data.get("incomplete_details", []):
                self.assertIn("reason", detail)
                self.assertIn("steps", detail)
                self.assertIn("last_state_key", detail)

    def test_exhaustive_includes_trust_and_validation(self):
        modes = SimulationModes(str(SOLO))
        result = modes.exhaustive(ExhaustiveConfig(max_states=15))
        self.assertIn("trust", result)
        self.assertIn("integrated_validation", result)
        self.assertEqual(result["integrated_validation"]["status"], "PASS")

    def test_executive_report_no_none_blockers_when_untrusted(self):
        modes = SimulationModes(str(SOLO))
        trace = modes.trace("random_legal", seed=1).to_dict()
        load = load_simulator_package(SOLO)
        report = _diagnostic_report(load, {"trace": trace}, {}, ["test"])
        out = Path(tempfile.mkdtemp())
        try:
            write_all_reports(out, report)
            md = (out / "executive_diagnostic.md").read_text(encoding="utf-8")
            self.assertNotIn("Integrated validation:** None", md)
            self.assertNotIn("Trust blockers\n- None", md)
            manifest = json.loads((out / "run_manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest.get("integrated_validation_status"), "PASS")
        finally:
            shutil.rmtree(out, ignore_errors=True)

    def test_simulate_mode_trust_propagation(self):
        modes = SimulationModes(str(SOLO))
        result = modes.monte_carlo()
        self.assertTrue(result["trust"].get("trusted"))
        self.assertEqual(result["integrated_validation"]["status"], "PASS")

    def test_exhaustive_blocked_finding_in_diagnose_report(self):
        modes = SimulationModes(str(SOLO))
        ex = modes.exhaustive(ExhaustiveConfig(max_states=10))
        load = load_simulator_package(SOLO)
        from simulator_v2.diagnostics import build_integration_findings

        findings = build_integration_findings(load, modes.model, {"exhaustive": ex}, ex["trust"])
        ids = [f.finding_id for f in findings]
        self.assertIn("SIM-EXHAUSTIVE-BLOCKED", ids)

    def test_cli_reproduction_commands(self):
        pkg = str(SOLO_IDNE if SOLO_IDNE.exists() else SOLO)
        self.assertEqual(cli_main(["validate", pkg]), 0)
        self.assertEqual(cli_main(["trace", pkg, "--seed", "42"]), 0)
        self.assertEqual(cli_main(["simulate", pkg, "--runs", "5", "--seed", "42"]), 0)
        self.assertEqual(cli_main(["compare", pkg, "--runs-per-strategy", "2"]), 0)
        self.assertIn(cli_main(["exhaustive", pkg, "--max-states", "20"]), (0, 1))

    def test_broad_explorer_reaches_terminal_with_fallback(self):
        modes = SimulationModes(str(SOLO))
        result = modes.trace("broad_explorer", seed=42)
        self.assertTrue(result.ending_id or result.incomplete_reason)
        if not result.ending_id:
            self.assertIn(result.incomplete_reason, ("MAX_STEPS", "CYCLE", "NO_LEGAL_ACTION", "CANCELLED", "ERROR"))


if __name__ == "__main__":
    unittest.main()
