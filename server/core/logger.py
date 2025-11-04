import logging
import sys
from typing import Optional

LOG_FORMAT = (
    "%(asctime)s | %(levelname)-8s | %(name)s | "
    "%(message)s"
)

def get_logger(name: Optional[str] = None, level: str = "INFO") -> logging.Logger:
    """Return a consistent application logger with stdout handler."""
    logger = logging.getLogger(name or "server")
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(LOG_FORMAT)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(level.upper())
        logger.propagate = False
    return logger


# Optional: FastAPI request logger middleware integration
def attach_request_logging(app, logger: logging.Logger):
    """Attach middleware to log incoming requests and responses."""

    @app.middleware("http")
    async def log_requests(request, call_next):
        logger.info(f"Incoming {request.method} {request.url.path}")
        try:
            response = await call_next(request)
        except Exception as e:
            logger.exception(f"Exception handling request: {e}")
            raise
        logger.info(f"Response {response.status_code} for {request.method} {request.url.path}")
        return response

