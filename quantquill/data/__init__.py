"""
Data module for QuantQuill.

This module contains market data handling and broker integration components.
"""

from .angel_one.platform import BackTestStrategyPlatform

__all__ = [
    "BackTestStrategyPlatform",
]
