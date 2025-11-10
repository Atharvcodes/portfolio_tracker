from datetime import date
from app.repositories.transaction_repository import TransactionRepository
from app.repositories.user_repository import UserRepository
from app.repositories.price_repository import PriceRepository
from app.services.portfolio_service import PortfolioService
from app.utils.exceptions import (
    UserNotFoundException, InsufficientHoldingsException,
    InvalidSymbolException, FutureDateException
)

class TransactionService:
    def __init__(self):
        self.transaction_repo = TransactionRepository()
        self.user_repo = UserRepository()
        self.price_repo = PriceRepository()
        self.portfolio_service = PortfolioService()
    
    def create_transaction(self, user_id: int, symbol: str, transaction_type: str,
                          units: int, price: float, transaction_date: date):
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundException(f"User {user_id} not found")
        
        symbol = symbol.upper()
        symbol_price = self.price_repo.get_by_symbol(symbol)
        if not symbol_price:
            raise InvalidSymbolException(f"Symbol {symbol} not found")
        
        if transaction_date > date.today():
            raise FutureDateException("Transaction date cannot be in the future")
        
        if transaction_type == 'SELL':
            holdings = self.portfolio_service.calculate_holdings(user_id)
            current_units = holdings.get(symbol, {}).get('total_units', 0)
            
            if current_units < units:
                raise InsufficientHoldingsException(
                    f"Insufficient holdings for {symbol}. Available: {current_units}, Requested: {units}"
                )
        
        return self.transaction_repo.create(
            user_id, symbol, transaction_type, units, price, transaction_date
        )
