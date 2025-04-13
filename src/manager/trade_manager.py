# Standard Library
import threading
import asyncio
import time
from typing import List, Dict, Tuple

# Custom Library
from custom_telegram.telegram_bot_class import CustomTelegramBot
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

    @staticmethod
    def verify_signal(
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
        telegram_bot: CustomTelegramBot,
        leverage: int = 20,
        trade_amount: float = 0.1, # 10% of the total asset
        take_profit_rate: float = 0.15, # 15%
        stop_loss_rate: float = 0.05, # 5%
        score_threashold: int = 2_000,
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

        self.telegram_bot: CustomTelegramBot = telegram_bot

        self.score_threshold: int = score_threashold

        # Set the thread pool as a member function.
        self.threads: List[threading.Threads] = list()

        # Set the trade score as a member variable.
        self.trade_score_lock: threading.Lock = threading.Lock()
        self.trade_score: int = 0

        self.leverage: int = leverage
        self.trade_amount: float = trade_amount
        self.tp_rate: float = take_profit_rate
        self.sl_rate: float = stop_loss_rate

        self.async_loop = asyncio.new_event_loop() # only for Telegram Client

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
        thread_get_signal: threading.Thread = threading.Thread(
            target = self.__thread_get_signal,
            name = "Thread-Get-Signal",
        )
        thread_decide_trade: threading.Thread = threading.Thread(
            target = self.thread_handle_async_trade_execution,
            name = "Thread-Decide-Trade",
            args = (self.async_loop, ),
        )

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
                raise RuntimeError(f"{__name__}: Failed to start thread '{thread.name}': {str(e)}")
            except Exception as e:
                logger.error(f"{__name__} - Unknown Error while starting the threads: {e}")
                raise Exception(f"{__name__}: Failed to start thread '{thread.name}': {str(e)}")
        
        return None

    """
    ######################################################################################################################
    #                                             Signal Management Method                                               #
    ######################################################################################################################
    """
    def thread_handle_async_trade_execution(self, loop) -> None:
        """
        """
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.__thread_decide_trade())
        return

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
                signal: TradeSignal = self.__get_signal(
                    timestamp_window = timestamp_window,
                )
                if signal:
                    with self.trade_score_lock:
                        self.trade_score += self.__calculate_signal_score_delta(
                            signal_data = signal,
                        )
            except Exception as e:
                logger.error(f"{__name__} - Error while getting the signal: {e}")
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
        return self.delta_mapper.map(signal = signal_data)
    
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
        return signal_data.signal if TradeManager.verify_signal(signal_data = signal_data, timestamp_window = timestamp_window) else None
    
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
        if score > self.score_threshold:
            return 1
        elif score < (-1 * self.score_threshold):
            return -1
        return 0 # default is do nothing

    async def __thread_decide_trade(
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
        """
        while True:
            try:
                with self.trade_score_lock:
                    score: int = self.trade_score
                
                decision: int = self.__decide_trade(
                    score = score,
                )

                await self.__execute_trade(
                    buy_or_sell = decision,
                )

                if decision != 0: # can be further improved in the future.
                    # reset the score, but based on the trend
                    # 
                    with self.trade_score_lock:
                        self.trade_score = 200 if decision == 1 else -200

                time.sleep(0.25)
            
            except Exception as e:
                logger.error(f"{__name__} - Error while deciding the trade: {e}")

        return None

    def __get_current_price(
        self,
    ) -> float:
        """
        func __get_current_price():
            - private method
            - get the current price from the MexC API Endpoint.
        
        param self:
            - TradeManager object
        
        return float:
            - current price of the asset
        """
        price_response: Dict = self.mexc_future_market_sdk.index_price()
        if (price_response.get('success')):
            return price_response.get('data').get('indexPrice')
        else:
            raise Exception(f"{__name__} - Error while getting the current price: {price_response}")
        return
    
    def __get_target_prices(
        self,
        buy_or_sell: int,
        current_price: float,
    ) -> Tuple[float] | None:
        """
        func __get_target_prices():
            - private method
            - get the target prices based on the current price and the signal.
            - It will return the target prices based on the signal.
        
        param self:
            - TradeManager object
        param buy_or_sell: int
            - 1: buy
            - -1: sell
            - 0: hold, nothing to do with the function.
        param current_price: float
            - current price of the BTC_USDT, i.e., Index Price is used.

        return Tuple[float]:
            - take profit price, stop loss price
        return None:
            - if the signal is not valid, then it will return None.
        """
        if (buy_or_sell == 1): # Long
            return current_price * (1 + (self.tp_rate / self.leverage)), current_price * (1 - (self.sl_rate / self.leverage))
        else: # Short
            return current_price * (1 - (self.tp_rate / self.leverage)), current_price * (1 + (self.sl_rate / self.leverage))

    def __get_trade_amount(
        self,
    ) -> float:
        open_amount_response: dict = self.mexc_future_market_sdk.asset(
            currency = "USDT",
        )

        if (open_amount_response.get('success')):
            return open_amount_response.get('data').get('availableOpen') * self.trade_amount
        else:
            raise Exception(f"{__name__} - Error while getting the trade amount: {open_amount_response}")
        return

    async def __execute_trade(
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
        try:
            if (buy_or_sell == 1 or buy_or_sell == -1):
                current_price: float = self.__get_current_price()
                tp_price, sl_price = self.__get_target_prices(
                    buy_or_sell = buy_or_sell,
                    current_price = current_price,
                )
                trade_amount: float = self.__get_trade_amount()
                order_type: int = 0

                if buy_or_sell == 1:
                    order_type = 1 # Long
                elif buy_or_sell == -1:
                    order_Type = 3 # Short

                # TODO: trigger the order
                await self.telegram_bot.send_text(
                    f"Trade Signal: {'Buy' if order_type == 1 else 'Sell'}\nEntry Price: {current_price}\nAmount: {trade_amount}\nTake Profit: {tp_price}\nStop Loss: {sl_price}"
                )
                logger.INFO(f"Trade Signal: {'Buy' if order_type == 1 else 'Sell'}\nEntry Price: {current_price}\nAmount: {trade_amount}\nTake Profit: {tp_price}\nStop Loss: {sl_price}")
    
        except Exception as e:
            logger.error(f"{__name__} - Error while executing the trade: {e}")
        return None