# Standard Library
import queue
from typing import Dict, Tuple

# CUSTOM LIBRARY
from logger.set_logger import operation_logger
from object.constants import IndexType
from object.indexes import Index
from .base_pipeline import BasePipeline


class DataPipeline(BasePipeline[Index]):  # TODO: Make the object for th Data object.
    def __init__(
        self,
    ) -> None:
        '''
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
                0 = <float>,
            }
        }
        '''
        # inherit the queue and data type in the queue from the base class.
        super().__init__()
        # data buffer, can be added in the future.

        return

    def push(
        self,
        data: Dict[str, int | str | Dict[int, float]],
        block: bool = False,
        timeout: int = 1,  # 1 second
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

        param self:
            - class object
        param data:
            - Tuple[float]
        param block:
            - if the thread will be spinning-wait for the data or not.
        param timeout:
            - give the timeout for the data pop.
            - default is None, for non-Time out.

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
