from base_sdk import *
import logging
import asyncio
import threading
import logging
import websocket # as recommended in the API page
from typing import Literal, Union, Optional
import time
import hashlib
import threading

logger = logging.getLogger(__name__)

# Global Variables
# ENDPOINTS
FUTURES: str = "wss://contract.mexc.com/edge"
SPOT: str = None # for now


class __BasicWebSocketManager:
    """
    Methods
    # _connect
    # _subscribe
    # _authenticate: using api_key and secret_key
    # _on_message
    # _on_close
    # _on_open
    # _on_error
    # _ping_loop
    # _is_connected
    """
    def __init__(
            self,
            # callback_function,
            api_key: Optional[str] = None,
            secret_key: Optional[str] = None,
            ping_interval: Optional[int] = 30,
            ping_timeout: Optional[int] = 10,
            retries: Optional[bool] = True,
            restart_on_error: Optional[bool] = True,
            log_or_not: Optional[bool] = True
        ):

        # Set API key
        self.api_key = api_key
        self.secret_key = secret_key

        # websocket API endpoint
        self.endpoint = FUTURES

        # get the callback function
        # self.callback = callback_function

        # get the websocket and store in the class
        self.ws = None

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

        self.retries = True
        self.restart_on_error = restart_on_error
    
    
    def _connect(self):
        infinite_reconnect: bool = False

        # if there is no retries attribute set to True, then no need to try, but we will anyway
        if self.retries:
            infinite_reconnect = True

        while (infinite_reconnect) and not self._is_connected():
            self.ws = websocket.WebSocketApp(
                url = self.endpoint,
                on_message=self._on_message(),
                on_open=self._on_open(),
                on_close=self._on_close(),
                on_error=self._on_error()
                )
            
            # thread for connection
            self.wst = threading.Thread(target = lambda: self.ws.run_forever(
                ping_interval = self.ping_interval,
                ping_timeout = self.ping_timeout
            ))
            self.wst.daemon = True
            self.wst.start()

            # thread for ping
            self.wsp = threading.Thread(target = lambda: self._ping_loop(
                ping_interval=30
            ))
            self.wsp.daemon = True
            self.wsp.start()

        # logger.INFO("")

        # TODO: implement timeout for connection


        return
    

    def _is_connected(self):
        try:
            if self.ws.sock or not self.ws.sock.is_connected:
                return True
            else:
                return False
        except:
            return False

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


    def _on_error(self, message):
        return
    

    def _on_open(self):
        return
    

    def _on_close(self):
        return

    
    def _ping_loop(
            self,
            ping_interval: int,
            ping_payload: str = '{"method":"ping"}',

        ) -> None:
        time.sleep(ping_interval)
        while True:
            self.ws.send(ping_payload)


    def _exit(self):
        """
        close the websocket
        """
        self.ws.close()
    

class _FutureWebsocketManager(__BasicWebSocketManager):
    def __init__(self):
        return