"""
Future Trade API
Documentation: https://mexcdevelop.github.io/apidocs/contract_v1_en
"""
from typing import Optional, Literal, Union, Callable

from mexc.base_sdk import FutureBase
from mexc.websocket_base import _FutureWebSocket
from logger.set_logger import logger

# no need to authenticate
class FutureMarket(FutureBase):
    """
    ######################################################################################################################
    #                                                    Public Endpoint                                                 #
    ######################################################################################################################
    """
    def ping(self) -> dict:
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
            method = 'GET',
            url = url,
        )
    
    def detail(
        self,
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
            params = dict(
                symbol = symbol
            ),
        )

    def support_currencies(self):
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
            method = "GET",
            url = url,
        )
    
    def depth(
        self,
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
        return self.call(
            method = "GET",
            url = url,
            params = dict(
                limit = limit
            ),
        )

    def depth_commits(
        self,
        limit: int = 5,
        symbol: str = "BTC_USDT"
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
        return self.call(
            method = "GET",
            url = url,
            params = dict(
                limit = limit
            ),
        )

    def index_price(
        self,
        symbol: str = "BTC_USDT"
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
        self,
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
        self,
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
        interval:
            Optional[
                Union[Literal["Min1"],
                    Literal["Min5"],
                    Literal["Min15"],
                    Literal["Min30"],
                    Literal["Min60"],
                    Literal["Hour4"],
                    Literal["Hour8"],
                    Literal["Day1"],
                    Literal["Week1"],
                    Literal["Month1"]]
            ] = "Min1", # default value is one minute.
            start: Optional[int] = None,
            end: Optional[int] = None,
            symbol: str = "BTC_USDT"
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
        return self.call(
            method = "GET",
            url = url,
            params = dict(
                symbol = symbol,
                interval = interval,
                start = start,
                end = end
            ),
        )
    
    def kline_index_price(
        self,
        interval:
            Optional[
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
                    Literal["Month1"]
                ]
            ] = "Min1",
        start: Optional[int] = None,
        end: Optional[int] = None,
        symbol: str = "BTC_USDT"
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
        return self.call(
            "GET",
            url,
            params=dict(
                symbol = symbol,
                interval = interval,
                start = start,
                end = end,
            ),
        )

    def kline_fair_price(
        self,
        interval:
            Optional[
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
                    Literal["Month1"]
                ]
            ] = "Min1",
        start: Optional[int] = None,
        end: Optional[int] = None,
        symbol: str = "BTC_USDT"
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
        return self.call(
            method = "GET",
            url = url,
            params = dict(
                symbol = symbol,
                interval = interval,
                start = start,
                end = end,
            ),
        )
    
    def deals(
        self,
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
        return self.call(
            method = "GET",
            url = url,
            params = dict(
                symbol = symbol,
                limit = limit,
            ),
        )
    
    def ticker(
        self,
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
        return self.call(
            method = "GET",
            url = url,
            params = dict(
                symbol = symbol,
            ),
        )
    
    def risk_reverse(self):
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
        self, 
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
        return self.call(
            method = "GET",
            url = url,
            params = dict(
                symbol = symbol,
                page_num = page_num,
                page_size = page_size
            ),
        )

    def funding_rate_history(
        self,
        symbol: str = "BTC_USDT",
        page_num: int = 1,
        page_size: int  = 100,
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
        return self.call(
            method = "GET",
            url = url,
            params = dict(
                symbol = symbol,
                page_num = page_num,
                page_size = page_size,
            ),
        )

    """
    ######################################################################################################################
    #                                                   Private Endpoint                                                 #
    ######################################################################################################################
    """
    def assets(self):
        """
        - method: assets()
            - Getting all information of user's asset
            - Required Permissions: Trade reading permission

        - Rate limit: 20 times / 2 seconds

        - Request parameters
            - None
        """
        return self.call("GET", "api/v1/private/account/assets")
    
    def asset(
        self, 
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
        self,
        symbol: Optional[str] = "BTC_USDT",
        type:   Optional[int] = None,
        page_num: Optional[int] = 1,
        page_size: Optional[int] = 100
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
        return self.call(
            "GET",
            "api/v1/private/position/list/history_positions",
            params = dict(
                symbol = symbol,
                type = type,
                page_num = page_num,
                page_size = page_size
            ),
        )

    def current_position(
        self,
        symbol: Optional[str] = "BTC_USDT"
    ):
        """
        - method: current_position()
            - get the user's current holding position
            - trade reading permission

        - Rate Limit: 20 times / 2 seconds

        - request parameters:
            - symbol: str, optional, the name of the contract
        """
        return self.call(
            "GET",
            "api/v1/private/position/open_positions",
            params = dict(
                symbol = symbol
            )
        )

    def pending_order(
        self,
        symbol: Optional[str] = "BTC_USDT",
        page_num: Optional[int] = 1,
        page_size: Optional[int] = 100
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
        return self.call(
            "GET",
            f"api/v1/private/order/list/open_orders/{symbol}",
            params = dict(
                symbol = symbol,
                page_num = page_num,
                page_size = page_size
            )
        )
    
    def risk_limit(
        self,
        symbol: Optional[str] = "BTC_USDT"
    ):
        """
        - method: risk_limit()
            - get the user's current pending order
            - trade reading permission

        - Rate Limit: 20 times / 2 seconds

        - request parameters:
            - symbol: str, optional, the name of the contract, not uploaded will return all
        """
        return self.call(
            "GET",
            "api/v1/private/account/risk_limit",
            params = dict(
                symbol = symbol
            )
        )
    
    def fee_rate(
        self,
        symbol: Optional[str] = "BTC_USDT"
    ):
        """
        - method: fee_rate()
            - get the user's current rading fee rate
            - trade reading permission

        - Rate Limit: 20 times / 2 seconds

        - request parameters:
            - symbol: str, optional, the nmae of the contract
        """
        return self.call(
            "GET",
            "api/v1/private/account/tiered_fee_rate",
            params = dict(
                symbol = symbol
            )
        )

    def place_order(
        self,
        price: float,
        vol: float,
        side: int, # 1 and 3
        type: int = 5, # 5 for market, need to test 6
        openType: int = 2, # 2 for cross
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
        return self.call(
            "POST",
            "api/v1/private/order/submit",
            params = dict(
                symbol = symbol,
                price = price,
                vol = vol,
                leverage = leverage,
                side = side,
                type = type,
                openType= openType,
                positionId = positionId,
                externalOid = externalOid,
                stopLossPrice = stopLossPrice,
                takeProfitPrice = takeProfitPrice,
                positionMode = positionMode,
                reduceOnly = reduceOnly
            )
        )
    

class FutureWebSocket(_FutureWebSocket):
    def __init__(
        ws_name: Optional[str] = None,
        api_key: Optional[str] = None,
        secret_key: Optional[str] = None,
        ping_interval: Optional[int] = 20, # as it is recommended
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
    def tickers(
        self,
        callback
    ):
        """
        - Get the latest transaction price, buy-price, sell-price and 24 transaction volume
        - of all the perpetual contracts on the platform without login.
        - Send once a second after subscribing
        """
        method = "sub.tickers"
        self._method_subscribe(
            method = method,
            callback = callback,
            param = {}
        )
        return
    
    def ticker(
        self,
        callback,
        param: Optional[dict] = dict(
            symbol = "BTC_USDT"
        )
    ):
        """
        - Get the latest transaction price, buy price, sell price and 24 transaction volume
        - of a contract, send the transaction data without users' login.
        - Send once a second after subscription.
        """
        method = "sub.ticker"
        self._method_subscribe(
            method = method,
            callback= callback,
            param = param
        )
        return
    
    def transaction(
        self,
        callback,
        param: Optional[dict] = dict(
            symbol = "BTC_USDT"
        )
    ):
        """
        - Access to the latest data without login, and keep updating
        """
        method = "sub.deal"
        self._method_subscribe(
            method=method,
            callback=callback,
            param=param
        )
        return
    
    def depth(
        self,
        callback,
        param: Optional[dict] = dict(
            symbol = "BTC_USDT"
        )
    ):
        method = "sub.depth"
        self._method_subscribe(
            method = method,
            callback=callback,
            param= param
        )
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
            Literal["Month1"]
        ] = "Min15"
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
        param = dict(
            symbol = symbol,
            interval = interval
        )
        method = "sub.kline"
        self._method_subscribe(
            method=method,
            callback=callback,
            param=param
        )
        return
    
    def funding_rate(
        self,
        callback,
        param: Optional[dict] = dict(
            symbol = "BTC_USDT"
        )
    ):
        """
        - Get the contract funding rate and keep updating
        """
        method = "sub.funding.rate"
        self._method_subscribe(
            method= method,
            callback=callback,
            param=param
        )
        return
    
    def index_price(
        self,
        callback,
        param: Optional[dict] = dict(
            symbol = "BTC_USDT"
        )
    ):
        """
        - Get the index price and will keep updating if there is any changes
        """
        method = "sub.index.price"
        self._method_subscribe(
            method = method,
            callback = callback,
            param = param,
        )
        return
    
    def fair_price(
        self,
        callback,
        param: Optional[dict] = dict(
            symbol = "BTC_USDT"
        ),
    ): 
        """
        - Get the fair price and will keep updating if there is any changes
        """
        method = "sub.fair_price"
        self._method_subscribe(
            method = method,
            callback = callback,
            param = param,
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
    def order(
        self,
        callback,
        param: Optional[dict] = dict()
    ) -> None:
        '''
            - place an order on the MexC broker
            - currently on the maintanence
                - tmeporarily closed
                # TODO: keep checking the upload log of MEXC API and testing
        '''
        method = "sub.personal.order"
        self._method_subscribe(
            method = method,
            callback = callback,
            param = param,
        )
        return
    
    def asset(
        self,
        callback,
        param: Optional[dict] = dict()
    ):
        method = "sub.personal.asset"
        self._method_subscribe(
            method = method,
            callback = callback,
            param = param,
        )
        return
    
    def position(
        self,
        callback,
        param: Optional[dict] = dict()
    ):
        method = "sub.personal.position"
        return
    
    def risk_limitation(
        self,
        callback,
        param: Optional[dict] = dict()
    ):
        return
    
    def adl(
        self,
        callback,
        param: Optional[dict] = dict()
    ):
        method = "sub.personal.adl.level"
        return
    
    def position_mode(
        self,
        callback,
        param: Optional[dict] = dict()
    ):
        method = "sub.personal.position.mode"
        return