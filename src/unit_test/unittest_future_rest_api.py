import sys
import os

import unittest
from typing import Tuple
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import mexc.future as future


def get_keys() -> Tuple[str, str]:
    try:
        with open("/src/mexc/keys.json", "r") as f:
            data = json.load(f)
        api_key: str = data.get("api_key")
        secret_key: str = data.get("secret_key")

        return api_key, secret_key

    except FileNotFoundError:
        print("The file containing keys for MexC broker has not been found")
        return None, None


api_key, secret_key = get_keys()
future_market = future.FutureMarket(
    api_key=api_key,
    secret_key=secret_key,
)


class unittest_FutureMarket(unittest.TestCase):
    '''
    #################################################################################
    #                               PUBLIC ENDPOINT                                 #
    #################################################################################
    '''
    def test_ping(self):
        response = future_market.ping()
        self.assertTrue(response["success"])
        return

    def test_detail(self):
        response = future_market.detail()
        self.assertTrue(response["success"])
        return

    def test_support_currencies(self):
        response = future_market.support_currencies()
        self.assertTrue(response["success"])
        return

    def test_depth(self):
        response = future_market.depth()
        self.assertTrue(response["success"])
        return

    def test_depth_commits(self):
        response = future_market.depth_commits()
        self.assertTrue(response["success"])
        return

    def test_index_price(self):
        response = future_market.index_price()
        self.assertTrue(response["success"])
        return

    def test_fair_price(self):
        response = future_market.fair_price()
        self.assertTrue(response["success"])
        return

    def test_funding_rate(self):
        response = future_market.funding_rate()
        self.assertTrue(response["success"])

    def test_kline(self):
        response = future_market.kline()
        self.assertTrue(response["success"])
        return

    def test_kline_index_price(self):
        response = future_market.kline_index_price()
        self.assertTrue(response["success"])
        return

    def kline_fair_price(self):
        response = future_market.kline_fair_price()
        self.assertTrue(response["success"])
        return

    def test_deals(self):
        response = future_market.deals()
        self.assertTrue(response["success"])
        return

    def test_ticker(self):
        response = future_market.ticker()
        self.assertTrue(response["success"])
        return

    def test_risk_reverse(self):
        response = future_market.risk_reverse()
        self.assertTrue(response["success"])
        return

    def test_risk_reverse_history(self):
        response = future_market.risk_reverse_history()
        self.assertTrue(response["success"])
        return

    def test_funding_rate_history(self):
        response = future_market.funding_rate_history()
        self.assertTrue(response["success"])
        return

    """
    #################################################################################
    #                               PRIVATE ENDPOINT                                #
    #################################################################################
    """

    def test_assets(self):
        response = future_market.assets()
        self.assertTrue(response["success"])
        return

    def test_history_position(self):
        response = future_market.history_position()
        self.assertTrue(response["success"])
        return

    def test_current_position(self):
        response = future_market.current_position()
        self.assertTrue(response["success"])
        return

    def test_pending_order(self):
        response = future_market.pending_order()
        self.assertTrue(response["success"])
        return

    def test_risk_limit(self):
        response = future_market.risk_limit()
        self.assertTrue(response.get("success"))
        return

    def test_fee_rate(self):
        response = future_market.fee_rate()
        self.assertTrue(response.get("success"))
        return


if __name__ == "__main__":
    unittest.main()
