"""
User model for authentication.

SQLModel class for user accounts managed by Better Auth.
"""

from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List


class User(SQLModel, table=True):
    """
    User account model.

    Attributes:
        id: Unique user identifier (UUID)
        email: User email address (unique)
        password_hash: Bcrypt hashed password
        created_at: Account creation timestamp
        updated_at: Last account update timestamp
    """

    id: Optional[str] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    password_hash: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    tasks: List["Task"] = Relationship(back_populates="user")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "email": "user@example.com",
                "created_at": "2026-02-08T10:00:00Z",
                "updated_at": "2026-02-08T10:00:00Z",
            }
        }
