from pydantic import BaseSettings, Field

class AgentSettings(BaseSettings):
    """Configuration for the agent loaded from environment variables."""
    agent_id: str = Field("agent-unknown", env="AGENT_ID")
    server_url: str = Field("http://localhost:8000/api/data", env="SERVER_URL")
    collect_interval_seconds: int = Field(60, env="COLLECT_INTERVAL_SECONDS")
    timeout_seconds: int = Field(10, env="REQUEST_TIMEOUT_SECONDS")

    class Config:
        env_file = ".env"

settings = AgentSettings()
