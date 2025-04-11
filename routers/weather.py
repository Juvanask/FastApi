import requests
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_weather_data():
    res = requests.get("https://api.data.gov.sg/v1/environment/air-temperature")
    return res.json()