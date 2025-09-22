# Standard Library
from typing import Union, Literal

# Custom Library
from sdk.base_sdk import CommonBaseSDK


class FutureBase(CommonBaseSDK):
    """
    SDK for Binance Futures API, inheriting from CommonBaseAPI.
    """
    def __init__(
        self: "FutureBase",
        api_key: str | None = None,
        secret_key: str | None = None,
        base_url: str = "https://fapi.binance.com",
    ) -> None:
        # Please comment the following line if you want to turn off the testNet.
        # base_url = "https://testnet.binancefuture.com"  # this is the testNet

        super().__init__(
            api_key = api_key,
            secret_key = secret_key,
            base_url = base_url,
        )
        # Set the specific content type for Binance
        self.set_content_type("application/x-www-form-urlencoded")
        return

    def call(
        self: "FutureBase",
        method: Union[
            Literal["GET"],
            Literal["POST"],
            Literal["PUT"],
            Literal["DELETE"],
        ],
        url: str,
        api_key_title: str = "X-MBX-APIKEY",
        params: dict | None = None,
        data: dict | None = None,
        headers: dict | None = None,
    ) -> dict | None:
        """
        Make a call to the Binance API.
        """
        return super().call(
            method = method,
            url = url,
            api_key_title = api_key_title,
            params = params,
            data = data,
            headers = headers,
        )
