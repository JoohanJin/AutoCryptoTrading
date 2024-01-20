import logging

# config the basic log format
logging.basicConfig(
    filename="example.log",
    encoding='utf-8',
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.DEBUG
    )
logger = logging.getLogger("mexc_client_logger")