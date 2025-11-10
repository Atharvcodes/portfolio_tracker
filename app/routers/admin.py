from fastapi import APIRouter
from app.utils.scheduler import trigger_price_update

router = APIRouter(prefix="/admin")

@router.post("/update-prices")
def manual_price_update():
    return trigger_price_update()
