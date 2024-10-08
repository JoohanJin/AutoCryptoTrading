import logging
import time
from functools import wraps

# config the basic log format
logging.basicConfig(
    filename=f"log/{time.strftime('%Y-%m-%d', time.localtime(time.time()))}.log",
    encoding='utf-8',
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
    )
logger = logging.getLogger("future logger")

# define log_decorator for the function, future usage consideration
def log_decorator(func: function) -> function:
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"Executing {func.__name__} with args: {args}, kwargas: {kwargs}")
        try:
            result = func(*args, **kwargs)
            logger.info(f"{func.__name__} returned {result}")
            return result
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {e}")
            raise
    return wrapper


"""
@log_decorator
def sample_function(list_of_params):
    do something

    return something
"""