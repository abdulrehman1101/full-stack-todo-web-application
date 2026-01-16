"""
Comprehensive test to verify user data isolation in the todo application.
This test ensures that one user cannot access another user's data.
"""

import pytest
from uuid import uuid4
from sqlmodel import Session, select
from unittest.mock import Mock
from src.database.models.user import User
from src.database.models.task import Task, TaskCreate
from src.database.crud import (
    create_task_for_user,
    get_task_by_id_for_user,
    get_tasks_for_user,
    update_task_for_user,
    delete_task_for_user
)


def test_comprehensive_data_isolation():
    """
    Comprehensive test that one user cannot access another user's data.

    This test verifies that:
    1. User A can access their own tasks
    2. User A cannot access User B's tasks
    3. Each user only sees their own tasks in their task list
    4. User A cannot update User B's tasks
    5. User A cannot delete User B's tasks
    """

    # Create mock session
    mock_session = Mock(spec=Session)

    # Create two different users
    user_a_id = uuid4()
    user_b_id = uuid4()

    # Create tasks for User A
    user_a_task_data = TaskCreate(description="User A's task", is_completed=False)
    user_a_task = Task(
        id=uuid4(),
        user_id=user_a_id,
        description="User A's task",
        is_completed=False
    )

    # Create tasks for User B
    user_b_task_data = TaskCreate(description="User B's task", is_completed=False)
    user_b_task = Task(
        id=uuid4(),
        user_id=user_b_id,
        description="User B's task",
        is_completed=False
    )

    # Mock session behavior for database operations
    def mock_exec(statement):
        mock_result = Mock()

        # Check the WHERE clauses to determine which query is being made
        where_conditions = getattr(statement, '_where_criteria', [])

        # Convert where conditions to string for easier matching
        where_str = str(where_conditions)

        # If querying for user_a_task by user_a
        if str(user_a_task.id) in where_str and str(user_a_id) in where_str:
            mock_result.first.return_value = user_a_task
            mock_result.all.return_value = [user_a_task]
        # If querying for user_b_task by user_b
        elif str(user_b_task.id) in where_str and str(user_b_id) in where_str:
            mock_result.first.return_value = user_b_task
            mock_result.all.return_value = [user_b_task]
        # If querying for user_b_task by user_a (should return None - data isolation)
        elif str(user_b_task.id) in where_str and str(user_a_id) in where_str:
            mock_result.first.return_value = None
            mock_result.all.return_value = []
        # If querying for user_a_task by user_b (should return None - data isolation)
        elif str(user_a_task.id) in where_str and str(user_b_id) in where_str:
            mock_result.first.return_value = None
            mock_result.all.return_value = []
        # If getting all tasks for user_a
        elif f"'{user_a_id}'" in where_str or str(user_a_id) in where_str:
            if "user_id" in where_str:  # Filtering by user_id
                mock_result.all.return_value = [user_a_task]
            else:
                mock_result.all.return_value = []
        # If getting all tasks for user_b
        elif f"'{user_b_id}'" in where_str or str(user_b_id) in where_str:
            if "user_id" in where_str:  # Filtering by user_id
                mock_result.all.return_value = [user_b_task]
            else:
                mock_result.all.return_value = []
        else:
            mock_result.first.return_value = None
            mock_result.all.return_value = []

        return mock_result

    mock_session.exec = Mock(side_effect=mock_exec)
    mock_session.add = Mock()
    mock_session.commit = Mock()
    mock_session.refresh = Mock()
    mock_session.get = Mock(return_value=None)  # We'll use exec for queries

    # Test 1: User A should be able to access their own task
    retrieved_task_a = get_task_by_id_for_user(
        session=mock_session,
        task_id=user_a_task.id,
        user_id=user_a_id
    )

    assert retrieved_task_a is not None, "User A should be able to access their own task"
    assert retrieved_task_a.id == user_a_task.id, "Retrieved task should match the requested task"

    # Test 2: User A should NOT be able to access User B's task
    retrieved_task_b_by_user_a = get_task_by_id_for_user(
        session=mock_session,
        task_id=user_b_task.id,
        user_id=user_a_id  # User A trying to access User B's task
    )

    assert retrieved_task_b_by_user_a is None, "User A should not be able to access User B's task"

    # Test 3: User B should be able to access their own task
    retrieved_task_b = get_task_by_id_for_user(
        session=mock_session,
        task_id=user_b_task.id,
        user_id=user_b_id
    )

    assert retrieved_task_b is not None, "User B should be able to access their own task"
    assert retrieved_task_b.id == user_b_task.id, "Retrieved task should match the requested task"

    # Test 4: User B should NOT be able to access User A's task
    retrieved_task_a_by_user_b = get_task_by_id_for_user(
        session=mock_session,
        task_id=user_a_task.id,
        user_id=user_b_id  # User B trying to access User A's task
    )

    assert retrieved_task_a_by_user_b is None, "User B should not be able to access User A's task"

    # Test 5: User A should only see their own tasks
    user_a_tasks = get_tasks_for_user(
        session=mock_session,
        user_id=user_a_id
    )

    assert len(user_a_tasks) == 1, "User A should only see their own tasks"
    assert user_a_tasks[0].id == user_a_task.id, "User A's task list should only contain their task"

    # Test 6: User B should only see their own tasks
    user_b_tasks = get_tasks_for_user(
        session=mock_session,
        user_id=user_b_id
    )

    assert len(user_b_tasks) == 1, "User B should only see their own tasks"
    assert user_b_tasks[0].id == user_b_task.id, "User B's task list should only contain their task"

    # Test 7: Attempt to update User B's task as User A (should fail)
    from src.database.models.task import TaskUpdate
    update_data = TaskUpdate(description="Updated by User A")
    update_result = update_task_for_user(
        session=mock_session,
        task_id=user_b_task.id,
        task_update=update_data,
        user_id=user_a_id  # User A trying to update User B's task
    )

    assert update_result is None, "User A should not be able to update User B's task"

    # Test 8: Attempt to delete User B's task as User A (should fail)
    delete_result = delete_task_for_user(
        session=mock_session,
        task_id=user_b_task.id,
        user_id=user_a_id  # User A trying to delete User B's task
    )

    assert delete_result is False, "User A should not be able to delete User B's task"

    print("✅ Comprehensive Data Isolation Test Passed: Users can only access, modify, and delete their own data")


if __name__ == "__main__":
    test_comprehensive_data_isolation()
    print("\n🎉 All comprehensive data isolation tests passed!")