from __future__ import annotations

import json
import sys
from pathlib import Path

# NOTE: This harness now stubs out the websocket dependency so it can verify the
# reconnect + resubscribe flow without opening real sockets, skipping gracefully
# when websocket-client is not installed.

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

try:
    from mexc.websocket_base import _FutureWebSocket
except ModuleNotFoundError:  # pragma: no cover - optional dependency chain (e.g. websocket-client)
    _FutureWebSocket = None  # type: ignore


class _DummyWebSocket:
    """Minimal stub that records payloads sent via `send`."""

    def __init__(self) -> None:
        self.sent_messages: list[str] = []

    def send(self, payload: str) -> None:
        """Track outgoing payloads for later assertions."""
        self.sent_messages.append(payload)


if _FutureWebSocket is not None:

    class _TestWebSocketManager(_FutureWebSocket):
        """Test double that replaces network IO with deterministic stubs."""

        def __init__(self, endpoint: str) -> None:
            """Boot the parent class and swap in our dummy websocket."""
            super().__init__(endpoint = endpoint)
            self.ws = _DummyWebSocket()
            self.reconnect_attempts: int = 0

        def _connect(self, url: str) -> None:  # type: ignore[override]
            """Record reconnect attempts and reset the dummy socket."""
            if url != self.endpoint:
                raise ValueError(f"Unexpected URL: {url}")
            self.reconnect_attempts += 1
            self.ws = _DummyWebSocket()

else:  # pragma: no cover - dependency missing

    class _TestWebSocketManager:  # type: ignore[override]
        """Fallback that raises when optional dependencies are absent."""

        def __init__(self, *args, **kwargs) -> None:
            raise RuntimeError("mexc.websocket_base dependencies unavailable; install websocket-client")


def simulate_close_and_replay() -> list[str]:
    """Trigger the close handler and return the replayed subscription payloads."""
    if _FutureWebSocket is None:
        raise RuntimeError("mexc.websocket_base dependencies unavailable; install websocket-client")
    manager = _TestWebSocketManager(endpoint = "wss://websocket.test.edge")
    manager.subscriptions = [
        {"method": "sub.ticker", "param": {"symbol": "BTCUSDT"}},
        {"method": "sub.orderbook", "param": {"symbol": "ETHUSDT", "depth": 5}},
    ]

    manager._BasicWebSocketManager__on_close(
        manager.ws,
        status_code = 4001,
        close_msg = "Test close",
    )

    # Should have attempted to reconnect once
    assert manager.reconnect_attempts == 1, "Reconnect was not triggered"

    # Normalize to readable JSON strings for inspection
    return [json.loads(msg) for msg in manager.ws.sent_messages]


if __name__ == "__main__":
    try:
        replayed = simulate_close_and_replay()
    except RuntimeError as exc:  # pragma: no cover - optional dependency missing
        print(f"Skipped: {exc}")
    else:
        print("Replayed subscriptions:")
        for payload in replayed:
            print(payload)
