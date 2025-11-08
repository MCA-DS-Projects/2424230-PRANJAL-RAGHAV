from flask import Blueprint, request, jsonify
import requests, os
from datetime import datetime

location_bp = Blueprint("location", __name__)

LOCATION_KEY = os.getenv("LOCATIONIQ_KEY")
WEATHER_KEY  = os.getenv("WEATHER_KEY")


def find_season(month:int):
    if month in [3,4,5]: return "Spring"
    if month in [6,7,8]: return "Summer"
    if month in [9,10,11]: return "Fall"
    return "Winter"


# ----------------------------------------------------------------------------
#  1) Reverse geocode  (lat,lon -> formatted location string)
# ----------------------------------------------------------------------------
@location_bp.get("/api/reverse_geocode")
def reverse_geocode():
    lat = request.args.get("lat")
    lon = request.args.get("lon")

    if not lat or not lon:
        return {"error":"lat/lon missing"},400

    url = "https://us1.locationiq.com/v1/reverse"
    r = requests.get(url, params={
        "key": LOCATION_KEY,
        "lat": lat,
        "lon": lon,
        "format": "json"
    }).json()

    a = r.get("address",{})
    formatted = ", ".join([x for x in [
        a.get("city") or a.get("town") or a.get("village"),
        a.get("state"),
        a.get("country")
    ] if x])

    return {
        "formatted": formatted,
        "address": a
    }


# ----------------------------------------------------------------------------
# 2) Weather
# ----------------------------------------------------------------------------
@location_bp.get("/api/weather")
def weather():
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    place = request.args.get("place")

    # must give either lat+lon OR place text
    if (not lat or not lon) and not place:
        return {"error":"lat/lon or place must be provided"},400

    if place:
        url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_KEY}&q={place}"
    else:
        url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_KEY}&q={lat},{lon}"

    r = requests.get(url).json()
    current = r["current"]
    month = datetime.now().month

    return {
        "weather":{
            "temperature_f": current["temp_f"],
            "humidity": current["humidity"]
        },
        "season": find_season(month),
        "lat": r["location"]["lat"],
        "lon": r["location"]["lon"]
    }


# ----------------------------------------------------------------------------
# 3) City Auto Suggest
# ----------------------------------------------------------------------------
@location_bp.get("/api/suggest_cities")
def suggest_cities():
    q = request.args.get("q")
    if not q or len(q) < 2:
        return {"items":[]}

    url = "https://us1.locationiq.com/v1/autocomplete.php"
    r = requests.get(url, params={
        "key": LOCATION_KEY,
        "q": q,
        "limit": 5,
        "format": "json"
    }).json()

    items = []
    for c in r:
        addr = c.get("address",{})
        items.append({
            "name": addr.get("city") or addr.get("town") or addr.get("village"),
            "region": addr.get("state"),
            "country": addr.get("country")
        })

    return {"items": items}
