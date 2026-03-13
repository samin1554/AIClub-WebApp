from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    SERVICE_NAME: str = "projects-api"
    SERVICE_PORT: int = 8010
    
    DATABASE_URL: str = "postgresql://aiclub:aiclub@localhost:5435/aiclub_projects"
    REDIS_URL: str = "redis://localhost:6379"
    
    SECRET_KEY: str = "dev-secret-key-for-testing"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080
    
    INTERNAL_API_KEY: str = "internal-dev-key"
    
    CORS_ORIGINS: str = "http://localhost:3000"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    
    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    class Config:
        env_file = ".env"

settings = Settings()
