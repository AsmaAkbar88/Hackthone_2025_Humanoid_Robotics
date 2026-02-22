import os
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database settings - using Neon PostgreSQL database
    database_url: str = os.getenv("DATABASE_URL", "postgresql://neondb_owner:npg_ZHpDlAIVvQ67@ep-late-star-aip8khsg-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require")
    async_database_url: str = os.getenv(
        "ASYNC_DATABASE_URL",
        "postgresql+asyncpg://neondb_owner:npg_ZHpDlAIVvQ67@ep-late-star-aip8khsg-pooler.c-4.us-east-1.aws.neon.tech/neondb?ssl=true"
    )
    database_echo: bool = os.getenv("DATABASE_ECHO", "False").lower() == "true"

    # JWT settings
    secret_key: str = os.getenv("SECRET_KEY", "your-super-secret-jwt-key-change-in-production")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # OpenAI settings
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")

    # Application settings
    app_name: str = "Todo Backend API"
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    api_prefix: str = "/api"

    class Config:
        env_file = ".env"


settings = Settings()