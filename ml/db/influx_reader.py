from influxdb_client import InfluxDBClient
from datetime import datetime, timedelta
import os

INFLUX_URL = os.getenv("INFLUX_URL")
INFLUX_TOKEN = os.getenv("INFLUX_TOKEN")
INFLUX_ORG = os.getenv("INFLUX_ORG")
INFLUX_BUCKET = os.getenv("INFLUX_BUCKET")


def fetch_recent_snapshots(minutes: int = 5):
    client = InfluxDBClient(
        url=INFLUX_URL,
        token=INFLUX_TOKEN,
        org=INFLUX_ORG,
    )

    query = f'''
    from(bucket: "{INFLUX_BUCKET}")
      |> range(start: -{minutes}m)
      |> filter(fn: (r) => r._measurement == "docker_containers")
    '''

    tables = client.query_api().query(query)

    rows = []
    for table in tables:
        for r in table.records:
            rows.append({
                "time": r.get_time().isoformat(),
                "container_id": r.values.get("container_id"),
                "name": r.values.get("name"),
                "status": r.get_value()
            })

    client.close()
    return rows
