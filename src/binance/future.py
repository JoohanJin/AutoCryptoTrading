# Standard Library
from abc import abstractmethod
import time

# Custom Library
from binance.base_sdk import FutureBase


class FutureMarket(FutureBase):
    """
    REST API Version 1 for Binance Futures.

    Market data endpoints for Binance Futures API.
    Every crypto currency trading pair is supported, while the default is "BTCUSDT".

    probably need to change this to "BTCUSDC" in the future.
    """
    @abstractmethod
    def generate_timestmap() -> int:
        return int(time.time() * 1_000)

    def __init__(
        self: "FutureMarket",
        api_key: str | None = None,
        secret_key: str | None = None,
        base_url: str | None = "https://fapi.binance.com",
    ) -> None:
        super().__init__(
            api_key = api_key,
            secret_key = secret_key,
            base_url = base_url,
        )

    def ping(
        self: "FutureMarket",
    ) -> dict:
        """
        Test connectivity to the Rest API.

        GET /fapi/v1/ping

        return: The response from the server as a dictionary.
        """
        url: str = "/fapi/v1/ping"

        return self.call(
            method = "GET",
            url = url,
        )

    def server_time(
        self: "FutureMarket",
    ) -> dict:
        """
        Test connectivity to the Rest API and get the current server time.

        GET /fapi/v1/time

        return: The response from the server as a dictionary.
        """
        url: str = "/fapi/v1/time"

        return self.call(
            method = "GET",
            url = url,
        )

    def exchange_info(
        self: "FutureMarket",
    ) -> dict:
        """
        Current exchange trading rules and symbol information.

        GET /fapi/v1/exchangeInfo

        return: The response from the server as a dictionary.
        """
        url: str = "/fapi/v1/exchangeInfo"

        return self.call(
            method = "GET",
            url = url,
        )

    def order_book(
        self: "FutureMarket",
        symbol: str = "BTCUSDT",
        limit: int = 1_000,
    ) -> dict:
        """
        Get the order book for a specific symbol.

        GET /fapi/v1/depth

        param symbol: The trading pair symbol (e.g., "BTCUSDT").
        param limit: The number of order book entries to return. Default is 100; max is 5000.

        return: The response from the server as a dictionary.
        """
        url: str = "/fapi/v1/depth"
        params: dict[str, str | int] = {
            "symbol": symbol,
            "limit": limit,
        }

        return self.call(
            method = "GET",
            url = url,
            params = params,
        )

    def recent_trades(
        self: "FutureMarket",
        symbol: str = "BTCUSDT",
        limit: int = 1_000,
    ) -> dict:
        """
        Get recent trades for a specific symbol.

        GET /fapi/v1/trades

        param symbol: The trading pair symbol (e.g., "BTCUSDT").
        param limit: The number of trades to return. Default is 500; max is 1000.

        return: The response from the server as a dictionary.
        """
        url: str = "/fapi/v1/trades"
        params: dict[str, str | int] = {
            "symbol": symbol,
            "limit": limit,
        }

        return self.call(
            method = "GET",
            url = url,
            params = params,
        )

    def historical_trades(
        self: "FutureMarket",
        symbol: str = "BTCUSDT",
        limit: int = 500,
        from_id: int | None = None,
    ) -> dict:
        """
        Get historical trades for a specific symbol.

        GET /fapi/v1/historicalTrades

        param symbol: The trading pair symbol (e.g., "BTCUSDT").
        param limit: The number of trades to return. Default is 500; max is 1000.
        param from_id: Trade id to fetch from. Default gets most recent trades.

        return: The response from the server as a dictionary.
        """
        url: str = "/fapi/v1/historicalTrades"
        params: dict[str, str | int] = {
            "symbol": symbol,
            "limit": limit,
        }
        if from_id is not None:
            params["fromId"] = from_id

        headers: dict[str, str] = {}
        # TODO: if api_key is None, raise an error.
        if self.api_key:
            headers["X-MBX-APIKEY"] = self.api_key

        return self.call(
            method = "GET",
            url = url,
            params = params,
            headers = headers,
        )

    def compressed_aggregate_trades(
        self: "FutureMarket",
        symbol: str = "BTCUSDT",
        from_id: int | None = None,
        start_time: int | None = None,
        end_time: int | None = None,
        limit: int = 1_000,
    ) -> dict:
        """
        Get compressed, aggregate trades. Trades that fill at the same time, from the same order, with the same price will have the quantity aggregated.

        GET /fapi/v1/aggTrades

        param symbol: The trading pair symbol (e.g., "BTCUSDT").
        param from_id: ID to get aggregate trades from INCLUSIVE.
        param start_time: Timestamp in ms to get aggregate trades from INCLUSIVE.
        param end_time: Timestamp in ms to get aggregate trades until INCLUSIVE.
        param limit: The number of trades to return. Default is 500; max is 1000.

        return: The response from the server as a dictionary.
        """
        url: str = "/fapi/v1/aggTrades"
        params: dict[str, str | int] = {
            "symbol": symbol,
            "limit": limit,
        }
        if from_id is not None:
            params["fromId"] = from_id
        if start_time is not None:
            params["startTime"] = start_time
        if end_time is not None:
            params["endTime"] = end_time

        return self.call(
            method = "GET",
            url = url,
            params = params,
        )

    def klines(
        self: "FutureMarket",
        symbol: str = "BTCUSDT",
        interval: str = "1m",
        startTime: int | None = None,
        endTime: int | None = None,
        limit: int | None = 500,  # maximum 1_500
    ) -> dict:
        """
        Get Kline/candlestick bars for a symbol. Klines are uniquely identified by their open time.

        GET /fapi/v1/klines

        param symbol: The trading pair symbol (e.g., "BTCUSDT").
        param interval: The interval for the klines (e.g., "1m", "5m", "1h", "1d").

        return: The response from the server as a dictionary.
        """
        url: str = "/fapi/v1/klines"
        params: dict[str, str | int] = {
            "symbol": symbol,
            "interval": interval,
        }

        if startTime is not None:
            params["startTime"] = startTime
        if endTime is not None:
            params["endTime"] = endTime
        if limit is not None:
            params["limit"] = limit

        return self.call(
            method = "GET",
            url = url,
            params = params,
        )

    def continuous_klines(
        self: "FutureMarket",
        pair: str = "BTCUSDT",
        contract_type: str = "PERPETUAL",
        interval: str = "1m",
        startTime: int | None = None,
        endTime: int | None = None,
        limit: int | None = 500,  # maximum 1_500
    ) -> dict:
        """
        Get Kline/candlestick bars for a specific pair and contract type. Klines are uniquely identified by their open time.

        GET /fapi/v1/continuousKlines

        param pair: The trading pair (e.g., "BTCUSDT").
        param contract_type: The contract type (e.g., "PERPETUAL", "CURRENT_MONTH", "NEXT_MONTH", "CURRENT_QUARTER", "NEXT_QUARTER").
        param interval: The interval for the klines (e.g., "1m", "5m", "1h", "1d").

        return: The response from the server as a dictionary.
        """
        url: str = "/fapi/v1/continuousKlines"
        params: dict[str, str | int] = {
            "pair": pair,
            "contractType": contract_type,
            "interval": interval,
        }

        if startTime is not None:
            params["startTime"] = startTime
        if endTime is not None:
            params["endTime"] = endTime
        if limit is not None:
            params["limit"] = limit

        return self.call(
            method = "GET",
            url = url,
            params = params,
        )

    def index_price_klines(
        self: "FutureMarket",
        pair: str = "BTCUSDT",
        interval: str = "1m",
        startTime: int | None = None,
        endTime: int | None = None,
        limit: int | None = 500,  # maximum 1_500
    ) -> dict:
        """
        Get Kline/candlestick bars for a specific symbol's index price. Klines are uniquely identified by their open time.

        GET /fapi/v1/indexPriceKlines

        param symbol: The trading pair symbol (e.g., "BTCUSDT").
        param interval: The interval for the klines (e.g., "1m", "5m", "1h", "1d").

        return: The response from the server as a dictionary.
        """
        url: str = "/fapi/v1/indexPriceKlines"
        params: dict[str, str | int] = {
            "pair": pair,
            "interval": interval,
        }

        if startTime is not None:
            params["startTime"] = startTime
        if endTime is not None:
            params["endTime"] = endTime
        if limit is not None:
            params["limit"] = limit

        return self.call(
            method = "GET",
            url = url,
            params = params,
        )

    def mark_price_klines(
        self: "FutureMarket",
        symbol: str = "BTCUSDT",
        interval: str = "1m",
        startTime: int | None = None,
        endTime: int | None = None,
        limit: int | None = 500,  # maximum 1_500
    ) -> dict:
        """
        Get Kline/candlestick bars for a specific symbol's mark price. Klines are uniquely identified by their open time.

        GET /fapi/v1/markPriceKlines

        param symbol: The trading pair symbol (e.g., "BTCUSDT").
        param interval: The interval for the klines (e.g., "1m", "5m", "1h", "1d").

        return: The response from the server as a dictionary.
        """
        url: str = "/fapi/v1/markPriceKlines"
        params: dict[str, str | int] = {
            "symbol": symbol,
            "interval": interval,
        }

        if startTime is not None:
            params["startTime"] = startTime
        if endTime is not None:
            params["endTime"] = endTime
        if limit is not None:
            params["limit"] = limit

        return self.call(
            method = "GET",
            url = url,
            params = params,
        )

    def premium_klines(
        self: "FutureMarket",
        symbol: str = "BTCUSDT",
        interval: str = "1m",
        startTime: int | None = None,
        endTime: int | None = None,
        limit: int | None = 500,  # maximum 1_500
    ) -> dict:
        """
        Get Kline/candlestick bars for a specific symbol's premium index. Klines are uniquely identified by their open time.

        GET /fapi/v1/premiumIndexKlines

        param symbol: The trading pair symbol (e.g., "BTCUSDT").
        param interval: The interval for the klines (e.g., "1m", "5m", "1h", "1d").

        return: The response from the server as a dictionary.
        """
        url: str = "/fapi/v1/premiumIndexKlines"
        params: dict[str, str | int] = {
            "symbol": symbol,
            "interval": interval,
        }

        if startTime is not None:
            params["startTime"] = startTime
        if endTime is not None:
            params["endTime"] = endTime
        if limit is not None:
            params["limit"] = limit

        return self.call(
            method = "GET",
            url = url,
            params = params,
        )

    def mark_price(
        self: "FutureMarket",
        symbol: str = "BTCUSDT",
    ) -> dict:
        """
        Get the current mark price and funding rate for a specific symbol.

        GET /fapi/v1/premiumIndex

        param symbol: The trading pair symbol (e.g., "BTCUSDT").

        return: The response from the server as a dictionary.
        """
        url: str = "/fapi/v1/premiumIndex"
        params: dict[str, str] = {
            "symbol": symbol,
        }

        return self.call(
            method = "GET",
            url = url,
            params = params,
        )

    def funding_rate_history(
        self: "FutureMarket",
        symbol: str = "BTCUSDT",
        startTime: int | None = None,
        endTime: int | None = None,
        limit: int = 100,  # maximum 1_000
    ) -> dict:
        """
        Get the funding rate history for a specific symbol.

        GET /fapi/v1/fundingRate

        param symbol: The trading pair symbol (e.g., "BTCUSDT").
        param startTime: Timestamp in ms to get funding rate history from INCLUSIVE.
        param endTime: Timestamp in ms to get funding rate history until INCLUSIVE.
        param limit: The number of records to return. Default is 100; max is 1000.

        return: The response from the server as a dictionary.
        """
        url: str = "/fapi/v1/fundingRate"
        params: dict[str, str | int] = {
            "symbol": symbol,
            "limit": limit,
        }
        if startTime is not None:
            params["startTime"] = startTime
        if endTime is not None:
            params["endTime"] = endTime

        return self.call(
            method = "GET",
            url = url,
            params = params,
        )

    def funding_rate_info(
        self: "FutureMarket",
    ) -> dict:
        """
        Get the current funding rate and funding rate history for all symbols.

        GET /fapi/v1/fundingRate

        return: The response from the server as a dictionary.
        """
        url: str = "/fapi/v1/fundingRate"

        return self.call(
            method = "GET",
            url = url,
        )

    def ticker_24hr(
        self: "FutureMarket",
        symbol: str = "BTCUSDT",
    ) -> dict:
        """
        Get 24 hour rolling window price change statistics for a specific symbol.

        GET /fapi/v1/ticker/24hr

        param symbol: The trading pair symbol (e.g., "BTCUSDT").

        return: The response from the server as a dictionary.
        """
        url: str = "/fapi/v1/ticker/24hr"
        params: dict[str, str] = {
            "symbol": symbol,
        }

        return self.call(
            method = "GET",
            url = url,
            params = params,
        )

    def top_trader_long_short_ratio(
        self = "FutureMarket",
        symbol: str = "BTCUSDT",
        period: str = "5m",
        limit: int = 30,  # maximum 500,
        startTime: int | None = None,
        endTime: int | None = None,
    ) -> dict:
        """
        - Get the long/short ratio of top traders for a specific symbol and time period.
        """
        url: str = "/futures/data/topLongShortAccountRatio"
        params: dict[str, str | int] = {
            "symbol": symbol,
            "period": period,
            "limit": limit,
        }
        if startTime is not None:
            params["startTime"] = startTime
        if endTime is not None:
            params["endTime"] = endTime

        return self.call(
            method = "GET",
            url = url,
            params = params,
        )

    def long_short_ratio(
        self = "FutureMarket",
        symbol: str = "BTCUSDT",
        period: str = "5m",
        limit: int = 30,  # maximum 500,
        startTime: int | None = None,
        endTime: int | None = None,
    ) -> dict:
        """
        - Get the long/short ratio for a specific symbol and time period.
        """
        url: str = "/futures/data/globalLongShortAccountRatio"
        params: dict[str, str | int] = {
            "symbol": symbol,
            "period": period,
            "limit": limit,
        }
        if startTime is not None:
            params["startTime"] = startTime
        if endTime is not None:
            params["endTime"] = endTime

        return self.call(
            method = "GET",
            url = url,
            params = params,
        )

    def taker_busy_sell_volume(
        self: "FutureMarket",
        symbol: str = "BTCUSDT",
        period: str = "5m",  # 5m, 15m, 30m, 1h, 2h, 4h, 6h, 12h, 1d
        limit: int = 30,  # maximum 500,
        startTime: int | None = None,
        endTime: int | None = None,
    ) -> dict:
        """
        - Get the taker buy/sell volume for a specific symbol and time period.
        """
        url: str = "/futures/data/takerlongshortRatio"
        params: dict[str, str | int] = {
            "symbol": symbol,
            "period": period,
            "limit": limit,
        }
        if startTime is not None:
            params["startTime"] = startTime
        if endTime is not None:
            params["endTime"] = endTime

        return self.call(
            method = "GET",
            url = url,
            params = params,
        )

    def basis(
        self: "FutureMarket",
        pair: str = "BTCUSDT",
        contract_type: str = "PERPETUAL",
        period: str = "5m",  # 5m, 15m, 30m, 1h, 2h, 4h, 6h, 12h, 1d
        limit: int = 30,  # maximum 500,
        startTime: int | None = None,
        endTime: int | None = None,
    ) -> dict:
        """
        - Get the basis for a specific pair, contract type, and time period.
        """
        url: str = "/futures/data/basis"
        params: dict[str, str | int] = {
            "pair": pair,
            "contractType": contract_type,
            "period": period,
            "limit": limit,
        }
        if startTime is not None:
            params["startTime"] = startTime
        if endTime is not None:
            params["endTime"] = endTime

        return self.call(
            method = "GET",
            url = url,
            params = params,
        )

    def composite_index_symbol_info(
        self: "FutureMarket",
        symbol: str | None = "BTCUSDT",
    ) -> dict:
        """
        - Get the composite index symbol information.
        """
        url: str = "/fapi/v1/indexInfo"
        params: dict[str, str] = {
            "symbol": symbol,
        }

        return self.call(
            method = "GET",
            url = url,
            params = params,
        )

    def asset_index(
        self: "FutureMarket",
        symbol: str = "BTCUSDT",
    ) -> dict:
        """
        - asset index for multi-assets mode.
        """
        url: str = "/fapi/v1/assetIndex"
        params: dict[str, str] = {
            "symbol": symbol,
        }

        return self.call(
            method = "GET",
            url = url,
            params = params,
        )

    def query_index_price_consituents(
        self: "FutureMarket",
        symbol: str = "BTCUSDT",
    ) -> dict:
        """
        - Query index price constituents.
        """
        url: str = "/fapi/v1/indexPriceConstituents"
        params: dict[str, str] = {
            "symbol": symbol,
        }

        return self.call(
            method = "GET",
            url = url,
            params = params,
        )

    """
    # ORDER ENDPOINTS
    """

    def new_order(
        self: "FutureMarket",
        symbol: str = "BTCUSDT",
        side: str = "BUY",
        position_side: str | None = None,  # "BOTH", "LONG", "SHORT"
        type: str = "MARKET",
        time_in_force: str | None = None,
        quantity: float | None = None,
        price: float | None = None,
        new_client_order_id: str | None = None,
        stop_price: float | None = None,
        close_position: str | None = None,
        activation_price: float | None = None,
        callback_rate: float | None = None,
        working_type: str | None = None,
        price_protect: str | None = None,
        new_order_resp_type: str | None = None,
        price_match: str | None = None,
        self_trade_prevention_mode: str | None = None,
        good_till_date: int | None = None,
        recvWindow: int | None = 5_000,  # 5_000 ms is the default value, i.e., 5 sec.
        timestamp: int | None = None,
    ):
        raise NotImplementedError
        return

    def multiple_orders(
        self: "FutureMarket",
    ):
        raise NotImplementedError
        return

    def modify_order(
        self: "FutureMarket",
    ):
        raise NotImplementedError
        return

    def modify_multiple_orders(
        self: "FutureMarket",
    ):
        raise NotImplementedError
        return

    def get_order_modify_history(
        self: "FutureMarket",
    ):
        raise NotImplementedError
        return

    def cancel_order(
        self: "FutureMarket",
    ):
        raise NotImplementedError
        return

    def cancel_multiple_orders(self: "FutureMarket",):
        raise NotImplementedError
        return

    def cancel_all_orders(
        self: "FutureMarket",
    ):
        raise NotImplementedError
        return

    def auto_cancel_all_open_orders(
        self: "FutureMarket",
    ):
        raise NotImplementedError
        return

    def query_order(self: "FutureMarket",):
        raise NotImplementedError
        return

    def query_all_orders(
        self: "FutureMarket",
        symbol: str = "BTCUSDT",
        order_id: int | None = None,
        start_time: int | None = None,
        end_time: int | None = None,
        limit: int | None = 500,  # max 1_000
        recv_window: int | None = 5_000,
        timestamp: int | None = None,
    ):
        url: str = "/fapi/v1/allOrders"

        params: dict[str, int | str] = {
            "symbol": symbol,
            "timestamp": timestamp if timestamp is not None else FutureMarket.generate_timestmap(),
        }

        if order_id is not None:
            params["orderId"] = order_id
        if start_time is not None:
            params["startTime"] = start_time
        if end_time is not None:
            params["endTime"] = end_time
        if limit is not None:
            params["limit"] = limit
        if recv_window is not None:
            params["recvWindow"] = recv_window

        return self.call(
            method = "GET",
            url = url,
            params = params,
        )

    def query_open_order(self: "FutureMarket",):
        raise NotImplementedError
        return

    def query_all_open_orders(self: "FutureMarket",):
        raise NotImplementedError
        return

    def query_account_trades(self: "FutureMarket",):
        raise NotImplementedError
        return

    def query_user_force_orders(self: "FutureMarket",):
        raise NotImplementedError
        return

    def change_margin_type(self: "FutureMarket",):
        raise NotImplementedError
        return

    def change_position_mode(self: "FutureMarket",):
        raise NotImplementedError
        return

    def change_initial_leverage(self: "FutureMarket",):
        raise NotImplementedError
        return

    def change_multi_assets_mode(self: "FutureMarket",):
        raise NotImplementedError
        return

    def change_isolated_position_margin(
        self: "FutureMarket",
    ):
        raise NotImplementedError
        return

    def postion_info_v2(self: "FutureMarket",):
        raise NotImplementedError
        return

    def position_info_v3(self: "FutureMarket",):
        raise NotImplementedError
        return

    def position_adl_quantile_estimation(self: "FutureMarket",):
        raise NotImplementedError
        return

    def get_position_margin_history(self: "FutureMarket",):
        return

    def test_new_order(self: "FutureMarket",):
        raise NotImplementedError
        return

    def future_account_balance_v3(
        self: "FutureMarket",
        url: str = "/fapi/v3/balance",
        recv_window: int = 5_000,
    ):
        params: dict[str, int] = dict(
            recvWindow = recv_window,
            timestamp = FutureMarket.generate_timestmap(),
        )

        return self.call(
            method = "GET",
            params = params,
            url = url,
        )


class FutureWebSocket:
    """
    WebSocket endpoints for Binance Futures API.
    """

    def __init__(
        self: "FutureWebSocket",
    ) -> None:
        return
