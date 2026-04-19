from fastapi import APIRouter, Depends, Request
from typing import Dict, Any
from datetime import datetime

from models.pydantic_models import MovingAverageStrategy, RSIStrategy, StrategyResult
from core.route_registry import register_route

def get_strategy_executor(request: Request):
    """Dependency to get strategy executor from app state"""
    return request.app.state.strategy_executor

@register_route(prefix="/strategies", tags=["strategies"])
class StrategyRouter:
    def __init__(self, prefix: str = "", tags: list = None, dependencies: list = None):
        self.router = APIRouter(prefix=prefix, tags=tags, dependencies=dependencies)

        # Register routes with dependencies
        self.router.add_api_route("/", self.list_strategies, methods=["GET"])
        self.router.add_api_route("/moving_average/execute", self.execute_moving_average, methods=["POST"])
        self.router.add_api_route("/rsi/execute", self.execute_rsi_strategy, methods=["POST"])
    
    async def list_strategies(self, request: Request):
        """List all available strategies from quantquill library"""
        executor = get_strategy_executor(request)
        return executor.list_strategies()

    async def execute_moving_average(self, strategy: MovingAverageStrategy, request: Request):
        """Execute moving average strategy with validated parameters"""
        executor = get_strategy_executor(request)
        result = executor.execute_strategy("moving_average", strategy.dict())
        return StrategyResult(
            strategy_name="moving_average",
            symbol=strategy.symbol,
            executed_at=datetime.now(),
            parameters=strategy.dict(),
            success=result["success"],
            message=result.get("message"),
            trades=result.get("trades")
        )

    async def execute_rsi_strategy(self, strategy: RSIStrategy, request: Request):
        """Execute RSI strategy with validated parameters"""
        executor = get_strategy_executor(request)
        result = executor.execute_strategy("rsi", strategy.dict())
        return StrategyResult(
            strategy_name="rsi",
            symbol=strategy.symbol,
            executed_at=datetime.now(),
            parameters=strategy.dict(),
            success=result["success"],
            message=result.get("message"),
            trades=result.get("trades")
        )
