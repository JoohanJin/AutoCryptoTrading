# Standard Library
import time

# Custom Library
from logger.set_logger import logger
from mexc.future import FutureMarket
from object.signal_int import TradeSignal
from pipeline.signal_pipeline import SignalPipeline

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
        signal_pipeline: SignalPipeline,
        mexc_future_market_sdk: FutureMarket,
    ) -> None:
        """
        # func __init__():
            # initialize the TradeManager with the given signal generator and REST API caller for MexC.
        """
        self.signal_pipeline: SignalPipeline = signal_pipeline
        self.mexc_future_market_sdk = mexc_future_market_sdk

        logger.info(f"{__name__} - TradeManager has been intialized and ready to get the signal")

        return None
    

    """
    ######################################################################################################################
    #                                               Private Method                                                       #
    ######################################################################################################################
    """
    def __verify_signal(
        self,
        signal_data: TradeSignal,
        timestamp_window: int = 5000,
    ) -> bool:
        return TradeManager.generate_timestamp() - signal_data.timestamp < 5000
    
    def __execute_trade(self, signal: TradeSignal) -> None:
        """
        
        """
        return None


    def __get_signal(
        self,
        timestamp_window: int = 5000,    
    ) -> TradeSignal:
        """
        # func __get_signal(): private method
            # get the signal from the signal pipeline

        # param self:
            # TradeManager object
        
        # return TradeSignal:
            # it will return the parameter signal and decide the action based on the signal.
        """
        signal_data = self.signal_pipeline.pop_signal()
        return signal_data if self.__verify_signal(signal_data = signal_data, timestamp_window = timestamp_window) else None