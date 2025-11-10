from pydantic import BaseModel, field_validator
from datetime import date, datetime
from typing import Literal

class TransactionCreate(BaseModel):
    user_id: int
    symbol: str
    transaction_type: Literal["BUY", "SELL"]
    units: int
    price: float
    transaction_date: date
    
    @field_validator('symbol')
    @classmethod
    def validate_symbol(cls, v):
        return v.upper()
    
    @field_validator('units')
    @classmethod
    def validate_units(cls, v):
        if v <= 0:
            raise ValueError('Units must be positive')
        return v
    
    @field_validator('price')
    @classmethod
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError('Price must be positive')
        return round(v, 2)
    
    @field_validator('transaction_date')
    @classmethod
    def validate_date(cls, v):
        if v > date.today():
            raise ValueError('Transaction date cannot be in the future')
        return v

class TransactionResponse(BaseModel):
    transaction_id: int
    user_id: int
    symbol: str
    transaction_type: str
    units: int
    price: float
    transaction_date: date
    created_at: datetime
