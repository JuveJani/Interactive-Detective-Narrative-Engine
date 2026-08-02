"""Partial recovery and runner tests."""

import json
import unittest
from pathlib import Path

from simulator.output import make_output_dir, write_all_outputs
from simulator.models import Finding


class TestPartialRecovery(unittest.TestCase):
    def test_output_folder_created(self):
        out = make_output_dir(Path("simulation_output"), mode="partial_test")
        self.assertTrue(out.exists())
        self.assertTrue(str(out).startswith("simulation_output"))

    def test_partial_write(self):
        out = make_output_dir(Path("simulation_output"), mode="partial_test")
        findings = [
            Finding(
                id="T-1",
                severity="info",
                confidence="high",
                evidence="test",
                file="test",
                identifier="x",
                expected_rule="rule",
                layer="SIMULATOR",
                auto_fix_possible=False,
                human_approval_required=False,
            )
        ]
        write_all_outputs(out, findings, {"runs": 0, "graph": {}}, [], {}, [], "test", ["log"])
        self.assertTrue((out / "findings.json").exists())
        data = json.loads((out / "findings.json").read_text())
        self.assertEqual(data[0]["id"], "T-1")


if __name__ == "__main__":
    unittest.main()
