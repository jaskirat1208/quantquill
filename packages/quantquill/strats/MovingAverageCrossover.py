

from quantquill.strats.BaseStrat import BaseStrategy
from quantquill.types import OHLCQuote
from quantquill.data.angel_one.platform.BackTestStrategyPlatform import BackTestStrategyPlatform
from enum import Enum
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
from quantquill.av_core.components import PositionManager as pm
from quantquill.types import Trade

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
        self.trades_history = []  # Track all booked trades
        self.no_of_crossovers = 0
        self.first_time = True

    
    def set_logger(self, logger):
        self.logger = logger
    
    def on_md(self, quote: OHLCQuote):
        if self.first_time:
            self.short_ewma = quote.close_price
            self.long_ewma = quote.close_price
            self.first_time = False
            return

        self.short_ewma = self.short_alpha * quote.close_price + (1 - self.short_alpha) * self.short_ewma
        self.long_ewma = self.long_alpha * quote.close_price + (1 - self.long_alpha) * self.long_ewma
        new_trend = Trend.OTHER
        
        if self.short_ewma > self.long_ewma:
            new_trend = Trend.UP
        elif self.short_ewma < self.long_ewma:
            new_trend = Trend.DOWN
        
        if new_trend != self.trend:
            self.logger.info(f"Trend changed from {self.trend} to {new_trend}")
            self.trend = new_trend
            self.no_of_crossovers += 1
            if(new_trend == Trend.UP):
                self.logger.info(f"Buy signal at price {quote.close_price}")
                trade = Trade(token="99926001", quantity=1, price=quote.close_price, side="BUY", timestamp=quote.timestamp)
                self.pf.book_trade(trade)
                self.trades_history.append(trade)  # Track the trade
            elif(new_trend == Trend.DOWN):
                self.logger.info(f"Sell signal at price {quote.close_price}")
                trade = Trade(token="99926001", quantity=1, price=quote.close_price, side="SELL", timestamp=quote.timestamp)
                self.pf.book_trade(trade)
                self.trades_history.append(trade)  # Track the trade

        self.ewma_history_df.append({
            'timestamp': datetime.fromisoformat(quote.timestamp),
            'short_ewma': self.short_ewma,
            'long_ewma': self.long_ewma
        })

    def summary(self):
        ewma_history_df = pd.DataFrame(self.ewma_history_df)
        fig = go.Figure()
        
        # Add EMA lines
        fig.add_trace(go.Scatter(x=ewma_history_df['timestamp'], y=ewma_history_df['short_ewma'], mode='lines', name='Short EMA'))
        fig.add_trace(go.Scatter(x=ewma_history_df['timestamp'], y=ewma_history_df['long_ewma'], mode='lines', name='Long EMA'))
        
        # Add trade markers
        if self.trades_history:
            trade_times = [datetime.fromisoformat(trade.timestamp) for trade in self.trades_history]
            trade_prices = [trade.price for trade in self.trades_history]
            trade_sides = ['BUY' if trade.side == 'BUY' else 'SELL' for trade in self.trades_history]
            
            # Buy trades (green triangles)
            buy_times = [trade_times[i] for i, side in enumerate(trade_sides) if side == 'BUY']
            buy_prices = [trade_prices[i] for i, side in enumerate(trade_sides) if side == 'BUY']
            if buy_times:
                fig.add_trace(go.Scatter(
                    x=buy_times, 
                    y=buy_prices, 
                    mode='markers', 
                    name='Buy Trades',
                    marker=dict(symbol='triangle-up', size=10, color='green')
                ))
            
            # Sell trades (red triangles)
            sell_times = [trade_times[i] for i, side in enumerate(trade_sides) if side == 'SELL']
            sell_prices = [trade_prices[i] for i, side in enumerate(trade_sides) if side == 'SELL']
            if sell_times:
                fig.add_trace(go.Scatter(
                    x=sell_times, 
                    y=sell_prices, 
                    mode='markers', 
                    name='Sell Trades',
                    marker=dict(symbol='triangle-down', size=10, color='red')
                ))
        
        fig.show()

        return {
            "short_ewma": self.short_ewma,
            "long_ewma": self.long_ewma,
            "trend": self.trend.value,
            "no_of_crossovers": self.no_of_crossovers,
            "total_trades": len(self.trades_history),
            "pnl": self.pf.get_position_manager().get_positions()
        }


if __name__ == "__main__":
    pf = BackTestStrategyPlatform()
    client = pf.get_client()
    instrument = client.getInstrumentBySymbol("BAJFINANCE")
    pf.set_backtest_data_params(["99926001"], "2024-09-06 11:15", "2026-02-28 12:00", "ONE_MINUTE")
    strategy = MovingAverageCrossoverStrategy()
    strategy.set_logger(pf.get_logger())
    strategy.set_platform(pf)
    pf.add_strat(strategy)
    pf.start()
    print(strategy.summary())