"""
Strategy module for QuantQuill.

This module contains trading strategies and base classes for strategy development.
"""

from .BaseStrat import BaseStrategy, OHLCQuote
from .MovingAverageCrossover import MovingAverageCrossoverStrategy

__all__ = [
    "BaseStrategy",
    "OHLCQuote", 
    "MovingAverageCrossoverStrategy",
]