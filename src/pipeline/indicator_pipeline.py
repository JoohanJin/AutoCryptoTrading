# Standard Library
from queue import Queue, Full, Empty
from typing import Literal, Optional, Dict, Queue

# Custom Library
from logger.set_logger import logger
from manager.strategy_manager import TradeSignal # TODO: Need to define this class in another class

class IndicatorPipeline:
    def __init__(self):
        self.indicator_queue: Queue[Dict[float, TradeSignal]] = Queue
        return