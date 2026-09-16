from datetime import datetime
from .open_meteo import get_air_quality
from .predict import predict_aqi


def get_location_prediction(name, latitude, longitude):

    air = get_air_quality(latitude, longitude)

    current = air["current"]

    pm25 = current["pm2_5"]
    pm10 = current["pm10"]
    no2 = current["nitrogen_dioxide"]
    so2 = current["sulphur_dioxide"]
    co = current["carbon_monoxide"]
    ozone = current["ozone"]

    # Convert Open-Meteo CO µg/m³ → mg/m³
    co_for_model = co / 1000

    now = datetime.now()

    aqi = predict_aqi(
        date=now.day,
        month=now.month,
        year=now.year,
        holidays_count=0,
        days=now.timetuple().tm_yday,
        pm25=pm25,
        pm10=pm10,
        no2=no2,
        so2=so2,
        co=co_for_model,
        ozone=ozone,
    )

    aqi = max(0, aqi)

    if aqi <= 50:
        risk = "Good"
    elif aqi <= 100:
        risk = "Satisfactory"
    elif aqi <= 200:
        risk = "Moderate"
    elif aqi <= 300:
        risk = "Poor"
    elif aqi <= 400:
        risk = "Very Poor"
    else:
        risk = "Severe"

    return {
        "name": name,
        "aqi": round(aqi),
        "risk": risk,
    }