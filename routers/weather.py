# import requests
# from fastapi import APIRouter

# router = APIRouter()

# @router.get("/")
# def get_weather_data():
#     res = requests.get("https://api.data.gov.sg/v1/environment/air-temperature")
#     return res.json()
import requests
from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Optional

router = APIRouter()

@router.get("/weather", response_model=List[Dict[str, str]])
def get_weather_data(location: Optional[str] = Query(None, description="Filter by location name")):
    try:
        res = requests.get("https://api.data.gov.sg/v1/environment/air-temperature")
        res.raise_for_status()
        data = res.json()

        stations = data.get("metadata", {}).get("stations", [])
        readings = data.get("items", [{}])[0].get("readings", [])
        timestamp = data.get("items", [{}])[0].get("timestamp", "")

        # Create a lookup for station_id -> full station data
        station_lookup = {s["id"]: s for s in stations}

        result = []
        for reading in readings:
            station_id = reading.get("station_id")
            value = reading.get("value")
            station = station_lookup.get(station_id)

            if not station or value is None:
                continue

            name = station.get("name", "Unknown")
            lat = station.get("location", {}).get("latitude")
            lon = station.get("location", {}).get("longitude")

            # Filter by location query if provided
            if location and location.lower() not in name.lower():
                continue

            result.append({
                "location": name,
                "temperature": f"{value:.1f}°C",
                "latitude": str(lat),
                "longitude": str(lon),
                "timestamp": timestamp
            })

        return result

    except requests.RequestException:
        raise HTTPException(status_code=502, detail="Error connecting to weather service")
    except Exception:
        raise HTTPException(status_code=500, detail="Unexpected data format from weather API")
