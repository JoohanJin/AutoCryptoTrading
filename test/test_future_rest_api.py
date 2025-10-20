from __future__ import annotations

import sys
from pathlib import Path
import unittest

# NOTE: Slimmed down the MEXC REST tests so they validate the public API surface
# without performing live HTTP calls, and skip when websocket-client is absent.

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

try:
    import mexc.future as future  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - optional dependency chain (e.g. websocket-client)
    future = None  # type: ignore


class FutureMarketInterfaceTest(unittest.TestCase):
    """Basic interface smoke tests for the MEXC FutureMarket SDK."""

    @classmethod
    def setUpClass(cls) -> None:
        """Skip the whole suite if the optional dependency stack is missing."""
        if future is None:
            raise unittest.SkipTest("mexc.future dependencies unavailable")
        cls.market_class = future.FutureMarket

    def test_expected_public_endpoints_exist(self) -> None:
        """Assert the key public endpoints exist on the SDK."""
        expected_methods = [
            "ping",
            "detail",
            "support_currencies",
            "depth",
            "depth_commits",
            "index_price",
            "fair_price",
            "funding_rate",
            "kline",
            "kline_index_price",
            "kline_fair_price",
            "deals",
            "ticker",
            "risk_reverse",
            "risk_reverse_history",
            "funding_rate_history",
        ]
        for method_name in expected_methods:
            with self.subTest(method = method_name):
                self.assertTrue(
                    hasattr(self.market_class, method_name),
                    msg = f"FutureMarket missing method {method_name}",
                )

    def test_expected_private_endpoints_exist(self) -> None:
        """Assert the private endpoint helpers are defined."""
        expected_methods = [
            "assets",
            "history_position",
            "current_position",
            "pending_order",
            "risk_limit",
            "fee_rate",
        ]
        for method_name in expected_methods:
            with self.subTest(method = method_name):
                self.assertTrue(
                    hasattr(self.market_class, method_name),
                    msg = f"FutureMarket missing method {method_name}",
                )


if __name__ == "__main__":
    unittest.main()
