"""
Dependency injection module for the todo application API.
This module provides reusable dependencies for FastAPI endpoints.
"""

from fastapi import Depends
from sqlmodel import Session
from ..database.session import get_session
from ..auth.middleware import get_current_user_id, verify_authenticated_user
from ..database.models.user import User


def get_db_session() -> Session:
    """
    Get database session dependency.

    Yields:
        Database session for use in endpoints
    """
    with get_session() as session:
        yield session


# Re-export authentication dependencies for easy access
CurrentUser = get_current_user_id
CurrentUserDetails = verify_authenticated_user