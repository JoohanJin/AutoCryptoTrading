from enum import IntFlag

class TradeSignal(IntFlag):
    # state management using the bit manipulation.
    SHORT_TERM_BUY: int = 1 # 0001
    LONG_TERM_BUY: int = 2 # 0010
    SHORT_TERM_SELL: int = 4 # 0010
    LONG_TERM_SELL: int = 8 # 0100
    HOLD: int = 16 # 1000