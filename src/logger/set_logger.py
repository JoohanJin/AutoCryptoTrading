import logging
from logging.handlers import TimedRotatingFileHandler
import time
from functools import wraps
import os

import logging
from logging.handlers import TimedRotatingFileHandler
import os
from datetime import datetime
import time

# Log directory
log_dir = "log"
os.makedirs(log_dir, exist_ok=True)

# Base log file name (not directly used for rotation but required by the handler)
log_filename: str = os.path.join(log_dir, f"{time.strftime('%Y-%m-%d', time.localtime(time.time()))}.log")


# Custom TimedRotatingFileHandler to use timestamps as file names
class TimestampedRotatingFileHandler(TimedRotatingFileHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def rotation_filename(self, default_name):
        """
        Override the default rotation filename logic to use a timestamp.
        """
        # Generate a timestamped file name in the format YYYY-MM-DD_HH-MM-SS.log
        timestamp = datetime.now().strftime("%Y-%m-%d")
        return os.path.join(os.path.dirname(self.baseFilename), f"{timestamp}.log")


# Create a custom handler
handler = TimestampedRotatingFileHandler(
    filename=log_filename,  # Base file name (required by the handler)
    when="s",               # Rotate every second
    interval=1,             # Interval of 1 second
    backupCount=5,          # Keep the last 5 rotated logs
    encoding='utf-8'
)

# Define log format
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

# Create logger
logger = logging.getLogger("Timestamped Logger")
logger.setLevel(logging.INFO)
logger.addHandler(handler)

# Prevent propagation
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