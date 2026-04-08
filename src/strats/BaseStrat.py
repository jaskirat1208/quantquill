from typing import Optional

from av_core.logger import LoggerConfig

class OHLCQuote:
    def __init__(self, symbol, timestamp, open_price, high_price, low_price, close_price, volume):
        self.timestamp = timestamp
        self.open_price = open_price
        self.high_price = high_price
        self.low_price = low_price
        self.close_price = close_price
        self.symbol = symbol
        self.volume = volume

    def __repr__(self):
        return f"OHLCQuote(symbol={self.symbol}, timestamp={self.timestamp}, open={self.open_price}, high={self.high_price}, low={self.low_price}, close={self.close_price}, volume={self.volume})"

class BaseStrategy:
    """
    Initializes the base strategy with a name and an optional configuration dictionary. The name is used to identify the strategy, while the configuration can hold any parameters or settings that the strategy may require.
    Args:        name (str): The name of the strategy.
        cfg (dict, optional): A dictionary containing configuration parameters for the strategy. Defaults to None.
    Depending on market data implementation, you can initialize  necessary market data subscriptions in the constructor and initite the market data feed. 
    """
    def __init__(self, *args):
        # if('name' in args):
        #     self.name = args['name']

        # self.name = type(self).__name__
        # self.logger = LoggerConfig.setup(name=self.name)
        pass

    def load(self):
        """
        This method can be used to load any necessary resources or data for the strategy. 
        Subclasses can override this method to provide specific loading behavior.
        """
        pass
    
    """
    This function should be called when new market data is received. S
    ubclasses should implement this method to define how they process incoming market data.
    """
    def on_md(self, md: OHLCQuote):
        raise NotImplementedError("on_md method must be implemented by subclasses.")

    def start(self):
        """
        This method can be used to start the strategy's main logic. 
        Subclasses can override this method to provide specific behavior when the strategy is started.
        """
        pass

