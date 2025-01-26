# Standard Library
import time

# Custom Library
from logger.set_logger import logger

class TradeManager:
    # need to have the REST API caller for the FutureMarket
    def __init__(
        self,
        # indicator_pipeline
        # FutureMarket: REST API caller
        ) -> None:
        """
        
        """
        return
    
    @staticmethod
    def generate_timestamp() -> int:
        """
        # func generate_timestamp(): staticmethod
            # return the timestamp based on the current time in ms
        """
        return int(time.time() * 1000)