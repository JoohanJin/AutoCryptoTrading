from typing import Dict

from src.object.constants import IndexType


class Index:
    '''
    json-like dictionary object

    1.
    ema/sma
    three different kinds of queue -> hard to extend
    {
        "timestamp": int(time.time() * 1000),
        "data": {
            10: <value>
            30: <value>
            60: <value>
            300: <value>
            600: <value>
            1200: <value>
            1800: <value>
        }
    }

    price
    {
        "timestamp": int(time.time() * 1000) # ms based timestamp
        "data": <value>
    }


    2. -> this one looks balanced - v
    how about one json with all consolidated field.
    e.g.,
    one queue -> one data object -> one queue
    non-uniform data structure
    data
    {
        ema: {
            "timestamp": int(time.time() * 1000),
            "data": {
                10: <value>
                30: <value>
                60: <value>
                300: <value>
                600: <value>
                1200: <value>
                1800: <value>
            }
        },
        sma: {
            "timestamp": int(time.time() * 1000),
            "data": {
                10: <value>
                30: <value>
                60: <value>
                300: <value>
                600: <value>
                1200: <value>
                1800: <value>
            }
        },
        currPrice: {
            "timestamp": int(time.time() * 1000),
            "data": <value>
        }
    }

    3.
    one queue, the same data structure
    -> too many?
    data
    {
        ema_10: {
            "timestamp": int(time.time() * 1000),
            "data": <value>
        },
        ema_30: {
            "timestamp": int(time.time() * 1000),
            "data": <value>
        },
        ema_60: {
            "timestamp": int(time.time() * 1000),
            "data": <value>
        },...
        # the same implementation for sma and ema
    }


    FINAL

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
    def __init__(
        self: 'Index',
        data: Dict[str, int | IndexType | Dict[int, float]],
    ) -> None:
        INDEXES: Dict[str, int | IndexType | Dict[int, float]] = data
        return
