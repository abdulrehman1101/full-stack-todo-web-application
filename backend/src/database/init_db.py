"""
Database initialization script for the todo application.
This script creates all database tables using SQLModel metadata.
"""
from sqlmodel import SQLModel
from .engine import engine, create_db_engine
from ..config.settings import settings
from .models.user import User
from .models.task import Task


def initialize_database():
    """
    Initializes the database by creating all tables based on SQLModel metadata.
    This function should be called once during application startup.
    """
    global engine

    if not settings.database_url:
        raise ValueError("DATABASE_URL environment variable not set")

    # Create the database engine with the configured URL
    engine = create_db_engine(settings.database_url)

    # Create all tables defined in SQLModel models
    SQLModel.metadata.create_all(engine)
    print("Database tables created successfully!")


if __name__ == "__main__":
    initialize_database()