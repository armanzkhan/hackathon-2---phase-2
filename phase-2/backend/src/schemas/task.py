"""
Task request/response schemas.

Pydantic models for task CRUD operations.
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class TaskCreateRequest(BaseModel):
    """Create task request."""

    title: str = Field(..., min_length=1, max_length=500, description="Task title")
    description: Optional[str] = Field(None, max_length=5000, description="Optional task description")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Complete project documentation",
                "description": "Write comprehensive API docs",
            }
        }


class TaskUpdateRequest(BaseModel):
    """Update task request."""

    title: Optional[str] = Field(None, min_length=1, max_length=500, description="Updated task title")
    description: Optional[str] = Field(None, max_length=5000, description="Updated task description")
    completed: Optional[bool] = Field(None, description="Updated completion status")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Complete project documentation (updated)",
                "completed": True,
            }
        }


class TaskResponse(BaseModel):
    """Task response model."""

    id: int = Field(..., description="Task ID")
    user_id: str = Field(..., description="Owner user ID")
    title: str = Field(..., description="Task title")
    description: Optional[str] = Field(None, description="Task description")
    completed: bool = Field(..., description="Completion status")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True
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
