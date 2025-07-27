# STANDARD LIBRARY
import threading
from typing import Dict, Optional, List
import time

# CUSTOM LIBRARY
from custom_telegram.telegram_bot_class import CustomTelegramBot
from pipeline.data_pipeline import DataPipeline
from pipeline.signal_pipeline import SignalPipeline
from logger.set_logger import operation_logger, trading_logger
from object.signal import TradeSignal, Signal


class SignalGenerator:
    """
    ######################################################################################################################
    #                                               Static Method                                                        #
    ######################################################################################################################
    """

    @staticmethod
    def generate_timestamp() -> int:
        """
        static func generate_timestamp():
            - Generate the timestamp using the current time, in the form of epoch in ms.

        param None

        return int
            - the timestam in the form of epoch in ms.
        """
        return int(time.time() * 1000)

    """
    ######################################################################################################################
    #                                               Function Method                                                      #
    ######################################################################################################################
    """

    def __init__(
        self,
        data_pipeline: DataPipeline,
        custom_telegram_bot: CustomTelegramBot,
        signal_pipeline: SignalPipeline,
        signal_window: int = 5_000,
    ) -> None:
        """
        func __init__():
            - Initialize the Strategy Handler.
            - It gets the pipeline as a parameter for the indicator fetching.
            - It initializes the telegram bot for the notification.
            - It initializes the threads for the indicator fetching.

        param self: StrategyHandler
            - class object
        param pipeline: DataPipeline
            - Data pipeline for the indicator fetching.

        return None
        """
        # data pipeline to get the indicators
        self.data_pipeline: DataPipeline = data_pipeline
        self.signal_pipeline: SignalPipeline = (
            signal_pipeline  # TODO: need to uncomment this for initialization.
        )

        # telegram bot manager to send the notification.
        self.__telegram_bot: CustomTelegramBot = custom_telegram_bot

        # Shared Structure
        # Mutex Lock
        self.indicators_lock: threading.Lock = threading.Lock()
        self.indicators: dict[str, dict[int, float]] | dict[str, None] = {
            "sma": None,  # Latest SMA data
            "ema": None,  # latest EMA data
            "price": None,  # latest Price data
        }

        # threads pool
        self.threads: List[threading.Thead] = list()

        # shared data structure to store Timestamp of the previoius invokation of each signal.
        self.signal_timestamps: dict[str, int] = dict()
        self.signal_timestamps_lock: threading.Lock = threading.Lock()
        self.signal_window: int = signal_window

        # TODO: separate this part as strat()
        # initialize the threads
        self._init_threads()
        # start each thread, which is in the threads pool.
        self._start_threads()

        return None

    """
    ######################################################################################################################
    #                                      Read Data from the Data Pipeline                                              #
    ######################################################################################################################
    """

    def get_test_data(self) -> Optional[Dict[int, float]]:
        """
        func get_test_data:
            - Get the test data from the data pipeline.
            - It will be used for the testing phase.
            - It will be used by the threads to get the data from the pipeline.

        param self: StrategyHandler

        return None
        """
        return self.data_pipeline.pop_data(
            type="test",
            block=True,  # if there is no data, then stop the process until the data is available.
            timeout=None,
        )

    def get_smas(self) -> Optional[Dict[int, float]]:
        """
        func get_smas:
            - Get the sma data from the data pipeline.
            - It will be used by the threads to get the data from the pipeline.

        param self: StrategyHandler

        return None
        """
        return self.data_pipeline.pop_data(
            type="sma",
            block=True,  # if there is no data, then stop the process until the data is available.
            timeout=None,
        )

    def get_emas(self) -> Optional[Dict[int, float]]:
        """
        func get_emas:
            - Get the ema data from the data pipeline.
            - It will be used by the threads to get the data from the pipeline.

        - param self: StrategyHandler

        - return None
        """
        return self.data_pipeline.pop_data(
            type="ema",
            block=True,  # if there is no data, then stop the process until the data is available.
            timeout=None,
        )

    def get_price_data(self) -> Optional[Dict[int, float]]:
        """
        - func get_price_data:
            - Get the test data from the data pipeline.
            - It will be used for the testing phase.
            - It will be used by the threads to get the data from the pipeline.

        - param self: StrategyHandler

        - return None
        """
        return self.data_pipeline.pop_data(
            type="price",
            block=True,  # if there is no data, then stop the process until the data is available.
            timeout=None,
        )

    """
    ######################################################################################################################
    #                         Send the important message to the Telegram Chat Room as a Logging                          #
    ######################################################################################################################
    """

    async def send_telegram_message(
        self,
        message: str = "",
    ) -> None:
        """
        - func send_telegram_message:
            - Send the message to the telegram chat room.
            - It will be used to send the notification to the telegram chat room.

        - param self: StrategyHandler
        - param message: str

        - param None
        """
        try:
            await self.__telegram_bot.send_text(
                message=message,
            )
        except Exception as e:
            operation_logger.error(f"Error sending Telegram message: {e}")

    # TODO: This is not used currently.
    def generate_telegram_msg(self, data) -> str:
        """
        - func generate_telegram_msg:
            - Generate the message for the telegram chat room.
            - It will be used to generate the message for the telegram chat room.

        - param self: StrategyHandler
        - param data: Tuple[float]

        - return str
        """
        return ""

    """
    ######################################################################################################################
    #                                                 Threads Management                                                 #
    ######################################################################################################################
    """

    def _init_threads(self):
        """
        - func _init_threads:
            - Initialize the threads for the indicator fetching.
            - It will be used to initialize the threads for the indicator fetching.
            - It will be used to consume the data and generate the signals based on the data and pass it to the signal pipeline.

        - param self: StrategyHandler

        - return None
        """

        # Update the data
        sma_thread: threading.Thread = threading.Thread(
            name="sma_data_getter",
            target=self.get_sma,
            daemon=True,
        )
        operation_logger.info(
            f"{__name__}: Thread for sma_data_getter has been set up!"
        )

        ema_thread: threading.Thread = threading.Thread(
            name="ema_data_getter",
            target=self.get_ema,
            daemon=True,
        )
        operation_logger.info(
            f"{__name__}: Thread for ema_data_getter has been set up!"
        )

        price_thread: threading.Thread = threading.Thread(
            name="price_data_getter",
            target=self.get_price,
            daemon=True,
        )
        operation_logger.info(
            f"{__name__}: Thread for price_data_getter has been set up!"
        )

        # add data-update threads into the Threads pool.
        self.threads.extend(
            [
                sma_thread,
                ema_thread,
                price_thread,
            ]
        )

        # Consume the data.
        golden_cross_thread: threading.Thread = threading.Thread(
            name="golden_cross_signal_generator",
            target=self.generate_golden_cross_signal,
            daemon=True,
        )
        operation_logger.info(
            f"{__name__}: Thread for golden_cross_signal_generator has been set up!"
        )

        death_cross_thread: threading.Thread = threading.Thread(
            name="death_cross_signal_generator",
            target=self.generate_death_cross_signal,
            daemon=True,
        )
        operation_logger.info(
            f"{__name__}: Thread for death_cross_signal_generator has been set up!"
        )

        price_ma_thread: threading.Thread = threading.Thread(
            name="price_ma_signal_generator",
            target=self.generate_price_moving_average_signal,
            daemon=True,
        )
        operation_logger.info(
            f"{__name__}: Thread for price_ma_signal_generator has been set up!"
        )

        ema_sma_divergence_thread: threading.Thread = threading.Thread(
            name="ema_sma_divergence_signal_generator",
            target=self.generate_ema_sma_divergence_signal,
            daemon=True,
        )
        operation_logger.info(
            f"{__name__}: Thread for ema_sma_divergence_signal_generator has been set up!"
        )

        price_reversal_thread: threading.Thread = threading.Thread(
            name="price_reversal_signal_generator",
            target=self.generate_price_reversal_signal,
            daemon=True,
        )
        operation_logger.info(
            f"{__name__}: Thread for price_reversal_signal_generator has been set up!"
        )

        # add data consumptions threads into the Threads pool.
        self.threads.extend(
            [
                golden_cross_thread,
                death_cross_thread,
                price_ma_thread,
                ema_sma_divergence_thread,
                price_reversal_thread,
            ]
        )

        return None

    def _start_threads(self) -> None:
        """
        - func _start_threads():
            - start the threads in the thread pool of the class.
            - will raise issues if there is  problem with the triggering of the thread.

        - param self: StrategyHandler
            - class object

        - return None
        """
        for thread in self.threads:
            try:
                # start the thread.
                thread.start()
                operation_logger.info(
                    f"{__name__} - Thread '{thread.name}' (ID: {thread.ident}) has started"
                )
            except RuntimeError as e:
                operation_logger.critical(
                    f"{__name__} - Failed to start thread '{thread.name}': {str(e)}"
                )
                raise RuntimeError(f"Failed to start thread '{thread.name}': {str(e)}")
            except Exception as e:
                operation_logger.critical(
                    f"{__name__} - Unexpected error starting thread: '{thread.name}': {str(e)}"
                )
                raise Exception(
                    f"Unexpected error starting thread: '{thread.name}': {str(e)}"
                )
        return

    """
    ######################################################################################################################
    #                                            Functions for Threads                                                   #
    ######################################################################################################################
    """

    def get_sma(self) -> bool:
        """
        - func get_sma():
            - get the sma data from the pipeline and put it into the shared structured.
            - target function of the thread.

        - param self: StrategyHandler
            - class object

        - return True if the update is successful.
        - return False if the update is not successful.
        """
        while True:
            data = self.get_smas()
            if data:
                # update to the shared structure to use them for analysis.
                with self.indicators_lock:
                    self.indicators["sma"] = data
        return

    def get_ema(self) -> bool:
        """
        - func get_ema():
            - get the ema data from the pipeline and put it into the shared structured.
            - target function of the thread.

        - param self: StrategyHandler
            - class object

        - return True if the update is successful.
        - return False if the update is not successful.
        """
        while True:
            data = self.get_emas()
            if data:
                # update to the shared structure to use them for analysis.
                with self.indicators_lock:
                    self.indicators["ema"] = data
        return

    def get_price(self) -> bool:
        """
        - func get_price():
            - get the price data from the pipeline and put it into the shared structured.
            - target function of the thread.

        - param self: StrategyHandler
            - class object

        - return True if the update is successful.
        - return False if the update is not successful.
        """
        while True:
            data = self.get_price_data()
            if data:
                # update to the shared structure to use them for analysis.
                with self.indicators_lock:
                    self.indicators["price"] = data
        return

    """
    ######################################################################################################################
    #                                                Generating Signal                                                   #
    ######################################################################################################################
    """

    # TODO: make it abstract
    @staticmethod
    def __generate_signal(
        signal: TradeSignal,
        timestamp: int = None,
    ) -> Signal:
        """
        - func __generate_signal():
            - Generate the signal based on the data.
            - It will be used to generate the signal based on the data.

        - param self: StrategyHandler
            - class object
        - param signal: object.TradeSignal
            - the signal object to be generated.

        - return indicator
        """
        return Signal(
            signal=signal,
            timestamp=(
                timestamp if (timestamp) else SignalGenerator.generate_timestamp()
            ),
        )

    def generate_golden_cross_signal(self) -> None:
        """
        - func generate_golden_cross_signal():
            - function to generate the golden cross signal generator.

        - A golden cross occurs when:
            - a short-term moving average (SMA) crosses above
            - a long-term moving average, indicating a potential bullish trend.
        """
        key: str = "golden_cross"
        while True:
            with self.indicators_lock:
                sma_data: dict | None = self.indicators.get("sma")
                ema_data: dict | None = self.indicators.get("ema")

            with self.signal_timestamps_lock:
                prev_timestamp: int = self.signal_timestamps.get(key, 0)
            curr_timestamp: int = SignalGenerator.generate_timestamp()

            if (curr_timestamp - prev_timestamp > self.signal_window) and (
                sma_data and ema_data
            ):  # only need to check if the sma and ema data are available.
                # generate the signal based on the data and passit to the signal pipeline.
                ten_sec_sma: float | None = sma_data.get(10)
                five_min_ema: float | None = ema_data.get(300)

                if ten_sec_sma and five_min_ema:
                    if ten_sec_sma > five_min_ema:
                        # generate the signal
                        signal: Signal = SignalGenerator.__generate_signal(
                            signal=TradeSignal.LONG_TERM_BUY
                        )
                        self.signal_pipeline.push_signal(signal)
                        trading_logger.info(
                            f"{__name__} - Golden Cross Signal has been generated!: Bullish Trend."
                        )

                with self.signal_timestamps_lock:
                    self.signal_timestamps[key] = curr_timestamp

            time.sleep(1.5)
        return None

    def generate_death_cross_signal(self) -> None:
        """
        - func generate_death_cross_signal():
            - function to generate the death cross signal generator.

        - A death cross occurs when:
            - a short-term moving average crosses below
            - a long-term moving average,
            - indicating a potential bearish trend.
        """
        key: str = "death_cross"
        while True:
            with self.indicators_lock:
                sma_data: dict = self.indicators.get("sma")
                ema_data: dict = self.indicators.get("ema")

            with self.signal_timestamps_lock:
                prev_timestamp: int = self.signal_timestamps.get(key, 0)
            curr_timestamp: int = SignalGenerator.generate_timestamp()

            if (curr_timestamp - prev_timestamp > self.signal_window) and (
                sma_data and ema_data
            ):  # only need to check if the sma and ema data are available.
                # generate the signal based on the data and passit to the signal pipeline.
                ten_sec_sma: float | None = sma_data.get(10)
                five_min_ema: float | None = ema_data.get(300)

                if ten_sec_sma and five_min_ema:
                    if ten_sec_sma < five_min_ema:
                        # generate the signal
                        signal: Signal = SignalGenerator.__generate_signal(
                            signal=TradeSignal.LONG_TERM_SELL
                        )
                        self.signal_pipeline.push_signal(signal)
                        trading_logger.info(
                            f"{__name__} - Death Cross Signal has been generated!: Bearish Trend."
                        )

                with self.signal_timestamps_lock:
                    self.signal_timestamps[key] = curr_timestamp

            time.sleep(1.5)
        return None

    def generate_price_moving_average_signal(self) -> None:
        """
        - func generate_price_moving_average_signal():
            - function to generate the price moving average signal generator.

        - Moving Average:
            - when the current price crosses above or below a specified MA.
            - This signal can indicate potential buy or sell opportunities based on the direction of the price movement relative to the moving average.

        - Compare the current price with the moving average.
            - If the current price crosses above the moving average, generate a "Price Above MA" signal.
            - If the current price crosses below the movign average, generate a "Price Below MA" signal.
        """
        key: str = (
            "price_moving_average"  # TODO: Check if we need to have the direction -> maybe separate this as well?
        )
        while True:
            with self.indicators_lock:
                sma_data: Dict[int, float] = self.indicators.get("sma")
                current_price: float = self.indicators.get("price")

            with self.signal_timestamps_lock:
                prev_timestamp: int = self.signal_timestamps.get(key, 0)
            curr_timestamp: int = SignalGenerator.generate_timestamp()

            if (curr_timestamp - prev_timestamp > self.signal_window) and (
                sma_data and current_price
            ):
                sma_60 = sma_data.get(60)  # Example for 1 min SMA

                if sma_60:
                    if current_price > sma_60:
                        signal: Signal = SignalGenerator.__generate_signal(
                            signal=TradeSignal.SHORT_TERM_BUY,
                        )
                        self.signal_pipeline.push_signal(signal)
                        trading_logger.info(
                            f"{__name__} - Short Term Buy Signal has been generated!: Bullish Trend."
                        )

                    elif current_price < sma_60:
                        signal: Signal = SignalGenerator.__generate_signal(
                            signal=TradeSignal.SHORT_TERM_SELL,
                        )
                        self.signal_pipeline.push_signal(signal)
                        trading_logger.info(
                            f"{__name__} - Short Term Sell Signal has been generated!: Bearish Trend."
                        )

                with self.signal_timestamps_lock:
                    self.signal_timestamps[key] = curr_timestamp

            time.sleep(1.5)
        return None

    def generate_ema_sma_divergence_signal(
        self,
        threshold: float = 0.05,  # TODO: need to define the threshold value.
    ) -> None:
        """
        - func generate_ema_sma_divergence_signal():
            - function to generate the EMA and SMA divergence signal generator.

        - param threshold: float
            - the threshold value to determine the divergence between EMA and SMA

        - Divergence:
            - There is a significant difference between the EMA and SMA.
            - This divergence can indicate potential changes in makret trends or momentum.
        """
        key: str = "ema_sma_divergence"
        while True:
            with self.indicators_lock:
                sma_data: Dict[int, float] = self.indicators.get("sma")
                ema_data: Dict[int, float] = self.indicators.get("ema")

            with self.signal_timestamps_lock:
                prev_timestamp: int = self.signal_timestamps.get(key, 0)
            curr_timestamp: int = SignalGenerator.generate_timestamp()

            if (curr_timestamp - prev_timestamp > self.signal_window) and (
                sma_data and ema_data
            ):
                sma_60 = sma_data.get(60)  # data for 1 min SMA
                ema_60 = ema_data.get(60)  # data for 1 min EMA

                if sma_60 and ema_60:
                    divergence: float = abs(sma_60 - ema_60)
                    if divergence > threshold:
                        signal: Signal = SignalGenerator.__generate_signal(
                            signal=TradeSignal.HOLD,
                        )
                        self.signal_pipeline.push_signal(signal)
                        trading_logger.info(
                            f"{__name__} - Divergence Signal has been generated!: Potential Trend Change."
                        )

                with self.signal_timestamps_lock:
                    self.signal_timestamps[key] = curr_timestamp

            time.sleep(1.5)
        return None

    def generate_price_reversal_signal(self) -> None:
        """
        - func generate_price_reversal_signal():
            - function to generate the price reversal signal generator.

        - A price reversal signal occurs when:
            - the price changes direction after a sustained trend.
            - This cna indicate potential buy or sell opportunities based on this.
        """
        key: str = "price_reversal"
        while True:
            with self.indicators_lock:
                sma_data: Dict[int, float] = self.indicators.get("sma")
                current_price: float = self.indicators.get("price")

            with self.signal_timestamps_lock:
                prev_timestamp: int = self.signal_timestamps.get(key, 0)
            curr_timestamp: int = SignalGenerator.generate_timestamp()

            if (curr_timestamp - prev_timestamp > self.signal_window) and (
                sma_data and current_price
            ):
                sma_60: float = sma_data.get(60)  # data for 1 min SMA

                if sma_60:
                    if current_price > sma_60:
                        signal: Signal = SignalGenerator.__generate_signal(
                            signal=TradeSignal.SHORT_TERM_BUY,
                        )
                        trading_logger.info(
                            f"{__name__} - Price Reversal Signal has been generated!: Bullish Reveral."
                        )
                        self.signal_pipeline.push_signal(signal)
                    elif current_price < sma_60:
                        signal: Signal = SignalGenerator.__generate_signal(
                            signal=TradeSignal.SHORT_TERM_SELL,
                        )
                        self.signal_pipeline.push_signal(signal)
                        trading_logger.info(
                            f"{__name__} - Price Reversal Signal has been generated!: Bearish Reveral."
                        )

                with self.signal_timestamps_lock:
                    self.signal_timestamps[key] = curr_timestamp

            time.sleep(1.5)
        return None
