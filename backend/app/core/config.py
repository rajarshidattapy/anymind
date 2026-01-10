"""Application configuration settings."""
from pydantic_settings import BaseSettings
from typing import Optional, List


class Settings(BaseSettings):
    """Application settings."""
    
    # Application
    APP_NAME: str = "Agent Management API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost/dbname"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # Storage
    STORAGE_PATH: str = "./storage"
    UPLOAD_MAX_SIZE: int = 100 * 1024 * 1024  # 100MB
    
    # Redis (optional)
    REDIS_URL: Optional[str] = None
    
    # Workers
    WORKER_CONCURRENCY: int = 4
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

