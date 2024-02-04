import requests
import hmac
import hashlib
from urllib.parse import urlencode
import logging
import time
import logging
import json
from typing import Union, Literal

logger = logging.getLogger("__name__")


'''
Class for Base SDK for MEXC APIs including Spot V3, Spot V2, Futures V1 and so on
'''
class MEXCBASE():
    '''
    Function Name: __init__

    Initializes a new instance of the class with the given "apiKey" and "secretKey"

    parameters
    ::api_key: str, personal api_key
    ::secret_key: str, personal api_secret key
    ::base_url: str, base endpoint for each API
    ::proxies
    '''
    def __init__(self, api_key: str, secret_key: str, base_url: str, proxies: dict = None):
        self.api_key = api_key
        self.secret_key = secret_key

        self.recvWindow = 5000

        self.base_url = base_url

        self.session = requests.Session()
        self.session.headers.update(
            {
                "Content-Type": "application/json"
            }
        )
        
        if (proxies):
            self.session.proxies.update(proxies)


class FutureBase(MEXCBASE):
    '''
    Function Name: __init__

    Initializes a new instance for the class with the given "apiKey" and "secretKey"

    Parameters:
        # api_key: str, personal api_key
        # secret_key: str, personal api_secret_key
        # base_url: str, base endpoint for each API
        # proxies
    '''
    def __init__(self, api_key: str = None, secret_key: str = None, proxies: dict = None):
        super().__init__(api_key=api_key, secret_key=secret_key, base_url="https://contract.mexc.com", proxies=proxies)

        self.session.headers.update({
            "Content-Type": "application/json",
            "ApiKey": self.api_key
        })
    

    '''
    Function Name: generate_signature()

    Generates a signature for an API request using HMAC SHA256 encryption.

    Parameters
    ::timestamp: str, timestamp in ms of the request.
    ::**kwargs: dict, arbitrary keyword arguments representing request parameters.
    '''
    def generate_signature(self, timestamp: str, **kwagrs):
        # generating signature
        query: str = "&".join(f"{x}={y}" for x, y in sorted(kwagrs.items()))
        query_string = self.api_key + timestamp + query
        
        return hmac.new(self.secret_key.encode("utf-8"), query.encode("utf-8"), hashlib.sha256).hexdigest()
    

    '''
    Function Name: call()

    The function makes a request to the given url using the specified method and args.

    Parameters
        # method: str, should be one of elements in the following:
            - GET
            - POST
            - PUT
            - DELETE
        # url: str
        # *args: list, arbitrary arguments representing request parameters.
        # **kwagrs: dict, arbitrary keyword representing request parameters.

    '''
    def call(self, method: Union[Literal["GET"], Literal["POST"], Literal["PUT"], Literal["DELETE"]], url: str, *args, **kwagrs):
        if (not url.startswith("/")):
            url = f"/{url}"
        
        kwagrs = {x:y for x, y in kwagrs.items() if y is not None}

        for i in ('params', 'json'):
            if kwagrs.get(i):
                kwagrs[i] = {x:y for x,y in kwagrs[i].items if y is not None}

                if self.api_key and self.secret_key:
                    timestamp: str = str(int(time.time() * 1000))

                    kwagrs[i] = {
                        "Request-Time": timestamp,
                        "Signature": self.generate_signature(timestamp, **kwagrs[i])
                    }

        response: str = self.session.request(method, f"{self.base_url}{url}", *args, **kwagrs)
        return response.json()