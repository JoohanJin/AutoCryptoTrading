# STANDARD LIBRARY
import time
import sys

# CUSTOM LIBRARY
from data_fetcher import DataCollectorAndProcessor
from strategy_manager import StrategyHandler
from pipeline.data_pipeline import DataPipeline
from set_logger import logger

class SystemManager:
    def __init__(
            self,
        ):
        pipeline: DataPipeline = DataPipeline()
        d: DataCollectorAndProcessor = DataCollectorAndProcessor(
            pipeline = pipeline
        )
        s: StrategyHandler = StrategyHandler(
            pipeline = pipeline
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

def main():
    main: SystemManager = SystemManager()

"""
######################################################################################################################
#                                                     Code Run                                                       #
######################################################################################################################
"""
if __name__ == "__main__":
    main()