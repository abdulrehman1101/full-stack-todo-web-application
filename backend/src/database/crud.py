"""
Database CRUD operations for the todo application.
This module provides functions for creating, reading, updating, and deleting
records in the database with proper user isolation.
"""

from typing import List, Optional
from sqlmodel import Session, select
from ..database.models.user import User
from ..database.models.task import Task, TaskCreate, TaskUpdate
from uuid import UUID


def create_user(*, session: Session, email: str) -> User:
    """
    Create a new user in the database.

    Args:
        session: Database session
        email: User's email address

    Returns:
        Created User object
    """
    user = User(email=email)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def get_user_by_id(*, session: Session, user_id: UUID) -> Optional[User]:
    """
    Get a user by their ID.

    Args:
        session: Database session
        user_id: User's UUID

    Returns:
        User object if found, None otherwise
    """
    statement = select(User).where(User.id == user_id)
    user = session.exec(statement).first()
    return user


def get_user_by_email(*, session: Session, email: str) -> Optional[User]:
    """
    Get a user by their email address.

    Args:
        session: Database session
        email: User's email address

    Returns:
        User object if found, None otherwise
    """
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()
    return user


def create_task_for_user(*, session: Session, task_create: TaskCreate, user_id: UUID) -> Task:
    """
    Create a new task for a specific user.

    Args:
        session: Database session
        task_create: Task creation data
        user_id: ID of the user creating the task

    Returns:
        Created Task object
    """
    task = Task.from_orm(task_create)
    task.user_id = user_id
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def get_task_by_id_for_user(*, session: Session, task_id: UUID, user_id: UUID) -> Optional[Task]:
    """
    Get a specific task for a specific user (enforces data isolation).

    Args:
        session: Database session
        task_id: Task ID to retrieve
        user_id: User ID that owns the task

    Returns:
        Task object if found and owned by user, None otherwise
    """
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(statement).first()
    return task


def get_tasks_for_user(*, session: Session, user_id: UUID) -> List[Task]:
    """
    Get all tasks for a specific user.

    Args:
        session: Database session
        user_id: User ID whose tasks to retrieve

    Returns:
        List of Task objects belonging to the user
    """
    statement = select(Task).where(Task.user_id == user_id)
    tasks = session.exec(statement).all()
    return tasks


def update_task_for_user(*, session: Session, task_id: UUID, task_update: TaskUpdate, user_id: UUID) -> Optional[Task]:
    """
    Update a task for a specific user (enforces data isolation).

    Args:
        session: Database session
        task_id: Task ID to update
        task_update: Update data
        user_id: User ID that owns the task

    Returns:
        Updated Task object if found and owned by user, None otherwise
    """
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(statement).first()

    if not task:
        return None

    # Update task fields based on provided values
    for field, value in task_update.dict(exclude_unset=True).items():
        setattr(task, field, value)

    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def delete_task_for_user(*, session: Session, task_id: UUID, user_id: UUID) -> bool:
    """
    Delete a task for a specific user (enforces data isolation).

    Args:
        session: Database session
        task_id: Task ID to delete
        user_id: User ID that owns the task

    Returns:
        True if task was found and deleted, False otherwise
    """
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(statement).first()

    if not task:
        return False

    session.delete(task)
    session.commit()
    return True


def delete_all_tasks_for_user(*, session: Session, user_id: UUID) -> int:
    """
    Delete all tasks for a specific user.

    Args:
        session: Database session
        user_id: User ID whose tasks to delete

    Returns:
        Number of tasks deleted
    """
    statement = select(Task).where(Task.user_id == user_id)
    tasks = session.exec(statement).all()

    count = 0
    for task in tasks:
        session.delete(task)
        count += 1

    session.commit()
    return count