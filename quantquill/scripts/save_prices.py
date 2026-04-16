from quantquill.strats import BaseStrat
from typing import Optional
from quantquill.data.angel_one.platform.BackTestStrategyPlatform import BackTestStrategyPlatform
from quantquill.strats.BaseStrat import OHLCQuote
from quantquill.av_core.logger import LoggerConfig

class PriceSaverStrat(BaseStrat.BaseStrategy):
    def __init__(self):
        super().__init__(self)
        self.logger = LoggerConfig.get_logger("PriceSaverStrat")
        self.logger.info("PriceSaverStrat initialized successfully.")

    def start(self):
        self.logger.info("PriceSaverStrat started.")
        # Initialize any necessary resources or subscriptions here
    
    def on_md(self, quote: OHLCQuote):
        self.logger.info(f"Received MD: {quote}")


if(__name__ == "__main__"):
    pf = BackTestStrategyPlatform()
    s1 = PriceSaverStrat()
    pf.add_strat(s1)
    pf.set_backtest_data_params(["99926000", "99926001"], "2025-09-06 11:15", "2026-02-30 12:00", "ONE_MINUTE")
    pf.start()