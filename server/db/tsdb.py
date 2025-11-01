"""
InfluxDB writer using influxdb-client (v2).
This module provides a simple, robust write function to store container snapshots.
"""
from influxdb_client import InfluxDBClient, Point, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS
from typing import Dict, List, Any
from datetime import datetime
from server.core.config import settings
from server.core.logger import get_logger

logger = get_logger(__name__)

# create client - module-level so it can be reused
_client = InfluxDBClient(url=settings.influx_url, token=settings.influx_token, org=settings.influx_org)
_write_api = _client.write_api(write_options=SYNCHRONOUS)

def _to_point(agent_id: str, container: Dict[str, Any], timestamp: datetime):
    """
    Convert one container JSON to an InfluxDB Point.
    Use tags for dimensions and fields for metrics/text.
    """
    # Basic tags
    container_id = container.get("ID") or container.get("Id") or "unknown"
    image = container.get("Image", "unknown")
    name = container.get("Names") or container.get("Name") or container.get("Names", "")

    p = Point("docker_containers") \
            .tag("agent_id", agent_id) \
            .tag("container_id", str(container_id)) \
            .tag("image", str(image)) \
            .tag("name", str(name))

    # Common textual fields stored as fields (InfluxDB fields can be strings or numbers)
    # Be mindful: fields are for non-indexed data; tags are indexed.
    status = container.get("Status")
    if status is not None:
        p.field("status", str(status))

    created = container.get("CreatedAt") or container.get("Created")
    if created:
        p.field("created_at", str(created))

    # Store raw JSON as a field (string) for full fidelity, but not indexed
    try:
        import json
        p.field("raw", json.dumps(container))
    except Exception:
        logger.debug("Could not json-encode container raw data")

    # Use provided timestamp for the point if available
    p.time(timestamp)

    return p

def write_snapshot(agent_id: str, containers: List[Dict[str, Any]], timestamp: datetime):
    """
    Write all containers from one snapshot as individual points.
    Uses synchronous write for simplicity; in production consider batching/async.
    """
    if not containers:
        logger.info("No containers to write for agent %s at %s", agent_id, timestamp.isoformat())
        return

    points = []
    for c in containers:
        try:
            p = _to_point(agent_id, c, timestamp)
            points.append(p)
        except Exception as exc:
            logger.exception("Failed to convert container to point: %s", exc)

    if not points:
        logger.warning("No valid points to write for agent %s", agent_id)
        return

    try:
        _write_api.write(bucket=settings.influx_bucket, org=settings.influx_org, record=points)
        logger.info("Wrote %s points to InfluxDB bucket=%s", len(points), settings.influx_bucket)
    except Exception as exc:
        logger.exception("Failed to write points to InfluxDB: %s", exc)
