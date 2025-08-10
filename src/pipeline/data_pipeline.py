# Standard Library
import queue
from typing import Dict, Tuple, Queue

# CUSTOM LIBRARY
from logger.set_logger import operation_logger
from src.object.constants import IndexType
from src.object.indexes import Index
from .base_pipeline import BasePipeline


class DataPipeline(BasePipeline[Dict]):  # TODO: Make the object for th Data object.
    def __init__(
        self,
    ) -> None:
        '''
        func __init__:
            - Creates a Queue object of Dict to store different technical indicators data.
            - Each queue has a maximum size of 100 elements to maintain a rolling window of historical values.
        queues:
            - test: general testing data.
            - sma: Simple Moving Average Values.
            - ema: Exponential Moving Average Values.
            - "?" : Purpose to be defined.
        param self

        return None

        Exi

        data_struct = {
            "price":{
                "price": <float>
            }
            "ema": {
                0: <float>
            }
            "sma":{
                0: <float>
            }
        }

        OR

        so each of them is just a data object pushed to the queue, not a group of data.

        data_struct = {
            "timestamp" = <int>, # int(time.time() * 1_000)
            "type" = "ema" || "sma",
            "data" = {
                10: <float>,
                30: <float>,
                60: <float>,
                300: <float>,
                600: <float>,
                1_200: <float>,
                1_800: <float>,
            }
        }

        AND

        data_struct = {
            "timestamp" = <int>, # int(time.time() * 1_000)
            "type" = "price",
            "data" = {
                "0" = <float>,
            }
        }
        '''
        self.queue: Queue[Dict[str, int | IndexType | Dict[int, float]]] = Queue.queue()
        # data buffer, can be added in the future.

        return

    def push(
        self,
        data: Dict[str, int | str | Dict[int, float]],
        block:  bool = False,
        timeout: int | None = 1,
    ) -> bool:
        '''
        func push_data:
            - pushes the data to the corresponding queue based on the key.
            - will be used by data fetcher.
        param self
        param key
            - will get the key value for self.queues to seletively push the data into the respective queue.
            - Enum:
                - "test"
                - "sma"
                - "ema"
                - "?"

        param data
            - Tuple[float]

        return bool
            - return True if the operation is successful.
            - return False if the operation is not successful.
        '''
        try:
            self.queue.push(
                data,
                block = block,
                timeout = timeout,
            )
            return True
        except queue.Full:
            operation_logger.warning(f"{__name__} - Queue is full. Data cannot be added.")
            return False
        except Exception as e:
            operation_logger.warning(f"{__name__} - self.queue: Unknown exception has occurred: {str(e)}")
            return False

    def pop(
        self,
        block: bool = True,
        timeout: int | None = None
    ) -> Dict[str, int | IndexType | Dict[int, float]]:
        '''
        func pop_data():
            - get the data from the queue with the given key.

        param self
            - class object
        param key
            - will get the key value for self.queues to seletively push the data into the respective queue.
            - Enum:
                - "test"
                - "sma"
                - "ema"
                - "?"
                - More queue with keywords will be added.

        param data
            - Tuple[float]

        return bool
            - return data if there is a valid data.
        '''
        try:
            return self.queue.pop(block = block, timeout = timeout)
        except queue.Empty:
            operation_logger.warning(f"{__name__} - self.queue is empty: Data cannot be retrieved.")
            return None
        except Exception as e:
            operation_logger.warning(f"{__name__} - self.queue: Unknown exception has occurred: {str(e)}.")
            return None
