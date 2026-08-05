"""Tests for Simulator v2 Part 1 — package, derivation, state core."""

from __future__ import annotations

import json
import shutil
import tempfile
import unittest
import zipfile
from pathlib import Path

from idne.idne_package import build_idne_package, verify_extracted_package
from simulator import __version__ as legacy_version
from simulator_v2 import LEGACY_SIMULATOR_MARKER, __version__ as v2_version
from simulator_v2.derivation import derive_simulation_model
from simulator_v2.legacy import is_legacy_simulator_path, legacy_simulator_notice
from simulator_v2.package_loader import load_simulator_package
from simulator_v2.service import RunStatus, SimulatorService
from simulator_v2.state import SimulationState, initial_state_from_model
from simulator_v2.types import LoadStatus

FIXTURES = Path(__file__).resolve().parent / "fixtures"
HARBORVIEW = Path(__file__).resolve().parents[1] / "adventures" / "CASE_BENCHMARK_v0.4"
SOLO = FIXTURES / "sim_v2_solo"
TWO = FIXTURES / "sim_v2_two_player"
SOLO_IDNE = FIXTURES / "sim_v2_solo.idne"
MISSING = FIXTURES / "sim_v2_missing_layer"
VALIDATION_FAIL = FIXTURES / "sim_v2_validation_fail"


class TestSimulatorV2Part1(unittest.TestCase):
    def test_valid_solo_package_load_directory(self):
        result = load_simulator_package(SOLO)
        self.assertEqual(result.status, LoadStatus.READY)
        self.assertEqual(result.play_mode, "single_investigator")
        self.assertTrue(result.simulation_ready)
        self.assertFalse(result.requires_legacy_adapter)

    def test_valid_solo_package_load_idne(self):
        self.assertTrue(SOLO_IDNE.exists())
        result = load_simulator_package(SOLO_IDNE)
        self.assertEqual(result.status, LoadStatus.READY)
        self.assertTrue(result.checksum_valid)
        self.assertEqual(result.play_mode, "single_investigator")

    def test_valid_two_player_package_load(self):
        result = load_simulator_package(TWO)
        self.assertEqual(result.status, LoadStatus.READY)
        self.assertEqual(result.play_mode, "two_player")
        self.assertTrue(result.simulation_ready)

    def test_broken_checksum_blocks(self):
        ws = Path(tempfile.mkdtemp())
        out = ws / "bad.idne"
        build_idne_package(SOLO, out, "sim_v2_bad_checksum")
        extract = ws / "extract"
        with zipfile.ZipFile(out, "r") as zf:
            zf.extractall(extract)
        adv_file = next((extract / "adventure").rglob("*.json"))
        adv_file.write_bytes(b"corrupted")
        bad = ws / "tampered.idne"
        shutil.make_archive(str(bad.with_suffix("")), "zip", extract)
        tampered = Path(str(bad.with_suffix("")) + ".zip")
        tampered.rename(bad)
        result = load_simulator_package(bad)
        self.assertEqual(result.status, LoadStatus.BLOCKED)
        self.assertFalse(result.checksum_valid)

    def test_unsupported_version_blocks(self):
        ws = Path(tempfile.mkdtemp())
        manifest = {"schema_version": "99.0", "adventure_id": "X", "entries": []}
        (ws / "package_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
        (ws / "package_checksum.sha256").write_text("", encoding="utf-8")
        (ws / "adventure").mkdir()
        shutil.copytree(SOLO, ws / "adventure", dirs_exist_ok=True)
        result = load_simulator_package(ws)
        self.assertEqual(result.status, LoadStatus.BLOCKED)
        self.assertIn("unsupported package version", result.errors[0])

    def test_missing_layer_blocks(self):
        result = load_simulator_package(MISSING)
        self.assertEqual(result.status, LoadStatus.BLOCKED)
        self.assertTrue(any("missing simulation layers" in e for e in result.errors))

    def test_failed_integrated_validation_blocks(self):
        result = load_simulator_package(VALIDATION_FAIL)
        self.assertEqual(result.status, LoadStatus.BLOCKED)
        self.assertIn(result.integrated_validation_status, ("FAIL", "BLOCKED"))

    def test_no_manual_adapter_dependency(self):
        result = load_simulator_package(SOLO)
        self.assertFalse(result.requires_legacy_adapter)
        self.assertFalse((SOLO / "sim_adapter.json").exists())

    def test_deterministic_derivation(self):
        load = load_simulator_package(SOLO)
        m1 = derive_simulation_model(load.adventure_root, load.play_mode)
        m2 = derive_simulation_model(load.adventure_root, load.play_mode)
        self.assertEqual(m1.report.to_dict(), m2.report.to_dict())
        self.assertEqual(sorted(m1.locations.keys()), sorted(m2.locations.keys()))

    def test_state_copying_and_identity(self):
        load = load_simulator_package(SOLO)
        model = derive_simulation_model(load.adventure_root, load.play_mode)
        s1 = initial_state_from_model(model)
        s2 = s1.copy()
        self.assertIsNot(s1, s2)
        self.assertEqual(s1.identity_key(), s2.identity_key())
        s2.player_knowledge.add("KNOW-001")
        self.assertNotEqual(s1.identity_key(), s2.identity_key())
        s3 = s1.with_state_id(7)
        self.assertEqual(s3.state_id, 7)
        self.assertEqual(s1.state_id, 0)

    def test_canonical_source_traceability(self):
        load = load_simulator_package(SOLO)
        model = derive_simulation_model(load.adventure_root, load.play_mode)
        loc = model.locations["LOC-LOBBY"]
        self.assertEqual(loc.ref.source_file, "DO_NOT_READ/environment_package.json")
        self.assertEqual(loc.ref.canonical_entity_id, "LOC-LOBBY")
        self.assertIn(loc, model.report.entities)

    def test_legacy_mode_clearly_marked(self):
        self.assertEqual(LEGACY_SIMULATOR_MARKER, "legacy_sim_adapter_required")
        self.assertIn("legacy", legacy_simulator_notice().lower())
        self.assertTrue(v2_version.startswith("2."))
        self.assertNotEqual(legacy_version, v2_version)
        if HARBORVIEW.exists():
            self.assertTrue(is_legacy_simulator_path(HARBORVIEW))

    def test_service_load_validate_start(self):
        svc = SimulatorService()
        load = svc.load_package(SOLO)
        self.assertEqual(load.status, LoadStatus.READY)
        readiness = svc.validate_readiness()
        self.assertTrue(readiness.ready)
        run_id = svc.start_run()
        progress = svc.get_progress(run_id)
        self.assertEqual(progress.status, RunStatus.RUNNING)
        results = svc.get_results(run_id)
        self.assertEqual(results.status, RunStatus.COMPLETED)
        self.assertIsNotNone(results.final_state)

    def test_service_cancel(self):
        svc = SimulatorService()
        svc.load_package(SOLO)
        run_id = svc.start_run()
        svc.cancel(run_id)
        progress = svc.get_progress(run_id)
        self.assertEqual(progress.status, RunStatus.CANCELLED)

    def test_fixed_truth_not_in_mutable_state(self):
        load = load_simulator_package(SOLO)
        model = derive_simulation_model(load.adventure_root, load.play_mode)
        state = initial_state_from_model(model)
        self.assertIsInstance(state, SimulationState)
        self.assertNotIn("culprit_id", state.flow_flags)
        self.assertIn("culprit_id", model.fixed_truth)


if __name__ == "__main__":
    unittest.main()
