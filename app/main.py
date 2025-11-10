from fastapi import FastAPI
from app.database import init_pool
from app.routers import users, transactions, portfolio, prices, auth, admin
from app.utils.scheduler import start_scheduler

app = FastAPI(
    title="WealthWise Portfolio Tracker API",
    version="1.0.0",
    description="Investment portfolio tracking system for stocks and mutual funds",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

@app.on_event("startup")
def startup():
    init_pool()
    start_scheduler()

app.include_router(auth.router, tags=["Authentication"])
app.include_router(users.router, tags=["Users"])
app.include_router(transactions.router, tags=["Transactions"])
app.include_router(portfolio.router, tags=["Portfolio"])
app.include_router(prices.router, tags=["Prices"])
app.include_router(admin.router, tags=["Admin"])

@app.get("/", tags=["Root"])
def root():
    return {
        "message": "WealthWise Portfolio Tracker API",
        "version": "1.0.0",
        "docs": "/docs",
        "openapi": "/openapi.json"
    }

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy"}
    