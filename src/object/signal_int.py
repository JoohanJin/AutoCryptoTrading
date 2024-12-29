from enum import IntFlag

class TradeSignal(IntFlag):
    # state management using the bit manipulation.
    BUY = 1 # 001
    SELL = 2 # 010
    HOLD = 4 # 100 # Do nothing