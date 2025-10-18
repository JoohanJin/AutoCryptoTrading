from __future__ import annotations

import sys
from pathlib import Path
import unittest

# NOTE: Replaced earlier integration-heavy tests with lightweight queue checks that
# confirm the data pipeline accepts and returns payloads as expected.

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from object.constants import IndexType  # type: ignore
from pipeline.data_pipeline import DataPipeline  # type: ignore


class DataPipelineTest(unittest.TestCase):
    """Exercise the minimal push/pop contract exposed by DataPipeline."""

    def setUp(self) -> None:
        """Create a fresh pipeline for each test to avoid shared state."""
        self.pipeline = DataPipeline()

    def test_push_accepts_index_payload(self) -> None:
        """Ensure push returns True when submitting a valid payload."""
        payload = {
            "timestamp": 1_700_000_000_000,
            "type": IndexType.SMA,
            "data": {5: 1.0},
        }
        self.assertTrue(self.pipeline.push(payload, block = False))

    def test_pop_returns_recent_payload(self) -> None:
        """Verify pop retrieves the same payload that was just queued."""
        payload = {
            "timestamp": 1_700_000_000_001,
            "type": IndexType.EMA,
            "data": {10: 2.0},
        }
        self.pipeline.push(payload, block = False)
        result = self.pipeline.pop(block = False)
        self.assertEqual(result, payload)


if __name__ == "__main__":
    unittest.main()
