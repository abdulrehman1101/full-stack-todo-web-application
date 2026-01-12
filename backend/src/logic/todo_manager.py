"""
Todo Manager for Todo Application

This module implements the core business logic for task management.
"""
from typing import List, Optional
from ..models.task_list import TaskList
from ..models.task import Task


class TodoManager:
    """
    Manages todo tasks using the TaskList collection.

    This class provides an interface for all task management operations.
    """

    def __init__(self):
        """Initialize the TodoManager with an empty TaskList."""
        self.task_list = TaskList()

    def add_task(self, description: str) -> Task:
        """
        Add a new task with the given description.

        Args:
            description: The description of the task to add

        Returns:
            The newly created Task object
        """
        return self.task_list.add_task(description)

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
        Update a task's properties.

        Args:
            task_id: The ID of the task to update
            description: New description for the task (optional)
            completed: New completion status for the task (optional)

        Returns:
            The updated Task object if found, None otherwise
        """
        return self.task_list.update_task(task_id, description, completed)

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

    def get_next_task_id(self) -> int:
        """
        Get the next available task ID.

        Returns:
            The next ID that will be assigned to a new task
        """
        return self.task_list.get_next_id()