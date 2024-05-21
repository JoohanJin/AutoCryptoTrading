from future import *
import json
import threading

# mx0vglMYg2KNBCmNsY
# 7240f9002fe44806ab41d10b791debde

# initialize
f = open('config.json')
data = json.load(f)
api_key: str = data['api_key']
secret_key: str = data['secret_key']

future_client = FutureMarket(api_key=api_key, secret_key=secret_key)

data = future_client.index_price("BTC_USDT")
print(data['data'])