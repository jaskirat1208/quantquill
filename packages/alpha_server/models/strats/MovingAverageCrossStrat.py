

from quantquill.strats import BaseStrategy
from quantquill.data.angel_one import platform as pf

class MovingAverageCrossStrat(BaseStrategy):
    def __init__(self):
        pass


class BackTestStratSimulator:
    def __init__(self, strategy: BaseStrategy):
        self.platform = pf.BackTestStrategyPlatform()
        client = self.platform.get_client()
        instrument = client.getInstrumentBySymbol("BAJFINANCE")
        self.strategy = strategy
        self.strategy.set_logger(self.platform.get_logger())
        self.strategy.set_platform(self.platform)
        self.platform.add_strat(strategy)


    def set_params(self, params):
        self.platform.set_backtest_data_params(params["instruments"], params["start_time"], params["end_time"], params["timeframe"])


    def simulate(self):
        self.platform.start()
        results = self.strategy.summary()
        return results