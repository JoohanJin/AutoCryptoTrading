# STANDARD LIBRARY
import json
import time
import sys

# CUSTOM LIBRARY
from custom_telegram.telegram_bot_class import CustomTelegramBot
from manager.data_collector_and_processor import DataCollectorAndProcessor
from manager.signal_generator import SignalGenerator
from mexc.future import FutureWebSocket
from pipeline.data_pipeline import DataPipeline
from logger.set_logger import logger

class SystemManager:
    def __init__(
            self,
        ):
        """
        # func __init__():
            # Initialize the System Manager.

        # param self: SystemManager
            # class object

        # return None
        """

        # TODO: getting credentials put it here for authentication of
            # TelegramBot
            # WebSocket API
            # REST API SDK

        telegram_api_key, telegram_channel_id = self.__get_telegram_credentials()

        ws: FutureWebSocket = FutureWebSocket()
        pipeline: DataPipeline = DataPipeline()

        # TODO: authentication can be done here.
        telegram_bot: CustomTelegramBot = CustomTelegramBot(
            api_key = telegram_api_key,
            channel_id = telegram_channel_id,
        )

        data_collector_processor: DataCollectorAndProcessor = DataCollectorAndProcessor(
            pipeline = pipeline,
            websocket = ws,
        )

        signal_generator: SignalGenerator = SignalGenerator(
            data_pipeline = pipeline,
            custom_telegram_bot = telegram_bot,
        )

        # one more classs: trade decider -> it will have the FutureMarket SDWK

        try:
            while True:
                time.sleep(1) # Sleep to reduce the cpu usage.
        except KeyboardInterrupt:
            logger.info("Program interrupted by user. Exiting...")
            sys.exit(0)
        except Exception as e:
            logger.critical(f"Program encounters critical errors.{e}\n Exiting...")
            sys.exit(0)
            return
        
    def __get_telegram_credentials(self):
        f = open('./credentials/telegram_key.json')
        credentials = json.load(f)
        
        api_key = credentials["api_key"]
        channel_id = credentials["channel_id"]

        return api_key, channel_id
    

def main(): # to test run the system manager.
    main_system_manager: SystemManager = SystemManager()


"""
######################################################################################################################
#                                                     Code Run                                                       #
######################################################################################################################
"""
if __name__ == "__main__":
    main()