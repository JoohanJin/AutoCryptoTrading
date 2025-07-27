import logging
from logging.handlers import TimedRotatingFileHandler
import time
from datetime import datetime
from functools import wraps
import os


"""
############################################################################################################################################
# Operator Logger
# This logger is used to log the operations of the system
# It logs the operations of the system, such as starting and stopping the system, and any errors that occur.
############################################################################################################################################
"""
# Operation logger
operation_logger: logging.Logger = logging.getLogger("SystemLogger")  # operation logger
operation_logger.setLevel(logging.INFO)  # Set the logging level to INFO

# Operation logger - Formatter for log messages
operation_logger_formatter: logging.Formatter = logging.Formatter(
    "System - %(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Operation logger - File Handler
operation_logger_file_handler: TimedRotatingFileHandler = TimedRotatingFileHandler(
    f"log/system-logging.log",
    when="midnight",  # rotate at midnight
    interval=1,  # Rotate every day
    backupCount=14,  # keep 14 days of logs
    encoding="utf-8",  # Set the encoding to utf-8
    delay=False,  # Do not delay the creation of the log file
)  # Log file handler
operation_logger_file_handler.setFormatter(
    operation_logger_formatter
)  # Set the formatter for the file handler

# Operation logger - Console Handller
operation_logger_console_handler: logging.StreamHandler = (
    logging.StreamHandler()
)  # Console handler
operation_logger_console_handler.setFormatter(
    operation_logger_formatter
)  # Set the formatter for the console handler

operation_logger.addHandler(
    operation_logger_file_handler
)  # Add the file handler to the logger
operation_logger.addHandler(
    operation_logger_console_handler
)  # Add the console handler to the logger

"""
############################################################################################################################################
# Trading Logger
# This logger is used for signal generator
############################################################################################################################################
"""
# Trading Logger
trading_logger: logging.Logger = logging.getLogger("TradingLogger")
trading_logger.setLevel(logging.INFO)  # Set the logging level to INFO

# Trading Logger - Formatter for log messages
trading_logger_formatter: logging.Formatter = logging.Formatter(
    "Trading - %(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Trading Logger - File Handler
trading_logger_file_handler: TimedRotatingFileHandler = TimedRotatingFileHandler(
    filename=f"log/trading-logging.log",
    when="midnight",  # rotate at midnight
    interval=1,  # Rotate every day
    backupCount=14,  # keep 14 days of logs
    encoding="utf-8",  # Set the encoding to utf-8
    delay=False,  # Do not delay the creation of the log file
)  # Log file handler
trading_logger_file_handler.setFormatter(
    trading_logger_formatter
)  # Set the formatter for the file handler

trading_logger.addHandler(
    trading_logger_file_handler
)  # Add the file handler to the logger

# Logger Generation has been completed.
operation_logger.info(
    f"{__name__} - {operation_logger.name} - Operation Logger generation completed."
)
trading_logger.info(
    f"{__name__} - {trading_logger.name} - Trading Logger generation completed."
)


# define log_decorator for the function, future usage consideration
# def log_decorator(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         operation_logger.info(f"Executing {func.__name__} with args: {args}, kwargas: {kwargs}")
#         try:
#             result = func(*args, **kwargs)
#             if (result is not None and type(result) is not bool):
#                 operation_logger.info(f"{func.__name__} returned {result}")
#             else:
#                 operation_logger.info(f"{func.__name__} executed and returned {result}")
#             return result
#         except Exception as e:
#             operation_logger.error(f"Error in {func.__name__}: {e}")
#             raise
#     return wrapper


def log_decorator(func):
    def entering(func, *args):
        operation_logger.debug(f"Entering function '{func.__name__}'")
        # operation_logger.info(func.__doc__)
        operation_logger.info(
            f"Function at line {func.__code__.co_firstlineno} in {func.__code__.co_filename}"
        )

    def exiting(func):
        operation_logger.debug(f"Exiting function '{func.__name__}'")

    @wraps(func)
    def wrapper(*args, **kwargs):
        entering(func, *args)
        result = func(*args, **kwargs)
        exiting(func)
        return result

    return wrapper


if __name__ == "__main__":
    # Test the logger
    operation_logger.info("This is a test log message.")
    trading_logger.info("This is a test trading log message.")
    operation_logger.error("This is a test error log message.")
    trading_logger.error("This is a test trading error log message.")
