# STANDARD LIBRARY
import threading
from typing import Optional, Tuple, Literal, Union, List
import time
from enum import IntFlag
from queue import Queue

# CUSTOM LIBRARY
from pipeline.data_pipeline import DataPipeline
from custom_telegram.telegram_bot_class import CustomTelegramBot
from logger.set_logger import logger


class TradeSignal(IntFlag):
    BUY = 1 # 001
    SELL = 2 # 010
    HOLD = 4 # 100


class StrategyHandler:
    def __init__(
            self,
            pipeline: DataPipeline,
        ) -> None:
        """
        # func __init__:
            # Initialize the Strategy Handler.
            # It gets the pipeline as a parameter for the indicator fetching.
            # It initializes the telegram bot for the notification.
            # It initializes the threads for the indicator fetching.

        # param self: StrategyHandler
        # param pipeline: DataPipeline
        
        # return None
        """
        # data pipeline to get the ema, sma data, for now.
        self.pipeline: DataPipeline = pipeline
        
        # threads pool
        self.threads: List[threading.Thead] = []
        
        # telegram bot manager to send the notification.
        self.__telegram_bot: CustomTelegramBot = CustomTelegramBot()

        # Data buffer for all of the data.
        self.__data_buffer: Queue = Queue(maxsize=100)

        # initialize the threads
        self._init_threads()
        # start each thread, which is in the threads pool.
        self._start_threads()

        return

    """
    ######################################################################################################################
    #                                      Read Data from the Data Pipeline                                              #
    ######################################################################################################################
    """
    def get_test_data(self) -> Optional[Tuple[float]]:
        """
        # func get_test_data:
            # Get the test data from the data pipeline.
            # It will be used for the testing phase.
            # It will be used by the threads to get the data from the pipeline.

        # param self: StrategyHandler
        
        # return None
        """
        return self.pipeline.pop_data(
            type = "test",
            block = True, # if there is no data, then stop the process until the data is available.
            timeout = None,
        )

    def get_smas(self) -> Optional[Tuple[float]]:
        """
        # func get_smas:
            # Get the sma data from the data pipeline.
            # It will be used by the threads to get the data from the pipeline.

        # param self: StrategyHandler

        # return None
        """
        return self.pipeline.pop_data(
            type = "sma",
            block = True, # if there is no data, then stop the process until the data is available.
            timeout = None,
        )
    
    def get_emas(self) -> Optional[Tuple[float]]:
        """
        # func get_emas:
            # Get the ema data from the data pipeline.
            # It will be used by the threads to get the data from the pipeline.

        # param self: StrategyHandler

        # return None
        """
        return self.pipeline.pop_data(
            type = "ema",
            block = True, # if there is no data, then stop the process until the data is available.
            timeout = None,
        )

    """
    ######################################################################################################################
    #                               Send the important message to the Telegram Chat Room                                 #
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
    #                                               Threading Management                                                 #
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
        thread1: threading.Thread = threading.Thread(
            name = "sma_data_getter",
            target = self.threads_sma,
            daemon = True,
        )
        logger.info(f"{__name__}: Thread for sma_data_getter has been set up!")

        thread2: threading.Thread = threading.Thread(
            name = "ema_data_getter",
            target = self.threads_ema,
            daemon = True,
        )
        logger.info(f"{__name__}: Thread for ema_data_getter has been set up!")

        # but no need touse it right now.
        thread3: threading.Thread = threading.Thread(
            name = "test_data_getter",
            target = self.threads_test,
            daemon = True,
        )
        logger.info(f"{__name__}: Thread for test_data_getter has been set up!")

        self.threads.extend(
            [
                thread1, 
                thread2,
                # thread3,
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
                thread.start()
                logger.info(f"{__name__}: Thread '{thread.name}' (ID: {thread.ident}) has started")
            except RuntimeError as e:
                logger.critical(f"{__name__}: Failed to start thread '{thread.name}': {str(e)}")
                raise
            except Exception as e:
                logger.critical(f"{__name__}: Unexpected error starting thread: '{thread.name}': {str(e)}")
                raise
        return
    
    """
    ######################################################################################################################
    #                                                      Threads                                                       #
    ######################################################################################################################
    """
    def threads_sma(self) -> bool:
        """
        # func threads_sma():
            # get the sma data from the pipeline.
            # target function of the thread.
        
        # param self: StrategyHandler
            # class object

        # return True if the update is successful.
        # return False if the update is not successful.
        """
        while True:
            data = self.get_smas()
            if (data):
                sma = data
                # do something with data
            time.sleep(1)
        return
    
    def threads_ema(self) -> bool:
        """
        # func threads_ema():
            # get the ema data from the pipeline.
            # target function of the thread.
        
        # param self: StrategyHandler
            # class object
        
        # return True if the update is successful.
        # return False if the update is not successful.
        """
        while True:
            data = self.get_emas()
            if (data):
                ema = data
                # do something with data
            time.sleep(1)
        return
    
    def threads_test(self) -> bool:
        """
        # func threads_test():

        # param self: StrategyHandler
            # class object

        # return True if the update is successful.
        # return False if the update is unsuccessful.
        """
        while True:
            data = self.get_test_data()
            if (data):
                test_data = data
                # do something with data
            time.sleep(1)
        return