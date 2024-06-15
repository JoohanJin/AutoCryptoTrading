# Built-in Library
import sys
from .base_sdk import *
import threading
from typing import Literal, Union, Optional
import time
import hashlib
import threading
import hmac
import json
import websocket

# get the Logger
sys.path.append('..')
from set_logger import logger


class __BasicWebSocketManager:
    def __init__(
        self,
        # callback_function = None,
        # endpoint: Optional[str] = "wss://contract.mexc.com/edge",
        ws_name: Optional[str] = None,
        api_key: Optional[str] = None,
        secret_key: Optional[str] = None,
        ping_interval: Optional[int] = 20,
        ping_timeout: Optional[int] = 10,
        retries: Optional[bool] = True,
        restart_on_error: Optional[bool] = True,
        log_or_not: Optional[bool] = True,
        conn_timeout: Optional[int] = 30,
    ):
        """
        # method: __init__()
            # params:
                # callback_function: function, general callback_function for entire response from the endpoint
                # endpoint: MexC Websocket API endpoint
                # ws_name: WebSocketName
                # api_key: api_key for API usage
                # secret_key: secret_key for API usage
                # ping_interval: WebSocketConnection ping interval, default 20 seconds
                # ping_timeout: if there is no response for ping resposne for 10 seconds, close the websocket with the endpoint
                # retries: retries for WebSocket Connection for error
                    # TODO: error handling not yet implemented
                # restart_on_error: retries on error
                # log_or_not: if the WebSocket behavior will be logged or not
                # conn_timeout: WebSocket will try to connect to the endpoint for the timeout interval
                # login_required: if the websocket needs to authenticate to the system or not
        """
        # Set API key
        self.api_key = api_key
        self.secret_key = secret_key

        # do we need to login for this WebSocketManager?

        # get the callback function
        # self.callback = callback_function

        # get the websocket name
        self.ws_name = ws_name

        # ping settings
        self.ping_interval = ping_interval
        self.ping_timeout = ping_timeout
        self.retry_count = retries

        # callback function setting
        # self.callback_function = callback_function

        # connection timeout interval
        self.conn_timeout = conn_timeout

        # to save the list of subcriptions and the function for each subcription
        # setup the directory as follow:
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
        # websocket_base.enableTrace(traceable=log_or_not, handler=logger, level='INFO')

    def _connect(self, url):
        """
        # connect WebSocketApp to the API endpoint

        # method: _connect()
            # WebSocket tries to connect to the Endpoint, with the given endpoint
        """
        # if there is no retries attribute set to True, then no need to try, but we will anyway
        infinite_reconnect: bool = False
        if self.retries:
            infinite_reconnect = True

        # will make the WebSocketApp and will try to connect to the host
        self.ws = websocket.WebSocketApp(
            url= url,
            on_message=self.__on_message,
            on_open=self.__on_open,
            on_close=self.__on_close,
            on_error=self.__on_error
        )
        
        # thread for connection
        self.wst = threading.Thread(
            target = lambda: self.ws.run_forever(
                ping_interval = 30,
            )
        )
        self.wst.daemon = True # set this as the background program where it tries to connect
        self.wst.start() # start the thread for making a connection

        # thread for ping
        self.wsp = threading.Thread(
            target = lambda: self._ping_loop(
                ping_interval=20,
            )
        )
        self.wsp.daemon = True # set as the background thread
        self.wsp.start() # start the thread for ping

        # wait until the websocket is connected to the endpoint
        while (infinite_reconnect or self.conn_timeout) and not self._is_connected():
            if not infinite_reconnect:
                self.conn_timeout -= 1
            
            time.sleep(1)

        # if timeout occurred
        if (not self.conn_timeout):
            # connection timeout
            # retry connection is set to False
            logger.info("connection timeout for the WebSocket")
            return

        # log the connection result
        logger.info(f"WebSocket has been connected to {url}")

        # if api_key and secret_key are given, login to the WebSocketApi
        if self.api_key and self.secret_key:
            time.sleep(0.5)
            self._authenticate()

        return
    
    def _authenticate(self):
        """
        # method: _authenticate
        # login to the endpoint for private endpoint
        """
        # create the timestamp
        timestamp: str = str(int(time.time() * 1000))
        # basic signature
        _signature: str = self.api_key + timestamp

        # hmac using sha256
        signature = hmac.new(
            self.secret_key.encode("utf-8"), # encoded secret key
            _signature.encode("utf-8"), # encoded _signature
            hashlib.sha256
        ).hexdigest()

        # make the parameter dictionary into json string
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
        self.ws.send(header) # send the header to the endpoint
        logger.info("login request has been sent!") # log the request
        return

    def _are_connections_connected(
        self,
        connections: list
    ):
        # if there is connection which is not active, return False
        for connection in connections:
            if not connection.is_connected():
                return False
        
        return True

    def _set_callback(
            self,
            topic: str,
            callback_function
    ):
        """
        # method: _set_callback
            # set the callback function for the specific topic and save it into the directory in the class
            # for response handling
        """
        self.callback_dictionary[topic] = callback_function
        return

    # get the callback function according to the topic
    def _get_callback(
        self,
        topic
    ):
        """
        # method: _get_callback
            # get the callback function for the specific topic from the callback_directory in the class
        """
        return self.callback_dictionary.get(topic)
    
    def _is_connected(self):
        '''
        # method: _is_connected()
            # check if the socket is connected to the endpoint or not
        '''
        try:
            if self.ws.sock or not self.ws.sock.is_connected:
                return True
            else:
                return False
        except AttributeError: # exception handling, if there is any error occurred just return False
            return False

    # def _generate_signature(self):
    #     """
    #     # make a signature for future private websocket API
    #     # Do we need this?
    #     """
    #     timestamp = str(int(time.time() * 1000))
    #     _query_str = self.api_key + timestamp
    #     signature = hmac.new(
    #         self.secret_key.encode("utf-8"),
    #         _query_str.encode("utf-8"),
    #         hashlib.sha256
    #         ).hexdigest()
    
    #     return signature
    
    def __on_message(
        self,
        wsa,
        message
    ):
        """
        # Parsing the message from the server
        """
        # parsing the message into the json
        response = json.loads(message)

        # now response is parsed as a dictionary so that we can do something with it.
        return self.callback_function(response)

    def __on_error(
        self,
        wsa,
        exception
    ):
        """
        # when there is an error
        # Exit and raise errors or attempt to reconnect
        """
        logger.error(f"Unknown Error Occurred: {exception}")
        return

    def __on_open(
        self,
        wsa
    ):
        """
        # when the websocket is open
        """
        logger.info("ws has been opened")
        return

    def __on_close(
        self,
        wsa,
        status_code,
        close_msg
    ):
        """
        # websocket close
        # logging the status code and the msg into the logger
        """
        logger.info(f"logger has been closed: status code - {status_code}, close message = {close_msg}")
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

    def exit(self):
        """
        close the websocket
        """
        self.ws.close()

        logger.info("The WebSocket Manager has been terminated - might need to restart the entire program")

        while self.ws.sock:
            continue
    

class _FutureWebSocketManager(__BasicWebSocketManager):
    def __init__(
        self,
        ws_name = "FutureWebSocketV1",
        **kwargs
    ):
        logger.debug(f"{kwargs}")
        # self.callback_function = kwargs.pop("callback_function") if kwargs.get("callback_function") else self._default_callback

        super().__init__(ws_name=ws_name, **kwargs)

        # if not callback_fuction:
        self.callback_function = self._deal_with_response

        return

    def subscribe(
        self, 
        method, 
        callback_function, 
        param: dict = {}
    ):
        query = dict(
            method = method,
            param = param
        )

        self._check_callback(query)

        while (not self._is_connected() and not self.ws):
            time.sleep(0.1)

        logger.info(f"subscription header for {method} has been sent!")

        header = json.dumps(query)
        self.ws.send(header)
        self.subscriptions.append(query)

        # set the callback function for specific topic
        # if there is no given callback function, we just put _print_normal_msg as a callback function
        self._set_callback(method.replace("sub.", ""), callback_function)

        # logger.info(f"new sub has been established: {self.subscriptions}")

        return
    
    def _deal_with_response(self, msg):
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
        
        def is_error_msg():
            if msg.get("channel", "") == "rs.error":
                return True
            return False
        
        if is_auth_response():
            self._deal_with_auth_msg(msg=msg)
        elif is_sub_response():
            self._deal_with_sub_msg(msg=msg)
        elif is_error_msg():
            logger.info(f"The error has been received from the host: {msg}")
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

    def _deal_with_sub_msg(
        self,
        msg
    ):
        topic = msg.get("channel")

        if ((msg.get("channel", "").startswith("rs.") or
            msg.get("channel", "").startswith("push.")) 
            and msg.get("channel", "") != "rs.error"):
            logger.info(f"Subcription to {topic} has been establisehd")

        else:
            logger.info(f"")


        if msg.get("channel", "") != "rs.error":
            logger.info(f"Subscription to {topic} has been established")
        elif msg.get("channel", "") == "rs.error":
            logger.debug(f"Subscription to {topic} has failed to establish")
        return

    def _deal_with_normal_msg(
        self,
        msg
    ):
        topic = msg.get("channel").replace("push.", "").replace("sub.", "")

        callback_function = self._get_callback(topic)

        callback_function(msg)

        return
    
    def _check_callback(
        self,
        topics
    ):
        for topic in topics:
            if topic in self.callback_dictionary:
                logger.info(f"{topic} is already subscribed")
                raise Exception
            

class _FutureWebSocket(_FutureWebSocketManager):
    def __init__(
        self,
        ws_name: str = "FutureMarketWebSocketV1",
        **kwargs
    ):
        self.ws_name = ws_name
        self.endpoint = "wss://contract.mexc.com/edge"

        self.active_connections = []

        super().__init__(**kwargs)

        self.private_topics = [
            "personal.order",
            "personal.asset",
            "personal.position",
            "personal.risk.limit",
            "personal.adl.level",
            "personal.position.mode"
        ]

        # initialize the WebSocket for Future End-point
        self.ws = _FutureWebSocketManager(
                self.ws_name,
                api_key = self.api_key,
                secret_key = self.secret_key
            )
        # connect the WebSocket to the API
        self.ws._connect(self.endpoint)

        return
    
    def is_connected(self):
        return self._are_connections_connected(self.active_connections)

    def _method_subscribe(self, method, callback, param: dict = {}):
        if not self.ws:
            self.ws = _FutureWebSocketManager(
                self.ws_name,
                api_key = self.api_key,
                secret_key = self.secret_key
            )

            self.ws._connect(url=self.endpoint)

        self.ws.subscribe(method=method, callback_function= callback, param=param)
        return