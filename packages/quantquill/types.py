"""
Type definitions for QuantQuill.

This module contains shared types and data structures used across the package.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class OHLCQuote:
    """OHLC (Open, High, Low, Close) market data quote."""
    symbol: str
    timestamp: str
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    volume: Optional[float] = None
    
    def __post_init__(self):
        if isinstance(self.timestamp, datetime):
            self.timestamp = self.timestamp.isoformat()


@dataclass
class Trade:
    """Trade execution details."""
    token: str
    quantity: float = 0
    price: float = 0
    side: str = "BUY"
    timestamp: str = ""
    trade_id: int = 0
    tx_cost: int = 0
    
    def __post_init__(self):
        if isinstance(self.timestamp, datetime):
            self.timestamp = self.timestamp.isoformat()
