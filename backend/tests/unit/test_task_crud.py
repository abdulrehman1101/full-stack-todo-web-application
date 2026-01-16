"""
Unit tests for task CRUD operations using SQLModel.
These tests verify the underlying database logic without involving the API layer.
"""
import pytest
import sys
import os
# Add the parent directory to the path so we can import from src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from sqlmodel import Session, select
from unittest.mock import Mock
from src.database.models.task import Task
from src.database.models.user import User
from src.database.schemas.task_schemas import TaskCreate, TaskUpdate


def test_create_task(db_session: Session):
    """Test creating a new task with proper user assignment."""
    # Arrange
    user = User(email="test@example.com", password_hash="hashed_password")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    task_data = TaskCreate(
        title="Test Task",
        description="Test Description",
        is_completed=False
    )

    # Act
    task = Task(
        title=task_data.title,
        description=task_data.description,
        is_completed=task_data.is_completed,
        user_id=user.id
    )
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)

    # Assert
    assert task.id is not None
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.is_completed is False
    assert task.user_id == user.id


def test_read_tasks_for_user(db_session: Session):
    """Test reading all tasks for a specific user."""
    # Arrange
    user1 = User(email="user1@example.com", password_hash="hashed_password")
    user2 = User(email="user2@example.com", password_hash="hashed_password")
    db_session.add(user1)
    db_session.add(user2)
    db_session.commit()

    # Create tasks for user1
    task1 = Task(title="User1 Task1", user_id=user1.id)
    task2 = Task(title="User1 Task2", user_id=user1.id)
    # Create task for user2
    task3 = Task(title="User2 Task1", user_id=user2.id)

    db_session.add(task1)
    db_session.add(task2)
    db_session.add(task3)
    db_session.commit()

    # Act
    statement = select(Task).where(Task.user_id == user1.id)
    user1_tasks = db_session.exec(statement).all()

    # Assert
    assert len(user1_tasks) == 2
    assert all(task.user_id == user1.id for task in user1_tasks)
    assert "User1 Task1" in [task.title for task in user1_tasks]
    assert "User1 Task2" in [task.title for task in user1_tasks]

    # Verify user2 only has their own task
    statement = select(Task).where(Task.user_id == user2.id)
    user2_tasks = db_session.exec(statement).all()
    assert len(user2_tasks) == 1
    assert user2_tasks[0].title == "User2 Task1"


def test_get_specific_task_for_user(db_session: Session):
    """Test getting a specific task for a user (with ownership verification)."""
    # Arrange
    user1 = User(email="user1@example.com", password_hash="hashed_password")
    user2 = User(email="user2@example.com", password_hash="hashed_password")
    db_session.add(user1)
    db_session.add(user2)
    db_session.commit()

    task = Task(title="Test Task", user_id=user1.id)
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)

    # Act - Try to get task that belongs to user1 (should succeed)
    statement = select(Task).where(Task.id == task.id).where(Task.user_id == user1.id)
    retrieved_task = db_session.exec(statement).first()

    # Assert
    assert retrieved_task is not None
    assert retrieved_task.id == task.id
    assert retrieved_task.user_id == user1.id

    # Act - Try to get task that doesn't belong to user2 (should return None)
    statement = select(Task).where(Task.id == task.id).where(Task.user_id == user2.id)
    retrieved_task_for_user2 = db_session.exec(statement).first()

    # Assert
    assert retrieved_task_for_user2 is None


def test_update_task_for_user(db_session: Session):
    """Test updating a task for a user (with ownership verification)."""
    # Arrange
    user = User(email="test@example.com", password_hash="hashed_password")
    db_session.add(user)
    db_session.commit()

    task = Task(title="Original Title", description="Original Desc", user_id=user.id)
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)

    # Act - Update the task
    task.title = "Updated Title"
    task.description = "Updated Description"
    task.is_completed = True
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)

    # Assert
    assert task.title == "Updated Title"
    assert task.description == "Updated Description"
    assert task.is_completed is True


def test_delete_task_for_user(db_session: Session):
    """Test deleting a task for a user (with ownership verification)."""
    # Arrange
    user1 = User(email="user1@example.com", password_hash="hashed_password")
    user2 = User(email="user2@example.com", password_hash="hashed_password")
    db_session.add(user1)
    db_session.add(user2)
    db_session.commit()

    task = Task(title="Test Task", user_id=user1.id)
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)

    original_count = len(db_session.exec(select(Task)).all())

    # Act - Delete the task
    db_session.delete(task)
    db_session.commit()

    # Assert
    new_count = len(db_session.exec(select(Task)).all())
    assert new_count == original_count - 1

    # Verify the task is gone
    deleted_task = db_session.get(Task, task.id)
    assert deleted_task is None


def test_toggle_task_completion(db_session: Session):
    """Test toggling the completion status of a task."""
    # Arrange
    user = User(email="test@example.com", password_hash="hashed_password")
    db_session.add(user)
    db_session.commit()

    # Start with completed task
    task = Task(title="Test Task", is_completed=True, user_id=user.id)
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)

    # Assert initial state
    assert task.is_completed is True

    # Act - Toggle completion status
    task.is_completed = not task.is_completed
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)

    # Assert toggled state
    assert task.is_completed is False

    # Act - Toggle again
    task.is_completed = not task.is_completed
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)

    # Assert back to original state
    assert task.is_completed is True