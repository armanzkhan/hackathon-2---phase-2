"""
Pytest configuration and fixtures.

Provides test database, test client, and authentication helpers.
"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from typing import Generator
import jwt
from datetime import datetime, timedelta

from src.main import app
from src.database import get_session
from src.config import settings


# Test database engine (in-memory SQLite for speed)
@pytest.fixture(name="engine")
def engine_fixture():
    """Create in-memory SQLite engine for testing."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    return engine


@pytest.fixture(name="session")
def session_fixture(engine) -> Generator[Session, None, None]:
    """Create test database session."""
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session) -> Generator[TestClient, None, None]:
    """
    Create test client with dependency override for database session.

    The test client uses the test database session instead of the real database.
    """

    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


# Authentication helpers
def create_test_jwt_token(user_id: str, exp_minutes: int = 60) -> str:
    """
    Create a test JWT token for authentication.

    Args:
        user_id: User ID to include in token
        exp_minutes: Token expiration in minutes (default 60)

    Returns:
        JWT token string
    """
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(minutes=exp_minutes),
    }
    return jwt.encode(payload, settings.BETTER_AUTH_SECRET, algorithm="HS256")


def create_expired_jwt_token(user_id: str) -> str:
    """
    Create an expired JWT token for testing token expiration.

    Args:
        user_id: User ID to include in token

    Returns:
        Expired JWT token string
    """
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() - timedelta(minutes=1),  # Expired 1 minute ago
    }
    return jwt.encode(payload, settings.BETTER_AUTH_SECRET, algorithm="HS256")


@pytest.fixture(name="auth_headers_user1")
def auth_headers_user1_fixture() -> dict:
    """Create authentication headers for test user 1."""
    token = create_test_jwt_token("user1")
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(name="auth_headers_user2")
def auth_headers_user2_fixture() -> dict:
    """Create authentication headers for test user 2."""
    token = create_test_jwt_token("user2")
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(name="expired_auth_headers")
def expired_auth_headers_fixture() -> dict:
    """Create authentication headers with expired token."""
    token = create_expired_jwt_token("user1")
    return {"Authorization": f"Bearer {token}"}


# Sample data fixtures
@pytest.fixture(name="sample_user_data")
def sample_user_data_fixture() -> dict:
    """Sample user registration data."""
    return {
        "email": "test@example.com",
        "password": "SecurePassword123",
    }


@pytest.fixture(name="sample_task_data")
def sample_task_data_fixture() -> dict:
    """Sample task creation data."""
    return {
        "title": "Test Task",
        "description": "This is a test task description",
    }
