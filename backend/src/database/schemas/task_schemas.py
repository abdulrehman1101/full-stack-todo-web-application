from typing import Optional
from uuid import UUID
from sqlmodel import SQLModel
from datetime import datetime


class TaskBase(SQLModel):
    """Base schema for task operations"""
    title: str
    description: Optional[str] = None
    is_completed: bool = False


class TaskCreate(TaskBase):
    """Schema for creating a new task"""
    pass  # All fields from TaskBase are required for creation


class TaskUpdate(SQLModel):
    """Schema for updating an existing task"""
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None


class TaskRead(TaskBase):
    """Schema for reading task data with additional fields"""
    id: UUID
    user_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True