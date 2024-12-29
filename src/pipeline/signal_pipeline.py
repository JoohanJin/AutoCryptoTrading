# Standard Library
from queue import Queue, Full, Empty
from typing import Literal, Optional, Dict, Any

# Custom Library
from logger.set_logger import logger
from object.signal_int import TradeSignal # TODO: Need to define this class in another class

class SignalPipeline:
    def __init__(self):
        """
        # func __init__:
            # create a Queue of Dict to store indicator
            # Queue has a maximum size of 100 elements to maintain a rolling window of historical indicators.

        # queue:
            # indicator_queue: indicator buffer

            indicator = {
                "indicator": {
                    "timestamp": <int>, int(time.time() * 1000),
                    "signal": <object.TradeSignal
                        # 001: for buy
                        # 010: for sell
                        # 100: for hold -> do nothing
                }
            }
        """
        self.indicator_queue: Queue[Dict[str, Dict[str, Any]]] = Queue()
        return
    
    def push_indicator(
        self,
        indicator: Dict[str, Dict[str, Any]],
    ) -> bool:
        return
    
    def pop_indicator(
        self,
        indicator: Dict[str, Dict[str, Any]],
        timeout: int | None = None,
        block: bool = True,
    ) -> Dict[str, Dict[str, Any]] | None:
        """
        # func pop_indicator():
            # get the indicator from the buffer.

        # param self
            # class object
        # param indicator
            # indicator got as a parameter.
            # Dict[str, Dict[str, Any]]
        # param timeout
            # the timeout value for getting indicator from the queue.
        # param block
            # the boolean value to indicate if the queue is blocked or not when we get the data.

        # return bool
            # return indicator if there is a valid indicator.
        """
        try:
            return self.queue.get(
                block = block,
                timeout = timeout,    
            )
        except Empty:
            logger.warning(f"{__name__} -  Indicator Queue is empty. Data cannot be added.")
            return None
        except Exception as e:
            logger.warning(f"{__name__} - Indicator Queue: Unknown exception has occurred: {str(e)}")
            return None