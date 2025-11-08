"""
Simple scheduler to periodically fetch data from InfluxDB
and trigger ML processing.
"""

import time
from datetime import datetime
from ml.jobs.influx_fetcher import fetch_recent_data
from server.core.logger import get_logger

logger = get_logger(__name__)

# TODO (Day 5): import anomaly detector once ready
# from ml.detect.anomaly_detector import detect_anomalies

FETCH_INTERVAL_SECS = 60  # configurable (e.g., 60 = every 1 min)


def run_once():
    """
    One cycle: fetch data and run detection.
    """
    logger.info("Starting ML fetch + detect cycle at %s", datetime.utcnow().isoformat())
    data = fetch_recent_data(minutes=5)

    if not data:
        logger.warning("No data fetched from Influx.")
        return

    logger.info("Fetched %d records for ML processing", len(data))

    # Placeholder for ML step (to be added in next phase)
    # anomalies = detect_anomalies(data)
    # logger.info("Detected %d anomalies", len(anomalies))


def scheduler_loop():
    """
    Run indefinitely with sleep interval.
    """
    logger.info("Starting ML scheduler loop...")
    while True:
        run_once()
        logger.info("Sleeping for %d seconds...", FETCH_INTERVAL_SECS)
        time.sleep(FETCH_INTERVAL_SECS)


if __name__ == "__main__":
    scheduler_loop()

