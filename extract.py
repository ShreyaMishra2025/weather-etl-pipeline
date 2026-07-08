import requests
import json
import os
import logging
from datetime import datetime
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")

# 5 Indian cities
CITIES = ["Mumbai", "Delhi",
          "Bengaluru", "Chennai", "Lucknow"]

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(message)s"
)

def extract_weather(city):
    """Fetch weather data for one city from API"""
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"  # Get temperature in Celsius
    }
    response = requests.get(url, params=params,
                           timeout=10)
    response.raise_for_status()
    logging.info(f"Data received: {city}")
    return response.json()

def save_raw(data, city):
    """Save raw JSON file to disk"""
    os.makedirs("data/raw", exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M")
    path = f"data/raw/weather_{city.lower()}_{ts}.json"
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    logging.info(f"Saved: {path}")

def save_raw(data, city):
    """Save raw JSON file to disk"""
    os.makedirs("data/raw", exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M")
    path = f"data/raw/weather_{city.lower()}_{ts}.json"
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    logging.info(f"Saved: {path}")

def extract_all_cities():
    """Fetch weather data for all cities"""
    all_data = []
    for city in CITIES:
        data = extract_weather(city)
        save_raw(data, city)
        all_data.append(data)
    return all_data

if __name__ == "__main__":
    logging.info("Extraction started...")
    extract_all_cities()
    logging.info("✅ Extraction complete!")