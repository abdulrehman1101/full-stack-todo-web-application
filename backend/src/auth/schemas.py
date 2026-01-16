"""
Authentication schemas for the todo application.
This module provides Pydantic schemas for authentication-related data.
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Token(BaseModel):
    """
    Schema for JWT token response.
    """
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """
    Schema for JWT token data payload.
    """
    user_id: Optional[str] = None
    email: Optional[str] = None
    expires_at: Optional[datetime] = None


class UserLogin(BaseModel):
    """
    Schema for user login request.
    """
    email: str
    password: str


class UserRegister(BaseModel):
    """
    Schema for user registration request.
    """
    email: str
    password: str


class UserResponse(BaseModel):
    """
    Schema for user response data.
    """
    id: str
    email: str
    name: Optional[str] = None
    username: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
        """Convert from ORM object to Pydantic model."""
        return cls(
            id=str(obj.id),
            email=obj.email,
            name=getattr(obj, 'name', None),
            username=getattr(obj, 'username', None),
            created_at=obj.created_at,
            updated_at=obj.updated_at
        )


class UserUpdateRequest(BaseModel):
    """
    Schema for user update request.
    """
    name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None