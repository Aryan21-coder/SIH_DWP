from pathlib import Path
import joblib
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent.parent

MODEL_PATH = BASE_DIR / "ml_model" / "air_pollution_model.pkl"

model = joblib.load(MODEL_PATH)


def predict_aqi(
    date,
    month,
    year,
    holidays_count,
    days,
    pm25,
    pm10,
    no2,
    so2,
    co,
    ozone
):

    data = pd.DataFrame([{
        "Date": date,
        "Month": month,
        "Year": year,
        "Holidays_Count": holidays_count,
        "Days": days,
        "PM2.5": pm25,
        "PM10": pm10,
        "NO2": no2,
        "SO2": so2,
        "CO": co,
        "Ozone": ozone
    }])

    prediction = model.predict(data)

    return float(prediction[0])