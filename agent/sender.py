"""Responsible for sending payloads to server with retries and basic validation."""
import requests
from typing import List, Dict, Any
from requests.exceptions import RequestException
from .config import settings
from .logger import get_logger

logger = get_logger(__name__)

class Sender:
    def __init__(self, server_url: str = None, timeout: int = None):
        self.server_url = server_url or settings.server_url
        self.timeout = timeout or settings.timeout_seconds

    def build_payload(self, containers: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create envelope payload with agent metadata and timestamp."""
        return {
            "agent_id": settings.agent_id,
            "containers": containers,
        }

    def send(self, payload: Dict[str, Any], max_retries: int = 3) -> requests.Response:
        last_exc = None
        for attempt in range(1, max_retries + 1):
            try:
                logger.info("Sending payload to %s (attempt %s)", self.server_url, attempt)
                resp = requests.post(self.server_url, json=payload, timeout=self.timeout)
                resp.raise_for_status()
                logger.info("Payload accepted with status %s", resp.status_code)
                return resp
            except RequestException as exc:
                logger.warning("Request failed on attempt %s: %s", attempt, exc)
                last_exc = exc
        logger.error("All retries exhausted")
        raise last_exc
