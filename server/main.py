import uvicorn
from fastapi import FastAPI
from server.core.logger import get_logger, attach_request_logging
from server.core.config import settings
from server.api.routes import router as api_router

logger = get_logger("server", level="INFO")
app = FastAPI(title="Container Anomaly Detector API Server")

attach_request_logging(app, logger)

app.include_router(api_router)

@app.get("/")
def root():
    logger.info("Root endpoint called")
    return {"message": "Docker Anomaly Detector Server running"}

def start():
    uvicorn.run("server.main:app", host=settings.server_host, port=settings.server_port, reload=True)

if __name__ == "__main__":
    start()
