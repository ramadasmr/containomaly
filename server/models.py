from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class ContainerInfo(BaseModel):
    ID: str
    Image: Optional[str] = None
    Command: Optional[str] = None
    CreatedAt: Optional[str] = None
    RunningFor: Optional[str] = None
    Status: Optional[str] = None
    Ports: Optional[str] = None
    Names: Optional[str] = None
    # Accept arbitrary keys from docker json
    extra: Optional[Dict[str, Any]] = None

    class Config:
        extra = "allow"

class DockerSnapshot(BaseModel):
    agent_id: str = Field(..., min_length=1)
    timestamp: Optional[datetime] = None   # client may provide; otherwise server will use now
    containers: List[Dict[str, Any]] = Field(default_factory=list)

    class Config:
        schema_extra = {
            "example": {
                "agent_id": "node-001",
                "timestamp": "2025-10-27T16:00:00Z",
                "containers": [
                    {"ID":"1a2b3c","Image":"nginx:latest","Status":"Up 1 hour","CreatedAt":"2025-10-27T15:00:00Z"}
                ]
            }
        }