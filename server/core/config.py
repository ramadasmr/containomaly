from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    server_host: str = "0.0.0.0"
    server_port: int = 8000
    log_level: str = "INFO"

    # InfluxDB settings (v2)
    influx_url: str = Field("http://localhost:8086", env="INFLUX_URL")
    influx_token: str = Field("my-token", env="INFLUX_TOKEN")
    influx_org: str = Field("my-org", env="INFLUX_ORG")
    influx_bucket: str = Field("containomaly", env="INFLUX_BUCKET")

    class Config:
        env_file = ".env"

settings = Settings()