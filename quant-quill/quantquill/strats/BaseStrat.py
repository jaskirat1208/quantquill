from typing import Optional

from quantquill.av_core.logger import LoggerConfig
from quantquill.types import OHLCQuote

class BaseStrategy:
    """
    Initializes the base strategy with a name and an optional configuration dictionary. The name is used to identify the strategy, while the configuration can hold any parameters or settings that the strategy may require.
    Args:        name (str): The name of the strategy.
        cfg (dict, optional): A dictionary containing configuration parameters for the strategy. Defaults to None.
    Depending on market data implementation, you can initialize  necessary market data subscriptions in the constructor and initite the market data feed. 
    """
    def __init__(self, **kwargs):
        if('logger' in kwargs):
            self.logger = kwargs['logger']
        else:
            self.logger = LoggerConfig.get_logger(self.__class__.__name__)

    def set_platform(self, pf):
        self.pf = pf

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

