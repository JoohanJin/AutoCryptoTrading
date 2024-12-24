# STANDARD LIBRARY
import time
import sys

# CUSTOM LIBRARY
from custom_telegram.telegram_bot_class import CustomTelegramBot
from manager.data_collector_and_processor import DataCollectorAndProcessor
from manager.strategy_manager import StrategyHandler
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
        pipeline: DataPipeline = DataPipeline()

        telegram_bot: CustomTelegramBot = CustomTelegramBot()

        data_collector_processor: DataCollectorAndProcessor = DataCollectorAndProcessor(
            pipeline = pipeline
        )

        strategy_handler: StrategyHandler = StrategyHandler(
            pipeline = pipeline,
            custom_telegram_bot = telegram_bot,
        )
        

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

def main(): # to test run the system manager.
    main_system_manager: SystemManager = SystemManager()


"""
######################################################################################################################
#                                                     Code Run                                                       #
######################################################################################################################
"""
if __name__ == "__main__":
    main()