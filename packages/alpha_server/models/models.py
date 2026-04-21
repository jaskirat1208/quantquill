from typing import Dict, List, Any, Optional
from datetime import datetime

# Base response models
class StrategyResult:
    def __init__(self, strategy_name: str, symbol: str, parameters: Dict[str, Any], 
                 success: bool, message: Optional[str] = None, trades: Optional[List[Dict]] = None):
        self.strategy_name = strategy_name
        self.symbol = symbol
        self.executed_at = datetime.now()
        self.parameters = parameters
        self.success = success
        self.message = message
        self.trades = trades
    
    def to_dict(self):
        return {
            "strategy_name": self.strategy_name,
            "symbol": self.symbol,
            "executed_at": self.executed_at.isoformat(),
            "parameters": self.parameters,
            "success": self.success,
            "message": self.message,
            "trades": self.trades
        }

class StrategyInfo:
    def __init__(self, name: str, description: str, parameters_schema: Dict[str, Any], 
                 supported_symbols: List[str]):
        self.name = name
        self.description = description
        self.parameters_schema = parameters_schema
        self.supported_symbols = supported_symbols
    
    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "parameters_schema": self.parameters_schema,
            "supported_symbols": self.supported_symbols
        }
