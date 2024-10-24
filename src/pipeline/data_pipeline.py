# Standard Library
from queue import Full, Queue, Empty
from typing import Union, Optional, Literal, Tuple

# CUSTOM LIBRARY
from src.set_logger import logger



class DataPipeline:
    def __init__(
        self,
    ) -> None:
        # data buffer
        self.queues = {
            "test": Queue(
                maxsize=100,
            ),
            "sma": Queue(
                maxsize = 100,
            ),
            "ema": Queue(
                maxsize = 100,
            ),
            "?": Queue(
                maxsize = 100,
            ),
        }

        return

    def push_data(
        self,
        type: Union[
            Literal["test"], # only this one is used for the test phase.
            Literal["sma"],
            Literal["ema"],
            Literal["?"],
        ],
        data: Tuple[float],
    ) -> bool:
        try:
            self.queues[type].put(
                data,
                block = True,
                timeout = 1
            )
            return True
        except Full:
            logger.warning(f"{__name__} - {type} Queue is full. Data cannot be added.")
            return False
        except KeyError:
            logger.warning(f"{__name__} - push_data(): Invalid Queue Type.")
            return False
        except Exception as e:
            logger.warning(f"{__name__} - {type} Queue: Unknown exception has occurred: {str(e)}")
            return False

    def pop_data(
        self,
        type: Union[
            Literal["test"],
            Literal["sma"],
            Literal["ema"],
            Literal["?"],
        ],
        block: bool = False,
    ) -> Optional[Tuple[float]]:
        try:
            data: Tuple[float] = self.queues[type].get(block = block)
            return data
        except Empty:
            logger.warning(f"{__name__} - {type} Queue is empty. Data cannot be retrieved.")
            return None
        except KeyError:
            logger.warning(f"{__name__} - pop_data(): Invalid Queue Type.")
            return None
        except Exception as e:
            logger.warning(f"{__name__} - {type} Queue: Unknown exception has occurred: {str(e)}.")
            return None
