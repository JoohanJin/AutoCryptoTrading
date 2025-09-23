# Built in libraries
from urllib.parse import urlencode
from typing import Optional, Union, Literal

# Custom libraries
from sdk.base_sdk import CommonBaseSDK
from logger.set_logger import operation_logger


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
        # Ensure the URL starts with "/"
        if not url.startswith("/"):
            url = f"/{url}"

        timestamp: int = FutureBase.generate_timestmap()

        if params is not None:
            params = {key: value for key, value in params.items() if value is not None}
            query_string = "&".join(f"{key}={value}" for key, value in sorted(params.items()))
        else:
            query_string: str = ""

        query_string = f"{self.api_key}{timestamp}{query_string}"

        # apiKey in header
        if self.api_key and self.secret_key:  # menas it is signed instance.
            if headers is None:
                headers = {
                    "Request-Time": str(timestamp),
                    api_key_title: self.api_key,
                    "Signature": self.generate_signature(query_string),
                }
            else:
                headers.update(
                    {
                        api_key_title: self.api_key,
                        "Request-Time": str(timestamp),
                        "Signature": self.generate_signature(query_string),
                    }
                )

        request = self.session.request(
            method = method,
            url = f"{self.base_url}{url}",
            params = params,
            headers = headers,
            json = data,
        )

        try:
            return request.json()
        except ValueError:
            request.raise_for_status()
        except Exception as e:
            operation_logger.critical(f"{__name__} - Unknown Exception: {str(e)}")
