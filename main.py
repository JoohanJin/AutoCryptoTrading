import requests
import json

endpoint: str = "https://api.mexc.com"

test_connect: str = "/api/v3/ping"
test_server_time: str = "/api/v3/time"

URL = f"{endpoint}/api/v3/depth"
response = requests.get(URL)

with open("config.json") as f:
    config = json.load(f)
    mexc_key = config['mexc']

access_key = mexc_key["access_key"]
secret_key = mexc_key["secret_key"]
auth_string = f"{access_key}:{secret_key}"

if (response.status_code != 200):
    print(response.status_code)
else:
    decoded_response = response.text
    print(
        json.loads(
            decoded_response
        )
    )