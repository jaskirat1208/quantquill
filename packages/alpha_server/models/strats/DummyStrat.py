

from dataclasses import asdict
from quantquill.av_core.components.PositionManager import Position
from quantquill.av_core.components.signals.types import TrendSignalType
from quantquill.av_core.components.signals.signal import Signal
from quantquill.types import Trade
from quantquill.data.angel_one.platform import BackTestStrategyPlatform
from quantquill.strats import MovingAverageCrossoverStrategy
from quantquill.av_core.components.signals import SignalHandler
from models.models import StrategyResult

from datetime import datetime, timedelta
from typing import Optional, Any

class DummyStrat(SignalHandler):
    def __init__(self, symbols, start_date, end_date, data_type):
        self.platform = BackTestStrategyPlatform()
        self.platform.set_backtest_data_params(symbols, start_date, end_date, data_type)
        self.strategy = MovingAverageCrossoverStrategy()
        self.strategy.set_logger(self.platform.get_logger())
        self.strategy.set_signal_handler(self)
        self.platform.add_strat(self.strategy)
        self.booked = False
        self.last_booked_time = None
        self.starting_capital = 100000
        self.platform.set_total_capital(self.starting_capital)
        super().__init__()


    def start(self):
        self.platform.start()
        # This strategy will get a buy signal 
        print("Strategy execution completed")

    def handle_signal(self, signal: Signal) -> Optional[Any]:
        print("Signal timestamp:", signal.timestamp)
        print("Last booked time: ", self.last_booked_time)
        if(not self.booked):
            side = 'BUY' if signal.signal_type == TrendSignalType.UP else 'SELL'
            qty = 1

            trd = Trade(
                token=signal.symbol,
                quantity=qty,
                price=signal.price,
                side=side,
                timestamp=signal.timestamp
            )
            try:
                self.platform.book_trade(trd)
                self.booked = True
                self.last_booked_time = datetime.fromisoformat(signal.timestamp)
            except Exception as e:
                import traceback
                traceback.print_exc()
                print("Error booking trade:", e)

        if(self.booked and datetime.fromisoformat(signal.timestamp) - self.last_booked_time > timedelta(days=1)):
            self.booked = False
            
 
        
    def result(self):
        """
        Returns portfolio positions and value over time using platform data
        """
        # Get actual data from platform
        position_manager = self.platform.get_position_manager()
        trades = position_manager.get_trades()
        positions = position_manager.get_positions()
        
        # Create portfolio snapshots from actual platform data
        risk = position_manager.calculate_risk()
        pnl = risk['pnl']

        trades_dict = [asdict(trade) for trade in trades]
        
        return StrategyResult(
            strategy_name=self.__class__.__name__,
            symbol=self.platform.symbols[0] if self.platform.symbols else "UNKNOWN",
            parameters={
                'start_date': self.platform.start_date,
                'end_date': self.platform.end_date,
            },
            success=True,
            trades=trades_dict,
            profit_loss=pnl,
            max_drawdown=risk['max_drawdown'],
            volatility=risk['volatility'],
            sharpe_ratio=risk['sharpe_ratio'],
            total_return=pnl / position_manager.starting_cash * 100,
            portfolio_snapshots=risk['snapshots']
        )    


if(__name__ == "__main__"):
    strat = DummyStrat(["99926001"], "2026-01-01 09:15", "2026-01-31 15:30", "ONE_MINUTE")
    strat.start()
    print(strat.result())