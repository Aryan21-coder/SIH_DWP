import requests


def get_air_quality(latitude, longitude):

    url = "https://air-quality-api.open-meteo.com/v1/air-quality"

    params = {
        "latitude": latitude,
        "longitude": longitude,
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
air = get_air_quality(28.6139, 77.2090)

co = air["hourly"]["carbon_monoxide"][0]