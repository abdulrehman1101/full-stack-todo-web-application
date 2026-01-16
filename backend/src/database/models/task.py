"""
Task model for the todo application.
This model represents a todo item associated with a user and serves as both
a database schema and API validation model.
"""
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy import ForeignKey


class TaskBase(SQLModel):
    """
    Base model for Task that contains common fields for validation.
    """
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(min_length=1, max_length=500)
    is_completed: bool = Field(default=False)


class Task(TaskBase, table=True):
    """
    Task model representing a todo item associated with a user.
    Contains fields: id (primary key), user_id (foreign key), title, description,
    is_completed (default False), and created_at.
    This model serves both as a database schema and API validation model.
    """
    __tablename__ = "task"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", nullable=False)
    title: str = Field(
        min_length=1,
        max_length=200,
        sa_column_kwargs={
            "nullable": False,
            "index": True
        }
    )
    description: str = Field(
        min_length=1,
        max_length=500,
        sa_column_kwargs={
            "nullable": False
        }
    )
    is_completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to User model
    user: Optional["User"] = Relationship(back_populates="tasks")


class TaskCreate(TaskBase):
    """
    Model for creating new tasks via API.
    Excludes id and created_at since they are auto-generated.
    user_id is passed separately in the API.
    """
    user_id: UUID


class TaskRead(TaskBase):
    """
    Model for reading task data via API.
    Includes id, user_id, and created_at fields.
    """
    id: UUID
    user_id: UUID
    created_at: datetime


class TaskUpdate(SQLModel):
    """
    Model for updating tasks via API.
    All fields are optional to allow partial updates.
    """
    description: Optional[str] = Field(default=None, min_length=1, max_length=500)
    is_completed: Optional[bool] = Field(default=None)