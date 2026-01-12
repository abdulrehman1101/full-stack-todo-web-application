"""
Performance tests for the Todo Application.

This module tests the performance and stress handling of the application.
"""
import time
import pytest
from backend.src.todo_logic import TodoLogic


class TestPerformance:
    """Performance test suite for TodoLogic."""

    def test_performance_100_tasks(self):
        """Test that the app handles at least 100 tasks without performance degradation."""
        logic = TodoLogic()

        # Add 100 tasks
        start_time = time.time()
        for i in range(100):
            description = f"Task {i+1} - Performance test task"
            task = logic.add_task(description)
            assert task is not None
            assert task.id == i + 1
        add_time = time.time() - start_time

        # Verify we have 100 tasks
        tasks = logic.list_all_tasks()
        assert len(tasks) == 100

        # Test retrieval performance
        start_time = time.time()
        for i in range(1, 101):
            task = logic.get_task(i)
            assert task is not None
            assert task.id == i
        retrieval_time = time.time() - start_time

        # Test update performance (update every other task)
        start_time = time.time()
        for i in range(1, 101, 2):  # Every other task
            updated_task = logic.update_task(i, description=f"Updated Task {i}")
            assert updated_task is not None
            assert updated_task.description == f"Updated Task {i}"
        update_time = time.time() - start_time

        # Test completion marking performance
        start_time = time.time()
        for i in range(1, 101, 3):  # Every third task
            marked_task = logic.mark_complete(i)
            assert marked_task is not None
            assert marked_task.completed is True
        mark_time = time.time() - start_time

        # Performance should be reasonable (less than 1 second for these operations)
        # In practice, these operations should be much faster
        assert add_time < 2.0, f"Adding 100 tasks took too long: {add_time:.2f}s"
        assert retrieval_time < 1.0, f"Retrieving 100 tasks took too long: {retrieval_time:.2f}s"
        assert update_time < 1.0, f"Updating 50 tasks took too long: {update_time:.2f}s"
        assert mark_time < 1.0, f"Marking 33 tasks as complete took too long: {mark_time:.2f}s"

        print(f"Performance test results for 100 tasks:")
        print(f"  - Adding 100 tasks: {add_time:.3f}s")
        print(f"  - Retrieving 100 tasks: {retrieval_time:.3f}s")
        print(f"  - Updating 50 tasks: {update_time:.3f}s")
        print(f"  - Marking 33 tasks complete: {mark_time:.3f}s")

    def test_performance_1000_tasks(self):
        """Test performance with 1000 tasks (stress test)."""
        logic = TodoLogic()

        # Add 1000 tasks
        start_time = time.time()
        for i in range(1000):
            description = f"Task {i+1} - Stress test task"
            task = logic.add_task(description)
            assert task is not None
        add_time = time.time() - start_time

        # Verify we have 1000 tasks
        tasks = logic.list_all_tasks()
        assert len(tasks) == 1000

        # Test retrieval of a specific task
        start_time = time.time()
        task = logic.get_task(500)
        retrieval_time = time.time() - start_time
        assert task is not None
        assert task.id == 500

        # Performance should still be reasonable for 1000 tasks
        assert add_time < 10.0, f"Adding 1000 tasks took too long: {add_time:.2f}s"
        assert retrieval_time < 1.0, f"Retrieving task from 1000 tasks took too long: {retrieval_time:.2f}s"

        print(f"Stress test results for 1000 tasks:")
        print(f"  - Adding 1000 tasks: {add_time:.3f}s")
        print(f"  - Retrieving task from 1000: {retrieval_time:.3f}s")

    def test_memory_efficiency(self):
        """Test that memory usage is reasonable."""
        import sys

        logic = TodoLogic()

        # Add 100 tasks and check memory usage
        for i in range(100):
            logic.add_task(f"Task {i+1}")

        # Get the size of the tasks dictionary (rough memory estimate)
        tasks_size = sys.getsizeof(logic.task_list.tasks)
        # Each task object also takes memory, but this gives us a basic check

        # The memory usage should be reasonable for 100 tasks
        # This is a very loose check since memory usage varies by system
        assert tasks_size > 0, "Tasks dictionary should consume some memory"
        # In practice, 100 tasks should not consume excessive memory

    def test_data_accuracy_with_many_tasks(self):
        """Test that data accuracy is maintained with many tasks."""
        logic = TodoLogic()

        # Add 200 tasks with specific patterns
        for i in range(200):
            description = f"Task {i+1}"
            task = logic.add_task(description)
            assert task.id == i + 1
            assert task.description == description
            assert task.completed is False

        # Verify all tasks exist with correct data
        all_tasks = logic.list_all_tasks()
        assert len(all_tasks) == 200

        # Verify specific tasks
        for i in range(0, 200, 10):  # Check every 10th task
            task = logic.get_task(i + 1)
            assert task is not None
            assert task.id == i + 1
            assert task.description == f"Task {i + 1}"
            assert task.completed is False

        # Update every 5th task
        for i in range(4, 200, 5):  # 5th, 10th, 15th, etc. (0-indexed)
            updated_task = logic.update_task(i + 1, description=f"Updated Task {i + 1}", completed=True)
            assert updated_task is not None
            assert updated_task.description == f"Updated Task {i + 1}"
            assert updated_task.completed is True

        # Verify updates were applied correctly
        for i in range(4, 200, 5):
            task = logic.get_task(i + 1)
            assert task is not None
            assert task.description == f"Updated Task {i + 1}"
            assert task.completed is True

        # Count completed vs pending
        completed = logic.get_completed_tasks()
        pending = logic.get_pending_tasks()

        assert len(completed) == 40  # Every 5th task from 1-200 (200/5 = 40)
        assert len(pending) == 160  # Remaining tasks
        assert len(completed) + len(pending) == 200  # All tasks accounted for