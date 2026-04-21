from quantquill.strats.BaseStrat import BaseStrategy
from quantquill.types import OHLCQuote, Trade
from quantquill.data.angel_one.platform.BackTestStrategyPlatform import BackTestStrategyPlatform
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
from quantquill.av_core.components import PositionManager as pm
from quantquill.av_core.components.signals import TrendSignalType
from quantquill.av_core.components.signals import TrendSignal
from quantquill.strats.MovingAverageCrossover import MovingAverageCrossoverStrategy


class PlatformSignalHandler(BackTestStrategyPlatform):
    def __init__(self):
        super().__init__()
        self.trades_history = []

    def handle_signal(self, signal):
        new_trend = signal.signal_type
        if(new_trend == TrendSignalType.UP):
            self.logger.info(f"Buy signal at price {signal.price}")
            trade = Trade(token="99926001", quantity=1, price=signal.price, side="BUY", timestamp=signal.timestamp)
            self.book_trade(trade)
            self.trades_history.append(trade)  # Track the trade
        elif(new_trend == TrendSignalType.DOWN):
            self.logger.info(f"Sell signal at price {signal.price}")
            trade = Trade(token="99926001", quantity=1, price=signal.price, side="SELL", timestamp=signal.timestamp)
            self.book_trade(trade)
            self.trades_history.append(trade)  # Track the trade
        
    def summary(self):
        return {
            "total_trades": len(self.trades_history),
            "pnl": self.get_position_manager().get_positions(),
            "trades_history": self.trades_history
        }


def visualize(pf_summary, strat_summary):
    ewma_history_df = strat_summary['ewma_history']
    trades_history = pf_summary['trades_history']
    fig = go.Figure()
    
    # Add EMA lines
    fig.add_trace(go.Scatter(x=ewma_history_df['timestamp'], y=ewma_history_df['short_ewma'], mode='lines', name='Short EMA'))
    fig.add_trace(go.Scatter(x=ewma_history_df['timestamp'], y=ewma_history_df['long_ewma'], mode='lines', name='Long EMA'))
    
    # Add trade markers
    if trades_history:
        trade_times = [datetime.fromisoformat(trade.timestamp) for trade in trades_history]
        trade_prices = [trade.price for trade in trades_history]
        trade_sides = ['BUY' if trade.side == 'BUY' else 'SELL' for trade in trades_history]
        
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



if __name__ == "__main__":
    pf = PlatformSignalHandler()
    client = pf.get_client()
    instrument = client.getInstrumentBySymbol("BAJFINANCE")
    pf.set_backtest_data_params(["99926001"], "2024-09-06 11:15", "2024-10-28 12:00", "ONE_MINUTE")
    strategy = MovingAverageCrossoverStrategy()
    strategy.set_logger(pf.get_logger())
    strategy.set_signal_handler(pf)
    pf.add_strat(strategy)
    pf.start()
    strat_summary = strategy.summary()
    pf_summary = pf.summary()
    visualize(pf_summary, strat_summary)
    # print(strategy.summary())