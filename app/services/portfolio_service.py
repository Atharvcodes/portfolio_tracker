from typing import Dict
from app.repositories.transaction_repository import TransactionRepository
from app.repositories.price_repository import PriceRepository
from app.schemas.portfolio import PortfolioSummaryResponse, HoldingDetail

class PortfolioService:
    def __init__(self):
        self.transaction_repo = TransactionRepository()
        self.price_repo = PriceRepository()
    
    def calculate_holdings(self, user_id: int) -> Dict[str, Dict]:
        transactions = self.transaction_repo.get_by_user(user_id)
        holdings = {}
        
        for txn in transactions:
            symbol = txn['symbol']
            if symbol not in holdings:
                holdings[symbol] = {
                    'total_buy_units': 0,
                    'total_buy_cost': 0.0,
                    'total_sell_units': 0
                }
            
            if txn['transaction_type'] == 'BUY':
                holdings[symbol]['total_buy_units'] += txn['units']
                holdings[symbol]['total_buy_cost'] += float(txn['units']) * float(txn['price'])
            else:
                holdings[symbol]['total_sell_units'] += txn['units']
        
        result = {}
        for symbol, data in holdings.items():
            current_units = data['total_buy_units'] - data['total_sell_units']
            if current_units > 0:
                avg_cost = data['total_buy_cost'] / float(data['total_buy_units'])
                result[symbol] = {
                    'total_units': current_units,
                    'average_cost': round(avg_cost, 2),
                    'cost_basis': round(avg_cost * float(current_units), 2)
                }
        
        return result
    
    def get_portfolio_summary(self, user_id: int) -> PortfolioSummaryResponse:
        holdings = self.calculate_holdings(user_id)
        prices = self.price_repo.get_all()
        
        total_invested = 0.0
        current_value = 0.0
        holding_details = []
        
        for symbol, data in holdings.items():
            current_price = float(prices.get(symbol, 0.0))
            units = float(data['total_units'])
            avg_cost = data['average_cost']
            
            value = current_price * units
            pl = (current_price - avg_cost) * units
            pl_percent = round((pl / data['cost_basis'] * 100), 2) if data['cost_basis'] > 0 else 0.0
            
            total_invested += data['cost_basis']
            current_value += value
            
            holding_details.append(HoldingDetail(
                symbol=symbol,
                total_units=data['total_units'],
                average_cost=avg_cost,
                current_price=current_price,
                current_value=round(value, 2),
                unrealized_pl=round(pl, 2),
                unrealized_pl_percent=pl_percent
            ))
        
        total_pl = current_value - total_invested
        total_pl_percent = round((total_pl / total_invested * 100), 2) if total_invested > 0 else 0.0
        
        return PortfolioSummaryResponse(
            user_id=user_id,
            total_invested=round(total_invested, 2),
            current_value=round(current_value, 2),
            total_pl=round(total_pl, 2),
            total_pl_percent=total_pl_percent,
            holdings=holding_details
        )
