from pydantic import BaseModel
from typing import List

class HoldingDetail(BaseModel):
    symbol: str
    total_units: int
    average_cost: float
    current_price: float
    current_value: float
    unrealized_pl: float
    unrealized_pl_percent: float

class PortfolioSummaryResponse(BaseModel):
    user_id: int
    total_invested: float
    current_value: float
    total_pl: float
    total_pl_percent: float
    holdings: List[HoldingDetail]
