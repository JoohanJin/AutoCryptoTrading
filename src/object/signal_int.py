from enum import IntFlag

class TradeSignal(IntFlag):
    # state management using the bit manipulation.
    BUY: int = 1 # 001
    SELL: int = 2 # 010
    HOLD: int = 4 # 100 # Do nothing