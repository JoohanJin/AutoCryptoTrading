# Standard Library
import threading
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
            # initialize the necessary member variables and start the TradeManager.
        """
        # Set the signal piepline as a member variable
        self.signal_pipeline: SignalPipeline = signal_pipeline

        # Set the MexC Future Market SDK as a member variable
        # to send the REST API to the MexC API Gateway.
        self.mexc_future_market_sdk = mexc_future_market_sdk

        # Set the thread pool as a member function.
        self.threads: threading.Threads = list()

        # Start the TradeManager
        self.start()       

        logger.info(f"{__name__} - TradeManager has been intialized and ready to get the signal")
        return None

    def __del__(
        self: object,
    ) -> None:
        """
        # func __del__():
            # delete the TradeManager object
            # need to remove all the threads and possibly dynamic objects as well.
        """
        logger.info(f"{__name__} - TradeManager has been deleted")

        return None
    
    """
    ######################################################################################################################
    #                                             Multi-Thread Management                                                #
    ######################################################################################################################
    """
    def start(
        self,
    ) -> None:
        """
        # func start():
            # start the TradeManager
            # It will initialize the threads and start the threads.
            # make it as a public so that in the future, it will be started at the outside of the class.
        """
        # Initialize the threads
        self.__initialize_threads()

        # Start the threads
        self.__start_threads()

        return None

    def __initialize_threads(
        self,
    ) -> None:
        """
        # func __initialize_threads():
            # private method
            # It will set up the thread pool for the TradeManager.

        # param self:
            # TradeManager object
        """
        tmp_threads: list[threading.Thread] = list()

        # initialize the threads for the operations
        self.threads.extend(tmp_threads)

        return None
    
    def __start_threads(
        self,
    ) -> None:
        """
        # func __start_threads():
            # private method
            # It will start the thread pool for the TradeManager.

        # param self:
            # TradeManager object
        
        # return None:
            # it is a void function.
        """
        for thread in self.threads:
            try:
                thread.start()
                logger.info(f"{__name__} - Thread {thread.name} has been started")
            except RuntimeError as e:
                logger.critical(f"{__name__}: Failed to start thread '{thread.name}': {str(e)}")
                raise RuntimeError
            except Exception as e:
                logger.error(f"{__name__} - Unknown Error while starting the threads: {e}")
                raise Exception
        
        return None

    """
    ######################################################################################################################
    #                                             Signal Management Method                                               #
    ######################################################################################################################
    """
    def __verify_signal(
        self,
        signal_data: TradeSignal,
        timestamp_window: int = 5000,
    ) -> bool:
        """
        # func __verify_signal():
            # private method
            # verify the signal based on the timestamp.

        # param self: TradeManager object
        # param signal_data: TradeSignal object
            # signal data which is passed from the signal pipeline.
        # param timestamp_window: int
            # limit for the signal generation timestamp.
            # If the difference between the current timestamp and signal timestamp is greater than the timestamp_window, then it will be ignored.
            # the default value is 5000 ms == 5 seconds.
        
        # return bool:
            # True if the signal is valid, otherwise False
        """
        return TradeManager.generate_timestamp() - signal_data.timestamp < timestamp_window
    
    def __execute_trade(
        self,
    ) -> None:
        """
        # func __execute_trade():
            # private method
            # execute the trade based on the signal.
            # This function should be run by the other function which is monitoring some schema.

        # param self:
            # TradeManager object
        """
        return None

    def __get_signal(
        self,
        timestamp_window: int = 5000,    
    ) -> TradeSignal | None:
        """
        # func __get_signal(): private method
            # get the signal from the signal pipeline
            # This function should be run by other thread which is monitoring the system.

        # param self:
            # TradeManager object
        
        # return TradeSignal:
            # it will return the parameter signal and decide the action based on the signal.
        # return None
            # if hte signal is not valid, then it will return None.
        """
        signal_data = self.signal_pipeline.pop_signal()
        return signal_data if self.__verify_signal(signal_data = signal_data, timestamp_window = timestamp_window) else None