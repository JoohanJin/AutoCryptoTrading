"""
Future Trade API
Documentation: https://mexcdevelop.github.io/apidocs/contract_v1_en
"""

from typing import Optional, Literal, Union, Callable

from mexc.base_sdk import FutureBase
from mexc.websocket_base import _FutureWebSocket
from logger.set_logger import operation_logger


# no need to authenticate
class FutureMarket(FutureBase):
    """
    ######################################################################################################################
    #                                                    Public Endpoint                                                 #
    ######################################################################################################################
    """

    def ping(
        self: "FutureMarket",
    ) -> dict:
        """
        - func ping():
            - Get The Server Time
            - Testing the connectivity of the server

        - Parameters: None

        - Rate Limit:
            - 20 times / 2 seconds

        - Documentation:
            - https://mexcdevelop.github.io/apidocs/contract_v1_en/?python#get-the-server-time
        """
        url: str = "api/v1/contract/ping"

        return self.call(
            method = "GET",
            url = url,
        )

    def server_time(
        self: "FutureMarket",
    ) -> dict:
        """
        - func server_time():
            - Get The Server Time from the mexc api endpoint.
        """
        url: str = "api/v1/contract/ping"

        return self.call(
            method = "GET",
            url = url,
        )

    def detail(
        self: "FutureMarket",
        symbol: Optional[str] = "BTC_USDT",
    ) -> dict:
        """
        - func detail():
            - Get the contract information

        - param:
            - symbol: Optional[str], the name of the contract
            - the default value is "BTC_USDT"
                - because I am only trading the BTC_USDT contract.

        - Rate Limit: 1 times / 5 seconds

        - Documentation:
            - https://mexcdevelop.github.io/apidocs/contract_v1_en/?python#get-the-contract-information
        """
        url: str = "api/v1/contract/detail"

        return self.call(
            method = "GET",
            url = url,
            params = dict(symbol = symbol),
        )

    def support_currencies(
        self: "FutureMarket",
    ) -> dict:
        """
        - func support_currencies():
            - Get the transferable currencies
            - The returned "data" field contains a list of string with each string represents a supported currencies

        - params
            - None

        - Rate Limit: 20 times / 2 seconds

        - Documentation:
            - https://mexcdevelop.github.io/apidocs/contract_v1_en/?python#get-the-transferable-currencies
        """
        url: str = "/api/v1/contract/support_currencies"

        return self.call(
            method="GET",
            url=url,
        )

    def depth(
        self: "FutureMarket",
        symbol: str = "BTC_USDT",
        limit: Optional[int] = None,
    ) -> dict:
        """
        - func depth():
            - Get the contract's depth information

        - params:
            - symbol: str, the name of the contract
            - limit: Optional[int], tier

        - Rate Limit:
            - 20 times / 2 seconds

        - Documentation:
            - https://mexcdevelop.github.io/apidocs/contract_v1_en/?python#get-the-contract-s-depth-information
        """
        url: str = f"api/v1/contract/depth/{symbol}"

        params: dict[str, int] = dict()
        if limit is not None:
            params["limit"] = limit

        return self.call(
            method = "GET",
            url = url,
            params = params,
        )

    def depth_commits(
        self: "FutureMarket",
        symbol: str = "BTC_USDT",
        limit: int = 5,
    ) -> dict:
        """
        - func depth_commits():
            - Get a snapshot of the lastest N depth information of the contract

        - params:
            - symbol: str, the name of the contract
            - limit: int, count

        - Rate Limit:
            - 20 times / 2 seconds

        - Documentation:
            - https://mexcdevelop.github.io/apidocs/contract_v1_en/?python#get-a-snapshot-of-the-latest-n-depth-information-of-the-contract
        """
        url: str = f"api/v1/contract/depth_commits/{symbol}/{limit}"

        params: dict[str, int] = dict()
        if limit is not None:
            params["limit"] = limit

        return self.call(
            method = "GET",
            url = url,
            params = params,
        )

    def index_price(
        self: "FutureMarket",
        symbol: str = "BTC_USDT",
    ) -> dict:
        """
        - func index_price()
            - Get contract index price

        - params:
            - symbol: str, the name of the contract

        - Rate Limit:
            - 20 times / 2 seconds

        - Documentation:
            - https://mexcdevelop.github.io/apidocs/contract_v1_en/?python#get-contract-index-price
        """
        url: str = f"api/v1/contract/index_price/{symbol}"

        return self.call(
            method = "GET",
            url = url,
        )

    def fair_price(
        self: "FutureMarket",
        symbol: str = "BTC_USDT",
    ) -> dict:
        """
        - func fair_price():
            - Get contract fair price

        - params:
            - symbol: str, the name of the contract

        - Rate Limit:
            - 20 times / 2 seconds

        - Documentation:
            - https://mexcdevelop.github.io/apidocs/contract_v1_en/?python#get-contract-fair-price
        """
        url: str = f"api/v1/contract/fair_price/{symbol}"
        return self.call(
            method = "GET",
            url = url,
        )

    def funding_rate(
        self: "FutureMarket",
        symbol: str = "BTC_USDT",
    ) -> dict:
        """
        - func funding_rate():
            - get contract funcding rate

        - params:
            - symbol: str, the name of the contract

        - Rate Limit:
            - 20 times / 2 seconds
        """
        url: str = f"api/v1/contract/funding_rate/{symbol}"
        return self.call(
            method = "GET",
            url = url,
        )

    def kline(
        self,
        interval: Optional[
            Union[
                Literal["Min1"],
                Literal["Min5"],
                Literal["Min15"],
                Literal["Min30"],
                Literal["Min60"],
                Literal["Hour4"],
                Literal["Hour8"],
                Literal["Day1"],
                Literal["Week1"],
                Literal["Month1"],
            ]
        ] = "Min1",  # default value is one minute.
        symbol: str = "BTC_USDT",
        start_time: int | None = None,
        end_time: int | None = None,
    ):
        """
        - func kline():
            - get the candle stick, or k-line data, for the price of the given cryptocurrency

        - params:
            - symbol: str, the name of the contract
            - interval: Optional[str], interval for the k-line data
                - must be one of the followings
                    - "Min1", "Min5", "Min15", "Min30", "Min60", "Hour4", "Hour8", "Day1", "Week1", "Month1"
                - default value is "Min1"
            - start: Optional[long], The start time of the k-line data in Unix timestamp format
            - end: Optional[long], The end time of the k-line data in Unix timestamp format

        - rate limit:
            - 20 times / 2 seconds

        - Warning:
            - the maximum number of data received in one request is 2000
                - multiple requests are needed to get the fine and smooth data for a long period of time
            - if only the start time is provided, then query the data from the start time and the current system time
            - if only the end time is provided, the 2000 pieces of data closest to the end time are returned
            - if neither start time nor end time is provided, the 2000 pieces of data closest to the current time in the system are queried.
        """
        url: str = f"api/v1/contract/kline/{symbol}"

        params: dict[str, int | str] = dict(
            symbol = symbol,
            interval = interval,
        )

        if start_time is not None:
            params["startTime"] = start_time
        if end_time is not None:
            params["endTime"] = end_time

        return self.call(
            method = "GET",
            url = url,
            params = params,
        )

    def kline_index_price(
        self,
        interval: Optional[
            Union[
                Literal["Min1"],
                Literal["Min5"],
                Literal["Min15"],
                Literal["Min30"],
                Literal["Min60"],
                Literal["Hour4"],
                Literal["Hour8"],
                Literal["Day1"],
                Literal["Week1"],
                Literal["Month1"],
            ]
        ] = "Min1",
        symbol: str = "BTC_USDT",
        start_time: int | None = None,
        end_time: int | None = None,
    ):
        """
        - func kline_index_price():
            - get the candle stick data for the index price of the given cryptocurrency

        - params:
            - symbol: str, the name of the contract
            - interval: Optional[str], interval for the k-line data
                - must be one of the followings
                - "Min1", "Min5", "Min15", "Min30", "Min60", "Hour4", "Hour8", "Day1", "Week1", "Month1"
                - default value is "Min1"
            - start: Optional[long], The start time of the k-line data in Unix timestamp format
            - end: Optional[long], The end time of the k-line data in Unix timestamp format

        - rate limit:
            - 20 times / 2 seconds
        """
        url: str = f"api/v1/contract/kline/index_price/{symbol}"

        params: dict[str, int | str] = dict(
            symbol=symbol,
            interval=interval,
        )

        if start_time is not None:
            params["startTime"] = start_time
        if end_time is not None:
            params["endTime"] = end_time

        return self.call(
            method = "GET",
            url = url,
            params = params,
        )

    def kline_fair_price(
        self,
        interval: Optional[
            Union[
                Literal["Min1"],
                Literal["Min5"],
                Literal["Min15"],
                Literal["Min30"],
                Literal["Min60"],
                Literal["Hour4"],
                Literal["Hour8"],
                Literal["Day1"],
                Literal["Week1"],
                Literal["Month1"],
            ]
        ] = "Min1",
        symbol: str = "BTC_USDT",
        start_time: int | None = None,
        end_time: int | None = None,
    ):
        """
        - func kline_fair_price():
            - get the candle stick data for the index price of the given cryptocurrency

        - params:
            - symbol: str, the name of the contract
            - interval: Optional[str], interval for the k-line data
                - must be one of the followings
                "Min1", "Min5", "Min15", "Min30", "Min60", "Hour4", "Hour8", "Day1", "Week1", "Month1"
                default value is "Min1"
            - start: Optional[long], the start time of the k-line data in Unix timestamp format
            - end: Optional[long], the end time of the k-line data in Unix timestamp format

        - rate limit:
            - 20 times / 2 seconds
        """
        url: str = f"api/v1/contract/kline/fair_price/{symbol}"

        params: dict[str | int] = dict(
            symbol = symbol,
            interval = interval,
        )

        if start_time is not None:
            params["startTime"] = start_time
        if end_time is not None:
            params["endTime"] = end_time

        return self.call(
            method = "GET",
            url = url,
            params = params,
        )

    def deals(
        self: "FutureMarket",
        limit: Optional[int] = 100,
        symbol: str = "BTC_USDT",
    ) -> dict:
        """
        - func deals():
            - get contract transaction data

        - params:
            - symbol: str, the name of the contract
            - limit: Optional[int], consequence set quantity, maximum is 100, default 100 without setting

        - rate limit:
            - 20 times / 2 seconds
        """
        url: str = f"api/v1/contract/deals/{symbol}"

        params: dict[str, int] = dict(
            symbol = symbol,
            limit = limit,
        )

        return self.call(
            method = "GET",
            url = url,
            params = params,
        )

    def ticker(
        self: "FutureMarket",
        symbol: Optional[str] = "BTC_USDT",
    ):
        """
        - func ticker():
            - get contract trend data

        - param:
            - symbol: Optional[str], the name of the contract

        - rate limit:
            - 20 times / 2 seconds
        """
        url: str = "api/v1/contract/ticker"

        params: dict[str, str] = dict(
            symbol = symbol,
        )

        return self.call(
            method = "GET",
            url = url,
            params = params,
        )

    def risk_reverse(
        self: "FutureMarket",
    ):
        """
        - func risk_reverse():
            - get all contract risk fund balance

        - params:
            - None

        - rate limit:
            - 20 times / 2 seconds
        """
        url: str = "api/v1/contract/risk_reverse"
        return self.call(
            method = "GET",
            url = url,
        )

    def risk_reverse_history(
        self: "FutureMarket",
        symbol: str = "BTC_USDT",
        page_num: int = 1,
        page_size: int = 100,
    ) -> dict:
        """
        - func risk_reverse_history():
            - get contract risk fund balance history

        - params:
            - symbol: str, the name of the contract
            - page number: int, current page number, default is 1
            - page size: int, the page size, default 20, maximum 100

        - rate limit:
            - 20 times / 2 seconds
        """
        url: str = "api/v1/contract/risk_reverse/history"

        params: dict[str, str | int] = dict(
            symbol = symbol,
            page_num = page_num,
            page_size = page_size,
        )

        return self.call(
            method = "GET",
            url = url,
            params = params,
        )

    def funding_rate_history(
        self,
        symbol: str = "BTC_USDT",
        page_num: int = 1,
        page_size: int = 100,
    ) -> dict:
        """
        - func funding_rate_history():
            - get contract funcding rate history

        - params:
            - symbol: str, the name of the contract
            - page_num: int, current page number, default is 1
            - page_size: int, the page size, default 20, maximum 100

        - rate limit:
            - 20 times / 2 seconds
        """
        url: str = "api/v1/contract/funding_rate/history"

        params: dict[int, str | int] = dict(
            symbol = symbol,
            page_num = page_num,
            page_size = page_size,
        )

        return self.call(
            url = url,
            method = "GET",
            params = params,
        )

    """
    ######################################################################################################################
    #                                                   Private Endpoint                                                 #
    ######################################################################################################################
    """

    def assets(self: "FutureMarket",):
        """
        - method: assets()
            - Getting all information of user's asset
            - Required Permissions: Trade reading permission

        - Rate limit: 20 times / 2 seconds

        - Request parameters
            - None
        """
        return self.call(
            method = "GET",
            url = "api/v1/private/account/assets",
        )

    def asset(
        self: "FutureMarket",
        currency: str = "USDT",
    ):
        """
        - method: assets(currency: str)
            - get the user's single currency asset information
            - Required Permissions: Account reading permission

        - Rate Limit: 20 times / 2 seconds

        - Request Parameters
            - currency: str, mandatory
        """
        return self.call("GET", f"api/v1/private/account/asset/{currency}")

    def history_position(
        self: "FutureMarket",
        symbol: str = "BTC_USDT",
        type: int = None,
        page_num: int | None = 1,
        page_size: int | None = 100,
    ):
        """
        - method: history_position()
            - get the user's history position information
            - trade reading permission

        - Rate Limit: 20 times / 2 seconds

        - Request Parameters
            - symbol: str, optional, the name of the contract
            - type: int, optional, position type i.e. 1 - long, 2 - short
            - page_num: current page, default is 1
            - page_size
        """
        params: dict[str, str | int] = dict(
            symbol = symbol,
            type = type,
            page_num = page_num,
            page_size = page_size,
        )

        return self.call(
            method = "GET",
            url = "api/v1/private/position/list/history_positions",
            params = params,
        )

    def current_position(self, symbol: str = "BTC_USDT"):
        """
        - method: current_position()
            - get the user's current holding position
            - trade reading permission

        - Rate Limit: 20 times / 2 seconds

        - request parameters:
            - symbol: str, optional, the name of the contract
        """
        params: dict[str, str | int] = dict(
            symbol = symbol,
        )

        return self.call(
            method = "GET",
            url = "api/v1/private/position/open_positions",
            params = params,
        )

    def pending_order(
        self: "FutureMarket",
        symbol: str | None = "BTC_USDT",
        page_num: int | None = 1,
        page_size: int | None = 100,
    ):
        """
        - method: pending_order
            - get the user's current pending order
            - trade reading permission

        - Rate Limit: 20 times / 2 seconds

        - request parameters
            - symbol: str, optional, the name of the contract, return all the contract parameters if there are no fill in
            - page_num: int, required,
            - page_size: int, required
        """
        url: str = "api/v1/private/order/list/open_orders"

        params: dict[str, str | int] = dict(
            symbol = symbol,
            page_num = page_num,
            page_size = page_size,
        )

        return self.call(
            method = "GET",
            url = url,
            params = params,
        )

    def risk_limit(self: "FutureMarket", symbol: str = "BTC_USDT"):
        """
        - method: risk_limit()
            - get the user's current pending order
            - trade reading permission

        - Rate Limit: 20 times / 2 seconds

        - request parameters:
            - symbol: str, optional, the name of the contract, not uploaded will return all
        """
        params: dict[str, str] = dict(
            symbol = symbol,
        )

        return self.call(
            method = "GET", url = "api/v1/private/account/risk_limit", params = params,
        )

    def fee_rate(self: "FutureMarket", symbol: str = "BTC_USDT"):
        """
        - method: fee_rate()
            - get the user's current rading fee rate
            - trade reading permission

        - Rate Limit: 20 times / 2 seconds

        - request parameters:
            - symbol: str, optional, the nmae of the contract
        """
        return self.call(
            method = "GET",
            url = "api/v1/private/account/tiered_fee_rate",
            params = dict(symbol = symbol),
        )

    def place_order(
        self: "FutureMarket",
        price: float,
        vol: float,
        side: int,  # 1 and 3
        type: int = 5,  # 5 for market, need to test 6
        openType: int = 1,  # 1 for isolatied, 2 for cross
        positionId: int = None,
        externalOid: int = None,
        stopLossPrice: float = None,
        takeProfitPrice: float = None,
        positionMode: int = None,
        reduceOnly: bool = False,
        symbol: str = "BTC_USDT",
        leverage: int = 20,
    ):
        """
        - Under-Maintanence on Broker Side
        - method: place_order()
            - USDT perpetual contract trading offers limit and market orders.
            - POST

        - Rate Limit: 20 times / 2 seconds

        - Request Parameters
            - symbol
                - str
                - Optional, BTC_USDT
                - the name of the contract
            - price
                - decimal
                - Required
                - price
            - vol
                - decimal
                - Required, 10%
                - volume
            - leverage
                - int
                - optional, 50
                - leverage, leverage is necessary on isolated margin
            - side
                - int
                - required
                - order direction
                    - 1: open long
                    - 2: close short
                    - 3: open short
                    - 4: close long
            - type
                - int
                - required
                - ordertype
                    - 1: price limited order
                    - 2: post only maker
                    - 3: transact or cancel instantly
                    - 4: transact completely or cancel completely
                    - 5: market orders
                    - 6: convert market price to current price
            - openType
                - int
                - required
                - open type
                    - 1: isolated
                    - 2: cross
            - positionId
                - long
                - optional
                - position id
                    - recommended to fill in this parameter when closing a position
            - externalOid
                - str
                - optional
                - external order ID
            - stopLossPrice
                - decimal
                - optional, default -5%
                - stop-loss price
            - takeProfitPrice
                - decimal
                - optional, default +15%
                - take-profit price
            - positionMode
                - int
                - optional
                - position mode
                    - 1: hedge
                    - 2: one-way
                    - default: user's current config
            - reduceOnly
                - bool
                - optional
                - defualt false
                    - one-way positions: if you need to only reduce positions, pass in true
                    - two-way positions: will not accept this parameter.
        """
        params: dict[str, str | int | float] = dict(
            symbol = symbol,
            price = price,
            vol = vol,
            leverage = leverage,
            side = side,
            type = type,
            openType = openType,
            positionId = positionId,
            externalOid = externalOid,
            stopLossPrice = stopLossPrice,
            takeProfitPrice = takeProfitPrice,
            positionMode = positionMode,
            reduceOnly = reduceOnly,
        )

        return self.call(
            method = "POST",
            url = "api/v1/private/order/submit",
            params = params,
        )


class FutureWebSocket(_FutureWebSocket):
    def __init__(
        ws_name: Optional[str] = None,
        api_key: Optional[str] = None,
        secret_key: Optional[str] = None,
        ping_interval: Optional[int] = 20,  # as it is recommended
        ping_timeout: Optional[int] = 10,
        conn_timeout: Optional[int] = 30,
    ) -> None:

        # pass the parameters to the FutureWebSocket
        kwargs = dict(
            api_key = api_key,
            secret_key = secret_key,
            ping_interval = ping_interval,
            ping_timeout = ping_timeout,
            conn_timeout = conn_timeout,
        )

        super().__init__(**kwargs)
        return

    """
    - Public Endpoint
        - Tickers
        - Ticker
        - Transaction
        - Depth
        - k-line
        - Funding Rate
        - Index Price
        - Fair Price
    """

    def tickers(self, callback):
        """
        - Get the latest transaction price, buy-price, sell-price and 24 transaction volume
        - of all the perpetual contracts on the platform without login.
        - Send once a second after subscribing
        """
        method = "sub.tickers"
        self._method_subscribe(method=method, callback=callback, param={})
        return

    def ticker(self, callback, param: Optional[dict] = dict(symbol="BTC_USDT")):
        """
        - Get the latest transaction price, buy price, sell price and 24 transaction volume
        - of a contract, send the transaction data without users' login.
        - Send once a second after subscription.
        """
        method = "sub.ticker"
        self._method_subscribe(method=method, callback=callback, param=param)
        return

    def transaction(self, callback, param: Optional[dict] = dict(symbol="BTC_USDT")):
        """
        - Access to the latest data without login, and keep updating
        """
        method = "sub.deal"
        self._method_subscribe(method=method, callback=callback, param=param)
        return

    def depth(self, callback, param: Optional[dict] = dict(symbol="BTC_USDT")):
        method = "sub.depth"
        self._method_subscribe(method=method, callback=callback, param=param)
        return

    def kline(
        self,
        callback,
        symbol: Optional[str] = "BTC_USDT",
        interval: Union[
            Literal["Min1"],
            Literal["Min5"],
            Literal["Min15"],
            Literal["Min30"],
            Literal["Min60"],
            Literal["Hour4"],
            Literal["Hour8"],
            Literal["Day1"],
            Literal["Week1"],
            Literal["Month1"],
        ] = "Min15",
    ):
        """
        - Get the k-line data of the contract and keep updating.
        - subscribe, unsubscribe, example is shown on the right.
        - interval optional parameters:
            - Min1
            - Min5
            - Min15
            - Min30
            - Min60
            - Hour4
            - Hour8
            - Day1
            - Week1
            - Month1
        """
        param = dict(symbol=symbol, interval=interval)
        method = "sub.kline"
        self._method_subscribe(method=method, callback=callback, param=param)
        return

    def funding_rate(self, callback, param: Optional[dict] = dict(symbol="BTC_USDT")):
        """
        - Get the contract funding rate and keep updating
        """
        method = "sub.funding.rate"
        self._method_subscribe(method=method, callback=callback, param=param)
        return

    def index_price(self, callback, param: Optional[dict] = dict(symbol="BTC_USDT")):
        """
        - Get the index price and will keep updating if there is any changes
        """
        method = "sub.index.price"
        self._method_subscribe(
            method=method,
            callback=callback,
            param=param,
        )
        return

    def fair_price(
        self,
        callback,
        param: Optional[dict] = dict(symbol="BTC_USDT"),
    ):
        """
        - Get the fair price and will keep updating if there is any changes
        """
        method = "sub.fair_price"
        self._method_subscribe(
            method=method,
            callback=callback,
            param=param,
        )
        return

    """
    #########################################################################################################################################################
    - Private Endpoint
        - Order
        - Asset
        - Position
        - Risk Limitation
        - Adl automatic reduction of position level
        - Position Mode
    #########################################################################################################################################################
    """

    def order(self, callback, param: Optional[dict] = dict()) -> None:
        """
        - It fetches the order list of the user's account.
        - currently on the maintanence
            - tmeporarily closed
            # TODO: keep checking the upload log of MEXC API and testing
        """
        method = "sub.personal.order"
        self._method_subscribe(
            method=method,
            callback=callback,
            param=param,
        )
        return

    def asset(self, callback, param: Optional[dict] = dict()) -> None:
        """
        func asset:
            - A function to subscribe to the asset information of the user.

        param callback:
            - The callback function to handle the asset information.
        param param:
            - Optional[dict], optional parameters for the subscription.
            - default is empty dictionary

        return None
        """
        method = "sub.personal.asset"
        self._method_subscribe(
            method=method,
            callback=callback,
            param=param,
        )
        return None

    def position(self, callback, param: Optional[dict] = dict()) -> None:
        # TODO: Need to implement the position function
        method = "sub.personal.position"
        return

    def risk_limitation(self, callback, param: Optional[dict] = dict()) -> None:
        # TODO: Need to implement the risk_limitation function
        return

    def adl(self, callback, param: Optional[dict] = dict()) -> None:
        # TODO: Need to implement the adl function
        method = "sub.personal.adl.level"
        return

    def position_mode(self, callback, param: Optional[dict] = dict()) -> None:
        # TODO: Need to implement the position_mode function
        method = "sub.personal.position.mode"
        return
