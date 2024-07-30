'''
For Strategy Manager for the Auto-Trading Bot, the MexC websocket api will be used for
continous data fetching to establish the trading strategy.
'''

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
        ws_name: Optional[str] = "strategyManager", # no need to authenticate
        # provide the list of strategy as variable
        # so that it can subscribe different values at the initiation.
    ) -> None:
        # it will automatically connect the websocket to the host
        # and will continue to keep the connection between the client and host
        # no need to login, no need to provide api_key and secret_key
        self.ws = future.WebSocket();

        time.sleep(1);

        self.ws.ticker(
            callback=self.put_data_buffer
        );

        # multi-thrading based queue
        # used as a buffer for data fetching from the MEXC Endpoint
        self.q = Queue();

        # mutex lock
        self.df_lock = threading.Lock();

        # default dataframe with the given columns
        # initalize the dataframe with the given columns while there is not content
        self.data_frame = pd.DataFrame(
            columns = [
                'symbol',
                'lastPrice',
                'riseFallRate',
                'fairPrice',
                'indexPrice',
                # 'volume24',
                # 'amount24',
                # 'maxBidPrice',
                # 'minAskPrice',
                # 'lower24Price',
                # 'high24Price',
                # 'bid1',
                # 'ask1',
                # 'holdVol',
                # 'riseFallValue',
                # 'fundingRate',
                # 'zone',
                # 'riseFallRates',
                # 'riseFallRatesOfTimezone',
            ]
        );

        # start the thread for the data fetch from the API
        threading.Thread(target=self.append_df, daemon=True).start();
        threading.Thread(target=self.calculate_ema, daemon=True).start();

        return
    
    def put_data_buffer(
        self,
        msg,
    ) -> None:
        self.q.put(msg.get('data'), block=False, timeout=None)
        return
    
    def get_data_buffer(self) -> dict:
        if (self.q.not_empty):
            result = self.q.get();
            self.q.task_done();
            return result;
        else:
            return;

    def append_df(self) -> None:
        '''

        '''
        while True:
            print("append_df")
            response = self.get_data_buffer();
            if (response):
                # TODO: store 'riseFallRates' and 'riseFallRatesTimezone'
                timestamp = response['timestamp'];
                for key in ['timestamp', 'volume24', 'amount24', 'fundingRate', "zone", 'riseFallRates', 'riseFallRatesOfTimezone', 'maxBidPrice', 'minAskPrice', 'lower24Price', 'high24Price', 'bid1', 'ask1', 'holdVol', 'riseFallValue']:
                    response.pop(key);

                # edit self.data_frame: i.e. concat
                self.df_lock.acquire();

                self.data_frame.loc[timestamp] = response;

                self.df_lock.release();
            else:
                # just ignore if the response returned is None
                pass ;

        return;
    
    def calculate_ema(self):
        while True:
            print("ema")
            self.df_lock.acquire();
            
            if (len(self.data_frame) < 9):
                self.df_lock.release();
                pass;
            else:
                self.data_frame['EMA_9'] = self.data_frame.iloc[-1]['lastPrice'].ewm(span=9, adjust=False).mean();
                print(self.data_frame.iloc[-1]['EMA_9']);

                self.df_lock.release();
        return;


if __name__ == "__main__":
    test = strategyManager();