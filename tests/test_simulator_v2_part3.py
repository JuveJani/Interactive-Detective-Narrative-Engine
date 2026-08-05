"""Tests for Simulator v2 Part 3 — diagnostics, CLI, reports, AI export."""

from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from idne.sim_v2.cli import main as cli_main
from simulator_v2.ai_context import export_ai_context
from simulator_v2.config import RunnerConfig
from simulator_v2.diagnostics import run_integrated_diagnostics
from simulator_v2.findings import DiagnosticFinding
from simulator_v2.modes import SimulationModes
from simulator_v2.reports import make_output_dir, write_all_reports
from simulator_v2.runner import cmd_compare, cmd_diagnose, cmd_exhaustive, cmd_simulate, cmd_trace, cmd_validate
from simulator_v2.service import SimulatorService

FIXTURES = Path(__file__).resolve().parent / "fixtures"
SOLO = FIXTURES / "sim_v2_solo"
TWO = FIXTURES / "sim_v2_two_player"
SOLO_IDNE = FIXTURES / "sim_v2_solo.idne"

REQUIRED_REPORTS = {
    "executive_diagnostic.md",
    "findings.md",
    "findings.json",
    "metrics.json",
    "repair_backlog.md",
    "simulator_log.txt",
    "parse_errors.md",
    "run_manifest.json",
}


class TestSimulatorV2Part3(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_diagnostic_finding_schema(self):
        f = DiagnosticFinding(
            finding_id="TEST-001",
            severity="major",
            confidence="proven",
            canonical_source="KNOW-001",
            source_file="DO_NOT_READ/investigation_core_package.json",
            affected_entity="KNOW-001",
            affected_paths=["WF-001"],
            simulation_evidence="test evidence",
            expected_behavior="expected",
            observed_behavior="observed",
            trust_impact="none",
            likely_owner="GENERATOR",
            repair_eligible=True,
            human_approval_required=True,
            validator="investigation",
        )
        d = f.to_dict()
        self.assertEqual(d["finding_id"], "TEST-001")
        self.assertIn("likely_owner", d)

    def test_integrated_diagnostics_solo(self):
        cfg = RunnerConfig(monte_carlo_runs=5, compare_runs_per_strategy=2, max_states=30)
        report = run_integrated_diagnostics(SOLO, config=cfg, run_simulation=True)
        self.assertEqual(report.adventure_id, "sim_v2_solo")
        self.assertIn("status", report.integrated_validation)
        self.assertIn("trusted", report.trust)

    def test_integrated_diagnostics_two_player(self):
        cfg = RunnerConfig(monte_carlo_runs=3, compare_runs_per_strategy=1, max_states=20)
        report = run_integrated_diagnostics(TWO, config=cfg, run_simulation=True)
        self.assertEqual(report.play_mode, "two_player")

    def test_write_all_reports(self):
        cfg = RunnerConfig(monte_carlo_runs=3, compare_runs_per_strategy=1, max_states=15)
        report = run_integrated_diagnostics(SOLO, config=cfg)
        out = self.tmp / "report"
        out.mkdir()
        write_all_reports(out, report)
        for name in REQUIRED_REPORTS:
            self.assertTrue((out / name).exists(), f"missing {name}")
        self.assertTrue((out / "strategy_comparison.csv").exists())
        self.assertTrue((out / "endings.csv").exists())
        self.assertTrue((out / "paths.csv").exists())
        self.assertTrue((out / "time_analysis.csv").exists())
        self.assertTrue((out / "state_transitions.csv").exists())
        self.assertTrue((out / "human_playtest_questions.md").exists())

    def test_cmd_validate_solo(self):
        cfg = RunnerConfig(output_base=str(self.tmp))
        result = cmd_validate(SOLO, cfg)
        self.assertEqual(result["status"], "PASS")

    def test_cmd_trace_deterministic(self):
        cfg = RunnerConfig(output_base=str(self.tmp))
        r1 = cmd_trace(SOLO, seed=7, config=cfg)
        r2 = cmd_trace(SOLO, seed=7, config=cfg)
        self.assertEqual(r1["result"]["path"], r2["result"]["path"])

    def test_cmd_simulate_smoke(self):
        cfg = RunnerConfig(output_base=str(self.tmp), monte_carlo_runs=5, max_runs=5)
        result = cmd_simulate(SOLO, runs=5, seed=42, config=cfg)
        self.assertEqual(result["result"]["status"], "COMPLETED")
        self.assertIn("ending_frequencies", result["result"])

    def test_cmd_exhaustive_bounded(self):
        cfg = RunnerConfig(output_base=str(self.tmp), max_states=25)
        result = cmd_exhaustive(SOLO, max_states=25, config=cfg)
        status = result["result"]["status"]
        self.assertIn(status, ("COMPLETED", "BLOCKED", "CANCELLED"))

    def test_cmd_compare_strategies(self):
        cfg = RunnerConfig(output_base=str(self.tmp))
        result = cmd_compare(SOLO, runs_per_strategy=2, seed=10, config=cfg)
        self.assertEqual(result["result"]["status"], "COMPLETED")

    def test_cli_validate(self):
        rc = cli_main(["validate", str(SOLO)])
        self.assertEqual(rc, 0)

    def test_cli_trace(self):
        rc = cli_main(["trace", str(SOLO), "--seed", "42"])
        self.assertEqual(rc, 0)

    def test_cli_simulate(self):
        rc = cli_main(["simulate", str(SOLO), "--runs", "3", "--seed", "1"])
        self.assertEqual(rc, 0)

    def test_cli_exhaustive(self):
        rc = cli_main(["exhaustive", str(SOLO), "--max-states", "20"])
        self.assertIn(rc, (0, 1))

    def test_cli_compare(self):
        rc = cli_main(["compare", str(SOLO), "--runs-per-strategy", "2"])
        self.assertEqual(rc, 0)

    def test_export_ai_context(self):
        cfg = RunnerConfig(monte_carlo_runs=2, compare_runs_per_strategy=1, max_states=10)
        report = run_integrated_diagnostics(SOLO, config=cfg)
        out = self.tmp / "out"
        out.mkdir()
        write_all_reports(out, report)
        findings = json.loads((out / "findings.json").read_text(encoding="utf-8"))
        if findings.get("findings"):
            fid = findings["findings"][0]["finding_id"]
            ctx_dir = export_ai_context(out, fid)
            self.assertTrue((ctx_dir / "context.json").exists())
            self.assertTrue((ctx_dir / "context.md").exists())
            ctx = json.loads((ctx_dir / "context.json").read_text(encoding="utf-8"))
            self.assertIn("PROVEN_FACTS", ctx)
            self.assertIn("PROHIBITED_CONCLUSIONS", ctx)

    def test_cli_export_ai_context(self):
        cfg = RunnerConfig(monte_carlo_runs=2, max_states=10)
        report = run_integrated_diagnostics(SOLO, config=cfg)
        out = self.tmp / "cli_out"
        out.mkdir()
        write_all_reports(out, report)
        findings = json.loads((out / "findings.json").read_text(encoding="utf-8"))
        if not findings.get("findings"):
            self.skipTest("no findings to export")
        fid = findings["findings"][0]["finding_id"]
        rc = cli_main(["export-ai-context", str(out), "--finding", fid])
        self.assertEqual(rc, 0)

    def test_service_interface(self):
        svc = SimulatorService()
        load = svc.load_package(SOLO)
        self.assertTrue(load.simulation_ready)
        readiness = svc.validate_readiness()
        self.assertTrue(readiness.ready)
        run_id = svc.start_run()
        progress = svc.get_progress(run_id)
        self.assertEqual(progress.status.value, "RUNNING")
        results = svc.get_results(run_id)
        self.assertEqual(results.status.value, "COMPLETED")

    def test_solo_idne_validate(self):
        if not SOLO_IDNE.exists():
            self.skipTest("idne fixture not built")
        modes = SimulationModes(str(SOLO_IDNE))
        self.assertEqual(modes.validate()["status"], "PASS")

    def test_atomic_output_dir_unique(self):
        cfg = RunnerConfig(output_base=str(self.tmp))
        o1 = make_output_dir(Path(cfg.output_base), "test")
        o2 = make_output_dir(Path(cfg.output_base), "test")
        self.assertNotEqual(o1, o2)

    def test_windows_scripts_exist(self):
        win = Path(__file__).resolve().parents[1] / "scripts" / "windows"
        for name in (
            "install.ps1",
            "setup-venv.ps1",
            "validate-package.ps1",
            "run-diagnostic.ps1",
            "open-latest-report.ps1",
            "export-ai-context.ps1",
            "resume-diagnostic.ps1",
        ):
            self.assertTrue((win / name).exists(), name)


if __name__ == "__main__":
    unittest.main()
