from typing import Dict


class Indexes:
    '''
    json-like dictionary object

    1.
    ema/sma
    three different kinds of queue -> hard to extend
    {
        "timestamp": str(int(time.time() * 1000)),
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
        "timestamp": str(int(time.time() * 1000)) # ms based timestamp
        "data": <value>
    }


    2. -> this one looks balanced
    how about one json with all consolidated field.
    e.g.,
    one queue -> one data object
    non-uniform data structure
    data
    {
        ema: {
            "timestamp": str(int(time.time() * 1000)),
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
            "timestamp": str(int(time.time() * 1000)),
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
            "timestamp": str(int(time.time() * 1000)),
            "data": <value>
        }
    }

    3.
    one queue, the same data structure
    -> too many?
    data
    {
        ema_10: {
            "timestamp": str(int(time.time() * 1000)),
            "data": <value>
        },
        ema_30: {
            "timestamp": str(int(time.time() * 1000)),
            "data": <value>
        },
        ema_60: {
            "timestamp": str(int(time.time() * 1000)),
            "data": <value>
        },...
        # the same implementation for sma and ema
    }
    '''
    INDEXES: Dict[
        str,
        Dict[
            str,
            float | Dict[
                int | str,
                float
                ]
            ]
        ] = dict()

    def push(
        self,
    ):
        return
    
    def pop(
        self,
    ):
        return
