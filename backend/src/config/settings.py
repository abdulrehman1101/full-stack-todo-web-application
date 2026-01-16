from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv
import re

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    database_url: str = os.getenv("DATABASE_URL", "")
    better_auth_secret: str = os.getenv("BETTER_AUTH_SECRET", "")
    cors_origins: str = os.getenv("CORS_ORIGINS", "http://localhost,http://localhost:3000,http://127.0.0.1,http://127.0.0.1:3000")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    @property
    def cors_origins_list(self) -> list:
        """Return CORS origins as a list."""
        return [origin.strip() for origin in self.cors_origins.split(",")]

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"

    def validate_database_url(self):
        """
        Validates that the DATABASE_URL is present and correctly formatted.
        """
        if not self.database_url:
            raise ValueError("DATABASE_URL environment variable not set")

        # Check if it's a valid SQLite connection string
        sqlite_pattern = r'^sqlite:///(.+)$'
        if re.match(sqlite_pattern, self.database_url):
            # Valid SQLite URL
            return

        # Check if it's a valid PostgreSQL connection string
        postgres_pattern = r'^postgresql://[a-zA-Z0-9_.-]+:[a-zA-Z0-9_.-]+@[a-zA-Z0-9.-]+:[0-9]+/[a-zA-Z0-9_.-]+$'
        if not re.match(postgres_pattern, self.database_url):
            # Also allow for more complex connection strings with query parameters
            extended_pattern = r'^postgresql://[a-zA-Z0-9_.\-~!$&\'()*+,;=%:@.]+/[a-zA-Z0-9_.-]+(\?[a-zA-Z0-9_.\-~!$&\'()*+,;=%:@/?&]+)?$'
            if not re.match(extended_pattern, self.database_url):
                raise ValueError(f"Invalid DATABASE_URL format: {self.database_url}")

# Create settings instance
settings = Settings()

# Validate the database URL when settings are loaded
settings.validate_database_url()