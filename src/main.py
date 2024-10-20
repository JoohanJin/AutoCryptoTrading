# STANDARD LIBRARY
import time
import sys

# CUSTOM LIBRARY
from src.data_fetcher import DataFetcher
from src.data_processor import StrategyHandler
from src.pipeline.data_pipeline import DataPipeline
from src.set_logger import logger


if __name__ == "__main__":
    pipeline: DataPipeline = DataPipeline()

    d: DataFetcher = DataFetcher(
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