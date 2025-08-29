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
    '''
    ##############################################################
    #                         Static Method                      #
    ##############################################################
    '''
    @staticmethod
    def generate_timestamp() -> int:
        return int(time.time() * 1_000)

    '''
    data_struct = {
    "indicator": {
        "timestamp": <int>, int(time.time() * 1000),
        "signal": object.TradeSignal
            # 001: for buy
            # 010: for sell
            # 100: for hold -> do nothing
            # Other signals
        }
    }
    '''

    def __init__(
        self: 'Signal',
        signal: TradeSignal,
    ) -> None:
        """
        func __init__:
            - Create an indicator instance with the given signal and timestamp.
        """
        self._timestamp: int = signal.get("timestamp", Signal.generate_timestamp())
        self._signal: TradeSignal = signal

        return None

    @property  # timestamp getter
    def timestamp(self) -> int:
        return self._timestamp

    @property  # signal getter.
    def signal(self) -> TradeSignal:
        return self._signal
