from apscheduler.schedulers.background import BackgroundScheduler
import random
from app.repositories.price_repository import PriceRepository
from app.services.cache_service import invalidate_cache

price_repo = PriceRepository()
scheduler = BackgroundScheduler()

def update_prices_job():
    try:
        prices = price_repo.get_all()
        
        for symbol, current_price in prices.items():
            fluctuation = random.uniform(-0.05, 0.05)
            new_price = current_price * (1 + fluctuation)
            new_price = round(new_price, 2)
            
            price_repo.update(symbol, new_price)
        
        invalidate_cache("portfolio:*")
        
        print(f"Updated {len(prices)} stock prices")
    except Exception as e:
        print(f"Price update job failed: {e}")

def start_scheduler():
    scheduler.add_job(
        update_prices_job,
        'interval',
        seconds=60,
        id='update_prices'
    )
    scheduler.start()
    print("Background scheduler started - prices will update every 60 seconds")

def trigger_price_update():
    update_prices_job()
    return {"message": "Price update triggered successfully"}
