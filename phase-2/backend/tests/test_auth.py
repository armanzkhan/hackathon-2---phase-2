"""
Integration tests for authentication endpoints.

Tests user signup, login, JWT token validation, and error cases.
"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session


class TestUserSignup:
    """Tests for user signup endpoint."""

    def test_signup_with_valid_credentials(self, client: TestClient):
        """T030: POST /api/auth/signup with valid email/password → 201 Created → returns user_id, email, token."""
        response = client.post(
            "/api/auth/signup",
            json={
                "email": "newuser@example.com",
                "password": "SecurePassword123",
            },
        )

        assert response.status_code == 201
        data = response.json()
        assert "user_id" in data
        assert "email" in data
        assert "token" in data
        assert data["email"] == "newuser@example.com"
        assert len(data["token"]) > 0  # JWT token should be present

    def test_signup_with_duplicate_email(self, client: TestClient):
        """T033: POST /api/auth/signup with existing email → 400 Bad Request."""
        # First signup
        client.post(
            "/api/auth/signup",
            json={
                "email": "duplicate@example.com",
                "password": "SecurePassword123",
            },
        )

        # Try to signup again with same email
        response = client.post(
            "/api/auth/signup",
            json={
                "email": "duplicate@example.com",
                "password": "AnotherPassword456",
            },
        )

        assert response.status_code == 400
        assert "email already registered" in response.json()["detail"].lower()


class TestUserLogin:
    """Tests for user login endpoint."""

    def test_login_with_correct_credentials(self, client: TestClient):
        """T031: POST /api/auth/login with correct credentials → 200 OK → returns token."""
        # First create a user
        client.post(
            "/api/auth/signup",
            json={
                "email": "loginuser@example.com",
                "password": "SecurePassword123",
            },
        )

        # Now login
        response = client.post(
            "/api/auth/login",
            json={
                "email": "loginuser@example.com",
                "password": "SecurePassword123",
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert "user_id" in data
        assert "email" in data
        assert "token" in data
        assert data["email"] == "loginuser@example.com"

    def test_login_with_wrong_password(self, client: TestClient):
        """T032: POST /api/auth/login with wrong password → 401 Unauthorized."""
        # First create a user
        client.post(
            "/api/auth/signup",
            json={
                "email": "wrongpass@example.com",
                "password": "CorrectPassword123",
            },
        )

        # Try to login with wrong password
        response = client.post(
            "/api/auth/login",
            json={
                "email": "wrongpass@example.com",
                "password": "WrongPassword456",
            },
        )

        assert response.status_code == 401
        assert "invalid" in response.json()["detail"].lower()


class TestJWTAuthentication:
    """Tests for JWT token validation."""

    def test_missing_jwt_token(self, client: TestClient):
        """T034: GET /api/{user_id}/tasks without Authorization header → 401 Unauthorized."""
        response = client.get("/api/user1/tasks")

        assert response.status_code == 401
        assert "missing" in response.json()["detail"].lower() or "unauthorized" in response.json()["detail"].lower()

    def test_invalid_jwt_token(self, client: TestClient):
        """T035: GET /api/{user_id}/tasks with malformed token → 401 Unauthorized."""
        response = client.get(
            "/api/user1/tasks",
            headers={"Authorization": "Bearer invalid-token-format"},
        )

        assert response.status_code == 401
        assert "invalid" in response.json()["detail"].lower() or "unauthorized" in response.json()["detail"].lower()

    def test_expired_jwt_token(self, client: TestClient, expired_auth_headers: dict):
        """T036: GET /api/{user_id}/tasks with expired token → 401 Unauthorized."""
        response = client.get(
            "/api/user1/tasks",
            headers=expired_auth_headers,
        )

        assert response.status_code == 401
        assert "expired" in response.json()["detail"].lower() or "unauthorized" in response.json()["detail"].lower()
