### Trading Bots
##### TODO:
- It implements the signal generator with the simple indicators and strategies.

##### Programming Convention

##### Main Brokers: MexC API
- [MexC Documentation](https://github.com/mexcdevelop/mexc-api-sdk/blob/main/test/python/trades.py)

##### Automated Bitcoin Trading Bot
- Basic Structgure
- Order-Analysis Basic Logic
    - MexC APIs

    - TradingView APIs

    - Trading Algorithm
        - Multiple Technical Analysis Indicators for comprehensive trading decision making.
    - Machine Learning
    - Large-Language Model (LLM)
    - Data Preprocessing
    - High Frequency Trading (?)

### Rough Trading Stratgey
- Entry/Exit Position
    - Bullish Market
        - Long Position
            - PT: 15%
            - SL: -5%
        - Short Position
            - PT: 10%
            - SL: -5%
    - Bearish Market
        - Long Position
            - PT: 10%
            - SL: -5%
        - Short Position
            - PT: 15%
            - SL: -5%

- Risk Management
    - Tight SL position
        - -5%
        - Considering the high leverage.
    - Position Size Algorithm
    - Trailing Stop Strategies
- Profit Targets?
- Multiple Technical Anlysis Indicator: To be decided.

##### How to run the code in parallel computation manner?
- Threading
- Lock-Free Implementation for shared memory.

##### Computation Logic
- Fetching Market Data
    - Price
        - WebSocket API to fetch the data regularly.
    - Indicator
        - MexC does not have the indicator data
- Analyzing
    - Start from simple, more sophisticated method would be available as I go through the development process.

##### Telegram Notification Function
- [Telegram Bot API example](https://github.com/freqtrade/freqtrade/blob/develop/docs/telegram-usage.md)
- Already has been developed. -> already passed the test which has been conducted.