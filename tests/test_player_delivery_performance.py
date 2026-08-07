"""Performance checks for structured player delivery."""

from __future__ import annotations

import json
import time
import unittest
from pathlib import Path

COLD = Path(__file__).resolve().parents[1] / "adventures" / "The_Cold_Storage_Alarm"


class TestPlayerDeliveryPerformance(unittest.TestCase):
    @unittest.skipUnless(COLD.exists(), "Cold Storage adventure not present")
    def test_cold_storage_load_and_distant_navigation(self):
        gamebook_path = COLD / "adventure" / "PLAYER" / "gamebook.json"
        self.assertTrue(gamebook_path.exists(), "run build_gamebook_package first")

        t0 = time.perf_counter()
        payload = json.loads(gamebook_path.read_text(encoding="utf-8"))
        load_ms = int((time.perf_counter() - t0) * 1000)

        start = str(payload["start_section"])
        start_section = payload["sections"][start]
        far_target = max(choice["target_section"] for choice in start_section["choices"])

        t1 = time.perf_counter()
        distant = payload["sections"][str(far_target)]
        nav_ms = int((time.perf_counter() - t1) * 1000)

        self.assertGreater(payload["section_count"], 4000)
        self.assertLess(load_ms, 5000, f"load took {load_ms}ms")
        self.assertLess(nav_ms, 5, f"distant lookup took {nav_ms}ms")
        self.assertTrue(distant["body"])


if __name__ == "__main__":
    unittest.main()
