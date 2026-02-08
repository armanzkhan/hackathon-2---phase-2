"""
Task model for todo items.

SQLModel class for tasks with user isolation.
"""

from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional


class Task(SQLModel, table=True):
    """
    Task model representing a todo item.

    CRITICAL: All queries MUST filter by user_id for user isolation.

    Attributes:
        id: Unique task identifier (auto-increment)
        user_id: Owner user ID (foreign key, indexed)
        title: Task title (required)
        description: Optional task description
        completed: Completion status (default False)
        created_at: Task creation timestamp
        updated_at: Last modification timestamp
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id", index=True)
    title: str = Field(min_length=1, max_length=500)
    description: Optional[str] = Field(default=None, max_length=5000)
    completed: bool = Field(default=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: Optional["User"] = Relationship(back_populates="tasks")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": "550e8400-e29b-41d4-a716-446655440000",
                "title": "Complete project documentation",
                "description": "Write comprehensive API docs",
                "completed": False,
                "created_at": "2026-02-08T10:30:00Z",
                "updated_at": "2026-02-08T10:30:00Z",
            }
        }
