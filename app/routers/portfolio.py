from fastapi import APIRouter, HTTPException, Query, status
from app.schemas.portfolio import PortfolioSummaryResponse
from app.services.portfolio_service import PortfolioService
from app.services.cache_service import get_cache, set_cache
from app.repositories.user_repository import UserRepository

router = APIRouter(prefix="/portfolio-summary")
portfolio_service = PortfolioService()
user_repo = UserRepository()

@router.get("", response_model=PortfolioSummaryResponse)
def get_portfolio_summary(user_id: int = Query(..., description="User ID to get portfolio for")):
    user = user_repo.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found"
        )
    
    cache_key = f"portfolio:{user_id}"
    cached_data = get_cache(cache_key)
    
    if cached_data:
        return PortfolioSummaryResponse(**cached_data)
    
    result = portfolio_service.get_portfolio_summary(user_id)
    set_cache(cache_key, result.model_dump())
    
    return result
