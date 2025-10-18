# Built-in Library
import sys
from abc import ABC, abstractmethod
from typing import Optional, Callable
import time
import websocket
import json
import threading
import hmac
import hashlib

# Get the logger
from logger.set_logger import operation_logger


class BasicWebSocketManager(ABC):
    '''
    # Static Method
    '''
    @staticmethod
    def generate_timestamp() -> int:
        return int(time.time() * 1000)

    '''
    # Class Method
    '''
    def __init__(
        self: "BasicWebSocketManager",
        api_key: str | None = None,
        secret_key: str | None = None,
        endpoint: str | None = None,
        ws_name: str = "BaseWebSocketManager",
        ping_interval: int = 5,  # Second
        connection_interval: int = 10,  # ?
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

            self.endpoint: str = endpoint

            # Set API key and Secret Key
            self.api_key = api_key
            self.secret_key = secret_key

            # ping settings
            self.ping_interval: int = ping_interval
            self.ping_timeout: int = ping_timeout

            # default callback
            self.callback_function: Callable | None = default_callback

            # Connection and timeout interval
            self.conn_interval: int = connection_interval
            self.conn_timeout: int = conn_timeout

            # to save the list of subcriptions and the function for each subcription
            # setup the directory as follow:
            """
            {
                <subscription-type>: <callback-function>
            }
            """
            self.callback_dictionary: dict = {}

            # record the subscription made
            # will store the query for ethe specific topic. -> self.ws.send(json.dumps(query))
            self.subscriptions = list()

            # has the Websocket been authroized by the API? -> false initially
            # if api_key and secret_key are given, then it should be authentication needed.
            self.auth = False if (self.api_key is None or self.secret_key is None) else True
        except Exception as e:
            operation_logger.error(f"{__name__} - func __init__(): {e}")

        return None

    def _connect(
        self: "BasicWebSocketManager",
    ) -> None:
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
        self._closing = False
        self.ws: websocket.WebSocketApp = websocket.WebSocketApp(
            url = self.endpoint,
            on_message = self.__on_message,
            on_open = self.__on_open,
            on_close = self.__on_close,
            on_error = self.__on_error,  # TODO: retry
        )

        time.sleep(1)

        # thread for connection
        self.wst: threading.Thread = threading.Thread(
            name = "Connection thread",
            target = lambda: self.ws.run_forever(
                # ping_interval = self.conn_interval,  # default 10 sec
                ping_interval = 0,  # since we do have the explicit ping thread.
            ),
            daemon = True,  # set this as the background program where it tries to connect
        )
        self.wst.start()  # start the thread for making a connection

        time.sleep(1)

        # thread for ping
        self.wsp = threading.Thread(
            name = "Ping thread",
            target = lambda: self._ping_loop(
                ping_interval = self.ping_interval,  # default 10 sec
            ),
            daemon = True,  # set this as the background program where it sends the ping to the host every <self.ping_interval> second, default is 10 seconds by the Class Setting.
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

    def _authenticate(self: "BasicWebSocketManager",) -> None:
        """
        func authenticate():
            - authenticate the WebSocket connection to the API endpoint
            - login to the endpoint for private endpoint

        param self:
            - self: the instance of the class

        return None
        """
        # create the timestamp
        timestamp: str = str(BasicWebSocketManager.generate_timestamp())

        # hmac using sha256
        signature = self._generate_signature(timestamp=timestamp)

        # make the parameter dictionary into json string
        header = json.dumps(
            dict(
                subscribe = False,
                method = "login",
                param = dict(
                    apiKey = self.api_key,
                    reqTime = timestamp,
                    signature = signature,
                ),
            )
        )
        self.ws.send(header)  # send the header to the endpoint
        return None

    def _generate_signature(
        self: "BasicWebSocketManager",
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

    def _are_connections_connected(self: "BasicWebSocketManager", connections: list) -> bool:
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
        self: "BasicWebSocketManager",
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
        self: "BasicWebSocketManager",
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

    def _is_connected(
        self: "BasicWebSocketManager",
    ):
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

    def __on_error(self: "BasicWebSocketManager", wsa, exception):
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

    def __on_open(self: "BasicWebSocketManager", wsa):
        """
        # when the websocket is open
        """
        operation_logger.info(f"{__name__} - WebSocket has been opened")
        return

    def __on_close(self: "BasicWebSocketManager", wsa, status_code, close_msg):
        """
        # websocket close
        # logging the status code and the msg into the operation_logger
        """
        operation_logger.warning(
            f"{__name__} - the websocket has been closed: {status_code} - {close_msg}. {self.ws_name} will try to reconnect."
        )

        # if there is no pre-defined endpoint, then it will raise RuntimeError
        if not self.endpoint:
            operation_logger.error(
                f"{__name__} - {self.ws_name} lost connection but no previous URL recorded; manual restart required."
            )
            raise RuntimeError(f"{__name__} - {self.ws_name} lost connection but no previous URL recorded; manual restart required.")

        # try to construct the channel again.
        for attempt, delay in enumerate((0, 0.5, 1.0), start = 1):
            if delay:
                time.sleep(delay)
            try:
                operation_logger.info(
                    f"{__name__} - Attempting to reconnect ({attempt}) to {self.endpoint}"
                )
                self._connect(self.endpoint)
                operation_logger.info(
                    f"{__name__} - {self.ws_name} reconnected successfully."
                )
                break
            except Exception as e:
                operation_logger.error(
                    f"{__name__} - {self.ws_name} reconnect attempt {attempt} failed: {str(e)}"
                )
        else:
            operation_logger.critical(
                f"{__name__} - {self.ws_name} could not re-establish the websocket connection."
            )
            raise RuntimeError(f"{__name__} - {self.ws_name} could not re-establish the websocket connection; manual restart is needed.")

        self._resubscribe()
        return

    def _resubscribe(self: "BasicWebSocketManager") -> None:
        """
        Resend cached subscriptions after the connection has been re-established.
        """
        if not self.subscriptions:
            raise RuntimeError(f"{__name__} - {self.ws_name} could not re-establish the websocket connection; manual restart is needed.")

        for query in self.subscriptions:
            try:
                header = json.dumps(query)
                self.ws.send(header)
                operation_logger.info(
                    f"{__name__} - {self.ws_name} resubscribed with header: {header}"
                )
            except Exception as e:
                operation_logger.critical(
                    f"{__name__} - {self.ws_name} could not resubscribe the query: {query} with the following error msg: {str(e)}"
                )
        return

    def _ping_loop(
        self: "BasicWebSocketManager",
        ping_interval: int,  # Second
        ping_payload: str = '{"method":"ping"}',
    ) -> None:
        """
        # method: _ping_loop
        # for the ping thread of WebSocketApp
        """
        curr_timestamp: int = 0
        while True:
            if (BasicWebSocketManager.generate_timestamp() - curr_timestamp > (ping_interval * 1_000)):
                self.ws.send(ping_payload)
                curr_timestamp = BasicWebSocketManager.generate_timestamp()
        return None

    def _reset(
        self: "BasicWebSocketManager",
    ):
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

    def exit(
        self: "BasicWebSocketManager",
    ):
        """
        close the websocket
        """
        self.ws.close()

        operation_logger.warning(
            "The WebSocket Manager has been terminated - You might need to restart the entire program"
        )

        while self.ws.sock:
            continue
