import requests
import hmac
import hashlib
import time
from typing import Union, Literal, Optional

# from logger.set_logger import operation_logger


class CommonBaseSDK:
    """
    A common base class for handling API requests, signature generation, and session management
    for different exchange SDKs (e.g., MEXC and Binance).
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        secret_key: Optional[str] = None,
        base_url: str = "",
    ):
        self.api_key = api_key
        self.secret_key = secret_key
        self.base_url = base_url

        # Initialize a session
        self.session = requests.Session()

    def set_content_type(self, content_type: str):
        """
        Set the Content-Type header for the session.
        """
        self.session.headers.update(
            {
                "Content-Type": content_type,
            }
        )

    def generate_signature(
        self,
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
            self.secret_key.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

    def call(
        self,
        method: Union[
            Literal["GET"],
            Literal["POST"],
            Literal["PUT"],
            Literal["DELETE"],
        ],
        url: str,
        params: Optional[dict] = None,
        data: Optional[dict] = None,
        headers: Optional[dict] = None,
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
        # Ensure the URL starts with "/"
        if not url.startswith("/"):
            url = f"/{url}"

        # Generate timestamp
        timestamp: str = str(int(time.time() * 1000))

        # Prepare query string for signature
        query_string: str = ""
        if params:
            params = {k: v for k, v in params.items() if v is not None}
            query_string = "&".join(f"{k}={v}" for k, v in sorted(params.items()))

        query_string = f"{self.api_key}{timestamp}{query_string}"

        # Add signature if API key and secret key are provided
        if self.api_key and self.secret_key:
            if headers is None:
                headers = {}

            headers.update(
                {
                    "Request-Time": timestamp,
                    "Signature": self.generate_signature(query_string=query_string),
                },
            )

        # Add API key to headers if needed
        if self.api_key:
            headers["ApiKey"] = self.api_key

        # Perform the request
        response = self.session.request(
            method=method,
            url=f"{self.base_url}{url}",
            params=params,
            json=data,
            headers=headers,
        )

        # Ensure a JSON response is returned
        try:
            return response.json()
        except ValueError:
            response.raise_for_status()
