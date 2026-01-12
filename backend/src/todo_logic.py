"""
Core Logic Module for Todo Application

This module implements the core business logic for task management as requested.
"""
import os
import sys
from typing import List, Optional

# Handle imports for both direct execution and module execution
try:
    from .models.task import Task
    from .models.task_list import TaskList
    from .models.exceptions import TaskNotFoundError, InvalidTaskDescriptionError
except ImportError:
    # When run as a script, need to handle imports differently
    import importlib.util

    # Import using absolute paths
    models_dir = os.path.join(os.path.dirname(__file__), "models")

    # Import task
    task_spec = importlib.util.spec_from_file_location("task", os.path.join(models_dir, "task.py"))
    task_module = importlib.util.module_from_spec(task_spec)
    task_spec.loader.exec_module(task_module)
    Task = task_module.Task

    # Import task_list
    task_list_spec = importlib.util.spec_from_file_location("task_list", os.path.join(models_dir, "task_list.py"))
    task_list_module = importlib.util.module_from_spec(task_list_spec)
    task_list_spec.loader.exec_module(task_list_module)
    TaskList = task_list_module.TaskList

    # Import exceptions
    exceptions_spec = importlib.util.spec_from_file_location("exceptions", os.path.join(models_dir, "exceptions.py"))
    exceptions_module = importlib.util.module_from_spec(exceptions_spec)
    exceptions_spec.loader.exec_module(exceptions_module)
    TaskNotFoundError = exceptions_module.TaskNotFoundError
    InvalidTaskDescriptionError = exceptions_module.InvalidTaskDescriptionError


class TodoLogic:
    """
    Implements the core business logic for task management operations.

    This class provides functions for adding, retrieving, updating, and deleting tasks
    with proper validation and error handling.
    """

    def __init__(self):
        """Initialize the TodoLogic with an empty TaskList."""
        self.task_list = TaskList()

    def add_task(self, description: str) -> Task:
        """
        Add a new task to the TaskList with validation.

        Args:
            description: The description of the task to add

        Returns:
            The newly created Task object

        Raises:
            InvalidTaskDescriptionError: If the description is invalid
        """
        try:
            # The TaskList.add_task method already handles validation
            return self.task_list.add_task(description)
        except ValueError as e:
            # Convert ValueError to our custom exception
            raise InvalidTaskDescriptionError(str(e)) from e

    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Retrieve a task by its ID.

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            The Task object if found, None otherwise
        """
        return self.task_list.get_task(task_id)

    def update_task(self, task_id: int, description: str = None, completed: bool = None) -> Optional[Task]:
        """
        Update a task's properties with validation.

        Args:
            task_id: The ID of the task to update
            description: New description for the task (optional)
            completed: New completion status for the task (optional)

        Returns:
            The updated Task object if found, None otherwise
        """
        # Check if task exists before attempting update
        task = self.task_list.get_task(task_id)
        if task is None:
            return None

        try:
            # Apply validation if description is being updated
            if description is not None:
                # Add validation for very long task descriptions (T045)
                if len(description) > 500:
                    raise InvalidTaskDescriptionError(f"Description must be less than 500 characters, got {len(description)}")

                # Implement validation for empty task descriptions (T046)
                if len(description.strip()) == 0:
                    raise InvalidTaskDescriptionError("Description must be non-empty (1+ characters)")

            return self.task_list.update_task(task_id, description, completed)
        except ValueError as e:
            # Handle validation errors during update
            raise InvalidTaskDescriptionError(str(e)) from e

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by its ID.

        Args:
            task_id: The ID of the task to delete

        Returns:
            True if the task was found and deleted, False otherwise
        """
        return self.task_list.delete_task(task_id)

    def list_all_tasks(self) -> List[Task]:
        """
        Get a list of all tasks.

        Returns:
            List of all Task objects sorted by ID
        """
        return self.task_list.list_all_tasks()

    def mark_complete(self, task_id: int) -> Optional[Task]:
        """
        Mark a task as complete.

        Args:
            task_id: The ID of the task to mark as complete

        Returns:
            The updated Task object if found, None otherwise
        """
        return self.task_list.mark_complete(task_id)

    def mark_incomplete(self, task_id: int) -> Optional[Task]:
        """
        Mark a task as incomplete.

        Args:
            task_id: The ID of the task to mark as incomplete

        Returns:
            The updated Task object if found, None otherwise
        """
        return self.task_list.mark_incomplete(task_id)

    def get_completed_tasks(self) -> List[Task]:
        """
        Get a list of all completed tasks.

        Returns:
            List of completed Task objects
        """
        return self.task_list.get_completed_tasks()

    def get_pending_tasks(self) -> List[Task]:
        """
        Get a list of all pending tasks.

        Returns:
            List of pending Task objects
        """
        return self.task_list.get_pending_tasks()


# Singleton instance if needed elsewhere
# todo_logic = TodoLogic()