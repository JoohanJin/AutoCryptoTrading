import logging
from logging.handlers import TimedRotatingFileHandler
import time
from functools import wraps
import os

#TODO: Need to implement the dynamic logging file generator.
# config the basic log format
# logging.basicConfig(
#     filename=f"log/{time.strftime('%Y-%m-%d', time.localtime(time.time()))}.log",
#     encoding='utf-8',
#     format="%(asctime)s - %(levelname)s - %(message)s",
#     level=logging.INFO
# )
log_dir: str = "log"
if (not os.path.exists(log_dir)):
    os.makedirs(log_dir)

log_filename: str = os.path.join(log_dir, f"{time.strftime('%Y-%m-%d', time.localtime(time.time()))}.log")

# create a TimedRotatingFileHandler object based on the current date, which rotates logs at midnight
handler = TimedRotatingFileHandler(
    log_filename,
    when="midnight",
    interval=1,
    encoding='utf-8'
)
handler.suffix = "%Y-%m-%d"

# define the log format
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

# create a logger
logger = logging.getLogger("TradingBot Logger")
logger.setLevel(logging.INFO)
logger.addHandler(handler)

# Prevent duplicate handlers if the logger is imported multiple times.
logger.propagate = False


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


"""
# Sample Usage

@log_decorator
def sample_function(list_of_params):
    do something

    return something
"""