"""
Task service layer.

Handles business logic for task CRUD operations with user isolation.
"""

from sqlmodel import Session, select
from typing import List

from ..models import Task


def get_user_tasks(user_id: str, session: Session, completed: bool | None = None) -> List[Task]:
    """
    Get all tasks for a specific user, optionally filtered by completion status.

    CRITICAL: Enforces user isolation by filtering on user_id.

    Args:
        user_id: The user ID to fetch tasks for
        session: Database session
        completed: Optional filter - True for completed only, False for incomplete only, None for all

    Returns:
        List of tasks belonging to the user, ordered by created_at descending
    """
    # Query tasks filtering by user_id
    statement = select(Task).where(Task.user_id == user_id)

    # Apply completion status filter if provided
    if completed is not None:
        statement = statement.where(Task.completed == completed)

    # Order by created_at desc
    statement = statement.order_by(Task.created_at.desc())

    tasks = session.exec(statement).all()
    return list(tasks)


def create_task(user_id: str, title: str, description: str | None, session: Session) -> Task:
    """
    Create a new task for a specific user.

    CRITICAL: Enforces user isolation by setting user_id from JWT.

    Args:
        user_id: The user ID from JWT token
        title: Task title (required, cannot be empty)
        description: Optional task description
        session: Database session

    Returns:
        Created task

    Raises:
        ValueError: If title is empty
    """
    from fastapi import HTTPException

    # Validate title is not empty
    if not title or title.strip() == "":
        raise HTTPException(status_code=400, detail="Title cannot be empty")

    # Create task with user_id from JWT
    task = Task(
        user_id=user_id,
        title=title.strip(),
        description=description.strip() if description else None,
        completed=False,
    )

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


def get_task_with_ownership(task_id: int, user_id: str, session: Session) -> Task:
    """
    Get a task by ID and verify ownership.

    CRITICAL: Enforces user isolation by verifying task belongs to user.

    Args:
        task_id: Task ID to fetch
        user_id: User ID from JWT token
        session: Database session

    Returns:
        Task if found and owned by user

    Raises:
        HTTPException 404: If task not found
        HTTPException 403: If task exists but belongs to another user
    """
    from fastapi import HTTPException

    # Get task by ID
    statement = select(Task).where(Task.id == task_id)
    task = session.exec(statement).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Verify ownership
    if task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Access denied: task belongs to another user")

    return task


def update_task(
    task_id: int,
    user_id: str,
    title: str | None,
    description: str | None,
    completed: bool | None,
    session: Session,
) -> Task:
    """
    Update a task.

    CRITICAL: Enforces user isolation by verifying ownership before update.

    Args:
        task_id: Task ID to update
        user_id: User ID from JWT token
        title: New title (optional)
        description: New description (optional)
        completed: New completion status (optional)
        session: Database session

    Returns:
        Updated task

    Raises:
        HTTPException 404: If task not found
        HTTPException 403: If task belongs to another user
        HTTPException 400: If title is empty
    """
    from fastapi import HTTPException
    from datetime import datetime

    # Get task and verify ownership
    task = get_task_with_ownership(task_id, user_id, session)

    # Validate title if provided
    if title is not None:
        if not title or title.strip() == "":
            raise HTTPException(status_code=400, detail="Title cannot be empty")
        task.title = title.strip()

    # Update description if provided
    if description is not None:
        task.description = description.strip() if description else None

    # Update completed status if provided
    if completed is not None:
        task.completed = completed

    # Update timestamp
    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


def delete_task(task_id: int, user_id: str, session: Session) -> None:
    """
    Delete a task.

    CRITICAL: Enforces user isolation by verifying ownership before deletion.

    Args:
        task_id: Task ID to delete
        user_id: User ID from JWT token
        session: Database session

    Raises:
        HTTPException 404: If task not found
        HTTPException 403: If task belongs to another user
    """
    # Get task and verify ownership
    task = get_task_with_ownership(task_id, user_id, session)

    # Delete task
    session.delete(task)
    session.commit()
