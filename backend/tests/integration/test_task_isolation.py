"""
Critical security test for task data isolation.
This test verifies that users cannot access, modify, or delete tasks belonging to other users.
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
from src.auth.utils import create_jwt_token


@pytest.fixture
def client():
    """Create a test client for the API."""
    with TestClient(app) as test_client:
        yield test_client


def test_cross_user_task_access_isolation(client: TestClient, db_session: Session):
    """
    Critical Security Test: Verify that User A cannot access/modify User B's tasks.

    Scenario: Log in as User A, create a task. Log in as User B, try to GET, PUT, or DELETE User A's task.
    Expected Result: The API must return a 404 Not Found for all cross-user attempts.
    """
    # Create User A
    user_a = User(email="user_a@example.com", password_hash="hashed_password_a")
    db_session.add(user_a)
    db_session.commit()
    db_session.refresh(user_a)

    # Create User B
    user_b = User(email="user_b@example.com", password_hash="hashed_password_b")
    db_session.add(user_b)
    db_session.commit()
    db_session.refresh(user_b)

    # User A creates a task (authenticate as User A)
    token_a = create_jwt_token({"user_id": user_a.id, "email": user_a.email})
    headers_a = {"Authorization": f"Bearer {token_a}"}

    task_data = {
        "title": "User A's Private Task",
        "description": "This belongs to User A only",
        "is_completed": False
    }

    create_response = client.post("/api/v1/tasks/", json=task_data, headers=headers_a)
    assert create_response.status_code == 200
    task_data_response = create_response.json()
    task_id = task_data_response["id"]
    assert task_data_response["title"] == "User A's Private Task"
    assert task_data_response["user_id"] == user_a.id

    # Now try to access User A's task as User B (authenticate as User B)
    token_b = create_jwt_token({"user_id": user_b.id, "email": user_b.email})
    headers_b = {"Authorization": f"Bearer {token_b}"}

    # Test 1: User B tries to GET User A's task (should return 404)
    get_response = client.get(f"/api/v1/tasks/{task_id}", headers=headers_b)
    assert get_response.status_code == 404, f"GET /api/v1/tasks/{task_id} should return 404, got {get_response.status_code}"
    assert get_response.json()["detail"] == "Task not found"

    # Test 2: User B tries to PUT (update) User A's task (should return 404)
    update_data = {"title": "User B trying to change User A's task"}
    put_response = client.put(f"/api/v1/tasks/{task_id}", json=update_data, headers=headers_b)
    assert put_response.status_code == 404, f"PUT /api/v1/tasks/{task_id} should return 404, got {put_response.status_code}"
    assert put_response.json()["detail"] == "Task not found"

    # Test 3: User B tries to DELETE User A's task (should return 404)
    delete_response = client.delete(f"/api/v1/tasks/{task_id}", headers=headers_b)
    assert delete_response.status_code == 404, f"DELETE /api/v1/tasks/{task_id} should return 404, got {delete_response.status_code}"
    assert delete_response.json()["detail"] == "Task not found"

    # Test 4: User B tries to PATCH (toggle completion) of User A's task (should return 404)
    patch_response = client.patch(f"/api/v1/tasks/{task_id}/complete", headers=headers_b)
    assert patch_response.status_code == 404, f"PATCH /api/v1/tasks/{task_id}/complete should return 404, got {patch_response.status_code}"
    assert patch_response.json()["detail"] == "Task not found"

    # Verify User A can still access their own task
    final_get_response = client.get(f"/api/v1/tasks/{task_id}", headers=headers_a)
    assert final_get_response.status_code == 200, f"User A should still be able to access their task, got {final_get_response.status_code}"
    final_task_data = final_get_response.json()
    assert final_task_data["id"] == task_id
    assert final_task_data["user_id"] == user_a.id

    print("✅ Critical Security Test PASSED: Data isolation is working correctly!")
    print("✅ User B cannot access, modify, or delete User A's tasks")
    print("✅ All cross-user attempts correctly return 404 Not Found")


def test_multiple_users_data_isolation(client: TestClient, db_session: Session):
    """
    Additional test: Verify data isolation with multiple users.
    """
    # Create multiple users
    users = []
    for i in range(3):
        user = User(email=f"user{i}@example.com", password_hash=f"hashed_password_{i}")
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        users.append(user)

    # Each user creates a task
    tokens = []
    task_ids = []

    for i, user in enumerate(users):
        token = create_jwt_token({"user_id": user.id, "email": user.email})
        tokens.append(token)

        headers = {"Authorization": f"Bearer {token}"}
        task_data = {
            "title": f"Task for User {i}",
            "description": f"This is User {i}'s task",
            "is_completed": False
        }

        response = client.post("/api/v1/tasks/", json=task_data, headers=headers)
        assert response.status_code == 200
        task_id = response.json()["id"]
        task_ids.append(task_id)

    # Verify each user can only access their own tasks
    for i, (user, token, own_task_id) in enumerate(zip(users, tokens, task_ids)):
        headers = {"Authorization": f"Bearer {token}"}

        # Each user should only see their own task when listing
        list_response = client.get("/api/v1/tasks/", headers=headers)
        assert list_response.status_code == 200
        tasks = list_response.json()

        # Verify all returned tasks belong to the current user
        for task in tasks:
            assert task["user_id"] == user.id

        # Verify each user can access their own task
        own_get_response = client.get(f"/api/v1/tasks/{own_task_id}", headers=headers)
        assert own_get_response.status_code == 200
        own_task = own_get_response.json()
        assert own_task["id"] == own_task_id
        assert own_task["user_id"] == user.id

        # Verify each user cannot access other users' tasks
        for j, other_task_id in enumerate(task_ids):
            if i != j:  # Different user's task
                other_get_response = client.get(f"/api/v1/tasks/{other_task_id}", headers=headers)
                assert other_get_response.status_code == 404, \
                    f"User {i} should not be able to access User {j}'s task {other_task_id}"

    print("✅ Multiple Users Data Isolation Test PASSED: Each user can only access their own data!")


def test_user_cannot_modify_other_users_tasks_even_if_id_known(client: TestClient, db_session: Session):
    """
    Test that knowing another user's task ID is not sufficient to access it without ownership.
    """
    # Create two users
    user_owner = User(email="owner@example.com", password_hash="owner_hash")
    user_attacker = User(email="attacker@example.com", password_hash="attacker_hash")
    db_session.add(user_owner)
    db_session.add(user_attacker)
    db_session.commit()

    # Owner creates a task
    token_owner = create_jwt_token({"user_id": user_owner.id, "email": user_owner.email})
    headers_owner = {"Authorization": f"Bearer {token_owner}"}

    task_data = {
        "title": "Owner's Secret Task",
        "description": "Only owner should see this",
        "is_completed": False
    }

    create_response = client.post("/api/v1/tasks/", json=task_data, headers=headers_owner)
    assert create_response.status_code == 200
    task_id = create_response.json()["id"]

    # Attacker tries to access the task knowing its ID
    token_attacker = create_jwt_token({"user_id": user_attacker.id, "email": user_attacker.email})
    headers_attacker = {"Authorization": f"Bearer {token_attacker}"}

    # All operations should fail with 404
    operations = [
        ("GET", f"/api/v1/tasks/{task_id}"),
        ("PUT", f"/api/v1/tasks/{task_id}", {"title": "Attacker trying to change"}),
        ("DELETE", f"/api/v1/tasks/{task_id}"),
        ("PATCH", f"/api/v1/tasks/{task_id}/complete")
    ]

    for op in operations:
        method = op[0]
        url = op[1]
        json_data = op[2] if len(op) > 2 else None

        if method == "GET":
            response = client.get(url, headers=headers_attacker)
        elif method == "PUT":
            response = client.put(url, json=json_data, headers=headers_attacker)
        elif method == "DELETE":
            response = client.delete(url, headers=headers_attacker)
        elif method == "PATCH":
            response = client.patch(url, headers=headers_attacker)

        assert response.status_code == 404, \
            f"Operation {method} {url} should return 404 for non-owner, got {response.status_code}"
        assert response.json()["detail"] == "Task not found"

    print("✅ Known-ID Attack Prevention Test PASSED: Knowing task ID is not enough without ownership!")