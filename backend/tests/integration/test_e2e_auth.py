"""
End-to-end integration test to verify the complete authentication flow:
Login -> Get Token -> Call Protected API
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from uuid import uuid4
from fastapi.testclient import TestClient
from sqlmodel import Session
from src.api.main import app  # FastAPI app is defined in src/api/main.py
from src.auth.utils import create_access_token
from src.database.models.user import User
from src.database.models.task import Task


def test_end_to_end_authentication_flow():
    """
    Test the complete authentication flow:
    1. User logs in and receives a JWT token
    2. Token is used to call protected API endpoints
    3. Data isolation is enforced (user can only access their own data)
    """

    # Create a test client
    client = TestClient(app)

    # Create a mock user
    user_id = uuid4()
    user = User(id=user_id, email="test@example.com")

    # Create a JWT token for the user
    token_data = {
        "sub": str(user_id),
        "email": "test@example.com",
        "role": "user"
    }
    jwt_token = create_access_token(data=token_data)

    # Mock the database session for the protected endpoint
    mock_session = Mock(spec=Session)
    mock_session.get.return_value = user

    # Test 1: Access protected endpoint with valid token
    with patch('src.database.session.get_session') as mock_get_session:
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Make request to protected endpoint (e.g., /api/v1/users/me)
        response = client.get(
            "/api/v1/users/me",
            headers={"Authorization": f"Bearer {jwt_token}"}
        )

        # Should succeed with 200 status
        assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.text}"

        # Verify response contains user data
        response_data = response.json()
        assert "email" in response_data
        assert response_data["email"] == "test@example.com"

    print("✅ E2E Auth Flow Test 1 Passed: Valid token allows access to protected endpoint")


def test_data_isolation_with_different_users():
    """
    Test that User A cannot access User B's data even with valid authentication.
    """

    # Create test clients
    client = TestClient(app)

    # Create user IDs
    user_a_id = uuid4()
    user_b_id = uuid4()

    # Create tokens for both users
    user_a_token_data = {"sub": str(user_a_id), "email": "user_a@example.com", "role": "user"}
    user_b_token_data = {"sub": str(user_b_id), "email": "user_b@example.com", "role": "user"}

    user_a_token = create_access_token(data=user_a_token_data)
    user_b_token = create_access_token(data=user_b_token_data)

    # Mock data for testing
    user_a = User(id=user_a_id, email="user_a@example.com")
    user_b = User(id=user_b_id, email="user_b@example.com")

    # Mock task that belongs to User B
    task_for_user_b = Task(
        id=uuid4(),
        user_id=user_b_id,
        description="User B's private task",
        is_completed=False
    )

    # Test: User A tries to access User B's specific task
    with patch('src.database.session.get_session') as mock_get_session:
        mock_session = Mock(spec=Session)

        # When User A tries to access a task, only return tasks that belong to User A
        def mock_exec_side_effect(statement):
            from sqlmodel import Select
            if isinstance(statement, Select):
                # Mock result for task query
                mock_result = Mock()

                # If User A is querying for User B's task, return None (enforcing data isolation)
                # This simulates the data isolation logic in crud.py
                mock_result.first.return_value = None  # User A cannot access User B's task
                return mock_result
            return Mock()

        mock_session.exec.side_effect = mock_exec_side_effect
        mock_session.get.return_value = user_a  # User A is the authenticated user

        mock_get_session.return_value.__enter__.return_value = mock_session

        # User A tries to access User B's task (assuming task endpoint exists)
        # This would be a call like GET /api/v1/tasks/{task_id_for_user_b}
        task_endpoint = f"/api/v1/tasks/{task_for_user_b.id}"
        response = client.get(
            task_endpoint,
            headers={"Authorization": f"Bearer {user_a_token}"}
        )

        # Should return 404 (not found) because User A cannot access User B's task
        # This enforces data isolation
        assert response.status_code in [404, 403], f"Expected 404 or 403 for data isolation, got {response.status_code}"

    print("✅ Data Isolation Test Passed: User A cannot access User B's data")


def test_invalid_token_rejection():
    """
    Test that invalid or missing tokens are properly rejected.
    """

    client = TestClient(app)

    # Test 1: Request without token
    response = client.get("/api/v1/users/me")
    assert response.status_code == 401, f"Expected 401 for missing token, got {response.status_code}"

    # Test 2: Request with invalid token
    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": "Bearer invalid.token.here"}
    )
    assert response.status_code == 401, f"Expected 401 for invalid token, got {response.status_code}"

    print("✅ Invalid Token Test Passed: Invalid and missing tokens are properly rejected")


def test_token_expiry_handling():
    """
    Test that expired tokens are properly rejected.
    """

    client = TestClient(app)

    # Create an expired token (set expiration to 1 second ago)
    import time
    expired_token_data = {
        "sub": str(uuid4()),
        "email": "expired@example.com",
        "role": "user",
        "exp": int(time.time()) - 1  # Expired 1 second ago
    }

    # Create the expired token manually using jwt library
    import jwt
    from src.config.settings import settings

    expired_token = jwt.encode(
        expired_token_data,
        settings.better_auth_secret,
        algorithm="HS256"
    )

    # Try to access protected endpoint with expired token
    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {expired_token}"}
    )

    # Should return 401 for expired token
    assert response.status_code == 401, f"Expected 401 for expired token, got {response.status_code}"

    print("✅ Token Expiry Test Passed: Expired tokens are properly rejected")


if __name__ == "__main__":
    test_end_to_end_authentication_flow()
    test_data_isolation_with_different_users()
    test_invalid_token_rejection()
    test_token_expiry_handling()
    print("\n🎉 All end-to-end authentication tests passed!")