"""
Application configuration module.
Manages environment variables and application settings.
"""
from pydantic_settings import BaseSettings
from functools import lru_cache
from pathlib import Path


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    DATABASE_URL: str = "postgresql://admin:admin123@localhost:5432/admin_panel"

    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # File Storage
    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_SIZE: int = 500 * 1024 * 1024  # 500MB

    # Application
    APP_NAME: str = "Admin Panel API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # CORS
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:8000",
        "file://",
    ]

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Ensure upload directories exist
def init_directories():
    """Create necessary directories if they don't exist."""
    settings = get_settings()
    upload_path = Path(settings.UPLOAD_DIR)
    upload_path.mkdir(parents=True, exist_ok=True)

    # Create subdirectories
    (upload_path / "videos").mkdir(exist_ok=True)
    (upload_path / "audio").mkdir(exist_ok=True)
    (upload_path / "thumbnails").mkdir(exist_ok=True)
    (upload_path / "projects").mkdir(exist_ok=True)
