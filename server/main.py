import uvicorn
from fastapi import FastAPI
from server.core.logger import get_logger
from server.core.config import settings
from server.api.routes import router as api_router

logger = get_logger(__name__)
app = FastAPI(title="Docker Anomaly Detector API (Server)")

app.include_router(api_router)

@app.get("/")
def root():
    logger.info("Root endpoint called")
    return {"message": "Docker Anomaly Detector Server running"}

def start():
    uvicorn.run("server.main:app", host=settings.server_host, port=settings.server_port, reload=True)

if __name__ == "__main__":
    start()
