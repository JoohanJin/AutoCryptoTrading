# Standard Library
from typing import Union, Literal
import json

# Custom Library
from logger.set_logger import operation_logger
from sdk.base_sdk import CommonBaseSDK


class FutureBase(CommonBaseSDK):
    """
    SDK for Binance Futures API, inheriting from CommonBaseAPI.
    """
    def __init__(
        self: "FutureBase",
        base_url: str = "https://fapi.binance.com",
        api_key: str | None = None,
        secret_key: str | None = None,
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
        # Ensure the URL starts with "/"
        if not url.startswith("/"):
            url = f"/{url}"

        if params is not None:
            params = {key: value for key, value in params.items() if value is not None}
            query_string = "&".join(f"{key}={value}" for key, value in sorted(params.items()))
        else:
            query_string: str = ""

        query_string = f"{query_string}"

        # apiKey in header
        if self.api_key and self.secret_key:  # menas it is signed instance.
            if headers is not None:
                headers.update(
                    {
                        api_key_title: self.api_key,
                    }
                )
            else:
                headers = {
                    api_key_title: self.api_key,
                }

            signature: str = self.generate_signature(query_string)
            if params is not None:
                params.update(
                    {
                        "signature": signature,
                    }
                )
            else:
                params = dict(
                    signature = signature,
                )

        request = self.session.request(
            url = f"{self.base_url}{url}",
            method = method,
            params = params,
            headers = headers,
            data = data if data is None else json.dumps(data),
        )

        try:
            return request.json()
        except ValueError:
            request.raise_for_status()
        except Exception as e:
            operation_logger.critical(f"{__name__} - Unknown Exception: {str(e)}")
