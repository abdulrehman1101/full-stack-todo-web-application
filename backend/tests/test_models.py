"""
Unit tests for the Todo Models layer.

This module tests the Task and TaskList models.
"""
import pytest
from datetime import datetime
from backend.src.models.task import Task, validate_task_description
from backend.src.models.task_list import TaskList
from backend.src.models.exceptions import InvalidTaskDescriptionError, TaskNotFoundError


class TestTask:
    """Test suite for Task class."""

    def test_task_creation_valid(self):
        """Test creating a valid Task instance."""
        task = Task(id=1, description="Test description")

        assert task.id == 1
        assert task.description == "Test description"
        assert task.completed is False
        assert isinstance(task.created_at, datetime)

    def test_task_creation_with_completion_status(self):
        """Test creating a Task with specific completion status."""
        task = Task(id=1, description="Test description", completed=True)

        assert task.id == 1
        assert task.description == "Test description"
        assert task.completed is True

    def test_task_creation_with_custom_datetime(self):
        """Test creating a Task with custom creation datetime."""
        custom_time = datetime(2023, 1, 1, 12, 0, 0)
        task = Task(id=1, description="Test description", created_at=custom_time)

        assert task.id == 1
        assert task.description == "Test description"
        assert task.created_at == custom_time

    def test_task_id_positive_integer(self):
        """Test that Task validates positive integer IDs."""
        # Valid positive ID
        task = Task(id=1, description="Test description")
        assert task.id == 1

        # Invalid IDs should raise ValueError
        with pytest.raises(ValueError):
            Task(id=0, description="Test description")

        with pytest.raises(ValueError):
            Task(id=-1, description="Test description")

        with pytest.raises(ValueError):
            Task(id="invalid", description="Test description")

    def test_task_description_validation_non_empty(self):
        """Test that Task validates non-empty descriptions."""
        # Valid description
        task = Task(id=1, description="Valid description")
        assert task.description == "Valid description"

        # Empty description should raise ValueError
        with pytest.raises(ValueError):
            Task(id=1, description="")

        # Whitespace-only description should raise ValueError
        with pytest.raises(ValueError):
            Task(id=1, description="   ")

    def test_task_description_length_limit(self):
        """Test that Task validates description length."""
        # Valid length description
        valid_desc = "x" * 499  # 499 chars, under 500 limit
        task = Task(id=1, description=valid_desc)
        assert task.description == valid_desc

        # Description at the limit (500 chars) should raise ValueError
        with pytest.raises(ValueError):
            Task(id=1, description="x" * 500)

    def test_task_completion_status_validation(self):
        """Test that Task validates completion status as boolean."""
        # Valid boolean values
        task1 = Task(id=1, description="Test", completed=True)
        assert task1.completed is True

        task2 = Task(id=2, description="Test", completed=False)
        assert task2.completed is False

        # Invalid completion status should raise ValueError
        with pytest.raises(ValueError):
            Task(id=1, description="Test", completed="invalid")

        with pytest.raises(ValueError):
            Task(id=1, description="Test", completed=1)

        with pytest.raises(ValueError):
            Task(id=1, description="Test", completed=0)

    def test_task_mark_complete(self):
        """Test marking a task as complete."""
        task = Task(id=1, description="Test description")
        assert task.completed is False

        task.mark_complete()
        assert task.completed is True

    def test_task_mark_incomplete(self):
        """Test marking a task as incomplete."""
        task = Task(id=1, description="Test description", completed=True)
        assert task.completed is True

        task.mark_incomplete()
        assert task.completed is False

    def test_validate_task_description_function(self):
        """Test the standalone validate_task_description function."""
        # Valid descriptions should return True
        assert validate_task_description("Valid description") is True
        assert validate_task_description("x" * 499) is True

        # Invalid descriptions should raise ValueError
        with pytest.raises(ValueError):
            validate_task_description("")

        with pytest.raises(ValueError):
            validate_task_description("   ")

        with pytest.raises(ValueError):
            validate_task_description("x" * 500)


class TestTaskList:
    """Test suite for TaskList class."""

    def setup_method(self):
        """Set up a fresh TaskList instance for each test."""
        self.task_list = TaskList()

    def test_initial_state(self):
        """Test the initial state of a TaskList."""
        assert len(self.task_list.tasks) == 0
        assert self.task_list.next_id == 1

    def test_add_task_success(self):
        """Test adding a task to the TaskList."""
        task = self.task_list.add_task("Test description")

        assert task is not None
        assert task.id == 1
        assert task.description == "Test description"
        assert task.completed is False
        assert len(self.task_list.tasks) == 1
        assert 1 in self.task_list.tasks

    def test_add_task_auto_increment_id(self):
        """Test that IDs are auto-incremented."""
        task1 = self.task_list.add_task("Task 1")
        task2 = self.task_list.add_task("Task 2")
        task3 = self.task_list.add_task("Task 3")

        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3
        assert self.task_list.next_id == 4

    def test_add_task_validation(self):
        """Test that adding a task validates the description."""
        # Valid task
        task = self.task_list.add_task("Valid description")
        assert task is not None

        # Invalid descriptions should raise ValueError
        with pytest.raises(ValueError):
            self.task_list.add_task("")

        with pytest.raises(ValueError):
            self.task_list.add_task("   ")

        with pytest.raises(ValueError):
            self.task_list.add_task("x" * 500)

    def test_get_task_existing(self):
        """Test retrieving an existing task."""
        task = self.task_list.add_task("Test task")
        retrieved_task = self.task_list.get_task(task.id)

        assert retrieved_task is not None
        assert retrieved_task.id == task.id
        assert retrieved_task.description == task.description

    def test_get_task_nonexistent(self):
        """Test retrieving a non-existent task."""
        result = self.task_list.get_task(999)

        assert result is None

    def test_update_task_description(self):
        """Test updating a task's description."""
        task = self.task_list.add_task("Original description")
        new_description = "Updated description"

        updated_task = self.task_list.update_task(task.id, description=new_description)

        assert updated_task is not None
        assert updated_task.description == new_description
        assert updated_task.id == task.id

    def test_update_task_completion_status(self):
        """Test updating a task's completion status."""
        task = self.task_list.add_task("Test task")

        # Initially not completed
        assert task.completed is False

        # Mark as complete
        updated_task = self.task_list.update_task(task.id, completed=True)

        assert updated_task is not None
        assert updated_task.completed is True

    def test_update_task_both_fields(self):
        """Test updating both description and completion status."""
        task = self.task_list.add_task("Original task")

        updated_task = self.task_list.update_task(
            task.id,
            description="Updated description",
            completed=True
        )

        assert updated_task is not None
        assert updated_task.description == "Updated description"
        assert updated_task.completed is True

    def test_update_task_nonexistent(self):
        """Test updating a non-existent task."""
        result = self.task_list.update_task(999, description="New description")

        assert result is None

    def test_update_task_invalid_description(self):
        """Test updating with invalid description."""
        task = self.task_list.add_task("Test task")

        # Updating with empty description should fail
        with pytest.raises(ValueError):
            self.task_list.update_task(task.id, description="")

        # Updating with too-long description should fail
        with pytest.raises(ValueError):
            self.task_list.update_task(task.id, description="x" * 500)

    def test_delete_task_existing(self):
        """Test deleting an existing task."""
        task = self.task_list.add_task("Test task")
        success = self.task_list.delete_task(task.id)

        assert success is True
        assert len(self.task_list.tasks) == 0
        assert task.id not in self.task_list.tasks

    def test_delete_task_nonexistent(self):
        """Test deleting a non-existent task."""
        success = self.task_list.delete_task(999)

        assert success is False

    def test_list_all_tasks_empty(self):
        """Test listing all tasks when empty."""
        tasks = self.task_list.list_all_tasks()

        assert len(tasks) == 0

    def test_list_all_tasks_multiple(self):
        """Test listing all tasks with multiple tasks."""
        task1 = self.task_list.add_task("Task 1")
        task2 = self.task_list.add_task("Task 2")
        task3 = self.task_list.add_task("Task 3")

        tasks = self.task_list.list_all_tasks()

        # Should be sorted by ID
        assert len(tasks) == 3
        assert tasks[0].id == task1.id
        assert tasks[1].id == task2.id
        assert tasks[2].id == task3.id

    def test_mark_complete_existing_task(self):
        """Test marking an existing task as complete."""
        task = self.task_list.add_task("Test task")
        assert task.completed is False

        marked_task = self.task_list.mark_complete(task.id)

        assert marked_task is not None
        assert marked_task.completed is True

    def test_mark_complete_nonexistent_task(self):
        """Test marking a non-existent task as complete."""
        result = self.task_list.mark_complete(999)

        assert result is None

    def test_mark_incomplete_existing_task(self):
        """Test marking an existing task as incomplete."""
        task = self.task_list.add_task("Test task")
        # First mark as complete
        self.task_list.mark_complete(task.id)

        marked_task = self.task_list.mark_incomplete(task.id)

        assert marked_task is not None
        assert marked_task.completed is False

    def test_mark_incomplete_nonexistent_task(self):
        """Test marking a non-existent task as incomplete."""
        result = self.task_list.mark_incomplete(999)

        assert result is None

    def test_get_completed_tasks(self):
        """Test getting only completed tasks."""
        task1 = self.task_list.add_task("Completed task 1")
        task2 = self.task_list.add_task("Completed task 2")
        task3 = self.task_list.add_task("Pending task")

        # Mark first two as complete
        self.task_list.mark_complete(task1.id)
        self.task_list.mark_complete(task2.id)

        completed_tasks = self.task_list.get_completed_tasks()

        assert len(completed_tasks) == 2
        completed_ids = {task.id for task in completed_tasks}
        assert task1.id in completed_ids
        assert task2.id in completed_ids
        assert task3.id not in completed_ids

    def test_get_pending_tasks(self):
        """Test getting only pending tasks."""
        task1 = self.task_list.add_task("Completed task")
        task2 = self.task_list.add_task("Pending task 1")
        task3 = self.task_list.add_task("Pending task 2")

        # Mark first as complete
        self.task_list.mark_complete(task1.id)

        pending_tasks = self.task_list.get_pending_tasks()

        assert len(pending_tasks) == 2
        pending_ids = {task.id for task in pending_tasks}
        assert task1.id not in pending_ids
        assert task2.id in pending_ids
        assert task3.id in pending_ids

    def test_get_next_id(self):
        """Test getting the next available ID."""
        assert self.task_list.get_next_id() == 1

        self.task_list.add_task("Task 1")
        assert self.task_list.get_next_id() == 2

        self.task_list.add_task("Task 2")
        assert self.task_list.get_next_id() == 3

    def test_data_integrity_after_operations(self):
        """Test that data remains consistent after various operations."""
        # Add multiple tasks
        task1 = self.task_list.add_task("Task 1")
        task2 = self.task_list.add_task("Task 2")
        task3 = self.task_list.add_task("Task 3")

        # Update one task
        self.task_list.update_task(task2.id, description="Updated Task 2", completed=True)

        # Delete one task
        self.task_list.delete_task(task1.id)

        # Verify remaining tasks
        remaining_tasks = self.task_list.list_all_tasks()
        assert len(remaining_tasks) == 2

        # Verify task2 was updated correctly
        updated_task2 = self.task_list.get_task(task2.id)
        assert updated_task2 is not None
        assert updated_task2.description == "Updated Task 2"
        assert updated_task2.completed is True

        # Verify task1 is gone
        assert self.task_list.get_task(task1.id) is None

    def test_edge_case_very_long_description(self):
        """Test handling of very long descriptions (edge case)."""
        # Test maximum allowed length
        max_length_desc = "x" * 499
        task = self.task_list.add_task(max_length_desc)
        assert task.description == max_length_desc

        # Test exceeding maximum length
        with pytest.raises(ValueError):
            self.task_list.add_task("x" * 500)

    def test_edge_case_special_characters(self):
        """Test handling of special characters in descriptions."""
        special_desc = "Task with special chars: !@#$%^&*()_+-=[]{}|;:,.<>?"
        task = self.task_list.add_task(special_desc)
        assert task.description == special_desc