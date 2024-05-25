"""
this script is for testing websocket connetion with the host, i.e. MexC Websocket API endpoint
"""

import websocket
import json
import time
import hmac
import hashlib
from threading import Thread


def on_message(wsapp, message):
    m = json.loads(message)
    print(m)

link = "wss://contract.mexc.com/edge"
ws = websocket.create_connection(link)


def ping():
    query = dict(
        method = "ping"
    )
    header = json.dumps(query)

    ws.send(header)
    re = ws.recv()
    print(re)
    ws.close()

def ticker(ws):
    symbol = "BTC_USDT"
    query = dict(
        method = "sub.ticker",
        param = dict(
            symbol = symbol
        ),
        gzip = False
    )
    header = json.dumps(query)
    ws.send(header)
    print("sub to rs.ticker")
    return


def ping_loop(
        wsa,
        ping_payload: str = '{"method":"ping"}',
        ping_interval = 30
    ):
    time.sleep(ping_interval)
    while True:
        wsa.send(ping_payload)
        time.sleep(ping_interval)


def connect():
    ws = websocket.WebSocketApp(link, on_message=on_message)
    wst = Thread(target=lambda: ws.run_forever(
        ping_interval=30,
        ))
    wst.daemon = True
    wst.start()

    wsl = Thread(
        target=lambda: ping_loop(
            ws,
            '{"method":"ping"}',
            30
        )
    )
    wsl.daemon = True
    wsl.start()

    conn_timeout = 30
    while (not ws.sock or not ws.sock.connected) and conn_timeout:
        time.sleep(1)
        conn_timeout -= 1
    
    if not conn_timeout:
        print("connection timeout")
        return

    print("connection succeed")
    login(ws)

    ticker(ws)
    try:
        input()
        ws.close()
    except KeyboardInterrupt:
        ws.close()
    return


def login(ws):
    """
    signature target string: accessKey + timestamp -> hmac sha256 algo
    """    
    timestamp = str(int(time.time() * 1000))
    _signature = api_key + timestamp

    signature = hmac.new(
        secret_key.encode("utf-8"),
        _signature.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

    query = dict(
        method = "login",
        param = dict(
            apiKey=api_key,
            reqTime=timestamp,
            signature=signature
        )
    )

    header = json.dumps(query)

    ws.send(header)
    # re = ws.recv()
    # print(re)
    # ws.close()

def filter():
    return

def main():
    try:
        login()

        while True:
            break

        ws.close()
    except KeyboardInterrupt:
        ws.close()
    

if __name__ == "__main__":
    connect()
    
