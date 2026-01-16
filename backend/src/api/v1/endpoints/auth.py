"""
Authentication endpoints for the todo application API.
This module provides endpoints for user login, registration, and token management with security hardening.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlmodel import Session
from ....database.session import get_session
from ....auth.schemas import UserLogin, UserRegister, Token
from ....database.models.user import User, UserCreate
from ....auth.utils import create_access_token, verify_token, hash_password, verify_password
from sqlalchemy.exc import IntegrityError
from ....config.settings import settings
from slowapi import Limiter
from slowapi.util import get_remote_address
from datetime import datetime, timedelta
import logging
from typing import Optional

# Configure logging
logger = logging.getLogger(__name__)

# Create rate limiter for auth endpoints
limiter = Limiter(key_func=get_remote_address)

router = APIRouter()

@router.post("/register", response_model=Token)
@limiter.limit("5/minute")  # Rate limit registration attempts
def register_user(
    user_register: UserRegister,
    request: Request,  # Needed for rate limiter
    session: Session = Depends(get_session)
) -> Token:
    """
    Register a new user and return an access token.

    Args:
        user_register: User registration data (email, password)
        request: HTTP request (needed for rate limiting)
        session: Database session

    Returns:
        Token containing access token for the new user
    """
    # Log registration attempt
    logger.info(f"Registration attempt for email: {user_register.email}")

    try:
        # Hash the password
        hashed_pwd = hash_password(user_register.password)

        # Create user in database
        db_user = User(email=user_register.email, hashed_password=hashed_pwd)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)

        # Create access token for the new user
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = create_access_token(
            data={"sub": str(db_user.id), "email": db_user.email},
            expires_delta=access_token_expires
        )

        # Log successful registration
        logger.info(f"Successful registration for user ID: {db_user.id}, email: {db_user.email}")

        return Token(access_token=access_token, token_type="bearer")

    except IntegrityError:
        # Email already exists
        session.rollback()
        logger.warning(f"Registration failed: Email {user_register.email} already exists")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    except Exception as e:
        logger.error(f"Unexpected error during registration: {str(e)}")
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )


@router.post("/login", response_model=Token)
@limiter.limit("10/minute")  # Rate limit login attempts
def login_user(
    user_login: UserLogin,
    request: Request,  # Needed for rate limiter
    session: Session = Depends(get_session)
) -> Token:
    """
    Authenticate user and return an access token.

    Args:
        user_login: User login data (email, password)
        request: HTTP request (needed for rate limiting)
        session: Database session

    Returns:
        Token containing access token for the authenticated user
    """
    # Log login attempt
    logger.info(f"Login attempt for email: {user_login.email}")

    # Find user in database
    user = session.query(User).filter(User.email == user_login.email).first()

    if not user:
        logger.warning(f"Login failed: User with email {user_login.email} not found")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verify the password
    if not verify_password(user_login.password, user.hashed_password):
        logger.warning(f"Login failed: Incorrect password for user {user_login.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email},
        expires_delta=access_token_expires
    )

    # Update last login time
    user.last_login_at = datetime.utcnow()
    session.add(user)
    session.commit()

    # Log successful login
    logger.info(f"Successful login for user ID: {user.id}, email: {user.email}")

    return Token(access_token=access_token, token_type="bearer")


@router.post("/logout")
def logout_user():
    """
    Logout endpoint (stateless - client should remove token).

    Returns:
        Success message
    """
    logger.info("Logout request received")
    # In a stateless JWT system, logout is typically handled client-side
    # This endpoint can be extended for token blacklisting if needed
    return {"message": "Successfully logged out"}