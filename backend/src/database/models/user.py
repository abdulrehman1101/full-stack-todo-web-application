"""
User model for the todo application.
This model represents a registered user in the system and serves as both
a database schema and API validation model.
"""
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from uuid import UUID, uuid4
import re
from pydantic import field_validator


class UserBase(SQLModel):
    """
    Base model for User that contains common fields for validation.
    """
    email: str = Field(min_length=5, max_length=255, regex=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    name: Optional[str] = Field(default=None, max_length=255)
    username: Optional[str] = Field(default=None, max_length=255, regex=r'^[a-zA-Z0-9_-]+$')


class UserCreate(UserBase):
    """
    Model for creating new users via API.
    Excludes id and created_at since they are auto-generated.
    """
    password: str = Field(min_length=8, max_length=128)  # Password field for creation


class User(UserBase, table=True):
    """
    User model representing a registered user in the system.
    Contains fields: id (primary key), email (unique), created_at, and audit fields.
    This model serves both as a database schema and API validation model.
    """
    __tablename__ = "user"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(
        sa_column_kwargs={
            "unique": True,
            "index": True,
            "nullable": False
        }
    )
    name: Optional[str] = Field(default=None, max_length=255)
    username: Optional[str] = Field(default=None, max_length=255, sa_column_kwargs={"unique": True, "index": True})
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)  # Track last update/activity time
    last_login_at: Optional[datetime] = Field(default=None)  # Audit trail for last login
    failed_login_attempts: int = Field(default=0)  # Track failed login attempts
    locked_until: Optional[datetime] = Field(default=None)  # Account lockout functionality

    # Password field for authentication
    hashed_password: str = Field(sa_column_kwargs={"nullable": False})

    # Relationship to Task model
    tasks: List["Task"] = Relationship(back_populates="user", sa_relationship_kwargs={"cascade": "all, delete-orphan"})

    @field_validator('email')
    @classmethod
    def validate_email_format(cls, v):
        """
        Validates email format using a regex pattern.
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, v):
            raise ValueError('Invalid email format')
        return v


class UserRead(UserBase):
    """
    Model for reading user data via API.
    Includes id, created_at, and audit fields.
    """
    id: UUID
    created_at: datetime
    updated_at: datetime
    last_login_at: Optional[datetime] = None
    failed_login_attempts: int = 0
    locked_until: Optional[datetime] = None