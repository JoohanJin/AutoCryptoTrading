# Standard Library
from typing import List, Dict, Union, Tuple
from enum import IntFlag
import time

class TradeSignal(IntFlag):
    # state management using the bit manipulation.
    SHORT_TERM_BUY = 1  # 0001
    LONG_TERM_BUY = 2  # 0010
    SHORT_TERM_SELL = 4  # 0010
    LONG_TERM_SELL = 8  # 0100
    HOLD = 16  # 1000


class Signal:
    @staticmethod
    def generate_timestamp() -> int:
        return int(time.time() * 1_000)

    def __init__(
        self: 'Signal',
        signal: TradeSignal,
        timestamp: int = None, # Default input is None
    ) -> None:
        """
        func __init__:
            - Create an indicator instance with the given signal and timestamp.
        """
        self.timestamp = Signal.generate_timestamp() if (not timestamp) else timestamp
        self.signal = signal
        return None
