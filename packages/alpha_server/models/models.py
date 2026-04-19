from typing import Dict, List, Any, Optional
from datetime import datetime
import random

# Strategy parameter models (Flask-compatible validation)
class MovingAverageStrategy:
    def __init__(self, data: Dict[str, Any]):
        self.symbol = data.get('symbol')
        self.short_window = int(data.get('short_window', 10))
        self.long_window = int(data.get('long_window', 30))
        self.position_size = float(data.get('position_size', 1000.0))
        
    def validate(self):
        errors = []
        if not self.symbol:
            errors.append("symbol is required")
        if self.short_window < 1 or self.short_window > 100:
            errors.append("short_window must be between 1 and 100")
        if self.long_window < 1 or self.long_window > 200:
            errors.append("long_window must be between 1 and 200")
        if self.position_size <= 0:
            errors.append("position_size must be greater than 0")
        return errors
    
    def to_dict(self):
        return {
            "symbol": self.symbol,
            "short_window": self.short_window,
            "long_window": self.long_window,
            "position_size": self.position_size
        }

class RSIStrategy:
    def __init__(self, data: Dict[str, Any]):
        self.symbol = data.get('symbol')
        self.rsi_period = int(data.get('rsi_period', 14))
        self.oversold = float(data.get('oversold', 30.0))
        self.overbought = float(data.get('overbought', 70.0))
        self.position_size = float(data.get('position_size', 1000.0))
        
    def validate(self):
        errors = []
        if not self.symbol:
            errors.append("symbol is required")
        if self.rsi_period < 1 or self.rsi_period > 50:
            errors.append("rsi_period must be between 1 and 50")
        if self.oversold < 0 or self.oversold > 50:
            errors.append("oversold must be between 0 and 50")
        if self.overbought < 50 or self.overbought > 100:
            errors.append("overbought must be between 50 and 100")
        if self.position_size <= 0:
            errors.append("position_size must be greater than 0")
        return errors
    
    def to_dict(self):
        return {
            "symbol": self.symbol,
            "rsi_period": self.rsi_period,
            "oversold": self.oversold,
            "overbought": self.overbought,
            "position_size": self.position_size
        }

# Response models
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

# Mock quantquill library (same as before)
class MockQuantQuillLibrary:
    """Mock version of your quantquill library for demonstration"""
    
    @staticmethod
    def get_available_strategies() -> List[str]:
        return ["moving_average", "rsi", "bollinger_bands"]
    
    @staticmethod
    def execute_moving_average(symbol: str, short_window: int, long_window: int, position_size: float) -> Dict:
        return {
            "success": True,
            "trades": [
                {"action": "BUY", "price": 150.25, "quantity": position_size / 150.25, "time": datetime.now().isoformat()},
                {"action": "SELL", "price": 152.10, "quantity": position_size / 150.25, "time": datetime.now().isoformat()}
            ],
            "profit_loss": random.uniform(-100, 500),
            "message": f"Moving average strategy executed for {symbol}"
        }
    
    @staticmethod
    def execute_rsi(symbol: str, rsi_period: int, oversold: float, overbought: float, position_size: float) -> Dict:
        return {
            "success": True,
            "trades": [
                {"action": "BUY", "price": 145.50, "quantity": position_size / 145.50, "time": datetime.now().isoformat()}
            ],
            "profit_loss": random.uniform(-50, 300),
            "message": f"RSI strategy executed for {symbol}"
        }

# Strategy executor (same as before)
class StrategyExecutor:
    def __init__(self):
        self.library = MockQuantQuillLibrary()
    
    def list_strategies(self) -> Dict[str, Any]:
        strategies = self.library.get_available_strategies()
        return {
            "strategies": [
                {
                    "name": "moving_average",
                    "description": "Moving average crossover strategy",
                    "parameters": ["symbol", "short_window", "long_window", "position_size"]
                },
                {
                    "name": "rsi", 
                    "description": "RSI overbought/oversold strategy",
                    "parameters": ["symbol", "rsi_period", "oversold", "overbought", "position_size"]
                },
                {
                    "name": "bollinger_bands",
                    "description": "Bollinger bands mean reversion strategy", 
                    "parameters": ["symbol", "period", "std_dev", "position_size"]
                }
            ]
        }
    
    def execute_strategy(self, strategy_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        if strategy_name == "moving_average":
            return self.library.execute_moving_average(**params)
        elif strategy_name == "rsi":
            return self.library.execute_rsi(**params)
        else:
            return {"success": False, "message": f"Strategy {strategy_name} not implemented yet"}
