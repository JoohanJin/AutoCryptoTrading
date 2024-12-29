# STANDARD LIBRARY
import threading
from typing import Dict, Optional, Tuple, Literal, Union, List
import time
from queue import Queue

# CUSTOM LIBRARY
from mexc.future import FutureMarket
from pipeline.data_pipeline import DataPipeline
from pipeline.signal_pipeline import SignalPipeline
from src.custom_telegram.telegram_bot_class import CustomTelegramBot
from logger.set_logger import logger


class StrategyHandler:
    def __init__(
            self,
            data_pipeline: DataPipeline,
            custom_telegram_bot: CustomTelegramBot,
            # signal_pipeline: SignalPipeline,
        ) -> None:
        """
        # func __init__():
            # Initialize the Strategy Handler.
            # It gets the pipeline as a parameter for the indicator fetching.
            # It initializes the telegram bot for the notification.
            # It initializes the threads for the indicator fetching.

        # param self: StrategyHandler
            # class object
        # param pipeline: DataPipeline
            # Data pipeline for the indicator fetching.
        
        # return None
        """
        # data pipeline to get the indicators
        self.data_pipeline: DataPipeline = data_pipeline
        # self.indicator_pipeline: IndicatorPipeline = indicator_pipeline
        
        # telegram bot manager to send the notification.
        self.__telegram_bot: CustomTelegramBot = custom_telegram_bot

        # Shared memory
        # Mutex Lock
        self.indicators_lock: threading.Lock = threading.Lock()
        self.indicators: dict = {
            "sma": None, # Latest SMA data
            "ema": None, # latest EMA data
            "price": None, # latest Price data
        }

        # threads pool
        self.threads: List[threading.Thead] = list()

        # TODO: separate this part as strat()
        # initialize the threads
        self._init_threads()
        # start each thread, which is in the threads pool.
        self._start_threads()

        return

    """
    ######################################################################################################################
    #                                               Static Method                                                        #
    ######################################################################################################################
    """
    @staticmethod
    def generate_timestamp() -> int:
        """
        # static func generate_timestamp():
            # Generate the timestamp using the current time, in the form of epoch in ms.

        # param None

        # return int
            # the timestam in the form of epoch in ms.
        """
        return int(time.time() * 1000)

    """
    ######################################################################################################################
    #                                      Read Data from the Data Pipeline                                              #
    ######################################################################################################################
    """
    def get_test_data(self) -> Optional[Dict[int, float]]:
        """
        # func get_test_data:
            # Get the test data from the data pipeline.
            # It will be used for the testing phase.
            # It will be used by the threads to get the data from the pipeline.

        # param self: StrategyHandler
        
        # return None
        """
        return self.data_pipeline.pop_data(
            type = "test",
            block = True, # if there is no data, then stop the process until the data is available.
            timeout = None,
        )

    def get_smas(self) -> Optional[Dict[int, float]]:
        """
        # func get_smas:
            # Get the sma data from the data pipeline.
            # It will be used by the threads to get the data from the pipeline.

        # param self: StrategyHandler

        # return None
        """
        return self.data_pipeline.pop_data(
            type = "sma",
            block = True, # if there is no data, then stop the process until the data is available.
            timeout = None,
        )
    
    def get_emas(self) -> Optional[Dict[int, float]]:
        """
        # func get_emas:
            # Get the ema data from the data pipeline.
            # It will be used by the threads to get the data from the pipeline.

        # param self: StrategyHandler

        # return None
        """
        return self.data_pipeline.pop_data(
            type = "ema",
            block = True, # if there is no data, then stop the process until the data is available.
            timeout = None,
        )

    def get_price_data(self) -> Optional[Dict[int, float]]:
        """
        # func get_price_data:
            # Get the test data from the data pipeline.
            # It will be used for the testing phase.
            # It will be used by the threads to get the data from the pipeline.

        # param self: StrategyHandler
        
        # return None
        """
        return self.data_pipeline.pop_data(
            type = "price",
            block = True, # if there is no data, then stop the process until the data is available.
            timeout = None,
        )

    """
    ######################################################################################################################
    #                         Send the important message to the Telegram Chat Room as a Logging                          #
    ######################################################################################################################
    """
    async def send_telegram_message(self, message: str)-> None:
        """
        # func send_telegram_message:
            # Send the message to the telegram chat room.
            # It will be used to send the notification to the telegram chat room.

        # param self: StrategyHandler
        # param message: str

        # param None
        """
        try:
            await self.__telegram_bot.send_text(
                message = message,
            )
        except Exception as e:
            logger.error(f"Error sending Telegram message: {e}")

    # this is not used currently
    def generate_telegram_msg(self, data) -> str:
        """
        # func generate_telegram_msg:
            # Generate the message for the telegram chat room.
            # It will be used to generate the message for the telegram chat room.
        
        # param self: StrategyHandler
        # param data: Tuple[float]

        # return str
        """
        return ""
    
    """
    ######################################################################################################################
    #                                                 Threads Management                                                 #
    ######################################################################################################################
    """
    def _init_threads(self):
        """
        # func _init_threads:
            # Initialize the threads for the indicator fetching.
            # It will be used to initialize the threads for the indicator fetching.
        
        # param self: StrategyHandler

        # return None
        """
        sma_thread: threading.Thread = threading.Thread(
            name = "sma_data_getter",
            target = self.get_sma,
            daemon = True,
        )
        logger.info(f"{__name__}: Thread for sma_data_getter has been set up!")

        ema_thread: threading.Thread = threading.Thread(
            name = "ema_data_getter",
            target = self.get_ema,
            daemon = True,
        )
        logger.info(f"{__name__}: Thread for ema_data_getter has been set up!")

        price_thread: threading.Thread = threading.Thread(
            name = "price_data_getter",
            target = self.get_price,
            daemon = True,
        )
        logger.info(f"{__name__}: Thread for price_data_getter has been set up!")

        # add threads into the Threads pool.
        self.threads.extend(
            [
                sma_thread, 
                ema_thread,
                price_thread,
            ]
        )
        return
    
    def _start_threads(self) -> None:
        """
        # func _start_threads():
            # start the threads in the thread pool of the class.
            # will raise issues if there is  problem with the triggering of the thread.
        
        # param self: StrategyHandler
            # class object

        # return None
        """
        for thread in self.threads:
            try:
                # start the thread.
                thread.start()
                logger.info(f"{__name__} - Thread '{thread.name}' (ID: {thread.ident}) has started")
            except RuntimeError as e:
                logger.critical(f"{__name__} - Failed to start thread '{thread.name}': {str(e)}")
                raise
            except Exception as e:
                logger.critical(f"{__name__} - Unexpected error starting thread: '{thread.name}': {str(e)}")
                raise
        return
    
    """
    ######################################################################################################################
    #                                            Functions for Threads                                                   #
    ######################################################################################################################
    """
    def get_sma(self) -> bool:
        """
        # func get_sma():
            # get the sma data from the pipeline and put it into the shared structured.
            # target function of the thread.
        
        # param self: StrategyHandler
            # class object

        # return True if the update is successful.
        # return False if the update is not successful.
        """
        while True:
            data = self.get_smas()
            if (data):
                # update to the shared structure to use them for analysis.
                with self.indicators_lock:
                    self.indicators["sma"] = data
        return
    
    def get_ema(self) -> bool:
        """
        # func get_ema():
            # get the ema data from the pipeline and put it into the shared structured.
            # target function of the thread.
        
        # param self: StrategyHandler
            # class object
        
        # return True if the update is successful.
        # return False if the update is not successful.
        """
        while True:
            data = self.get_emas()
            if (data):
                # update to the shared structure to use them for analysis.
                with self.indicators_lock:
                    self.indicators["ema"] = data
        return
    
    def get_price(self) -> bool:
        """
        # func get_price():
            # get the price data from the pipeline and put it into the shared structured.
            # target function of the thread.
        
        # param self: StrategyHandler
            # class object
        
        # return True if the update is successful.
        # return False if the update is not successful.
        """
        while True:
            data = self.get_price_data()
            if (data):
                # update to the shared structure to use them for analysis.
                with self.indicators_lock:
                    self.indicators["price"] = data
        return
    
    """
    ######################################################################################################################
    #                                                 Signal Generator                                                   #
    ######################################################################################################################
    """
    # TODO: Need to figure out how to make a signal.

    # buffer -> queue
        # queue[Dict[float, TradeSignal]]
        # dict will be
        # {timestamp in ms: TradeSignal}
        # timestamp is to indicate when the signal has been generated.

    # signal reader
        # windows value, default 3000 ms (3 sec)
        # if the signal was made more than 3 seconds, then just ignore.


    """
    # declare a signal buffer -> thread safe one
    # order decider will pop the data
    # one more class just making trading decision bsed on the indicators?
    """