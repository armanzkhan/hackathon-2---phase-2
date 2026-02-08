"""
Tasks router.

Handles task CRUD endpoints with user isolation.
"""

from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from typing import List

from ..middleware import get_current_user
from ..middleware.auth import verify_user_id_match
from ..database import get_session
from ..services import get_user_tasks, create_task, update_task, get_task_with_ownership, delete_task
from ..schemas.task import TaskResponse, TaskCreateRequest, TaskUpdateRequest


router = APIRouter(prefix="/api", tags=["Tasks"])


@router.get("/{user_id}/tasks", response_model=List[TaskResponse])
async def get_tasks(
    user_id: str,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session),
    completed: bool | None = None,
):
    """
    Get all tasks for the authenticated user, optionally filtered by completion status.

    CRITICAL: Enforces user isolation - JWT user_id must match URL user_id.

    Query Parameters:
        completed: Optional filter - true for completed only, false for incomplete only, omit for all

    Returns:
        List of tasks belonging to the user, ordered by created_at descending
    """
    # Verify JWT user_id matches URL user_id (403 if mismatch)
    verify_user_id_match(user_id, current_user)

    # Fetch tasks from service layer with optional filter
    tasks = get_user_tasks(user_id, session, completed)

    return tasks


@router.post("/{user_id}/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task_endpoint(
    user_id: str,
    request: TaskCreateRequest,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """
    Create a new task for the authenticated user.

    CRITICAL: Enforces user isolation - JWT user_id must match URL user_id.

    Returns:
        Created task with id, user_id, and timestamps
    """
    # Verify JWT user_id matches URL user_id (403 if mismatch)
    verify_user_id_match(user_id, current_user)

    # Create task using service layer
    task = create_task(user_id, request.title, request.description, session)

    return task


@router.get("/{user_id}/tasks/{task_id}", response_model=TaskResponse)
async def get_task(
    user_id: str,
    task_id: int,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """
    Get a specific task for the authenticated user.

    CRITICAL: Enforces user isolation - JWT user_id must match URL user_id and task ownership.

    Returns:
        Task details
    """
    # Verify JWT user_id matches URL user_id (403 if mismatch)
    verify_user_id_match(user_id, current_user)

    # Get task with ownership verification
    task = get_task_with_ownership(task_id, user_id, session)

    return task


@router.put("/{user_id}/tasks/{task_id}", response_model=TaskResponse)
async def update_task_endpoint(
    user_id: str,
    task_id: int,
    request: TaskUpdateRequest,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """
    Update a task for the authenticated user.

    CRITICAL: Enforces user isolation - JWT user_id must match URL user_id and task ownership.

    Returns:
        Updated task
    """
    # Verify JWT user_id matches URL user_id (403 if mismatch)
    verify_user_id_match(user_id, current_user)

    # Update task using service layer
    task = update_task(
        task_id,
        user_id,
        request.title,
        request.description,
        request.completed,
        session,
    )

    return task


@router.delete("/{user_id}/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task_endpoint(
    user_id: str,
    task_id: int,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """
    Delete a task for the authenticated user.

    CRITICAL: Enforces user isolation - JWT user_id must match URL user_id and task ownership.

    Returns:
        204 No Content on successful deletion
    """
    # Verify JWT user_id matches URL user_id (403 if mismatch)
    verify_user_id_match(user_id, current_user)

    # Delete task using service layer
    delete_task(task_id, user_id, session)

    # Return 204 No Content (no response body)
    return
