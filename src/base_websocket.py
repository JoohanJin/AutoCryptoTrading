# Built-in Library
from base_sdk import *
import asyncio
import threading
import logging
import websocket # as recommended in the API page
from typing import Literal, Union, Optional
import time
import hashlib
import threading

# Customized Library
from set_logger import logger

# Global Variables
# ENDPOINTS
FUTURES: str = "wss://contract.mexc.com/edge"
SPOT: str = None # for now

# TODO: implement the logging functionality -> send the log to the telegram for making an order
# logging file
# telegram

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
    # _authenticate
    """
    def __init__(
        self,
        callback_function: Optional[function] = None,
        api_key: Optional[str] = None,
        secret_key: Optional[str] = None,
        ping_interval: Optional[int] = 30,
        ping_timeout: Optional[int] = 10,
        retries: Optional[bool] = True,
        restart_on_error: Optional[bool] = True,
        log_or_not: Optional[bool] = True,
        conn_timeout: Optional[int] = 30,
    ):
        """
        # 
        """
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

        # connection timeout interval
        self.conn_timeout = 30

        # to save the list of subcriptions and the function for each subcription
        """
        {
            <subscription-type>: <callback-function>
        }
        """
        self.callback_dictionary = {}

        self.retries = True
        self.restart_on_error = restart_on_error
    

    def _subscribe(self):
        return

    
    def _connect(self):
        # if there is no retries attribute set to True, then no need to try, but we will anyway
        infinite_reconnect: bool = False
        if self.retries:
            infinite_reconnect = True

        while (infinite_reconnect or self.conn_timeout) and not self._is_connected():
            # will make the WebSocketApp and will try to connect to the host
            self.ws = websocket.WebSocketApp(
                url = self.endpoint,
                on_message=self._on_message(),
                on_open=self._on_open(),
                on_close=self._on_close(),
                on_error=self._on_error()
            )
            
            # TODO: implement timeout for connection

            # thread for connection
            self.wst = threading.Thread(
                target = lambda: self.ws.run_forever(
                    ping_interval = self.ping_interval,
                    ping_timeout = self.ping_timeout
                )
            )

            self.wst.daemon = True # set this as the background program where it tries to connect
            self.wst.start() # start the thread for making a connection

            # thread for ping
            self.wsp = threading.Thread(
                target = lambda: self._ping_loop(
                    ping_interval=30
                )
            )

            self.wsp.daemon = True # set as the background thread
            self.wsp.start() # start the thread for ping

            if not infinite_reconnect:
                self.conn_timeout -= 1

        # logger.INFO("")
        return
    
    
    def _authenticate(self):
        """
        # method: _authenticate
        # login for the websocket
        """
        timestamp: str = str(int(time.time() * 1000))
        _signature: str = self.api_key + timestamp

        signature = hmac.new(
            self.secret_key.encode("utf-8"),
            _signature.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()

        header = json.dumps(
            dict(
                subscribe = False,
                method = "login",
                param = dict(
                    apiKey = self.api_key,
                    reqTime = timestamp,
                    signature = signature
                )
            )
        )
        self.ws.send(header)
        return
    

    def _is_connected(self):
        try:
            if self.ws.sock or not self.ws.sock.is_connected:
                return True
            else:
                return False
        except: # exception handling, if there is any error occurred just return False
            # TODO: logging
            return False
        

    def _generate_signature(self):
        """
        # make a signature for future private websocket API
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
        # Parsing the message from the server
        """
        # parsing the message into the json
        response = json.loads(message)

        # now response is parsed as a dictionary so that we can do something with it.
        return


    def _on_error(self, message):
        """
        # when there is an error
        # Exit and raise errors or attempt to reconnect
        """
        # TODO: logging
        # TODO: 
        return
    

    def _on_open(self):
        """
        # when the websocket is open
        """
        # TODO: logging
        return
    

    def _on_close(self):
        """
        # websocket close
        # logging
        """
        return

    
    def _ping_loop(
            self,
            ping_interval: int,
            ping_payload: str = '{"method":"ping"}',
        ) -> None:
        """
        # method: _ping_loop
        # for the ping thread of WebSocketApp
        """
        time.sleep(ping_interval)
        while True:
            self.ws.send(ping_payload)


    def _exit(self):
        """
        close the websocket
        """
        self.ws.close()

        # TODO: need to add a logging

        while self.ws.sock:
            continue
    

class _FutureWebsocketManager(__BasicWebSocketManager):
    def __init__(self):
        return