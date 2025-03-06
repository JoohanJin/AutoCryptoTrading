import logging
from logging.handlers import TimedRotatingFileHandler
import time
from datetime import datetime
from functools import wraps
import os

# TODO: Need to debug the behavior of the logger, it is not working as expected.

logging.basicConfig(
    level=logging.DEBUG,  # Set the logging level
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Format of the log messages
    handlers=[
        logging.FileHandler(f"log/{datetime.now().strftime('%Y-%m-%d')}~.log"),  # Log to a file
        logging.StreamHandler()  # Log to the console
    ]
)


logger = logging.getLogger("AutoTradingBot_Logger")
logger.setLevel(logging.INFO)

# define log_decorator for the function, future usage consideration
def log_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"Executing {func.__name__} with args: {args}, kwargas: {kwargs}")
        try:
            result = func(*args, **kwargs)
            if (result is not None and type(result) is not bool):
                logger.info(f"{func.__name__} returned {result}")
            else:
                logger.info(f"{func.__name__} executed and returned {result}")
            return result
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {e}")
            raise
    return wrapper