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
            callback_function,
            websocket_name,
            api_key: Optional[str] = None,
            secret_key: Optional[str] = None,
            ping_interval: Optional[int] = 20,
            ping_timeout: Optional[int] = 10,
            retries: Optional[int] = 10,
            restart_on_error: Optional[bool] = True,
            # trace_logging: Optional[bool] = False
        ) -> None:

        # Set API key
        self.api_key = api_key
        self.secret_key = secret_key

        # get the callback function
        self.callback = callback_function

        # get the websocket and store in the class
        self.ws = websocket_name

        if (api_key):
            self.ws += " (Auth)"

        # ping settings
        self.ping_interval = ping_interval
        self.ping_timeout = ping_timeout
        self.retry_count = retries

        # to save the list of subcriptions and the function for each subcription
        """
        {
            <subscription-type>: callback function
        }
        """
        self.callback_directory = {}

        self.restart_on_error = restart_on_error

        return
    
    def exit(self):
        """
        close the wevsocket
        """
        self.ws.close()
    

    

class _FutureWebsocketManager(_WebSocketManager):
    def __init__(self) -> None:
        return