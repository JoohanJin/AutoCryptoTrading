# STANDARD LIBRARY
import json
import time
import sys

# CUSTOM LIBRARY
from custom_telegram.telegram_bot_class import CustomTelegramBot
from manager.data_collector_and_processor import DataCollectorAndProcessor
from manager.signal_generator import SignalGenerator
from manager.trade_manager import TradeManager
from mexc.future import FutureMarket, FutureWebSocket
import object
from pipeline.data_pipeline import DataPipeline
from logger.set_logger import operation_logger, log_decorator
from pipeline.signal_pipeline import SignalPipeline
from src.interface.pipeline_interface import PipelineController
from src.object.constants import IndexType


class SystemManager:
    @log_decorator
    def __init__(
        self,
    ):
        """
        func __init__():
            - Initialize the System Manager.

        param self: SystemManager
            - class object

        return None
        """
        # prepare the necessary parts for injection.
        self.ws:            FutureWebSocket = FutureWebSocket()  # type: ignore
        self.data_pipeline:    DataPipeline = DataPipeline()
        self.signal_pipline: SignalPipeline = SignalPipeline()
        self.mapper:     object.ScoreMapper = object.ScoreMapper()

        self.data_pipeline_controller: PipelineController[dict[str, int | IndexType, dict[int, float]]] = PipelineController(pipeline = self.data_pipeline)
        self.signal_pipeline_controller:        PipelineController[dict[str, int | object.TradeSignal]] = PipelineController(pipeline = self.signal_pipline)

        # TODO: authentication can be done here.
        self.telegram_bot: CustomTelegramBot = self.__set_up_telegram_bot()
        self.mexc_sdk:          FutureMarket = self.__set_up_mexc_sdk()

        self.data_collector_processor: DataCollectorAndProcessor = (
            DataCollectorAndProcessor(
                pipeline_controller = self.data_pipeline_controller,
                websocket = self.ws,
            )
        )

        self.signal_generator: SignalGenerator = SignalGenerator(
            data_pipeline = self.data_pipeline,
            custom_telegram_bot = self.telegram_bot,
            signal_pipeline = self.signal_pipline,
        )

        # one more classs: trade_manager -> it will have the FutureMarket SDWK
        self.trade_manager: TradeManager = TradeManager(
            signal_pipeline = self.signal_pipline,
            mexc_future_market_sdk = self.mexc_sdk,
            delta_mapper = self.mapper,
            telegram_bot = self.telegram_bot,
        )

        try:
            while True:
                time.sleep(1)  # Sleep to reduce the cpu usage.
        except KeyboardInterrupt:
            operation_logger.info("Program interrupted by user. Exiting...")
            sys.exit(0)
        except Exception as e:
            operation_logger.critical(
                f"{__name__} - Program encounters critical errors."
            )
            raise Exception(f"Program encounters critical errors.{str(e)}\n Exiting...")  # ! raise the custom Exceptions.

        return

    @log_decorator
    def __set_up_telegram_bot(
        self,
    ) -> CustomTelegramBot:
        """
        func __set_up_telegram_bot():
            - Set up the telegram bot with the given credentials.

        param self: SystemManager
            - class object

        return CustomTelegramBot
            - CustomTelegramBot object
            - has been registered with the custom channel id.
        """
        api_key, channel_id = SystemManager.__get_telegram_credentials()
        return CustomTelegramBot(
            api_key=api_key,
            channel_id=channel_id,
        )

    @log_decorator
    def __set_up_mexc_sdk(
        self,
    ) -> FutureMarket:
        """
        func __set_up_mexc_sdk():
            - Set up the MexC SDK with the given credentials.

        param self: SystemManager
            - class object

        return FutureWebSocket
            - FutureWebSocket object
            - has been registered with the given api_key and secret_key.
        """
        api_key, secret_key = SystemManager.__get_mexc_crendentials()
        return FutureMarket(
            api_key=api_key,
            secret_key=secret_key,
        )

    """
    ######################################################################################################################
    #                                                Static Method                                                       #
    ######################################################################################################################
    """

    @staticmethod
    def __get_telegram_credentials():
        # TODO: Fetch credentials from Environment Variable
        f = open("./credentials/telegram_key.json")
        credentials = json.load(f)

        api_key = credentials["api_key"]
        channel_id = credentials["channel_id"]

        return api_key, channel_id

    @staticmethod
    def __get_mexc_crendentials():
        # TODO: Fetch credentials from Environment Variable
        f = open("./credentials/mexc_keys.json")
        credentials = json.load(f)

        api_key = credentials["api_key"]
        secret_key = credentials["secret_key"]

        return api_key, secret_key


def main():  # to test run the system manager.
    main_system_manager: SystemManager = SystemManager()


"""
######################################################################################################################
#                                                     Code Run                                                       #
######################################################################################################################
"""
if __name__ == "__main__":
    main()
