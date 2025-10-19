"""
Configuration settings for LogViewer FastAPI backend
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List, Optional
import os

class Settings(BaseSettings):
    """Application settings"""
    
    # Application settings
    APP_NAME: str = "LogViewer API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = Field(default=False, env="DEBUG")
    
    # Server settings
    HOST: str = Field(default="0.0.0.0", env="HOST")
    PORT: int = Field(default=8000, env="PORT")
    
    # CORS settings
    ALLOWED_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:3001"],
        env="ALLOWED_ORIGINS"
    )
    
    # Processing settings
    LOG_PROCESSING_INTERVAL: int = Field(default=30, env="LOG_PROCESSING_INTERVAL")  # seconds
    MAX_LOG_BATCH_SIZE: int = Field(default=1000, env="MAX_LOG_BATCH_SIZE")
    LOG_RETENTION_HOURS: int = Field(default=24, env="LOG_RETENTION_HOURS")
    
    # AI/ML settings
    GROQ_API_KEY: Optional[str] = Field(default=None, env="GROQ_API_KEY")
    AGNO_API_KEY: Optional[str] = Field(default=None, env="AGNO_API_KEY")
    ENABLE_AI_CLASSIFICATION: bool = Field(default=True, env="ENABLE_AI_CLASSIFICATION")
    
    # File storage settings
    LOG_STORAGE_PATH: str = Field(default="./data/logs", env="LOG_STORAGE_PATH")
    OUTPUT_STORAGE_PATH: str = Field(default="./data/outputs", env="OUTPUT_STORAGE_PATH")
    
    # Database settings (for future use)
    DATABASE_URL: Optional[str] = Field(default=None, env="DATABASE_URL")
    
    # Redis settings (for caching)
    REDIS_URL: Optional[str] = Field(default=None, env="REDIS_URL")
    
    # Notification settings
    ENABLE_NOTIFICATIONS: bool = Field(default=True, env="ENABLE_NOTIFICATIONS")
    NOTIFICATION_WEBHOOK_URL: Optional[str] = Field(default=None, env="NOTIFICATION_WEBHOOK_URL")
    
    # WebSocket settings
    MAX_WEBSOCKET_CONNECTIONS: int = Field(default=100, env="MAX_WEBSOCKET_CONNECTIONS")
    WEBSOCKET_KEEPALIVE_INTERVAL: int = Field(default=30, env="WEBSOCKET_KEEPALIVE_INTERVAL")
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Global settings instance
settings = Settings()
