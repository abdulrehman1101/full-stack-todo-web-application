"""
TaskList Model for Todo Application

This module defines the TaskList collection that manages tasks in memory.
"""
import os
import sys
from typing import Dict, List, Optional

# Handle imports for both direct execution and module execution
try:
    from .task import Task, validate_task_description
except ImportError:
    # When run as a script, need to handle imports differently
    import importlib.util

    # Import using absolute paths
    task_spec = importlib.util.spec_from_file_location("task", os.path.join(os.path.dirname(__file__), "task.py"))
    task_module = importlib.util.module_from_spec(task_spec)
    task_spec.loader.exec_module(task_module)
    Task = task_module.Task
    validate_task_description = task_module.validate_task_description


class TaskList:
    """
    Collection of Task entities managed in memory during application runtime.

    Attributes:
        tasks: Dictionary mapping task IDs to Task objects
        next_id: Integer representing the next available ID for auto-generation
    """

    def __init__(self):
        """Initialize an empty TaskList with starting ID counter."""
        self.tasks: Dict[int, Task] = {}
        self.next_id: int = 1

    def add_task(self, description: str) -> Task:
        """
        Creates new task and adds to collection.

        Args:
            description: The task description

        Returns:
            The newly created Task object

        Raises:
            ValueError: If the description is invalid
        """
        # Validate the description before creating the task
        validate_task_description(description)

        # Create a new task with the next available ID
        task = Task(id=self.next_id, description=description, completed=False)

        # Add the task to the collection
        self.tasks[self.next_id] = task

        # Increment the ID counter for the next task
        self.next_id += 1

        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Retrieves task by ID.

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            The Task object if found, None otherwise
        """
        return self.tasks.get(task_id)

    def update_task(self, task_id: int, description: str = None, completed: bool = None) -> Optional[Task]:
        """
        Updates task properties.

        Args:
            task_id: The ID of the task to update
            description: New description (optional)
            completed: New completion status (optional)

        Returns:
            The updated Task object if found, None otherwise
        """
        task = self.get_task(task_id)
        if task is None:
            return None

        # Update description if provided
        if description is not None:
            validate_task_description(description)
            task.description = description

        # Update completion status if provided
        if completed is not None:
            if not isinstance(completed, bool):
                raise ValueError(f"Completed status must be a boolean, got {type(completed)}")
            task.completed = completed

        return task

    def delete_task(self, task_id: int) -> bool:
        """
        Removes task from collection.

        Args:
            task_id: The ID of the task to delete

        Returns:
            True if the task was found and deleted, False otherwise
        """
        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False

    def list_all_tasks(self) -> List[Task]:
        """
        Returns all tasks sorted by ID.

        Returns:
            List of all Task objects sorted by ID
        """
        return sorted(self.tasks.values(), key=lambda x: x.id)

    def mark_complete(self, task_id: int) -> Optional[Task]:
        """
        Marks task as completed.

        Args:
            task_id: The ID of the task to mark as complete

        Returns:
            The updated Task object if found, None otherwise
        """
        task = self.get_task(task_id)
        if task:
            task.mark_complete()
            return task
        return None

    def mark_incomplete(self, task_id: int) -> Optional[Task]:
        """
        Marks task as incomplete.

        Args:
            task_id: The ID of the task to mark as incomplete

        Returns:
            The updated Task object if found, None otherwise
        """
        task = self.get_task(task_id)
        if task:
            task.mark_incomplete()
            return task
        return None

    def get_completed_tasks(self) -> List[Task]:
        """
        Returns only completed tasks.

        Returns:
            List of completed Task objects
        """
        return [task for task in self.tasks.values() if task.completed]

    def get_pending_tasks(self) -> List[Task]:
        """
        Returns only pending tasks.

        Returns:
            List of pending Task objects
        """
        return [task for task in self.tasks.values() if not task.completed]

    def get_next_id(self) -> int:
        """
        Returns the next available ID.

        Returns:
            The next ID that will be assigned to a new task
        """
        return self.next_id