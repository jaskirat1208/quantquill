from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

# Strategy parameter models - FastAPI auto-validates these!
class MovingAverageStrategy(BaseModel):
    symbol: str = Field(..., description="Trading symbol (e.g., 'AAPL')")
    short_window: int = Field(10, ge=1, le=100, description="Short MA window")
    long_window: int = Field(30, ge=1, le=200, description="Long MA window")
    position_size: float = Field(1000.0, gt=0, description="Position size in $")

class RSIStrategy(BaseModel):
    symbol: str = Field(..., description="Trading symbol")
    rsi_period: int = Field(14, ge=1, le=50, description="RSI period")
    oversold: float = Field(30.0, ge=0, le=50, description="Oversold threshold")
    overbought: float = Field(70.0, ge=50, le=100, description="Overbought threshold")
    position_size: float = Field(1000.0, gt=0, description="Position size in $")

# Response models
class StrategyResult(BaseModel):
    strategy_name: str
    symbol: str
    executed_at: datetime
    parameters: Dict[str, Any]
    success: bool
    message: Optional[str] = None
    trades: Optional[List[Dict]] = None

class StrategyInfo(BaseModel):
    name: str
    description: str
    parameters_schema: Dict[str, Any]
    supported_symbols: List[str]
