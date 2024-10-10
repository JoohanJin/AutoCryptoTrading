# Standard Module
import time
import asyncio
from typing import Literal, Optional, Union, Tuple
import pandas as pd 
import numpy as np
import threading
from queue import Queue
import sys

# Custom Module
from mexc import future
from set_logger import logger, log_decorator

class strategyManager:
    def __init__(
        self,
        ws_name: Optional[str] = "strategyManager", # no need to authenticate1
        # provide the list of strategy as variable
        # so that it can subscribe different values at the initiation.
    ) -> None:
        """
        :Function Name: __init__() for StrategyManager
        """
        # it will automatically connect the websocket to the host
        # and will continue to keep the connection between the client and host
        # no need to login, no need to provide api_key and secret_key
        self.ws = future.WebSocket()
        self.ma_period: int = 10 # set the period of moving average, in minute

        # wait till WebSocket set up is done
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

        # start the thread for the data fetch from the API
        threading.Thread(target=self.append_df, daemon=True).start()
        threading.Thread(target=self.calculate_sma_thread, daemon=True).start()
        return
    
    def _put_data_buffer(
        self,
        msg: dict,
    ) -> None:
        """
        Put price data of the crypto into the buffer.

        :param:
            :msg: response from the websockt client, put it into the buffer.

        :returns: None in python, it put the value into the buffer and return nothing.
        """
        self.q.put(msg.get('data'), block=False, timeout=None)
        return
    
    def _get_data_buffer(self) -> dict:
        try:
            result = self.q.get(block = True)
            self.q.task_done()
            return result
        except Exception as e:
            print(f"Error retreving data from queue: {e}")
            return None

    @log_decorator
    def _append_df(self) -> None:
        '''
            Continuously fetches data from the queue, processes it and appends it to the DataFrame.
        '''
        # consider append each data into the list and convert it to df periodically.
        # buffer: list = list()
        # buffer_size: int = 3
        while True:
            try:
                response: dict = self.get_data_buffer()
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
            finally:
                self.df_lock.release()
                logger.info("self.df_lock has been released")
        return
    
    def _calculate_sma_thread(self):
        while True:
            sma = self.__calculate_smas()
            if sma:
                print(sma)
            time.sleep(1)
    
    @log_decorator
    def __calculate_smas(self) -> Optional[Tuple[float]]:
        """
        Calculate the simple moving average (SMA) of the lastPrice

        :returns: The calculated SMA or None if there is not enough data
        """
        self.df_lock.acquire()

        try:
            if (self.dataFrame.shape[0] < self.ma_period):
                print("None")
                return
            
            sma_5 = self.dataFrame['lastPrice'].tail(5).astype(float).mean()
            sma_10 = self.dataFrame['lastPrice'].tail(10).astype(float).mean()
            sma_15 = self.dataFrame['lastPrice'].tail(15).astype(float).mean()
            sma_20 = self.dataFrame['lastPrice'].tail(20).astype(float).mean()

            return sma_5, sma_10, sma_15, sma_20
        finally:
            self.df_lock.release()
            logger.info("self.df_lock has been released")
            return


if __name__ == "__main__":
    s: strategyManager = strategyManager()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Program interrupted by user. Exiting...")
        sys.exit(0)