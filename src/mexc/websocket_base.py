# Built-in Library
import sys

import threading
from typing import Optional, Callable
import time
import hashlib
import hmac
import json
import websocket

# get the Logger
from logger.set_logger import operation_logger


class __BasicWebSocketManager:
    def __init__(
        self,
        api_key: str | None = None,
        secret_key: str | None = None,
        ws_name: str = "BaseWebSocketManager",
        ping_interval: int = 5,
        connection_interval: int = 10,
        ping_timeout: int = 10,
        conn_timeout: int = 30,
        default_callback: Callable | None = None,
    ) -> None:
        """
        func __init__():
            - instantiate the WebSocketManager class

        params:
            - callback_function: function, general callback_function for entire response from the endpoint
            - endpoint: MexC Websocket API endpoint
            - ws_name: WebSocketName
            - api_key: api_key for API usage
            - secret_key: secret_key for API usage
            - ping_interval: WebSocketConnection ping interval, default 20 seconds
            - ping_timeout: if there is no response for ping resposne for 10 seconds, close the websocket with the endpoint
            - retries: retries for WebSocket Connection for error
                # TODO: need to implement the automatic reconnect and restart (by default)
                # TODO: error handling not yet implemented
            - restart_on_error: retries on error
            - conn_timeout: WebSocket will try to connect to the endpoint for the timeout interval
            - login_required: if the websocket needs to authenticate to the system or not

        return None
        """
        try:
            # get the websocket name
            self.ws_name = ws_name

            # Set API key
            # do we need to login for this WebSocketManager?
            self.api_key = api_key
            self.secret_key = secret_key

            # ping settings
            self.ping_interval: int = ping_interval
            self.ping_timeout: int = ping_timeout

            # default callback
            self.callback_function: Callable | None = default_callback

            # Connection interval
            self.conn_interval: int = connection_interval

            # connection timeout interval
            self.conn_timeout: int = conn_timeout

            # to save the list of subcriptions and the function for each subcription
            self.callback_dictionary: dict = {}

            # setup the directory as follow:
            """
            {
                <subscription-type>: <callback-function>
            }
            """

            # record the subscription made
            self.subscriptions = []

            # has the Websocket been authroized by the API? -> false initially
            # if api_key and secret_key are given, then it should be authentication needed.
            self.auth = (
                False if (self.api_key is None or self.secret_key is None) else True
            )
        except Exception as e:
            operation_logger.error(f"{__name__} - func __init__(): {e}")
            raise e

        return None

    def _connect(self, url) -> None:
        """
        func connect():
            - connect WebSocketApp to the API endpoint
            - WebSocket tries to connect to the given Endpoint.

        param: url
            - the endpoint url to establish the connection.
            - will keep the session witht he API broker

        return None
        """
        # if there is no retries attribute set to True, then no need to try, but we will anyway
        infinite_reconnect: bool = True

        # will make the WebSocketApp and will try to connect to the host
        self.ws: websocket.WebSocketApp = websocket.WebSocketApp(
            url = url,
            on_message = self.__on_message,
            on_open = self.__on_open,
            on_close = self.__on_close,  # TODO:
            on_error = self.__on_error,  # TODO:
        )

        # thread for connection
        self.wst: threading.Thread = threading.Thread(
            name = "Connection thread",
            target = lambda: self.ws.run_forever(
                ping_interval = self.conn_interval,  # default 10 sec
            ),
            daemon = True,  # set this as the background program where it tries to connect
        )
        self.wst.start()  # start the thread for making a connection

        # thread for ping
        self.wsp: threading.Thread = threading.Thread(
            name = "Ping thread",
            target = lambda: self._ping_loop(
                ping_interval = self.ping_interval,  # default 10 sec
            ),
            daemon = True,  # set this as the background program where it sends the ping to the host every 10 sec.
        )
        self.wsp.start()  # start the thread for ping

        # wait until the websocket is connected to the host.
        while (infinite_reconnect or self.conn_timeout) and not self._is_connected():
            if not infinite_reconnect:
                self.conn_timeout -= 1

            time.sleep(1)

            # if timeout occurred
            if not self.conn_timeout:
                operation_logger.warning(
                    f"{__name__}: connection to the host time out. You may restart the entire program."
                )
                # connection timeout
                # retry connection is set to False
                return

        operation_logger.info(
            f"{__name__} - func _connect: Websocket Connection to the host has been established."
        )
        # if api_key and secret_key are given, login to the WebSocketApi
        if self.auth:
            time.sleep(1)
            self._authenticate()

        return None

    def _authenticate(self) -> None:
        """
        func authenticate():
            - authenticate the WebSocket connection to the API endpoint
            - login to the endpoint for private endpoint

        param self:
            - self: the instance of the class

        return None
        """
        # create the timestamp
        timestamp: str = str(int(time.time() * 1000))

        # hmac using sha256
        signature = self._generate_signature(timestamp=timestamp)

        # make the parameter dictionary into json string
        header = json.dumps(
            dict(
                subscribe=False,
                method="login",
                param=dict(
                    apiKey=self.api_key,
                    reqTime=timestamp,
                    signature=signature,
                ),
            )
        )
        self.ws.send(header)  # send the header to the endpoint
        return None

    def _generate_signature(
        self,
        timestamp: str | None = None,
    ) -> str | None:
        """
        func generate_signature():
            - generate the signature for the private API endpoint
        """
        if not timestamp:
            timestamp = str(int(time.time() * 1000))

        if (self.api_key and self.secret_key):
            _query_str = self.api_key + timestamp

            return hmac.new(
                self.secret_key.encode("utf-8"),
                _query_str.encode("utf-8"),
                hashlib.sha256,
            ).hexdigest()

        return

    def _are_connections_connected(self, connections: list) -> bool:
        """
        func _are_connections_connected():
            - check if the connection is connected to the endpoint or not

        param: connections
            - check the connection status of the connections

        return bool
            - if there is connection which is not connected, return False
            - if all of the connections are connected, return True
        """
        for connection in connections:
            if not connection.is_connected():
                return False
        return True

    def _set_callback(
        self,
        topic: str,
        callback_function: Callable | None = None,
    ) -> None:
        """
        func _set_callback():
            - It sets the callback function for the specific topic and save it into the directory in the class
            - For response handling

        param topic
            - the topic for the callback function
            - e.g., "ticker", "order", "trade", etc.
        param callback
            - function to be called when there is a new data.

        return
        """
        self.callback_dictionary[topic] = callback_function
        return None

    # get the callback function according to the topic
    def _get_callback(
        self,
        topic: str,
    ) -> Callable | None:
        """
        func _get_callback():
            - get the callback function for the specific topic from the callback_directory in the class
            - if there is no callback function, return None

        param topic:
            - key for the dictionary where the callback function is saved.
            - e.g., "ticker", "order", "trade", etc.

        return Callable or None
            - if there is no such topic stored in the dictionary, return None
            - if there is such topic, return the callback function for that topic
        """
        return self.callback_dictionary.get(topic)

    def _is_connected(self):
        """
        # method: _is_connected()
            # check if the socket is connected to the endpoint or not
        """
        try:
            if self.ws.sock or not self.ws.sock.is_connected:
                return True
            else:
                return False
        except (
            AttributeError
        ):  # exception handling, if there is any error occurred just return False
            return False

    """
    ######################################################################################################################
    #                                Websocket Message Handling Function                                                 #
    ######################################################################################################################
    """

    def __on_message(self, wsa, message):
        """
        # Parsing the message from the server
        """
        # parsing the message into the json
        response = json.loads(message)

        # now response is parsed as a dictionary so that we can do something with it.
        if (self.callback_function):
            return self.callback_function(response)

        return

    def __on_error(self, wsa, exception):
        """
        # when there is an error
            # Exit and raise errors OR
            # attempt to reconnect
        """
        operation_logger.error(
            f"{__name__} - WebSocket API: Unknown Error Occurred: {exception}"
        )
        sys.exit()
        return

    def __on_open(self, wsa):
        """
        # when the websocket is open
        """
        operation_logger.info(f"{__name__} - WebSocket has been opened")
        return

    def __on_close(self, wsa, status_code, close_msg):
        """
        # websocket close
        # logging the status code and the msg into the operation_logger
        """
        operation_logger.warning(
            f"{__name__} - the websocket has been closed. Need to reconnect"
        )
        # TODO: need to implement the function for reconnect.
        sys.exit()
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
        # clear the list of subscritpions and the callback function
        self.subscriptions.clear()
        self.callback_dictionary.clear()
        self.auth = False
        operation_logger.info(f"{__name__} - WebSocket {self.ws_name} has been reset.")
        return

    def exit(self):
        """
        close the websocket
        """
        self.ws.close()

        operation_logger.warning(
            "The WebSocket Manager has been terminated - You might need to restart the entire program"
        )

        while self.ws.sock:
            continue


# MexC Future Websocket Manager
class _FutureWebSocketManager(__BasicWebSocketManager):
    def __init__(self, ws_name = "FutureWebSocketV1", **kwargs):
        super().__init__(ws_name = ws_name, **kwargs)

        # if there is no default function.
        self.callback_function = self._deal_with_response

        return

    def subscribe(
        self,
        method: Optional[str] = "sub.ticker",
        callback_function=None,
        param: dict = {},
    ):
        query = dict(method=method, param=param)

        self._check_callback(query)

        while not self._is_connected() and not self.ws:
            time.sleep(0.1)

        # make dict into json, so that it can be on the header of the HTTP Socket.
        header = json.dumps(query)
        self.ws.send(header)
        self.subscriptions.append(query)

        # set the callback function for specific topic
        # if there is no given callback function, we just put _print_normal_msg as a callback function
        if method:  # just in case
            self._set_callback(method.replace("sub.", ""), callback_function)

        # operation_logger.info(f"new sub has been established: {self.subscriptions}")

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
            if msg.get("channel") == "rs.login":
                return True
            return False

        def is_sub_response():
            if str(msg.get("channel", "")).startswith("rs.sub."):
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
            operation_logger.info(
                f"{__name__} - func _deal_with_response(): The error has been received from the host: {msg}"
            )
        elif is_pong_msg():
            pass
        else:
            self._deal_with_normal_msg(msg=msg)

        return

    def _deal_with_auth_msg(self, msg):
        """
        Determine if the login has been successful.
        # notify the result to the user by operation_logger.
        """
        if msg.get("data") == "success":  # login success
            operation_logger.info(
                f"Authorization for {self.ws_name} has been successful."
            )
            self.auth = True
        else:  # login fail
            operation_logger.debug(
                f"Authoriztion for {self.ws_name} has not been successful."
                f"Please check your keys!"
            )
        return

    def _deal_with_sub_msg(self, msg):
        # TODO: refactor websocket base class with try-catch block for better error handling.
        topic = msg.get("channel")

        if (
            msg.get("channel", "").startswith("rs.")
            or msg.get("channel", "").startswith("push.")
        ) and msg.get("channel", "") != "rs.error":
            operation_logger.info(
                f"{__name__} - func _dealwith_sub_msg(): Subcription to {topic} has been establisehd"
            )
        else:
            operation_logger.info(
                f"{__name__} - func _dealwith_sub_msg(): Subscription to {topic} has failed to establish."
            )

        return

    def _deal_with_normal_msg(self, msg):
        topic = msg.get("channel").replace("push.", "").replace("sub.", "")

        callback_function = self._get_callback(topic)

        if (callback_function):  # if callback_function is not None.
            callback_function(msg)

        return

    def _check_callback(self, topics):
        for topic in topics:
            if topic in self.callback_dictionary:
                operation_logger.info(
                    f"{__name__} - func _deal_with_normal_msg(): {topic} is already subscribed"
                )
                raise Exception


class _FutureWebSocket(_FutureWebSocketManager):
    def __init__(self, ws_name: str = "FutureMarketWebSocketV1", **kwargs):
        """ """
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
            "personal.position.mode",
        ]

        # initialize the WebSocket for Future End-point
        self.__initialize_websocket()

        return

    def __initialize_websocket(
        self,
    ):
        """ """
        try:
            self.ws = _FutureWebSocketManager(
                self.ws_name,
                api_key = self.api_key,
                secret_key = self.secret_key,
            )
            self.ws._connect(self.endpoint)
        except Exception as e:
            operation_logger.error(f"{__name__} - func initialize_websocket(): {e}")
            print(f"{__name__} - func initialize_websocket(): {e}")
            return

        return

    def is_connected(self):
        """ """
        return self._are_connections_connected(self.active_connections)

    def _method_subscribe(self, method, callback, param: dict = {}):
        """ """
        if not self.ws:
            # if there is no websocket object that has been established.
            self.__initialize_websocket()

        self.ws.subscribe(
            method = method,
            callback_function = callback,
            param = param,
        )
        return
