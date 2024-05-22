from base_sdk import *
import logging
import threading
import logging
import websocket # as recommended in the API page

logger = logging.getLogger(__name__)

# Global Variables
# ENDPOINTS
FUTURES: str = "https://contract.mexc.com"
SPOT: str = None # for now


class _GeneralWebSocket:
    def __init__(self) -> None:
        return