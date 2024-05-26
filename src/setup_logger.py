import logging
import time

# config the basic log format
logging.basicConfig(
    filename=f"{time.strftime('%Y-%m-%d', time.localtime(time.time()))}.log",
    encoding='utf-8',
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
    )
logger = logging.getLogger("bot_logger")

if __name__=="__main__":
    logger.info("test")

"""
logging.basicConfig(
    filename = f"{time.strftime("%Y-%m-%D %H:%M:%S %Z", time.localtime(time.time()))}",
    filemode='a', # append, if the file exists, create new if there is no such file
    level="INFO"
)
"""

"""
# testing logging library

import logging
logger = logging.getLogger("client_logger")

def main():
    logging.basicConfig(
        filename="test.log",
        encoding='utf-8',
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=logging.INFO
        )
    logger.info('started')
    print("do something")
    logger.info('done')

if __name__ == "__main__":
    main()
"""