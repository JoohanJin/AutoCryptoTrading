# Built in libraries
from urllib.parse import urlencode
import logging
from typing import Union, Literal, Optional

# Custom libraries
from sdk.base_sdk import CommonBaseSDK


class BinanceFutureSDK(CommonBaseSDK):
    """
    SDK for Binance Futures API, inheriting from CommonBaseAPI.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        secret_key: Optional[str] = None,
        base_url: str = "https://fapi.binance.com",
    ):
        super().__init__(
            api_key=api_key,
            secret_key=secret_key,
            base_url=base_url,
        )
        # Set the specific content type for Binance
        self.set_content_type("application/x-www-form-urlencoded")

    def generate_signature(
        self,
        query_string: str,
    ) -> str:
        """
        Generate the signature for Binance API.
        """
        return super().generate_signature(query_string=query_string)
