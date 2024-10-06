import requests
import hmac
import hashlib
from urllib.parse import urlencode
import logging
import time
import logging
import json
from typing import Union, Literal


'''
Class for Base SDK for MEXC APIs including SpotV3, Spot V2, Futures V1 and so on
'''
class _MexCBase():
    '''
    Function Name: __init__

    Initializes a new instance of the class with the given "apiKey" and "secretKey"

    parameters
    ::api_key: str, personal api_key
    ::secret_key: str, personal api_secret key
    ::base_url: str, base endpoint for each API
    ::proxies
    '''
    def __init__(
            self,
            api_key: str,
            secret_key: str,
            base_url: str,
            # proxies: dict = None
    ) -> None:
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
        
        # if (proxies):
        #     self.session.proxies.update(proxies)


class FutureBase(_MexCBase):
    def __init__(
            self,
            api_key: str = None,
            secret_key: str = None,
            # proxies: dict = None,
        ) -> None:
        '''
        Function Name: __init__

        Initializes a new instance for the class with the given "apiKey" and "secretKey"

        Parameters:
            # api_key: str, personal api_key
            # secret_key: str, personal api_secret_key
            # base_url: str, base endpoint for each API
            # proxies
        '''
        super().__init__(
            api_key=api_key,
            secret_key=secret_key,
            base_url="https://contract.mexc.com",
            # proxies=proxies,
        )

        self.session.headers.update(
            {
            "Content-Type": "application/json",
            "ApiKey": self.api_key
            }
        )
    

    def generate_signature_get_del(self, timestamp: str, **kwargs) -> str:
        '''
        Function Name: generate_signature_get_del()

        Generates a signature for an API request using HMAC SHA256 encryption.

        Parameters
        ::timestamp: str, timestamp in ms of the request.
        ::**kwargs: dict, arbitrary keyword arguments representing request parameters.
        '''
        # generating signature
        query: str = "&".join(f"{x}={y}" for x, y in sorted(kwargs.items()))
        query_string: str = self.api_key + timestamp + query
        
        return hmac.new(self.secret_key.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256).hexdigest()
    

    def generate_signature_post(self, timestamp: str, param) -> str:
        query: str = param
        query_string: str = self.api_key + timestamp + query

        return hmac.new(self.secret_key.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256).hexdigest()
    

    def call(
        self,
        method: Union[
            Literal["GET"],
            Literal["POST"],
            Literal["PUT"],
            Literal["DELETE"]
        ],
        url: str,
        *args,
        **kwargs
    ):
        '''
        # MEXC place/cancel Order Endpoint is under maintanence, 
        
        Function Name: call()

        The function makes a request to the given url using the specified method and args.

        Parameters
            # method: str, should be one of following elements:
                - GET
                - POST
                - PUT
                - DELETE
            # url: str
            # *args: list, arbitrary arguments representing request parameters.
            # **kwagrs: dict, arbitrary keyword representing request parameters.
        '''
        if (not url.startswith("/")):
            url = f"/{url}"
        
        # remove the elements if there is no corresponding value
        kwargs = {x:y for x, y in kwargs.items() if y}

        # generating epoch timestamp generator for order
        timestamp: str = str(int(time.time() * 1000))

        for i in ('params', 'json'):
            if kwargs.get(i):
                kwargs[i] = {x:y for x,y in kwargs[i].items() if y}
                if self.api_key and self.secret_key:
                    kwargs['headers'] = {
                        "Request-Time": timestamp,
                        "Signature": self.generate_signature_get_del(timestamp, **kwargs[i])
                    }
            elif not kwargs.get('headers') and i == "json":
                if self.api_key and self.secret_key:
                    kwargs['headers'] = {
                        "Request-Time": timestamp,
                        "Signature": self.generate_signature_get_del(timestamp)
                    }
        
        # send the request to the endpoint to make the order
        response = self.session.request(method, f"{self.base_url}{url}", *args, **kwargs)
        return response.json()