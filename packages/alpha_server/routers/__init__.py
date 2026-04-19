# Routers package
# Import all routers so they get registered
from .health_router import HealthRouter
from .strategy_router import StrategyRouter
from .example_router import ExampleRouter

__all__ = ["HealthRouter", "StrategyRouter", "ExampleRouter"]