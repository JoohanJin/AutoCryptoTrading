# STANDARD LIBRARY
import time
import sys

# CUSTOM LIBRARY
from src.data_fetcher import DataCollectorAndProcessor
from src.strategy_manager import StrategyHandler
from src.pipeline.data_pipeline import DataPipeline
from src.set_logger import logger


def main():
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


"""
######################################################################################################################
#                                                     Code Run                                                       #
######################################################################################################################
"""
if __name__ == "__main__":
    main()