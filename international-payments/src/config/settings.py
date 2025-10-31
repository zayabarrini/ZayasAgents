import os
from typing import Dict, Any
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application settings"""

    # Application
    app_name: str = "International Payment System"
    app_version: str = "1.0.0"
    debug: bool = False

    # Security
    secret_key: str = "your-secret-key-here"  # Change in production
    encryption_key: str = "your-encryption-key-here"

    # API
    api_prefix: str = "/api/v1"
    allowed_hosts: list = ["localhost", "127.0.0.1", "yourdomain.com"]

    # Rate limiting
    rate_limit_per_minute: int = 10
    rate_limit_per_hour: int = 100

    # Exchange rates
    exchange_rate_cache_minutes: int = 5
    exchange_rate_providers: list = ["ecb", "fixer", "openexchangerates"]

    # Compliance
    compliance_check_enabled: bool = True
    aml_check_enabled: bool = True

    # Database (would be added for production)
    database_url: str = "sqlite:///./payments.db"

    class Config:
        env_file = ".env"
        case_sensitive = False


def get_settings() -> Settings:
    return Settings()


# Global settings instance
settings = get_settings()
