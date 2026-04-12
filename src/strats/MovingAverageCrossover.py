

from strats.BaseStrat import BaseStrategy, OHLCQuote
from data.angel_one.platform.BackTestStrategyPlatform import BackTestStrategyPlatform
from enum import Enum
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
from av_core.components import PositionManager as pm

class Trend(Enum):
    OTHER = 0
    UP = 1
    DOWN = 2

class MovingAverageCrossoverStrategy(BaseStrategy):
    def __init__(self, *args):
        super().__init__(*args)
        self.short_window = 59
        self.long_window = 200
        self.short_alpha = 2.0 / (self.short_window + 1)
        self.long_alpha = 2.0 / (self.long_window + 1)
        self.short_ewma = 0
        self.long_ewma = 0
        self.trend = Trend.OTHER
        self.ewma_history_df = []
        self.first_cross_detected = False
        self.no_of_crossovers = 0

    
    def set_logger(self, logger):
        self.logger = logger
    
    def on_md(self, quote: OHLCQuote):
        self.short_ewma = self.short_alpha * quote.close_price + (1 - self.short_alpha) * self.short_ewma
        self.long_ewma = self.long_alpha * quote.close_price + (1 - self.long_alpha) * self.long_ewma
        new_trend = Trend.OTHER
        
        if self.short_ewma > self.long_ewma:
            new_trend = Trend.UP
            self.pf.book_trade(pm.Trade(token="99926001", quantity=1, price=quote.close_price, side=pm.Side.BUY, timestamp=quote.timestamp))
        elif self.short_ewma < self.long_ewma:
            new_trend = Trend.DOWN
            self.pf.book_trade(pm.Trade(token="99926001", quantity=1, price=quote.close_price, side=pm.Side.SELL, timestamp=quote.timestamp))
        
        if new_trend != self.trend:
            self.logger.info(f"Trend changed from {self.trend} to {new_trend}")
            self.trend = new_trend
            self.no_of_crossovers += 1

        self.ewma_history_df.append({
            'timestamp': datetime.fromisoformat(quote.timestamp),
            'short_ewma': self.short_ewma,
            'long_ewma': self.long_ewma
        })

    def summary(self):
        ewma_history_df = pd.DataFrame(self.ewma_history_df)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=ewma_history_df['timestamp'], y=ewma_history_df['short_ewma'], mode='lines', name='Short EMA'))
        fig.add_trace(go.Scatter(x=ewma_history_df['timestamp'], y=ewma_history_df['long_ewma'], mode='lines', name='Long EMA'))
        fig.show()

        return {
            "short_ewma": self.short_ewma,
            "long_ewma": self.long_ewma,
            "trend": self.trend.value,
            "no_of_crossovers": len(self.ewma_history_df) - 1,
            "pnl": self.pf.get_position_manager().get_positions()
        }


if __name__ == "__main__":
    pf = BackTestStrategyPlatform()
    client = pf.get_client()
    instrument = client.getInstrumentBySymbol("BAJFINANCE")
    pf.set_backtest_data_params(["99926001"], "2024-09-06 11:15", "2026-02-30 12:00", "ONE_MINUTE")
    strategy = MovingAverageCrossoverStrategy()
    strategy.set_logger(pf.get_logger())
    strategy.set_platform(pf)
    pf.add_strat(strategy)
    pf.start()
    print(strategy.summary())