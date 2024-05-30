import numpy as np
import pandas as pd
import time
import asyncio

from future import webSocket

test = webSocket()
df = pd.DataFrame()
# df.set_index("ts")

cnt: int = 0
def update_df(msg):
    global df
    data = msg.get("data")
    data["ts"] = msg.get("ts")
    tmp = pd.DataFrame([data])
    tmp = tmp.set_index("ts")
    df = pd.concat([df, tmp], ignore_index = False)

async def print_df():
    global df
    await update_df
    print(df)


time.sleep(0.3)

test.ticker(
    callback=update_df
)

while True:
    # print_df()
    # time.sleep(2)
    # pass
    asyncio.run(print_df())
    # print(df)
    # time.sleep(2)