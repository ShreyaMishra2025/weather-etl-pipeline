import pandas as pd
import json
import os
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(message)s"
)

def read_raw_files():
    """Read all JSON files from data/raw/"""
    raw_data = []
    folder = "data/raw"
    for file in os.listdir(folder):
        if file.endswith(".json"):
            with open(f"{folder}/{file}", "r") as f:
                data = json.load(f)
                raw_data.append(data)
    logging.info(f"Read {len(raw_data)} raw files")
    return raw_data

def transform_raw(raw_data):
    """Clean and transform raw data"""
    records = []
    for data in raw_data:
        record = {
            # City info
            "city_name"     : data["name"],
            "country"       : data["sys"]["country"],
            "latitude"      : data["coord"]["lat"],
            "longitude"     : data["coord"]["lon"],

            # Temperature
            "temperature_c" : round(data["main"]["temp"], 2),
            "feels_like_c"  : round(data["main"]["feels_like"], 2),
            "temp_min_c"    : round(data["main"]["temp_min"], 2),
            "temp_max_c"    : round(data["main"]["temp_max"], 2),

            # Other weather info
            "humidity_pct"     : data["main"]["humidity"],
            "pressure_hpa"     : data["main"]["pressure"],
            "wind_speed_kmh"   : round(
                                   data["wind"]["speed"] * 3.6, 2
                                 ),
            "visibility_km"    : round(
                                   data.get("visibility", 0) / 1000, 2
                                 ),
            "weather_condition": data["weather"][0]["main"],
            "description"      : data["weather"][0]["description"],

            # Timestamp
            "recorded_at" : datetime.now().strftime(
                              "%Y-%m-%d %H:%M:%S"
                            )
        }
        records.append(record)

    # Convert to DataFrame
    df = pd.DataFrame(records)
    logging.info(f"Transformed {len(df)} records")
    logging.info(f"\n{df[['city_name','temperature_c','humidity_pct','weather_condition']].to_string()}")
    return df

if __name__ == "__main__":
    raw_data = read_raw_files()
    df = transform_raw(raw_data)
    print("\n✅ Transformed Data:")
    print(df[["city_name", "temperature_c",
              "feels_like_c", "humidity_pct",
              "wind_speed_kmh", "weather_condition"]])