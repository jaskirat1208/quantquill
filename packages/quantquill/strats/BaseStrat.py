from typing import Optional

from quantquill.av_core.logger import LoggerConfig
from quantquill.types import OHLCQuote
from quantquill.av_core.components.signals.signal import SignalHandler


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

    def set_signal_handler(self, signal_handler: SignalHandler):
        self.signal_handler = signal_handler

    def set_platform(self, pf):
        self.pf = pf
    
    def process_signal(self, signal):
        """
        Process a signal immediately when generated.
        
        This method sends the signal to the registered signal handler
        for immediate processing (e.g., execution, risk management).
        
        Args:
            signal: The signal to process
        """
        if hasattr(self, 'signal_handler') and self.signal_handler:
            return self.signal_handler.handle_signal(signal)
        else:
            self.logger.warning("No signal handler registered - signal not processed")
            return None

    def create_signal(self, signal_type, quote, value=None, confidence=1.0, **kwargs):
        """
        Create a signal and automatically process it.
        
        This method creates a signal and immediately sends it to the signal handler.
        Users don't need to call process_signal() manually.
        
        Args:
            signal_type: Type of signal (Enum)
            quote: OHLCQuote object
            value: Signal value (optional, defaults to None)
            confidence: Signal confidence (0.0-1.0, defaults to 1.0)
            **kwargs: Additional signal metadata
            
        Returns:
            Result of signal processing (e.g., Trade object) or None
        """
        from quantquill.av_core.components.signals.signal import Signal
        
        signal = Signal(
            signal_type=signal_type,
            value=value,
            confidence=confidence,
            quote=quote,
            **kwargs
        )
        
        return self.process_signal(signal)

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

