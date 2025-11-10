from fastapi import APIRouter, HTTPException, Query, status
from typing import Optional
from app.schemas.transaction import TransactionCreate, TransactionResponse
from app.services.transaction_service import TransactionService
from app.services.cache_service import invalidate_cache
from app.utils.exceptions import (
    UserNotFoundException, InsufficientHoldingsException,
    InvalidSymbolException, FutureDateException
)

router = APIRouter(prefix="/transactions")
transaction_service = TransactionService()

@router.post("", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def create_transaction(transaction: TransactionCreate):
    try:
        result = transaction_service.create_transaction(
            transaction.user_id,
            transaction.symbol,
            transaction.transaction_type,
            transaction.units,
            transaction.price,
            transaction.transaction_date
        )
        
        invalidate_cache(f"portfolio:{transaction.user_id}")
        
        return TransactionResponse(**result)
    except UserNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except InvalidSymbolException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except InsufficientHoldingsException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except FutureDateException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("", response_model=list[TransactionResponse])
def get_transactions(
    user_id: int = Query(..., description="User ID to get transactions for"),
    symbol: Optional[str] = Query(None, description="Filter by symbol")
):
    if symbol:
        transactions = transaction_service.transaction_repo.get_by_user_and_symbol(user_id, symbol)
    else:
        transactions = transaction_service.transaction_repo.get_by_user(user_id)
    
    return [TransactionResponse(**txn) for txn in transactions]
