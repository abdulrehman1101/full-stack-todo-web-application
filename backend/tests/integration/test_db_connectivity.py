"""
Integration tests for database connectivity in the todo application.
This module tests that the application can successfully connect to the database
and perform basic CRUD operations.
"""
import pytest
from sqlmodel import Session, select
from uuid import uuid4
from datetime import datetime
from backend.src.database.engine import engine
from backend.src.database.models.user import User
from backend.src.database.models.task import Task


def test_database_connectivity():
    """
    Test that the application can successfully connect to the database
    and perform a basic SELECT operation.
    """
    assert engine is not None, "Database engine should be initialized"

    with Session(engine) as session:
        # Execute a simple query to test connectivity
        result = session.exec(select(1))
        assert result is not None, "Should be able to execute a simple query"


def test_create_and_retrieve_user():
    """
    Test creating and retrieving a temporary user record from the database.
    """
    with Session(engine) as session:
        # Create a temporary user for testing
        temp_email = f"test_{uuid4()}@example.com"

        user = User(
            email=temp_email,
            created_at=datetime.utcnow()
        )

        session.add(user)
        session.commit()
        session.refresh(user)

        # Verify the user was created
        assert user.id is not None, "User should have an ID after creation"
        assert user.email == temp_email, "User email should match what was set"

        # Retrieve the user from the database
        retrieved_user = session.get(User, user.id)
        assert retrieved_user is not None, "Should be able to retrieve the created user"
        assert retrieved_user.id == user.id, "Retrieved user ID should match created user ID"
        assert retrieved_user.email == user.email, "Retrieved user email should match created user email"


def test_create_and_retrieve_task():
    """
    Test creating and retrieving a temporary task record from the database.
    """
    with Session(engine) as session:
        # First create a temporary user
        temp_email = f"task_test_{uuid4()}@example.com"

        user = User(
            email=temp_email,
            created_at=datetime.utcnow()
        )

        session.add(user)
        session.commit()
        session.refresh(user)

        # Create a temporary task associated with the user
        task_description = "Test task for integration testing"

        task = Task(
            user_id=user.id,
            description=task_description,
            is_completed=False,
            created_at=datetime.utcnow()
        )

        session.add(task)
        session.commit()
        session.refresh(task)

        # Verify the task was created
        assert task.id is not None, "Task should have an ID after creation"
        assert task.user_id == user.id, "Task should be associated with the correct user"
        assert task.description == task_description, "Task description should match what was set"

        # Retrieve the task from the database
        retrieved_task = session.get(Task, task.id)
        assert retrieved_task is not None, "Should be able to retrieve the created task"
        assert retrieved_task.id == task.id, "Retrieved task ID should match created task ID"
        assert retrieved_task.user_id == task.user_id, "Retrieved task user_id should match created task user_id"


def test_user_task_relationship():
    """
    Test that the relationship between User and Task works correctly.
    """
    with Session(engine) as session:
        # Create a temporary user
        temp_email = f"relationship_test_{uuid4()}@example.com"

        user = User(
            email=temp_email,
            created_at=datetime.utcnow()
        )

        session.add(user)
        session.commit()
        session.refresh(user)

        # Create a task associated with the user
        task_description = "Test task for relationship testing"

        task = Task(
            user_id=user.id,
            description=task_description,
            is_completed=False,
            created_at=datetime.utcnow()
        )

        session.add(task)
        session.commit()
        session.refresh(task)

        # Query for the user's tasks to verify the relationship
        statement = select(Task).where(Task.user_id == user.id)
        user_tasks = session.exec(statement).all()

        assert len(user_tasks) == 1, "User should have exactly one task"
        assert user_tasks[0].id == task.id, "The task should be the one we created"


if __name__ == "__main__":
    print("Running database connectivity integration tests...")

    try:
        test_database_connectivity()
        print("✓ Database connectivity test passed")

        test_create_and_retrieve_user()
        print("✓ User creation and retrieval test passed")

        test_create_and_retrieve_task()
        print("✓ Task creation and retrieval test passed")

        test_user_task_relationship()
        print("✓ User-task relationship test passed")

        print("\nAll database connectivity tests PASSED!")

    except Exception as e:
        print(f"\nDatabase connectivity tests FAILED: {str(e)}")
        raise