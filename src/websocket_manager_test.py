"""Quick harness to verify WebSocket retry logic on close events."""

from __future__ import annotations

import json

from mexc.websocket_base import _FutureWebSocket


class _DummyWebSocket:
    """Minimal stub that records payloads sent via `send`."""

    def __init__(self) -> None:
        self.sent_messages: list[str] = []

    def send(self, payload: str) -> None:
        self.sent_messages.append(payload)


class _TestWebSocketManager(_FutureWebSocket):
    """Test double that avoids opening real network connections."""

    def __init__(self, endpoint: str) -> None:
        super().__init__(endpoint = endpoint)
        self.ws = _DummyWebSocket()
        self.reconnect_attempts: int = 0

    def _connect(self, url: str) -> None:  # type: ignore[override]
        """Override network connection with a deterministic stub."""
        if url != self.endpoint:
            raise ValueError(f"Unexpected URL: {url}")
        self.reconnect_attempts += 1
        self.ws = _DummyWebSocket()


def simulate_close_and_replay() -> list[str]:
    """Trigger the close handler and return the replayed subscription payloads."""
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
    replayed = simulate_close_and_replay()
    print("Replayed subscriptions:")
    for payload in replayed:
        print(payload)
