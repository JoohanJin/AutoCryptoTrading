# STANDARD LIBRARY
import threading
import pandas
from typing import Optional, Tuple, Literal, Union, List
import asyncio
import time

# CUSTOM LIBRARY
from pipeline.data_pipeline import DataPipeline
from custom_telegram.telegram_bot_class import CustomTelegramBot
from set_logger import logger

class StrategyHandler:
    def __init__(
            self,
            pipeline: DataPipeline,
        ) -> None:
        self.pipeline: DataPipeline = pipeline
        self.threads: List[threading.Thead] = []
        self.__telegram_bot: CustomTelegramBot = CustomTelegramBot()

        self._init_threads()
        self._start_threads()

        return

    """
    ######################################################################################################################
    #                                      Read Data from the Data Pipeline                                              #
    ######################################################################################################################
    """
    def get_test_data(self) -> Optional[Tuple[float]]:
        return self.pipeline.pop_data(
            type = "test",
            block = True,
            timeout = None,
        )

    def get_smas(self) -> Optional[Tuple[float]]:
        return self.pipeline.pop_data(
            type = "sma",
            block = True,
            timeout = None,
        )
    
    def get_emas(self) -> Optional[Tuple[float]]:
        return self.pipeline.pop_data(
            type = "ema",
            block = True,
            timeout = None,
        )

    """
    ######################################################################################################################
    #                               Send the important message to the Telegram Chat Room                                 #
    ######################################################################################################################
    """
    async def send_telegram_message(self, message: str)-> None:
        # asyncio.run(self.send_telegram_message(message))
        try:
            await self.__telegram_bot.send_text(message)
        except Exception as e:
            logger.debug(f"Error sending Telegram message: {e}")

    def generate_telegram_msg(self, data) -> str:
        return ""
    
    """
    ######################################################################################################################
    #                                               Threading Management                                                 #
    ######################################################################################################################
    """
    def _init_threads(self):
        thread1: threading.Thread = threading.Thread(
            name = "sma data getter",
            target = self.threads_sma,
            daemon = True,
        )
        logger.info(f"{__name__}: Thread for sma data getter has been set up!")

        thread2: threading.Thread = threading.Thread(
            name = "ema data getter",
            target = self.threads_ema,
            daemon = True,
        )
        logger.info(f"{__name__}: Thread for sma data getter has been set up!")

        thread3: threading.Thread = threading.Thread(
            name = "test data getter",
            target = self.threads_test,
            daemon = True,
        )
        logger.info(f"{__name__}: Thread for sma data getter has been set up!")

        self.threads.extend([thread1, thread2])
        return
    
    def _start_threads(self):
        """
        # function name: _start_threads()
            # start the threads in the thread pool of the class.
            # will raise issues if there is  problem with the triggering of the thread.
        
        # param self
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
    #                                                   Functionality                                                    #
    ######################################################################################################################
    """
    def threads_sma(self) -> Tuple[float]:
        while True:
            data = self.get_smas()
            if (data):
                pass
                # do something with data
            time.sleep(1.5)
        return
    
    def threads_ema(self) -> Tuple[float]:
        while True:
            data = self.get_emas()
            if (data):
                pass
                # do something with data
            time.sleep(1.5)
        return
    
    def threads_test(self) -> Tuple[float]  :
        while True:
            data = self.get_test_data()
            if (data):
                pass
                # do something with data
            time.sleep(1.5)
        return