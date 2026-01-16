"""
Authentication utilities for the todo application.
This module provides JWT encoding/decoding utilities and token validation functions.
"""

from typing import Optional, Dict, Any
import jwt
from jose import jwt as jose_jwt, JWTError
from datetime import datetime, timedelta
import uuid
import time
import calendar
import hashlib


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token with the provided data.

    Args:
        data: Dictionary containing the data to encode in the token
        expires_delta: Optional timedelta for token expiration (default: 15 minutes)

    Returns:
        Encoded JWT token as string
    """
    from ..config.settings import settings

    if not settings.better_auth_secret:
        raise ValueError("BETTER_AUTH_SECRET environment variable not set")

    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    # Convert datetime to timestamp for JWT
    expire_timestamp = calendar.timegm(expire.utctimetuple())

    to_encode.update({"exp": expire_timestamp, "jti": str(uuid.uuid4())})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.better_auth_secret,
        algorithm="HS256"
    )
    return encoded_jwt


def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Verify and decode a JWT token with enhanced security for tampering detection.

    Args:
        token: JWT token string to verify

    Returns:
        Decoded token payload if valid, None if invalid
    """
    from ..config.settings import settings
    import logging

    logger = logging.getLogger(__name__)

    if not settings.better_auth_secret:
        raise ValueError("BETTER_AUTH_SECRET environment variable not set")

    if not token:
        logger.warning("Empty token provided for verification")
        return None

    try:
        # Additional validation: check token structure before decoding
        parts = token.split('.')
        if len(parts) != 3:
            logger.warning("Invalid token format: not a valid JWT structure")
            return None

        # Decode the token
        payload = jose_jwt.decode(
            token,
            settings.better_auth_secret,
            algorithms=["HS256"]
        )

        # Additional validation: check if token is expired
        exp = payload.get("exp")
        if exp and exp < time.time():
            logger.warning("Token validation failed: token has expired")
            return None

        # Validate required claims
        required_claims = ['sub', 'exp', 'jti']
        for claim in required_claims:
            if claim not in payload:
                logger.warning(f"Token validation failed: missing required claim '{claim}'")
                return None

        logger.info("Token validation successful")
        return payload
    except JWTError as e:
        logger.warning(f"JWT validation error: {str(e)} - possible token tampering")
        return None
    except Exception as e:
        logger.error(f"Unexpected error during token verification: {str(e)}")
        return None


def extract_user_id_from_token(token: str) -> Optional[str]:
    """
    Extract the user ID from a JWT token.

    Args:
        token: JWT token string

    Returns:
        User ID if found and token is valid, None otherwise
    """
    payload = verify_token(token)
    if payload:
        return payload.get("sub")  # 'sub' is standard for subject/user ID
    return None


def hash_password(password: str) -> str:
    """
    Hash a password using SHA-256 with salt.

    Args:
        password: Plain text password

    Returns:
        Hashed password string
    """
    # Simple SHA-256 hashing with a static salt (in production, use bcrypt or similar)
    # For demo purposes only - in production use bcrypt, scrypt, or argon2
    import secrets
    salt = secrets.token_hex(16)  # Generate a random salt
    pwdhash = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()
    return f"{salt}${pwdhash}"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.

    Args:
        plain_password: Plain text password to verify
        hashed_password: Previously hashed password

    Returns:
        True if password matches, False otherwise
    """
    # Split the stored hash to get salt and hash
    try:
        salt, stored_hash = hashed_password.split('$')
        pwdhash = hashlib.sha256((plain_password + salt).encode('utf-8')).hexdigest()
        return pwdhash == stored_hash
    except ValueError:
        # If the format is incorrect, return False
        return False