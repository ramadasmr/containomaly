from fastapi import APIRouter, HTTPException, status, Request
from server.models import DockerSnapshot
from server.core.logger import get_logger
from server.db.tsdb import write_snapshot
from datetime import datetime, timezone

router = APIRouter(prefix="/api")
logger = get_logger(__name__)

@router.get("/health")
async def health():
    return {"status": "ok"}

@router.post("/data", status_code=status.HTTP_201_CREATED)
async def receive_data(payload: DockerSnapshot, request: Request):
    """
    Endpoint for agents to POST docker snapshots.
    Validates payload, writes to TSDB and returns acknowledgement.
    """
    try:
        # Determine timestamp: payload timestamp (if any) else now (UTC)
        ts = payload.timestamp
        if ts is None:
            ts = datetime.now(timezone.utc)
        # payload.containers may be list of dicts; send to write API
        write_snapshot(payload.agent_id, payload.containers, ts)
        return {"status": "accepted", "agent_id": payload.agent_id, "written": len(payload.containers)}
    except Exception as exc:
        logger.exception("Error handling payload from %s: %s", payload.agent_id, exc)
        raise HTTPException(status_code=500, detail="internal server error")
