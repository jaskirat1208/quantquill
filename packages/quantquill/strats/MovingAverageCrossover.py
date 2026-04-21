

from quantquill.strats.BaseStrat import BaseStrategy
from quantquill.types import OHLCQuote, Trade
from quantquill.data.angel_one.platform.BackTestStrategyPlatform import BackTestStrategyPlatform
from quantquill.av_core.components.signals import TrendSignalType
from quantquill.av_core.components.signals import TrendSignal
import pandas as pd
from datetime import datetime


class MovingAverageCrossoverStrategy(BaseStrategy):
    def __init__(self, *args):
        super().__init__(*args)
        self.short_window = 59
        self.long_window = 200
        self.short_alpha = 2.0 / (self.short_window + 1)
        self.long_alpha = 2.0 / (self.long_window + 1)
        self.short_ewma = 0
        self.long_ewma = 0
        self.trend = TrendSignalType.SIDEWAYS
        self.ewma_history_df = []
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
        new_trend = TrendSignalType.SIDEWAYS
        
        if self.short_ewma > self.long_ewma:
            new_trend = TrendSignalType.UP
        elif self.short_ewma < self.long_ewma:
            new_trend = TrendSignalType.DOWN
        
        if new_trend != self.trend:
            self.logger.info(f"Trend changed from {self.trend} to {new_trend}")
            self.trend = new_trend
            self.no_of_crossovers += 1
            signal = self.create_signal(new_trend, quote)
            

        self.ewma_history_df.append({
            'timestamp': datetime.fromisoformat(quote.timestamp),
            'short_ewma': self.short_ewma,
            'long_ewma': self.long_ewma
        })

    def create_signal(self, signal_type: TrendSignalType, quote: OHLCQuote):
        signal = TrendSignal(
            signal_type=signal_type,
            timestamp=quote.timestamp,
            price=quote.close_price,
            symbol=quote.symbol,
            metadata=quote.__dict__
        )
        self.process_signal(signal)
        return signal

    def summary(self):
        ewma_history_df = pd.DataFrame(self.ewma_history_df)

        return {
            "ewma_history": ewma_history_df,
            "short_ewma": self.short_ewma,
            "long_ewma": self.long_ewma,
            "trend": self.trend.value,
            "no_of_crossovers": self.no_of_crossovers,
        }


