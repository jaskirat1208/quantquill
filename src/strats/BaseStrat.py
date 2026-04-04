from av_core import app
from typing import Optional

class BaseStrategy(app.App):
    """
    Initializes the base strategy with a name and an optional configuration dictionary. The name is used to identify the strategy, while the configuration can hold any parameters or settings that the strategy may require.
    Args:        name (str): The name of the strategy.
        cfg (dict, optional): A dictionary containing configuration parameters for the strategy. Defaults to None.
    Depending on market data implementation, you can initialize  necessary market data subscriptions in the constructor and initite the market data feed. 
    """
    def __init__(self, config_file: Optional[str] = None,  log_file: Optional[str] = None, instance_name: str = ""):
        super().__init__(config_file=config_file, log_file=log_file, instance_name=instance_name)

    """
    This function should be called when new market data is received. Subclasses should implement this method to define how they process incoming market data.
    """
    def on_md(self, md):
        raise NotImplementedError("on_md method must be implemented by subclasses.")

    def start(self):
        """
        This method can be used to start the strategy, such as initializing any necessary resources or starting market data subscriptions. Subclasses can override this method to provide specific startup behavior.
        """
        pass
