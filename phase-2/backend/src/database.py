"""
Database connection and initialization.

Provides SQLModel engine with connection pooling for PostgreSQL.
"""

from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.pool import QueuePool
from typing import Generator
from .config import settings


# Create database engine with connection pooling
engine = create_engine(
    settings.DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,  # Maximum connections in pool
    max_overflow=20,  # Additional connections if pool exhausted
    pool_timeout=30,  # Wait time for available connection (seconds)
    pool_recycle=3600,  # Recycle connections after 1 hour
    echo=settings.is_development,  # Log SQL queries in development
)


def init_db() -> None:
    """
    Initialize database by creating all tables.

    For development: uses SQLModel.metadata.create_all()
    For production: should use Alembic migrations instead
    """
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """
    Dependency to get database session.

    Yields:
        Session: SQLModel session for database operations

    Usage:
        @app.get("/endpoint")
        def endpoint(session: Session = Depends(get_session)):
            # Use session here
            pass
    """
    with Session(engine) as session:
        yield session
