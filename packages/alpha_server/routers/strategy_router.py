from fastapi import APIRouter, Depends, Request
from typing import Dict, Any
from datetime import datetime

from models.models import StrategyResult
from alpha_server.models.strats import MovingAverageCrossoverStrat
from core.route_registry import register_route
from models import strats
from alpha_server.models.strats.DummyStrat import DummyStrat

@register_route(prefix="/strategies", tags=["strategies"])
class StrategyRouter:
    def __init__(self, prefix: str = "", tags: list = None, dependencies: list = None):
        self.router = APIRouter(prefix=prefix, tags=tags, dependencies=dependencies)

        # Register routes with dependencies
        self.router.add_api_route("/", self.list_strategies, methods=["GET"])
        self.router.add_api_route("/{strategy_name}/execute", self.execute_strategy, methods=["POST"])
    
    async def list_strategies(self, request: Request):
        """List all available strategies"""
        # Get strategy classes from the strats module
        available_strategies = []
        for attr_name in dir(strats):
            attr = getattr(strats, attr_name)
            if isinstance(attr, type) and hasattr(attr, '__name__'):
                available_strategies.append(attr.__name__)
        
        print(f"Available strategies: {available_strategies}")
        return {
            "strategies": available_strategies,
            "message": "Strategy listing to be implemented"
        }

    async def execute_strategy(self, strategy_name: str, strategy_data: Dict[str, Any], request: Request):
        """Execute a strategy with given parameters"""
        strat = DummyStrat(
            strategy_data.get("symbols", ["99926001"]),
            strategy_data.get("start_date", "2026-01-01 09:15"),
            strategy_data.get("end_date", "2026-01-31 15:30"),
            strategy_data.get("data_type", "ONE_MINUTE")
        )
        
        # Get strategy results
        strat.start()
        return strat.result()
