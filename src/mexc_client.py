'''
PYTHON File for MEXC REST API v3
class and method
'''

import logging
import requests
import json
import sys
import hashlib
import hmac
import time
# import pandas


'''
Class Name: clientBase(object)
Operations:
    - _get_server_time
    - _get_timestamp
    - _sign
    - _open_api
    - _signed_api
Task:
'''
class clientBase(object):
    '''
    function name: __init__
    parameters:
        - access_key: str
        - secret_key:: str
    returned type: void
    task: 
    '''
    # def __init__(self, access_key:str, secret_key:str):
    def __init__(self):
        self._endpoint = "https://api.mexc.com"
        # self._access_key = access_key
        # self._secret_key = secret_key
        # self.session = requests.session()

    '''
    function name: _check_connectivity
    parameters: None
    returned type: bool
    task: return true if the connection can be made, return false otherwise
    '''
    def _check_connectivity(self) -> bool:
        request: requests.models.Response = requests.request("get", f"{self._endpoint}/api/v3/ping")
        if (request.status_code == 200):
            return True
        return False
    
    '''
    function name: _get_server_time
    parameters: None or get the link as param?
    returned type: int 
    task: get the timestamp with ms from the server side (mexc server side)
    '''
    def _get_server_time(self) -> int:
        return int(requests.request('get', f"{self._endpoint}/api/v3/time").json()['serverTime'])

    '''
    function name: _get_timestamp
    parameters: None
    returned type: int
    task: get the local timestamp with ms (in the client)
    '''
    def _get_local_time(self) -> int:
        return int(time.time() * 1000)

    '''
    function name: _sign
    parameters: request_timestamp (int)
    returned type: str (params)
    task: made the header for the request for signed endpoint such as /buy
    '''
    def _sign(self, request_timestamp: int, params: dict = {}):
        if params:
            # TODO: implement the url parsing function
            raise NotImplementedError
        else:
            param = f"timestamp={request_timestamp}"
        return hmac.new(self._secret_key.encode('utf-8'), param.encode('utf-8'), hashlib.sha256).hexdigest()
    
    '''
    function name: _public_api
    parameters:
        - path (str)
        - method (str)
        - params (dict)
    returned type: dict (from requests.model.Request.json() parsing)
    task: access the api that does not require api keys
    '''
    def _public_api(self, path: str, method: str = "get", params: dict = None):
        url: str = f"{self._endpoint}{path}"
        response = requests.request(method=method, url= url, params= params)
        return response.json()
    
    '''
    function name: _signed_api
    parameters:
        - path: str
        - method: str
        - params: dict
    returned type:
    task: access the api that requires api keys
    '''
    def _signed_api(self, path: str, method: str= "get", params: dict = {}):
        requested_time = self._get_server_time()
        if params:
            # params['signature'] = self._sign(timestamp = requested_time, params= params)
            raise NotImplementedError
        else:
            params['signature'] = self._sign(request_timestamp=requested_time)

        params['timestamp'] = requested_time

        headers: dict = {
            "x-mexc-apikey": self._access_key,
            'Content-Type': "application/json"
        }

        return requests.request(method=method, headers=headers, )


'''
'''
class mexcPublicClient(clientBase):
    '''
    function name: __init__
    parameters:
        - inherited from the class, clientBase
            - _endpoint: given that it is a string, "https://api.mexc.com"
            - access_key: a string, api access key
            - secret_key: a string, api secret key 
        - 
    '''
    def __init__(self):
        # super().__init__()
        self._endpoint = "https://api.mexc.com"
        self.api_prefix: str = "/api/v3"
        self.method = "get"


'''
'''
class mexcSignedClient(clientBase):
    def __init__(self, method: str = "get"):
        self._endpoint = "https://api.mexc.com"
        self.api_prefix: str = "/api/v3"
        self._method = method
