from object.signal_int import TradeSignal


class ScoreMapper:
    def __init__(self) -> None:
        self.map: dict = dict(
            {
                TradeSignal.SHORT_TERM_BUY: 1,
                TradeSignal.LONG_TERM_BUY: 2,
                TradeSignal.SHORT_TERM_SELL: -1,
                TradeSignal.LONG_TERM_SELL: -2,
                TradeSignal.HOLD: 0,
            }
        )
        return

    def map(
        self,
        signal: TradeSignal,
    ) -> float:
        return self.map.get(signal, 0)