"""
Exception Classes for Todo Application

This module defines custom exception classes for task operations.
"""


class TaskNotFoundError(Exception):
    """Raised when a requested task does not exist in the TaskList."""

    def __init__(self, task_id: int):
        self.task_id = task_id
        super().__init__(f"Task with ID {task_id} not found")


class InvalidTaskDescriptionError(Exception):
    """Raised when a task description is invalid according to validation rules."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class DuplicateTaskIdError(Exception):
    """Raised when attempting to add a task with an ID that already exists."""

    def __init__(self, task_id: int):
        self.task_id = task_id
        super().__init__(f"Task with ID {task_id} already exists")