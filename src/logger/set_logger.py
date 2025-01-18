import logging
from logging.handlers import TimedRotatingFileHandler
import time
from datetime import datetime
from functools import wraps
import os

# TODO: Need to debug the behavior of the logger, it is not working as expected.

# Custom TimedRotatingFileHandler to use timestamps as file names
class TimestampedRotatingFileHandler(TimedRotatingFileHandler):
    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)

    def rotation_filename(
        self,
        default_name,
    ) -> str:
        """
        Override the default rotation filename logic to use a timestamp.
        """
        # Generate a timestamped file name in the format YYYY-MM-DD_HH-MM-SS.log
        timestamp = datetime.now().strftime("%Y-%m-%d")
        return os.path.join(os.path.dirname(self.baseFilename), f"{timestamp}.log")

# Log directory
log_dir = "log"

# Log directory creations
os.makedirs(
    log_dir,
    exist_ok = True
)

# Base log file name (not directly used for rotation but required by the handler)
log_filename: str = os.path.join(
    log_dir,
    f"log_file.log"
)


# Create a custom handler
handler = TimestampedRotatingFileHandler(
    filename = log_filename,  # Base file name (required by the handler)
    when = "midnight",  # Rotate every second
    interval = 1,   # Interval of 1 second
    encoding = 'utf-8', # Encoding
)

# Define log format
formatter: logging.Formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Set log formatter
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