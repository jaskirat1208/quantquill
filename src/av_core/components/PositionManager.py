from enum import Enum
from strats.BaseStrat import OHLCQuote
from datetime import datetime

class Side(Enum):
    BUY = "BUY"
    SELL = "SELL"

class Trade:    
    def __init__(self, token: str, quantity: float = 0, price: float = 0, side: Side = Side.BUY, timestamp: int = 0, trade_id: int = 0, tx_cost: int = 0):
        self.token = token
        self.quantity = quantity
        self.price = price
        self.side = side
        self.timestamp = timestamp
        self.trade_id = trade_id
        self.tx_cost = tx_cost

    def __repr__(self):
        return f"Trade(token={self.token}, quantity={self.quantity}, price={self.price}, side={self.side}, timestamp={self.timestamp}, trade_id={self.trade_id}, tx_cost={self.tx_cost})"


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
        curr_qty = self.quantity
        self.tx_costs += trade.tx_cost
        if(trade.side == Side.BUY):
            self.quantity += trade.quantity
            self.total_buy_value += trade.quantity * trade.price
            self.total_buy_qty += trade.quantity
        elif(trade.side == Side.SELL):
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
    def __init__(self):
        self.positions = {}
        self.trades = []

    def book_trade(self, trade: Trade):
        if trade.token not in self.positions:
            self.positions[trade.token] = Position(trade.token)
        
        self.positions[trade.token].on_trade(trade)
        self.trades.append(trade)
    
    def on_md(self, md: OHLCQuote):
        # Update Unrealized PnL based on current market data
        # md should be a dictionary/object with token and current_price
        for tok, pos in self.positions.items():
            pos.on_md(md)

    
    def get_position(self, token):
        return self.positions.get(token)
    
    def get_positions(self):
        return self.positions
    

if __name__ == "__main__":
    pm = PositionManager()
    pm.book_trade(Trade("BTC", 5, 50000, Side.BUY, 1, 1, 10))
    pm.book_trade(Trade("BTC", 1, 51000, Side.SELL, 2, 2, 10))
    quote = OHLCQuote("BTC", 2, 50500, 50500, 49500, 50500, 2)
    print(quote)
    pm.on_md(quote)
    print(pm.get_position("BTC"))