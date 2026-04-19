# QuantQuill

A comprehensive quantitative trading framework for strategy development, backtesting, and execution.

## Features

- **Strategy Development**: Base classes and tools for creating custom trading strategies
- **Backtesting Platform**: Full-featured backtesting with historical data
- **Position Management**: Automated position tracking and P&L calculation
- **Market Data Integration**: Support for multiple data sources (Angel One, etc.)
- **Visualization**: Built-in charts and performance analytics
- **Extensible Architecture**: Modular design for easy customization

## Installation

### From PyPI (when published)
```bash
pip install quantquill
```

### From Source
```bash
git clone https://github.com/jaskirat1208/quantquill.git
cd quantquill
pip install -e .
```

### Development Installation
```bash
git clone https://github.com/jaskirat1208/quantquill.git
cd quantquill
pip install -e ".[dev]"
```

## Quick Start

```python
from quantquill import MovingAverageCrossoverStrategy, BackTestStrategyPlatform

# Create backtesting platform
platform = BackTestStrategyPlatform()

# Configure backtest data
platform.set_backtest_data_params(
    tokens=["99926001"], 
    start_date="2024-09-06 11:15", 
    end_date="2025-12-31 12:00", 
    timeframe="ONE_MINUTE"
)

# Create and configure strategy
strategy = MovingAverageCrossoverStrategy()
strategy.set_logger(platform.get_logger())
strategy.set_platform(platform)

# Add strategy and run backtest
platform.add_strat(strategy)
platform.start()

# Get results
results = strategy.summary()
print(f"Total trades: {results['total_trades']}")
print(f"P&L: {results['pnl']}")
```

## Core Components

### Strategies
- **BaseStrategy**: Abstract base class for all trading strategies
- **MovingAverageCrossoverStrategy**: Example EMA crossover strategy

### Platforms
- **BackTestStrategyPlatform**: Historical data backtesting platform

### Components
- **PositionManager**: Trade execution and position tracking
- **LoggerConfig**: Centralized logging configuration

## Creating Custom Strategies

```python
from quantquill import BaseStrategy, OHLCQuote
from enum import Enum

class MyStrategy(BaseStrategy):
    def __init__(self, *args):
        super().__init__(*args)
        # Initialize your strategy parameters
        
    def on_md(self, quote: OHLCQuote):
        # Process market data and generate signals
        # Example: self.pf.book_trade(trade)
        
    def summary(self):
        # Return strategy performance summary
        return {"custom_metric": "value"}
```

## Configuration

### Environment Variables
- `QUANTQUILL_LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)
- `QUANTQUILL_CONFIG_PATH`: Path to configuration file

### Configuration Files
Place your configuration files in the `configs/` directory:
- `broker_config.json`: Broker API credentials
- `strategy_config.yaml`: Strategy parameters

## Development

### Running Tests
```bash
pytest
```

### Code Formatting
```bash
black quantquill/
```

### Type Checking
```bash
mypy quantquill/
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- **Documentation**: [https://quantquill.readthedocs.io/](https://quantquill.readthedocs.io/)
- **Issues**: [https://github.com/jaskirat1208/quantquill/issues](https://github.com/jaskirat1208/quantquill/issues)
- **Discussions**: [https://github.com/jaskirat1208/quantquill/discussions](https://github.com/jaskirat1208/quantquill/discussions)

## Acknowledgments

- SmartAPI Python library for broker integration
- Plotly for visualization capabilities
- Pandas for data manipulation
