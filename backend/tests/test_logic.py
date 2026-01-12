"""
Unit tests for the Todo Logic layer.

This module tests the core business logic functions in todo_logic.py.
"""
import pytest
from backend.src.todo_logic import TodoLogic
from backend.src.models.task import Task
from backend.src.models.exceptions import InvalidTaskDescriptionError


class TestTodoLogic:
    """Test suite for TodoLogic class."""

    def setup_method(self):
        """Set up a fresh TodoLogic instance for each test."""
        self.logic = TodoLogic()

    def test_add_task_success(self):
        """Test adding a valid task."""
        description = "Test task description"
        task = self.logic.add_task(description)

        assert task is not None
        assert task.id == 1
        assert task.description == description
        assert task.completed is False

    def test_add_task_empty_description_fails(self):
        """Test that adding a task with empty description raises an exception."""
        with pytest.raises(InvalidTaskDescriptionError):
            self.logic.add_task("")

        with pytest.raises(InvalidTaskDescriptionError):
            self.logic.add_task("   ")

    def test_add_task_long_description_fails(self):
        """Test that adding a task with very long description raises an exception."""
        long_desc = "x" * 501  # More than 500 characters
        with pytest.raises(InvalidTaskDescriptionError):
            self.logic.add_task(long_desc)

    def test_get_task_existing(self):
        """Test retrieving an existing task."""
        task = self.logic.add_task("Test task")
        retrieved_task = self.logic.get_task(task.id)

        assert retrieved_task is not None
        assert retrieved_task.id == task.id
        assert retrieved_task.description == task.description

    def test_get_task_nonexistent(self):
        """Test retrieving a non-existent task returns None."""
        result = self.logic.get_task(999)

        assert result is None

    def test_update_task_description(self):
        """Test updating a task's description."""
        task = self.logic.add_task("Original task")
        new_description = "Updated task description"

        updated_task = self.logic.update_task(task.id, description=new_description)

        assert updated_task is not None
        assert updated_task.description == new_description
        assert updated_task.id == task.id  # ID should remain unchanged

    def test_update_task_completion_status(self):
        """Test updating a task's completion status."""
        task = self.logic.add_task("Test task")

        # Initially not completed
        assert task.completed is False

        # Mark as complete
        updated_task = self.logic.update_task(task.id, completed=True)

        assert updated_task is not None
        assert updated_task.completed is True

    def test_update_task_both_fields(self):
        """Test updating both description and completion status."""
        task = self.logic.add_task("Original task")

        updated_task = self.logic.update_task(
            task.id,
            description="Updated description",
            completed=True
        )

        assert updated_task is not None
        assert updated_task.description == "Updated description"
        assert updated_task.completed is True

    def test_update_task_nonexistent(self):
        """Test updating a non-existent task returns None."""
        result = self.logic.update_task(999, description="New description")

        assert result is None

    def test_update_task_invalid_description_fails(self):
        """Test that updating with invalid description raises an exception."""
        task = self.logic.add_task("Test task")

        with pytest.raises(InvalidTaskDescriptionError):
            self.logic.update_task(task.id, description="")

        with pytest.raises(InvalidTaskDescriptionError):
            self.logic.update_task(task.id, description="x" * 501)

    def test_delete_task_existing(self):
        """Test deleting an existing task."""
        task = self.logic.add_task("Test task")
        success = self.logic.delete_task(task.id)

        assert success is True

        # Verify the task no longer exists
        retrieved_task = self.logic.get_task(task.id)
        assert retrieved_task is None

    def test_delete_task_nonexistent(self):
        """Test deleting a non-existent task returns False."""
        success = self.logic.delete_task(999)

        assert success is False

    def test_list_all_tasks_empty(self):
        """Test listing all tasks when there are no tasks."""
        tasks = self.logic.list_all_tasks()

        assert len(tasks) == 0

    def test_list_all_tasks_multiple(self):
        """Test listing all tasks with multiple tasks."""
        task1 = self.logic.add_task("Task 1")
        task2 = self.logic.add_task("Task 2")
        task3 = self.logic.add_task("Task 3")

        tasks = self.logic.list_all_tasks()

        assert len(tasks) == 3
        # Tasks should be sorted by ID
        assert tasks[0].id == task1.id
        assert tasks[1].id == task2.id
        assert tasks[2].id == task3.id

    def test_mark_complete_existing_task(self):
        """Test marking an existing task as complete."""
        task = self.logic.add_task("Test task")
        assert task.completed is False

        marked_task = self.logic.mark_complete(task.id)

        assert marked_task is not None
        assert marked_task.completed is True

    def test_mark_complete_nonexistent_task(self):
        """Test marking a non-existent task as complete."""
        result = self.logic.mark_complete(999)

        assert result is None

    def test_mark_incomplete_existing_task(self):
        """Test marking an existing task as incomplete."""
        task = self.logic.add_task("Test task")
        # First mark as complete
        self.logic.mark_complete(task.id)

        marked_task = self.logic.mark_incomplete(task.id)

        assert marked_task is not None
        assert marked_task.completed is False

    def test_mark_incomplete_nonexistent_task(self):
        """Test marking a non-existent task as incomplete."""
        result = self.logic.mark_incomplete(999)

        assert result is None

    def test_get_completed_tasks(self):
        """Test getting only completed tasks."""
        task1 = self.logic.add_task("Completed task 1")
        task2 = self.logic.add_task("Completed task 2")
        task3 = self.logic.add_task("Pending task")

        # Mark first two as complete
        self.logic.mark_complete(task1.id)
        self.logic.mark_complete(task2.id)

        completed_tasks = self.logic.get_completed_tasks()

        assert len(completed_tasks) == 2
        completed_ids = {task.id for task in completed_tasks}
        assert task1.id in completed_ids
        assert task2.id in completed_ids
        assert task3.id not in completed_ids

    def test_get_pending_tasks(self):
        """Test getting only pending tasks."""
        task1 = self.logic.add_task("Completed task")
        task2 = self.logic.add_task("Pending task 1")
        task3 = self.logic.add_task("Pending task 2")

        # Mark first as complete
        self.logic.mark_complete(task1.id)

        pending_tasks = self.logic.get_pending_tasks()

        assert len(pending_tasks) == 2
        pending_ids = {task.id for task in pending_tasks}
        assert task1.id not in pending_ids
        assert task2.id in pending_ids
        assert task3.id in pending_ids

    def test_data_integrity_after_operations(self):
        """Test that data remains consistent after various operations."""
        # Add multiple tasks
        task1 = self.logic.add_task("Task 1")
        task2 = self.logic.add_task("Task 2")
        task3 = self.logic.add_task("Task 3")

        # Update one task
        self.logic.update_task(task2.id, description="Updated Task 2", completed=True)

        # Delete one task
        self.logic.delete_task(task1.id)

        # Verify remaining tasks
        remaining_tasks = self.logic.list_all_tasks()
        assert len(remaining_tasks) == 2

        # Verify task2 was updated correctly
        updated_task2 = self.logic.get_task(task2.id)
        assert updated_task2 is not None
        assert updated_task2.description == "Updated Task 2"
        assert updated_task2.completed is True

        # Verify task1 is gone
        assert self.logic.get_task(task1.id) is None

    def test_auto_increment_id_generation(self):
        """Test that IDs are generated sequentially."""
        task1 = self.logic.add_task("Task 1")
        task2 = self.logic.add_task("Task 2")
        task3 = self.logic.add_task("Task 3")

        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3

    def test_edge_case_very_long_description(self):
        """Test handling of very long descriptions (edge case)."""
        # Test maximum allowed length (499 chars should work)
        max_length_desc = "x" * 499
        task = self.logic.add_task(max_length_desc)
        assert task.description == max_length_desc

        # Test at the limit (500 chars should fail)
        with pytest.raises(InvalidTaskDescriptionError):
            self.logic.add_task("x" * 500)

        # Test exceeding maximum length
        with pytest.raises(InvalidTaskDescriptionError):
            self.logic.add_task("x" * 501)

    def test_edge_case_special_characters(self):
        """Test handling of special characters in descriptions."""
        special_desc = "Task with special chars: !@#$%^&*()_+-=[]{}|;:,.<>?"
        task = self.logic.add_task(special_desc)
        assert task.description == special_desc