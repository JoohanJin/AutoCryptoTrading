    # Standard Library
from typing import List, Dict, Union, Tuple
from enum import IntFlag

class TradeSignal(IntFlag):
    # state management using the bit manipulation.
    SHORT_TERM_BUY: int = 1 # 0001
    LONG_TERM_BUY: int = 2 # 0010
    SHORT_TERM_SELL: int = 4 # 0010
    LONG_TERM_SELL: int = 8 # 0100
    HOLD: int = 16 # 1000

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