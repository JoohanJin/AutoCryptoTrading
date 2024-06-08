# Standard Module
import time
import asyncio
from typing import Literal, Optional
import pandas as pd
import numpy as np
import threading
from queue import Queue

# Custom Module
from mexc import future

class strategyManager:
    def __init__(
        self,
        ws_name: Optional[str] = "test_strategy_manager",
        # provide the list of strategy?
    ) -> None:
        # it will automatically connect the websocket to the host
        # and will continue to keep the connection between the client and host
        # no need to login, no need to provide api_key and secret_key
        self.ws = future.WebSocket()

        time.sleep(1)

        self.ws.ticker(
            callback=self.put_data_buffer
        )

        # multi-thrading based queue
        self.q = Queue()

        # mutex lock
        self.df_lock = threading.Lock()

        self.dataFrame = pd.DataFrame(
            columns = [
                'symbol',
                'lastPrice',
                'riseFallRate',
                'fairPrice',
                'indexPRice',
                'volume24',
                'amoun24',
                'maxBidPrice',
                'minAskPrice',
                'lower24Price',
                'high24Price',
                'timestamp',
                'bid1',
                'ask1',
                'holdVol',
                'riseFallValue',
                # 'fundingRate',
                # 'zone',
                # 'riseFallRates',
                # 'riseFallRatesOfTimezone',
            ]
        )

        threading.Thread(target=self.append_df, daemon=True).start()

        return
    
    def put_data_buffer(
        self,
        msg,
    ) -> None:
        self.q.put(msg.get('data'), block=False, timeout=None)
        return
    
    def get_data_buffer(self) -> dict:
        if (self.q.not_empty):
            result = self.q.get()
            self.q.task_done()
            return result

    def append_df(self) -> None:
        while True:
            response = self.get_data_buffer()
            if response:
                # TODO: store 'riseFallRates' and 'riseFallRatesTimezone'

                timestamp = response.pop('timestamp')
                riseFallRates = response.pop('riseFallRates')
                riseFallRatesOfTimezone = response.pop('riseFallRatesOfTimezone')
                fundingRate = response.pop('fundingRate')
                time_zone = response.pop('zone')

                tmp = pd.DataFrame(
                    response,
                    index = [timestamp]
                )

                # edit self.dataFrame: i.e. concat
                self.df_lock.acquire()
                self.dataFrame=pd.concat([self.dataFrame, tmp], axis=0)
                self.df_lock.release()
            else:
                pass

        return