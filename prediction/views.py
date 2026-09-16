from .services.location_prediction import get_location_prediction
from datetime import datetime

from django.shortcuts import render

from .services.open_meteo import get_weather
from .services.air_quality import get_air_quality
from .services.predict import predict_aqi


def home(request):

    # ==========================================
    # 1. DELHI NCR COORDINATES
    # ==========================================

    latitude = 28.6139
    longitude = 77.2090


    # ==========================================
    # 2. GET WEATHER DATA
    # ==========================================

    weather = get_weather(latitude, longitude)

    current_weather = weather["current"]

    temperature = current_weather["temperature_2m"]
    humidity = current_weather["relative_humidity_2m"]
    wind_speed = current_weather["wind_speed_10m"]


    # ==========================================
    # 3. GET AIR QUALITY DATA
    # ==========================================

    air = get_air_quality(latitude, longitude)

    hourly_air = air["hourly"]

    pm25 = hourly_air["pm2_5"][0]
    pm10 = hourly_air["pm10"][0]
    no2 = hourly_air["nitrogen_dioxide"][0]
    so2 = hourly_air["sulphur_dioxide"][0]
    co = hourly_air["carbon_monoxide"][0]
    ozone = hourly_air["ozone"][0]


    # ==========================================
    # 4. DATE INFORMATION FOR ML MODEL
    # ==========================================

    now = datetime.now()

    date = now.day
    month = now.month
    year = now.year

    holidays_count = 0

    # IMPORTANT:
    # Keep this consistent with how your original
    # dataset defined the "Days" column.
    days = now.weekday()


    # ==========================================
    # 5. ML PREDICTION
    # ==========================================

    aqi = predict_aqi(
        date=date,
        month=month,
        year=year,
        holidays_count=holidays_count,
        days=days,
        pm25=pm25,
        pm10=pm10,
        no2=no2,
        so2=so2,
        co=co,
        ozone=ozone
    )


    # ==========================================
    # 6. RISK CLASSIFICATION
    # ==========================================

    if aqi <= 50:
        risk_level = "Low"

    elif aqi <= 100:
        risk_level = "Moderate"

    elif aqi <= 200:
        risk_level = "High"

    elif aqi <= 300:
        risk_level = "Very High"

    else:
        risk_level = "Severe"


    # ==========================================
    # 7. SEND DATA TO HTML
    # ==========================================

    context = {

        "location": "Delhi NCR",

        # Weather
        "temperature": round(temperature, 1),
        "humidity": round(humidity, 1),
        "wind_speed": round(wind_speed, 1),

        # Pollution
        "pm25": round(pm25, 2),
        "pm10": round(pm10, 2),
        "no2": round(no2, 2),
        "so2": round(so2, 2),
        "co": round(co, 2),
        "ozone": round(ozone, 2),

        # Prediction
        "aqi": round(aqi, 2),
        "risk_level": risk_level,
        "risk_locations": risk_locations,
    }


    return render(
        request,
        "prediction/home.html",
        context
    )

locations = [
    {
        "name": "Haryana",
        "latitude": 28.4595,
        "longitude": 77.0266,
    },
    {
        "name": "UP",
        "latitude": 28.6139,
        "longitude": 77.2090,
    },
    {
        "name": "Rajasthan",
        "latitude": 26.9124,
        "longitude": 75.7873,
    },
    {
        "name": "Punjab",
        "latitude": 30.9010,
        "longitude": 75.8573,
    },
]
risk_locations = []

for location in locations:

    result = get_location_prediction(
        location["name"],
        location["latitude"],
        location["longitude"],
    )

    risk_locations.append(result)