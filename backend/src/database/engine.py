"""
Database engine initialization for the todo application.
This module sets up the database engine and connection pool optimized for Neon Serverless PostgreSQL.
"""
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool
from typing import Optional
from ..config.settings import settings
import urllib.parse


def create_db_engine(database_url: str):
    """
    Creates a database engine with appropriate configuration for Neon Serverless PostgreSQL or SQLite.

    Args:
        database_url: The database connection string

    Returns:
        SQLAlchemy engine instance
    """
    # Check if it's a SQLite connection
    if database_url.startswith("sqlite"):
        # SQLite doesn't need SSL or pooling
        engine = create_engine(
            database_url,
            connect_args={"check_same_thread": False},  # Required for SQLite with FastAPI
        )
    else:
        # Add sslmode=require to the PostgreSQL connection string if not already present
        if "sslmode" not in database_url:
            if "?" in database_url:
                database_url += "&sslmode=require"
            else:
                database_url += "?sslmode=require"

        engine = create_engine(
            database_url,
            poolclass=QueuePool,
            pool_size=5,  # Smaller pool size for serverless
            max_overflow=0,  # Limit overflow for serverless
            pool_pre_ping=True,  # Verify connections before use (essential for serverless)
            pool_recycle=300,  # Recycle connections every 5 minutes
            pool_timeout=30,  # 30 seconds to get connection from pool
            pool_reset_on_return="commit",  # Reset connection state after each use
        )

    return engine


# Initialize engine when module is loaded
engine: Optional[object] = None

if settings.database_url:
    engine = create_db_engine(settings.database_url)
else:
    raise ValueError("DATABASE_URL environment variable not set. Please configure your .env file.")