"""
Task Model for Todo Application

This module defines the Task data model with all required attributes and validation.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Task:
    """
    Represents a single todo item in the application.

    Attributes:
        id: Unique identifier for the task (auto-incremented)
        description: Task description (required, 1+ characters, < 500 characters)
        completed: Boolean indicating completion status (default: False)
        created_at: Timestamp of task creation (auto-set)
    """

    id: int
    description: str
    completed: bool = False
    created_at: datetime = None

    def __post_init__(self):
        """Initialize the created_at timestamp if not provided."""
        if self.created_at is None:
            self.created_at = datetime.now()

        # Validate the task attributes
        self._validate()

    def _validate(self):
        """Validate the task attributes according to the data model."""
        if not isinstance(self.id, int) or self.id <= 0:
            raise ValueError(f"ID must be a positive integer, got {self.id}")

        if not isinstance(self.description, str):
            raise ValueError(f"Description must be a string, got {type(self.description)}")

        if len(self.description.strip()) == 0:
            raise ValueError("Description must be non-empty (1+ characters)")

        if len(self.description) >= 500:
            raise ValueError(f"Description must be less than 500 characters, got {len(self.description)}")

        if not isinstance(self.completed, bool):
            raise ValueError(f"Completed status must be a boolean, got {type(self.completed)}")

    def mark_complete(self):
        """Mark the task as complete."""
        self.completed = True

    def mark_incomplete(self):
        """Mark the task as incomplete."""
        self.completed = False


def validate_task_description(description: str) -> bool:
    """
    Validate a task description according to the data model rules.

    Args:
        description: The description to validate

    Returns:
        True if valid, raises ValueError if invalid
    """
    if not isinstance(description, str):
        raise ValueError(f"Description must be a string, got {type(description)}")

    if len(description.strip()) == 0:
        raise ValueError("Description must be non-empty (1+ characters)")

    if len(description) >= 500:
        raise ValueError(f"Description must be less than 500 characters, got {len(description)}")

    return True