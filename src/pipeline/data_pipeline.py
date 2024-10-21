# Standard Library
from queue import Full, Queue
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
            # "sma": Queue(
            #     maxsize = 100,
            # ),
            # "ema": Queue(
            #     maxsize = 100,
            # ),
            # "?": Queue(
            #     maxsize = 100,
            # ),
        }

        return

    def push_data(
        self,
        type: Union[
            Literal["test"],
            Literal["sma"],
            Literal["ema"],
            Literal["?"],
        ],
        data: Tuple[float],
    ) -> bool:
        try:
            self.queues[type].put(data)
            return True
        except Full:
            logger.warning(f"{__name__} - {type} Queue is full. Data cannot be added.")
            return False
        except KeyError:
            logger.warning(f"{__name__} - Invalid Queue Type.")
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
        ]
    ) -> Optional[Tuple[float]]:
        try:
            data: Tuple[float] = self.queues[type].get(block = False)

        except Exception as e:

            return None
        finally:
            return data

        return None