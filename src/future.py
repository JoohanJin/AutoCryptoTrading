"""
Future Trade API
Documentation: https://mexcdevelop.github.io/apidocs/contract_v1_en/?python#access-to-url
"""

import logging
from typing import Optional, Literal, Union

logger = logging.getLogger(__name__)

try:
    from base_sdk import FutureBase
except:
    from .base_sdk import FutureBase


# no need to authenticate
class FutureMarket(FutureBase):
    def ping(self) -> dict:
        """
        Function Name: ping

        Parameters: None

        Task: Get The Server Time

        Rate Limit: 20 times / 2 seconds

        Documentation:
            https://mexcdevelop.github.io/apidocs/contract_v1_en/?python#get-the-server-time
        """
        url: str = "api/v1/contract/ping"
        return self.call('GET', url)
    
    
    def detail(self, symbol: Optional[str] = None) -> dict:
        """
        Function Name: detail

        Parameters:
            # symbol: Optional[str], the name of the contract

        Task: Get the contract information

        Rate Limit: 1 times / 5 seconds
        
        Documentation:
            https://mexcdevelop.github.io/apidocs/contract_v1_en/?python#get-the-contract-information
        """    
        url: str = "api/v1/contract/detail"
        return self.call("GET", url, parmas = dict(
            symbol= symbol
        ))


    def support_currencies(self):
        """
        Function Name: support_currencies

        Parameters: None

        Task:
            # Get the transferable currencies
            # The returned "data" field contains a list of string with each string represents a supported currencies

        Rate Limit: 20 times / 2 seconds

        Documentation:
            https://mexcdevelop.github.io/apidocs/contract_v1_en/?python#get-the-transferable-currencies
        """
        url: str = "/api/v1/contract/support_currencies"
        return self.call("GET", url)
    
    
    def depth(self, symbol: str = "BTC_USDT", limit: Optional[int] = None) -> dict:
        """
        Function Name: depth

        Parameters:
            # symbol: str, the name of the contract
            # limit: Optional[int], tier
        
        Task:
            # Get the contract's depth information

        Rate Limit: 20 times / 2 seconds

        Documentation:
            https://mexcdevelop.github.io/apidocs/contract_v1_en/?python#get-the-contract-s-depth-information
        """
        url: str = f"api/v1/contract/depth/{symbol}"
        return self.call("GET", url, params = dict(
            limit = limit
        ))

    
    def depth_commits(self, limit: int, symbol: str = "BTC_USDT") -> dict:
        """
        function name: depth_commits

        parameters:
            # symbol: str, the name of the contract
            # limit: int, count

        Task:
            # Get a snapshot of the lastest N depth information of the contract
        
        Rate Limit: 20 times / 2 seconds

        Documentation:
            https://mexcdevelop.github.io/apidocs/contract_v1_en/?python#get-a-snapshot-of-the-latest-n-depth-information-of-the-contract
        """
        url: str = f"api/v1/contract/depth_commits/{symbol}/{limit}"
        return self.call("GET", url, params = dict(
            limit = limit
        ))

    
    def index_price(self, symbol: str = "BTC_USDT"):
        """
        function name: index_price

        parameters:
            # symbol: str, the name of the contract
        
        Task:
            # Get contract index price

        Rate Limit: 20 times / 2 seconds

        Documentation:
            https://mexcdevelop.github.io/apidocs/contract_v1_en/?python#get-contract-index-price
        """
        url: str = f"api/v1/contract/index_price/{symbol}"
        return self.call("GET", url)

    
    def fair_price(self, symbol: str = "BTC_USDT"):
        """
        function name: fair_price

        parameters:
            # symbol: str, the name of the contract

        tasks:
            # Get contract fair price
        
        Rate Limit: 20 times / 2 seconds

        Documentation:
            https://mexcdevelop.github.io/apidocs/contract_v1_en/?python#get-contract-fair-price
        """
        url: str = f"api/v1/contract/fair_price/{symbol}"
        return self.call("GET", url)

    
    def funding_rate(self, symbol: str = "BTC_USDT") -> dict:
        """
        function name: funding_rate

        parameters:
            # symbol: str, the name of the contract
        
        tasks:
            # get contract funcding rate

        Rate Limit: 20 times / 2 seconds

        Documentation:
            https://mexcdevelop.github.io/apidocs/contract_v1_en/?python#get-contract-funding-rate
        """
        url: str = f"api/v1/contract/funding_rate/{symbol}"
        return self.call("GET", url)

    
    def kline(self,
              interval: Optional[Union[Literal["Min1"], Literal["Min5"], Literal["Min15"], Literal["Min30"], Literal["Min60"], Literal["Hour4"], Literal["Hour8"], Literal["Day1"], Literal["Week1"], Literal["Month1"]]] = None,
              start: Optional[int] = None,
              end: Optional[int] = None,
              symbol: str = "BTC_USDT"
              ):
        """
        function name: kline

        parameters:
            # symbol: str, the name of the contract
            # interval: Optional[str], interval for the k-line data
                # must be one of the followings
                "Min1", "Min5", "Min15", "Min30", "Min60", "Hour4", "Hour8", "Day1", "Week1", "Month1"
                default value is "Min1"
            # start: Optional[long], The start time of the k-line data in Unix timestamp format
            # end: Optional[long], The end time of the k-line data in Unix timestamp format

        tasks:
            # get the candle stick, or k-line data, for the price of the given cryptocurrency

        rate limit:
            20 times / 2 seconds

        Documentation:
            https://mexcdevelop.github.io/apidocs/contract_v1_en/?python#k-line-data

        Warning:
            # the maximum number of data received in one request is 2000
                # multiple requests are needed to get the fine and smooth data for a long period of time
            # if only the start time is provided, then query the data from the start time and the current system time
            # if only the end time is provided, the 2000 pieces of data closest to the end time are returned
            # if neither start time nor end time is provided, the 2000 pieces of data closest to the current time in the system are queried.
        """
        url: str = f"api/v1/contract/kline/{symbol}"
        return self.call("GET", url, params = dict(
            symbol = symbol,
            interval = interval,
            start = start,
            end = end
        ))

    
    def kline_index_price(self,
                          interval: Optional[Union[Literal["Min1"], Literal["Min5"], Literal["Min15"], Literal["Min30"], Literal["Min60"], Literal["Hour4"], Literal["Hour8"], Literal["Day1"], Literal["Week1"], Literal["Month1"]]] = None,
                          start: Optional[int] = None,
                          end: Optional[int] = None,
                          symbol: str = "BTC_USDT"
                          ):
        """
        function name: kline_index_price

        parameters:
            # symbol: str, the name of the contract
            # interval: Optional[str], interval for the k-line data
                # must be one of the followings
                "Min1", "Min5", "Min15", "Min30", "Min60", "Hour4", "Hour8", "Day1", "Week1", "Month1"
                default value is "Min1"
            # start: Optional[long], The start time of the k-line data in Unix timestamp format
            # end: Optional[long], The end time of the k-line data in Unix timestamp format

        task:
            # get the candle stick data for the index price of the given cryptocurrency

        rate limit:
            20 times / 2 seconds
        """
        url: str = f"api/v1/contract/kline/index_price/{symbol}"
        return self.call("GET", url, parmas=dict(
            symbol = symbol,
            interval = interval,
            start = start,
            end = end
        ))


    def kline_fair_price(self,
                         interval: Optional[Union[Literal["Min1"], Literal["Min5"], Literal["Min15"], Literal["Min30"], Literal["Min60"], Literal["Hour4"], Literal["Hour8"], Literal["Day1"], Literal["Week1"], Literal["Month1"]]] = None,
                         start: Optional[int] = None,
                         end: Optional[int] = None,
                         symbol: str = "BTC_USDT"
                         ):
        """
        function name: kline_fair_price

        parameters:
            # symbol: str, the name of the contract
            # interval: Optional[str], interval for the k-line data
                # must be one of the followings
                "Min1", "Min5", "Min15", "Min30", "Min60", "Hour4", "Hour8", "Day1", "Week1", "Month1"
                default value is "Min1"
            # start: Optional[long], the start time of the k-line data in Unix timestamp format
            # end: Optional[long], the end time of the k-line data in Unix timestamp format
        
        task:
            # get the candle stick data for the index price of the given cryptocurrency.

        rate limit:
            20 times / 2 seconds
        """
        url: str = f"api/v1/contract/kline/fair_price/{symbol}"
        return self.call("GET", url, params = dict(
            symbol = symbol,
            interval = interval,
            start = start,
            end = end
        ))
    

    
    def deals(self, symbol: str, limit: Optional[int]) -> dict:
        """
        function name: deals

        parameters:
            # symbol: str, the name of the contract
            # limit: Optional[int], consequence set quantity, maximum is 100, default 100 without setting

        task:
            # get contract transaction data
        
        rate limit:
            20 times / 2 seconds
        """
        url: str = f"api/v1/contract/deals/{symbol}"
        return self.call("GET", url, params = dict(
            symbol = symbol,
            limit = limit
        ))


    
    def ticker(self, symbol: Optional[str]):
        """
        function name: ticker

        parameters:
            # symbol: Optional[str], the name of the contract

        task:
            # get contract trend data
        
        rate limit:
            20 times / 2 seconds
        """
        url: str = "api/v1/contract/ticker"
        return self.call("GET", url, params = dict(
            symbol = symbol
        ))
    
    
    def risk_reverse(self):
        """
        function name: risk_reverse

        parameters: None

        task:
            # get all contract risk fund balance

        rate limit:
            20 times / 2 seconds
        """
        url: str = "api/v1/contract/risk_reverse"
        return self.call("GET", url)
    

    def risk_reverse_history(
        self, 
        symbol: str, 
        page_num: int, 
        page_size: int
    ) -> dict:
        """
        function name: risk_reverse_history

        parameters:
            # symbol: str, the name of the contract
            # page number: int, current page number, default is 1
            # page size: int, the page size, default 20, maximum 100
        
        task:
            # get contract risk fund balance history
        
        rate limit:
            20 times / 2 seconds
        """
        url: str = "api/v1/contract/risk_reverse/history"
        return self.call("GET", url, params = dict(
            symbol = symbol,
            page_num = page_num,
            page_size = page_size
        ))
    

    def funding_rate_history(
        self,
        symbol: str,
        page_num: int,
        page_size: int
    ) -> dict:
        """
        function name: funding_rate_history

        parameters:
            # symbol: str, the name of the contract
            # page_num: int, current page number, default is 1
            # page_size: int, the page size, default 20, maximum 100
        
        task:
            # get contract funcding rate history

        rate limit:
            20 times / 2 seconds
        """
        url: str = "api/v1/contract/funding_rate/history"
        return self.call("GET", url, params = dict(
            symbol = symbol,
            page_num = page_num,
            page_size = page_size
        ))

    # need to authenticate, i.e., need to have apiKey and secretKey
    def assets(self):
        """
        # method: assets()
            # Getting all information of user's asset
            # Required Permissions: Trade reading permission

        # Rate limit: 20 times / 2 seconds

        # Request parameters
            # None

        # documnetation link:
            https://mexcdevelop.github.io/apidocs/contract_v1_en/?python#get-all-informations-of-user-39-s-asset
        """
        return self.call("GET", "api/v1/private/account/assets")
    
    # function override
    def asset(self, currency: str = "USDT"):
        """
        # method: assets(currency: str)
            # get the user's single currency asset information
            # Required Permissions: Account reading permission

        # Rate Limit: 20 times / 2 seconds

        # Request Parameters
            # currency: str, mandatory

        # documenation link:
            https://mexcdevelop.github.io/apidocs/contract_v1_en/?python#get-the-user-39-s-single-currency-asset-information
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
        # method: history_position()
            # get the user's history position information
            # trade reading permission
        
        # Rate Limit: 20 times / 2 seconds

        # Request Parameters
            # symbol: str, optional, the name of the contract
            # type: int, optional, position type i.e. 1 - long, 2 - short
            # page_num: current page, default is 1
            # page_size

        # documentation link:
            # https://mexcdevelop.github.io/apidocs/contract_v1_en/?python#get-the-user-s-history-position-information
        """
        return self.call("GET",
                         "api/v1/private/position/list/history_positions",
                         params = dict(
                            symbol = symbol,
                            type = type,
                            page_num = page_num,
                            page_size = page_size
                         ))


    def current_position(
        self,
        symbol: Optional[str] = "BTC_USDT"
    ):
        """
        # method: current_position()
            # get the user's current holding position
            # trade reading permission

        # Rate Limit: 20 times / 2 seconds

        # request parameters:
            # symbol: str, optional, the name of the contract

        # documentation link
            # https://mexcdevelop.github.io/apidocs/contract_v1_en/?python#get-the-user-39-s-current-holding-position
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
        # method: pending_order
            # get the user's current pending order
            # trade reading permission

        # Rate Limit: 20 times / 2 seconds

        # request parameters
            # symbol: str, optional, the name of the contract, return all the contract parameters if there are no fill in
            # page_num: int, required, 
            # page_size: int, required

        # documentation link
            # https://mexcdevelop.github.io/apidocs/contract_v1_en/?python#get-the-user-39-s-current-pending-order
        """
        return self.call(
            "GET",
            f"api/v1/private/order/list/open_orders/{symbol}",
            parmas = dict(
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
        # method: risk_limit()
            # get the user's current pending order
            # trade reading permission

        # Rate Limit: 20 times / 2 seconds

        # request parameters:
            # symbol: str, optional, the name of the contract, not uploaded will return all

        # documentation link
            # https://mexcdevelop.github.io/apidocs/contract_v1_en/?python#get-risk-limits
        """
        return self.call(
            "GET",
            "api/v1/private/account/risk_limit",
            params = dict(
                symbol = symbol
            )
        )
    

    def fee_rete(
        self,
        symbol: Optional[str] = "BTC_USDT"
    ):
        """
        # method: fee_rate()
            # get the user's current rading fee rate
            # trade reading permission

        # Rate Limit: 20 times / 2 seconds

        # request parameters:
            # symbol: str, optional, the nmae of the contract

        # documenation link
            # https://mexcdevelop.github.io/apidocs/contract_v1_en/?python#gets-the-user-39-s-current-trading-fee-rate
        """
        return self.call(
            "GET",
            "api/v1/private/account/tiered_fee_rate",
            params = dict(
                symbol = symbol
            )
        )
    

    def order(
        self,
        price: float,
        vol: float,
        side: int, # 1 and 3
        type: int = 5, # 5 for market, need to test 6
        openType: int = 2, # 2 for cross
        positionId: Optional[int] = None,
        externalOid: Optional[int] = None,
        stopLossPrice: Optional[float] = None,
        takeProfitPrice: Optional[float] = None,
        positionMode: Optional[int] = None,
        reduceOnly: Optional[bool] = False,
        symbol: str = "BTC_USDT",
        leverage: Optional[int] = 50,
    ):
        """
        # Under-Maintanence on Broker Side
        # method: order()
            # USDT perpetual contract trading offers limit and market orders.
            # POST
        
        # Rate Limit: 20 times / 2 seconds

        # Request Parameters
            # symbol
                # str
                # Optional, BTC_USDT
                # the name of the contract
            # price
                # decimal
                # Required
                # price
            # vol
                # decimal
                # Required, 10%
                # volume
            # leverage
                # int
                # optional, 50
                # leverage, leverage is necessary on isolated margin
            # side
                # int
                # required
                # order direction
                    # 1: open long
                    # 2: close short
                    # 3: open short
                    # 4: close long
            # type
                # int
                # required
                # ordertype
                    # 1: price limited order
                    # 2: post only maker
                    # 3: transact or cancel instantly
                    # 4: transact completely or cancel completely
                    # 5: market orders
                    # 6: conver market price to current price
            # openType
                # int
                # required
                # open type
                    # 1: isolated
                    # 2: cross
            # positionId
                # long
                # optional
                # position id
                    # recommended to fill in this parameter when closing a position
            # externalOid
                # str
                # optional
                # external order ID
            # stopLossPrice
                # decimal
                # optional, -5%
                # stop-loss price
            # takeProfitPrice
                # decimal
                # optional, +15%
                # take-profit price
            # positionMode
                # int
                # optional
                # position mode
                    # 1: hedge
                    # 2: one-way
                    # default: user's current config
            # reduceOnly
                # bool
                # optional
                # defualt false
                    # one-way positions: if you need to only reduce positions, pass in true
                    # two-way positions: will not accept this parameter.

        # documentation link
            # https://mexcdevelop.github.io/apidocs/contract_v1_en/?python#order-under-maintenance
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