from fastapi import FastAPI, Depends
from auth import verify_token, create_token
from rate_limiter import check_rate_limit
from data_fetcher import fetch_market_data
from ai_analyzer import analyze_with_ai
from utils import validate_sector

app = FastAPI(title="Trade Opportunities API")
users = {"admin": "password"}

@app.get("/")
def home():
    return {"message": "Trade Opportunities API Running"}

@app.post("/login")
def login(username: str, password: str):
    if username in users and users[username] == password:
        token = create_token(username)
        return {"access_token": token}
    return {"error": "Invalid credentials"}

@app.get("/analyze/{sector}")
async def analyze_sector(sector: str, user: str = Depends(verify_token)):
    validate_sector(sector)
    check_rate_limit(user)
    data = await fetch_market_data(sector)
    report = await analyze_with_ai(sector, data)

    return {
        "sector": sector,
        "report": report
    }
