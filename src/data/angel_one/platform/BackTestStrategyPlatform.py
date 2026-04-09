
from datetime import datetime
from typing import Optional
from av_core.logger import LoggerConfig
from data.angel_one.utils.app import AngelOneSmartApp
from strats.BaseStrat import BaseStrategy, OHLCQuote

class BackTestStrategyPlatform(AngelOneSmartApp):
    def __init__(self, config_file: Optional[str] = None, log_file: Optional[str] = None, instance_name: str = ""):
        AngelOneSmartApp.__init__(self, config_file=config_file, log_file=log_file, instance_name=instance_name)
        self.strats = []

    def add_strat(self, strat):
        self.strats.append(strat)

    def set_backtest_data_params(self, symbols, start_date, end_date, interval):
        self.symbols = symbols
        self.start_date = start_date
        self.end_date = end_date
        self.interval = interval
        self.candle_info = {symbol: [] for symbol in symbols}

        for symbol in symbols:
            self.subscribe_md(symbol, start_date, end_date, self.interval)


    def subscribe_md(self, symbol, start_date, end_date, interval):
        # Implement logic to subscribe to market data for backtesting
        candle_info_params = {
            "exchange": "NSE",
            "symboltoken": symbol,
            "interval": interval,
            "fromdate": start_date,
            "todate": end_date
        }
        # Subscribe to market data using the parameters
        self.logger.info("Fetching historical candle data for backtesting...")
        candle_info = self.m_client.getCandleData(candle_info_params)
        self.candle_info[symbol] += (candle_info['data'])
        self.logger.info(f"Successfully fetched candle data for symbol: {symbol}")
        if symbol not in self.candle_info:
            self.candle_info[symbol] = []

    def load(self):
        """
        Initialize subscribers. It calls the getCandleinfo API to fetch historical data for the 
        specified symbols and stores it in the candle_info dictionary. This data will be used for 
        backtesting the strategy.
        """
        # Implement logic to load any necessary resources or data for backtesting
        for symbol in self.symbols:
            self.subscribe_md(symbol, self.start_date, self.end_date, self.interval)

    def on_md(self, md):
        # Process market data for backtesting
        self.logger.debug("Tick received", md)

    def start(self):
        """
         Start the backtesting strategy. This method processes the historical market data stored
         in the candle_info dictionary and plays it from start to end symbol-by-symbol.
         
         The method iterates through the market data for each symbol and calls the on_md method to
         process the data. The backtesting continues until all the market data for all symbols 
         has been processed.
        """
        self.logger.info("Starting backtesting strategy...")
        finished = False
        while not finished:
            for symbol in self.symbols:
                if symbol in self.candle_info and self.candle_info[symbol]:
                    md = self.candle_info[symbol].pop(0)
                    md_obj = OHLCQuote(symbol, md[0], md[1], md[2], md[3], md[4], md[5])
                    self.on_md(md_obj)
                    for strat in self.strats:
                        strat.on_md(md_obj)
            if all(symbol not in self.candle_info or not self.candle_info[symbol] for symbol in self.symbols):
                finished = True        


if(__name__ == "__main__"):
    app = BackTestPlatform()
    app.set_backtest_data_params(["99926000", "99926001"], "2025-09-06 11:15", "2026-02-30 12:00", "ONE_MINUTE")
    app.start()