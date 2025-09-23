import requests
import hmac
import hashlib
import time
from typing import Union, Literal
from abc import ABC, abstractmethod


class CommonBaseSDK(ABC):
    """
    A common base class for handling API requests, signature generation, and session management
    for different exchange SDKs (e.g., MEXC and Binance).
    """
    @staticmethod
    def generate_timestmap() -> int:
        return int(time.time() * 1_000)

    def __init__(
        self: "CommonBaseSDK",
        base_url: str,
        api_key: str | None = None,
        secret_key: str | None = None,
    ):
        self.api_key = api_key
        self.secret_key = secret_key
        self.base_url = base_url

        # Initialize a session
        self.session = requests.Session()

    def set_content_type(self: "CommonBaseSDK", content_type: str):
        """
        Set the Content-Type header for the session.
        """
        self.session.headers.update(
            {
                "Content-Type": content_type,
            }
        )

    def generate_signature(
        self: "CommonBaseSDK",
        query_string: str,
    ) -> str:
        """
        fucn generate_signature:
            - Generate a signature for the request using HMAC SHA256.
            - This is used for authentication with the API.
            - Child classes would override this method if needed.

        param query_string:
        - The query string to be signed.

        return: The generated signature as a hex digest (readable string).
            - if we do not disgest using hexdigest, the signature will be a hmac object.
        """
        if not self.secret_key:
            raise ValueError("Secret key is required for signature generation.")

        return hmac.new(
            key = self.secret_key.encode("utf-8"),
            msg = query_string.encode("utf-8"),
            digestmod = hashlib.sha256,
        ).hexdigest()

    @abstractmethod
    def call(
        self: "CommonBaseSDK",
        method: Union[
            Literal["GET"],
            Literal["POST"],
            Literal["PUT"],
            Literal["DELETE"],
        ],
        url: str,
        api_key_title: str,
        params: dict | None = None,
        data: dict | None = None,
        headers: dict | None = None,
    ) -> dict | None:
        """
        func call:
            - Make a generic API call with the specified method, URL, and parameters.
            - Automatically handles signature generation and timestamping.
            - Returns the JSON response from the API.

        param method: HTTP method (GET, POST, PUT, DELETE)
        param url: API endpoint URL (should start with "/")
        param params: Query parameters for the request
        param data: JSON body for the request
        param headers: Additional headers for the request

        return: JSON response from the API
        """
        return
