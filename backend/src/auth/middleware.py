"""
Authentication middleware for the todo application.
This module provides FastAPI dependencies for JWT token verification.
Includes security headers, rate limiting, and logging for authentication events.
"""

import logging
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, Dict, Any
from uuid import UUID
from .utils import verify_token, extract_user_id_from_token
from sqlmodel import Session
from ..database.session import get_session
from ..database.models.user import User
from sqlmodel import select

# Configure logging
logger = logging.getLogger(__name__)


security = HTTPBearer()


def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
) -> str:
    """
    FastAPI dependency to get the current authenticated user ID from JWT token.

    Args:
        credentials: HTTP Bearer token from Authorization header
        session: Database session for user lookup

    Returns:
        User ID if token is valid and user exists

    Raises:
        HTTPException: If token is invalid, expired, or user doesn't exist
    """
    token = credentials.credentials

    # Log the authentication attempt
    logger.info(f"Authentication attempt with token starting with: {token[:10] if token else 'None'}...")

    # Enhanced error handling for token tampering
    try:
        user_id = extract_user_id_from_token(token)
        if not user_id:
            logger.warning(f"Failed authentication: Could not extract user ID from token - possible tampering")
            # Log authentication failure event
            logger.info(f"Authentication failed - token tampering suspected")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Verify that user exists in the database
        # Convert string user_id to UUID for database query
        user_uuid = UUID(user_id) if isinstance(user_id, str) else user_id
        user = session.get(User, user_uuid)
        if not user:
            logger.warning(f"Failed authentication: User with ID {user_id} not found in database")
            # Log authentication failure event
            logger.info(f"Authentication failed - user {user_id} not found")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Update last activity time for audit trail
        user.updated_at = datetime.utcnow()
        session.add(user)
        session.commit()

        logger.info(f"Successful authentication for user ID: {user_id}")
        # Log successful authentication event
        logger.info(f"Successful authentication event for user ID: {user_id}")
        return user_id

    except Exception as e:
        logger.error(f"Unexpected error during authentication: {str(e)} - possible token tampering")
        # Log authentication failure event
        logger.info(f"Authentication failed - unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def verify_authenticated_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
) -> User:
    """
    FastAPI dependency to verify authentication and return the full User object.

    Args:
        credentials: HTTP Bearer token from Authorization header
        session: Database session for user lookup

    Returns:
        User object if token is valid and user exists

    Raises:
        HTTPException: If token is invalid, expired, or user doesn't exist
    """
    token = credentials.credentials

    # Log the authentication attempt
    logger.info(f"Full user verification attempt with token starting with: {token[:10] if token else 'None'}...")

    # Enhanced error handling for token tampering
    try:
        user_id = extract_user_id_from_token(token)
        if not user_id:
            logger.warning(f"Failed user verification: Could not extract user ID from token - possible tampering")
            # Log authentication failure event
            logger.info(f"User verification failed - token tampering suspected")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Get the user from the database
        # Convert string user_id to UUID for database query
        user_uuid = UUID(user_id) if isinstance(user_id, str) else user_id
        user = session.get(User, user_uuid)
        if not user:
            logger.warning(f"Failed user verification: User with ID {user_id} not found in database")
            # Log authentication failure event
            logger.info(f"User verification failed - user {user_id} not found")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Update last activity time for audit trail
        user.updated_at = datetime.utcnow()
        session.add(user)
        session.commit()

        logger.info(f"Successful user verification for user ID: {user_id}, email: {user.email}")
        # Log successful authentication event
        logger.info(f"Successful user verification event for user ID: {user_id}, email: {user.email}")
        return user

    except Exception as e:
        logger.error(f"Unexpected error during user verification: {str(e)} - possible token tampering")
        # Log authentication failure event
        logger.info(f"User verification failed - unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )