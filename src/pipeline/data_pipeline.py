# Standard Library
from queue import Full, Queue, Empty
from typing import Union, Optional, Literal, Tuple

# CUSTOM LIBRARY
from logger.set_logger import logger


class DataPipeline:
    def __init__(
        self,
    ) -> None:
        """
        # func __init__:
            # Creates a dictionary of Queue objects to store different technical indicators data.
            # Each queue has a maximum size of 100 elements to maintain a rolling window of historical values.
        
        # queues:
            # test: general testing data.
            # sma: Simple Moving Average Values.
            # ema: Exponential Moving Average Values.
            # "?" : Purpose to be defined.
        
        # param self

        # return None
        """
        # data buffer, can be added in the future.
        self.queues: Queue[Tuple[float]] = {
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
        """
        # func push_data:
            # pushes the data to the corresponding queue based on the type.
            # will be used by data fetcher.
        
        # param self
        # param type
            # will get the key value for self.queues to seletively push the data into the respective queue.
            # Enum:
                # "test"
                # "sma"
                # "ema"
                # "?"

        # param data
            # Tuple[float]

        # return bool
            # return True if the operation is successful.
            # return False if the operation is not successful.
        """
        try:
            self.queues[type].put(
                data,
                block = True,
                timeout = 1,
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
        timeout: int | None = None
    ) -> Optional[Tuple[float]]:
        """
        # func pop_data
            # get the data from the 
        
        # param self
        # param type
            # will get the key value for self.queues to seletively push the data into the respective queue.
            # Enum:
                # "test"
                # "sma"
                # "ema"
                # "?"
                # More queue with keywords will be added.

        # param data
            # Tuple[float]

        # return bool
            # return True if the operation is successful.
            # return False if the operation is not successful.
        """
        try:
            data: Tuple[float] = self.queues[type].get(block = block, timeout = timeout)
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
