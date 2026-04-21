

from quantquill.data.angel_one.platform import BackTestStrategyPlatform
from quantquill.strats import MovingAverageCrossoverStrategy
from quantquill.av_core.components.signals import SignalHandler


class MovingAverageCrossoverStrat(SignalHandler):
    def __init__(self, symbols, start_date, end_date, data_type):
        self.platform = BackTestStrategyPlatform()
        self.platform.set_backtest_data_params(symbols, start_date, end_date, data_type)
        self.strategy = MovingAverageCrossoverStrategy()
        self.strategy.set_logger(self.platform.get_logger())
        self.strategy.set_signal_handler(self)
        self.platform.add_strat(self.strategy)

    def handle_signal(self, signal):
        # TODO: Implement execution logic
        print("Signal received:", signal)

    def start(self):
        self.platform.start()
        print("Strategy execution completed")


if(__name__ == "__main__"):
    strat = MovingAverageCrossoverStrat(["99926001"], "2026-01-01 09:15", "2026-01-31 15:30", "ONE_MINUTE")
    strat.start()