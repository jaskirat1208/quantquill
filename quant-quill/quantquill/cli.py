#!/usr/bin/env python3
"""
Command line interface for QuantQuill.
"""

import argparse
import sys
from quantquill import MovingAverageCrossoverStrategy, BackTestStrategyPlatform


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="QuantQuill - Quantitative Trading Framework")
    parser.add_argument("--version", action="version", version="QuantQuill 0.1.0")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Backtest command
    backtest_parser = subparsers.add_parser("backtest", help="Run backtesting")
    backtest_parser.add_argument("--tokens", nargs="+", required=True, help="Trading tokens")
    backtest_parser.add_argument("--start-date", required=True, help="Start date (YYYY-MM-DD HH:MM)")
    backtest_parser.add_argument("--end-date", required=True, help="End date (YYYY-MM-DD HH:MM)")
    backtest_parser.add_argument("--timeframe", default="ONE_MINUTE", help="Timeframe")
    backtest_parser.add_argument("--strategy", default="ma_crossover", help="Strategy to use")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == "backtest":
        run_backtest(args)


def run_backtest(args):
    """Run backtesting with specified parameters."""
    print(f"Running backtest with strategy: {args.strategy}")
    print(f"Tokens: {args.tokens}")
    print(f"Period: {args.start_date} to {args.end_date}")
    print(f"Timeframe: {args.timeframe}")
    
    try:
        # Create platform
        platform = BackTestStrategyPlatform()
        
        # Configure backtest
        platform.set_backtest_data_params(
            tokens=args.tokens,
            start_date=args.start_date,
            end_date=args.end_date,
            timeframe=args.timeframe
        )
        
        # Create strategy
        if args.strategy == "ma_crossover":
            strategy = MovingAverageCrossoverStrategy()
        else:
            print(f"Unknown strategy: {args.strategy}")
            sys.exit(1)
        
        # Configure strategy
        strategy.set_logger(platform.get_logger())
        strategy.set_platform(platform)
        
        # Run backtest
        platform.add_strat(strategy)
        platform.start()
        
        # Show results
        results = strategy.summary()
        print("\n=== Backtest Results ===")
        print(f"Total trades: {results['total_trades']}")
        print(f"Crossovers: {results['no_of_crossovers']}")
        print(f"Final P&L: {results['pnl']}")
        
    except Exception as e:
        print(f"Error during backtest: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
