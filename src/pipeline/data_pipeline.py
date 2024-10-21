# Standard Library
from queue import Queue

# CUSTOM LIBRARY
from src.set_logger import logger
from src.custom_telegram.telegram_bot_class import CustomTelegramBot
from src.pipeline.data_pipeline import DataPipeline


class DataPipeline:
    def __init__(self):
        self.q = list()
        return