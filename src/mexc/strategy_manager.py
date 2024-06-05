# Standard Module
import time
import asyncio
from typing import Literal, Optional
import pandas as pd
import numpy as np
import threading

# Custom Module
from future import WebSocket

class strategyManager:
    def __init__(
        self,
        ws_name: Optional[str],
        # provide the list of strategy?
    ) -> None:
        # it will automatically connect the websocket to the host
        # and will continue to keep the connection between the client and host
        # no need to login, no need to provide api_key and secret_key
        self.ws = WebSocket(
            ws_name = ws_name,
        )




        
        
        return