"""
Strategy module for QuantQuill.

This module contains trading strategies and base classes for strategy development.
"""

from quantquill.types import OHLCQuote
from .BaseStrat import BaseStrategy
from .MovingAverageCrossover import MovingAverageCrossoverStrategy

__all__ = [
    "BaseStrategy",
    "OHLCQuote", 
    "MovingAverageCrossoverStrategy",
]