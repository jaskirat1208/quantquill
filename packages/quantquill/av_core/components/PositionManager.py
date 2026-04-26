from enum import Enum
from quantquill.types import OHLCQuote, Trade
from typing import Optional
from datetime import datetime

class Side(Enum):
    BUY = "BUY"
    SELL = "SELL"

class Position:  
    def __init__(self, token: str, quantity: float = 0, avg_price: float = 0):
        self.token = token
        self.quantity = quantity
        self.avg_price = avg_price
        self.unrealized_pnl = 0
        self.realized_pnl = 0
        self.total_buy_value = 0
        self.total_buy_qty = 0
        self.total_sell_value = 0
        self.total_sell_qty = 0
        self.total_pnl = 0
        self.tx_costs = 0
    
        if(quantity > 0):
            self.total_buy_value += quantity * avg_price
            self.total_buy_qty += quantity
        if(quantity < 0):
            self.total_sell_value += abs(quantity) * avg_price
            self.total_sell_qty += abs(quantity)
    
    def on_trade(self, trade: Trade):
        # TODO: Implement trade booking logic
        curr_price = trade.price
        self.tx_costs += trade.tx_cost
        if(str(trade.side) == Side.BUY.value):
            self.quantity += trade.quantity
            self.total_buy_value += trade.quantity * trade.price
            self.total_buy_qty += trade.quantity
        elif(str(trade.side) == Side.SELL.value):
            self.quantity -= trade.quantity
            self.total_sell_value += trade.quantity * trade.price
            self.total_sell_qty += trade.quantity
        
        self.total_pnl = self.total_sell_value + self.quantity * curr_price - self.total_buy_value - self.tx_costs
        if(self.quantity > 0):
            self.avg_price = self.total_buy_value / self.total_buy_qty
        elif(self.quantity < 0):
            self.avg_price = self.total_sell_value / self.total_sell_qty
        else:
            self.avg_price = 0
        self.unrealized_pnl = self.quantity * (curr_price - self.avg_price)
        self.realized_pnl = self.total_pnl - self.unrealized_pnl

    
            

    def on_md(self, md: OHLCQuote):
        # TODO: Implement market data update logic
        self.unrealized_pnl = self.quantity * (md.close_price - self.avg_price)        

    def __repr__(self):
        return f"Position(token={self.token}, quantity={self.quantity}, avg_price={self.avg_price}, unrealized_pnl={self.unrealized_pnl}, realized_pnl={self.realized_pnl})"

class PositionManager:
    def __init__(self, max_capital = 10000000000):
        self.positions: dict[str, Position] = {}
        self.cash_available = max_capital
        self.trades = []
        self.risk_manager = PortfolioRiskManager(self)
        self.starting_cash = max_capital

    def set_total_capital(self, capital: float):
        self.cash_available = capital
        self.starting_cash = capital

    def book_trade(self, trade: Trade):
        if trade.token not in self.positions:
            self.positions[trade.token] = Position(trade.token)

        if(not self.risk_manager.trade_allowed(trade)):
            raise "Trade not permitted. You don't have enough funds to trade."

        self.cash_available -= trade.quantity * trade.price if str(trade.side) == Side.BUY.value else -trade.quantity * trade.price
        self.positions[trade.token].on_trade(trade)
        self.risk_manager.add_snapshot()
        self.trades.append(trade)
        print(self.positions)
    
    def on_md(self, md: OHLCQuote):
        # Update Unrealized PnL based on current market data
        # md should be a dictionary/object with token and current_price
        for tok, pos in self.positions.items():
            pos.on_md(md)

        self.risk_manager.on_md(md)
    
    def get_position(self, token):
        return self.positions.get(token)
    
    def get_positions(self):
        return self.positions

    def get_trades(self):
        return self.trades

    def calculate_risk(self):
        return self.risk_manager.calculateRisk()

    def get_cash_available(self):
        return self.cash_available

class PortfolioRiskManager:
    def __init__(self, position_manager: PositionManager):
        self.position_manager = position_manager
        self.ltp: dict[str, float] = {}
        self.positions: dict[str, Position] = {}
        self.portfolio_snapshots = []
        self.last_quote_time: Optional[datetime] = None

    def add_snapshot(self):
        snapshot_dict = {
            "total_value": self.position_manager.get_cash_available(),
            "timestamp": self.last_quote_time
        }

        for token, position in self.position_manager.get_positions().items():
            snapshot_dict[token] = {
                "quantity": position.quantity,
                "avg_price": position.avg_price,
            }
            snapshot_dict['total_value'] += position.quantity * self.ltp[token]

        snapshot_dict['pnl'] = snapshot_dict['total_value'] - self.position_manager.starting_cash
        self.portfolio_snapshots.append(snapshot_dict)
    
    def on_md(self, md: OHLCQuote):
        self.ltp[md.symbol] = md.close_price
        self.last_quote_time = datetime.fromisoformat(md.timestamp)

    def calculateRisk(self):
        print("Calculating Total portfolio value")
        positions = self.position_manager.get_positions()
        print(f"Positions: {positions}")
        pf_value = self.position_manager.get_cash_available()
        for(token, position) in positions.items():
            pf_value += position.quantity * self.ltp[token]

        self.total_capital = pf_value

        return {
            "total_value": pf_value,
            "max_drawdown": self._calculate_max_drawdown(self.portfolio_snapshots),
            "volatility": self._calculate_volatility(self.portfolio_snapshots),
            "sharpe_ratio": self._calculate_sharpe_ratio(self.portfolio_snapshots),
            "pnl": pf_value - self.position_manager.starting_cash,
            "snapshots": self.portfolio_snapshots
        }

    def trade_allowed(self, trade: Trade):
        curr_position = self.position_manager.get_position(trade.token)
        new_position = (trade.quantity if str(trade.side) == Side.BUY.value else -trade.quantity) + (curr_position.quantity if curr_position else 0)
        if(new_position < 0):
            print(f"Trade not allowed: {trade.token} {trade.quantity} {curr_position.quantity}")
            return False
        
        if(self.position_manager.get_cash_available() < trade.price * trade.quantity):
            print(f"Trade not allowed: {trade.token} {trade.quantity} {self.position_manager.get_cash_available()}")
            return False
        
        return True

    def _calculate_max_drawdown(self, snapshots):
        """Calculate maximum drawdown from portfolio snapshots"""
        peak = snapshots[0]['total_value']
        max_drawdown = 0.0
        
        for snapshot in snapshots:
            current_value = snapshot['total_value']
            if current_value > peak:
                peak = current_value
            
            drawdown = (peak - current_value) / peak * 100
            if drawdown > max_drawdown:
                max_drawdown = drawdown
        
        return max_drawdown
    
    def _calculate_volatility(self, snapshots):
        """Calculate portfolio volatility"""
        returns = []
        for i in range(1, len(snapshots)):
            prev_value = snapshots[i-1]['total_value']
            curr_value = snapshots[i]['total_value']
            if prev_value > 0:
                returns.append((curr_value - prev_value) / prev_value)
        
        if not returns:
            return 0.0
        
        mean_return = sum(returns) / len(returns)
        variance = sum((r - mean_return) ** 2 for r in returns) / len(returns)
        return (variance ** 0.5) * (252 ** 0.5) * 100  # Annualized volatility
    
    def _calculate_sharpe_ratio(self, snapshots):
        """Calculate Sharpe ratio"""
        returns = []
        for i in range(1, len(snapshots)):
            prev_value = snapshots[i-1]['total_value']
            curr_value = snapshots[i]['total_value']
            if prev_value > 0:
                returns.append((curr_value - prev_value) / prev_value)
        
        if not returns:
            return 0.0
        
        mean_return = sum(returns) / len(returns)
        volatility = self._calculate_volatility(snapshots) / 100
        risk_free_rate = 0.03 / 252  # Daily risk-free rate
        
        return (mean_return - risk_free_rate) / volatility if volatility > 0 else 0.0

        

            

if __name__ == "__main__":
    pm = PositionManager()
    pm.book_trade(Trade("BTC", 5, 50000, Side.BUY, 1, 1, 10))
    pm.book_trade(Trade("BTC", 1, 51000, Side.SELL, 2, 2, 10))
    quote = OHLCQuote("BTC", 2, 50500, 50500, 49500, 50500, 2)
    print(quote)
    pm.on_md(quote)
    print(pm.get_position("BTC"))