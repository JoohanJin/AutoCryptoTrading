from base_sdk import *
import logging
import asyncio
import threading
import logging
import websocket # as recommended in the API page
from typing import Literal, Union, Optional
import time
import hashlib

logger = logging.getLogger(__name__)

# Global Variables
# ENDPOINTS
FUTURES: str = "wss://contract.mexc.com/edge"
SPOT: str = None # for now


class __BasicWebSocketManager:
    """
    Methods
    # _subscribe
    # _authenticate: using api_key and secret_key
    # _on_message
    # _on_close
    # _on_open
    # _on_error
    # _ping_loop
    # 
    """
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
            log_or_not: Optional[bool] = True
        ):

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
            <subscription-type>: <callback-function>
        }
        """
        self.callback_dictionary = {}

        self.restart_on_error = restart_on_error
    
    
    def _generate_signature(self):
        """
        # make a signatrue for future 
        """

        timestamp = str(int(time.time() * 1000))
        _query_str = self.api_key + timestamp
        signature = hmac.new(
            self.secret_key.encode("utf-8"),
            _query_str.encode("utf-8"),
            hashlib.sha256
            ).hexdigest()
        
        return signature
    
    
    def _on_message(self, message):
        """
        Parsing the message from the server
        """

        return
    

    def _exit(self):
        """
        close the websocket
        """
        self.ws.close()
    

    def _ping_loop(
            self,
            ping_interval: int,
            ping_payload: str = '{"method":"ping"}',

        ) -> None:
        time.sleep(ping_interval)
        while True:
            self.ws.send(ping_payload)

    

class _FutureWebsocketManager(__BasicWebSocketManager):
    def __init__(self):
        return