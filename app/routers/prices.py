from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from app.repositories.price_repository import PriceRepository

router = APIRouter(prefix="/prices")
price_repo = PriceRepository()

class PriceUpdate(BaseModel):
    price: float

@router.get("/{symbol}")
def get_price(symbol: str):
    price = price_repo.get_by_symbol(symbol)
    if not price:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Symbol {symbol} not found"
        )
    return price

@router.put("/{symbol}")
def update_price(symbol: str, update: PriceUpdate):
    result = price_repo.update(symbol, update.price)
    return result

@router.get("")
def get_all_prices():
    prices = price_repo.get_all()
    return {"prices": prices}
