"""
Future Trade API
Documentation: https://mexcdevelop.github.io/apidocs/contract_v1_en/?python#access-to-url
"""

import logging
from typing import Optional

logger = logging.getLogger(__name__)

try:
    from base_sdk import FutureBase
except:
    from .base_sdk import FutureBase


# no need to authenticate
class FutureMarket(FutureBase):
    """
    Function Name: ping

    Parameters: None

    Task: Get The Server Time

    Rate Limit: 20 times / 2 seconds

    Documentation:
        https://mexcdevelop.github.io/apidocs/contract_v1_en/?python#get-the-server-time
    """
    def ping(self) -> dict:
        url: str = "api/v1/contract/support_currencies"
        return self.call('GET', url)
    
    """
    Function Name: detail

    Parameters:
        # symbol: str [optional], the name of the contract

    Task: Get the contract information

    Rate Limit: 1 times / 5 seconds
    
    Documentation:
        https://mexcdevelop.github.io/apidocs/contract_v1_en/?python#get-the-contract-information
    """    
    def detail(self, symbol: Optional[str] = None) -> dict:
        url: str = "api/v1/contract/detail"
        return self.call("GET", url, parmas = dict(
            symbol= symbol
        ))


    """
    Function Name: support_currencies

    Parameters: None

    Task:
        # Get the transferable currencies
        # The returned "data" field contains a list of string with each string represents a supported currencies

    Rate Limit: 20 times / 2 seconds

    Documentation:
        https://mexcdevelop.github.io/apidocs/contract_v1_en/?python#get-the-transferable-currencies
    """
    def support_currencies(self):
        url: str = "/api/v1/contract/support_currencies"
        return self.call("GET", url)


# need to authenticate, i.e., need to have apiKey and secretKey
class FutureAccountingTrading:
    def __init__(self):
        pass     