from datetime import datetime
from typing import List, Dict


STATUS_MAP = {
    "up": 1,
    "exited": 0,
    "paused": 2
}


def normalize_status(status: str) -> int:
    if not status:
        return -1

    status = status.lower()
    for key in STATUS_MAP:
        if status.startswith(key):
            return STATUS_MAP[key]

    return -1


def is_running(status_code: int) -> int:
    return 1 if status_code == 1 else 0


def extract_features(
    records: List[Dict],
    previous_state: Dict[str, Dict]
) -> List[Dict]:
    """
    records: current snapshot from Influx
    previous_state: last known container state (in-memory or Redis later)
    """

    features = []

    for r in records:
        container_id = r["container_id"]
        status_code = normalize_status(r.get("status"))

        prev = previous_state.get(container_id)

        status_changed = False
        if prev:
            status_changed = prev["status_code"] != status_code

        feature = {
            "time": r["time"],
            "agent_id": r["agent_id"],
            "container_id": container_id,
            "container_name": r.get("name"),
            "status_code": status_code,
            "is_running": is_running(status_code),
            "status_changed": status_changed,
            "container_seen": True
        }

        features.append(feature)

    return features
