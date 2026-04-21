"""
Signals module for QuantQuill core functionality.

This module contains signal types and signal handling classes.
"""

from .types import (
    TrendSignalType,
    MomentumSignalType,
    VolatilitySignalType,
    RiskSignalType,
    CompositeSignalType,
    SignalPriority
)
from .signal import (
    Signal,
    TrendSignal,
    MomentumSignal,
    VolatilitySignal,
    RiskSignal,
    SignalHandler
)

__all__ = [
    # Signal types
    "TrendSignalType",
    "MomentumSignalType", 
    "VolatilitySignalType",
    "RiskSignalType",
    "CompositeSignalType",
    "SignalPriority",
    
    # Signal classes
    "Signal",
    "TrendSignal",
    "MomentumSignal", 
    "VolatilitySignal",
    "RiskSignal",
    "SignalHandler",
]