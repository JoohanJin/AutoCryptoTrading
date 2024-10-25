# STANDARD LIBRARY
import threading
import pandas
from typing import Optional, Tuple, Literal, Union

# CUSTOM LIBRARY
from src.pipeline.data_pipeline import DataPipeline
from src.custom_telegram import CustomTelegramBot
from src.set_logger import logger

class StrategyHandler:
    def __init__(
            self,
            pipeline: DataPipeline,
        ) -> None:
        self.pipeline: DataPipeline = pipeline
        self.__telegram_bot: CustomTelegramBot = CustomTelegramBot()
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