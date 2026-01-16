from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ....database.models.task import Task
from ....database.schemas.task_schemas import TaskCreate, TaskRead, TaskUpdate
from ....auth.middleware import verify_authenticated_user
from ....database.session import get_session
from ....database.models.user import User


router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskRead)
def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(verify_authenticated_user),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the authenticated user.
    The user_id is automatically assigned from the JWT token.
    """
    # Create a new task instance with the user_id from the authenticated user
    task = Task(
        title=task_data.title,
        description=task_data.description,
        is_completed=task_data.is_completed,
        user_id=current_user.id
    )

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


@router.get("/", response_model=List[TaskRead])
def list_tasks(
    current_user: User = Depends(verify_authenticated_user),
    session: Session = Depends(get_session)
):
    """
    List all tasks for the authenticated user.
    Only returns tasks that belong to the current user.
    """
    # Query tasks filtered by the current user's ID
    statement = select(Task).where(Task.user_id == current_user.id)
    tasks = session.exec(statement).all()

    return tasks


@router.get("/{id}", response_model=TaskRead)
def get_task(
    id: UUID,
    current_user: User = Depends(verify_authenticated_user),
    session: Session = Depends(get_session)
):
    """
    Get a specific task by ID.
    Verifies that the task belongs to the current user.
    """
    # Query for the task that belongs to the current user
    statement = select(Task).where(Task.id == id).where(Task.user_id == current_user.id)
    task = session.exec(statement).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@router.put("/{id}", response_model=TaskRead)
def update_task(
    id: UUID,
    task_update: TaskUpdate,
    current_user: User = Depends(verify_authenticated_user),
    session: Session = Depends(get_session)
):
    """
    Update a specific task by ID.
    Verifies that the task belongs to the current user.
    """
    # Find the task that belongs to the current user
    statement = select(Task).where(Task.id == id).where(Task.user_id == current_user.id)
    task = session.exec(statement).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Update the task with the provided data
    for field, value in task_update.dict(exclude_unset=True).items():
        setattr(task, field, value)

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


@router.delete("/{id}")
def delete_task(
    id: UUID,
    current_user: User = Depends(verify_authenticated_user),
    session: Session = Depends(get_session)
):
    """
    Delete a specific task by ID.
    Verifies that the task belongs to the current user.
    """
    # Find the task that belongs to the current user
    statement = select(Task).where(Task.id == id).where(Task.user_id == current_user.id)
    task = session.exec(statement).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    session.delete(task)
    session.commit()

    return {"message": "Task deleted successfully"}


@router.patch("/{id}/complete", response_model=TaskRead)
def toggle_task_completion(
    id: UUID,
    current_user: User = Depends(verify_authenticated_user),
    session: Session = Depends(get_session)
):
    """
    Toggle the completion status of a specific task by ID.
    Verifies that the task belongs to the current user.
    """
    # Find the task that belongs to the current user
    statement = select(Task).where(Task.id == id).where(Task.user_id == current_user.id)
    task = session.exec(statement).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Toggle the completion status
    task.is_completed = not task.is_completed

    session.add(task)
    session.commit()
    session.refresh(task)

    return task