from future import *
import json
import threading



# initialize
f = open('config.json')
data = json.load(f)
api_key: str = data['api_key']
secret_key: str = data['secret_key']

future_client = FutureMarket(api_key=api_key, secret_key=secret_key)

data = future_client.history_position()
print(data)