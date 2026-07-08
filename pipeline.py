import logging
import sys
from datetime import datetime
from extract import extract_all_cities
from transform import transform_raw
from load import load_all

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(message)s",
    handlers=[
        logging.FileHandler("pipeline.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

def run_pipeline():
    start = datetime.now()
    logging.info("=" * 40)
    logging.info("PIPELINE STARTED")
    logging.info("=" * 40)

    try:
        # Step 1 - Extract
        logging.info("Step 1: Extracting data...")
        raw_data = extract_all_cities()
        logging.info("Extraction done!")

        # Step 2 - Transform
        logging.info("Step 2: Transforming data...")
        df = transform_raw(raw_data)
        logging.info("Transform done!")

        # Step 3 - Load
        logging.info("Step 3: Loading to database...")
        load_all(df)
        logging.info("Load done!")

        # Done!
        elapsed = (datetime.now() - start).seconds
        logging.info("=" * 40)
        logging.info(f"PIPELINE COMPLETE in {elapsed}s")
        logging.info("=" * 40)

    except Exception as e:
        logging.error(f"PIPELINE FAILED: {e}")
        raise

if __name__ == "__main__":
    run_pipeline()