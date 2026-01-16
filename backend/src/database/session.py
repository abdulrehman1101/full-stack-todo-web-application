"""
Database session management for the todo application.
This module provides session context managers and utilities optimized for Neon Serverless PostgreSQL.
"""
from contextlib import contextmanager
from typing import Generator
from sqlmodel import Session
from .engine import engine


def get_session() -> Generator[Session, None, None]:
    """
    Dependency function for database sessions.
    Used with FastAPI Depends() to inject database sessions.
    Optimized for Neon Serverless PostgreSQL with proper connection handling.
    """
    if engine is None:
        raise RuntimeError("Database engine not initialized")

    with Session(engine) as session:
        try:
            yield session
        finally:
            # Ensure the session is properly closed and connection is returned to pool
            session.close()


@contextmanager
def get_session_context() -> Generator[Session, None, None]:
    """
    Context manager for database sessions.
    Uses the yield pattern to ensure sessions are automatically closed after use.
    Optimized for Neon Serverless PostgreSQL with proper connection handling.
    """
    if engine is None:
        raise RuntimeError("Database engine not initialized")

    with Session(engine) as session:
        try:
            yield session
        finally:
            # Ensure the session is properly closed and connection is returned to pool
            session.close()