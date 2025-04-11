# 🔐📊🌤️ FastAPI Backend – Auth + Binance + Weather API

This is a FastAPI-based backend service that supports:

- ✅ User Authentication (Register, Login, Profile Management)
- 🔐 Google Login (Simulated)
- 📉 Real-time Crypto Data from Binance API
- 🌤️ Weather Data from Data.gov.sg
- 🖼️ Image Upload & Profile Picture Support
- 🧪 Auto-generated API documentation with Swagger and ReDoc

---

## 🚀 Live API Endpoint

**Base URL:**  
`https://fastapi-cy6x.onrender.com`

---

## 📚 API Docs

- Swagger UI: [`/docs`](https://fastapi-cy6x.onrender.com/docs)
- ReDoc: [`/redoc`](https://fastapi-cy6x.onrender.com/redoc)

---

## 📦 Project Structure

```bash
.
├── main.py                  # Main FastAPI application entry point
├── routers/
│   ├── auth.py              # Authentication & user profile management
│   ├── coin.py              # Binance cryptocurrency endpoints
│   └── weather.py           # Weather data from Data.gov.sg
└──                  
```

---

## ⚙️ Running Locally

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Server

```bash
uvicorn main:app --reload --port 10000
```

Then open `http://127.0.0.1:10000/docs` in your browser.

---

## 🔐 Authentication

This backend uses JWT tokens for authentication. Use the `/auth/login` or `/auth/google-login` endpoint to obtain a token and send it as a query parameter (`?token=...`) for authenticated routes.

---

## ✨ Endpoints Overview

### Auth
- `POST /auth/register`
- `POST /auth/login`
- `POST /auth/google-login`
- `GET /auth/me`
- `POST /auth/edit`
- `POST /auth/upload-photo`
- `POST /auth/logout`

### Crypto
- `GET /coins/` — All coins
- `GET /coins/{symbol}` — Specific coin info
- `GET /coins/{symbol}/graph` — 24h price trend graph (PNG image)

### Weather
- `GET /weather/` — Latest temperature data from Singapore

---

## 🔐 Sample Token Flow

```bash
# Register
curl -X POST -d "email=test@example.com&name=TestUser&password=1234" https://fastapi-cy6x.onrender.com/auth/register

# Login
curl -X POST -d "email=test@example.com&password=1234" https://fastapi-cy6x.onrender.com/auth/login

# Use returned access_token as ?token=YOUR_TOKEN in authenticated routes
```

---

## 📸 Uploads

User-uploaded images are saved in the `/static/` directory and paths are returned via `/auth/upload-photo`.

---

## 🛡️ Tech Stack

- **FastAPI** – Web Framework
- **Uvicorn** – ASGI Server
- **JWT** – Token-Based Authentication
- **PassLib** – Password Hashing
- **Requests** – External API Calls
- **Matplotlib** – Coin Graph Generation

---

## 📩 Contact

Developed by Juvana   
Feel free to report issues or suggest improvements!