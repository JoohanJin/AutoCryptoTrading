import requests
import hmac
import hashlib
from urllib.parse import urlencode
import logging
import time
import logging
import json
from typing import Union, Literal, Optional

logger = logging.getLogger('__name__')

class _BinanceFutureSdk:
    def __init__(
        self,
        api_key: Optional[str] = None,
        secret_key: Optional[str] = None,
        base_url: str = "https://fapi.binanace.com"
    ):
        # authentification credintial
        self.api_key = api_key
        self.secret_key = secret_key

        self.base_url = base_url

        self.session = requests.Session()
        self.session.headers.update(
            {
                "Content-Type": "application/x-www-form-urlencoded",
            }
        )
        return
    
    def generate_signature(
        self,
        timestamp: str,
        **kwargs,
    ):
        query: str = "&".join(f"{key}={val}" for key, val in sorted(kwargs.items()))
        query_string: str = self.api_key + timestamp + query

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
        url: Optional[str] = None,
        *args,
        **kwargs,
    ):
        # string exception handler
        if (not url.startswith("/")):
            url = '/' + url

        kwargs = {key: val for key, val in kwargs.items() if val}

        timestamp: str = str(int(time.time() * 1000))

        if kwargs.get('params'):
            kwargs['params'] = {key: val for key, val in kwargs['params'].items() if val}
            if self.api_key and self.secret_key:
                kwargs['headers'] = {
                    "Request-Time": timestamp,
                    "Signature": self.generate_signature(
                        timestamp=timestamp,
                        **kwargs['params']
                    )
                }

        response = self.session.request(method, f"{self.base_url}{url}", *args, **kwargs)
        return response.json()