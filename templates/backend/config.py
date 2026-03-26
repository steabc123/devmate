from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables or .env file.
    Priority: Environment Variables > .env file > Default values
    """
    
    # Application
    app_name: str = "DevMate App"
    app_version: str = "0.1.0"
    debug: bool = True
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Database
    database_url: str = "sqlite:///./data/app.db"
    database_pool_size: int = 5
    database_max_overflow: int = 10
    
    # CORS
    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000"
    cors_allow_credentials: bool = True
    cors_allow_methods: str = "GET,POST,PUT,DELETE"
    cors_allow_headers: str = "*"
    
    # Security
    secret_key: str = "change-this-secret-key-in-production"
    api_prefix: str = "/api"
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "json"
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    @property
    def cors_allow_methods_list(self) -> List[str]:
        """Parse CORS methods from comma-separated string."""
        return [method.strip().upper() for method in self.cors_allow_methods.split(",")]
    
    @property
    def cors_allow_headers_list(self) -> List[str]:
        """Parse CORS headers from comma-separated string."""
        if self.cors_allow_headers == "*":
            return ["*"]
        return [header.strip() for header in self.cors_allow_headers.split(",")]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    Using LRU cache to avoid reloading settings on every request.
    """
    return Settings()
