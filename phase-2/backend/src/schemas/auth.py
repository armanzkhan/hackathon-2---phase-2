"""
Authentication request/response schemas.

Pydantic models for signup, login, and auth responses.
"""

from pydantic import BaseModel, EmailStr, Field


class SignupRequest(BaseModel):
    """User signup request."""

    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=8, description="User password (min 8 characters)")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "SecurePassword123",
            }
        }


class LoginRequest(BaseModel):
    """User login request."""

    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "SecurePassword123",
            }
        }


class AuthResponse(BaseModel):
    """Authentication response with JWT token."""

    user_id: str = Field(..., description="Unique user identifier")
    email: str = Field(..., description="User email address")
    token: str = Field(..., description="JWT authentication token")

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "550e8400-e29b-41d4-a716-446655440000",
                "email": "user@example.com",
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            }
        }
