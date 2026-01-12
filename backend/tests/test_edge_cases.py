"""
Edge case tests for the Todo Application.

This module tests edge cases and error handling scenarios.
"""
import pytest
from backend.src.todo_logic import TodoLogic
from backend.src.models.exceptions import InvalidTaskDescriptionError


class TestEdgeCases:
    """Edge case test suite for TodoLogic."""

    def setup_method(self):
        """Set up a fresh TodoLogic instance for each test."""
        self.logic = TodoLogic()

    def test_empty_string_description(self):
        """Test adding task with empty string description."""
        with pytest.raises(InvalidTaskDescriptionError):
            self.logic.add_task("")

    def test_whitespace_only_description(self):
        """Test adding task with whitespace-only description."""
        with pytest.raises(InvalidTaskDescriptionError):
            self.logic.add_task("   ")

        with pytest.raises(InvalidTaskDescriptionError):
            self.logic.add_task("\t\n  \r  ")

    def test_very_long_description(self):
        """Test adding task with very long description."""
        # Test at the limit (499 chars should work)
        long_desc = "x" * 499
        task = self.logic.add_task(long_desc)
        assert task.description == long_desc

        # Test exceeding the limit (500 chars should fail)
        with pytest.raises(InvalidTaskDescriptionError):
            self.logic.add_task("x" * 500)

        # Test much longer description
        with pytest.raises(InvalidTaskDescriptionError):
            self.logic.add_task("x" * 1000)

    def test_update_with_empty_description(self):
        """Test updating task with empty description."""
        task = self.logic.add_task("Original description")

        with pytest.raises(InvalidTaskDescriptionError):
            self.logic.update_task(task.id, description="")

        with pytest.raises(InvalidTaskDescriptionError):
            self.logic.update_task(task.id, description="   ")

    def test_update_with_very_long_description(self):
        """Test updating task with very long description."""
        task = self.logic.add_task("Original description")

        with pytest.raises(InvalidTaskDescriptionError):
            self.logic.update_task(task.id, description="x" * 500)

    def test_get_nonexistent_task(self):
        """Test getting a task that doesn't exist."""
        result = self.logic.get_task(999)
        assert result is None

        # Test with negative ID
        result = self.logic.get_task(-1)
        assert result is None

        # Test with zero ID
        result = self.logic.get_task(0)
        assert result is None

    def test_update_nonexistent_task(self):
        """Test updating a task that doesn't exist."""
        result = self.logic.update_task(999, description="New description")
        assert result is None

        result = self.logic.update_task(999, completed=True)
        assert result is None

        result = self.logic.update_task(999, description="New", completed=True)
        assert result is None

    def test_delete_nonexistent_task(self):
        """Test deleting a task that doesn't exist."""
        result = self.logic.delete_task(999)
        assert result is False

        result = self.logic.delete_task(-1)
        assert result is False

        result = self.logic.delete_task(0)
        assert result is False

    def test_mark_complete_nonexistent_task(self):
        """Test marking complete a task that doesn't exist."""
        result = self.logic.mark_complete(999)
        assert result is None

        result = self.logic.mark_complete(-1)
        assert result is None

        result = self.logic.mark_complete(0)
        assert result is None

    def test_mark_incomplete_nonexistent_task(self):
        """Test marking incomplete a task that doesn't exist."""
        result = self.logic.mark_incomplete(999)
        assert result is None

        result = self.logic.mark_incomplete(-1)
        assert result is None

        result = self.logic.mark_incomplete(0)
        assert result is None

    def test_special_characters_in_description(self):
        """Test handling of special characters in descriptions."""
        special_desc = "Task with special chars: !@#$%^&*()_+-=[]{}|;:,.<>?"
        task = self.logic.add_task(special_desc)
        assert task.description == special_desc

        unicode_desc = "Task with unicode: ñáéíóú 中文 🚀"
        task2 = self.logic.add_task(unicode_desc)
        assert task2.description == unicode_desc

        multiline_desc = "Task with\nmultiline\ndescription"
        task3 = self.logic.add_task(multiline_desc)
        assert task3.description == multiline_desc

    def test_consecutive_operations(self):
        """Test consecutive operations to ensure data integrity."""
        # Add multiple tasks quickly
        tasks = []
        for i in range(50):
            task = self.logic.add_task(f"Task {i}")
            tasks.append(task)

        # Verify all tasks exist
        all_tasks = self.logic.list_all_tasks()
        assert len(all_tasks) == 50

        # Update every other task
        for i in range(0, 50, 2):
            updated = self.logic.update_task(tasks[i].id, description=f"Updated {i}")
            assert updated is not None
            assert updated.description == f"Updated {i}"

        # Mark every third task as complete
        for i in range(0, 50, 3):
            marked = self.logic.mark_complete(tasks[i].id)
            assert marked is not None
            assert marked.completed is True

        # Delete every fifth task
        for i in range(0, 50, 5):
            deleted = self.logic.delete_task(tasks[i].id)
            assert deleted is True

        # Verify final state
        final_tasks = self.logic.list_all_tasks()
        assert len(final_tasks) == 40  # 50 - 10 deleted = 40

        completed_count = len(self.logic.get_completed_tasks())
        pending_count = len(self.logic.get_pending_tasks())
        assert completed_count + pending_count == 40

    def test_mixed_operations_with_errors(self):
        """Test operations mixed with invalid operations."""
        # Add some valid tasks
        task1 = self.logic.add_task("Valid task 1")
        task2 = self.logic.add_task("Valid task 2")

        # Try some invalid operations
        with pytest.raises(InvalidTaskDescriptionError):
            self.logic.add_task("")  # Empty description

        # These should still work after the error
        result = self.logic.get_task(task1.id)
        assert result is not None
        assert result.description == "Valid task 1"

        # Try updating with invalid description
        with pytest.raises(InvalidTaskDescriptionError):
            self.logic.update_task(task1.id, description="")  # Empty description

        # Update should still work with valid description
        updated = self.logic.update_task(task1.id, description="Updated task")
        assert updated is not None
        assert updated.description == "Updated task"

        # Try operations on non-existent task
        result = self.logic.get_task(999)
        assert result is None

        # Valid operations should still work
        task3 = self.logic.add_task("Another valid task")
        assert task3 is not None

    def test_boundary_values(self):
        """Test boundary values for task IDs and descriptions."""
        # Test with minimal description
        minimal_task = self.logic.add_task("x")
        assert minimal_task is not None
        assert minimal_task.description == "x"

        # Test with description at max length
        max_desc = "x" * 499  # Max allowed length
        max_task = self.logic.add_task(max_desc)
        assert max_task is not None
        assert max_task.description == max_desc

        # Test with max length - 1
        almost_max_desc = "x" * 498
        almost_max_task = self.logic.add_task(almost_max_desc)
        assert almost_max_task is not None
        assert almost_max_task.description == almost_max_desc

    def test_completion_state_transitions(self):
        """Test various completion state transitions."""
        task = self.logic.add_task("Test task")

        # Initially incomplete
        assert task.completed is False

        # Mark complete
        marked = self.logic.mark_complete(task.id)
        assert marked is not None
        assert marked.completed is True

        # Mark incomplete again
        marked = self.logic.mark_incomplete(task.id)
        assert marked is not None
        assert marked.completed is False

        # Mark complete again
        marked = self.logic.mark_complete(task.id)
        assert marked is not None
        assert marked.completed is True

        # Update description while keeping completion status
        updated = self.logic.update_task(task.id, description="Updated task")
        assert updated is not None
        assert updated.completed is True  # Should still be complete
        assert updated.description == "Updated task"

        # Update only completion status
        updated = self.logic.update_task(task.id, completed=False)
        assert updated is not None
        assert updated.completed is False  # Should now be incomplete
        assert updated.description == "Updated task"  # Description should remain

    def test_large_number_of_tasks_operations(self):
        """Test operations on a large number of tasks."""
        # Add 200 tasks
        for i in range(200):
            self.logic.add_task(f"Task {i+1}")

        # Verify all exist
        all_tasks = self.logic.list_all_tasks()
        assert len(all_tasks) == 200

        # Update every 10th task
        for i in range(0, 200, 10):
            updated = self.logic.update_task(i + 1, description=f"Updated {i + 1}")
            assert updated is not None

        # Mark every 5th task as complete
        for i in range(0, 200, 5):
            marked = self.logic.mark_complete(i + 1)
            assert marked is not None

        # Verify counts
        completed = self.logic.get_completed_tasks()
        pending = self.logic.get_pending_tasks()
        all_tasks = self.logic.list_all_tasks()

        assert len(all_tasks) == 200
        assert len(completed) == 40  # Every 5th task: 200/5 = 40
        assert len(pending) == 160  # Remaining: 200 - 40 = 160
        assert len(completed) + len(pending) == 200

    def test_error_handling_consistency(self):
        """Test that error handling is consistent across operations."""
        # Try operations on non-existent task - should not crash
        assert self.logic.get_task(999) is None
        assert self.logic.update_task(999, description="test") is None
        assert self.logic.delete_task(999) is False
        assert self.logic.mark_complete(999) is None
        assert self.logic.mark_incomplete(999) is None

        # Valid operations should still work after non-existent operations
        valid_task = self.logic.add_task("Valid task after non-existent ops")
        assert valid_task is not None
        assert valid_task.description == "Valid task after non-existent ops"

        # Try invalid operations - should raise appropriate exceptions
        with pytest.raises(InvalidTaskDescriptionError):
            self.logic.add_task("")  # Empty description

        # Try another invalid operation
        with pytest.raises(InvalidTaskDescriptionError):
            self.logic.add_task("x" * 500)  # Too long description

        # Valid operations should still work after validation errors
        valid_task2 = self.logic.add_task("Another valid task after errors")
        assert valid_task2 is not None
        assert valid_task2.description == "Another valid task after errors"

        # Try updating with invalid description on existing task
        with pytest.raises(InvalidTaskDescriptionError):
            self.logic.update_task(valid_task2.id, description="")  # Update with empty description

        # Valid operations should still work after update validation errors
        valid_task3 = self.logic.add_task("Yet another valid task")
        assert valid_task3 is not None
        assert valid_task3.description == "Yet another valid task"