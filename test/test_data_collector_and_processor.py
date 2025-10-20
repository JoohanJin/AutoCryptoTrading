from __future__ import annotations

import sys
from pathlib import Path
import unittest

# NOTE: These unit tests were rewritten to act as light smoke checks that do not
# require live services. Each block skips gracefully if optional dependencies
# (e.g. websocket-client, h11) are missing so CI can still run.

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from object.constants import IndexType  # type: ignore
from object.signal import Signal, TradeSignal  # type: ignore

try:
    from manager.data_collector_and_processor import (  # type: ignore
        DataCollectorAndProcessor,
        IndexFactory,
    )
except ModuleNotFoundError:  # pragma: no cover - optional dependency (e.g. h11)
    DataCollectorAndProcessor = None  # type: ignore
    IndexFactory = None  # type: ignore

try:
    from manager.trade_manager import TradeManager  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - optional dependency chain
    TradeManager = None  # type: ignore


class DataCollectorTest(unittest.TestCase):
    """Validate static timestamp helper without touching network resources."""

    def test_timestamp_generation_returns_int(self) -> None:
        """Ensure timestamps are emitted as integers."""
        if DataCollectorAndProcessor is None:
            self.skipTest("data_collector_and_processor dependencies unavailable")
        timestamp = DataCollectorAndProcessor.generate_timestamp()
        self.assertIsInstance(timestamp, int)


class IndexFactoryTest(unittest.TestCase):
    """Cover the happy-path and failure cases for IndexFactory."""

    def test_generate_index_happy_path(self) -> None:
        """Factory should produce an Index when payload contains data."""
        if IndexFactory is None:
            self.skipTest("index factory dependencies unavailable")
        factory = IndexFactory()
        payload = {
            "timestamp": 1_700_000_000_000,
            "type": IndexType.SMA,
            "data": {5: 1.0, 10: 2.0},
        }

        index = factory.generate_index(payload)  # type: ignore[arg-type]

        self.assertIsNotNone(index)
        self.assertEqual(index.index_type, IndexType.SMA)
        self.assertEqual(index.data, payload["data"])

    def test_generate_index_returns_none_on_missing_data(self) -> None:
        """Factory should decline payloads that omit the data field."""
        if IndexFactory is None:
            self.skipTest("index factory dependencies unavailable")
        factory = IndexFactory()
        payload = {
            "timestamp": 1_700_000_000_000,
            "type": IndexType.SMA,
            "data": None,
        }

        self.assertIsNone(factory.generate_index(payload))  # type: ignore[arg-type]


class TradeManagerUtilitiesTest(unittest.TestCase):
    """Target TradeManager helpers that do not depend on live infrastructure."""

    def test_trade_manager_timestamp(self) -> None:
        """TradeManager timestamps should be emitted as integers."""
        if TradeManager is None:
            self.skipTest("trade_manager dependencies unavailable")
        timestamp = TradeManager.generate_timestamp()
        self.assertIsInstance(timestamp, int)

    def test_verify_signal_uses_timestamp_window(self) -> None:
        """verify_signal accepts recent signals inside the configured window."""
        if TradeManager is None:
            self.skipTest("trade_manager dependencies unavailable")
        recent_signal = Signal(TradeSignal.HOLD)
        self.assertTrue(TradeManager.verify_signal(recent_signal, timestamp_window = 10_000))


if __name__ == "__main__":
    unittest.main()
