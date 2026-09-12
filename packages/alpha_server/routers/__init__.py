# Routers package
# Import all routers so they get registered
from .health_router import HealthRouter
from .strategy_router import StrategyRouter
from .example_router import ExampleRouter
from .instruments import InstrumentsRouter
from .oi_monitor import OIMonitorRouter

__all__ = ["HealthRouter", "StrategyRouter", "ExampleRouter", "InstrumentsRouter", "OIMonitorRouter"]