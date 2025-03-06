# Standard Library
import threading
import time
from typing import List

# Custom Library
from logger.set_logger import logger
from mexc.future import FutureMarket
from object.score_mapping import ScoreMapper
from object.signal import Signal, TradeSignal
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
        func generate_timestamp(): staticmethod
            - return the timestamp based on the current time in ms
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
        delta_mapper: ScoreMapper,
    ) -> None:
        """
        func __init__():
            - initialize the TradeManager with the given signal generator and REST API caller for MexC.
            - initialize the necessary member variables and start the TradeManager.
        """
        # Set the signal piepline as a member variable
        self.signal_pipeline: SignalPipeline = signal_pipeline

        # Set the MexC Future Market SDK as a member variable
        # to send the REST API to the MexC API Gateway.
        self.mexc_future_market_sdk = mexc_future_market_sdk

        self.delta_mapper: ScoreMapper = delta_mapper

        # Set the thread pool as a member function.
        self.threads: List[threading.Threads] = list()

        # Set the trade score as a member variable.
        self.trade_score_lock: threading.Lock = threading.Lock()
        self.trade_score: int = 0

        # Start the TradeManager
        self.start()       

        logger.info(f"{__name__} - TradeManager has been intialized and ready to get the signal")
        return None

    def __del__(
        self: object,
    ) -> None:
        """
        func __del__():
            - delete the TradeManager object
            - need to remove all the threads and possibly dynamic objects as well.
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
        func start():
            - start the TradeManager
            - It will initialize the threads and start the threads.
            - make it as a public so that in the future, it will be started at the outside of the class.
        
        param self:
            - TradeManager object
        
        return None:
            - it is a void function.
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
        func __initialize_threads():
            - private method
            - It will set up the thread pool for the TradeManager.

        param self:
            - TradeManager object
        """
        # Generate the threads for the function, need to plan it.
        thread_get_signal: threading.Thread = threading.Thread(target = self.__thread_get_signal, name = "Thread-Get-Signal")
        thread_decide_trade: threading.Thread = threading.Thread(target = self.__thread_decide_trade, name = "Thread-Decide-Trade")

        # initialize the threads for the operations
        self.threads.extend([thread_get_signal, thread_decide_trade])
        return None
    
    def __start_threads(
        self,
    ) -> None:
        """
        func __start_threads():
            - private method
            - It will start the thread pool for the TradeManager.

        param self:
            - TradeManager object
        
        return None:
            - it is a void function.
        """
        for thread in self.threads:
            try:
                thread.start()
                logger.info(f"{__name__} - Thread {thread.name} has been started")
            except RuntimeError as e:
                logger.critical(f"{__name__}: Failed to start thread '{thread.name}': {str(e)}")
                print(f"{__name__}: Failed to start thread '{thread.name}': {str(e)}")
                raise RuntimeError(f"{__name__}: Failed to start thread '{thread.name}': {str(e)}")
            except Exception as e:
                logger.error(f"{__name__} - Unknown Error while starting the threads: {e}")
                print(f"{__name__} - Unknown Error while starting the threads: {e}")
                raise Exception(f"{__name__}: Failed to start thread '{thread.name}': {str(e)}")
        
        return None

    """
    ######################################################################################################################
    #                                             Signal Management Method                                               #
    ######################################################################################################################
    """
    def __thread_get_signal(
        self,
        timestamp_window: int = 5000,
    ) -> None:
        """
        func __thread_get_signal():
            - A private method
            - It gets the signal from the signal pipeline
            - This function should be run by other thread which is monitoring the system.

        param self:
            - TradeManager object
        param timestamp_window: int
            - limit for the signal generation timestamp for the signal.
            - If the difference between the current timestamp and signal timestamp is greater than the timestamp_window, then it will be ignored.
        """
        while True:
            try:
                signal: TradeSignal = self.__get_signal(timestamp_window = timestamp_window)
                if signal:
                    with self.trade_score_lock:
                        self.trade_score += self.__calculate_signal_score_delta(signal_data = signal)
            except Exception as e:
                logger.error(f"{__name__} - Error while getting the signal: {e}")
                print(f"{__name__} - Error while getting the signal: {e}")
        return None

    def __calculate_signal_score_delta(
        self,
        signal_data: TradeSignal,
    ) -> int:
        """
        func __calculate_delta():
            - private method
            - calculate the delta based on the signal data.
            - It will return the delta value based on the signal data.

        param self:
            - TradeManager object
        param signal_data: TradeSignal
            - signal data which is passed from the signal pipeline.

        return int:
            - delta value based on the signal data.
        """
        return self.delta_mapper.map(TradeSignal = signal_data)

    def __verify_signal(
        self,
        signal_data: TradeSignal,
        timestamp_window: int = 5_000,
    ) -> bool:
        """
        func __verify_signal():
            - private method
            - verify the signal based on the timestamp.

        param self: TradeManager object
        param signal_data: TradeSignal object
            - signal data which is passed from the signal pipeline.
        param timestamp_window: int
            - limit for the signal generation timestamp.
            - If the difference between the current timestamp and signal timestamp is greater than the timestamp_window, then it will be ignored.
            - the default value is 5000 ms == 5 seconds.
        
        return bool:
            - True if the signal is valid, otherwise False
        """
        return TradeManager.generate_timestamp() - signal_data.timestamp < timestamp_window
    
    def __get_signal(
        self,
        timestamp_window: int = 5000,    
    ) -> TradeSignal | None:
        """
        func __get_signal(): private method
            - get the signal from the signal pipeline
            - This function should be run by other thread which is monitoring the system.

        param self:
            - TradeManager object
        
        return TradeSignal:
            - it will return the parameter signal and decide the action based on the signal.
        return None
            - if the signal is not valid, then it will return None.
        """
        signal_data: Signal = self.signal_pipeline.pop_signal()
        return signal_data.signal if self.__verify_signal(signal_data = signal_data, timestamp_window = timestamp_window) else None
    
    def __decide_trade(
        self,
        score: int,
    ) -> int:
        """
        func __decide_trade():
            - private method
            - decide the trade based on the score.
            - It will return the decision based on the score.

        param self:
            - TradeManager object
        param score: int
            - score based on the signal data.

        return int:
            - 1: buy
            - -1: sell
            - 0: hold
        """
        if score > 100:
            return 1
        elif score < -100:
            return -1
        return 0 # default is do nothing

    def __thread_decide_trade(
        self,
    ) -> None:
        """
        func __thread_decide_trade():
            - private method
            - decide the trade based on the signal.
            - This function should be run by the other function which is monitoring some schema.

        param self:
            - TradeManager object
        
        return None:
            - it is a void function
        """
        while True:
            try:
                with self.trade_score_lock:
                    score: int = self.trade_score
                
                decision: int = self.__decide_trade(
                    score = score,
                )

                self.__execute_trade(
                    buy_or_sell = decision,
                )

                if decision != 0: # can be further improved in the future.
                    with self.trade_score_lock:
                        self.trade_score = 0

                time.sleep(0.5)
            
            except Exception as e:
                logger.error(f"{__name__} - Error while deciding the trade: {e}")
                print(f"{__name__} - Error while deciding the trade: {e}")
        return None

    def __execute_trade(
        self,
        buy_or_sell: int,
    ) -> None:
        """
        func __execute_trade():
            - private method
            - execute the trade based on the signal.
            - This function should be run by the other function which is monitoring some schema.

        param self:
            - TradeManager object
        """
        if buy_or_sell == 1:
            # execute the buy order
            print("Buy Order")
            pass
        elif buy_or_sell == -1:
            # execute the sell order
            print("Sell Order")
            pass
        else:
            # do nothing - hold
            print("Hold")
            pass
        return None