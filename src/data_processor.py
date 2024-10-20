import threading
import pandas

# CUSTOM LIBRARY
from src.pipeline.data_pipeline import DataPipeline
from src.custom_telegram import CustomTelegramBot
from src.set_logger import logger

class StrategyHandler:
    def __init__(
            self,
            pipeline: DataPipeline,
        ):
        self.pipeline: DataPipeline = pipeline
        self.__telegram_bot: CustomTelegramBot = CustomTelegramBot()
        return
    
    """
    ######################################################################################################################
    #                               Send the important message to the Telegram Chat Room                                 #
    ######################################################################################################################
    """
    async def send_telegram_message(self, message: str)-> None:
        # how to use this from the other functions?
        # asyncio.run(self.send_telegram_message(message))
        try:
            await self.__telegram_bot.send_text(message)
        except Exception as e:
            logger.debug(f"Error sending Telegram message: {e}")