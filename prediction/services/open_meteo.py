import requests


def get_weather(latitude, longitude):

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,

        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "wind_speed_10m"
        ],

        "hourly": [
            "temperature_2m",
            "relative_humidity_2m",
            "precipitation",
            "surface_pressure",
            "wind_speed_10m",
            "wind_direction_10m"
        ],

        "forecast_hours": 72,
        "timezone": "Asia/Kolkata"
    }

    response = requests.get(
        url,
        params=params,
        timeout=20
    )

    response.raise_for_status()

    return response.json()


def get_air_quality(latitude, longitude):

    url = "https://air-quality-api.open-meteo.com/v1/air-quality"

    params = {
        "latitude": latitude,
        "longitude": longitude,

        "current": [
            "pm2_5",
            "pm10",
            "nitrogen_dioxide",
            "sulphur_dioxide",
            "carbon_monoxide",
            "ozone"
        ],

        "hourly": [
            "pm2_5",
            "pm10",
            "nitrogen_dioxide",
            "sulphur_dioxide",
            "carbon_monoxide",
            "ozone"
        ],

        "forecast_hours": 72,
        "timezone": "Asia/Kolkata"
    }

    response = requests.get(
        url,
        params=params,
        timeout=20
    )

    response.raise_for_status()

    return response.json()