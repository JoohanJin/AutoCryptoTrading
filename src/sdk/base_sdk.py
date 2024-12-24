import requests
import hmac
import hashlib
from urllib.parse import urlencode
import logging
import time
import logging
from typing import Union, Literal, Optional

logger = logging.getLogger('__name__')

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
        self.session.headers.update({
            "Content-Type": content_type,
        })

    def generate_signature(
        self,
        query_string: str,
    ) -> str:
        """
        Generate an HMAC SHA256 signature. Child classes can override this if needed.
        """
        if not self.secret_key:
            raise ValueError("Secret key is required for signature generation.")

        return hmac.new(
            self.secret_key.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
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
    ):
        """
        Make a generic API call with the specified method, URL, and parameters.
        """
        # Ensure the URL starts with "/"
        if not url.startswith("/"):
            url = f"/{url}"

        # Generate timestamp
        timestamp = str(int(time.time() * 1000))

        # Prepare query string for signature
        query_string = ""
        if params:
            params = {k: v for k, v in params.items() if v is not None}
            query_string = "&".join(f"{k}={v}" for k, v in sorted(params.items()))

        # Add signature if API key and secret key are provided
        if self.api_key and self.secret_key:
            if headers is None:
                headers = {}
            headers.update({
                "Request-Time": timestamp,
                "Signature": self.generate_signature(query_string=query_string),
            })

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