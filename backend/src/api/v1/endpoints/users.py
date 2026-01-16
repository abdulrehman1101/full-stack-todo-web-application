"""
Protected user endpoints for the todo application API.
This module provides endpoints that require authentication.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from ....database.session import get_session
from ....auth.middleware import verify_authenticated_user
from ....database.models.user import User
from ....auth.schemas import UserResponse, UserUpdateRequest

router = APIRouter()


@router.get("/me", response_model=UserResponse)
def get_current_user(
    current_user: User = Depends(verify_authenticated_user),
    session: Session = Depends(get_session)
) -> UserResponse:
    """
    Get the current authenticated user's information.

    Args:
        current_user: The authenticated user obtained from JWT token
        session: Database session

    Returns:
        UserResponse containing user information
    """
    return UserResponse.from_orm(current_user)


@router.put("/me", response_model=UserResponse)
def update_current_user(
    user_update: UserUpdateRequest,
    current_user: User = Depends(verify_authenticated_user),
    session: Session = Depends(get_session)
) -> UserResponse:
    """
    Update the current authenticated user's information.

    Args:
        user_update: Updated user information
        current_user: The authenticated user obtained from JWT token
        session: Database session

    Returns:
        UserResponse containing updated user information
    """
    # Update user fields if provided
    if user_update.name is not None:
        current_user.name = user_update.name
    if user_update.username is not None:
        current_user.username = user_update.username
    if user_update.email is not None:
        current_user.email = user_update.email

    # Commit changes to database
    session.add(current_user)
    session.commit()
    session.refresh(current_user)

    return UserResponse.from_orm(current_user)