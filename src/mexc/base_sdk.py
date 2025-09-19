# Built in libraries
from urllib.parse import urlencode
from typing import Optional, Union, Literal

# Custom libraries
from sdk.base_sdk import CommonBaseSDK


class FutureBase(CommonBaseSDK):
    """
    Class for Base SDK for MEXC APIs including SpotV3, Spot V2, Futures V1 and so on
    SDK for MEXC API, inheriting from CommonBaseAPI.
    """
    def __init__(
        self,
        api_key: Optional[str] = None,
        secret_key: Optional[str] = None,
        base_url: str = "https://contract.mexc.com",
    ):
        super().__init__(
            api_key = api_key,
            secret_key = secret_key,
            base_url = base_url,
        )
        # Set the specific content type for MEXC
        self.set_content_type("application/json")

    def generate_signature(
        self,
        query_string: str,
    ) -> str:
        """
        Generate the signature for MEXC API.
        """
        return super().generate_signature(
            query_string = query_string,
        )

    def call(
        self: "FutureBase",
        method: Union[
            Literal["GET"],
            Literal["POST"],
            Literal["PUT"],
            Literal["DELETE"],
        ],
        url: str,
        api_key_title: str = "ApiKey",
        params: dict | None = None,
        data: dict | None = None,
        headers: dict | None = None,
    ) -> dict | None:
        """
        Make a call to the MEXC API.
        """
        return super().call(
            method = method,
            url = url,
            api_key_title = api_key_title,
            params = params,
            data = data,
            headers = headers,
        )
