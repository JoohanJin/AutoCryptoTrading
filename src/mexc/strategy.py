import numpy as np
import pandas as pd
import time
import asyncio

# from future import WebSocket
import threading
import websocket


def ping_loop(
    ws,
    ping_interval: int = 20,
    ping_payload: str = '{"method":"ping"}'
):
    while True:
        time.sleep(ping_interval)
        ws.send(ping_payload)


test_ws = websocket.WebSocket()

test_ws.connect("wss://contract.mexc.com/edge")

# thread for connect
wsp = threading.Thread(
    target = lambda: ping_loop(
        ws=test_ws,
        ping_interval=20,
    )
)
wsp.daemon = True # background Thread
wsp.start()

test_ws.send(
    '{"method":"sub.ticker", "param":{"symbol":"BTC_USDT"}}'
)

# test = webSocket()
# df = pd.DataFrame()
# # df.set_index("ts")

cnt: int = 0
def update_df(msg):
    global df
    data = msg.get("data")
    data["ts"] = msg.get("ts")
    tmp = pd.DataFrame([data])
    tmp = tmp.set_index("ts")
    df = pd.concat([df, tmp], ignore_index = False)

def print_msg(msg):
    print(msg.get("channel"))
    print(msg.get("data"))

async def print_df():
    global df
    await update_df
    print(df)


if __name__ == "__main__":
    while True:
        response = test_ws.recv()
        print(response)
    test_ws.close()