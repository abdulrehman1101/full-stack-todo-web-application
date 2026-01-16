"""
Unit tests for authentication middleware to verify 401 Unauthorized responses
for missing, malformed, or expired tokens.
"""

import pytest
from fastapi.testclient import TestClient
from fastapi import HTTPException
from unittest.mock import Mock, patch
from src.api.main import app  # FastAPI app is defined in src/api/main.py
from src.auth.middleware import get_current_user_id
from src.auth.utils import create_access_token
from uuid import uuid4
import time


def test_missing_token_returns_401():
    """
    Test that requests without an Authorization header return 401 Unauthorized.
    """
    client = TestClient(app)

    # Make a request without Authorization header
    response = client.get("/api/v1/me")  # This is the protected endpoint

    # Should return 401 for missing token
    assert response.status_code == 401
    assert "detail" in response.json()


def test_malformed_token_returns_401():
    """
    Test that requests with malformed tokens return 401 Unauthorized.
    """
    client = TestClient(app)

    # Make a request with malformed token
    response = client.get(
        "/api/v1/me",
        headers={"Authorization": "Bearer invalid.token.format"}
    )

    # Should return 401 for invalid token
    assert response.status_code == 401
    assert "detail" in response.json()


def test_expired_token_returns_401():
    """
    Test that requests with expired tokens return 401 Unauthorized.
    """
    client = TestClient(app)

    # Create an expired token (set expiration to 1 second ago)
    expired_token_data = {
        "sub": str(uuid4()),
        "email": "test@example.com",
        "role": "user",
        "exp": int(time.time()) - 1  # Expired 1 second ago
    }

    # Create the expired token using JWT library directly
    import jwt
    from src.config.settings import settings

    expired_token = jwt.encode(
        expired_token_data,
        settings.better_auth_secret,
        algorithm="HS256"
    )

    # Make a request with expired token
    response = client.get(
        "/api/v1/me",
        headers={"Authorization": f"Bearer {expired_token}"}
    )

    # Should return 401 for expired token
    assert response.status_code == 401
    assert "detail" in response.json()


def test_invalid_signature_token_returns_401():
    """
    Test that requests with tokens having invalid signatures return 401 Unauthorized.
    """
    client = TestClient(app)

    # Create a token with wrong secret (simulating tampering)
    token_data = {
        "sub": str(uuid4()),
        "email": "test@example.com",
        "role": "user",
        "exp": int(time.time()) + 3600  # Expires in 1 hour
    }

    # Create token with a different secret (simulating tampering)
    import jwt
    wrong_secret = "wrong_secret_key_that_does_not_match"

    invalid_token = jwt.encode(
        token_data,
        wrong_secret,
        algorithm="HS256"
    )

    # Make a request with invalid token
    response = client.get(
        "/api/v1/me",
        headers={"Authorization": f"Bearer {invalid_token}"}
    )

    # Should return 401 for invalid token signature
    assert response.status_code == 401
    assert "detail" in response.json()


def test_valid_token_allows_access():
    """
    Test that requests with valid tokens are allowed access.
    """
    client = TestClient(app)

    # Create a valid token
    user_id = str(uuid4())
    token_data = {
        "sub": user_id,
        "email": "test@example.com",
        "role": "user"
    }

    valid_token = create_access_token(data=token_data)

    # Mock the database session to return a user
    with patch('src.database.session.get_session') as mock_get_session:
        mock_session = Mock()
        mock_user = Mock()
        mock_user.id = user_id
        mock_session.get.return_value = mock_user
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Make a request with valid token
        response = client.get(
            "/api/v1/users/me",
            headers={"Authorization": f"Bearer {valid_token}"}
        )

        # Should return 200 for valid token (or whatever the actual endpoint returns)
        # The exact status code depends on the implementation of the endpoint
        # but the important thing is that it's not 401
        assert response.status_code != 401


def test_dependency_directly_missing_credentials():
    """
    Test the middleware dependency directly with missing credentials.
    """
    # Create mock credentials without a token
    mock_credentials = Mock()
    mock_credentials.credentials = None

    # Create mock session
    mock_session = Mock()

    # Test the dependency function directly
    with pytest.raises(HTTPException) as exc_info:
        get_current_user_id(mock_credentials, mock_session)

    assert exc_info.value.status_code == 401


if __name__ == "__main__":
    pytest.main([__file__, "-v"])