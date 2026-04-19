import unittest
import sys
import os


from quantquill.av_core.components.PositionManager import PositionManager, Trade, Side, Position
from quantquill.strats.BaseStrat import OHLCQuote


class TestPositionManager(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.pm = PositionManager()
    
    def test_buy_long_position(self):
        """Test buying and creating a long position."""
        trade = Trade("BTC", 10, 50000, Side.BUY, 1, 1, 0)
        self.pm.book_trade(trade)
        
        position = self.pm.get_position("BTC")
        self.assertEqual(position.quantity, 10)
        self.assertEqual(position.avg_price, 50000)
        self.assertEqual(position.total_buy_value, 500000)
        self.assertEqual(position.total_buy_qty, 10)
    
    def test_sell_short_position(self):
        """Test selling and creating a short position."""
        trade = Trade("BTC", 5, 50000, Side.SELL, 1, 1, 0)
        self.pm.book_trade(trade)
        
        position = self.pm.get_position("BTC")
        self.assertEqual(position.quantity, -5)
        self.assertEqual(position.avg_price, 50000)
        self.assertEqual(position.total_sell_value, 250000)
        self.assertEqual(position.total_sell_qty, 5)
    
    def test_partial_close_long_position(self):
        """Test partially closing a long position."""
        # Buy 10 BTC at 50000
        self.pm.book_trade(Trade("BTC", 10, 50000, Side.BUY, 1, 1, 0))
        # Sell 3 BTC at 51000 (partial close)
        self.pm.book_trade(Trade("BTC", 3, 51000, Side.SELL, 2, 2, 0))
        
        position = self.pm.get_position("BTC")
        self.assertEqual(position.quantity, 7)  # 10 - 3
        self.assertEqual(position.avg_price, 50000)  # Should remain 50000
        
        # Check realized P&L: (51000 - 50000) * 3 = 30000
        expected_realized = 3000
        self.assertEqual(position.realized_pnl, expected_realized)
    
    def test_partial_close_short_position(self):
        """Test partially closing a short position."""
        # Short sell 8 BTC at 50000
        self.pm.book_trade(Trade("BTC", 8, 50000, Side.SELL, 1, 1, 0))
        # Buy back 3 BTC at 49000 (partial close)
        self.pm.book_trade(Trade("BTC", 3, 49000, Side.BUY, 2, 2, 0))
        
        position = self.pm.get_position("BTC")
        self.assertEqual(position.quantity, -5)  # -8 + 3
        self.assertEqual(position.avg_price, 50000)
        
        # Check realized P&L: (50000 - 49000) * 3 = 3000
        expected_realized = 3000
        self.assertEqual(position.realized_pnl, expected_realized)
    
    def test_full_close_long_position(self):
        """Test fully closing a long position."""
        # Buy 5 BTC at 50000
        self.pm.book_trade(Trade("BTC", 5, 50000, Side.BUY, 1, 1, 0))
        # Sell 5 BTC at 52000 (full close)
        self.pm.book_trade(Trade("BTC", 5, 52000, Side.SELL, 2, 2, 0))
        
        position = self.pm.get_position("BTC")
        self.assertEqual(position.quantity, 0)
        self.assertEqual(position.avg_price, 0)
        
        # Check realized P&L: (52000 - 50000) * 5 = 100000
        expected_realized = 10000
        self.assertEqual(position.realized_pnl, expected_realized)
    
    def test_full_close_short_position(self):
        """Test fully closing a short position."""
        # Short sell 5 BTC at 50000
        self.pm.book_trade(Trade("BTC", 5, 50000, Side.SELL, 1, 1, 0))
        # Buy back 5 BTC at 48000 (full close)
        self.pm.book_trade(Trade("BTC", 5, 48000, Side.BUY, 2, 2, 0))
        
        position = self.pm.get_position("BTC")
        self.assertEqual(position.quantity, 0)
        self.assertEqual(position.avg_price, 0)
        
        # Check realized P&L: (50000 - 48000) * 5 = 10000
        expected_realized = 10000
        self.assertEqual(position.realized_pnl, expected_realized)
    
    def test_add_to_long_position(self):
        """Test adding to an existing long position."""
        # Buy 5 BTC at 50000
        self.pm.book_trade(Trade("BTC", 5, 50000, Side.BUY, 1, 1, 0))
        # Buy 3 more BTC at 52000
        self.pm.book_trade(Trade("BTC", 3, 52000, Side.BUY, 2, 2, 0))
        
        position = self.pm.get_position("BTC")
        self.assertEqual(position.quantity, 8)
        
        # Average price should be: (50000*5 + 52000*3) / 8 = 50750
        expected_avg_price = (50000*5 + 52000*3) / 8
        self.assertEqual(position.avg_price, expected_avg_price)
        
        # No realized P&L when adding to position
        self.assertEqual(position.realized_pnl, 0)
    
    def test_add_to_short_position(self):
        """Test adding to an existing short position."""
        # Short sell 5 BTC at 50000
        self.pm.book_trade(Trade("BTC", 5, 50000, Side.SELL, 1, 1, 0))
        # Short sell 3 more BTC at 52000
        self.pm.book_trade(Trade("BTC", 3, 52000, Side.SELL, 2, 2, 0))
        
        position = self.pm.get_position("BTC")
        self.assertEqual(position.quantity, -8)
        
        # Average price should be: (50000*5 + 52000*3) / 8 = 50750
        expected_avg_price = (50000*5 + 52000*3) / 8
        self.assertEqual(position.avg_price, expected_avg_price)
        
        # No realized P&L when adding to position
        self.assertEqual(position.realized_pnl, 0)
    
    def test_unrealized_pnl_long_position(self):
        """Test unrealized P&L calculation for long position."""
        # Buy 10 BTC at 50000
        self.pm.book_trade(Trade("BTC", 10, 50000, Side.BUY, 1, 1, 0))
        
        # Update with market data at 52000
        quote = OHLCQuote("BTC", 1, 52000, 52500, 51500, 52000, 100)
        self.pm.on_md(quote)
        
        position = self.pm.get_position("BTC")
        # Unrealized P&L: (52000 - 50000) * 10 = 200000
        expected_unrealized = 20000
        self.assertEqual(position.unrealized_pnl, expected_unrealized)
    
    def test_unrealized_pnl_short_position(self):
        """Test unrealized P&L calculation for short position."""
        # Short sell 10 BTC at 50000
        self.pm.book_trade(Trade("BTC", 10, 50000, Side.SELL, 1, 1, 0))
        
        # Update with market data at 48000
        quote = OHLCQuote("BTC", 1, 48000, 48500, 47500, 48000, 100)
        self.pm.on_md(quote)
        
        position = self.pm.get_position("BTC")
        # Unrealized P&L: (50000 - 48000) * 10 = 200000
        expected_unrealized = 20000
        self.assertEqual(position.unrealized_pnl, expected_unrealized)
    
    def test_transaction_costs(self):
        """Test transaction costs are properly accounted for."""
        # Buy with transaction cost
        self.pm.book_trade(Trade("BTC", 5, 50000, Side.BUY, 1, 1, 100))
        # Sell with transaction cost
        self.pm.book_trade(Trade("BTC", 5, 52000, Side.SELL, 2, 2, 100))
        
        position = self.pm.get_position("BTC")
        
        # Total P&L should account for transaction costs
        # (52000 - 50000) * 5 - 100 - 100 = 100000 - 200 = 99800
        expected_total_pnl = 9800
        self.assertEqual(position.total_pnl, expected_total_pnl)
        self.assertEqual(position.tx_costs, 200)
    
    def test_multiple_tokens(self):
        """Test managing positions for multiple tokens."""
        # Trade BTC
        self.pm.book_trade(Trade("BTC", 10, 50000, Side.BUY, 1, 1, 0))
        # Trade ETH
        self.pm.book_trade(Trade("ETH", 100, 3000, Side.BUY, 1, 1, 0))
        
        btc_position = self.pm.get_position("BTC")
        eth_position = self.pm.get_position("ETH")
        
        self.assertEqual(btc_position.quantity, 10)
        self.assertEqual(btc_position.avg_price, 50000)
        self.assertEqual(eth_position.quantity, 100)
        self.assertEqual(eth_position.avg_price, 3000)
        
        # Check both positions are tracked
        positions = self.pm.get_positions()
        self.assertEqual(len(positions), 2)
        self.assertIn("BTC", positions)
        self.assertIn("ETH", positions)
    
    def test_position_flip_long_to_short(self):
        """Test flipping from long to short position."""
        # Buy 5 BTC at 50000
        self.pm.book_trade(Trade("BTC", 5, 50000, Side.BUY, 1, 1, 0))
        # Sell 8 BTC at 52000 (flip to short)
        self.pm.book_trade(Trade("BTC", 8, 52000, Side.SELL, 2, 2, 0))
        
        position = self.pm.get_position("BTC")
        self.assertEqual(position.quantity, -3)  # 5 - 8 = -3 (short)
        self.assertEqual(position.avg_price, 52000)  # Should be sell price now
        
        # Should have realized P&L from closing the long position
        # (52000 - 50000) * 5 = 100000
        expected_realized = 10000
        self.assertEqual(position.realized_pnl, expected_realized)
    
    def test_position_flip_short_to_long(self):
        """Test flipping from short to long position."""
        # Short sell 5 BTC at 50000
        self.pm.book_trade(Trade("BTC", 5, 50000, Side.SELL, 1, 1, 0))
        # Buy 8 BTC at 48000 (flip to long)
        self.pm.book_trade(Trade("BTC", 8, 48000, Side.BUY, 2, 2, 0))
        
        position = self.pm.get_position("BTC")
        self.assertEqual(position.quantity, 3)  # -5 + 8 = 3 (long)
        self.assertEqual(position.avg_price, 48000)  # Should be buy price now
        
        # Should have realized P&L from closing the short position
        # (50000 - 48000) * 5 = 100000
        expected_realized = 10000
        self.assertEqual(position.realized_pnl, expected_realized)
    
    def test_zero_quantity_position(self):
        """Test handling of zero quantity positions."""
        # Create and immediately close position
        self.pm.book_trade(Trade("BTC", 5, 50000, Side.BUY, 1, 1, 0))
        self.pm.book_trade(Trade("BTC", 5, 50000, Side.SELL, 2, 2, 0))
        
        position = self.pm.get_position("BTC")
        self.assertEqual(position.quantity, 0)
        self.assertEqual(position.avg_price, 0)
        self.assertEqual(position.unrealized_pnl, 0)
    
    def test_market_data_update_no_position(self):
        """Test market data update when no position exists."""
        # Update market data without any trades
        quote = OHLCQuote("BTC", 1, 50000, 51000, 49000, 50500, 100)
        self.pm.on_md(quote)
        
        # Should not create a position
        position = self.pm.get_position("BTC")
        self.assertIsNone(position)


class TestPosition(unittest.TestCase):
    
    def test_position_initialization(self):
        """Test Position class initialization."""
        # Test with positive quantity (long)
        pos_long = Position("BTC", 10, 50000)
        self.assertEqual(pos_long.quantity, 10)
        self.assertEqual(pos_long.avg_price, 50000)
        self.assertEqual(pos_long.total_buy_value, 500000)
        self.assertEqual(pos_long.total_buy_qty, 10)
        self.assertEqual(pos_long.total_sell_value, 0)
        self.assertEqual(pos_long.total_sell_qty, 0)
        
        # Test with negative quantity (short)
        pos_short = Position("BTC", -5, 50000)
        self.assertEqual(pos_short.quantity, -5)
        self.assertEqual(pos_short.avg_price, 50000)
        self.assertEqual(pos_short.total_buy_value, 0)
        self.assertEqual(pos_short.total_buy_qty, 0)
        self.assertEqual(pos_short.total_sell_value, 250000)
        self.assertEqual(pos_short.total_sell_qty, 5)
    
    def test_position_repr(self):
        """Test Position string representation."""
        pos = Position("BTC", 10, 50000)
        repr_str = repr(pos)
        self.assertIn("BTC", repr_str)
        self.assertIn("10", repr_str)
        self.assertIn("50000", repr_str)


class TestTrade(unittest.TestCase):
    
    def test_trade_creation(self):
        """Test Trade object creation."""
        trade = Trade("BTC", 10, 50000, Side.BUY, 1234567890, 1, 50)
        
        self.assertEqual(trade.token, "BTC")
        self.assertEqual(trade.quantity, 10)
        self.assertEqual(trade.price, 50000)
        self.assertEqual(trade.side, Side.BUY)
        self.assertEqual(trade.timestamp, 1234567890)
        self.assertEqual(trade.trade_id, 1)
        self.assertEqual(trade.tx_cost, 50)
    
    def test_trade_repr(self):
        """Test Trade string representation."""
        trade = Trade("BTC", 10, 50000, Side.BUY, 1234567890, 1, 50)
        repr_str = repr(trade)
        self.assertIn("BTC", repr_str)
        self.assertIn("10", repr_str)
        self.assertIn("50000", repr_str)
        self.assertIn("BUY", repr_str)
        self.assertIn("50", repr_str)


if __name__ == '__main__':
    unittest.main()