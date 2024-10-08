'''
For Strategy Manager for the Auto-Trading Bot, the MexC websocket api will be used for
continous data fetching to establish the trading strategy.
'''

# Standard Module
import time
import asyncio
from typing import Literal, Optional, Union
import pandas as pd 
import numpy as np
import threading
from queue import Queue

# Custom Module
from mexc import future
from set_logger import logger, log_decorator

class strategyManager:
    def __init__(
        self,
        ws_name: Optional[str] = "strategyManager", # no need to authenticate
        # provide the list of strategy as variable
        # so that it can subscribe different values at the initiation.
        ma_period: Optional[int] = 1, # in minute
    ) -> None:
        # it will automatically connect the websocket to the host
        # and will continue to keep the connection between the client and host
        # no need to login, no need to provide api_key and secret_key
        self.ws = future.WebSocket()

        time.sleep(1)

        # multi-thrading based queue
        # used as a buffer for data fetching from the MEXC Endpoint
        self.q = Queue()

        self.ws.ticker(
            # callback = print, # for debugging purpose
            callback=self.put_data_buffer
        )

        # mutex lock
        self.df_lock = threading.Lock()

        # default dataframe with the given columns
        self.dataFrame = pd.DataFrame(
            columns = [
                'symbol', 'lastPrice', 'riseFallRate', 'fairPrice', 'indexPrice',
                'volume24', 'amoun24', 'maxBidPrice', 'minAskPrice', 'lower24Price', 
                'high24Price', 'timestamp', 'bid1', 'ask1', 'holdVol', 'riseFallValue',
                # 'fundingRate', 'zone', 'riseFallRates', 'riseFallRatesOfTimezone'
            ]
        )

        self.ma_period: int = ma_period # set the period of moving average, in minute

        # start the thread for the data fetch from the API
        threading.Thread(target=self.append_df, daemon=True).start()

        return
    
    def put_data_buffer(
        self,
        msg,
    ) -> None:
        """
        Put price data of the crypto into the buffer.

        :param

        :returns: None in python, it put the value into the buffer and return nothing.
        """
        print(msg.get('data'))
        # self.q.put(msg.get('data'), block=False, timeout=None)
        return
    
    def get_data_buffer(self) -> dict:
        try:
            result = self.q.get(block = True)
            self.q.task_done()
            return result
        except Exception as e:
            print(f"Error retreving data from queue: {e}")
            return None

    def append_df(self) -> None:
        '''

        '''
        # consider append each data into the list and convert it to df periodically.
        while True:
            response = self.get_data_buffer()
            if response:
                # TODO: store 'riseFallRates' and 'riseFallRatesTimezone'
                timestamp = response.pop('timestamp')
                riseFallRates = response.pop('riseFallRates')
                riseFallRatesOfTimezone = response.pop('riseFallRatesOfTimezone')
                fundingRate = response.pop('fundingRate')
                time_zone = response.pop('zone')

                tmp = pd.DataFrame(
                    response,
                    index = [timestamp]
                )

                # edit self.dataFrame: i.e. concat
                self.df_lock.acquire()
                self.dataFrame=pd.concat([self.dataFrame, tmp], axis=0)
                self.df_lock.release()
            else:
                # just ignore if the response returned is None
                pass

        return
    
    def calculate_ma(self) -> Optional[float]:
        """
        Calculate the simple moving average (SMA) of the lastPrice
        """
        return