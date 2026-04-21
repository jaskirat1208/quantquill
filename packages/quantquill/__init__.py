"""
QuantQuill - A comprehensive quantitative trading framework.

This package provides tools for:
- Strategy development and backtesting
- Market data handling
- Trade execution and position management
- Performance analysis and visualization
"""

__version__ = "0.1.0"
__author__ = "jaskirat1208"
__email__ = "jaskirat@example.com"

# Core imports
from quantquill.types import OHLCQuote, Trade
from quantquill.strats import BaseStrategy
from quantquill.data.angel_one.platform import BackTestStrategyPlatform

# Strategy imports
from quantquill.strats.MovingAverageCrossover import MovingAverageCrossoverStrategy

# Component imports
from quantquill.av_core.components import PositionManager
from quantquill.av_core.logger import LoggerConfig

__all__ = [
    # Core classes
    "OHLCQuote",
    "Trade",
    "BaseStrategy", 
    "BackTestStrategyPlatform",
    
    # Strategies
    "MovingAverageCrossoverStrategy",
    
    # Components
    "PositionManager",
    "LoggerConfig",
    
    # Version info
    "__version__",
    "__author__",
    "__email__",
]