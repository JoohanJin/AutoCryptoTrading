from base_sdk import *
import logging
import asyncio
import threading
import logging
import websocket # as recommended in the API page
from typing import Literal, Union, Optional

logger = logging.getLogger(__name__)

# Global Variables
# ENDPOINTS
FUTURES: str = "wss://contract.mexc.com/edge"
SPOT: str = None # for now


class _WebSocketManager:
    def __init__(
            self,
            # callback_function,
            websocket_name,
            api_key: Optional[str] = None,
            secret_key: Optional[str] = None,
            ping_interval: Optional[int] = 20,
            ping_timeout: Optional[int] = 10,
            retries: Optional[int] = 10,
            restart_on_error: Optional[bool] = True,
            trace_logging: Optional[bool] = False
        ) -> None:

        self.api_key = api_key
        self.secret_key = secret_key

        self.ws = websocket_name
        return
    

class _FutureWebsocketManager(_WebSocketManager):
    def __init__(self) -> None:
        return