

from enum import Enum

class TrendSignalType(Enum):
    UP = "UP"
    DOWN = "DOWN"
    SIDEWAYS = "SIDEWAYS"

class MomentumSignalType(Enum):
    BULLISH = "BULLISH"
    BEARISH = "BEARISH"
    NEUTRAL = "NEUTRAL"

class VolatilitySignalType(Enum):
    HIGH = "HIGH"
    LOW = "LOW"
    NORMAL = "NORMAL"

class RiskSignalType(Enum):
    HIGH = "HIGH"
    LOW = "LOW"
    NORMAL = "NORMAL"

class CompositeSignalType(Enum):
    AND = "AND"
    OR = "OR"
    XOR = "XOR"
    
class SignalPriority(Enum):
    """Signal priority levels for handling multiple signals."""
    CRITICAL = 1    # Must be handled immediately (e.g., stop loss)
    HIGH = 2       # Important signals (e.g., primary trading signals)
    MEDIUM = 3     # Regular signals (e.g., trend changes)
    LOW = 4        # Informational signals (e.g., market conditions)