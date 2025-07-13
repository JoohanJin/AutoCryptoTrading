    # Standard Library
from typing import List, Dict, Union, Tuple
from enum import IntFlag

class TradeSignal(IntFlag):
    # state management using the bit manipulation.
    SHORT_TERM_BUY = 1 # 0001
    LONG_TERM_BUY = 2 # 0010
    SHORT_TERM_SELL = 4 # 0010
    LONG_TERM_SELL = 8 # 0100
    HOLD = 16 # 1000

class Signal:
    def __init__(
        self,
        signal: TradeSignal,
        timestamp: int,
    ) -> None:
        """
        # func __init__:
            # Create an indicator instance with the given signal and timestamp.
        """
        self.timestamp = timestamp
        self.signal = signal
        return None