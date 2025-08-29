import time
from typing import Dict

from object.constants import IndexType


class Index:
    '''
    json-like dictionary object

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
        "type" = <IndexType>,
        "data" = {
            "0" = <float>,
        }
    }
    '''
    @staticmethod
    def generate_timestamp() -> int:
        return int(time.time() * 1_000)

    def __init__(
        self: 'Index',
        index: Dict[str, IndexType | Dict[int, float]],
    ) -> None:
        self._timestamp: int = index.get("timestamp", Index.generate_timestamp())
        self._index_type: IndexType = index.get("type", None)  # if there is no data, type
        self._index: Dict[str, Dict[int, float]] = index.get("data", None)
        return

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def index(self):
        return self._index

    @property
    def index_type(self):
        return self._index_type
