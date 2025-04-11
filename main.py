from fastapi import FastAPI
from routers.auth import router as auth_router
from routers.coin import router as coin_router
from routers.weather import router as weather_router

app = FastAPI(title="Authentication + Binance + Weather API")

app.include_router(auth_router, prefix="/auth")
app.include_router(coin_router, prefix="/coins")
app.include_router(weather_router, prefix="/weather")