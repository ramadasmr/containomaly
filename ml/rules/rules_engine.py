from typing import List, Dict
from datetime import datetime, timedelta
from collections import defaultdict


FLAP_THRESHOLD = 3
FLAP_WINDOW_SECONDS = 300  # 5 minutes


def detect_anomalies(
    features: List[Dict],
    history: Dict[str, List[Dict]]
) -> List[Dict]:
    """
    features: output from feature extractor
    history: recent feature history per container
    """

    anomalies = []
    now = datetime.utcnow()

    for f in features:
        cid = f["container_id"]
        cname = f.get("container_name")

        # Init history
        if cid not in history:
            history[cid] = []

        history[cid].append(f)

        # Keep history small (last 10 mins)
        history[cid] = [
            h for h in history[cid]
            if datetime.fromisoformat(h["time"].replace("Z", ""))
            > now - timedelta(minutes=10)
        ]

        # Rule 1: Container stopped
        if f["is_running"] == 0:
            anomalies.append({
                "time": f["time"],
                "container_id": cid,
                "container_name": cname,
                "type": "CONTAINER_STOPPED",
                "severity": "high",
                "description": "Container is not running"
            })

        # Rule 2: Restart / status change
        if f["status_changed"]:
            anomalies.append({
                "time": f["time"],
                "container_id": cid,
                "container_name": cname,
                "type": "STATUS_CHANGED",
                "severity": "medium",
                "description": "Container status changed"
            })

        # Rule 3: Flapping detection
        recent_changes = [
            h for h in history[cid] if h["status_changed"]
        ]

        if len(recent_changes) >= FLAP_THRESHOLD:
            anomalies.append({
                "time": f["time"],
                "container_id": cid,
                "container_name": cname,
                "type": "FLAPPING",
                "severity": "critical",
                "description": "Container status flapping detected"
            })

    return anomalies