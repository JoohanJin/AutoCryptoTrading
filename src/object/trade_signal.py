# Standard Library
from typing import List, Dict, Union, Tuple

# Custom Library
from signal_int import TradeSignal


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