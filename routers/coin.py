import requests
from fastapi import APIRouter, HTTPException, Response
import matplotlib.pyplot as plt
from io import BytesIO
from datetime import datetime

router = APIRouter()

@router.get("/")
def get_all_coins():
    res = requests.get("https://api.binance.com/api/v3/ticker/24hr")
    return res.json()[:100]  # ✅ Limit to 100 coins

@router.get("/{symbol}")
def get_coin(symbol: str):
    res = requests.get(f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol.upper()}")
    if res.status_code != 200:
        return {"error": "Invalid symbol"}
    data = res.json()
    trend = "Up" if float(data['priceChangePercent']) >= 0 else "Down"
    return {
        "symbol": symbol.upper(),
        "price": data["lastPrice"],
        "trend": trend,
        "change_percent": data["priceChangePercent"]
    }

@router.get("/{symbol}/graph")
def get_coin_graph(symbol: str):
    try:
        url = f"https://api.binance.com/api/v3/klines?symbol={symbol.upper()}&interval=1h&limit=24"
        res = requests.get(url)
        if res.status_code != 200:
            raise HTTPException(status_code=404, detail="Could not fetch coin data")

        kline_data = res.json()
        timestamps = [datetime.fromtimestamp(candle[0]/1000).strftime('%H:%M') for candle in kline_data]
        prices = [float(candle[4]) for candle in kline_data]  # Closing prices

        plt.figure(figsize=(10, 4))
        plt.plot(timestamps, prices, marker='o')
        plt.title(f"{symbol.upper()} - Last 24H Price Trend")
        plt.xlabel("Time")
        plt.ylabel("Price (USDT)")
        plt.xticks(rotation=45)
        plt.tight_layout()

        buf = BytesIO()
        plt.savefig(buf, format="png")
        plt.close()
        buf.seek(0)
        return Response(content=buf.read(), media_type="image/png")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
