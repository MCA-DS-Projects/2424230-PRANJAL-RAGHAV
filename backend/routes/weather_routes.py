# from flask import Blueprint, request, jsonify
# import requests, datetime

# weather_bp = Blueprint("weather", __name__)
# UA = {"User-Agent": "NutraExpertAI/1.0"}

# @weather_bp.get("/api/weather")
# def weather():
#     lat = request.args.get("lat")
#     lon = request.args.get("lon")
#     place = request.args.get("place")

#     # if user typed city
#     if place and not (lat and lon):
#         geo = requests.get("https://geocoding-api.open-meteo.com/v1/search",
#               params={"name":place,"count":1},headers=UA).json()
#         if not geo.get("results"):
#             return {"error":"place not found"},404
#         lat=geo["results"][0]["latitude"]
#         lon=geo["results"][0]["longitude"]

#     url="https://api.open-meteo.com/v1/forecast"
#     r=requests.get(url,params={
#         "latitude":lat,"longitude":lon,
#         "current":["temperature_2m","relative_humidity_2m"],
#         "timezone":"auto"
#     },headers=UA).json()

#     tempC = r["current"]["temperature_2m"]
#     hum = r["current"]["relative_humidity_2m"]
#     tempF = round((tempC*9/5)+32,1)

#     # small season logic
#     m=datetime.date.today().month
#     if m in (12,1,2):season="Winter"
#     elif m in (3,4,5):season="Spring"
#     elif m in (6,7,8):season="Summer"
#     else:season="Fall"

#     return {
#         "weather":{"temperature_f":tempF,"humidity":hum},
#         "season":season,
#         "updated_at":datetime.datetime.now().isoformat()
#     }
from flask import Blueprint, request, jsonify
import requests, datetime

weather_bp = Blueprint("weather", __name__)
UA = {"User-Agent": "NutraExpertAI/1.0"}

@weather_bp.get("/api/weather")
def weather():
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    place = request.args.get("place")

    # if user typed city
    if place and not (lat and lon):
        geo = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": place, "count": 1},
            headers=UA
        ).json()
        if not geo.get("results"):
            return {"error": "place not found"}, 404
        lat = geo["results"][0]["latitude"]
        lon = geo["results"][0]["longitude"]

    url = "https://api.open-meteo.com/v1/forecast"
    r = requests.get(url, params={
        "latitude": lat,
        "longitude": lon,
        "current": ["temperature_2m", "relative_humidity_2m"],
        "timezone": "auto"
    }, headers=UA).json()

    tempC = r["current"]["temperature_2m"]
    hum = r["current"]["relative_humidity_2m"]
    tempF = round((tempC * 9/5) + 32, 1)

    m = datetime.date.today().month
    if m in (12,1,2): season="Winter"
    elif m in (3,4,5): season="Spring"
    elif m in (6,7,8): season="Summer"
    else: season="Fall"

    return {
    "weather":{"temperature_f":tempF,"humidity":hum},
    "season":season,
    "lat": float(lat),
    "lon": float(lon),
    "updated_at":datetime.datetime.now().isoformat()
}

