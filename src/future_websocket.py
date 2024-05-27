# Built-in Library
from base_sdk import *
import asyncio
import threading
import logging
import websocket # as recommended in the API page, https://websocket-client.readthedocs.io/en/latest/index.html
from typing import Literal, Union, Optional
import time
import hashlib
import threading

# Customized Library
from set_logger import logger

# Global Variables
# ENDPOINTS
FUTURE: str = "wss://contract.mexc.com/edge"
# SPOT: str = None

# TODO: implement the logging functionality -> send the log to the telegram for making an order
# logging file
# telegram

class __BasicWebSocketManager:
    def __init__(
        self,
        callback_function = None,
        endpoint: Optional[str] = "wss://contract.mexc.com/edge",
        ws_name: Optional[str] = None,
        api_key: Optional[str] = None,
        secret_key: Optional[str] = None,
        ping_interval: Optional[int] = 30,
        ping_timeout: Optional[int] = 10,
        retries: Optional[bool] = True,
        restart_on_error: Optional[bool] = True,
        log_or_not: Optional[bool] = True,
        conn_timeout: Optional[int] = 30,
        login_required: Optional[bool] = False
    ):
        # Set API key
        self.api_key = api_key
        self.secret_key = secret_key

        # do we need to login for this WebSocketManager?
        self.login_required = login_required

        # websocket API endpoint
        self.endpoint = endpoint

        # get the callback function
        # self.callback = callback_function

        # get the websocket name
        self.ws_name = ws_name

        # ping settings
        self.ping_interval = ping_interval
        self.ping_timeout = ping_timeout
        self.retry_count = retries

        # callback function setting
        self.callback_function = callback_function

        # connection timeout interval
        self.conn_timeout = conn_timeout

        # to save the list of subcriptions and the function for each subcription
        """
        {
            <subscription-type>: <callback-function>
        }
        """
        self.callback_dictionary = {}

        # record the subscription made
        self.subscriptions = []

        self.retries = True
        self.restart_on_error = restart_on_error

        # has the Websocket been authroized by the API? -> false initially
        self.auth = False

        # enable logging -> TODO: Test
        websocket.enableTrace(traceable=log_or_not, handler=logger, level='INFO')


    def _connect(self):
        """
        # connect WebSocketApp to the API endpoint
        """
        # if there is no retries attribute set to True, then no need to try, but we will anyway
        infinite_reconnect: bool = False
        if self.retries:
            infinite_reconnect = True

        while (infinite_reconnect or self.conn_timeout) and not self._is_connected():
            # will make the WebSocketApp and will try to connect to the host
            self.ws = websocket.WebSocketApp(
                url= self.endpoint,
                on_message=lambda ws, msg: self._on_message(msg),
                on_open=self._on_open(),
                on_close=self._on_close(),
                on_error=lambda ws, err: self._on_error(err)
            )
            
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
            
            time.sleep(1)

        # if timeout occurred
        if (not self.conn_timeout):
            # connection timeout
            # retry connection is set to False
            logger.info("connection trial timeout for the WebSocket")
            return

        logger.info(f"WebSocket has been connected to {self.endpoint}")

        if self.login_required:
            try:
                if self.api_key and self.secret_key:
                    self._authenticate()
            except Exception as e: # most likely no api_key
                logger.info(f"Exception Occured: {e}")

        return
    
    
    def _authenticate(self):
        """
        # method: _authenticate
        # login to the endpoint for private endpoint
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
        logger.info("login request has been sent!")
        return


    def _set_callback(
            self,
            topic: str,
            callback_func
    ):
        # self.callback_dictionary[topic] = callback_func
        return
    

    def _is_connected(self):
        try:
            if self.ws.sock or not self.ws.sock.is_connected:
                return True
            else:
                return False
        except AttributeError: # exception handling, if there is any error occurred just return False
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
        return self.callback_function(response)


    def _on_error(
            self,
            exception
        ):
        """
        # when there is an error
        # Exit and raise errors or attempt to reconnect
        """
        logger.error(f"Unknown Error Occurred: {exception}")
        return
    

    def _on_open(self):
        """
        # when the websocket is open
        """
        logger.info("ws has been opened")
        return
    

    def _on_close(
            self,
            # status_code : int,
            # close_msg : str
        ):
        """
        # websocket close
        # logging the status code and the msg into the logger
        """
        # logger.info(f"logger has been closed: status code - {status_code}, close message = {close_msg}")
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
            time.sleep(ping_interval)


    def _reset(self):
        """
        # _reset the WebSocket when reset signal incurred
            # e.g., when there is error and we need to reset the entire program
        """
        self.subscriptions.clear()
        self.callback_dictionary.clear()
        logger.info(f"WebSocketApp, {self.ws_name} has been reset.")
        return
    

    def _exit(self):
        """
        close the websocket
        """
        self.ws.close()

        logger.info("The WebSocket Manager has been terminated - might need to restart the entire program")

        while self.ws.sock:
            continue
    

class _FutureWebsocketManager(__BasicWebSocketManager):
    def __init__(
        self,
        callback_fuction= None,
        ws_name = "test",
        **kwargs
    ):
        logger.debug(f"{kwargs}")
        # self.callback_function = kwargs.pop("callback_function") if kwargs.get("callback_function") else self._default_callback

        super().__init__(callback_function=callback_fuction, ws_name=ws_name, **kwargs)

        self.private_topics = [
            "personal.order",
            "personal.asset",
            "personal.position",
            "personal.risk.limit",
            "personal.adl.level",
            "personal.position.mode"
        ]

        if not callback_fuction:
            self.callback_function = self._default_callback

        # self._connect()

        return

    def connect(self):
        self._connect()
        return
    
    def subscribe(
            self, 
            topic, 
            callback = None, 
            params: dict = None
    ):
        query = dict(
            method = topic,
            param = params
        )

        while (not self._is_connected()):
            time.sleep(0.1)

        logger.info("subscription header has been sent")

        header = json.dumps(query)
        self.ws.send(header)
        self.subscriptions.append(query)

        logger.info(f"new sub has been established: {self.subscriptions}")

        self._set_callback(topic, self.callback_function)

        return

    
    def _default_callback(self, msg):
        # comprehensive callback function which can deal with all of the message
        """
        Types of Response
            # auth_message
            # subscribe response
            # pong
        """

        def is_auth_response():
            if msg.get("channel") == 'rs.login':
                return True
            return False
        
        def is_sub_response():
            if str(msg.get("channel","")).startswith("rs.sub."):
                return True
            return False
        
        def is_pong_msg():
            if msg.get("channel", "") == "pong":
                return True
            return False
        
        if is_auth_response():
            self._deal_with_auth_msg(msg=msg)
        elif is_sub_response():
            self._deal_with_sub_msg(msg=msg)
        elif is_pong_msg():
            pass
        else:
            self._deal_with_normal_msg(msg=msg)

        return
    

    def _deal_with_auth_msg(
            self,
            msg
        ):
        """
        Determine if the login has been successful.
        # notify the result to the user by logger.
        """
        if msg.get("data") == "success": # login success
            logger.info(f"Authorization for {self.ws_name} has been successful.")
            self.auth = True
        else: # login fail
            logger.debug(
                f"Authoriztion for {self.ws_name} has not been successful."
                f"Please check your keys!"
            )
        return

    
    def _deal_with_sub_msg(self, msg):
        topic = msg.get("channel")

        if msg.get("channel", "") != "rs.error":
            logger.info(f"Subscription to {topic} has been established")
        elif msg.get("channel", "") == "rs.error":
            logger.debug(f"Subscription to {topic} has failed to establish")
        return
    

    def _deal_with_normal_msg(self, msg):
        topic = msg.get("channel")
        data = msg.get("data")

        # logger.info(f"msg regarding {topic} has been received")

        print(f"topic is : {topic}")
        print(f"data is : {data}")
        return