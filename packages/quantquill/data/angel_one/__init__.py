"""
Angel One broker integration module for QuantQuill.

This module contains the Angel One specific implementations for market data,
trade execution, and backtesting functionality.
"""

from .platform import BackTestStrategyPlatform

__all__ = [
    "BackTestStrategyPlatform",
]
