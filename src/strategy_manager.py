# STANDARD LIBRARY
import threading
import pandas
from typing import Optional, Tuple, Literal, Union
import asyncio

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
        self.threads = []
        self.__telegram_bot: CustomTelegramBot = CustomTelegramBot()

        self._init_threads()
        self._start_threads()

        # Test
        while True:
            sma_values = self.get_smas()
            if (sma_values):
                asyncio.run(self.send_telegram_message(
                    f"SMAs:\nsma_5: {sma_values[0]}\nsma_10: {sma_values[1]}\nsma_15: {sma_values[2]}\nsma_20: {sma_values[3]}"
                ))
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
        )

    def get_smas(self) -> Optional[Tuple[float]]:
        return self.pipeline.pop_data(
            type = "sma",
            block = True,
        )
    
    def get_emas(self) -> Optional[Tuple[float]]:
        return self.pipeline.pop_data(
            type = "ema",
            block = True,
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
        

        self.threads.extend([])
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