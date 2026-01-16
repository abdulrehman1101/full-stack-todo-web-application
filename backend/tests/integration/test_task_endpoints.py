"""
Integration tests for task API endpoints.
These tests verify the API routes using TestClient and httpx.
"""
import pytest
import sys
import os
# Add the parent directory to the path so we can import from src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from fastapi.testclient import TestClient
from sqlmodel import Session, select
from src.api.main import app
from src.database.models.user import User
from src.database.models.task import Task
from src.database.session import get_session
from src.auth.utils import create_jwt_token
from unittest.mock import patch
import json


@pytest.fixture
def client():
    """Create a test client for the API."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def mock_user_and_token(db_session: Session):
    """Create a mock user and JWT token for testing."""
    user = User(
        id=1,
        email="test@example.com",
        password_hash="hashed_password"
    )
    db_session.add(user)
    db_session.commit()

    token = create_jwt_token({"user_id": user.id, "email": user.email})
    return user, token


def test_create_task_endpoint(client: TestClient, mock_user_and_token):
    """Test creating a task via the API endpoint."""
    user, token = mock_user_and_token

    headers = {"Authorization": f"Bearer {token}"}
    task_data = {
        "title": "Test Task",
        "description": "Test Description",
        "is_completed": False
    }

    response = client.post("/api/v1/tasks/", json=task_data, headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "Test Description"
    assert data["is_completed"] is False
    assert data["user_id"] == user.id
    assert "id" in data
    assert "created_at" in data


def test_list_tasks_endpoint(client: TestClient, mock_user_and_token, db_session: Session):
    """Test listing tasks via the API endpoint."""
    user, token = mock_user_and_token

    # Create some tasks for the user
    task1 = Task(title="Task 1", user_id=user.id)
    task2 = Task(title="Task 2", user_id=user.id)
    db_session.add(task1)
    db_session.add(task2)
    db_session.commit()

    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/v1/tasks/", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2  # At least the 2 we created plus any from test_create_task_endpoint

    # Verify all returned tasks belong to the user
    for task in data:
        assert task["user_id"] == user.id


def test_get_specific_task_endpoint(client: TestClient, mock_user_and_token, db_session: Session):
    """Test getting a specific task via the API endpoint."""
    user, token = mock_user_and_token

    # Create a task
    task = Task(title="Specific Task", user_id=user.id)
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)

    headers = {"Authorization": f"Bearer {token}"}
    response = client.get(f"/api/v1/tasks/{task.id}", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task.id
    assert data["title"] == "Specific Task"
    assert data["user_id"] == user.id


def test_get_nonexistent_task_endpoint(client: TestClient, mock_user_and_token):
    """Test getting a nonexistent task returns 404."""
    _, token = mock_user_and_token

    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/v1/tasks/99999", headers=headers)

    assert response.status_code == 404


def test_update_task_endpoint(client: TestClient, mock_user_and_token, db_session: Session):
    """Test updating a task via the API endpoint."""
    user, token = mock_user_and_token

    # Create a task
    task = Task(title="Original Title", description="Original Description", user_id=user.id)
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)

    headers = {"Authorization": f"Bearer {token}"}
    update_data = {
        "title": "Updated Title",
        "description": "Updated Description",
        "is_completed": True
    }

    response = client.put(f"/api/v1/tasks/{task.id}", json=update_data, headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["description"] == "Updated Description"
    assert data["is_completed"] is True


def test_delete_task_endpoint(client: TestClient, mock_user_and_token, db_session: Session):
    """Test deleting a task via the API endpoint."""
    user, token = mock_user_and_token

    # Create a task
    task = Task(title="Task to Delete", user_id=user.id)
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)

    headers = {"Authorization": f"Bearer {token}"}
    response = client.delete(f"/api/v1/tasks/{task.id}", headers=headers)

    assert response.status_code == 200
    assert response.json() == {"message": "Task deleted successfully"}

    # Verify the task was deleted
    remaining_task = db_session.get(Task, task.id)
    assert remaining_task is None


def test_toggle_task_completion_endpoint(client: TestClient, mock_user_and_token, db_session: Session):
    """Test toggling task completion status via the API endpoint."""
    user, token = mock_user_and_token

    # Create a task with is_completed=False initially
    task = Task(title="Toggle Task", is_completed=False, user_id=user.id)
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)

    headers = {"Authorization": f"Bearer {token}"}

    # Toggle completion status
    response = client.patch(f"/api/v1/tasks/{task.id}/complete", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task.id
    assert data["is_completed"] is True  # Should be toggled to True

    # Toggle again to False
    response = client.patch(f"/api/v1/tasks/{task.id}/complete", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task.id
    assert data["is_completed"] is False  # Should be toggled back to False


def test_unauthorized_access_to_task_returns_404(client: TestClient, db_session: Session):
    """Test that accessing another user's task returns 404."""
    # Create two users
    user1 = User(email="user1@example.com", password_hash="hash1")
    user2 = User(email="user2@example.com", password_hash="hash2")
    db_session.add(user1)
    db_session.add(user2)
    db_session.commit()

    # Create a task for user1
    task = Task(title="User1's Task", user_id=user1.id)
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)

    # Generate token for user2
    token_user2 = create_jwt_token({"user_id": user2.id, "email": user2.email})
    headers = {"Authorization": f"Bearer {token_user2}"}

    # Try to access user1's task as user2 - should return 404
    response = client.get(f"/api/v1/tasks/{task.id}", headers=headers)
    assert response.status_code == 404

    # Try to update user1's task as user2 - should return 404
    update_data = {"title": "Hacked Task"}
    response = client.put(f"/api/v1/tasks/{task.id}", json=update_data, headers=headers)
    assert response.status_code == 404

    # Try to delete user1's task as user2 - should return 404
    response = client.delete(f"/api/v1/tasks/{task.id}", headers=headers)
    assert response.status_code == 404

    # Try to toggle user1's task completion as user2 - should return 404
    response = client.patch(f"/api/v1/tasks/{task.id}/complete", headers=headers)
    assert response.status_code == 404