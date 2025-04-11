import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from routers.auth import router as auth_router
from routers.coin import router as coin_router
from routers.weather import router as weather_router

app = FastAPI(title="Authentication + Binance + Weather API")

app.include_router(auth_router, prefix="/auth")
app.include_router(coin_router, prefix="/coins")
app.include_router(weather_router, prefix="/weather")

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <html>
        <head>
            <title>Welcome</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    text-align: center;
                    padding-top: 100px;
                    background-color: #f0f0f0;
                }
                h1 {
                    color: #333;
                }
                .btn {
                    display: inline-block;
                    margin: 10px;
                    padding: 10px 20px;
                    font-size: 16px;
                    color: white;
                    background-color: #007bff;
                    border: none;
                    border-radius: 5px;
                    text-decoration: none;
                }
                .btn:hover {
                    background-color: #0056b3;
                }
            </style>
        </head>
        <body>
            <h1>Welcome to the API</h1>
            <p>Use the buttons below to explore the API documentation:</p>
            <a href="/docs" class="btn">Swagger UI</a>
            <a href="/redoc" class="btn">ReDoc</a>
        </body>
    </html>
    """

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=10000, reload=True)
