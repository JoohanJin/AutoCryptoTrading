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
from mexc.future import FutureWebSocket
from logger.set_logger import logger, log_decorator
from data_saver import DataSaver
from custom_telegram.telegram_bot_class import CustomTelegramBot
from pipeline.data_pipeline import DataPipeline

class DataCollectorAndProcessor:
    def __init__(
        self,
        pipeline: DataPipeline
        # provide the list of strategy as variable
        # so that it can subscribe different values at the initiation.
    ) -> None:
        """
        # func __init__() for StrategyManager
            # set the WebSocket() for data fetching
                # set the subscription for the ticker data.
            # set the DataSaver() for control of the DataFrame Size.
            # set the Threads pool for the necessary operations for the Strategy Manager.
            # set the Telegram Bot for the automated log system.
            # set the DataBuffer for the price buffer.
            # set the Price Data Table

        # params self
            # class object
        # params pipeline
            # pipeline to transmit the data to the StrategyManager.

        # return None
        """
        # it will automatically connect the websocket to the host
        # and will continue to keep the connection between the client and host
        # no need to provide api_key and secret_key, i.e., no authentication on API side
        self.ws: FutureWebSocket = FutureWebSocket()
        self._ma_period: int = 20 # set the period of moving average
        self._memory_saver: DataSaver = DataSaver()
        self._df_size_limit: int = 1_000
        self.threads: list[threading.Thread] = list()
        self.pipeline: DataPipeline = pipeline

        # wait till WebSocket set up is done
        time.sleep(1)

        # used as  buffer for data fetching from the MEXC Endpoint
        self.price_fetch_buffer = Queue()

        # subsribe to the ticker data from the MexC data
        self.ws.ticker(
            callback=self._put_ticker_data
        )

        # lock for accessing Price DataFrame.
        self.df_lock = threading.Lock()

        # default dataframe with the given columns
        self.priceData: pd.DataFrmae = pd.DataFrame(
            data = [],
            columns = [
                'symbol', 'lastPrice', 'riseFallRate', 'fairPrice', 'indexPrice',
                'volume24', 'amount24', 'maxBidPrice', 'minAskPrice', 'lower24Price', 
                'high24Price', 'bid1', 'ask1', 'holdVol', 'riseFallValue',
                'fundingRate', 'zone', 'riseFallRates', 'riseFallRatesOfTimezone'
            ],
            index = [int(time.time() * 1000)]
        )
        self.priceData.index.name = "timestamp"

        self._init_threads()
        self._start_threads()
        return
    
    """
    ######################################################################################################################
    #                                               Threading Management                                                 #
    ######################################################################################################################
    """
    def _init_threads(self) -> None:
        """
        # func _init_threads():
            # set the threads for the necessary operations and append them into the list of thread pool

        # params self
            # class object

        # return None

        # The list of threads are as follows:
            :price fetching
                :get the price from the broker
            :calculate the simple moving average
                :calculate the simple moving average based on the 
            :memory saver 
                :used to control the size of the Price DataFrame.

        :return None:
        """
        # start the thread for the data fetch from the API
        thread_price_fetch: threading.Thread = threading.Thread(
            name = "price_data_fetch",
            target = self._price_data_fetch,
            daemon = True
        )
        logger.info(f"{__name__}: Thread for price fetch has been set up!")

        thread_calculate_sma: threading.Thread = threading.Thread(
            name = "calculate_sma_thread",
            target = self._calculate_moving_averages,
            daemon = True,
        )
        logger.info(f"{__name__}: Thread for calculating sma has been set up!")

        thread_memory_save: threading.Thread = threading.Thread(
            name= "resize_df",
            target=self._resize_df,
            daemon=True
        )
        logger.info(f"{__name__}: Thread for DataFrame size limit has been set up!")

        self.threads.extend([thread_price_fetch, thread_calculate_sma, thread_memory_save])
        return

    def _start_threads(self) -> None:
        """
        # func _start_threads():
            # start the threads in the thread pool of the class.
            # Will raise issues if there is  problem with the triggering of the thread.
        
        # param self: dataCollectorAndProcessor
            # class object

        # return None
        """
        for thread in self.threads:
            try:
                thread.start()
                logger.info(f"{__name__}: Thread '{thread.name}' (ID: {thread.ident}) has started")
            except RuntimeError as e:
                logger.critical(f"{__name__}: Failed to start thread '{thread.name}': {str(e)}")
                raise RuntimeError
            except Exception as e:
                logger.critical(f"{__name__}: Unexpected error starting thread: '{thread.name}': {str(e)}")
                raise
        return

    """
    ######################################################################################################################
    #                                     Get Ticker Data and Put Them in the Buffer                                     #
    ######################################################################################################################
    """
    def _put_ticker_data(
        self,
        msg: dict,
    ) -> None:
        """
        # func _put_ticker_data():
            # Put price data of the crypto into the buffer.

        # param self: DataCollectorAndProcessor
            # class object
        # param msg: dict
            # message from the MexC API, json format, but parsed as python dict.

        # return None
        """
        try:
            self.price_fetch_buffer.put(
                msg.get('data'),
                block = False,
                timeout = None,
            )
        except Exception as e:
            logger.critical(
                f"{__name__}: Error in class {self.__class__.__name__} in method _put_ticker_data(): {e}"
            )
        return
    
    """
    ######################################################################################################################
    #                                   Get the Ticker Data from the Data Buffer                                         #
    ######################################################################################################################
    """
    def _price_data_fetch(self) -> None:
        '''
        # func _price_data_fetch():
            # It continuously fetches data from the queue, processes it and appends it to the DataFrame.
            # the processing includes the followings:
                # change the data to a dataframe
                # get the timestamp
                # set the timestamp as an index of the dataframe
                # concatenate the dataframe to the entire data buffer.
        '''
        while True:
            try:
                response: dict = self._get_data_buffer() # data from the data buffer
                if response:
                    # TODO: store 'riseFallRates' and 'riseFallRatesTimezone'
                    timestamp = response['timestamp']

                    # make the data, dictionary, into the pandas dataframe.
                    tmp = pd.DataFrame(
                        data = [response],
                    )

                    # set the timestamp as the index of the dataframe.
                    tmp.set_index(
                        "timestamp",
                        inplace = True
                    )

                    # merge the new dataframe to the existing dataframe.
                    with self.df_lock:
                        self.priceData = pd.concat(
                            [self.priceData, tmp],
                            axis=0
                        )

            except Exception as e:
                logger.critical(f"Unexpected Error Occurred in function \"_price_data_fetch\": {e}")
        return
    
    def _get_data_buffer(self) -> Optional[dict]:
        """
        # func _get_data_buffer():
            # Get the data from the buffer and return it.
            # if there is no data in the buffer, then wait until the data is available.
            # if there is an error then, return None
        """
        try:
            result = self.price_fetch_buffer.get(block = True)

            self.price_fetch_buffer.task_done()

            return result
        except Exception as e:
            logger.critical(f"{__name__} - Error retreving data from queue: {e}")
            return None

    # for batch processing of the data.
    def __append_df(
        self, 
        data_buffer: list,
        timestamp_buffer: list,
    ) -> bool:
        """
        # func __append_df():
            # Make the data as an Pandas dataframe.
            # store the dataframe into the list, for the batch processing
        """
        try:
            tmp = pd.DataFrame(
                data_buffer,
                index = [timestamp_buffer],
            )
            with self.df_lock:
                self.priceData=pd.concat([self.priceData, tmp], axis=0)
            return True
        except Exception as e:
            return False 
        finally:
            data_buffer.clear()
            timestamp_buffer.clear()

    """
    ######################################################################################################################
    #                                  Calculate the SMAs Using Data From the Buffer                                     #
    ######################################################################################################################
    """
    def _calculate_moving_averages(self) -> None:
        """
        # func _calculate_moving_averages():
            # call the function __calculate_ema_sma() to calculate the EMA and SMA
            # get tuple of data where:
                # data[0] = SMA values
                # data[1] = EMA values
            # when the data is available, push the data to the data pipeline.
        """
        while True:
            data: Tuple[Tuple[float]] | None = self.__calculate_ema_sma()

            if data:
                sma_values = data[0]
                ema_values = data[1]

            # TODO: need to change -> other wrapper which can get the result and push to the data pipeline.
                if (sma_values): self.__push_sma_data(sma_values)
                if (ema_values): self.__push_ema_data(ema_values)

            time.sleep(2)
        return
    
    def __calculate_ema_sma(
        self,
        periods: Tuple[int] = (
            5, # 10 sec
            15, # 30 sec
            30, # 1 min
            150, # 5 min
            300, # 10 min
            # 600, # 20 min
            # 900, # 30 min
        ),
    ) -> Optional[Tuple[Tuple[float], Tuple[float]]]:
        """
        # func __calculate_ema_sma():
            # It calculate the simple moving average (SMA) of the lastPrice

        # params self: DataCollectorAndProcessor
            # class object
        # params periods: Tuple[int]
            # periods for the calculation of the SMA and EMA

        # return (smas, emas): Tuple[Tuple[float], Tuple[float]] | None
            # Tuple of SMA and EMA values
        """

        try:
            with self.df_lock:
                if (self.priceData.shape[0] < periods[-1]):
                    return None

                tmpDataframe = self.priceData[-periods[-1]:]["lastPrice"].copy()

            smas = tuple(np.mean(tmpDataframe[-period:]) for period in periods)
            emas = tuple(pd.Series(tmpDataframe).ewm(span=period, adjust = False).mean().iloc[-1] for period in periods)
        
            return smas, emas

        except KeyError as e:
            # Specific error handling for KeyError, i.e., missing collumn
            logger.error(f"{__name__}: function {self.__class__.__name__}.__calculate_ema_sma has raised the KeyError: {e}")
            return None
        
        except IndexError as e:
            # Specific error handling for IndexError, i.e., out of range and slicing of the DataFrame.
            logger.error(f"{__name__}: function {self.__class__.__name__}.__calculate_ema_sma has raised the IndexError: {e}")
            return None

        except Exception as e:
            logger.warning(f"{__name__}: function {self.__class__.__name__}.__calculate_ema_sma has has raised the Unknown Exception.")
            return None
        

    
    """
    ######################################################################################################################
    #                                  Resize the DataFrame holding the Price Info                                       #
    ######################################################################################################################
    """
    def _resize_df(self) -> None:
        """
        # func: __resize_df()
            # using _data_saver to move the dataframe storing the price movement to the csv file in data
        
        # make a use of data saver, i.e., custom class using the df.to_csv()

        # params self: DataCollectorAndProcessor
            # class object

        # return None
        """
        while True:
            data = None
            try:
                with self.df_lock:
                    if (self.priceData.shape[0] > self._df_size_limit):
                        data = self.priceData.iloc[:-self._df_size_limit]
                        self.priceData = self.priceData.iloc[-self._df_size_limit:]
                    else:
                        logger.warning(f"Data Saver has not stored the recent price data, since the data size is below the threshold: {self.priceData.shape[0]}")

                if (data is not None):
                    self._memory_saver.write(data)
                    logger.info(f"Data Saver has stored the recent price data: size: {data.shape[0]} rows and {data.shape[1]} columns")
                time.sleep(149.9) # make an adjustment.

                return None
            
            except Exception as e:
                logger.warning(f"{__name__}: _resize_df - Exception caused: {e}")

        return None
    
    """
    ######################################################################################################################
    #                                        Push Data to the Data Pipeline                                              #
    ######################################################################################################################
    """
    def __push_ema_data(
        self,
        data: Tuple[float],
    ) -> bool:
        return self.pipeline.push_data(
            type = 'ema',
            data = data
        )
    
    def __push_sma_data(
        self,
        data: Tuple[float],
    ) -> bool:
        return self.pipeline.push_data(
            type = 'sma',
            data = data
        )