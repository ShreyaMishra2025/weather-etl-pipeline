import pandas as pd
from sqlalchemy import create_engine, text
import os
import logging
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DATABASE_URL")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(message)s"
)

def create_engine_conn():
    """Create database connection"""
    engine = create_engine(DB_URL)
    logging.info("✅ Database connected!")
    return engine

def create_tables(engine):
    """Create all tables if not exist"""
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS dim_city (
                city_id     SERIAL PRIMARY KEY,
                city_name   VARCHAR(100) UNIQUE,
                country     VARCHAR(10),
                latitude    NUMERIC(9,6),
                longitude   NUMERIC(9,6)
            )
        """))

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS dim_date (
                date_id     VARCHAR(20) PRIMARY KEY,
                full_date   DATE,
                day_of_week VARCHAR(20),
                month_name  VARCHAR(20),
                quarter     INTEGER,
                year        INTEGER,
                is_weekend  BOOLEAN
            )
        """))

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS fact_weather (
                weather_id        SERIAL PRIMARY KEY,
                city_id           INTEGER 
                                  REFERENCES dim_city(city_id),
                date_id           VARCHAR(20)
                                  REFERENCES dim_date(date_id),
                temperature_c     NUMERIC(5,2),
                feels_like_c      NUMERIC(5,2),
                humidity_pct      INTEGER,
                wind_speed_kmh    NUMERIC(6,2),
                visibility_km     NUMERIC(5,2),
                weather_condition VARCHAR(100),
                description       VARCHAR(200),
                recorded_at       TIMESTAMP
            )
        """))
        conn.commit()
    logging.info("✅ Tables created!")

def load_dim_city(df, engine):
    """Load city dimension table"""
    cities = df[["city_name", "country",
                 "latitude", "longitude"]].drop_duplicates()

    with engine.connect() as conn:
        for _, row in cities.iterrows():
            conn.execute(text("""
                INSERT INTO dim_city
                (city_name, country, latitude, longitude)
                VALUES (:city, :country, :lat, :lon)
                ON CONFLICT (city_name) DO NOTHING
            """), {
                "city"    : row["city_name"],
                "country" : row["country"],
                "lat"     : row["latitude"],
                "lon"     : row["longitude"]
            })
        conn.commit()
    logging.info("✅ dim_city loaded!")

def load_dim_date(engine):
    """Load date dimension table"""
    from datetime import datetime, date
    today = date.today()
    date_id = today.strftime("%Y%m%d")

    with engine.connect() as conn:
        conn.execute(text("""
            INSERT INTO dim_date
            (date_id, full_date, day_of_week,
             month_name, quarter, year, is_weekend)
            VALUES
            (:date_id, :full_date, :dow,
             :month, :quarter, :year, :weekend)
            ON CONFLICT (date_id) DO NOTHING
        """), {
            "date_id"  : date_id,
            "full_date": today,
            "dow"      : today.strftime("%A"),
            "month"    : today.strftime("%B"),
            "quarter"  : (today.month - 1) // 3 + 1,
            "year"     : today.year,
            "weekend"  : today.weekday() >= 5
        })
        conn.commit()
    logging.info("✅ dim_date loaded!")
    return date_id

def load_fact_weather(df, engine, date_id):
    """Load fact table"""
    with engine.connect() as conn:
        # Get city IDs
        result = conn.execute(
            text("SELECT city_id, city_name FROM dim_city")
        )
        city_map = {row[1]: row[0] for row in result}

    # Add IDs to dataframe
    df["city_id"] = df["city_name"].map(city_map)
    df["date_id"] = date_id

    # Select only fact columns
    fact_df = df[[
        "city_id", "date_id",
        "temperature_c", "feels_like_c",
        "humidity_pct", "wind_speed_kmh",
        "visibility_km", "weather_condition",
        "description", "recorded_at"
    ]]

    fact_df.to_sql(
        "fact_weather", engine,
        if_exists="append",
        index=False
    )
    logging.info(f"✅ fact_weather loaded — {len(fact_df)} rows!")

def load_all(df):
    """Load all tables"""
    engine = create_engine_conn()
    create_tables(engine)
    load_dim_city(df, engine)
    date_id = load_dim_date(engine)
    load_fact_weather(df, engine, date_id)
    logging.info("🎉 All data loaded successfully!")

if __name__ == "__main__":
    from extract import extract_all_cities
    from transform import transform_raw

    raw_data = extract_all_cities()
    df = transform_raw(raw_data)
    load_all(df)