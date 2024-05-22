from future import *
import json
import threading


# initialize
f = open('config.json')
data = json.load(f)
api_key: str = data['api_key']
secret_key: str = data['secret_key']

# define client
future_client = FutureMarket(api_key=api_key, secret_key=secret_key)


# re = future_client.risk_limit()
# print(re)

def calculate_vol():
    re = future_client.asset()
    volume = re['data']['availableBalance'] * 0.1
    return volume



if __name__ == "__main__":
    amount: float = calculate_vol()

