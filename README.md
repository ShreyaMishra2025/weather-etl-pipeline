# Weather ETL Pipeline

An end-to-end batch data engineering pipeline that 
fetches real-time weather data for 5 Indian cities 
and loads it into a PostgreSQL data warehouse.

## Architecture
OpenWeatherMap API
|
v
extract.py  (Python + requests)
|
v
transform.py  (Pandas)
|
v
load.py  (SQLAlchemy + PostgreSQL)
|
v
PostgreSQL Star Schema
(fact_weather, dim_city, dim_date)

## Tech Stack

- Python 3.13
- Pandas
- SQLAlchemy
- PostgreSQL 15
- Docker
- Great Expectations (coming soon)

## Cities Covered

- Mumbai
- Delhi
- Bengaluru
- Chennai
- Lucknow

## Project Structure
weather-etl-pipeline/
├── extract.py        # Fetch data from API
├── transform.py      # Clean and transform data
├── load.py           # Load to PostgreSQL
├── pipeline.py       # Main orchestrator
├── .env              # API keys (not committed)
├── .gitignore
└── README.md

## How to Run

1. Clone the repo
2. Create virtual environment
   python -m venv venv
   venv\Scripts\activate

3. Install dependencies
   pip install -r requirements.txt

4. Add your API key in .env file
   WEATHER_API_KEY=your_key_here
   DATABASE_URL=postgresql+psycopg2://postgres:deproject@localhost:5432/weather_dwh

5. Start PostgreSQL with Docker
   docker run --name de-postgres 
   -e POSTGRES_PASSWORD=deproject 
   -e POSTGRES_DB=weather_dwh 
   -p 5432:5432 -d postgres:15

6. Run the pipeline
   python pipeline.py

## Star Schema

fact_weather
- weather_id (PK)
- city_id (FK)
- date_id (FK)
- temperature_c
- feels_like_c
- humidity_pct
- wind_speed_kmh
- visibility_km
- weather_condition

dim_city
- city_id (PK)
- city_name
- country
- latitude
- longitude

dim_date
- date_id (PK)
- full_date
- day_of_week
- month_name
- quarter
- year
- is_weekend

## What I Learned

- Building end-to-end ETL pipelines
- Working with REST APIs in Python
- Data transformation with Pandas
- Star schema design
- Loading data to PostgreSQL with SQLAlchemy
- Docker for local development