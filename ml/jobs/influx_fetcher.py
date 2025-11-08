"""
Fetches recent container snapshots from InfluxDB.
Used by ML scheduler to retrieve data for anomaly detection or analysis.
"""

from datetime import datetime, timedelta, timezone
from influxdb_client import InfluxDBClient
from server.core.config import settings
from server.core.logger import get_logger

logger = get_logger(__name__)

# Create client (reuse across fetches)
_client = InfluxDBClient(
    url=settings.influx_url,
    token=settings.influx_token,
    org=settings.influx_org
)
_query_api = _client.query_api()


def fetch_recent_data(minutes: int = 5):
    """
    Fetch container data from the last `minutes`.
    Returns a list of records (dict).
    """
    stop = datetime.now(timezone.utc)
    start = stop - timedelta(minutes=minutes)

    query = f"""
    from(bucket: "{settings.influx_bucket}")
      |> range(start: {start.isoformat()}, stop: {stop.isoformat()})
      |> filter(fn: (r) => r["_measurement"] == "docker_containers")
      |> pivot(rowKey:["_time"], columnKey:["_field"], valueColumn:"_value")
      |> keep(columns: ["_time", "agent_id", "container_id", "image", "name", "status", "created_at", "raw"])
    """

    logger.info(f"Fetching data from InfluxDB for last {minutes} minutes...")
    try:
        tables = _query_api.query(query)
        results = []
        for table in tables:
            for record in table.records:
                results.append(record.values)
        logger.info(f"Fetched {len(results)} records.")
        return results
    except Exception as exc:
        logger.exception(f"Failed to fetch from InfluxDB: {exc}")
        return []

