import logging

# config the basic log format
logging.basicConfig(
    filename="test.log",
    encoding='utf-8',
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
    )
logger = logging.getLogger("mexc_client_logger")


logger.info("test")
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