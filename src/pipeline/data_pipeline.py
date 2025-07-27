# Standard Library
from queue import Full, Queue, Empty
from typing import Dict, Union, Optional, Literal, Tuple

# CUSTOM LIBRARY
from logger.set_logger import operation_logger


class DataPipeline:
    def __init__(
        self,
    ) -> None:
        """
        # func __init__:
            # Creates a Queue object of Dict to store different technical indicators data.
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
        self.queues: Dict[str, Queue[Tuple[Dict[int, float]]]] = {
            "price": Queue(
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
        data: Tuple[Dict[int, float]],
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
                block = False,
                timeout = 1,
            )
            return True
        except Full:
            operation_logger.warning(f"{__name__} - {type} Queue is full. Data cannot be added.")
            return False
        except KeyError:
            operation_logger.warning(f"{__name__} - push_data(): Invalid Queue Type.")
            return False
        except Exception as e:
            operation_logger.warning(f"{__name__} - {type} Queue: Unknown exception has occurred: {str(e)}")
            return False

    def pop_data(
        self,
        type: Union[
            Literal["test"],
            Literal["sma"],
            Literal["ema"],
            Literal["price"],
        ],
        block: bool = True,
        timeout: int | None = None
    ) -> Tuple[Dict[int, float]] | None:
        """
        # func pop_data():
            # get the data from the queue with the given type.
        
        # param self
            # class object
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
            # return data if there is a valid data.
        """
        try:
            data: Tuple[Dict[int, float]] = self.queues[type].get(block = block, timeout = timeout)
            return data
        except Empty:
            operation_logger.warning(f"{__name__} - {type} Queue is empty. Data cannot be retrieved.")
            return None
        except KeyError:
            operation_logger.warning(f"{__name__} - pop_data(): Invalid Queue Type - type_input: {type}")
            return None
        except Exception as e:
            operation_logger.warning(f"{__name__} - {type} Queue: Unknown exception has occurred: {str(e)}.")
            return None
