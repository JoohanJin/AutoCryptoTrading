# Standard Library
import time

# Custom Library
from logger.set_logger import logger
from manager.signal_generator import SignalGenerator
from mexc.future import FutureMarket

class TradeManager:
    """
    ######################################################################################################################
    #                                               Static Method                                                        #
    ######################################################################################################################
    """
    @staticmethod
    def generate_timestamp() -> int:
        """
        # func generate_timestamp(): staticmethod
            # return the timestamp based on the current time in ms
        """
        return int(time.time() * 1000)

    """
    ######################################################################################################################
    #                                                Class Method                                                        #
    ######################################################################################################################
    """
    def __init__(
        self,
        signal_generator: SignalGenerator,
        mexc_future_market_sdk: FutureMarket,
    ) -> None:
        """
        # func __init__():
            # initialize the TradeManager with the given signal generator and REST API caller for MexC.
        """
        self.signal_generator = signal_generator
        self.mexc_future_market_sdk = mexc_future_market_sdk

        logger.info(f"{__name__} - TradeManager has been intialized and ready to get the signal")

        return None
    

    """
    
    """