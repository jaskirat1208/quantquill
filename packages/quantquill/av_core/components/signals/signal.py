
from dataclasses import dataclass, field
from typing import Optional, Any, List, Dict

import uuid

from quantquill.types import OHLCQuote
from quantquill.av_core.components.signals.types import (
    TrendSignalType, 
    MomentumSignalType, 
    VolatilitySignalType, 
    RiskSignalType,
    CompositeSignalType, 
    SignalPriority
)

from enum import Enum
from datetime import datetime

@dataclass
class Signal:
    """Simple signal using dataclass."""
    signal_type: Enum
    timestamp: str
    price: float
    symbol: str
    confidence: float = 1.0
    priority: SignalPriority = SignalPriority.MEDIUM
    metadata: Dict[str, Any] = field(default_factory=dict)
    signal_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    source: str = ""
    expires_at: Optional[str] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()
        if self.metadata is None:
            self.metadata = {}


@dataclass
class TrendSignal(Signal):
    """Trend-based signal."""
    signal_type: TrendSignalType


@dataclass
class MomentumSignal(Signal):
    """Momentum-based signal."""
    signal_type: MomentumSignalType


@dataclass
class VolatilitySignal(Signal):
    """Volatility-based signal."""
    signal_type: VolatilitySignalType


@dataclass
class RiskSignal(Signal):
    """Risk-based signal."""
    signal_type: RiskSignalType


# @dataclass
# class CompositeSignal(Signal):
#     """Composite signal made of multiple signals."""
#     signal_type: CompositeSignalType
#     signals: List[Signal]


class SignalHandler:
    """
    Base class for signal handlers.
    
    Signal handlers are responsible for processing signals
    and taking appropriate actions (e.g., executing trades).
    """
    
    def __init__(self, name: str = ""):
        self.name = name or self.__class__.__name__
        self.processed_signals: List[Signal] = []
    
    def handle_signal(self, signal: Signal) -> Optional[Any]:
        """
        Handle a single signal.
        
        Args:
            signal: The signal to handle
            
        Returns:
            Result of handling the signal (e.g., Trade object)
        """
        self.processed_signals.append(signal)
        raise NotImplementedError("handle_signal must be implemented by subclasses")

    def get_processed_signals(self) -> List[Signal]:
        """
        Get all processed signals.
        
        Returns:
            List of processed signals
        """
        return self.processed_signals
