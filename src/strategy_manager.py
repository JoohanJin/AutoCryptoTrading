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
from data_saver import DataSaver
from custom_telegram.telegram_bot_class import CustomTelegramBot

class strategyManager:
    def __init__(
        self,
        # provide the list of strategy as variable
        # so that it can subscribe different values at the initiation.
    ) -> None:
        """
        :Function Name: __init__() for StrategyManager
        """
        # it will automatically connect the websocket to the host
        # and will continue to keep the connection between the client and host
        # no need to provide api_key and secret_key, i.e., no authentication on API side
        self.ws = future.WebSocket()
        self._ma_period: int = 20 # set the period of moving average
        self._memory_saver = DataSaver()
        self._df_size_limit = 100

        self.__telegram_bot = CustomTelegramBot()

        self.loop = asyncio.get_event_loop()

        # wait till WebSocket set up is done
        time.sleep(1)

        # multi-thrading based queue
        # used as a buffer for data fetching from the MEXC Endpoint
        self.price_q = Queue()

        self.ws.ticker(
            # callback = print, # for debugging purpose
            callback=self._put_data_buffer
        )

        # mutex lock
        self.df_lock = threading.Lock()

        # default dataframe with the given columns
        self.dataFrame = pd.DataFrame(
            data = [],
            columns = [
                'symbol', 'lastPrice', 'riseFallRate', 'fairPrice', 'indexPrice',
                'volume24', 'amount24', 'maxBidPrice', 'minAskPrice', 'lower24Price', 
                'high24Price', 'bid1', 'ask1', 'holdVol', 'riseFallValue',
                'fundingRate', 'zone', 'riseFallRates', 'riseFallRatesOfTimezone'
            ],
            index = [int(time.time() * 1000)]
        )
        # self.dataFrame.set_index("timestamp")
        self.dataFrame.index.name = "timestamp"

        # start the thread for the data fetch from the API
        threading.Thread(target=self._price_data_fetch, daemon=True).start()
        logger.info("Thread for price fetch has been started")
        threading.Thread(target=self._calculate_sma_thread, daemon=True).start()
        logger.info("Thread for calculating sma has been started")
        threading.Thread(target=self._resize_df, daemon=True).start()
        logger.info("Thread for DataFrame size limit has been started")
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
        self.price_q.put(msg.get('data'), block=False, timeout=None)
        return
    
    def _get_data_buffer(self) -> Optional[dict]:
        try:
            result = self.price_q.get(block = True)
            self.price_q.task_done()
            return result
        except Exception as e:
            print(f"Error retreving data from queue: {e}")
            return None

    def _price_data_fetch(self) -> None:
        '''
            Continuously fetches data from the queue, processes it and appends it to the DataFrame.
        '''
        # consider append each data into the list and convert it to df periodically.
        # data_buffer: list = list()
        # timestamp_buffer: list = list()
        # buffer_size: int = 3
        while True:
            try:
                response: dict = self._get_data_buffer()
                if response:
                    # TODO: store 'riseFallRates' and 'riseFallRatesTimezone'
                    timestamp = response['timestamp']
                    # timestamp_buffer.append(timestamp)
                    # data_buffer.append(response)

                    tmp = pd.DataFrame(
                        data = [response],
                    )

                    tmp.set_index("timestamp", inplace = True)
                    # tmp.index.name = "timestamp"


                    with self.df_lock:
                        self.dataFrame=pd.concat([self.dataFrame, tmp], axis=0)

                    # if (len(data_buffer) >= buffer_size):
                    #     self.__append_df(
                    #         data_buffer=data_buffer,
                    #         timestamp_buffer=timestamp_buffer,
                    #     )
            except Exception as e:
                print(f"Unexpected Error Occurred in function \"_price_data_fetch\": {e}")
        return

    def __append_df(
        self, 
        data_buffer: list,
        timestamp_buffer: list,
    ) -> bool:
        try:
            tmp = pd.DataFrame(
                data_buffer,
                index = [timestamp_buffer],
            )
            with self.df_lock:
                self.dataFrame=pd.concat([self.dataFrame, tmp], axis=0)
            return True
        except Exception as e:
            return False 
        finally:
            data_buffer.clear()
            timestamp_buffer.clear()

    
    def _calculate_sma_thread(self) -> None:
        while True:
            sma_values = self.__calculate_smas()
            if sma_values:
                sma_5, sma_10, sma_15, sma_20 = sma_values
                message: str = f"SMA Update:\nSMA5: {sma_5:.2f}\nSMA10: {sma_10:.2f}\nSMA15: {sma_15:.2f}\nSMA20: {sma_20:.2f}"
                asyncio.run(self.send_telegram_message(message))
            time.sleep(2)
            # now do something with sma
        return
    
    def __calculate_smas(self) -> Optional[Tuple[float]]:
        """
        Calculate the simple moving average (SMA) of the lastPrice

        :returns: The calculated SMA or None if there is not enough data
        """
        self.df_lock.acquire()

        try:
            if (self.dataFrame.shape[0] < self._ma_period):
                # print("None")
                return
            
            sma_5 = self.dataFrame['lastPrice'].tail(5).astype(float).mean()
            sma_10 = self.dataFrame['lastPrice'].tail(10).astype(float).mean()
            sma_15 = self.dataFrame['lastPrice'].tail(15).astype(float).mean()
            sma_20 = self.dataFrame['lastPrice'].tail(20).astype(float).mean()


            return sma_5, sma_10, sma_15, sma_20
        except Exception as e:
            logger.warnning(f"from {__name__}, function: {self}.__calculate_smas has has raised the Exception")
            return False
        finally:
            self.df_lock.release()
        return
    
    def _resize_df(self) -> None:
        """
        :func: __save_data()
            : using _data_saver to move the dataframe stroing the price movement to the csv file in data
        
        :make a use of data saver, i.e., custom class using the df.to_csv()
        """
        while True:
            time.sleep(40)
            if self.dataFrame.shape[0] > 20:
                with self.df_lock:
                    data = self.dataFrame.iloc[:-20]
                    self.dataFrame = self.dataFrame.iloc[-20:]
                self._memory_saver.write(data)
        return
    
    async def send_telegram_message(self, message: str)-> None:
        try:
            await self.__telegram_bot.send_text(message)
        except Exception as e:
            logger.debug(f"Error sending Telegram message: {e}")


if __name__ == "__main__":
    s: strategyManager = strategyManager()
    try:
        s.loop.run_forever()
    except KeyboardInterrupt:
        logger.info("Program interrupted by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        logger.debug(f"Program encounters critical errors.{e}\n Exiting...")
        sys.exit(0)