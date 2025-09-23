from typing import Optional

from pydantic_settings import BaseSettings

class ApplicationConfig(BaseSettings):
    """Configuration for the application."""

    app_name: str = "LangGraph Application"
    version: str = "1.0.0"
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"

application_config = ApplicationConfig()